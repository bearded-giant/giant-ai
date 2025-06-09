-- Giant AI Neovim Integration
-- A focused plugin for Giant AI features with smart Avante integration

local M = {}

-- Plugin state
local config = {
  -- Commands
  ai_search_cmd = "ai-search-analyze",
  rag_search_cmd = "ai-search", 
  
  -- Defaults
  default_limit = 5,
  default_provider = "claude",
  
  -- UI preferences
  use_telescope = true,        -- Use Telescope for search input if available
  use_floating_windows = true, -- Floating windows for results
  auto_avante = true,         -- Auto-send analysis to Avante if available
  
  -- Keymaps (can be disabled)
  keymaps = {
    search_prompt = "<leader>rs",
    search_analyze = "<leader>ra", 
    search_word = "<leader>rw",
    search_word_analyze = "<leader>rW",
  }
}

-- State tracking
local state = {
  has_telescope = false,
  has_avante = false,
  project_root = nil,
}

-- Utility functions
local function notify(msg, level)
  vim.notify("[Giant AI] " .. msg, level or vim.log.levels.INFO)
end

local function execute_command(cmd)
  local handle = io.popen(cmd .. " 2>&1")
  if not handle then
    return nil, "Failed to execute command"
  end
  
  local result = handle:read("*all")
  local success = handle:close()
  
  if not success then
    return nil, "Command failed: " .. result
  end
  
  return result, nil
end

local function get_project_root()
  if state.project_root then
    return state.project_root
  end
  
  local cwd = vim.fn.getcwd()
  local git_root = vim.fn.system("git rev-parse --show-toplevel 2>/dev/null"):gsub("\n", "")
  
  if vim.v.shell_error == 0 and git_root ~= "" then
    state.project_root = git_root
  else
    state.project_root = cwd
  end
  
  return state.project_root
end

local function get_visual_selection()
  local start_pos = vim.fn.getpos("'<")
  local end_pos = vim.fn.getpos("'>")
  local lines = vim.api.nvim_buf_get_lines(0, start_pos[2]-1, end_pos[2], false)
  
  if #lines == 1 then
    return string.sub(lines[1], start_pos[3], end_pos[3])
  else
    return table.concat(lines, " ")
  end
end

-- Core functionality
local function create_result_buffer(content, title, filetype)
  local buf = vim.api.nvim_create_buf(false, true)
  local lines = vim.split(content, "\n")
  
  vim.api.nvim_buf_set_lines(buf, 0, -1, false, lines)
  vim.api.nvim_buf_set_option(buf, 'buftype', 'nofile')
  vim.api.nvim_buf_set_option(buf, 'filetype', filetype or 'markdown')
  vim.api.nvim_buf_set_option(buf, 'modifiable', false)
  vim.api.nvim_buf_set_name(buf, title)
  
  -- Keymaps for result buffer
  local opts = { buffer = buf, silent = true }
  vim.keymap.set('n', 'q', '<cmd>close<cr>', opts)
  vim.keymap.set('n', '<Esc>', '<cmd>close<cr>', opts)
  
  return buf
end

local function open_floating_window(buf, title)
  if not config.use_floating_windows then
    vim.cmd('vsplit')
    vim.api.nvim_win_set_buf(0, buf)
    return
  end
  
  local width = math.floor(vim.o.columns * 0.8)
  local height = math.floor(vim.o.lines * 0.8)
  local row = math.floor((vim.o.lines - height) / 2)
  local col = math.floor((vim.o.columns - width) / 2)
  
  local win = vim.api.nvim_open_win(buf, true, {
    relative = 'editor',
    width = width,
    height = height,
    row = row,
    col = col,
    style = 'minimal',
    border = 'rounded',
    title = title,
    title_pos = 'center',
  })
  
  return win
end

local function send_to_avante(content)
  if not state.has_avante then
    return false
  end
  
  local avante = require('avante')
  if avante and avante.ask then
    avante.ask(content)
    return true
  end
  
  return false
end

-- Main search functions
function M.rag_search(query, opts)
  opts = opts or {}
  local limit = opts.limit or config.default_limit
  local project_root = get_project_root()
  
  notify("Searching: " .. query)
  
  local cmd = string.format('%s "%s" "%s" %d text', 
    config.rag_search_cmd, query, project_root, limit)
  
  local result, err = execute_command(cmd)
  if err then
    notify("Search failed: " .. err, vim.log.levels.ERROR)
    return
  end
  
  local buf = create_result_buffer(result, "Giant AI Search: " .. query)
  open_floating_window(buf, "🔍 " .. query)
  
  notify("Search completed")
end

function M.rag_analyze(query, opts)
  opts = opts or {}
  local limit = opts.limit or config.default_limit  
  local provider = opts.provider or config.default_provider
  local project_root = get_project_root()
  
  notify("Analyzing with " .. provider .. ": " .. query)
  
  local cmd = string.format('%s "%s" "%s" --limit %d --analyze --provider %s', 
    config.ai_search_cmd, query, project_root, limit, provider)
  
  local result, err = execute_command(cmd)
  if err then
    notify("Analysis failed: " .. err, vim.log.levels.ERROR)
    return
  end
  
  -- Try to send to Avante first
  if config.auto_avante and send_to_avante(result) then
    notify("Analysis sent to Avante")
  else
    -- Fallback to buffer
    local buf = create_result_buffer(result, "Giant AI Analysis: " .. query)
    open_floating_window(buf, "🤖 " .. query)
    notify("Analysis complete (consider installing Avante for interactive AI)")
  end
end

-- Input handlers
local function search_prompt(analyze)
  if config.use_telescope and state.has_telescope then
    -- TODO: Implement telescope integration
    notify("Telescope integration coming soon")
  end
  
  -- Fallback to vim.ui.input
  vim.ui.input({ prompt = "Giant AI Search: " }, function(query)
    if not query or query == "" then
      return
    end
    
    if analyze then
      M.rag_analyze(query)
    else
      M.rag_search(query)
    end
  end)
end

function M.search_current_context(analyze)
  local mode = vim.api.nvim_get_mode().mode
  local query
  
  if mode == 'v' or mode == 'V' then
    query = get_visual_selection()
  else
    query = vim.fn.expand("<cword>")
  end
  
  if not query or query == "" then
    notify("No text to search", vim.log.levels.WARN)
    return
  end
  
  if analyze then
    M.rag_analyze(query)
  else
    M.rag_search(query)
  end
end

-- Commands
local function create_commands()
  vim.api.nvim_create_user_command('GiantAISearch', function(opts)
    if opts.args == "" then
      search_prompt(false)
    else
      M.rag_search(opts.args)
    end
  end, { nargs = '?', desc = 'Giant AI semantic search' })
  
  vim.api.nvim_create_user_command('GiantAIAnalyze', function(opts)
    if opts.args == "" then
      search_prompt(true)
    else
      M.rag_analyze(opts.args)
    end
  end, { nargs = '?', desc = 'Giant AI search with AI analysis' })
  
  vim.api.nvim_create_user_command('GiantAIStatus', function()
    local project_root = get_project_root()
    local status = {
      "# Giant AI Status",
      "",
      "**Project**: " .. project_root,
      "**Avante**: " .. (state.has_avante and "✅ Available" or "❌ Not found"),
      "**Telescope**: " .. (state.has_telescope and "✅ Available" or "❌ Not found"),
      "**Provider**: " .. config.default_provider,
      "",
      "**Commands**:",
      "- `:GiantAISearch [query]` - Semantic search",
      "- `:GiantAIAnalyze [query]` - Search + AI analysis", 
      "- `:GiantAIStatus` - Show this status",
    }
    
    local buf = create_result_buffer(table.concat(status, "\n"), "Giant AI Status")
    open_floating_window(buf, "📊 Giant AI Status")
  end, { desc = 'Giant AI status and info' })
end

-- Keymaps
local function create_keymaps()
  if not config.keymaps then
    return
  end
  
  local function map(mode, lhs, rhs, desc)
    if lhs and lhs ~= "" then
      vim.keymap.set(mode, lhs, rhs, { 
        noremap = true, 
        silent = true, 
        desc = "Giant AI: " .. desc 
      })
    end
  end
  
  map('n', config.keymaps.search_prompt, function() search_prompt(false) end, "Search")
  map('n', config.keymaps.search_analyze, function() search_prompt(true) end, "Search + Analyze")
  map('n', config.keymaps.search_word, function() M.search_current_context(false) end, "Search word")
  map('n', config.keymaps.search_word_analyze, function() M.search_current_context(true) end, "Search word + Analyze")
  
  -- Visual mode
  map('v', config.keymaps.search_prompt, function() M.search_current_context(false) end, "Search selection")
  map('v', config.keymaps.search_analyze, function() M.search_current_context(true) end, "Search selection + Analyze")
end

-- Setup function
function M.setup(opts)
  opts = opts or {}
  
  -- Merge config
  config = vim.tbl_deep_extend("force", config, opts)
  
  -- Detect integrations
  state.has_telescope = pcall(require, 'telescope')
  state.has_avante = pcall(require, 'avante')
  
  -- Create commands and keymaps
  create_commands()
  create_keymaps()
  
  -- Status notification
  local integrations = {}
  if state.has_avante then table.insert(integrations, "Avante") end
  if state.has_telescope then table.insert(integrations, "Telescope") end
  
  local integration_str = #integrations > 0 and 
    " (integrated with " .. table.concat(integrations, ", ") .. ")" or ""
  
  notify("Plugin loaded" .. integration_str)
end

return M
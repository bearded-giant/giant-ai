-- Giant AI RAG + Avante Integration for Neovim
-- Place this in your Neovim config or load it from Giant AI setup

local M = {}

-- Configuration
local config = {
  ai_search_cmd = "ai-search-analyze",  -- Command for AI-enhanced search
  rag_search_cmd = "ai-search",         -- Command for raw RAG search
  default_limit = 5,                    -- Default number of search results
  default_provider = "claude",          -- Default AI provider for analysis
}

-- Execute shell command and return output
local function execute_command(cmd)
  local handle = io.popen(cmd)
  if not handle then
    return nil, "Failed to execute command"
  end
  
  local result = handle:read("*all")
  local success = handle:close()
  
  if not success then
    return nil, "Command failed"
  end
  
  return result, nil
end

-- Get current project root (look for git repo or use cwd)
local function get_project_root()
  local cwd = vim.fn.getcwd()
  
  -- Try to find git root
  local git_root = vim.fn.system("git rev-parse --show-toplevel 2>/dev/null"):gsub("\n", "")
  if vim.v.shell_error == 0 and git_root ~= "" then
    return git_root
  end
  
  return cwd
end

-- RAG search with raw results (existing behavior)
function M.rag_search_raw(query, limit)
  limit = limit or config.default_limit
  local project_root = get_project_root()
  
  local cmd = string.format('%s "%s" "%s" %d text', 
    config.rag_search_cmd, query, project_root, limit)
  
  local result, err = execute_command(cmd)
  if err then
    vim.notify("RAG search failed: " .. err, vim.log.levels.ERROR)
    return
  end
  
  -- Display results in new buffer
  local buf = vim.api.nvim_create_buf(false, true)
  local lines = vim.split(result, "\n")
  vim.api.nvim_buf_set_lines(buf, 0, -1, false, lines)
  vim.api.nvim_buf_set_option(buf, 'buftype', 'nofile')
  vim.api.nvim_buf_set_option(buf, 'filetype', 'markdown')
  vim.api.nvim_buf_set_name(buf, "RAG Search: " .. query)
  
  -- Open in split
  vim.cmd('split')
  vim.api.nvim_win_set_buf(0, buf)
  
  vim.notify(string.format("RAG search completed: %d results", #lines - 3))
end

-- RAG search with AI analysis (new enhanced behavior)
function M.rag_search_analyze(query, limit, provider)
  limit = limit or config.default_limit
  provider = provider or config.default_provider
  local project_root = get_project_root()
  
  vim.notify("Searching and analyzing with " .. provider .. "...", vim.log.levels.INFO)
  
  local cmd = string.format('%s "%s" "%s" --limit %d --analyze --provider %s', 
    config.ai_search_cmd, query, project_root, limit, provider)
  
  local result, err = execute_command(cmd)
  if err then
    vim.notify("RAG analysis failed: " .. err, vim.log.levels.ERROR)
    return
  end
  
  -- Check if Avante is available and use it, otherwise create buffer
  local has_avante = pcall(require, 'avante')
  
  if has_avante then
    -- Send to Avante for interactive analysis
    local avante = require('avante')
    if avante.ask then
      avante.ask(result)
    else
      -- Fallback: create buffer and suggest copying to Avante
      M.create_analysis_buffer(result, query, "Copy this analysis to Avante for further interaction")
    end
  else
    -- Create buffer with analysis
    M.create_analysis_buffer(result, query, "Install Avante.nvim for interactive AI analysis")
  end
end

-- Create buffer with analysis results
function M.create_analysis_buffer(content, query, footer_note)
  local buf = vim.api.nvim_create_buf(false, true)
  
  local lines = vim.split(content, "\n")
  if footer_note then
    table.insert(lines, "")
    table.insert(lines, "---")
    table.insert(lines, "💡 " .. footer_note)
  end
  
  vim.api.nvim_buf_set_lines(buf, 0, -1, false, lines)
  vim.api.nvim_buf_set_option(buf, 'buftype', 'nofile')
  vim.api.nvim_buf_set_option(buf, 'filetype', 'markdown')
  vim.api.nvim_buf_set_name(buf, "AI Analysis: " .. query)
  
  -- Open in split
  vim.cmd('vsplit')
  vim.api.nvim_win_set_buf(0, buf)
  
  vim.notify("AI analysis completed", vim.log.levels.INFO)
end

-- Interactive search with input
function M.interactive_search(analyze)
  vim.ui.input({ prompt = "Search query: " }, function(query)
    if not query or query == "" then
      return
    end
    
    if analyze then
      M.rag_search_analyze(query)
    else
      M.rag_search_raw(query)
    end
  end)
end

-- Search current word/selection
function M.search_current_word(analyze)
  local mode = vim.api.nvim_get_mode().mode
  local query
  
  if mode == 'v' or mode == 'V' then
    -- Visual mode: get selected text
    local start_pos = vim.fn.getpos("'<")
    local end_pos = vim.fn.getpos("'>")
    local lines = vim.api.nvim_buf_get_lines(0, start_pos[2]-1, end_pos[2], false)
    if #lines == 1 then
      query = string.sub(lines[1], start_pos[3], end_pos[3])
    else
      query = table.concat(lines, " ")
    end
  else
    -- Normal mode: get word under cursor
    query = vim.fn.expand("<cword>")
  end
  
  if not query or query == "" then
    vim.notify("No text to search", vim.log.levels.WARN)
    return
  end
  
  if analyze then
    M.rag_search_analyze(query)
  else
    M.rag_search_raw(query)
  end
end

-- Setup key mappings
function M.setup(opts)
  opts = opts or {}
  
  -- Merge user config
  config = vim.tbl_deep_extend("force", config, opts)
  
  -- Key mappings
  local keymap_opts = { noremap = true, silent = true, desc = "Giant AI RAG" }
  
  -- <leader>rs - RAG search raw results
  vim.keymap.set('n', '<leader>rs', function()
    M.interactive_search(false)
  end, vim.tbl_extend("force", keymap_opts, { desc = "RAG search (raw)" }))
  
  -- <leader>ra - RAG search with AI analysis
  vim.keymap.set('n', '<leader>ra', function()
    M.interactive_search(true)
  end, vim.tbl_extend("force", keymap_opts, { desc = "RAG search + AI analysis" }))
  
  -- <leader>rw - Search word under cursor (raw)
  vim.keymap.set('n', '<leader>rw', function()
    M.search_current_word(false)
  end, vim.tbl_extend("force", keymap_opts, { desc = "RAG search word (raw)" }))
  
  -- <leader>rW - Search word under cursor with AI analysis
  vim.keymap.set('n', '<leader>rW', function()
    M.search_current_word(true)
  end, vim.tbl_extend("force", keymap_opts, { desc = "RAG search word + AI analysis" }))
  
  -- Visual mode search
  vim.keymap.set('v', '<leader>rs', function()
    M.search_current_word(false)
  end, vim.tbl_extend("force", keymap_opts, { desc = "RAG search selection (raw)" }))
  
  vim.keymap.set('v', '<leader>ra', function()
    M.search_current_word(true)
  end, vim.tbl_extend("force", keymap_opts, { desc = "RAG search selection + AI analysis" }))
  
  vim.notify("Giant AI RAG integration loaded", vim.log.levels.INFO)
end

return M
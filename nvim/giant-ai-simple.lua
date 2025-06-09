-- Giant AI Neovim Integration - Simple & Effective
-- Focuses on what actually works: getting useful results to the user

local M = {}

-- Simple config - just what matters
local config = {
  provider = "claude",
  limit = 5,
  -- Keymaps  
  search_raw = "<leader>rs",
  search_analyze = "<leader>ra",
}

local function notify(msg, level)
  vim.notify("[Giant AI] " .. msg, level or vim.log.levels.INFO)
end

local function get_project_root()
  local git_root = vim.fn.system("git rev-parse --show-toplevel 2>/dev/null"):gsub("\n", "")
  if vim.v.shell_error == 0 and git_root ~= "" then
    return git_root
  end
  return vim.fn.getcwd()
end

local function has_giant_ai_config(project_root)
  -- Check if .giant-ai directory exists (project is initialized)
  local giant_ai_dir = project_root .. "/.giant-ai"
  return vim.fn.isdirectory(giant_ai_dir) == 1
end

local function is_project_indexed(project_root)
  -- First check if project has .giant-ai (is initialized)
  if not has_giant_ai_config(project_root) then
    return false
  end
  
  -- Quick check if project is indexed by testing ai-search
  local cmd = string.format('ai-search "test" "%s" 1 json 2>/dev/null', project_root)
  local result = vim.fn.system(cmd)
  
  -- Parse the JSON result
  local success, parsed = pcall(vim.fn.json_decode, result)
  if not success or not parsed then
    return false
  end
  
  -- Check for explicit error about not being indexed
  if parsed.error and parsed.error == "Project not indexed" then
    return false
  end
  
  -- If no error, assume indexed (whether it has results or not)
  return not parsed.error
end

local function get_selection_or_word()
  local mode = vim.api.nvim_get_mode().mode
  if mode == 'v' or mode == 'V' then
    local start_pos = vim.fn.getpos("'<")
    local end_pos = vim.fn.getpos("'>")
    local lines = vim.api.nvim_buf_get_lines(0, start_pos[2]-1, end_pos[2], false)
    if #lines == 1 then
      return string.sub(lines[1], start_pos[3], end_pos[3])
    else
      return table.concat(lines, " ")
    end
  else
    return vim.fn.expand("<cword>")
  end
end

-- The core functions that actually work
function M.rag_search_raw(query)
  if not query or query == "" then
    vim.ui.input({ prompt = "Search: " }, function(input)
      if input then M.rag_search_raw(input) end
    end)
    return
  end
  
  local project_root = get_project_root()
  
  -- Check if project is initialized and indexed
  if not has_giant_ai_config(project_root) then
    notify("Project not initialized. Run 'ai-init-project-smart' to enable Giant AI", vim.log.levels.WARN)
    return
  end
  
  if not is_project_indexed(project_root) then
    notify("Project not indexed. Run 'ai-rag index .' to enable semantic search", vim.log.levels.WARN)
    return
  end
  
  notify("Searching...")
  
  local cmd = string.format('ai-search "%s" "%s" %d text', query, project_root, config.limit)
  
  vim.fn.jobstart(cmd, {
    stdout_buffered = true,
    on_stdout = function(_, data)
      if data and #data > 0 then
        local result = table.concat(data, "\n")
        if result:match("%S") then
          -- Copy to clipboard instead of buffer hell
          vim.fn.setreg('+', result)
          notify("✅ Results copied to clipboard (" .. #vim.split(result, "\n") .. " lines)")
          
          -- Show brief summary
          local lines = vim.split(result, "\n")
          local files = {}
          for _, line in ipairs(lines) do
            local file = line:match("(%S+%.%w+)")
            if file and not files[file] then
              files[file] = true
            end
          end
          
          local file_list = {}
          for file in pairs(files) do
            table.insert(file_list, file)
          end
          
          if #file_list > 0 then
            notify("📁 Found in: " .. table.concat(file_list, ", "))
          end
        else
          notify("❌ No results found")
        end
      end
    end,
    on_stderr = function(_, data)
      if data and #data > 0 then
        notify("❌ Error: " .. table.concat(data, " "), vim.log.levels.ERROR)
      end
    end,
  })
end

function M.rag_analyze(query)
  if not query or query == "" then
    vim.ui.input({ prompt = "Analyze: " }, function(input)
      if input then M.rag_analyze(input) end
    end)
    return
  end
  
  local project_root = get_project_root()
  
  -- Check if project is initialized and indexed
  if not has_giant_ai_config(project_root) then
    notify("Project not initialized. Run 'ai-init-project-smart' to enable Giant AI", vim.log.levels.WARN)
    return
  end
  
  if not is_project_indexed(project_root) then
    notify("Project not indexed. Run 'ai-rag index .' to enable semantic search", vim.log.levels.WARN)
    return
  end
  
  notify("Analyzing with " .. config.provider .. "... (10-30s)")
  
  local cmd = string.format('ai-search-pipe "%s" "%s" %d %s', 
    query, project_root, config.limit, config.provider)
  
  vim.fn.jobstart(cmd, {
    stdout_buffered = true,
    on_stdout = function(_, data)
      if data and #data > 0 then
        local result = table.concat(data, "\n")
        if result:match("%S") then
          -- Try Avante first
          local has_avante, avante = pcall(require, 'avante')
          if has_avante and avante.ask then
            avante.ask(result)
            notify("✅ Analysis sent to Avante")
          else
            -- Fallback: copy to clipboard and show notification
            vim.fn.setreg('+', result)
            notify("✅ Analysis copied to clipboard - open your AI tool and paste")
            
            -- Also show first few lines as preview
            local lines = vim.split(result, "\n")
            local preview = {}
            for i = 1, math.min(5, #lines) do
              if lines[i]:match("%S") then
                table.insert(preview, lines[i])
              end
            end
            if #preview > 0 then
              print("\n" .. table.concat(preview, "\n") .. "\n(Full analysis in clipboard)")
            end
          end
        else
          notify("❌ No analysis generated")
        end
      end
    end,
    on_stderr = function(_, data)
      if data and #data > 0 then
        local error_msg = table.concat(data, " ")
        notify("❌ Error: " .. error_msg, vim.log.levels.ERROR)
        
        -- If ai-search-analyze doesn't exist, fallback to raw search
        if error_msg:match("command not found") or error_msg:match("No such file") then
          notify("⚠️  ai-search-analyze not found, falling back to raw search")
          M.rag_search_raw(query)
        end
      end
    end,
  })
end

-- Convenience functions
function M.search_word_raw()
  local word = get_selection_or_word()
  if word and word ~= "" then
    M.rag_search_raw(word)
  else
    notify("No word under cursor")
  end
end

function M.analyze_word()
  local word = get_selection_or_word()
  if word and word ~= "" then
    M.rag_analyze(word)
  else
    notify("No word under cursor")
  end
end

-- Status check
function M.status()
  local project_root = get_project_root()
  local has_avante = pcall(require, 'avante')
  local has_config = has_giant_ai_config(project_root)
  local indexed = is_project_indexed(project_root)
  
  local status_lines = {
    "Giant AI Status:",
    "  Project: " .. project_root,
    "  Initialized: " .. (has_config and "Yes" or "No"),
    "  Indexed: " .. (indexed and "Yes" or "No"),
    "  Provider: " .. config.provider,
    "  Avante: " .. (has_avante and "Yes" or "No"),
    "",
    "Commands:",
    "  :GiantAISearch [query] - Raw search" .. (indexed and "" or " (requires setup)"),
    "  :GiantAIAnalyze [query] - AI analysis" .. (indexed and "" or " (requires setup)"),
    "  :GiantAIStatus - This status",
    "",
    "Keymaps:",
    "  " .. config.search_raw .. " - Search prompt",
    "  " .. config.search_analyze .. " - Analyze prompt",
  }
  
  if not has_config then
    table.insert(status_lines, "")
    table.insert(status_lines, "To enable Giant AI:")
    table.insert(status_lines, "  1. Run: ai-init-project-smart")
    table.insert(status_lines, "  2. Run: ai-rag index .")
  elseif not indexed then
    table.insert(status_lines, "")
    table.insert(status_lines, "To enable semantic search:")
    table.insert(status_lines, "  Run: ai-rag index .")
  end
  
  print(table.concat(status_lines, "\n"))
end

-- Setup
function M.setup(opts)
  opts = opts or {}
  config = vim.tbl_extend("force", config, opts)
  
  -- Commands
  vim.api.nvim_create_user_command('GiantAISearch', function(cmd_opts)
    if cmd_opts.args == "" then
      M.rag_search_raw()
    else
      M.rag_search_raw(cmd_opts.args)
    end
  end, { nargs = '?', desc = 'Giant AI search' })
  
  vim.api.nvim_create_user_command('GiantAIAnalyze', function(cmd_opts)
    if cmd_opts.args == "" then
      M.rag_analyze()
    else
      M.rag_analyze(cmd_opts.args)
    end
  end, { nargs = '?', desc = 'Giant AI analyze' })
  
  vim.api.nvim_create_user_command('GiantAIStatus', M.status, { desc = 'Giant AI status' })
  
  -- Keymaps
  if config.search_raw then
    vim.keymap.set({'n', 'v'}, config.search_raw, function()
      local word = get_selection_or_word()
      if word and word ~= "" then
        M.rag_search_raw(word)
      else
        M.rag_search_raw()
      end
    end, { desc = "Giant AI search" })
  end
  
  if config.search_analyze then
    vim.keymap.set({'n', 'v'}, config.search_analyze, function()
      local word = get_selection_or_word()
      if word and word ~= "" then
        M.rag_analyze(word)
      else
        M.rag_analyze()
      end
    end, { desc = "Giant AI analyze" })
  end
  
  -- Check project status and show appropriate message
  local project_root = get_project_root()
  local has_config = has_giant_ai_config(project_root)
  local indexed = is_project_indexed(project_root)
  
  if indexed then
    notify("Ready! Use " .. config.search_analyze .. " for AI analysis")
  elseif has_config then
    notify("Ready! Run 'ai-rag index .' to enable semantic search")
  else
    notify("Ready! Run 'ai-init-project-smart' to enable Giant AI features")
  end
end

return M
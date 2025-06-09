# RAG + AI Analysis Workflow Guide

## Problem Solved

Previously, RAG search returned raw code chunks that weren't useful on their own. Now you have multiple options for making search results actionable with AI analysis.

## Available Tools

### 1. **Enhanced Command Line Search**

```bash
# Raw search (original behavior)
ai-search "caching strategies"

# NEW: Search + AI analysis 
ai-search-analyze "caching strategies" --analyze

# With options
ai-search-analyze "authentication" --analyze --limit 3 --provider claude
```

### 2. **Neovim Integration** 

Add to your Neovim config:
```lua
-- Load Giant AI RAG integration
local rag = require('path/to/giant-ai/nvim/rag-avante-integration')
rag.setup({
  default_provider = "claude",  -- or "openai" when available
  default_limit = 5,
})
```

**Key Bindings:**
```vim
<leader>rs   " RAG search - raw results in buffer
<leader>ra   " RAG search + AI analysis (auto-sends to Avante if available)
<leader>rw   " Search word under cursor (raw)
<leader>rW   " Search word under cursor + AI analysis

" Visual mode
<leader>rs   " Search selected text (raw)  
<leader>ra   " Search selected text + AI analysis
```

## Workflow Examples

### Terminal Workflow

```bash
# 1. Quick raw search for reference
ai-search "error handling patterns" . 3

# 2. Deep analysis with AI
ai-search-analyze "error handling patterns" --analyze
# Returns: Analyzed patterns, consistency review, recommendations
```

### Neovim + Avante Workflow

```vim
" 1. Place cursor on interesting code/concept
" 2. Press <leader>rW  
" → Searches for similar patterns
" → Automatically analyzes with AI
" → Opens results in Avante for interaction

" 3. Ask follow-up questions in Avante:
"   - "How consistent are these patterns?"
"   - "What's the best approach here?"  
"   - "Are there any security issues?"
```

### Manual Integration Workflow

```bash
# Pipe raw search to your AI tool
ai-search "database connection patterns" | claude "Analyze these patterns"

# Or save and analyze
ai-search "auth middleware" > patterns.md
claude --file patterns.md "Review these auth patterns for security"
```

## What the AI Analysis Provides

The AI analysis includes:

1. **Pattern Summary** - What approaches were found
2. **Consistency Analysis** - How well implementations align  
3. **Quality Assessment** - Code quality and best practices
4. **Gap Identification** - Missing patterns or inconsistencies
5. **Recommendations** - Specific improvement suggestions
6. **Relevance Ranking** - Most useful code sections highlighted

## Example: Before vs After

### Before (Raw Search)
```
Search results for 'caching strategies':
==================================================

1. services/cache.js
   Lines: 23-45
   Type: function_definition  
   Distance: 0.2341
   Preview: function setupCache(options) {
     const redis = new Redis(options.redis);
     const memoryCache = new MemoryCache({
       max: options.memory.maxItems || 1000,
       ttl: options.memory.ttl || 3600000
     });...

2. utils/cache-wrapper.js
   Lines: 12-34
   Type: function_definition
   Distance: 0.2876  
   Preview: class CacheWrapper {
     constructor(cacheProvider, defaultTTL = 300) {
       this.cache = cacheProvider;
       this.defaultTTL = defaultTTL;
     }...
```

### After (AI Analysis)
```
# Caching Strategy Analysis

Based on your search for "caching strategies", I found 2 distinct approaches in your codebase:

## Patterns Found

1. **Multi-layer Caching** (services/cache.js)
   - Uses Redis + in-memory cache combination
   - Good: Fallback strategy, configurable TTL
   - Distance: 76.6% relevance

2. **Cache Wrapper Pattern** (utils/cache-wrapper.js)  
   - Provider-agnostic abstraction layer
   - Good: Clean interface, testable design
   - Distance: 71.2% relevance

## Analysis

**Consistency**: Both use similar TTL patterns  
**Quality**: No error handling in wrapper class
**Architecture**: Good separation of concerns

## Recommendations

1. **Standardize error handling** - Add try/catch in CacheWrapper
2. **Consider cache invalidation** - No invalidation strategy found
3. **Add monitoring** - Cache hit/miss metrics missing
4. **Use wrapper pattern** - Migrate setupCache to use CacheWrapper

## Most Relevant Code
The CacheWrapper pattern (utils/cache-wrapper.js) is your best foundation for standardizing caching across the application.
```

## Setup Instructions

### 1. Install the Enhanced Tools
```bash
# Re-run setup to get new ai-search-analyze command
./scripts/ai-setup
```

### 2. Test Enhanced Search
```bash
# Test basic search (should work as before)
ai-search "function" . 3

# Test new AI analysis
ai-search-analyze "authentication" --analyze --limit 3
```

### 3. Configure Neovim (Optional)
```lua
-- Add to your init.lua or plugin config
local giant_ai_path = "/path/to/giant-ai"
package.path = package.path .. ";" .. giant_ai_path .. "/nvim/?.lua"

local rag = require('rag-avante-integration')
rag.setup({
  default_provider = "claude",  -- Your AI CLI tool
  default_limit = 5,
})
```

### 4. Verify Integration
```vim
" In Neovim, test the keybindings:
:lua vim.notify("Testing RAG integration")

" Try searching:
<leader>ra
" Enter query: "error handling"  
" Should show AI analysis
```

## Troubleshooting

### "ai-search-analyze: command not found"
```bash
# Re-run setup script
./scripts/ai-setup

# Verify PATH includes ~/.local/bin
echo $PATH | grep ".local/bin"

# Check if command exists
which ai-search-analyze
```

### "AI provider failed"
```bash
# Test your AI CLI directly
claude "test message"

# Check provider name
ai-search-analyze "test" --analyze --provider claude
```

### Neovim integration not working
```lua
-- Check if Giant AI path is correct
:lua print(package.path)

-- Test manual function call
:lua require('rag-avante-integration').rag_search_analyze("test")
```

### No Avante integration
- Install Avante.nvim if you want interactive AI analysis
- Without Avante, results will open in a buffer (still useful!)
- You can copy analysis results to any AI tool

## Next Steps

1. **Try the enhanced search** on your current project
2. **Set up Neovim integration** if you use Neovim
3. **Experiment with different providers** (when OpenAI CLI becomes available)
4. **Integrate into your workflow** - replace manual code searches with semantic analysis

The goal is to make RAG search results **actionable** rather than just informational!
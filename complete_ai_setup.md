# Complete AI Development Setup

A comprehensive AI-powered development environment that rivals Cursor IDE while maintaining the flexibility and power of Neovim.

## 🚀 Quick Start (TLDR)

```bash
# 1. One-time setup (installs everything: CLI tools, MCP servers, Neovim config)
./scripts/ai-setup

# 2. Per-project setup (auto-detects language/framework/conventions)
ai-init-project-smart                # Smart auto-detection  
ai-init-project-smart --clean        # Fresh install, overwrites existing

# 3. Index for semantic search
ai-rag index .

# 4. Use AI in multiple ways:
claude                               # Enhanced terminal AI with project context
# OR in Neovim:
<leader>cc                          # Terminal AI with project context
<leader>ca                          # Avante AI chat in editor
<leader>rs                          # Semantic code search
```

**What each does:**
- `ai-setup`: One-time install of CLI tools, MCP servers, and optional Neovim integration
- `ai-init-project-smart`: Auto-detects your project and creates intelligent `.ai-setup/` config  
- `ai-rag index`: Creates searchable index of your codebase
- `<leader>cc`: AI CLI with full project context and RAG integration
- `<leader>ca`: Avante AI interface with MCP tools and RAG search
- `<leader>rs`: Direct semantic search of your codebase

## Overview

This setup transforms your development workflow with:
- **Semantic Code Search (RAG)** - Find code by meaning, not keywords
- **Model Context Protocol (MCP)** - Enhanced AI context and tools
- **Neovim AI Integration** - Multiple AI providers in your editor
- **Project-Aware AI** - Context that understands your architecture
- **Template Generation** - Smart POC and boilerplate creation

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Neovim IDE    │    │   AI CLI Tool   │    │   RAG System    │
│                 │    │                 │    │                 │
│ • Avante.nvim   │◄──►│ • CLI Tool      │◄──►│ • Chunked Index │
│ • Codeium       │    │ • Project Root  │    │ • Semantic Search│
│ • MCP Tools     │    │ • Git Aware     │    │ • ChromaDB      │
│ • Treesitter    │    │ • Context Load  │    │ • Local Storage │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  MCP Servers    │
                    │                 │
                    │ • Project Tools │
                    │ • Architecture  │
                    │ • Templates     │
                    │ • Context       │
                    └─────────────────┘
```

## Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 18+** with npm  
- **AI CLI Tool** - Install via: `npm install -g @anthropic/claude-code` (or equivalent AI CLI)
- **Claude Desktop** (optional, for desktop app MCP integration)
- **Neovim** (optional, for IDE integration)

### One-Time Installation
```bash
# 1. Clone the giant-ai-dev setup
git clone <giant-ai-dev-repo>
cd giant-ai-dev

# 2. Run global setup
./scripts/ai-setup
```

This script automatically:
- ✅ Installs Python dependencies for RAG (sentence-transformers, chromadb, tree-sitter)
- ✅ Installs Node.js dependencies for MCP servers
- ✅ Creates CLI symlinks in `~/.local/bin/`
- ✅ Configures MCP hub with global servers
- ✅ Sets up RAG database directory
- ✅ Configures Claude Desktop MCP integration
- ✅ Sets up AI CLI global context

### Add to PATH
```bash
# Add to your .bashrc/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### Per-Project Setup
```bash
# Navigate to any project
cd your-project

# Initialize AI configuration (smart auto-detection)
ai-init-project

# Clean install - fresh configuration files (overwrites existing)
ai-init-project --clean
```

**Smart Initialization** automatically detects and configures:
- **Language**: JavaScript/TypeScript, Python, Rust, Go, Java
- **Framework**: React/Next.js, Express, Django/FastAPI/Flask, etc.
- **Conventions**: File naming, indentation, quote style from existing code
- **Project Structure**: Components, routes, testing patterns

This creates **intelligent, pre-filled** configuration:
```
your-project/
├── .ai-setup/
│   ├── context.md       # Auto-generated project analysis & AI instructions
│   └── conventions.yml  # Auto-detected coding standards from codebase
└── .gitignore          # Updated with AI entries
```

**Example Smart Detection:**
```bash
🔍 Analyzing project...
✅ Detected: javascript (nextjs)

Detected Configuration:
• Language: javascript
• Framework: nextjs
• File naming: kebab-case
• Indentation: spaces (2)
```

### Index for Search
```bash
# Index current project for semantic search
ai-rag index .

# Verify indexing
ai-rag list-projects
```

### Neovim Integration (Optional)
Add to your Neovim config:
```lua
-- Load the enhanced AI plugins
require("config.ai-keymaps")
require("config.mcp-autocmds") 
require("config.claude-status")
```

## 📁 Directory Structure & Storage

### Giant AI Dev Setup
```
giant-ai-dev/                    # Standalone AI development toolkit
├── rag/
│   ├── db/                    # ChromaDB storage for all projects
│   │   ├── project_abc123/    # Hashed project path
│   │   │   ├── chroma.sqlite3 # Vector embeddings
│   │   │   └── index.json     # Project metadata
│   │   └── project_def456/    # Another project
│   ├── indexer.py            # RAG indexing script
│   ├── search.py            # Search interface
│   └── requirements.txt     # Python dependencies
├── mcp/
│   ├── project-server.js    # Global MCP tools
│   ├── package.json
│   └── node_modules/
├── scripts/
│   ├── ai-setup        # One-time setup script
│   └── ai-init-project # Per-project initialization
├── templates/              # POC templates
├── prompts/               # AI prompts
└── settings.local.json    # Local configuration

~/.local/bin/              # CLI tools (symlinked by setup)
├── ai-rag            # → giant-ai-dev/rag/indexer.py
├── ai-search        # → giant-ai-dev/rag/search.py
├── ai-setup         # → giant-ai-dev/scripts/ai-setup
└── ai-init-project  # → giant-ai-dev/scripts/ai-init-project

~/.ai-setup/                # AI setup runtime (managed separately)
├── CLAUDE.md@           # → dotfiles/claude-code/.ai-setup/CLAUDE.md (stowed)
├── projects/            # AI project sessions
├── todos/              # AI todo management
└── statsig/            # AI analytics

~/.config/mcp-hub/
└── config.json         # MCP server configuration

~/.config/claude-desktop/
└── claude_desktop_config.json  # Claude Desktop MCP config
```

### Per-Project Structure
```
your-project/
├── .ai-setup/
│   ├── context.md           # Project-specific AI context
│   ├── conventions.yml      # Coding standards
│   └── mcp/                # Optional project MCP server
│       └── server.js
├── .gitignore              # Updated to exclude .ai-setup/rag/db/
└── [your project files]
```

### RAG Storage Details

**Project-Specific Collections:**
Each project gets its own ChromaDB collection stored in `~/.ai-setup/rag/db/`:

```python
# Collection naming
project_id = Path(project_path).name.replace(" ", "_").replace("/", "_")
collection_name = f"codebase_{project_id}"

# Storage location
giant-ai-dev/rag/db/
├── chroma.sqlite3           # ChromaDB database file
└── [hash-based-folders]/    # Project-specific vector storage
```

**Chunking Strategy:**
- **Python files**: Tree-sitter parsing for functions/classes
- **Other files**: Line-based chunking (50 lines default)
- **File size limit**: 10MB max per file
- **Exclusions**: node_modules, .git, build dirs, etc.

**Search Commands:**
```bash
# Index current project
ai-rag index .

# Index with custom settings
ai-rag index . --batch-size 100 --chunk-size 30 --max-file-size 20

# Search current project
ai-search "authentication middleware"

# Search specific project
ai-rag search "error handling" /path/to/project --limit 5

# List all indexed projects
ai-rag list-projects
```

## RAG System - Semantic Code Search

### Chunked Indexing & Storage
The RAG system uses intelligent chunking and stores indexes per-project:

```python
# Automatic chunking strategies
class CodeChunker:
    def chunk_by_function(self, code, language):
        # Uses tree-sitter to extract complete functions
        
    def chunk_by_class(self, code, language):
        # Extracts classes with methods
        
    def chunk_by_semantic_blocks(self, code):
        # Groups related statements
```

**Storage Structure:**
```
giant-ai-dev/rag/db/
├── project_abc123/          # Hashed project path
│   ├── chroma.sqlite3       # ChromaDB database
│   ├── metadata.json       # Project info, last index time
│   └── chunks/              # Cached chunk data
├── project_def456/
│   ├── chroma.sqlite3
│   └── metadata.json
```

### Usage
```bash
# Index with chunking (creates project-specific store)
ai-rag index .

# Search semantically within current project
ai-search "authentication middleware"
ai-search "database connection pooling"
ai-search "error handling patterns"

# Advanced search with project targeting
ai-rag search "JWT token validation" --limit 10
ai-rag search "React hooks for API calls" --project /path/to/project
ai-rag list-projects  # Show all indexed projects
```

### Integration Points
- **Neovim**: `<leader>rs` for instant search in current project
- **AI CLI**: Automatic context injection from current project's RAG
- **MCP Tools**: `semantic_code_search` function accesses project-specific index
- **Avante**: RAG results automatically fed into AI context

## MCP (Model Context Protocol) Integration

### Available Tools

**Architecture Analysis**
```javascript
analyze_codebase_structure({
  focus: "api-layer",
  depth: "detailed"
})
```

**Template Generation**
```javascript
get_proof_of_concept_template({
  language: "typescript",
  pattern: "rest-api",
  framework: "express"
})
```

**Context Extraction**
```javascript
extract_function_context({
  file_path: "src/auth.ts",
  function_name: "validateToken"
})
```

### Project-Specific MCP
Create `.ai-setup/mcp/server.js` for custom tools:
```javascript
const server = new Server({
  name: "project-tools",
  version: "1.0.0"
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "run_tests",
      description: "Execute project test suite",
      inputSchema: { /* ... */ }
    }
  ]
}));
```

## Avante ↔ MCP ↔ RAG Integration Flow

### How the Systems Work Together

**1. Context Assembly Pipeline**
```lua
-- When Avante starts, it automatically:
function load_project_context()
  local context = {}
  
  -- Load project-specific context
  context.project = read_file(".ai-setup/context.md")
  context.conventions = read_file(".ai-setup/conventions.yml")
  
  -- Get MCP server status and available tools
  context.mcp_tools = mcphub.list_available_tools()
  
  -- Check RAG indexing status
  context.rag_status = check_rag_index_status()
  
  -- Combine into system prompt
  return build_system_prompt(context)
end
```

**2. Real-time Tool Access**
When you interact with Avante, it can dynamically call:

```lua
-- MCP tools available in Avante prompts
{
  "analyze_codebase_structure",    -- Via MCP
  "semantic_code_search",          -- Via MCP → RAG
  "get_proof_of_concept_template", -- Via MCP  
  "extract_function_context",      -- Via MCP
}
```

**3. Workflow Example: Code Analysis**
```
User: <leader>ca (analyze this function)
  ↓
Avante receives selected code
  ↓
System prompt includes:
  • Project context from .ai-setup/context.md
  • Available MCP tools
  • RAG search capabilities
  ↓
Avante can automatically:
  • Call semantic_code_search via MCP to find similar patterns
  • Use analyze_codebase_structure to understand architecture
  • Reference project conventions from context
  ↓
Response includes contextual analysis with:
  • Similar implementations found via RAG
  • Architectural insights from MCP tools
  • Project-specific recommendations
```

### MCP Tools in Avante Prompts

You can explicitly use MCP tools in your Avante conversations:

```
User in Avante: "Find similar authentication patterns in our codebase"
  ↓
Avante calls: semantic_code_search("authentication patterns")
  ↓
Returns: RAG results from current project's index
  ↓
Avante analyzes: Results with project context awareness
```

```
User in Avante: "Generate a REST API template for user management"
  ↓
Avante calls: get_proof_of_concept_template({
  language: "typescript",
  pattern: "rest-api", 
  domain: "user-management"
})
  ↓
Returns: Template following project conventions
  ↓
Avante customizes: Based on .ai-setup/conventions.yml
```

### RAG Integration in Avante

**Automatic Context Enhancement:**
```lua
-- Avante automatically enhances prompts with RAG
function enhance_prompt_with_rag(user_prompt)
  -- Extract intent from user prompt
  local search_terms = extract_search_intent(user_prompt)
  
  if search_terms then
    -- Search current project's RAG index
    local rag_results = rag_search(search_terms, {
      project = get_current_project(),
      limit = 5
    })
    
    -- Inject relevant code snippets into context
    return user_prompt .. "\n\nRelevant code from codebase:\n" .. rag_results
  end
  
  return user_prompt
end
```

**Manual RAG Queries:**
```
User in Avante: "Search for error handling patterns and analyze them"
  ↓
Avante understands this as: semantic_code_search + analysis request
  ↓
Executes: RAG search → returns code chunks → analyzes patterns
  ↓
Response: Detailed analysis of error handling across your project
```

## Neovim AI Integration

### Core Plugins

**Avante.nvim** - Primary AI Interface
```lua
{
  "yetone/avante.nvim",
  opts = {
    provider = "claude",
    claude = {
      model = "claude-3-7-sonnet-latest",
      temperature = 0,
      max_tokens = 30000,
    },
    system_prompt = function()
      -- Loads .ai-setup/context.md + MCP awareness
      return load_project_context()
    end,
    mappings = {
      ask = "<leader>aa",
      edit = "<leader>ae", 
      refresh = "<leader>ar",
    },
  },
}
```

**Codeium** - Real-time Completion
```lua
{
  "Exafunction/codeium.nvim",
  config = function()
    require("codeium").setup({
      enable_chat = true,
      tools = {
        curl = "curl",
        gzip = "gzip",
        uname = "uname",
        uuidgen = "uuidgen",
      },
    })
  end,
}
```

**MCP Hub** - Context Protocol
```lua
{
  "ravitemer/mcphub.nvim", 
  config = function()
    require("mcphub").setup({
      servers = {
        ["project-context"] = {
          command = "node",
          args = { "./.ai-setup/mcp/server.js" },
          auto_start = true,
        },
      },
    })
  end,
}
```

### Key Bindings & Tool Interoperability

| Key | Primary Tool | Secondary Tools | Workflow |
|-----|-------------|----------------|----------|
| `<leader>cc` | AI CLI | Auto-loads RAG context | Terminal AI with full project awareness |
| `<leader>ca` | Avante | MCP tools + RAG search | Visual analysis with architecture context |
| `<leader>cp` | Avante | MCP template tools | POC generation with project conventions |
| `<leader>cr` | Avante | RAG pattern search | Refactoring with similar implementations |
| `<leader>cf` | Avante | MCP context extraction | Function analysis with codebase patterns |
| `<leader>rs` | RAG | Direct search results | Pure semantic search, no AI analysis |
| `<leader>ra` | RAG → Avante | Search then AI analysis | Find code, then analyze with AI |
| `<leader>ma` | MCP → Avante | Architecture analysis | MCP tool output fed to Avante |
| `<leader>mp` | MCP → Avante | Template generation | MCP generates, Avante explains/extends |

### Integration Workflows

**Code Discovery & Analysis**
```
<leader>rs "user session management"
  ↓ Shows RAG search results in buffer
  
<leader>ra "user session management"  
  ↓ Same search + automatically opens Avante with results
  ↓ Avante analyzes patterns found across codebase
  ↓ Provides insights about implementation consistency
```

**Architecture Understanding**
```
<leader>ma
  ↓ Calls MCP analyze_codebase_structure
  ↓ Results automatically fed to Avante
  ↓ Avante explains architecture with project context
  ↓ Can suggest improvements based on conventions
```

**Smart Refactoring**
```
1. Select code block
2. <leader>cr
  ↓ Avante receives selection
  ↓ Automatically searches RAG for similar patterns
  ↓ Uses MCP to understand function context
  ↓ Suggests refactoring with project-specific patterns
```

**Template-Driven Development**
```
<leader>mp "API endpoint"
  ↓ MCP generates template based on project conventions
  ↓ Avante receives template and explains it
  ↓ Can modify template based on specific requirements
  ↓ Applies project naming conventions automatically
```

### Auto-Features

**Directory Change Detection**
```lua
vim.api.nvim_create_autocmd("DirChanged", {
  callback = function()
    -- Auto-register project MCP servers
    -- Update Avante context
    -- Check RAG indexing status
    require("config.mcp-autocmds").setup_project()
  end
})
```

**Smart Context Loading**
- Loads `.ai-setup/context.md` for project-specific instructions
- Detects available MCP servers automatically
- Checks RAG indexing status and suggests reindex if needed
- Updates Avante system prompt with full project awareness

## AI CLI Integration

### Enhanced Terminal AI
The AI CLI automatically inherits all your setup:

**Context Loading:**
```bash
# When you run the AI CLI in a project directory:
# 1. Detects git repository boundaries
# 2. Loads .ai-setup/context.md if present
# 3. Reads .ai-setup/conventions.yml
# 4. Includes recent git changes
# 5. Maps directory structure
# 6. Connects to available MCP servers
```

**Usage Patterns:**
```bash
# Basic AI assistance
claude  # or your preferred AI CLI

# Continue previous conversation
claude --continue

# Non-interactive mode for scripts
claude --print "analyze this error log"

# With specific context
claude --context "reviewing pull request"
```

**Automatic Enhancements:**
- **Git Integration**: Recent commits and changes included in context
- **Project Awareness**: Understands codebase structure and patterns
- **MCP Tools**: Access to semantic search and analysis tools
- **Convention Compliance**: Generates code following project standards

## Smart Project Configuration

### Intelligent Auto-Generation
The `ai-init-project` script now **automatically analyzes your codebase** and generates intelligent, pre-filled configuration instead of generic templates.

**Detection Capabilities:**
- **Languages**: JavaScript/TypeScript, Python, Rust, Go, Java
- **Frameworks**: React, Next.js, Express, Vue, Angular, Django, FastAPI, Flask, etc.
- **Conventions**: File naming patterns, indentation style, quote preferences
- **Structure**: Component architecture, test organization, API patterns
- **Context**: Project description from README.md or package.json

### Smart Context Generation (`.ai-setup/context.md`)
**Example auto-generated content for a Next.js project:**

```markdown
# Project Context

## Overview
A modern web application built with Next.js and TypeScript for server-side rendering... # ← From README.md

## Architecture
Primary Language: javascript
Framework: nextjs

### Project Structure
- Source code organized in `src/` directory
- Component-based architecture
- API layer structure

### Key Technologies
- Next.js React framework with SSR/SSG capabilities

## Development Guidelines

### Code Style
- Follow existing javascript conventions
- File naming: kebab-case        # ← Auto-detected
- Indentation: 2 spaces          # ← Auto-detected

### Testing Strategy
- Component testing with React Testing Library  # ← Framework-specific
- API testing with Jest/Mocha

## AI Assistant Instructions

### When generating code:
- Use Next.js App Router patterns and server components where appropriate
- Use React hooks and functional components
- Follow javascript best practices and idioms

## Current Focus
- [What are you currently working on?]
- [Any specific areas that need attention?]
- [Known issues or technical debt?]
```

### Smart Convention Detection (`.ai-setup/conventions.yml`)
**Example auto-detected conventions for the same Next.js project:**

```yaml
# Project Conventions (Auto-detected)
naming:
  files: kebab-case        # ← Detected from existing files
  components: PascalCase
  functions: camelCase
  constants: UPPER_SNAKE_CASE

structure:
  src_layout: feature      # ← Based on component structure analysis
  test_location: alongside # ← Detected from test file locations
  
code_style:
  max_line_length: 100
  indent: spaces           # ← Analyzed from existing code
  indent_size: 2           # ← Detected indentation size
  quotes: single           # ← Found in JavaScript files
  semicolons: true         # ← JavaScript-specific detection
  
git:
  branch_naming: feature/ticket-description
  commit_style: conventional
  
dependencies:
  package_manager: npm     # ← Detected from package.json
  version_strategy: exact
```

### Smart Auto-Setup Features

**Project Analysis Output:**
```bash
🔍 Analyzing project...
✅ Detected: javascript (nextjs)

Detected Configuration:
• Language: javascript
• Framework: nextjs
• File naming: kebab-case
• Indentation: spaces (2)
```

**Smart .gitignore Updates:**
The init script automatically adds AI-specific entries:
```bash
# AI setup local files
.ai-setup/rag/db/
```

**Optional Immediate Indexing:**
```bash
Would you like to index this project for semantic search now? (y/N)
```

**Fallback to Basic Mode:**
If you prefer generic templates, choose option 2:
```bash
Initialization options:
1. Smart initialization (auto-detects language/framework)
2. Basic initialization (templates with placeholders)

Choose option (1/2, default: 1):
```

**CLI Tool Availability:**
After setup, these commands are available globally:
```bash
ai-rag index <path>        # Index codebase
ai-rag search <query>      # Search with results
ai-search <query> [path]   # Quick search
ai-init-project           # Initialize project config
ai-init-project --clean   # Clean install - fresh configuration
ai-setup                  # Re-run global setup
```

## Tool Interoperability Examples

### Scenario 1: Understanding New Codebase
```bash
# Start with semantic exploration
<leader>rs "authentication"
# → Shows all auth-related code chunks from RAG

# Deep dive with AI analysis  
<leader>ra "authentication flow"
# → RAG search + Avante analyzes the flow across files
# → Avante has access to:
#   • Project context (.ai-setup/context.md)
#   • Found code patterns via RAG
#   • Architecture info via MCP tools
#   • Project conventions

# Get architectural overview
<leader>ma  
# → MCP analyzes codebase structure
# → Results fed to Avante for explanation
# → Avante correlates with RAG findings
```

### Scenario 2: Implementing New Feature
```bash
# Find similar implementations
<leader>ra "API rate limiting"
# → RAG finds existing patterns
# → Avante analyzes consistency and suggests approach

# Generate starting template
<leader>mp "Express middleware"
# → MCP generates template following project conventions
# → Avante explains template and suggests customizations
# → Template includes project-specific patterns from context

# Validate approach
Ask Avante: "Does this follow our API patterns?"
# → Avante automatically searches RAG for similar middleware
# → Compares against project conventions
# → Suggests improvements based on codebase patterns
```

### Scenario 3: Code Review & Refactoring
```bash
# Select problematic function
<leader>cr
# → Avante receives function
# → Automatically searches RAG for similar functions
# → Uses MCP to understand function's role in architecture
# → Suggests refactoring based on:
#   • Project conventions
#   • Similar implementations in codebase
#   • Architectural best practices

# Validate refactoring
<leader>cf (on refactored function)
# → MCP extracts full context around function
# → RAG searches for usage patterns
# → Avante analyzes impact and suggests tests
```

### Scenario 4: Documentation & Knowledge Transfer
```bash
# Generate documentation
Ask Avante: "Document our authentication system"
# → Avante automatically:
#   • Uses semantic_code_search to find all auth components
#   • Calls analyze_codebase_structure for flow understanding
#   • References project context for business logic
#   • Creates comprehensive documentation

# Update team knowledge
Ask Avante: "What should new developers know about our error handling?"
# → RAG finds all error handling patterns
# → MCP provides architectural context
# → Avante creates onboarding guide with examples
```

## 🔧 Advanced Integration Patterns

### Custom MCP Tool Creation for Avante
```javascript
// .ai-setup/mcp/server.js - Project-specific tools
const projectTools = {
  analyze_test_coverage: async (args) => {
    const coverage = await runCoverage(args.file);
    return {
      coverage_percent: coverage.percent,
      uncovered_lines: coverage.uncovered,
      suggestions: generateCoverageSuggestions(coverage)
    };
  },
  
  find_usage_patterns: async (args) => {
    const ragResults = await ragSearch(args.function_name);
    const usageAnalysis = analyzeUsagePatterns(ragResults);
    return {
      usage_count: usageAnalysis.count,
      common_patterns: usageAnalysis.patterns,
      edge_cases: usageAnalysis.edgeCases
    };
  }
};

// Avante can then call these tools:
// "Check test coverage for this component"
// "Find how this function is typically used"
```

### RAG-Enhanced Avante Prompts
```lua
-- Enhanced system prompt includes RAG awareness
local function build_enhanced_prompt()
  return string.format([[
You are an expert developer working on %s.

Project Context:
%s

Available Tools:
- semantic_code_search: Find code by meaning in this project
- analyze_codebase_structure: Understand architecture  
- get_proof_of_concept_template: Generate templates

When analyzing code:
1. Search for similar patterns using semantic_code_search
2. Consider project conventions and architecture
3. Reference existing implementations for consistency

Current Project RAG Status: %s files indexed
]], 
    get_project_name(),
    read_project_context(), 
    get_rag_file_count()
  )
end
```

### Avante Auto-Enhancement
```lua
-- Automatic RAG integration in Avante responses
local function enhance_avante_response(user_input, ai_response)
  -- If response mentions code patterns, auto-search RAG
  local patterns = extract_code_patterns(ai_response)
  
  if #patterns > 0 then
    local rag_examples = {}
    for _, pattern in ipairs(patterns) do
      local examples = rag_search(pattern, {limit = 3})
      table.insert(rag_examples, {
        pattern = pattern,
        examples = examples
      })
    end
    
    -- Append real examples to AI response
    return ai_response .. format_rag_examples(rag_examples)
  end
  
  return ai_response
end
```

## Advanced Configuration

### Custom MCP Tools
```javascript
// .ai-setup/mcp/server.js
const customTools = {
  run_tests: async (args) => {
    const result = await exec(`npm test ${args.pattern}`);
    return { result: result.stdout };
  },
  
  deploy_preview: async (args) => {
    const url = await deployPreview(args.branch);
    return { preview_url: url };
  },
  
  analyze_performance: async (args) => {
    const metrics = await getPerformanceMetrics();
    return { metrics };
  }
};
```

### Template Customization
```json
// ~/.ai-setup/templates/poc-templates.json
{
  "typescript": {
    "microservice": {
      "files": {
        "src/index.ts": "import express from 'express';\n// Service entry point",
        "src/routes/health.ts": "// Health check endpoint",
        "docker-compose.yml": "# Development environment"
      }
    }
  }
}
```

### RAG Configuration
```python
# ~/.ai-setup/rag/config.py
RAG_CONFIG = {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "embedding_model": "all-MiniLM-L6-v2",
    "supported_extensions": [
        ".ts", ".tsx", ".js", ".jsx", ".py", ".rs", 
        ".go", ".java", ".cpp", ".c", ".h"
    ],
    "exclude_patterns": [
        "node_modules", "dist", "build", ".git",
        "*.min.js", "*.bundle.js"
    ]
}
```

## Troubleshooting & Verification

### Check Setup Status
```bash
# Verify CLI tools are available
which ai-rag ai-search ai-init-project

# Test RAG indexing
ai-rag index . --batch-size 10  # Small test

# List indexed projects
ai-rag list-projects

# Test search
ai-search "function" . 5
```

### Common Issues

**Missing Dependencies:**
```bash
# If indexing fails
cd giant-ai-dev/rag
pip3 install -r requirements.txt

# If MCP server fails
cd giant-ai-dev/mcp  
npm install
```

**PATH Issues:**
```bash
# Add to shell config
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**RAG Index Problems:**
```bash
# Clear and rebuild index
ai-rag index . --clear

# Check permissions (from giant-ai-dev directory)
ls -la ./rag/db/

# Manual cleanup
rm -rf ./rag/db/project_*
```

**MCP Server Issues:**
```bash
# Test MCP server manually
node giant-ai-dev/mcp/project-server.js --test

# Check MCP hub configuration
cat ~/.config/mcp-hub/config.json

# Check Claude Desktop MCP config
cat ~/.config/claude-desktop/claude_desktop_config.json
```

### Neovim Integration Debug
```vim
" Check AI plugin status
:ClaudeStatus

" Reinitialize setup  
:ClaudeSetup

" Debug keybindings
:verbose map <leader>cc
```

### Performance Optimization

**RAG Tuning:**
```bash
# For large codebases
ai-rag index . --batch-size 100 --max-file-size 20

# For better granularity
ai-rag index . --chunk-size 30

# Exclude more directories (edit indexer.py)
exclude_dirs = {'.git', 'node_modules', 'dist', 'build', 'target', '.next', '.venv'}
```

**Context Management:**
- Keep `.ai-setup/context.md` under 2000 words
- Focus on current development priorities
- Remove outdated architectural decisions
- Update conventions after team changes

## Performance Tips

### RAG Optimization
- Index only source code directories
- Exclude build artifacts and dependencies
- Reindex after major refactors
- Use specific search terms for better results

### Context Management
- Keep `.ai-setup/context.md` under 2000 words
- Focus on current sprint/focus areas
- Remove outdated architectural decisions
- Update conventions after team changes

### MCP Efficiency
- Use project-specific servers for domain tools
- Keep global servers lightweight
- Implement caching for expensive operations
- Monitor server resource usage

## Benefits Over Cursor IDE

- **No Vendor Lock-in** - Use any AI provider  
- **Extensible** - Custom MCP tools and templates  
- **Local RAG** - Your code never leaves your machine  
- **Team Scalable** - Share configs via git  
- **Editor Choice** - Works with any editor supporting MCP  
- **Cost Effective** - No subscription required  
- **Privacy First** - Control your data completely  

## Team Setup

### For Team Leads
1. Initialize project: `ai-init-project`
2. Customize `.ai-setup/context.md` with team patterns
3. Commit `.ai-setup/` directory to repo
4. Share this README with team

### For Developers  
1. Run global setup: `./scripts/ai-setup`
2. In each project: `ai-rag index .`
3. Start using: `ai-search` and `<leader>cc`

### CI/CD Integration
```yaml
# .github/workflows/ai-index.yml
name: Update RAG Index
on:
  push:
    branches: [main]
    
jobs:
  index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Update search index
        run: |
          ai-rag index . --ci
          # Upload to shared storage if needed
```

---

*Transform your development workflow with AI that understands your code, your patterns, and your goals.*
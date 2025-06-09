# Giant AI Dev - Intelligent Development Toolkit

A standalone AI-powered development toolkit that provides semantic code search, enhanced AI context, and project-aware assistance. Works with multiple LLM providers (Claude, OpenAI, etc.) through Model Context Protocol (MCP) and CLI tools.

## 🚀 Quick Start (TLDR)

```bash
# 1. One-time setup (installs CLI tools, creates symlinks)
./scripts/ai-setup

# 2. Per-project initialization (auto-detects language/framework) 
ai-init-project-smart                # Smart auto-detection
ai-init-project-smart --clean        # Fresh install, overwrites existing

# 3. Index project for semantic search
ai-rag index .

# 4. Use your AI CLI with enhanced context
claude  # (or your preferred AI CLI)

# 5. Search your code semantically
ai-search "authentication middleware"

# 6. NEW: Agent mode for autonomous coding
ai-agent task "Add dark mode to settings page" --auto-accept
```

**What each does:**
- `ai-setup`: One-time install of CLI tools and MCP servers
- `ai-init-project-smart`: Auto-detects your project and creates intelligent `.ai-setup/` config
- `ai-rag index`: Creates searchable index of your codebase  
- `ai-search`: Find code by meaning, not keywords
- `ai-agent`: Autonomous coding with checkpoints (like Cursor's agent mode)

## Overview

Transform your development workflow with:
- **Semantic Code Search (RAG)** - Find code by meaning, not keywords
- **Model Context Protocol (MCP)** - Enhanced AI context and tools
- **Project-Aware AI** - Context that understands your architecture
- **Template Generation** - Smart POC and boilerplate creation
- **Agent Mode** - Autonomous coding with checkpoints and safety controls
- **CLI Tools** - Global commands for project initialization and search
- **AI-Enhanced Tooling** - Semantic refactoring, test generation, documentation sync

## 🛠️ Available Tools

### ✅ **Implemented Tools**
- **`ai-rag`** - Semantic code indexing and search
- **`ai-search`** - Quick codebase search
- **`ai-init-project-smart`** - Intelligent project setup with auto-detection
- **`ai-agent`** - Autonomous coding with safety controls and checkpoints  
- **`ai-pattern-refactor`** - Semantic pattern-based refactoring across multiple files

### 🚧 **Planned Tools** (Coming Soon)
- **`ai-test-generate`** - Context-aware test generation following your patterns
- **`ai-doc-sync`** - Keep documentation synchronized with code changes
- **`ai-bridge`** - Basic tooling layer for non-tooling LLMs (OpenAI, local models)

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  LLM Providers  │    │   RAG System    │    │  MCP Servers    │
│                 │    │                 │    │                 │
│ • Claude Code   │◄──►│ • Chunked Index │◄──►│ • Project Tools │
│ • OpenAI (TBD)  │    │ • Semantic Search│    │ • Architecture  │
│ • Custom CLIs   │    │ • ChromaDB      │    │ • Templates     │
│ • Agent Mode    │    │ • Local Storage │    │ • Context       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐    ┌─────────────────┐
                    │   Agent Mode    │    │ Editor Support  │
                    │                 │    │                 │
                    │ • Checkpoints   │    │ • Claude Desktop│
                    │ • Auto Tasks    │    │ • Neovim (opt)  │
                    │ • Batch Exec    │    │ • VS Code (opt) │
                    │ • Safety Ctrl   │    │ • Any MCP       │
                    └─────────────────┘    └─────────────────┘
```

## Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 18+** with npm  
- **LLM CLI Tool** - Examples:
  - Claude: `npm install -g @anthropic/claude-code`
  - OpenAI: `npm install -g @openai/chatgpt-cli` (when available)
  - Or any MCP-compatible AI assistant

### Installation
```bash
# 1. Clone or download giant-ai-dev
git clone <giant-ai-dev-repo>
cd giant-ai-dev

# 2. Run setup script
./scripts/ai-setup
```

This automatically:
- ✅ Creates isolated Python environment in `.venv/` (no global pollution)
- ✅ Installs Python dependencies for RAG in isolation
- ✅ Installs Node.js dependencies for MCP servers
- ✅ Creates wrapper scripts in `~/.local/bin/` that use the isolated environment
- ✅ Configures MCP hub with global servers
- ✅ Sets up RAG database directory
- ✅ Configures LLM integrations (Claude Desktop, etc.)

### Add to PATH
```bash
# Add to your .bashrc/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

## Usage

### Initialize a Project
```bash
# Navigate to any project
cd your-project

# Initialize LLM project configuration (smart auto-detection)
ai-init-project

# Clean install - fresh configuration files (overwrites existing)
ai-init-project --clean
```

**Smart Initialization** automatically detects and configures:
- **Language**: JavaScript/TypeScript, Python, Rust, Go, Java
- **Framework**: React/Next.js, Express, Django/FastAPI/Flask, etc.
- **Conventions**: File naming, indentation, quote style
- **Project structure**: Components, routes, testing patterns

Creates intelligent, pre-filled configuration:
```
your-project/
├── .ai-setup/
│   ├── context.md       # Auto-generated with project analysis
│   └── conventions.yml  # Detected coding standards and patterns
└── .gitignore          # Updated with AI Dev entries
```

**Example Smart Output:**
```yaml
# conventions.yml (auto-detected)
naming:
  files: kebab-case        # ← Detected from existing files
code_style:
  indent: spaces           # ← Analyzed from codebase
  indent_size: 2
  quotes: single           # ← Found in JavaScript files
```

```markdown
# context.md (auto-generated)
## Architecture
Primary Language: javascript
Framework: nextjs

### Key Technologies
- Next.js React framework with SSR/SSG capabilities

### When generating code:
- Use Next.js App Router patterns and server components
- Follow React hooks and functional components
```

### Index for Semantic Search
```bash
# Index current project for semantic search
ai-rag index .

# Verify indexing
ai-rag list-projects
```

### Search Your Code
```bash
# Search semantically within current project
ai-search "authentication middleware"
ai-search "database connection pooling"
ai-search "error handling patterns"

# Advanced search with project targeting
ai-rag search "JWT token validation" --limit 10
ai-rag search "React hooks for API calls" --project /path/to/project
```

### Use Your LLM CLI
```bash
# Basic AI assistance (automatically loads project context)
# Claude example:
claude

# OpenAI example (future):
# openai-chat

# Continue previous conversation
claude --continue

# With specific context
claude --context "reviewing pull request"
```

## Directory Structure

```
giant-ai-dev/                    # Standalone AI development toolkit
├── docs/
│   └── rag-search-usage-guide.md # RAG vs grep usage guide
├── rag/
│   ├── db/                    # ChromaDB storage for all projects
│   │   ├── project_abc123/    # Hashed project path
│   │   │   ├── chroma.sqlite3 # Vector embeddings
│   │   │   └── index.json     # Project metadata
│   ├── indexer.py            # RAG indexing script
│   ├── search.py            # Search interface
│   └── requirements.txt     # Python dependencies
├── mcp/
│   ├── project-server.js    # Global MCP tools
│   ├── package.json
│   └── node_modules/
├── scripts/
│   ├── ai-setup            # One-time setup script
│   └── ai-init-project     # Per-project initialization
├── providers/
│   └── claude-config.md    # Claude-specific configuration
├── templates/              # POC templates
├── prompts/               # AI prompts
└── settings.local.json    # Local configuration

~/.local/bin/              # CLI tools (symlinked by setup)
├── ai-rag               # → giant-ai-dev/rag/indexer.py
├── ai-search            # → giant-ai-dev/rag/search.py
├── ai-setup             # → giant-ai-dev/scripts/ai-setup
└── ai-init-project      # → giant-ai-dev/scripts/ai-init-project
```

## RAG System - Semantic Code Search

> **💡 When to Use RAG vs Grep?** See [docs/rag-search-usage-guide.md](docs/rag-search-usage-guide.md) for a detailed comparison and practical examples of when RAG search provides value over traditional text search.

### Intelligent Chunking
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

### Search Capabilities
- **Function-level chunking**: Tree-sitter parsing for precise boundaries  
- **Semantic similarity**: Find code by meaning, not keywords
- **Cross-file patterns**: Identify similar implementations across codebase
- **Implementation similarity**: Match patterns and approaches

### Storage Structure
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

**Semantic Search**
```javascript
semantic_code_search({
  query: "user authentication flow",
  limit: 5
})
```

### LLM Desktop Integration

After setup, compatible LLM desktop applications (like Claude Desktop) automatically connect to your MCP servers, giving you access to all tools in the desktop app.

## Editor Integration

### Neovim (Optional)
Complete Neovim integration available with AI keybindings and workflow automation. See `nvim/NEOVIM_AI_SETUP.md` for details.

### VS Code (Future)
MCP support coming to VS Code and other editors.

### Any MCP-Compatible Editor
The MCP servers work with any editor that supports the Model Context Protocol.

## Project Configuration

### Smart Auto-Generated Configuration

When you run `ai-init-project`, it automatically analyzes your codebase and generates intelligent, pre-filled configuration files instead of generic placeholders.

**Language & Framework Detection:**
- Detects primary language by analyzing file counts and config files
- Identifies frameworks (React, Next.js, Express, Django, FastAPI, etc.)
- Extracts project description from README.md or package.json

**Convention Analysis:**
- File naming patterns (kebab-case, camelCase, snake_case)
- Indentation style (tabs vs spaces, size)
- Quote preferences (single vs double)
- Test organization (alongside vs separate directories)

### Generated Context File (`.ai-setup/context.md`)
**Auto-populated based on project analysis:**
```markdown
# Project Context

## Overview
A modern web application built with Next.js and TypeScript... # ← From README

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
- File naming: kebab-case
- Indentation: 2 spaces

### Testing Strategy
- Component testing with React Testing Library
- API testing with Jest/Mocha

### When generating code:
- Use Next.js App Router patterns and server components where appropriate
- Use React hooks and functional components
- Follow javascript best practices and idioms
```

### Generated Conventions File (`.ai-setup/conventions.yml`)
**Auto-detected from your codebase:**
```yaml
# Project Conventions (Auto-detected)
naming:
  files: kebab-case        # ← Detected from existing files
  components: PascalCase
  functions: camelCase
  constants: UPPER_SNAKE_CASE

structure:
  src_layout: feature      # ← Based on project structure analysis
  test_location: alongside # ← Detected from test file locations
  
code_style:
  max_line_length: 100
  indent: spaces  # or tabs
  indent_size: 2
  quotes: single  # or double
  semicolons: false  # JS/TS specific
  
git:
  branch_naming: feature/ticket-description
  commit_style: conventional  # conventional commits
  
dependencies:
  package_manager: npm  # or yarn, pnpm, cargo, pip, etc.
  version_strategy: exact  # or caret, tilde
```

## CLI Commands Reference

### RAG Commands
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

# Clear and rebuild index
ai-rag index . --clear
```

### Project Commands
```bash
# Initialize project config
ai-init-project

# Clean install - fresh configuration files
ai-init-project --clean

# Re-run global setup
ai-setup
```

## Troubleshooting

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
# If indexing fails - dependencies are isolated in .venv
cd giant-ai-dev
source .venv/bin/activate
pip install -r rag/requirements.txt
deactivate

# Or just re-run setup to fix everything
./scripts/ai-setup

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

## Agent Mode - Autonomous Coding

Giant AI Dev includes a powerful agent mode that rivals Cursor IDE's capabilities while maintaining flexibility across LLM providers.

### Features
- **Autonomous task execution** - Give high-level instructions, agent handles implementation
- **Checkpoint system** - Automatic snapshots before changes, easy rollback
- **Multi-provider support** - Works with Claude Code, OpenAI (coming), and custom CLIs
- **Batch operations** - Execute multiple tasks in sequence
- **Safety boundaries** - No git commits/pushes, respects project boundaries

### Quick Examples
```bash
# Single task with auto-accept
ai-agent task "Add comprehensive error handling to all API endpoints" --auto-accept

# Batch tasks from file
ai-agent batch refactor-plan.txt --continue-on-failure

# Interactive mode with checkpoint control
ai-agent interactive

# Manual checkpoint management
ai-agent checkpoint "Before major refactor"
ai-agent list
ai-agent restore 20240106_143022
```

For detailed agent mode documentation, see [giant-agent.md](giant-agent.md).

## Benefits Over Other Solutions

- **No Vendor Lock-in** - Use any AI provider  
- **Extensible** - Custom MCP tools and templates  
- **Local RAG** - Your code never leaves your machine  
- **Team Scalable** - Share configs via git  
- **Editor Choice** - Works with any editor supporting MCP  
- **Cost Effective** - No subscription required  
- **Privacy First** - Control your data completely  
- **Agent Mode** - Cursor-like autonomous coding across providers
- **Isolated Dependencies** - Python deps in `.venv/`, no global pollution  

## Team Setup

### For Team Leads
1. Initialize project: `ai-init-project`
2. Customize `.ai-setup/context.md` with team patterns
3. Commit `.ai-setup/` directory to repo
4. Share this README with team

### For Developers  
1. Run global setup: `./scripts/ai-setup`
2. In each project: `ai-rag index .`
3. Start using: `ai-search` and your LLM CLI

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

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Setting up the development environment
- Submitting pull requests
- Contributor License Agreement (CLA)
- Community guidelines

Areas where we especially welcome contributions:
- **RAG improvements** - Better semantic search and code understanding
- **MCP tools** - New analysis and context extraction capabilities
- **Agent mode enhancements** - Additional prompt templates and safety features
- **Development tools** - Implementation of planned utilities (ai-pattern-refactor, ai-test-generate, etc.)
- **Documentation** - Tutorials, examples, and architecture explanations

## License

Giant AI Dev is licensed under the [Apache License 2.0](LICENSE).

---

*A next-generation development toolkit that understands your code, respects your privacy, and amplifies your productivity.*
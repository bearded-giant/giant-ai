# Claude Code Enhanced Setup

This is a global installation of Claude Code enhancements with RAG (Retrieval-Augmented Generation) and MCP (Model Context Protocol) support.

## Features

- **Global RAG System**: Semantic code search across any project
- **MCP Servers**: Project-aware context and tools 
- **Neovim Integration**: Enhanced AI workflows with keybindings
- **Project Templates**: POC templates for multiple languages
- **Context Management**: Global and project-specific context files

## Installation

1. Run the setup script:
   ```bash
   cd ~/dotfiles/claude/.claude
   ./bin/claude-setup
   ```

2. Add to your PATH (if not already):
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

3. Stow the configuration:
   ```bash
   cd ~/dotfiles
   stow claude
   ```

## Usage

### Index a Project
```bash
claude-rag index /path/to/project
# or from within a project:
claude-rag index .
```

### Search Code
```bash
# Command line search
claude-rag search "function definition" /path/to/project

# Quick search (from within project)
claude-search "async handler"
```

### Initialize Project
```bash
# In any project directory
claude-init-project
```

This creates:
- `.claude/context.md` - Project-specific AI context
- `.claude/conventions.yml` - Coding conventions

### Neovim Keybindings

| Key | Description |
|-----|-------------|
| `<leader>cc` | Open Claude Code |
| `<leader>ca` | Architecture analysis (visual mode) |
| `<leader>cp` | POC planning (visual mode) |
| `<leader>cr` | Refactoring suggestions (visual mode) |
| `<leader>cf` | Analyze current function |
| `<leader>rs` | RAG search codebase |
| `<leader>rS` | Telescope RAG search |
| `<leader>ce` | Edit project context |
| `<leader>ci` | Initialize Claude project |

## Configuration

### Global Context
Edit `~/.claude/templates/default-context.md` for global AI instructions.

### Project Context
Edit `.claude/context.md` in any project for project-specific guidelines.

### Templates
POC templates are in `~/.claude/templates/poc-templates.json`.

## MCP Servers

The MCP server provides these tools:
- `analyze_codebase_structure` - Analyze project patterns
- `get_proof_of_concept_template` - Generate POC templates
- `extract_function_context` - Extract code with context
- `semantic_code_search` - RAG search integration
- `get_project_context` - Load project guidelines

## Troubleshooting

### RAG Index Issues
```bash
# Clear and rebuild index
claude-rag index /path/to/project --clear
```

### List Indexed Projects
```bash
claude-rag list-projects
```

### Python Dependencies
If you encounter dependency issues:
```bash
cd ~/.claude/rag
pip install -r requirements.txt
```

## Architecture

```
~/.claude/
├── bin/              # CLI tools
├── mcp/              # MCP server
├── rag/              # RAG indexer and search
├── templates/        # Code templates
└── prompts/          # AI prompts
```

The system uses:
- ChromaDB for vector storage
- Sentence transformers for embeddings
- Tree-sitter for code parsing
- MCP for tool integration
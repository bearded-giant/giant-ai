# LLM Connectivity Guide - How Giant AI Connects to AI Models

## Overview

Giant AI provides a flexible architecture for connecting to different AI providers and models. Unlike monolithic AI coding tools, Giant AI acts as an **orchestration layer** that works with your preferred AI providers through standardized interfaces.

## Connection Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Your Code     │    │   Giant AI      │    │   AI Providers  │
│                 │    │                 │    │                 │
│ • Editor        │◄──►│ • Agent Mode    │◄──►│ • Claude Code   │
│ • Terminal      │    │ • RAG System    │    │ • OpenAI CLI    │
│ • Neovim        │    │ • MCP Tools     │    │ • Local Models  │
│ • CLI Tools     │    │ • Orchestration │    │ • Custom APIs   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Key Principle**: Giant AI doesn't replace your AI provider - it **enhances** your existing AI tools with semantic search, project context, and autonomous coding capabilities.

## Connection Methods

### 1. **Agent Mode (Autonomous Coding)**

**Purpose**: Cursor-like autonomous coding with checkpoints and safety controls.

**Configuration File**: `.giant-ai/agent.yml` (per project)
```yaml
provider: claude-code          # Primary provider
checkpoint_before_tasks: true  # Safety feature
auto_restore_on_failure: false
max_checkpoints: 20

prompt_templates:
  default: agent/prompts/default.md
  refactor: agent/prompts/refactor.md
  feature: agent/prompts/feature.md
```

**How It Works**:
```bash
# Agent calls your AI CLI with enhanced context
ai-agent task "Add dark mode support" --auto-accept

# Behind the scenes:
# 1. Loads .giant-ai/context.md (project understanding)
# 2. Creates checkpoint (safety backup)
# 3. Calls: claude --auto-accept [enhanced prompt with context]
# 4. Monitors changes and can rollback if needed
```

**Supported Providers**:
- **Claude Code**: Full auto-accept support
- **OpenAI CLI**: Planned (when available)
- **Custom CLIs**: Extensible via provider system

### 2. **AI CLI Integration (Enhanced Terminal)**

**Purpose**: Your existing AI CLI tool with automatic project context injection.

**How It Works**:
```bash
# Your normal AI CLI command
claude "How should I structure this API?"

# Giant AI automatically enhances with:
# • Project context from .giant-ai/context.md  
# • Coding conventions from .giant-ai/conventions.yml
# • Recent git changes and project structure
# • RAG search results for relevant code
```

**Context Assembly Pipeline**:
```python
def load_project_context():
    context = {}
    
    # Load project-specific context
    context.project = read_file(".giant-ai/context.md")
    context.conventions = read_file(".giant-ai/conventions.yml")
    
    # Get MCP server status and available tools
    context.mcp_tools = mcphub.list_available_tools()
    
    # Check RAG indexing status  
    context.rag_status = check_rag_index_status()
    
    return build_system_prompt(context)
```

### 3. **Neovim Integration (Direct Provider APIs)**

**Purpose**: In-editor AI with semantic search and MCP tool integration.

**Configuration**: Your Neovim configuration
```lua
-- Avante.nvim - Primary AI interface
{
  "yetone/avante.nvim",
  opts = {
    provider = "claude",  -- Direct API connection
    claude = {
      model = "claude-3-7-sonnet-latest",  -- Specific model
      temperature = 0,
      max_tokens = 30000,
    },
    system_prompt = function()
      return load_project_context()  -- Giant AI context
    end,
  },
}

-- MCP Hub - Tool integration
{
  "ravitemer/mcphub.nvim", 
  config = function()
    require("mcphub").setup({
      servers = {
        ["project-context"] = {
          command = "node",
          args = { "./.giant-ai/mcp/server.js" },  -- Giant AI MCP server
          auto_start = true,
        },
      },
    })
  end,
}
```

**Available Models by Provider**:
```lua
-- Claude (via Anthropic API)
claude = {
  model = "claude-3-7-sonnet-latest",     -- Latest Sonnet
  model = "claude-3-opus-latest",         -- Most capable
  model = "claude-3-haiku-latest",        -- Fastest
}

-- OpenAI (via OpenAI API)
openai = {
  model = "gpt-4-turbo",                  -- Balanced
  model = "gpt-4o",                       -- Latest
  model = "gpt-3.5-turbo",               -- Fast/cheap
}
```

### 4. **RAG System (Model-Agnostic)**

**Purpose**: Semantic code search that enhances any AI provider.

**How It Works**:
```bash
# Index your codebase
ai-rag index .

# Search semantically (feeds into AI context)
ai-search "authentication middleware" 

# Auto-enhancement in Neovim
<leader>rs  # Direct search
<leader>ra  # Search + AI analysis
```

**Integration Points**:
- **Terminal AI**: Auto-injects relevant code snippets
- **Neovim**: `semantic_code_search` MCP tool
- **Agent Mode**: Context-aware task planning

## Configuration Hierarchy

### Global Configuration
```
~/.giant-ai/                    # Global Giant AI settings
├── tools.yml                  # Tool defaults
└── templates/                 # Global templates
```

### Per-Project Configuration
```
your-project/
├── .giant-ai/
│   ├── agent.yml              # Agent mode provider
│   ├── context.md             # AI instructions
│   ├── conventions.yml        # Coding standards  
│   └── mcp/server.js         # Custom MCP tools
```

### External Tool Configuration
```
~/.config/claude-code/         # Claude Code CLI config
~/.config/openai/              # OpenAI CLI config (future)
~/.config/nvim/                # Neovim AI plugin config
```

## Provider System Architecture

### Abstract Provider Interface
```python
# agent/providers/base.py
class BaseLLMProvider(ABC):
    @abstractmethod
    def execute_agent_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an agent task with the provider"""
        pass
    
    @abstractmethod 
    def supports_auto_accept(self) -> bool:
        """Check if provider supports auto-accept mode"""
        pass
```

### Current Providers
```python
class LLMProviderFactory:
    _providers = {
        "claude-code": ClaudeCodeProvider,  # Full support
        "openai": OpenAIProvider,          # Placeholder
    }
```

### Claude Code Provider Implementation
```python
class ClaudeCodeProvider(BaseLLMProvider):
    def execute_agent_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        cmd = ["claude"]
        
        if context.get("auto_accept"):
            cmd.extend(["--auto-accept"])  # Autonomous mode
            
        if context.get("continue_session"):
            cmd.extend(["--continue"])     # Session continuity
            
        cmd.extend(["--print", task])      # Enhanced task prompt
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return {"success": result.returncode == 0, "output": result.stdout}
```

## How to Configure Your Setup

### Step 1: Choose Your Primary AI Provider

**Claude Code (Recommended)**:
```bash
# Install Claude Code CLI
npm install -g @anthropic/claude-code

# Configure API key
claude config

# Verify connection
claude "test connection"
```

**OpenAI CLI (Future)**:
```bash
# Will be available when OpenAI releases CLI
# pip install openai-cli  # (hypothetical)
```

### Step 2: Configure Giant AI Agent Mode

```bash
# In your project directory
cd your-project

# Initialize Giant AI
ai-init-project-smart

# Customize agent configuration
vi .giant-ai/agent.yml
```

Example `.giant-ai/agent.yml`:
```yaml
provider: claude-code
checkpoint_before_tasks: true
auto_restore_on_failure: false
max_checkpoints: 20

# Model-specific settings (passed to provider)
model_config:
  temperature: 0
  max_tokens: 30000
  
prompt_templates:
  default: default
  refactor: refactor  
  feature: feature
  debug: debug
```

### Step 3: Configure Neovim Integration (Optional)

Add to your Neovim configuration:
```lua
-- Enhanced AI coding with Giant AI context
{
  "yetone/avante.nvim",
  opts = {
    provider = "claude",
    claude = {
      model = "claude-3-7-sonnet-latest",
      api_key_name = "ANTHROPIC_API_KEY",
    },
    system_prompt = function()
      -- Load Giant AI project context
      local context_file = vim.fn.getcwd() .. "/.giant-ai/context.md"
      if vim.fn.filereadable(context_file) == 1 then
        return vim.fn.readfile(context_file)
      end
      return "You are an expert developer."
    end,
  },
}

-- MCP tool integration
{
  "ravitemer/mcphub.nvim",
  config = function()
    require("mcphub").setup({
      servers = {
        ["giant-ai-project"] = {
          command = "node",
          args = { "./.giant-ai/mcp/server.js" },
          auto_start = true,
        },
      },
    })
  end,
}
```

### Step 4: Index Your Project for RAG

```bash
# Create semantic search index
ai-rag index .

# Test semantic search
ai-search "error handling patterns" . 5

# Verify indexing
ai-rag list-projects
```

## Model Switching Workflows

### Switching Agent Provider
```bash
# Edit project config
vi .giant-ai/agent.yml

# Change provider
provider: openai  # from claude-code

# Test new provider
ai-agent task "simple test" --dry-run
```

### Switching Neovim Model
```lua
-- In your Neovim config
claude = {
  model = "claude-3-opus-latest",  -- More capable
  -- or
  model = "claude-3-haiku-latest", -- Faster/cheaper
}
```

### Using Multiple Providers
```bash
# Different providers for different tasks
ai-agent task "complex refactoring" --provider claude-code
ai-agent task "simple fix" --provider openai

# Provider-specific strengths
claude "analyze architecture"     # Claude: better at analysis
openai "write unit test"         # OpenAI: faster for simple tasks
```

## Advanced Integration Patterns

### Custom Provider Implementation
```python
# Create custom provider
class LocalLlamaProvider(BaseLLMProvider):
    def execute_agent_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Integration with local Llama model
        cmd = ["ollama", "run", "codellama"]
        # ... implementation
        
# Register provider
LLMProviderFactory.register_provider("local-llama", LocalLlamaProvider)
```

### Project-Specific MCP Tools
```javascript
// .giant-ai/mcp/server.js - Custom tools for your project
const server = new Server({
  name: "project-specific-tools",
  version: "1.0.0"
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "run_project_tests",
      description: "Run this project's specific test suite",
      inputSchema: { /* ... */ }
    },
    {
      name: "deploy_to_staging", 
      description: "Deploy current branch to staging environment",
      inputSchema: { /* ... */ }
    }
  ]
}));
```

### Multi-Model Workflows
```bash
# Use different models for different phases
ai-agent task "analyze requirements" --provider claude-code     # Analysis
ai-agent task "generate boilerplate" --provider openai         # Code gen
ai-agent task "optimize performance" --provider claude-code    # Optimization
```

## Benefits of This Architecture

### **No Vendor Lock-in**
- Switch providers without changing workflows
- Use multiple providers simultaneously
- Maintain consistent tooling across teams

### **Flexible Configuration**
- Global defaults with project overrides
- Provider-specific optimizations
- Easy A/B testing of different models

### **Enhanced Context**
- Automatic project context injection
- Semantic code search integration
- MCP tool ecosystem

### **Cost Optimization**
- Use different models for different tasks
- Local models for simple operations
- Cloud models for complex reasoning

### **Safety & Control**
- Checkpoint system for autonomous operations
- Rollback capabilities
- Manual override options

---

## Related Documentation

- [Agent Mode vs Manual Coding](agent-mode-vs-manual-coding.md) - When to use autonomous vs interactive AI
- [MCP Demystified](mcp-demystified.md) - Model Context Protocol integration
- [RAG Overview](rag-overview-explained.md) - Semantic search system
- [LLM Provider Practical Guide](llm-provider-practical-guide.md) - Provider comparison and selection

---

**Ready to get started?** Follow the [main setup guide](../README.md#quick-start) to configure your preferred AI provider with Giant AI!
# Claude Desktop Provider Guide - Use A Paid Plan

## Overview

The Claude Desktop Provider allows you to use a paid Claude Pro Max subscription directly through Giant AI, without consuming API tokens. This leverages your existing Claude Desktop application to execute tasks.

## Benefits

- **No API tokens needed** - Uses your Pro Max plan
- **Unlimited usage** - Leverages your Pro Max benefits
- **Large context window** - Full 200K token context
- **Faster responses** - Direct desktop integration
- **Cost savings** - No per-token charges

## Quick Start

### 1. Prerequisites

- Claude Desktop app installed and logged in with Pro Max account
- macOS (currently - Windows/Linux support tbd)
- Giant AI agent mode configured

### 2. Basic Usage

```bash
# Use Claude Desktop instead of API tokens
ai-agent task "Your task here" --provider claude-desktop

# No checkpoint (faster for simple tasks)
ai-agent task "Create a hello world function" --provider claude-desktop --no-checkpoint

# With auto-accept for autonomous operation
ai-agent task "Refactor the auth module" --provider claude-desktop --auto-accept
```

### 3. Configuration

Create or update `.giant-ai/agent.yml`:

```yaml
# Use Claude Desktop as default provider
provider: claude-desktop

claude_desktop:
  auto_accept_enabled: true
  timeout: 300 # 5 minutes for complex tasks
  context_window: 200000 # Claude's large context
```

Or use the provided configuration:

```bash
cp .giant-ai/agent-claude-desktop.yml .giant-ai/agent.yml
```

## How It Works

### Architecture

```
Your Code → Agent Mode → ClaudeDesktopProvider → Claude Desktop App → Anthropic (Pro Max)
                                                         ↑
                                                   Your Session
```

### Integration Methods

#### 1. AppleScript Integration (Current)

- Uses AppleScript to send tasks to Claude Desktop
- Works on macOS
- Simple and reliable

#### 2. MCP Integration (Future!)

- Will use Model Context Protocol when Claude Desktop exposes MCP server
- Cross-platform support
- Real-time streaming

## Advanced Usage

### Setting as Default Provider

```bash
# Edit .giant-ai/agent.yml
provider: claude-desktop  # Set as default

# Now all commands use Claude Desktop
ai-agent task "Any task"  # Automatically uses claude-desktop
```

### Batch Processing

```bash
# Create tasks file
cat > tasks.txt << EOF
Add error handling to the API endpoints
Create unit tests for the auth module
Refactor the database connection pooling
EOF

# Execute batch with Claude Desktop
ai-agent batch tasks.txt --provider claude-desktop
```

### Interactive Mode

```bash
# Start interactive mode with Claude Desktop
ai-agent interactive

# In the prompt:
agent> task "Your task here"
```

## Troubleshooting

### Claude Desktop Not Found

```bash
# Check if Claude is running
ps aux | grep -i claude

# The provider looks for:
# 1. 'claude' command in PATH
# 2. /Applications/Claude.app/Contents/MacOS/Claude
```

### Task Not Executing

- Ensure Claude Desktop is running and logged in
- Check that you have an active Pro Max subscription
- Try running Claude Desktop manually first

### Checkpoint Errors

```bash
# If checkpoint fails in certain directories
ai-agent task "..." --provider claude-desktop --no-checkpoint
```

## Provider Comparison

| Feature            | claude-desktop | claude-code | anthropic (API) |
| ------------------ | -------------- | ----------- | --------------- |
| Requires API Token | ❌             | ❌          | ✅              |
| Uses Pro Max Plan  | ✅             | ❌          | ❌              |
| Context Window     | 200K           | 100K        | 200K            |
| Auto-accept        | ✅             | ✅          | ❌              |
| File Operations    | ✅             | ✅          | ❌              |
| Streaming          | 🔜             | ✅          | ✅              |

## Best Practices

### 1. Use for Long Tasks

Claude Desktop is good for complex, multi-step tasks:

```bash
ai-agent task "Implement complete authentication system with JWT" \
  --provider claude-desktop \
  --auto-accept
```

### 2. Disable Checkpoints for Simple Tasks

```bash
ai-agent task "Explain this code" --provider claude-desktop --no-checkpoint
```

### 3. Combine with RAG Search

```bash
# First, search for context
ai-search "authentication implementation"

# Then use Claude Desktop with context
ai-agent task "Improve the authentication based on search results" \
  --provider claude-desktop
```

## Current Limitations

1. **macOS Only** - AppleScript integration is Mac-specific
2. **No Streaming** - Responses arrive all at once
3. **Manual Result Check** - Need to check Claude Desktop app for detailed output
4. **Single Task at a Time** - No parallel execution

## Future Enhancements

### Coming Soon

- Windows/Linux support via different automation methods
- MCP protocol integration for better communication
- Response streaming
- Automatic result extraction
- Parallel task execution

### Planned Features

- Direct file synchronization
- Real-time progress monitoring
- Automatic context injection
- Tool execution feedback

## Tips

### Maximize Efficiency

1. **Keep Claude Desktop Open** - Faster task execution
2. **Use Templates** - Configure prompt templates for common tasks
3. **Batch Similar Tasks** - Group related work together

### Integration with Workflow

```bash
# Morning routine
ai-agent task "Review and summarize overnight PRs" --provider claude-desktop
ai-agent task "Generate daily standup notes" --provider claude-desktop
ai-agent task "Plan today's development tasks" --provider claude-desktop
```

## Related Documentation

- [Agent Mode Guide](agent/README.md)
- [Provider Comparison](docs/providers-guide.md)
- [Implementation Details](IMPLEMENTATION_PLAN_ANTHROPIC_COPILOT_AGENT.md)


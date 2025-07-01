# Giant AI Provider Guide

Giant AI now supports multiple AI providers for agent mode, giving you flexibility to choose the best provider for your needs and budget.

## Quick Provider Reference

| Provider | ID | Auth Method | Use Case |
|----------|-----|------------|----------|
| Claude (CLI) | `claude-code` | Browser/SSO | Interactive development |
| Claude (API) | `anthropic` | API Key | Automation, CI/CD |
| OpenAI | `openai` | API Key | General purpose |
| Google | `gemini` | API Key | Cost-effective |
| Ollama | `ollama` | None | Privacy, offline |

## Available Providers

### 1. Claude Code (Default)
- **Provider ID**: `claude-code`
- **Requirements**: Claude CLI (via Desktop OR Web)
- **Cost**: Free with Claude subscription
- **Best For**: Interactive development, file operations, terminal access

```yaml
# .giant-ai/agent.yml
provider: claude-code
```

**Three Ways to Get Claude CLI:**

1. **Claude Desktop** - Installs `claude` CLI automatically
2. **Claude Code (Web)** - Install CLI via: `npm install -g @anthropic-ai/claude-cli`
3. **Enterprise/Team Plans** - Works with SSO/SAML authentication

**Authentication Methods:**
- **Desktop**: Automatic through app
- **Web/Enterprise**: Browser-based auth (opens browser on first use)
- **Team Plans**: SSO/SAML through your organization

**Pros:**
- Native file system access
- Terminal integration
- Auto-accept mode
- No API key needed
- Works with all Claude subscription types

**Cons:**
- Requires active Claude subscription
- Browser auth needed for web version

### 2. OpenAI
- **Provider ID**: `openai`
- **Requirements**: OpenAI API key
- **Cost**: Pay per token (see OpenAI pricing)
- **Best For**: Versatile tasks, GPT-4 intelligence

```yaml
# .giant-ai/agent.yml
provider: openai
openai_api_key: ${OPENAI_API_KEY}  # or set directly
openai_model: gpt-4-turbo-preview
openai_temperature: 0.7
openai_max_tokens: 4000
```

**Available Models:**
- `gpt-4-turbo-preview` - Latest GPT-4 Turbo
- `gpt-4` - Standard GPT-4
- `gpt-3.5-turbo` - Faster, cheaper option

**Pros:**
- Excellent code understanding
- Good instruction following
- Wide knowledge base

**Cons:**
- Requires API key
- Pay per use
- No direct file system access (handled by Giant AI)

### 3. Anthropic API
- **Provider ID**: `anthropic`
- **Requirements**: Anthropic API key
- **Cost**: Pay per token (see Anthropic pricing)
- **Best For**: API-based automation, CI/CD, headless environments

```yaml
# .giant-ai/agent.yml
provider: anthropic
anthropic_api_key: ${ANTHROPIC_API_KEY}
anthropic_model: claude-3-opus-20240229
anthropic_temperature: 0.7
anthropic_max_tokens: 4000
```

**Available Models:**
- `claude-3-opus-20240229` - Most capable
- `claude-3-sonnet-20240229` - Balanced performance/cost
- `claude-3-haiku-20240307` - Fast and affordable

**Use Cases:**
- When you need API access without browser auth
- CI/CD pipelines and automation
- Server-side applications
- When you want usage-based billing

**Pros:**
- Direct API access (no browser needed)
- Works in headless environments
- Usage-based pricing
- Same Claude models as claude-code

**Cons:**
- Requires API key
- Pay per token usage
- No direct file system access

### 4. Google Gemini
- **Provider ID**: `gemini`
- **Requirements**: Google AI API key
- **Cost**: Free tier available, then pay per use
- **Best For**: Cost-effective tasks, multimodal support

```yaml
# .giant-ai/agent.yml
provider: gemini
gemini_api_key: ${GEMINI_API_KEY}
gemini_model: gemini-pro
gemini_temperature: 0.7
gemini_max_tokens: 4000
```

**Available Models:**
- `gemini-pro` - Text generation
- `gemini-pro-vision` - Multimodal (future support)

**Pros:**
- Free tier available
- Good performance
- Competitive pricing

**Cons:**
- Newer, less proven for coding
- Limited model options
- No direct file system access

### 5. Ollama (Local Models)
- **Provider ID**: `ollama`
- **Requirements**: Ollama installed and running
- **Cost**: Free (you provide the hardware)
- **Best For**: Privacy-focused development, offline work, Jetson/edge devices

```yaml
# .giant-ai/agent.yml
provider: ollama
ollama_base_url: http://localhost:11434  # Or your Jetson IP
ollama_model: codellama  # Or any model you've pulled
ollama_temperature: 0.7
ollama_context_length: 4096
```

**Popular Models:**
- `llama2` - General purpose (7B, 13B, 70B)
- `codellama` - Code-optimized (7B, 13B, 34B)
- `mistral` - Fast and efficient (7B)
- `mixtral` - MoE architecture (8x7B)
- `deepseek-coder` - Specialized for code (1.3B, 6.7B, 33B)
- `phi-2` - Microsoft's small model (2.7B)

**Setup:**
1. Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
2. Pull a model: `ollama pull codellama`
3. Verify it's running: `ollama list`
4. Configure giant-ai to use it

**For Jetson Orin:**
```yaml
# Point to your Jetson's IP
ollama_base_url: http://192.168.1.100:11434
ollama_model: codellama:7b  # 7B fits well on Orin
```

**Pros:**
- Complete privacy - runs 100% locally
- No API costs ever
- Works offline
- You control the model
- Great for edge devices

**Cons:**
- Requires GPU/hardware
- Slower than cloud APIs
- Limited by local resources
- Model quality varies

## Authentication Methods

### Claude Code (Browser/SSO)
For Claude Code web users (including Enterprise/Team plans):

1. **First Time Setup**:
   ```bash
   # Install Claude CLI if not already installed
   npm install -g @anthropic-ai/claude-cli
   
   # First use will open browser for auth
   claude --version
   ```

2. **Authentication Flow**:
   - CLI opens your browser
   - Log in with your Claude account (or SSO)
   - CLI stores auth token locally
   - No API key needed!

3. **Verify Authentication**:
   ```bash
   # Test that it works
   echo "Hello" | claude --print
   ```

### API Keys (OpenAI, Anthropic API, Gemini)

#### Environment Variables (Recommended)
```bash
# Add to your ~/.bashrc, ~/.zshrc, or environment
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="AI..."
```

#### Direct Configuration
```yaml
# .giant-ai/agent.yml (be careful not to commit!)
openai_api_key: "sk-..."
anthropic_api_key: "sk-ant-..."
gemini_api_key: "AI..."
```

## Claude: Two Ways to Access

Giant AI provides two different providers for Claude:

| Feature | `claude-code` | `anthropic` |
|---------|--------------|-------------|
| **Authentication** | Browser/SSO/Desktop | API Key |
| **Billing** | Claude subscription | Pay per token |
| **Best For** | Interactive dev | Automation/CI/CD |
| **File Operations** | Native via CLI | JSON blocks |
| **Requires Browser** | First auth only | Never |

### When to Use Each:

**Use `claude-code` when:**
- You have a Claude Pro/Team subscription
- You're doing interactive development
- You want included usage (no per-token costs)
- You're OK with browser-based auth

**Use `anthropic` when:**
- You need headless/server operation
- You're building CI/CD pipelines
- You want precise usage tracking
- You prefer API key simplicity

## Provider Selection Strategy

### For Interactive Development
Choose **Claude Code** if:
- You have a Claude subscription
- You want included usage
- You prefer browser/SSO auth

Choose **API providers** if:
- You need headless operation
- You want usage-based billing
- You're automating workflows

## File Operations with API Providers

API providers (OpenAI, Anthropic, Gemini) handle file operations through JSON blocks:

```json
{
  "action": "create",
  "file": "src/new-feature.js",
  "content": "// File content here"
}
```

Giant AI automatically:
1. Parses these JSON blocks from responses
2. Executes file operations safely
3. Respects excluded paths and safety settings

## Cost Comparison

| Provider | Model | Input Cost | Output Cost | Free Tier |
|----------|-------|------------|-------------|-----------|
| Claude Code | Claude 3.5 Sonnet | Included | Included | With subscription |
| OpenAI | GPT-4 Turbo | $0.01/1K | $0.03/1K | No |
| OpenAI | GPT-3.5 | $0.0005/1K | $0.0015/1K | No |
| Anthropic | Claude 3 Opus | $0.015/1K | $0.075/1K | No |
| Anthropic | Claude 3 Sonnet | $0.003/1K | $0.015/1K | No |
| Gemini | Gemini Pro | Free* | Free* | 60 queries/min |

*Gemini has a generous free tier, then competitive pricing

**Note on Claude Code**: Whether you use Desktop, Web, or Enterprise SSO, the cost is included in your Claude subscription (Pro, Team, or Enterprise).

## Switching Providers

To switch providers, simply update your `.giant-ai/agent.yml`:

```bash
# Edit configuration
vim .giant-ai/agent.yml

# Change provider
provider: openai  # was claude-code

# Run agent with new provider
ai-agent task "Add user authentication"
```

## Troubleshooting

### API Key Issues
```bash
# Test API key is set
echo $OPENAI_API_KEY

# Verify in Python
python3 -c "import os; print('Key set:', bool(os.environ.get('OPENAI_API_KEY')))"
```

### Provider Not Found
```bash
# List available providers
ai-agent list-providers

# Should show: claude-code, openai, anthropic, gemini
```

### File Operations Not Working
- Check that Giant AI has proper permissions
- Verify excluded_paths in agent.yml
- Ensure JSON blocks are properly formatted in prompts

## Best Practices

1. **Start with Claude Code** for local development
2. **Use API providers** for CI/CD and automation
3. **Set temperature low (0.3-0.5)** for consistent code generation
4. **Monitor costs** with API providers
5. **Use environment variables** for API keys
6. **Test with smaller models first** (GPT-3.5, Gemini) before upgrading

## Future Providers

Planned support for:
- Local LLMs (Ollama, LLaMA)
- Azure OpenAI
- AWS Bedrock
- Custom endpoints

Stay tuned for updates!
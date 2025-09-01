# Anthropic Provider Comparison - Using Your Pro Max Plan

## Overview
There are two ways to use your Anthropic Pro Max plan with Giant AI, both providing unlimited usage without API tokens.

## Provider Options

### 1. claude-code (Recommended)
**What it is**: Claude CLI tool (`claude` command)
**Authentication**: `claude login` with your Anthropic account
**Platforms**: Mac, Windows, Linux
**Output**: Direct to terminal
**Best for**: Most users, automation, cross-platform work

```bash
ai-agent task "Your task" --provider claude-code
```

### 2. claude-desktop 
**What it is**: Claude Desktop application integration
**Authentication**: Logged into Claude Desktop app
**Platforms**: Mac only (uses AppleScript)
**Output**: Appears in Claude Desktop app
**Best for**: Mac users who prefer the desktop interface

```bash
ai-agent task "Your task" --provider claude-desktop
```

## Quick Comparison

| Feature | claude-code | claude-desktop |
|---------|------------|----------------|
| Uses Pro Max Plan | ✅ | ✅ |
| API Tokens Needed | ❌ | ❌ |
| Mac Support | ✅ | ✅ |
| Windows Support | ✅ | ❌ |
| Linux Support | ✅ | ❌ |
| Output Capture | ✅ | ❌ |
| Auto-accept | ✅ | ✅ |
| File Operations | ✅ | ✅ |

## Setting Your Default

Edit `.giant-ai/agent.yml`:
```yaml
provider: claude-code
```
or
```yaml  
provider: claude-desktop
```

## Authentication

### For claude-code:
```bash
claude login
```

### For claude-desktop:
Open Claude Desktop app and log in with your account.

## Both Use Your Pro Max Plan
Both providers leverage your Anthropic Pro Max subscription for unlimited usage without consuming API tokens. The main difference is the interface and platform support.
# Giant AI Commands & Location Cheat Sheet

## 🎯 Quick Reference: Where to Run What

### 🌍 **Global Commands (Run from ANYWHERE)**
These work from any directory once Giant AI is installed:

```bash
# System management
ai-setup                    # Install/update Giant AI system
ai-rag list-projects       # Show all indexed projects

# Project setup (run IN the project you want to set up)
ai-init-project-smart      # Smart project initialization
ai-init-project-smart --clean  # Clean reinit (overwrites existing)

# Search & analysis (run IN the project you want to search)
ai-search "query"          # Raw semantic search
ai-search-analyze "query" --analyze  # Search + AI analysis
ai-search-pipe "query"     # Simple pipe to AI (new, reliable)

# Agent mode (run IN the project you want to modify)
ai-agent task "description" --auto-accept  # Autonomous coding
ai-agent interactive       # Interactive agent mode

# Pattern refactoring (run IN the project you want to refactor)
ai-pattern-refactor analyze "pattern"      # Analyze patterns
ai-pattern-refactor refactor "pattern" --execute  # Apply refactoring
```

### 🏠 **Core Giant AI Directory Commands (cd ~/dotfiles/giant-ai-dev first)**
These must be run from the Giant AI source directory:

```bash
# Development & testing
./scripts/ai-setup         # Direct setup (bypass symlink issues)
git status                 # Check for changes to Giant AI itself
git pull                   # Update Giant AI source code

# When adding new tools or making changes to Giant AI itself:
git add .
git commit -m "Add new feature"
git push
```

### 📁 **Project Directory Commands (cd to your project first)**
These must be run from within a project you're working on:

```bash
# Project initialization
ai-init-project-smart      # Set up .giant-ai/ directory for this project
ai-init-project-smart --clean  # Reset project config

# Indexing & search  
ai-rag index .             # Index THIS project for semantic search
ai-rag index . --clear     # Rebuild index for THIS project
ai-search "auth patterns"  # Search THIS project
ai-search-analyze "caching" --analyze  # Analyze patterns in THIS project

# Agent mode for THIS project
ai-agent task "Add dark mode to settings" --auto-accept
ai-agent checkpoint "Before refactor"
ai-agent restore checkpoint_id

# Check project status
ls -la .giant-ai/          # Check project AI configuration
cat .giant-ai/context.md   # View project AI context
```

## 📍 **Command Location Matrix**

| Command | Global (anywhere) | Core Giant AI Dir | Project Dir | Notes |
|---------|-------------------|-------------------|-------------|-------|
| `ai-setup` | ✅ | ✅ (direct) | ✅ | Global system install/update |
| `ai-init-project-smart` | ❌ | ❌ | ✅ | Must be in target project |
| `ai-rag index .` | ❌ | ❌ | ✅ | Indexes current project |
| `ai-search "query"` | ❌ | ❌ | ✅ | Searches current project |
| `ai-agent task "..."` | ❌ | ❌ | ✅ | Modifies current project |
| `git commit` (giant-ai) | ❌ | ✅ | ❌ | Only for Giant AI development |

## 🔄 **Common Workflows**

### **🆕 Setting Up Giant AI (First Time)**
```bash
# 1. From anywhere:
cd ~/dotfiles/giant-ai-dev  # Go to Giant AI source
./scripts/ai-setup          # Install system globally

# 2. Verify installation:
which ai-setup              # Should show ~/.local/bin/ai-setup
ai-setup                    # Should work from anywhere now
```

### **📦 Setting Up a New Project**
```bash
# Must be in your project directory:
cd ~/my-awesome-project

# Initialize:
ai-init-project-smart       # Auto-detects language/framework
ai-rag index .              # Index for semantic search

# Test:
ai-search "main function"   # Should find code
```

### **🔧 Updating Giant AI System**
```bash
# 1. Update source (if you have changes):
cd ~/dotfiles/giant-ai-dev
git pull                    # Get latest changes

# 2. Reinstall system (from anywhere):
ai-setup                    # Updates all global commands
```

### **🔍 Daily Development Usage**
```bash
# In any project directory:
cd ~/my-project

# Search & analyze:
ai-search-analyze "error handling" --analyze  # Get AI insights
ai-search "database" --limit 10               # Quick search

# Autonomous coding:
ai-agent task "Add input validation to forms" --auto-accept

# Pattern refactoring:
ai-pattern-refactor analyze "API endpoints"
ai-pattern-refactor refactor "API endpoints" --execute
```

### **🛠️ Contributing to Giant AI**
```bash
# Must be in Giant AI source directory:
cd ~/dotfiles/giant-ai-dev

# Make changes, then:
git add .
git commit -m "Fix search integration"
git push

# Update your installation:
./scripts/ai-setup          # Or just: ai-setup (from anywhere)
```

## ⚠️ **Common Mistakes & Fixes**

### **"Command not found" errors:**
```bash
# Check if in PATH:
echo $PATH | grep -o '[^:]*\.local/bin[^:]*'

# If missing, add to shell config:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### **"No results found" errors:**
```bash
# Make sure project is indexed:
cd your-project-directory
ai-rag index .              # Index the project first
ai-rag list-projects        # Verify it's listed
```

### **"Directory not found" during setup:**
```bash
# If ai-setup fails, run directly:
cd ~/dotfiles/giant-ai-dev
./scripts/ai-setup
```

### **Wrong project being searched:**
```bash
# Always cd to project first:
cd ~/correct-project        # ← Important!
ai-search "your query"      # Searches THIS project, not previous one
```

## 🎯 **Memory Aids**

### **"Where am I?" Quick Check**
```bash
pwd                         # Current directory
ls -la .giant-ai/          # Am I in a Giant AI project? (shows config)
ai-rag list-projects       # What projects are indexed?
which ai-setup             # Is Giant AI installed globally?
```

### **"What can I do here?" Quick Check**
```bash
# In any directory:
ai-setup                    # Always works (global)

# In a project directory:
ls .giant-ai/               # If exists: can use ai-search, ai-agent
ai-rag index .              # If no .giant-ai: run this first

# In Giant AI source directory:
git status                  # Check for Giant AI development changes
./scripts/ai-setup          # Direct setup bypass
```

## 🚀 **Power User Tips**

### **Batch Project Setup**
```bash
# Set up multiple projects quickly:
for project in ~/projects/*/; do
  cd "$project"
  if [ -f "package.json" ] || [ -f "*.py" ]; then
    echo "Setting up: $project"
    ai-init-project-smart
    ai-rag index .
  fi
done
```

### **Quick Status Check**
```bash
# Add to your shell aliases:
alias giant-status='pwd && ls -la .giant-ai/ 2>/dev/null && ai-rag list-projects'
```

### **Project Context Switching**
```bash
# Add project-aware prompt:
# In .bashrc/.zshrc:
export PS1='[\W$([ -d .giant-ai ] && echo " 🤖" || echo "")] $ '
# Shows 🤖 when in a Giant AI enabled project
```

---

## 📋 **TL;DR - The Essentials**

```bash
# Setup (run once):
cd ~/dotfiles/giant-ai-dev && ./scripts/ai-setup

# Per project (run in each project):
cd ~/my-project
ai-init-project-smart && ai-rag index .

# Daily usage (run in project):
ai-search-analyze "your query" --analyze   # Most useful command

# Updates (run from anywhere):
ai-setup   # Update Giant AI system
```

**Remember**: Most commands work in your PROJECT directory, not the Giant AI source directory!
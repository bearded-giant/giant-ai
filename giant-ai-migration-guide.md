# Giant AI Migration Guide
## Upgrading from .ai-setup to .giant-ai

This guide helps you migrate existing projects from the old `.ai-setup` directory structure to the new `.giant-ai` naming convention.

## 🔄 Quick Migration (Recommended)

For most projects, the simplest approach is to re-initialize:

```bash
# 1. Navigate to your existing project
cd your-project

# 2. Remove old configuration (backup important customizations first!)
rm -rf .ai-setup

# 3. Re-initialize with new smart detection
ai-init-project-smart

# 4. Re-index for RAG search
ai-rag index .
```

**This approach:**
- ✅ Uses the latest smart auto-detection
- ✅ Generates optimized configuration based on current codebase
- ✅ Ensures compatibility with all new features
- ⚠️ Requires re-customizing any manual edits to context.md

## 📋 Manual Migration (Preserve Customizations)

If you have heavily customized `.ai-setup/context.md` or other configuration files:

### Step 1: Backup Your Customizations
```bash
# Create backup of your customizations
cp -r .ai-setup .ai-setup-backup
```

### Step 2: Extract Key Customizations
Review and extract your customizations from:
- `.ai-setup/context.md` - Project-specific AI instructions
- `.ai-setup/conventions.yml` - Custom coding standards
- `.ai-setup/mcp/server.js` - Custom MCP tools (if any)

### Step 3: Clean Migration
```bash
# Remove old directory
rm -rf .ai-setup

# Initialize new structure
ai-init-project-smart

# Re-index with new paths
ai-rag index .
```

### Step 4: Restore Customizations
```bash
# Edit the new context file
code .giant-ai/context.md
# Merge your custom content from .ai-setup-backup/context.md

# Edit conventions if you had custom ones
code .giant-ai/conventions.yml
# Merge from .ai-setup-backup/conventions.yml

# Copy custom MCP server if you had one
cp .ai-setup-backup/mcp/server.js .giant-ai/mcp/server.js
```

### Step 5: Clean Up
```bash
# Remove backup once migration is verified
rm -rf .ai-setup-backup
```

## 🔍 What Changed

### Directory Structure
```diff
your-project/
- ├── .ai-setup/              # OLD
+ ├── .giant-ai/              # NEW
-    ├── context.md
+    ├── context.md           # Same content, new location
-    ├── conventions.yml
+    ├── conventions.yml      # Same content, new location  
-    └── mcp/
+    └── mcp/                 # Same structure, new location
-        └── server.js
+        └── server.js
```

### RAG Database Location
```diff
- ~/.ai-dev/rag/db/          # OLD location
+ ~/.giant-ai/rag/db/        # NEW location
```

### Tool Names (Unchanged)
- `ai-setup` - Still the same
- `ai-init-project` - Still the same
- `ai-rag` - Still the same
- `ai-search` - Still the same

## 🚨 Important Notes

### RAG Index Migration
**Your existing RAG indexes will be rebuilt** because:
- New location: `~/.giant-ai/rag/db/` instead of `~/.ai-dev/rag/db/`
- Improved indexing with latest optimizations
- Better project isolation

**Impact:** First search after migration will need re-indexing (run `ai-rag index .`)

### Git Integration
**Update your .gitignore:**
```diff
# Remove old entry (if present)
- .ai-setup/rag/db/

# Add new entry
+ .giant-ai/rag/db/
```

### Neovim Users
**Update your Neovim configuration:**
```diff
servers = {
  ["project-context"] = {
    command = "node",
-   args = { "./.ai-setup/mcp/server.js" },
+   args = { "./.giant-ai/mcp/server.js" },
    auto_start = true,
  },
},
```

### MCP Hub Configuration
**The global MCP hub config is automatically updated** when you run the new `ai-setup` script.

## 📊 Migration Checklist

### Per-Project Migration
- [ ] Backup `.ai-setup/` customizations (if any)
- [ ] Remove old `.ai-setup/` directory
- [ ] Run `ai-init-project-smart`
- [ ] Restore custom content to `.giant-ai/context.md`
- [ ] Re-index project: `ai-rag index .`
- [ ] Update `.gitignore` if needed
- [ ] Test AI integration: `ai-search "test query"`

### Global System Migration  
- [ ] Run `ai-setup` to update global configuration
- [ ] Update Neovim MCP server paths (if using)
- [ ] Verify CLI tools work: `ai-rag list-projects`

### Validation
- [ ] AI CLI recognizes project context: `claude` (should load .giant-ai/context.md)
- [ ] RAG search works: `ai-search "function" . 5`
- [ ] MCP tools accessible in Neovim (if configured)
- [ ] Agent mode works: `ai-agent task "test task" --dry-run`

## 🔧 Troubleshooting

### "No projects indexed yet"
```bash
# Re-index your projects
ai-rag index .
ai-rag list-projects  # Should show your project
```

### "MCP server not found"
```bash
# Check if .giant-ai/mcp/server.js exists
ls -la .giant-ai/mcp/

# If missing, re-run initialization
ai-init-project-smart
```

### AI CLI doesn't load project context
```bash
# Verify context file exists
cat .giant-ai/context.md

# Check file permissions
ls -la .giant-ai/
```

### Neovim integration broken
1. Update MCP server paths in your Neovim config
2. Restart Neovim
3. Check `:ClaudeStatus` or equivalent

## 💡 Migration Tips

### For Teams
1. **Coordinate migration** - Have all team members migrate together
2. **Update documentation** - Update any team docs with new paths
3. **Commit new structure** - Commit `.giant-ai/` to your repo
4. **Share migration guide** - Send this guide to your team

### For CI/CD
```bash
# Update any CI scripts that reference .ai-setup
sed -i 's/\.ai-setup/\.giant-ai/g' .github/workflows/*.yml
```

### For Multiple Projects
```bash
# Script to migrate all projects in a directory
find ~/projects -name ".ai-setup" -type d | while read dir; do
  project_dir=$(dirname "$dir")
  echo "Migrating $project_dir"
  cd "$project_dir"
  rm -rf .ai-setup
  ai-init-project-smart
  ai-rag index .
done
```

## 🎯 Benefits of Migration

### Improved Features
- **Smarter auto-detection** - Better language/framework recognition
- **Enhanced MCP integration** - More robust tool ecosystem
- **Optimized RAG indexing** - Faster and more accurate search
- **Better agent mode** - Enhanced autonomous coding capabilities

### Simplified Naming
- **Shorter paths** - `.giant-ai` vs `.ai-setup`
- **Consistent branding** - Aligns with "Giant AI" project name
- **Clearer purpose** - Directory name reflects the tool ecosystem

---

## 🚀 Quick Start After Migration

Once migrated, verify everything works:

```bash
# Test the full workflow
cd your-project

# 1. Context loading
claude "What kind of project is this?"  # Should understand your project

# 2. Semantic search  
ai-search "error handling" . 5         # Should find relevant code

# 3. Agent mode
ai-agent task "Add a simple test" --dry-run  # Should plan the task

# 4. Neovim integration (if configured)
nvim                                    # Open file and test <leader>cc
```

**Everything working? You're successfully migrated! 🎉**

---

**Need help?** Open an issue at: https://github.com/your-org/giant-ai/issues
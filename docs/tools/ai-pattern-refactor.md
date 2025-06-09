# AI Pattern Refactor - Semantic Code Refactoring

AI Pattern Refactor uses RAG (semantic search) to find and refactor similar code patterns across your entire codebase, ensuring consistency and best practices.

## Overview

Traditional refactoring tools work on exact text matches or AST patterns. AI Pattern Refactor:
- **Finds semantically similar code** even with different variable names or structures
- **Analyzes patterns** to understand commonalities and variations
- **Applies consistent refactoring** across all matching code
- **Creates backups** before making any changes
- **Provides dry-run mode** to preview changes

## Installation

The tool is automatically installed when you run `ai-setup`. To install manually:

```bash
cd giant-ai-dev
./scripts/ai-setup
```

This creates the `ai-pattern-refactor` command in your PATH.

## Usage

### Basic Commands

#### 1. Analyze Patterns (Read-Only)
```bash
# Find and analyze similar patterns without making changes
ai-pattern-refactor analyze "error handling"

# Adjust similarity threshold (0-1, lower is more similar)
ai-pattern-refactor analyze "database queries" --threshold 0.3

# Limit number of files analyzed
ai-pattern-refactor analyze "authentication" --limit 10
```

#### 2. Dry Run (Preview Changes)
```bash
# Default mode - shows what would be changed
ai-pattern-refactor refactor "error handling" --dry-run

# Or simply (dry-run is default)
ai-pattern-refactor refactor "error handling"
```

#### 3. Execute Refactoring
```bash
# Actually apply the refactoring (creates backup first)
ai-pattern-refactor refactor "error handling" --execute

# Auto-accept all changes without prompting
ai-pattern-refactor refactor "error handling" --execute --auto-accept

# Use a target pattern file
ai-pattern-refactor refactor "error handling" \
  --target-pattern patterns/error-handling-consistent.js \
  --execute
```

### Advanced Usage

#### Using Target Patterns
Target patterns provide a template for how refactored code should look:

```bash
# Standardize all API endpoints to match a pattern
ai-pattern-refactor refactor "API endpoints" \
  --target-pattern patterns/api-endpoint-pattern.ts \
  --execute

# Convert promise chains to async/await
ai-pattern-refactor refactor "promise chains" \
  --target-pattern patterns/async-await-pattern.js \
  --execute
```

#### Managing Backups
```bash
# List all backups
ai-pattern-refactor backup --list

# Restore from a specific backup
ai-pattern-refactor backup --restore /path/to/backup

# Backups are automatically created before any refactoring
```

#### Fine-Tuning Search
```bash
# Very similar patterns only (threshold closer to 0)
ai-pattern-refactor refactor "validation logic" --threshold 0.2

# Broader pattern matching (threshold closer to 1)
ai-pattern-refactor refactor "utility functions" --threshold 0.6

# Search in specific project
ai-pattern-refactor refactor "tests" --project-path ../other-project
```

## Examples

### Example 1: Standardize Error Handling

```bash
# First, analyze existing error handling patterns
ai-pattern-refactor analyze "try catch error handling"

# Output shows various error handling approaches:
# - Some use console.log
# - Some use custom logger
# - Some don't log at all
# - Different error formats

# Apply consistent error handling pattern
ai-pattern-refactor refactor "try catch error handling" \
  --target-pattern patterns/error-handling-consistent.js \
  --execute
```

### Example 2: Modernize Async Code

```bash
# Find all promise-based code
ai-pattern-refactor analyze "then().catch() promises"

# Convert to async/await pattern
ai-pattern-refactor refactor "then().catch() promises" \
  --target-pattern patterns/async-await-pattern.js \
  --execute --auto-accept
```

### Example 3: Refactor Authentication Patterns

```bash
# Find all authentication-related code
ai-pattern-refactor analyze "authentication middleware check user"

# See what patterns exist
# Then refactor to consistent approach
ai-pattern-refactor refactor "authentication middleware" \
  --threshold 0.3 \
  --execute
```

### Example 4: Database Query Patterns

```bash
# Analyze database query patterns
ai-pattern-refactor analyze "database SELECT query"

# Standardize to use query builder pattern
ai-pattern-refactor refactor "raw SQL queries" \
  --target-pattern patterns/query-builder.js \
  --execute
```

## How It Works

1. **Semantic Search**: Uses RAG to find code semantically similar to your query
2. **Pattern Analysis**: LLM analyzes the found code to identify:
   - Common patterns across files
   - Variations that should be preserved
   - Refactoring opportunities
3. **Plan Generation**: Creates a refactoring plan with risk assessment
4. **Safe Execution**: 
   - Creates backup before any changes
   - Applies refactoring file by file
   - Allows manual review (unless --auto-accept)
   - Provides rollback capability

## Pattern Files

Pattern files in `patterns/` directory provide templates for common refactoring scenarios:

- `error-handling-consistent.js` - Standardized error handling with logging
- `async-await-pattern.js` - Modern async/await instead of promises
- `api-endpoint-pattern.ts` - Consistent REST API endpoint structure
- Add your own patterns for project-specific conventions

## Safety Features

1. **Automatic Backups**: Every refactoring creates a timestamped backup
2. **Dry Run Default**: Won't make changes without explicit --execute flag
3. **Manual Review**: Prompts for each file unless --auto-accept
4. **Risk Assessment**: Shows risk level (low/medium/high) for each file
5. **Restore Capability**: Can restore from any backup

## Configuration

### Project Configuration
Create `.ai-setup/tools.yml` for project-specific settings:

```yaml
tools:
  ai-pattern-refactor:
    # Default similarity threshold
    similarity_threshold: 0.4
    
    # Always create backups
    auto_backup: true
    
    # Require confirmation for high-risk files
    confirmation_required: true
    
    # Exclude patterns
    exclude_patterns:
      - "*.test.js"
      - "*.spec.ts"
```

### Global Configuration
Set defaults in `~/.ai-setup/tools.yml`:

```yaml
ai-pattern-refactor:
  default_threshold: 0.4
  max_files_per_refactor: 50
  backup_retention_days: 30
```

## Troubleshooting

### No patterns found
- Try adjusting threshold (lower = more similar)
- Use more specific search terms
- Check if project is indexed: `ai-rag index .`

### Refactoring seems incorrect
- Use a target pattern file for better guidance
- Review and adjust the analysis before executing
- Start with a smaller scope (fewer files)

### Performance issues
- Limit number of files with --limit flag
- Use more specific queries
- Ensure RAG index is up to date

## Best Practices

1. **Start with Analysis**: Always analyze patterns first to understand scope
2. **Use Dry Run**: Preview changes before executing
3. **Target Patterns**: Provide clear examples of desired outcome
4. **Incremental Refactoring**: Start with low-risk files
5. **Review Changes**: Use version control to review refactoring results
6. **Keep Backups**: Don't delete backups until changes are verified

## Integration with Other Tools

Works seamlessly with Giant AI Dev ecosystem:
- Uses **RAG indexes** for semantic search
- Integrates with **agent mode** for complex refactoring
- Respects **project conventions** from .ai-setup/
- Can be used in **CI/CD pipelines** for code quality

## Future Enhancements

Planned improvements:
- Language-specific refactoring patterns
- Integration with test runners to verify refactoring
- Batch refactoring with multiple patterns
- Visual diff preview before applying changes
- Integration with popular IDEs
# Context Management Explained - How AI Decides What Code Matters

## The Magic Users See

When you work with AI coding assistants, you experience:
- **"AI understands my project"** - Suggestions match your coding style
- **"Responses get worse over time"** - Later responses seem generic or off-target  
- **"AI forgot what we discussed"** - Earlier conversation context disappears
- **"Some sessions are much better"** - Inconsistent quality between conversations
- **"AI knows which files are relevant"** - Finds related code across your project

**What appears to happen:** AI has mysterious and inconsistent understanding of your codebase.

## What's Really Happening

Behind the scenes, AI assistants face **fundamental limitations** in managing context:

1. **Context window limits** - AI can only "see" a fixed amount of text at once
2. **Relevance algorithms** - Systems must choose what code to include
3. **Token counting** - Every character consumes limited "thinking space"
4. **Chunking strategies** - Large files get broken into pieces
5. **Memory degradation** - Long conversations lose early context
6. **Context competition** - Your code competes with conversation history for space

### The Context Window Problem

```
Context Window = 128k tokens ≈ 100k words ≈ 300-500 files worth of code

Your codebase: 2,000 files, 50k lines
AI can see: ~500 lines at once (0.1% of your code)
```

**The challenge:** How does AI choose which 0.1% of your code to look at?

## Giant AI's Context Management Strategy

Let's examine how Giant AI solves context management:

### 1. Project-Aware Context Loading

From `scripts/ai-init-project-smart`:
```bash
# Smart detection creates focused context
detect_language() {
    # Analyzes file counts and config files
    local js_files=$(find "$PROJECT_DIR" -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" | wc -l)
    local py_files=$(find "$PROJECT_DIR" -name "*.py" | wc -l)
    
    # Prioritizes config files over raw counts
    if [ -f "$PROJECT_DIR/package.json" ]; then
        primary_lang="javascript"
    elif [ -f "$PROJECT_DIR/Cargo.toml" ]; then
        primary_lang="rust"
    fi
}
```

**Result:** AI gets **structured project understanding** instead of random file reads.

### 2. Intelligent Chunking with RAG

From `rag/indexer.py`:
```python
def prepare_file_fast(self, file_path):
    """Fast mode - index entire file as one document with smart context"""
    content = file_path.read_text(encoding='utf-8')
    
    # Extract key components for metadata
    functions = []
    classes = []
    if file_path.suffix == '.py' and self.parser:
        tree = self.parser.parse(bytes(content, "utf8"))
        functions, classes = self.extract_python_symbols(tree.root_node, content)
    
    # Create document with rich metadata
    metadata = {
        'file_path': str(file_path.relative_to(self.project_path)),
        'file_type': file_path.suffix,
        'functions': json.dumps(functions[:20]),  # Top functions
        'classes': json.dumps(classes[:10]),      # Top classes
        'line_count': len(content.split('\n'))
    }
    
    return content, metadata, doc_id
```

**What this does:**
- **Tree-sitter parsing** understands code structure, not just text
- **Metadata enrichment** adds function/class information for better search
- **Semantic chunking** preserves logical code boundaries

### 3. Context Layering Strategy

Giant AI uses a **layered context approach**:

```
Layer 1: Project conventions (.giant-ai/conventions.yml)
    ↓
Layer 2: Architecture overview (.giant-ai/context.md)  
    ↓
Layer 3: Semantic search results (relevant code via RAG)
    ↓
Layer 4: Current file/selection context
    ↓
Layer 5: Conversation history (recent only)
```

**Example from MCP server** (`mcp/project-server.js`):
```javascript
async getProjectContext(projectPath) {
    // Layer 1: Local project context
    const localContext = path.join(targetPath, '.giant-ai', 'context.md');
    let context = await fs.readFile(localContext, 'utf-8');
    
    // Layer 2: Project conventions
    const conventionsPath = path.join(targetPath, '.giant-ai', 'conventions.yml');
    const conventions = await fs.readFile(conventionsPath, 'utf-8');
    context += "\n\n## Project Conventions\n" + yaml.stringify(parsed);
    
    return context;
}
```

## Context Window Optimization Techniques

### Smart Context Selection

Instead of including random files, Giant AI uses **relevance ranking**:

```python
# From semantic search
def search(self, query, n_results=10):
    results = self.collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    # Returns most semantically relevant code
    return [
        {
            'content': doc,
            'metadata': meta,
            'distance': dist  # Semantic similarity score
        }
        for doc, meta, dist in zip(
            results['documents'][0],
            results['metadatas'][0], 
            results['distances'][0]
        )
    ]
```

**Real example:**
```bash
Query: "authentication middleware"
Results:
1. src/auth/middleware.js (distance: 0.12) ← Exact match
2. src/routes/protected.js (distance: 0.34) ← Uses auth
3. tests/auth.test.js (distance: 0.41) ← Tests auth
4. config/jwt.js (distance: 0.45) ← Auth config
```

**Traditional approach** might include:
- README.md (mentioned "auth" once)
- package.json (lists auth dependencies)  
- Random middleware files (same directory)

### Context Compression Strategies

#### 1. **Function-Level Extraction**
```javascript
// MCP tool: extract_function_context
async extractFunctionContext(filePath, lineNumber, projectPath) {
    // Find function boundaries using regex patterns
    for (let i = lineNumber; i >= 0; i--) {
        if (lines[i].match(/^(function|def|fn |class |impl |async fn)/)) {
            startLine = i;
            break;
        }
    }
    
    // Return just the relevant function, not entire file
    const functionCode = lines.slice(startLine, endLine).join('\n');
    return { file: filePath, line_range: [startLine, endLine], code: functionCode };
}
```

**Benefit:** 50-line function vs 2,000-line file (40x reduction in context usage)

#### 2. **Metadata-First Approach**
```python
# Instead of sending full file content
{
    "file_path": "src/auth.py",
    "functions": ["login", "logout", "verify_token", "refresh_token"],
    "classes": ["AuthManager", "JWTHandler"],
    "dependencies": ["jwt", "bcrypt", "redis"],
    "line_count": 450
}
```

**AI can reason about structure first, request specific functions second.**

## Why Responses Degrade Over Time

### The Context Window Fill-Up

```
Start of conversation:
[Project Context] [Relevant Code] [Available Space for Reasoning]
     20%              30%                      50%

After 10 exchanges:
[Project Context] [Conversation History] [New Code] [Reasoning Space]
     15%                45%                 25%           15%

After 20 exchanges:
[Conversation History] [Current Request] [Minimal Reasoning]
         75%                 20%                5%
```

**What happens:** AI "forgets" your project context as conversation history fills the window.

### Giant AI's Solutions

#### 1. **Session Boundaries**
```python
# From agent mode
def execute_task(self, task: str, options: Dict[str, Any] = None):
    if options.get("continue_session", False):
        # Keep conversation context
        task_context["session_history"] = self.session_log[-5:]  # Last 5 interactions
    else:
        # Fresh start with full project context
        task_context["project_context"] = self.context  # Full context reload
```

#### 2. **Context Refresh Commands**
```bash
# Neovim integration
vim.keymap.set('n', '<leader>rp', function()
    -- Refresh project context in AI conversation
    local context = mcp_call("get_project_context", { project_path = vim.fn.getcwd() })
    -- Start new conversation with fresh context
end)
```

## Practical Context Management Strategies

### For Users

#### 1. **Start Fresh When Quality Degrades**
```bash
# Signs you need a fresh start:
# - Generic responses
# - AI suggests patterns that don't match your project
# - AI asks for file contents it had earlier

# Solution:
# End current conversation, start new one
```

#### 2. **Provide Context Hints**
```bash
# Instead of:
"Fix this function"

# Better:
"Fix this authentication function - we use JWT tokens and Redis for sessions"
```

#### 3. **Use Semantic Search for Context Discovery**
```bash
# Before asking AI about complex topics:
ai-search "authentication patterns" . 5

# Then reference results in your AI conversation:
"Based on the auth patterns in src/auth/, how should I..."
```

### For Teams

#### 1. **Maintain Quality Context Files**
```yaml
# .giant-ai/conventions.yml - Keep this current
naming:
  files: kebab-case
  components: PascalCase
  
testing:
  framework: jest
  patterns: "tests alongside source files"
  
errors:
  logging: winston
  handling: "throw custom errors, catch at boundaries"
```

#### 2. **Document Architecture Decisions**
```markdown
# .giant-ai/context.md - Update after major changes
## Recent Architecture Changes
- Migrated from REST to GraphQL (Q2 2024)
- Added microservices for user management
- Switched from SQL to NoSQL for session storage

## Current Focus Areas
- Performance optimization
- Security hardening
- Mobile app API compatibility
```

## Real-World Context Management Examples

### Example 1: Large React Application

**Problem:** AI suggests class components in a hooks-based codebase
**Context Issue:** AI can't see enough examples to understand current patterns

**Giant AI Solution:**
```yaml
# .giant-ai/conventions.yml
react:
  component_style: "functional with hooks"
  state_management: "Redux Toolkit"
  styling: "styled-components"
  testing: "React Testing Library"
```

**Result:** AI suggestions match your patterns from conversation start.

### Example 2: Multi-Language Microservices

**Problem:** AI mixes Python and Node.js patterns when working on Go service
**Context Issue:** Semantic search returns results from all languages

**Giant AI Solution:**
```bash
# Project-specific indexing
cd user-service-go
ai-rag index . --clear  # Index only this service

# Search within service context
ai-search "API error handling" . 10  # Only Go results
```

### Example 3: Legacy Code Refactoring

**Problem:** AI suggests modern patterns that break legacy system constraints
**Context Issue:** Constraints not visible in code structure

**Giant AI Solution:**
```markdown
# .giant-ai/context.md
## Legacy Constraints
- Must support IE11 (no modern JS features)
- Cannot modify database schema (migrations forbidden)
- Third-party API rate limits: 100 requests/hour
- Memory limit: 512MB per container

## Refactoring Guidelines
- Incremental changes only
- Maintain backward compatibility
- Test on legacy browser stack
```

## Performance Optimization Tips

### Minimize Context Noise

#### 1. **Exclude Build Artifacts**
```bash
# .gitignore patterns also help AI focus
node_modules/
dist/
build/
*.pyc
__pycache__/
```

#### 2. **Use Focused Searches**
```bash
# Too broad (lots of irrelevant results)
ai-search "component" .

# Focused (relevant results)
ai-search "button component validation" ./src/components
```

#### 3. **Structure Context Files**
```markdown
# Good context structure
## Current Sprint Focus
- User authentication refactoring
- Performance optimization for search

## Implementation Guidelines
[Specific, actionable guidelines]

## Common Patterns
[Examples with code snippets]
```

### Monitor Context Usage

```bash
# Check conversation length
wc -w conversation.txt  # Rough token estimate

# Signs of context overflow:
# - AI asks for information provided earlier
# - Responses become generic
# - AI suggests outdated patterns
```

## The Bottom Line

**Context management is the hidden complexity behind AI coding assistance.**

### The Core Challenge
- **AI context windows are limited** (128k tokens ≈ 500 lines of code)
- **Your codebase is large** (thousands of files, millions of lines)
- **Relevance is subjective** (what's "related" depends on your task)

### Giant AI's Approach
- **Structured project understanding** via smart initialization
- **Semantic search** for relevance-based context selection  
- **Layered context** with conventions, architecture, and current focus
- **MCP tools** for efficient, targeted information retrieval
- **Session management** to prevent context degradation

### Best Practices
1. **Keep context files current** - Update .giant-ai/ files regularly
2. **Start fresh when quality degrades** - Don't fight context overflow
3. **Use semantic search** - Let RAG find relevant context for you
4. **Be specific in requests** - Help AI understand what context matters
5. **Structure your project** - Clear organization helps AI navigate

**The goal:** Transform AI from "smart autocomplete" to "project-aware assistant" through intelligent context management.
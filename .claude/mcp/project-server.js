#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import fs from 'fs/promises';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import yaml from 'yaml';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

class ProjectMCPServer {
  constructor(projectPath) {
    this.projectPath = projectPath || process.cwd();
    this.server = new Server(
      { name: "claude-project-context", version: "1.0.0" },
      { capabilities: { tools: {}, resources: {}, prompts: {} } }
    );
    this.setupHandlers();
  }

  setupHandlers() {
    this.server.setRequestHandler('tools/list', async () => ({
      tools: [
        {
          name: "analyze_codebase_structure",
          description: "Analyze project structure and detect patterns",
          inputSchema: {
            type: "object",
            properties: {
              focus: { 
                type: "string", 
                enum: ["dependencies", "architecture", "patterns", "config", "all"]
              },
              project_path: {
                type: "string",
                description: "Project path to analyze (optional, defaults to current)"
              }
            }
          }
        },
        {
          name: "get_proof_of_concept_template", 
          description: "Generate POC template based on tech stack",
          inputSchema: {
            type: "object",
            properties: {
              language: { type: "string", enum: ["rust", "javascript", "python", "go", "typescript"] },
              pattern: { type: "string", enum: ["api", "cli", "service", "library", "webapp"] }
            },
            required: ["language", "pattern"]
          }
        },
        {
          name: "extract_function_context",
          description: "Extract function/class with full context for analysis",
          inputSchema: {
            type: "object", 
            properties: {
              file_path: { type: "string" },
              line_number: { type: "number" },
              project_path: {
                type: "string",
                description: "Project path (optional)"
              }
            },
            required: ["file_path", "line_number"]
          }
        },
        {
          name: "semantic_code_search",
          description: "Search codebase using RAG semantic search",
          inputSchema: {
            type: "object",
            properties: {
              query: { type: "string" },
              limit: { type: "number", default: 10 },
              project_path: {
                type: "string",
                description: "Project path to search (optional)"
              }
            },
            required: ["query"]
          }
        },
        {
          name: "get_project_context",
          description: "Get project-specific context and conventions",
          inputSchema: {
            type: "object",
            properties: {
              project_path: {
                type: "string",
                description: "Project path (optional)"
              }
            }
          }
        }
      ]
    }));

    this.server.setRequestHandler('tools/call', async (request) => {
      const { name, arguments: args } = request.params;
      
      switch (name) {
        case "analyze_codebase_structure":
          return await this.analyzeCodebase(args.focus || "all", args.project_path);
        case "get_proof_of_concept_template":
          return await this.getPOCTemplate(args.language, args.pattern);
        case "extract_function_context":
          return await this.extractFunctionContext(args.file_path, args.line_number, args.project_path);
        case "semantic_code_search":
          return await this.semanticSearch(args.query, args.limit || 10, args.project_path);
        case "get_project_context":
          return await this.getProjectContext(args.project_path);
        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });

    // Add prompts handler
    this.server.setRequestHandler('prompts/list', async () => ({
      prompts: [
        {
          name: "architecture_review",
          description: "Perform architecture review of the project",
          arguments: [
            {
              name: "project_path",
              description: "Path to project to review",
              required: false
            }
          ]
        },
        {
          name: "poc_planning", 
          description: "Plan a proof of concept implementation",
          arguments: [
            {
              name: "feature",
              description: "Feature to create POC for",
              required: true
            }
          ]
        }
      ]
    }));

    this.server.setRequestHandler('prompts/get', async (request) => {
      const { name, arguments: args } = request.params;
      
      switch (name) {
        case "architecture_review":
          return await this.getArchitectureReviewPrompt(args?.project_path);
        case "poc_planning":
          return await this.getPOCPlanningPrompt(args?.feature);
        default:
          throw new Error(`Unknown prompt: ${name}`);
      }
    });
  }

  async analyzeCodebase(focus, projectPath) {
    const targetPath = projectPath || this.projectPath;
    const analysis = {};
    
    if (focus === "all" || focus === "dependencies") {
      analysis.dependencies = {
        npm: await this.getPackageJson(targetPath),
        cargo: await this.getCargoToml(targetPath),
        python: await this.getRequirementsTxt(targetPath),
        go: await this.getGoMod(targetPath)
      };
    }
    
    if (focus === "all" || focus === "architecture") {
      analysis.architecture = {
        structure: await this.getDirectoryStructure(targetPath),
        entry_points: await this.findEntryPoints(targetPath),
        config_files: await this.findConfigFiles(targetPath)
      };
    }
    
    if (focus === "all" || focus === "patterns") {
      analysis.patterns = {
        detected: await this.detectCodePatterns(targetPath),
        conventions: await this.analyzeConventions(targetPath)
      };
    }
    
    if (focus === "all" || focus === "config") {
      analysis.config = {
        env_files: await this.findFiles(targetPath, ['.env*', '*.yml', '*.yaml', '*.toml']),
        docker: await this.getDockerInfo(targetPath),
        ci_cd: await this.getCICDInfo(targetPath)
      };
    }
    
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          focus,
          timestamp: new Date().toISOString(),
          project_path: targetPath,
          analysis
        }, null, 2)
      }]
    };
  }

  async getPOCTemplate(language, pattern) {
    const templatesPath = path.join(__dirname, '../templates/poc-templates.json');
    let templates = {};
    
    try {
      const templatesContent = await fs.readFile(templatesPath, 'utf-8');
      templates = JSON.parse(templatesContent);
    } catch {
      // Use default templates if file doesn't exist
      templates = this.getDefaultTemplates();
    }
    
    const template = templates[language]?.[pattern] || "# POC Template not found";
    
    return {
      content: [{
        type: "text",
        text: template
      }]
    };
  }

  async extractFunctionContext(filePath, lineNumber, projectPath) {
    const targetPath = projectPath || this.projectPath;
    
    try {
      const fullPath = path.isAbsolute(filePath) 
        ? filePath 
        : path.join(targetPath, filePath);
        
      const content = await fs.readFile(fullPath, 'utf-8');
      const lines = content.split('\n');
      
      let startLine = Math.max(0, lineNumber - 10);
      let endLine = Math.min(lines.length, lineNumber + 20);
      
      // Find function/class boundaries
      for (let i = lineNumber; i >= 0; i--) {
        if (lines[i].match(/^(function|def|fn |class |impl |async fn|const |export |interface |type )/)) {
          startLine = i;
          break;
        }
      }
      
      // Find end of function/class
      let braceCount = 0;
      let foundStart = false;
      for (let i = startLine; i < lines.length; i++) {
        const line = lines[i];
        if (line.includes('{')) {
          braceCount++;
          foundStart = true;
        }
        if (line.includes('}')) {
          braceCount--;
        }
        if (foundStart && braceCount === 0) {
          endLine = i + 1;
          break;
        }
      }
      
      const functionCode = lines.slice(startLine, endLine).join('\n');
      
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            file: filePath,
            line_range: [startLine + 1, endLine],
            code: functionCode,
            context: "Function/class context extracted for analysis"
          }, null, 2)
        }]
      };
    } catch (error) {
      throw new Error(`Failed to extract context: ${error.message}`);
    }
  }

  async semanticSearch(query, limit, projectPath) {
    const targetPath = projectPath || this.projectPath;
    
    try {
      // Call the Python RAG search
      const searchScript = path.join(__dirname, '../rag/search.py');
      const cmd = `python3 "${searchScript}" "${query}" "${targetPath}" ${limit} json`;
      const output = execSync(cmd, { encoding: 'utf-8' });
      
      return {
        content: [{
          type: "text",
          text: output
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            error: "Search failed",
            message: error.message,
            hint: "Make sure the project is indexed using: claude-rag index <project-path>"
          }, null, 2)
        }]
      };
    }
  }

  async getProjectContext(projectPath) {
    const targetPath = projectPath || this.projectPath;
    
    // Check for local .claude/context.md first
    const localContext = path.join(targetPath, '.claude', 'context.md');
    const globalContext = path.join(__dirname, '../templates', 'default-context.md');
    
    try {
      let context = "";
      
      // Try local context first
      try {
        context = await fs.readFile(localContext, 'utf-8');
      } catch {
        // Fall back to global default
        try {
          context = await fs.readFile(globalContext, 'utf-8');
        } catch {
          context = "No project context found. Create .claude/context.md in your project.";
        }
      }
      
      // Also check for local .claude/conventions.yml
      try {
        const conventionsPath = path.join(targetPath, '.claude', 'conventions.yml');
        const conventions = await fs.readFile(conventionsPath, 'utf-8');
        const parsed = yaml.parse(conventions);
        
        context += "\n\n## Project Conventions\n";
        context += yaml.stringify(parsed);
      } catch {
        // No conventions file
      }
      
      return {
        content: [{
          type: "text",
          text: context
        }]
      };
    } catch (error) {
      throw new Error(`Failed to get project context: ${error.message}`);
    }
  }

  async getArchitectureReviewPrompt(projectPath) {
    const analysis = await this.analyzeCodebase("all", projectPath);
    const prompt = `
# Architecture Review

Based on the following project analysis, provide a comprehensive architecture review:

${analysis.content[0].text}

Focus on:
1. Design patterns and their effectiveness
2. Dependency management and potential issues
3. Scalability considerations
4. Code organization and maintainability
5. Security implications
6. Performance bottlenecks
7. Testing strategy

Provide specific, actionable recommendations.
`;
    
    return {
      description: "Architecture review prompt with project analysis",
      messages: [{
        role: "user",
        content: {
          type: "text",
          text: prompt
        }
      }]
    };
  }

  async getPOCPlanningPrompt(feature) {
    return {
      description: "POC planning prompt",
      messages: [{
        role: "user", 
        content: {
          type: "text",
          text: `
# Proof of Concept Planning: ${feature}

Create a detailed POC plan for implementing "${feature}". Include:

1. **Objective**: Clear statement of what we're proving/testing
2. **Hypothesis**: What we expect to learn
3. **Technical Approach**:
   - Technology choices and rationale
   - Architecture decisions
   - Integration points
4. **Implementation Steps**:
   - Ordered list of development tasks
   - Time estimates for each
5. **Success Criteria**:
   - Measurable outcomes
   - Performance benchmarks if applicable
6. **Risks and Mitigations**:
   - Technical risks
   - Mitigation strategies
7. **Next Steps**:
   - How to evolve POC to production
   - Scaling considerations

Keep the scope minimal but representative of the full solution.
`
        }
      }]
    };
  }

  // Helper methods
  async getPackageJson(targetPath) {
    try {
      const content = await fs.readFile(path.join(targetPath, 'package.json'), 'utf-8');
      return JSON.parse(content);
    } catch { return null; }
  }

  async getCargoToml(targetPath) {
    try {
      return await fs.readFile(path.join(targetPath, 'Cargo.toml'), 'utf-8');
    } catch { return null; }
  }

  async getRequirementsTxt(targetPath) {
    try {
      return await fs.readFile(path.join(targetPath, 'requirements.txt'), 'utf-8');
    } catch { return null; }
  }

  async getGoMod(targetPath) {
    try {
      return await fs.readFile(path.join(targetPath, 'go.mod'), 'utf-8');
    } catch { return null; }
  }

  async getDirectoryStructure(targetPath) {
    try {
      const cmd = `find "${targetPath}" -type d -name .git -prune -o -type d -print | grep -v node_modules | head -30`;
      return execSync(cmd, { encoding: 'utf-8' }).trim().split('\n');
    } catch { return []; }
  }

  async findEntryPoints(targetPath) {
    const patterns = ['main.js', 'index.js', 'app.js', 'main.py', '__main__.py', 'main.rs', 'main.go', 'cmd/*/main.go'];
    const found = [];
    
    for (const pattern of patterns) {
      try {
        if (pattern.includes('*')) {
          const files = execSync(`find "${targetPath}" -path "*/${pattern}" -type f 2>/dev/null`, { encoding: 'utf-8' })
            .trim().split('\n').filter(Boolean);
          found.push(...files.map(f => path.relative(targetPath, f)));
        } else {
          await fs.access(path.join(targetPath, pattern));
          found.push(pattern);
        }
      } catch {}
    }
    
    return found;
  }

  async detectCodePatterns(targetPath) {
    const patterns = [];
    
    if (await this.dirExists(targetPath, 'src/routes') || await this.dirExists(targetPath, 'routes')) {
      patterns.push('MVC/Routes pattern');
    }
    if (await this.dirExists(targetPath, 'src/models') || await this.dirExists(targetPath, 'models')) {
      patterns.push('Model layer pattern');
    }
    if (await this.dirExists(targetPath, 'src/services') || await this.dirExists(targetPath, 'services')) {
      patterns.push('Service layer pattern');
    }
    if (await this.dirExists(targetPath, 'src/components') || await this.dirExists(targetPath, 'components')) {
      patterns.push('Component-based architecture');
    }
    if (await this.fileExists(targetPath, 'docker-compose.yml') || await this.fileExists(targetPath, 'Dockerfile')) {
      patterns.push('Containerized application');
    }
    
    return patterns;
  }

  async analyzeConventions(targetPath) {
    // Try to detect naming conventions
    const conventions = [];
    
    try {
      // Check JS/TS files for naming patterns
      const jsFiles = execSync(`find "${targetPath}" -name "*.js" -o -name "*.ts" | head -10`, { encoding: 'utf-8' })
        .trim().split('\n').filter(Boolean);
      
      if (jsFiles.some(f => f.includes('-'))) {
        conventions.push("kebab-case file naming");
      }
      if (jsFiles.some(f => /[A-Z]/.test(path.basename(f)))) {
        conventions.push("PascalCase components");
      }
    } catch {}
    
    return conventions;
  }

  async dirExists(targetPath, dir) {
    try {
      const stats = await fs.stat(path.join(targetPath, dir));
      return stats.isDirectory();
    } catch { return false; }
  }

  async fileExists(targetPath, file) {
    try {
      await fs.access(path.join(targetPath, file));
      return true;
    } catch { return false; }
  }

  async findFiles(targetPath, patterns) {
    try {
      const cmd = `find "${targetPath}" -type f \\( ${patterns.map(p => `-name "${p}"`).join(' -o ')} \\) | grep -v node_modules`;
      return execSync(cmd, { encoding: 'utf-8' }).trim().split('\n').filter(Boolean);
    } catch { return []; }
  }

  async findConfigFiles(targetPath) {
    return await this.findFiles(targetPath, ['*.config.js', '*.config.json', 'Dockerfile', '.env*', '*.yml', '*.yaml']);
  }

  async getDockerInfo(targetPath) {
    const dockerFiles = await this.findFiles(targetPath, ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml']);
    return dockerFiles.length > 0 ? { containerized: true, files: dockerFiles } : null;
  }

  async getCICDInfo(targetPath) {
    const ciFiles = await this.findFiles(targetPath, ['.github/workflows/*.yml', '.gitlab-ci.yml', 'Jenkinsfile', '.circleci/config.yml']);
    return ciFiles.length > 0 ? { ci_cd: true, files: ciFiles } : null;
  }

  getDefaultTemplates() {
    return {
      rust: {
        api: `use axum::{routing::get, Router, Json};
use serde::{Deserialize, Serialize};
use tokio::net::TcpListener;

#[derive(Serialize, Deserialize)]
struct ApiResponse {
    message: String,
    data: Option<serde_json::Value>,
}

async fn health_check() -> Json<ApiResponse> {
    Json(ApiResponse {
        message: "POC API is running".to_string(),
        data: None,
    })
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/health", get(health_check));
    
    let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();
    println!("POC server running on http://0.0.0.0:3000");
    
    axum::serve(listener, app).await.unwrap();
}`,
        cli: `use clap::{Arg, Command};

fn main() {
    let matches = Command::new("poc-cli")
        .version("1.0")
        .about("Proof of concept CLI tool")
        .arg(Arg::new("input")
            .short('i')
            .long("input")
            .value_name("FILE")
            .help("Input file to process"))
        .get_matches();

    if let Some(input) = matches.get_one::<String>("input") {
        println!("Processing file: {}", input);
    }
}`
      },
      javascript: {
        api: `const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({
    message: 'POC API is running',
    timestamp: new Date().toISOString()
  });
});

app.listen(port, () => {
  console.log(\`POC server running on port \${port}\`);
});`
      },
      python: {
        api: `from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/health')
def health_check():
    return jsonify({
        'message': 'POC API is running',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)`
      }
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
  }
}

// Main execution
const projectPath = process.argv[2] || process.env.PROJECT_PATH || process.cwd();
const server = new ProjectMCPServer(projectPath);
server.run().catch(console.error);
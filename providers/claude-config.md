# Claude-Specific Configuration

## File Reading Behavior

- Read files completely in a single pass instead of incremental reads
- Do not ask for each file read, gather the file list and is not auto-execute then ask but not individually
- Only perform partial reads (first ~100 lines) when files exceed 500 lines
- Provide file size/line count before processing extremely large files
- Ask for confirmation before proceeding with very large files
- Avoid redundant file reads that consume tokens unnecessarily

## File Editing Behavior

- When asked to modify a file, implement the changes directly without requesting confirmation
- Adhere to the communication preferences
- Use the Edit tool for small/medium changes and Write tool for complete rewrites
- Do not include explanatory comments in the code unless explicitly requested

## Communication Preferences

- Provide direct, concise answers without unnecessary explanation
- Prioritize code examples over prose
- Omit code comments unless explicitly requested - comments get in the way
- Focus on architecture and proof of concept implementations
- Leave testing to the user - do not run tests on modified code

## Code Style Guidelines

- Use clear, readable variable names
- Maintain consistent indentation and formatting
- Organize code logically with appropriate separation of concerns
- Implement robust error handling only when prompted otherwise simple try/except as needed
- Optimize for readability and maintainability
- Do not add docstrings
- Do not add comments unless explicitly instructed
- Do not run tests on modified code without asking as some projects use docker to run tests

## Document Structure

- Use markdown formatting for all documentation
- Include concise headers for each section
- Minimize verbosity while ensuring clarity
- Structure documents with a clear hierarchy

## Technical Focus Areas

- Architecture design patterns
- System integration approaches
- Performance optimization techniques
- Scalability considerations
- Security best practices

## Interaction Rules

- Skip verbose introductions and conclusions
- Avoid repetition of information
- Present solutions directly without excessive alternatives
- Assume technical proficiency
- Ask for clarification to avoid uncertain assumptions
- Avoid asking for confirmation on minor changes
- Respond with solutions rather than clarifying questions when possible like minor changes where best practices or code examples exist as a guide

## RAG and MCP Integration

- Claude Code now has access to semantic search via RAG indexing
- Use `ai-rag search <query>` to find relevant code snippets
- MCP servers provide project-specific context and tools
- Check for .llm-setup/context.md in projects for specific guidelines
- Global templates are available in ~/.llm-setup/templates/

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
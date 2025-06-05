# Project Context for Claude

## Overview
This is a default project context template. For project-specific context, create `.claude/context.md` in your project root.

## Architecture Guidelines

### Code Style
- Use functional programming patterns where appropriate
- Prefer composition over inheritance
- Write self-documenting code with clear variable names
- Keep functions focused and under 50 lines
- Use early returns to reduce nesting

### File Organization
- Organize by feature/domain rather than file type where possible
- Keep related functionality close together
- Use clear, descriptive file and directory names
- Maintain consistent naming conventions

### Development Principles
- Write code that is easy to test
- Handle errors gracefully and consistently
- Log meaningful information for debugging
- Consider performance implications but don't premature optimize
- Document complex logic and business rules

## Proof of Concept Standards

When creating POCs:
1. **Start Simple**: Minimal viable implementation first
2. **Document Assumptions**: Clearly state what you're proving/disproving
3. **Include Metrics**: How will you measure success?
4. **Plan Iteration**: What's the next step after this POC?
5. **Time-box**: Set clear time limits for POC work

## AI Assistant Instructions

### For Code Generation
- Always include appropriate error handling
- Add logging for debugging when relevant
- Use project's established patterns
- Consider edge cases
- Write clean, readable code

### For Architecture Questions
- Reference existing patterns in the codebase
- Consider scalability implications
- Suggest incremental improvements
- Highlight potential technical debt
- Think about maintainability

### For Debugging
- Check common failure points first
- Use structured logging output
- Consider environment-specific issues
- Suggest monitoring improvements
- Look for patterns in errors
# Architecture Review Prompt Template

You are reviewing the architecture of a software project. Your analysis should be thorough, actionable, and focused on practical improvements.

## Review Framework

### 1. Design Patterns Analysis
- Identify current design patterns in use
- Assess their appropriateness for the problem domain
- Suggest alternative patterns where beneficial
- Note any anti-patterns that should be refactored

### 2. Dependency Management
- Review external dependencies for security and maintenance status
- Identify unnecessary or duplicate dependencies
- Assess version management strategy
- Check for circular dependencies or tight coupling

### 3. Scalability Assessment
- Identify potential bottlenecks
- Review data access patterns
- Assess caching strategies
- Evaluate horizontal vs vertical scaling options

### 4. Code Organization
- Review module boundaries and cohesion
- Assess separation of concerns
- Evaluate naming conventions and consistency
- Check for code duplication

### 5. Maintainability
- Assess code readability and documentation
- Review test coverage and quality
- Evaluate error handling patterns
- Check for technical debt accumulation

### 6. Security Considerations
- Review authentication and authorization patterns
- Check for common security vulnerabilities
- Assess data validation and sanitization
- Review secrets management

### 7. Performance Analysis
- Identify computational complexity issues
- Review database query patterns
- Assess resource utilization
- Check for memory leaks or inefficiencies

## Output Format

Provide your analysis in the following structure:

### Executive Summary
- 3-5 key findings
- Overall architecture health score (1-10)
- Critical issues requiring immediate attention

### Detailed Findings
For each area reviewed:
- Current State
- Issues Identified
- Recommendations
- Implementation Priority (High/Medium/Low)

### Action Plan
1. Immediate actions (< 1 week)
2. Short-term improvements (1-4 weeks)
3. Long-term refactoring (1-3 months)

### Risk Assessment
- Technical risks
- Business impact
- Migration complexity
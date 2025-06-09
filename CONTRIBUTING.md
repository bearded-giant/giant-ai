# Contributing to Giant AI

We welcome contributions to Giant AI! This document outlines the process for contributing to the project and helps ensure that contributions can be incorporated effectively.

## 🎯 Contributing Philosophy

Giant AI aims to be the premier open-source AI development toolkit. We encourage contributions that:

- **Enhance semantic understanding** - Improve RAG, MCP, or context management
- **Add specialized tools** - RAG-integrated utilities that provide unique value
- **Improve developer experience** - Better documentation, clearer workflows
- **Expand compatibility** - Support for new LLM providers, editors, frameworks

## 📋 Contribution Process

### 1. Before You Start

**For significant changes:**
- Open an issue to discuss your idea before implementing
- Check existing issues and PRs to avoid duplication
- Review our [roadmap](docs/) to align with project direction

**For small fixes:**
- Feel free to submit PRs directly for bug fixes, typos, small improvements

### 2. Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/your-org/giant-ai.git
cd giant-ai

# Run setup to install dependencies
./scripts/ai-setup

# Test your setup
ai-rag index . --clear
ai-search "test query" . 3
```

### 3. Making Changes

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes following the project conventions
# (See .giant-ai/conventions.yml for coding standards)

# Test your changes
./scripts/test-all.sh  # If available, or manual testing

# Commit with clear messages
git commit -m "Add semantic refactoring tool for pattern consistency"
```

### 4. Submitting Your Contribution

```bash
# Push your branch
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
# Include:
# - Clear description of changes
# - Reasoning for the change
# - Any testing performed
# - Documentation updates (if applicable)
```

## 🛡️ Contributor License Agreement (CLA)

**Important**: By contributing to Giant AI, you agree to the following terms:

### Grant of Rights
You grant the Giant AI project maintainers:
- **Perpetual license** to use, modify, and distribute your contributions
- **Rights to relicense** your contributions under compatible licenses
- **Patent license** for any patents your contributions may infringe

### Your Assurances
You represent that:
- You have the right to make the contribution
- Your contribution is your original work or properly attributed
- You have not violated any third-party rights

### Rationale
This CLA allows the project to:
- Maintain consistent licensing across the codebase
- Adapt to future licensing needs
- Defend against potential legal issues
- Ensure long-term project sustainability

*This CLA is based on industry-standard agreements used by Apache, Google, and other major open-source projects.*

## 🎨 Contribution Guidelines

### Code Quality Standards

- **Follow existing patterns** - Match the coding style in similar files
- **Add appropriate tests** - Include tests for new functionality
- **Update documentation** - Keep docs in sync with code changes
- **Security first** - Be mindful of security implications

### Specific Areas for Contributions

#### 🔍 **RAG & Semantic Search**
- Improvements to embedding models or chunking strategies
- Better language-specific parsing (JavaScript, Python, Rust, etc.)
- Performance optimizations for large codebases

#### 🔧 **MCP Integration**
- New MCP tools for code analysis
- Integration with additional AI providers
- Enhanced project structure detection

#### 🤖 **Agent Mode**
- New prompt templates for specific task types
- Safety improvements and validation
- Integration with additional LLM providers

#### 🛠️ **Development Tools**
- Implementation of planned tools (ai-pattern-refactor, ai-test-generate, etc.)
- Editor integrations (VS Code, Vim, Emacs)
- CI/CD integration tools

#### 📚 **Documentation**
- Tutorial improvements and examples
- Architecture explanations
- Troubleshooting guides

### Review Process

1. **Automated checks** - CI runs tests and linting
2. **Maintainer review** - Core team reviews for:
   - Code quality and consistency
   - Security implications
   - Alignment with project goals
   - Documentation completeness
3. **Community feedback** - Input from other contributors
4. **Integration testing** - Ensure changes work across different environments

## 🤝 Community Guidelines

### Communication
- **Be respectful** - Treat all contributors with respect
- **Be constructive** - Provide helpful feedback and suggestions
- **Be patient** - Understand that reviews take time
- **Be collaborative** - Work together toward common goals

### Issue Reporting
When reporting bugs or requesting features:

```markdown
## Description
Clear description of the issue or request

## Steps to Reproduce (for bugs)
1. Step one
2. Step two
3. Expected vs actual behavior

## Environment
- OS: [e.g., macOS 14, Ubuntu 22.04]
- Python version: [e.g., 3.11]
- Node.js version: [e.g., 18.x]
- Giant AI version: [e.g., 1.2.3]

## Additional Context
Any other relevant information
```

## 🏆 Recognition

Contributors will be recognized in:
- **CONTRIBUTORS.md** - List of all project contributors
- **Release notes** - Acknowledgment in version releases
- **Documentation** - Attribution for significant contributions

## 📞 Getting Help

- **Questions about contributing** - Open a GitHub issue with the "question" label
- **Technical discussions** - Use GitHub Discussions
- **Security issues** - Email security@giant-ai.com (if project email exists)

## 📜 Legal Notes

### Copyright Assignment
By contributing, you assign copyright of your contributions to the Giant AI project. This ensures:
- Consistent ownership structure
- Ability to enforce license terms
- Flexibility for future licensing decisions

### Patent Protection
Your contributions are covered under Apache 2.0's patent protection clauses, providing legal protection for both contributors and users.

---

## Quick Checklist for Contributors

Before submitting a PR, ensure:

- [ ] **Code follows project conventions** (see .giant-ai/conventions.yml)
- [ ] **Tests are included** for new functionality
- [ ] **Documentation is updated** (README, inline docs, etc.)
- [ ] **Commit messages are clear** and descriptive
- [ ] **Branch is up to date** with main/master
- [ ] **No sensitive information** is included (API keys, passwords, etc.)
- [ ] **CLA terms are understood** and agreed to

---

Thank you for contributing to Giant AI! Your contributions help make AI-powered development more accessible and powerful for developers worldwide. 🚀
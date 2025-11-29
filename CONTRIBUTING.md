# Contributing to Numismatch

Thank you for your interest in contributing to Numismatch! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** and clone it locally
2. **Set up your development environment**:
   ```bash
   cd numismatch
   pip install -r requirements.txt
   ```
3. **Configure Google Cloud credentials**:
   ```bash
   gcloud auth application-default login
   ```
4. **Copy `.env.example` to `.env`** and configure your settings

## Development Workflow

### Running Locally

Test the agent locally using ADK web interface:

```bash
adk web --module numismatch.agent --object root_agent
```

Visit http://localhost:8000 to interact with the agent.

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints for function parameters and return values
- Add docstrings to all public functions and classes
- Keep functions focused and modular

### Testing

Before submitting a pull request:

1. **Test your changes locally** using `adk web`
2. **Verify imports work correctly**:
   ```bash
   python -c "from numismatch.agent import root_agent; print(root_agent.name)"
   ```
3. **Run any existing tests** (if available):
   ```bash
   pytest tests/
   ```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-tool` - for new features
- `fix/agent-response-bug` - for bug fixes
- `docs/update-readme` - for documentation updates

### Commit Messages

Write clear commit messages:
- Use present tense ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Provide details in the body if needed

Example:
```
Add Byzantine coin detection tool

- Implements check_byzantine_origin function
- Updates main agent prompt to handle Byzantine coins
- Adds tests for Byzantine vs Roman distinction
```

## Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Ensure no breaking changes** to the agent API
3. **Test that the agent still works** end-to-end
4. **Submit a pull request** with:
   - Clear description of changes
   - Motivation for the changes
   - Screenshots/examples if applicable

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Documentation updated (if needed)
- [ ] Agent tested locally and works correctly
- [ ] No sensitive data (API keys, credentials) in code
- [ ] Commit messages are clear and descriptive

## Areas for Contribution

### High Priority
- Additional coin identification tools
- Improved image preprocessing
- Market data integration
- Authentication detection features

### Documentation
- More example queries and responses
- Deployment guides for different platforms
- Video tutorials
- Translation to other languages

### Testing
- Unit tests for tools
- Integration tests for agent workflows
- Load testing for production scenarios

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Publishing others' private information
- Trolling or insulting/derogatory comments
- Any conduct inappropriate for a professional setting

## Questions?

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Open a GitHub Issue
- **Security issues**: Email the maintainers directly (do not open public issues)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for contributing to Numismatch! 🪙


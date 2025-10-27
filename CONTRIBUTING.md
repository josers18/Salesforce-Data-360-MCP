# Contributing to MCP-OpenAI Bridge

First off, thank you for considering contributing to MCP-OpenAI Bridge! It's people like you that make this project great.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include logs and error messages**
- **Specify your environment** (OS, Python version, package versions)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the proposed feature**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the existing style
6. Write a clear commit message

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/mcp-openai-bridge.git
cd mcp-openai-bridge

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## Development Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clear, commented code
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run tests
pytest

# Run linting
flake8 .

# Format code
black .

# Type checking
mypy .
```

### 4. Commit Your Changes

Use clear and meaningful commit messages:

```bash
git commit -m "feat: add streaming response support"
git commit -m "fix: resolve async cleanup issue"
git commit -m "docs: update installation instructions"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://github.com/psf/black) for code formatting
- Use type hints where possible
- Write docstrings for all public functions/classes

### Commit Message Style

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Build process or auxiliary tool changes

### Documentation Style

- Use Markdown for documentation
- Keep line length to 80-100 characters
- Include code examples where helpful
- Update the CHANGELOG.md

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_bridge.py

# Run with coverage
pytest --cov=mcp_openai_bridge

# Run with verbose output
pytest -v
```

### Writing Tests

- Write unit tests for new functions
- Write integration tests for new features
- Aim for >80% code coverage
- Use descriptive test names

Example:

```python
def test_bridge_connect_with_valid_credentials():
    """Test that bridge connects successfully with valid credentials."""
    bridge = MCPOpenAIBridge(...)
    result = await bridge.connect()
    assert result is True
```

## Documentation

### Updating Documentation

When adding features or making changes:

1. Update relevant documentation in `docs/`
2. Update docstrings in code
3. Update README.md if needed
4. Add examples to `docs/EXAMPLES.md`
5. Update CHANGELOG.md

### Building Documentation Locally

```bash
cd docs
pip install -r requirements.txt
make html
```

## Release Process

(For maintainers)

1. Update version in `setup.py` and `__version__.py`
2. Update CHANGELOG.md
3. Create a git tag
4. Push to GitHub
5. Create a GitHub release
6. Publish to PyPI

## Questions?

Feel free to:
- Open an issue with your question
- Join our [Discord server](https://discord.gg/your-invite)
- Email us at support@example.com

## Recognition

Contributors will be recognized in:
- README.md contributors section
- CHANGELOG.md for each release
- GitHub contributors page

Thank you for contributing! 🎉

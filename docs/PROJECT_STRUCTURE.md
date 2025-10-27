# Project Structure

```
mcp-openai-bridge/
│
├── README.md                          # Main project documentation
├── LICENSE                            # MIT License
├── CHANGELOG.md                       # Version history
├── CONTRIBUTING.md                    # Contribution guidelines
├── CODE_OF_CONDUCT.md                 # Community guidelines
├── .gitignore                         # Git ignore rules
├── .env.example                       # Example environment variables
│
├── setup.py                           # Package setup configuration
├── requirements.txt                   # Production dependencies
├── requirements-dev.txt               # Development dependencies
│
├── src/                               # Source code (if using src layout)
│   └── mcp_openai_bridge/
│       ├── __init__.py
│       ├── bridge.py                  # Main bridge class
│       ├── cli.py                     # CLI interface
│       └── utils.py                   # Utility functions
│
├── mcp_openai_bridge.py              # Core bridge implementation
├── interactive_chat.py               # CLI interface
├── streamlit_app_daemon.py           # Streamlit UI
├── mcp_daemon.py                     # Background MCP daemon
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── test_bridge.py                # Bridge tests
│   ├── test_cli.py                   # CLI tests
│   ├── test_integration.py           # Integration tests
│   └── fixtures/                     # Test fixtures
│
├── docs/                             # Documentation
│   ├── INSTALLATION.md               # Installation guide
│   ├── CONFIGURATION.md              # Configuration guide
│   ├── EXAMPLES.md                   # Usage examples
│   ├── API.md                        # API reference
│   ├── DOCKER.md                     # Docker deployment
│   ├── TROUBLESHOOTING.md            # Troubleshooting guide
│   └── images/                       # Documentation images
│
├── examples/                         # Example scripts
│   ├── basic_usage.py
│   ├── advanced_queries.py
│   ├── batch_processing.py
│   └── fastapi_integration.py
│
├── docker/                           # Docker configuration
│   ├── Dockerfile                    # Main Dockerfile
│   ├── docker-compose.yml            # Compose configuration
│   └── entrypoint.sh                 # Container entrypoint
│
├── .github/                          # GitHub configuration
│   ├── workflows/                    # CI/CD workflows
│   │   ├── tests.yml                 # Test automation
│   │   ├── lint.yml                  # Code quality checks
│   │   └── publish.yml               # Package publishing
│   ├── ISSUE_TEMPLATE/               # Issue templates
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md      # PR template
│
└── scripts/                          # Utility scripts
    ├── setup.sh                      # Setup script
    ├── test.sh                       # Test runner
    └── deploy.sh                     # Deployment script
```

## Directory Descriptions

### Root Files

- **README.md**: Main project documentation with quick start guide
- **LICENSE**: MIT license for open source distribution
- **CHANGELOG.md**: Version history and release notes
- **CONTRIBUTING.md**: Guidelines for contributors
- **CODE_OF_CONDUCT.md**: Community standards
- **.gitignore**: Files to exclude from version control
- **.env.example**: Template for environment variables
- **setup.py**: Python package configuration
- **requirements.txt**: Production dependencies
- **requirements-dev.txt**: Development dependencies

### Source Code

- **mcp_openai_bridge.py**: Core bridge implementation
  - `MCPOpenAIBridge` class
  - Async connection management
  - Tool discovery and calling
  - OpenAI integration

- **interactive_chat.py**: Command-line interface
  - Interactive REPL
  - Conversation history
  - Pretty formatting

- **streamlit_app_daemon.py**: Web UI
  - Chat interface
  - Configuration panel
  - Debug tools

- **mcp_daemon.py**: Background process manager
  - Persistent MCP connection
  - IPC communication
  - Error handling

### Tests

- **test_bridge.py**: Unit tests for bridge class
- **test_cli.py**: CLI interface tests
- **test_integration.py**: End-to-end integration tests
- **fixtures/**: Test data and mocks

### Documentation

- **INSTALLATION.md**: Step-by-step installation
- **CONFIGURATION.md**: Configuration options
- **EXAMPLES.md**: Usage examples and patterns
- **API.md**: API reference documentation
- **DOCKER.md**: Docker deployment guide
- **TROUBLESHOOTING.md**: Common issues and solutions

### Examples

- **basic_usage.py**: Simple examples for getting started
- **advanced_queries.py**: Complex query patterns
- **batch_processing.py**: Processing multiple queries
- **fastapi_integration.py**: API integration example

### Docker

- **Dockerfile**: Container image definition
- **docker-compose.yml**: Multi-container setup
- **entrypoint.sh**: Container initialization script

### GitHub Configuration

- **workflows/**: CI/CD automation
  - **tests.yml**: Run tests on push/PR
  - **lint.yml**: Code quality checks
  - **publish.yml**: Publish to PyPI
- **ISSUE_TEMPLATE/**: Standardized issue reporting
- **PULL_REQUEST_TEMPLATE.md**: PR checklist

### Scripts

- **setup.sh**: Automated setup for development
- **test.sh**: Run all tests with coverage
- **deploy.sh**: Deployment automation

## File Relationships

```
interactive_chat.py
    ↓ imports
mcp_openai_bridge.py
    ↓ connects to
MCP Server (external)
    ↓ queries
Salesforce Data Cloud

streamlit_app_daemon.py
    ↓ spawns
mcp_daemon.py
    ↓ imports
mcp_openai_bridge.py
    ↓ connects to
MCP Server
```

## Key Components

### 1. Bridge Layer
- Handles MCP protocol communication
- Manages async connections
- Translates between OpenAI and MCP

### 2. Interface Layer
- CLI (interactive_chat.py)
- Web UI (streamlit_app_daemon.py)
- Python API (importable bridge)

### 3. Infrastructure Layer
- Docker containerization
- Environment configuration
- Logging and monitoring

### 4. Testing Layer
- Unit tests
- Integration tests
- CI/CD automation

## Development Workflow

1. **Setup**: Run `scripts/setup.sh`
2. **Code**: Edit files in root or `src/`
3. **Test**: Run `pytest` or `scripts/test.sh`
4. **Lint**: Run `black .` and `flake8 .`
5. **Commit**: Use conventional commit messages
6. **Push**: CI runs automatically
7. **Release**: Tag version, publish to PyPI

## Deployment Options

### Local Development
```
mcp_openai_bridge.py + interactive_chat.py
```

### Docker Deployment
```
Dockerfile + docker-compose.yml
```

### Production API
```
FastAPI + mcp_openai_bridge.py + Docker
```

### Web Demo
```
streamlit_app_daemon.py + mcp_daemon.py + Docker
```

## Adding New Features

1. Add code to appropriate module
2. Add tests to `tests/`
3. Update documentation in `docs/`
4. Add examples to `examples/`
5. Update CHANGELOG.md
6. Create PR with description

## Code Organization Principles

- **Separation of Concerns**: Each file has a single responsibility
- **DRY**: Shared code in utilities
- **Testability**: Functions designed for easy testing
- **Documentation**: Every public interface documented
- **Type Hints**: All functions have type annotations

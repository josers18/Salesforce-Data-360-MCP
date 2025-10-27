# Configuration Guide

## Overview

MCP-OpenAI Bridge can be configured using environment variables, a configuration file, or command-line arguments.

## Environment Variables

### Required Variables

Create a `.env` file in your project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Salesforce Data Cloud
SF_CLIENT_ID=your-salesforce-client-id
SF_CLIENT_SECRET=your-salesforce-client-secret

# MCP Server
SERVER_PATH=/path/to/mcp-server/server.py
```

### Optional Variables

```bash
# OpenAI Model Selection
OPENAI_MODEL=gpt-4o  # Options: gpt-4o, gpt-4, gpt-3.5-turbo

# Python Path
PYTHON_PATH=/usr/local/bin/python3

# Debug Mode
DEBUG=false

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

## Configuration File

### YAML Configuration

Create `config.yaml`:

```yaml
openai:
  api_key: "sk-your-api-key"
  model: "gpt-4o"
  temperature: 0.7
  max_tokens: 2000

mcp:
  command: "python3"
  server_path: "/path/to/server.py"
  timeout: 30
  
salesforce:
  client_id: "your-client-id"
  client_secret: "your-client-secret"
  
logging:
  level: "INFO"
  file: "app.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### JSON Configuration

Create `config.json`:

```json
{
  "openai": {
    "api_key": "sk-your-api-key",
    "model": "gpt-4o",
    "temperature": 0.7
  },
  "mcp": {
    "command": "python3",
    "server_path": "/path/to/server.py"
  },
  "salesforce": {
    "client_id": "your-client-id",
    "client_secret": "your-client-secret"
  }
}
```

## Getting Credentials

### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy and save your key securely

### Salesforce Data Cloud Credentials

1. Log into your Salesforce org
2. Navigate to Setup → Apps → App Manager
3. Create a new Connected App or use existing
4. Enable OAuth settings
5. Copy Client ID and Client Secret

**Required OAuth Scopes:**
- `api`
- `cdp_api` (for Data Cloud)
- `refresh_token`

## Configuration Options Reference

### OpenAI Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_key` | string | required | Your OpenAI API key |
| `model` | string | `gpt-4o` | Model to use |
| `temperature` | float | 0.7 | Response randomness (0-2) |
| `max_tokens` | int | 2000 | Maximum response length |
| `top_p` | float | 1.0 | Nucleus sampling parameter |

### MCP Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `command` | string | `python3` | Python executable path |
| `server_path` | string | required | Path to MCP server |
| `timeout` | int | 30 | Connection timeout (seconds) |
| `retry_attempts` | int | 3 | Number of retry attempts |

### Salesforce Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `client_id` | string | required | Connected App Client ID |
| `client_secret` | string | required | Connected App Secret |
| `instance_url` | string | auto | Salesforce instance URL |

### Logging Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `level` | string | `INFO` | Log level (DEBUG, INFO, WARNING, ERROR) |
| `file` | string | `app.log` | Log file path |
| `format` | string | standard | Log message format |
| `console` | bool | `true` | Log to console |

## Advanced Configuration

### Custom MCP Server Environment

```python
bridge = MCPOpenAIBridge(
    openai_api_key="your-key",
    mcp_command="python3",
    mcp_args=["/path/to/server.py"],
    mcp_env={
        "SF_CLIENT_ID": "your-id",
        "SF_CLIENT_SECRET": "your-secret",
        "CUSTOM_VAR": "custom-value"
    }
)
```

### Streaming Responses

```python
bridge = MCPOpenAIBridge(
    openai_api_key="your-key",
    # ... other params
    stream=True  # Enable streaming
)
```

### Custom Timeout

```python
bridge = MCPOpenAIBridge(
    openai_api_key="your-key",
    # ... other params
    timeout=60  # Increase timeout to 60 seconds
)
```

## Docker Configuration

### docker-compose.yml

```yaml
version: '3.8'

services:
  mcp-bridge:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SF_CLIENT_ID=${SF_CLIENT_ID}
      - SF_CLIENT_SECRET=${SF_CLIENT_SECRET}
      - SERVER_PATH=/app/mcp-server/server.py
    volumes:
      - /path/to/mcp-server:/app/mcp-server
    restart: unless-stopped
```

### Environment File for Docker

Create `.env` for docker-compose:

```bash
OPENAI_API_KEY=sk-your-key
SF_CLIENT_ID=your-id
SF_CLIENT_SECRET=your-secret
MCP_SERVER_PATH=/path/to/mcp-server
```

## Security Best Practices

### 1. Never Commit Credentials

```bash
# Add to .gitignore
.env
.env.local
.env.*.local
config.yaml
config.json
secrets/
```

### 2. Use Environment Variables

```bash
# Set in shell
export OPENAI_API_KEY="sk-your-key"

# Or use a .env file (never commit!)
```

### 3. Rotate Keys Regularly

- Change OpenAI API key every 90 days
- Rotate Salesforce credentials regularly
- Use different keys for dev/prod

### 4. Limit Permissions

- Use minimal OAuth scopes
- Create read-only API keys when possible
- Restrict IP addresses if supported

## Troubleshooting Configuration

### Issue: "API key not found"

**Check:**
```bash
# Verify .env file exists
ls -la .env

# Check environment variables
echo $OPENAI_API_KEY

# Load .env file
export $(cat .env | xargs)
```

### Issue: "Invalid credentials"

**Verify:**
```bash
# Test OpenAI key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Test Salesforce credentials
# Use Salesforce API explorer or Postman
```

### Issue: "MCP server not found"

**Check:**
```bash
# Verify server path
ls -l $SERVER_PATH

# Test server directly
python $SERVER_PATH
```

## Example Configurations

### Development

```yaml
openai:
  api_key: "sk-dev-key"
  model: "gpt-3.5-turbo"  # Cheaper for dev
  
logging:
  level: "DEBUG"
  console: true

mcp:
  timeout: 60  # Longer timeout for debugging
```

### Production

```yaml
openai:
  api_key: "sk-prod-key"
  model: "gpt-4o"
  
logging:
  level: "WARNING"
  file: "/var/log/mcp-bridge/app.log"
  
mcp:
  timeout: 30
  retry_attempts: 5
```

## Next Steps

- [Run Examples](EXAMPLES.md)
- [Deploy with Docker](DOCKER.md)
- [Troubleshooting](TROUBLESHOOTING.md)

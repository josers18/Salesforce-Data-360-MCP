# Installation Guide

## Prerequisites

Before installing MCP-OpenAI Bridge, ensure you have:

- **Python 3.11 or higher**
- **pip** package manager
- **OpenAI API key** - [Get one here](https://platform.openai.com/api-keys)
- **Salesforce Data Cloud credentials**
  - Client ID
  - Client Secret
- **MCP Server** - e.g., [datacloud-mcp-query](https://github.com/salesforce/datacloud-mcp-query)

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mcp-openai-bridge.git
cd mcp-openai-bridge
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI API client
- `mcp` - Model Context Protocol SDK
- `httpx` - HTTP client
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation
- `rfc3986` - URI validation
- `anyio` - Async I/O
- `streamlit` - Web UI framework (optional for CLI-only use)

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit with your credentials
nano .env  # or use your preferred editor
```

Add your credentials:

```bash
OPENAI_API_KEY=sk-your-openai-api-key
SF_CLIENT_ID=your-salesforce-client-id
SF_CLIENT_SECRET=your-salesforce-client-secret
SERVER_PATH=/path/to/mcp-server/server.py
PYTHON_PATH=/usr/local/bin/python3
```

Or set them in your shell:

```bash
export OPENAI_API_KEY="sk-your-key"
export SF_CLIENT_ID="your-id"
export SF_CLIENT_SECRET="your-secret"
export SERVER_PATH="/path/to/server.py"
```

### 5. Verify Installation

```bash
# Test CLI
python interactive_chat.py

# Test Streamlit (optional)
streamlit run streamlit_app.py
```

## Installing MCP Server

You'll need an MCP server to connect to your data source.

### For Salesforce Data Cloud:

```bash
# Clone the Salesforce MCP server
git clone https://github.com/salesforce/datacloud-mcp-query.git
cd datacloud-mcp-query

# Install dependencies
pip install -r requirements.txt

# Test it works
python server.py
```

Then set `SERVER_PATH` to point to this `server.py` file.

## Platform-Specific Instructions

### macOS

```bash
# Install Python 3.11+ via Homebrew
brew install python@3.11

# Use the brew Python path
export PYTHON_PATH=/opt/homebrew/bin/python3.11
```

### Linux (Ubuntu/Debian)

```bash
# Install Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Set Python path
export PYTHON_PATH=/usr/bin/python3.11
```

### Windows

1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Open Command Prompt or PowerShell:

```powershell
# Set environment variables
$env:OPENAI_API_KEY="sk-your-key"
$env:SF_CLIENT_ID="your-id"
$env:SF_CLIENT_SECRET="your-secret"
$env:SERVER_PATH="C:\path\to\server.py"
```

## Troubleshooting Installation

### Issue: "Python version too old"

**Check version:**
```bash
python --version
```

**Solution:** Install Python 3.11 or higher from [python.org](https://www.python.org/downloads/)

### Issue: "pip: command not found"

**macOS/Linux:**
```bash
python -m ensurepip --upgrade
```

**Windows:**
```bash
python -m ensurepip --upgrade
```

### Issue: "Permission denied"

**Solution:** Use a virtual environment (recommended) or install with `--user`:
```bash
pip install --user -r requirements.txt
```

### Issue: "ModuleNotFoundError after installation"

**Solution:** Make sure you're in the virtual environment:
```bash
# Check if venv is activated (should see (venv) in prompt)
which python  # Should point to venv/bin/python

# If not activated, activate it
source venv/bin/activate
```

### Issue: "SSL certificate verification failed"

**Temporary fix (use with caution):**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

**Better solution:** Update your certificates or use a corporate proxy if behind one.

## Getting Credentials

### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy and save your key securely (starts with `sk-`)

### Salesforce Data Cloud Credentials

1. Log into your Salesforce org
2. Navigate to **Setup → Apps → App Manager**
3. Click **New Connected App**
4. Fill in the basic information
5. Enable **OAuth Settings**
6. Add OAuth scopes:
   - `api`
   - `cdp_api` (for Data Cloud)
   - `refresh_token`
7. Save and copy:
   - **Consumer Key** (this is your Client ID)
   - **Consumer Secret** (this is your Client Secret)

## Verifying Everything Works

### Test 1: Check Python and Packages

```bash
python --version  # Should be 3.11+
pip list | grep openai  # Should show openai package
pip list | grep mcp  # Should show mcp package
```

### Test 2: Check Environment Variables

```bash
echo $OPENAI_API_KEY  # Should show your key
echo $SF_CLIENT_ID  # Should show your client ID
echo $SERVER_PATH  # Should show path to server.py
```

### Test 3: Test MCP Server Directly

```bash
python $SERVER_PATH
# Should start without errors
# Press Ctrl+C to stop
```

### Test 4: Run CLI

```bash
python interactive_chat.py
# Should connect and show available tools
```

### Test 5: Run Streamlit

```bash
streamlit run streamlit_app.py
# Should open browser to http://localhost:8501
```

## Next Steps

- [Configuration Guide](CONFIGURATION.md) - Customize your setup
- [Usage Examples](EXAMPLES.md) - Learn what you can do
- [Troubleshooting](TROUBLESHOOTING.md) - Fix common issues

## Upgrading

To upgrade to a newer version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf mcp-openai-bridge

# Remove virtual environment and files
```

## Additional Resources

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [pip Documentation](https://pip.pypa.io/en/stable/)
- [Salesforce Connected Apps](https://help.salesforce.com/articleView?id=sf.connected_app_overview.htm)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

**Installation complete! Ready to start querying your Data Cloud!** 🚀

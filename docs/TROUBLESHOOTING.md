# Troubleshooting Guide

## Common Issues and Solutions

### Connection Issues

#### "Connection to MCP server failed"

**Symptoms:**
- CLI shows "❌ Connection failed"
- Streamlit shows connection error

**Solutions:**

1. **Verify MCP server path:**
```bash
echo $SERVER_PATH
ls -l $SERVER_PATH  # Should show the file exists
```

2. **Test MCP server directly:**
```bash
python $SERVER_PATH
# Should start without errors
```

3. **Check Salesforce credentials:**
```bash
echo $SF_CLIENT_ID
echo $SF_CLIENT_SECRET
# Should show your credentials (not empty)
```

4. **Verify Python path:**
```bash
which python3
# Update PYTHON_PATH to match
export PYTHON_PATH=/path/to/your/python3
```

---

### Async/Event Loop Issues

#### "Attempted to exit cancel scope in a different task"

**Symptoms:**
- Streamlit shows async generator error
- Event loop warnings

**Solution:**
✅ **Use the provided `streamlit_app.py`** - It has a background thread that handles async properly.

**What NOT to do:**
- ❌ Don't use `asyncio.run()` repeatedly in Streamlit
- ❌ Don't create new event loops for each query

---

### Module/Import Errors

#### "ModuleNotFoundError: No module named 'mcp'"

**Solution:**
```bash
pip install mcp fastmcp httpx python-dotenv pydantic rfc3986 anyio
# Or simply:
pip install -r requirements.txt
```

#### "ModuleNotFoundError: No module named 'openai'"

**Solution:**
```bash
pip install openai
```

#### "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
pip install streamlit
```

---

### API Key Issues

#### "OpenAI API key not found"

**Solution:**
```bash
# Check if set
echo $OPENAI_API_KEY

# If not set:
export OPENAI_API_KEY="sk-your-actual-key"

# Or add to .env file
echo "OPENAI_API_KEY=sk-your-key" >> .env
```

#### "Invalid API key"

**Symptoms:**
- Error: "Incorrect API key provided"

**Solution:**
1. Verify your key is correct (starts with `sk-`)
2. Generate a new key at https://platform.openai.com/api-keys
3. Make sure there are no extra spaces or quotes

---

### Salesforce Credential Issues

#### "Authentication failed"

**Solution:**

1. **Verify Connected App settings:**
   - OAuth is enabled
   - Correct scopes: `api`, `cdp_api`, `refresh_token`
   - Callback URL configured (if needed)

2. **Check credentials format:**
```bash
# Client ID should be a long alphanumeric string
# Client Secret should also be a long alphanumeric string
# No quotes or extra characters
```

3. **Test credentials:**
   - Try authenticating directly through Salesforce
   - Verify the Connected App is activated

---

### Python Version Issues

#### "Python version too old"

**Check version:**
```bash
python --version
# Needs to be 3.11 or higher
```

**Solution:**

**macOS:**
```bash
brew install python@3.11
export PYTHON_PATH=/opt/homebrew/bin/python3.11
```

**Linux:**
```bash
sudo apt install python3.11
export PYTHON_PATH=/usr/bin/python3.11
```

**Windows:**
- Download from https://www.python.org/downloads/
- Install and add to PATH

---

### Streamlit Issues

#### "Streamlit won't start"

**Solution:**
```bash
# Make sure streamlit is installed
pip install streamlit

# Run with full path
python -m streamlit run streamlit_app.py

# Check port isn't in use
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows
```

#### "Streamlit shows blank page"

**Solution:**
1. Clear browser cache
2. Try incognito/private window
3. Check browser console for errors (F12)
4. Try a different browser

#### "Connection keeps disconnecting in Streamlit"

**Solution:**
✅ This is normal! The bridge reconnects automatically.
- Click "Connect to Data Cloud" button again
- The background thread maintains the connection

---

### Performance Issues

#### "Queries are slow"

**Causes:**
- Large result sets
- Complex queries
- Network latency
- OpenAI API rate limits

**Solutions:**
1. Limit result size in queries
2. Use faster OpenAI model (`gpt-3.5-turbo` instead of `gpt-4o`)
3. Check network connection
4. Verify MCP server performance

---

### Environment Variable Issues

#### "Environment variables not loading"

**Solution:**

**Option 1: Shell environment**
```bash
export OPENAI_API_KEY="sk-your-key"
export SF_CLIENT_ID="your-id"
export SF_CLIENT_SECRET="your-secret"
export SERVER_PATH="/path/to/server.py"
```

**Option 2: .env file**
```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-your-key
SF_CLIENT_ID=your-id
SF_CLIENT_SECRET=your-secret
SERVER_PATH=/path/to/server.py
EOF

# Load it
export $(cat .env | xargs)
```

**Option 3: Python-dotenv (automatic)**
- The application loads `.env` automatically via `python-dotenv`
- Just make sure `.env` exists in the project root

---

### CLI-Specific Issues

#### "CLI exits immediately"

**Check for:**
```bash
# Missing environment variables
python interactive_chat.py
# Should show which variables are missing
```

#### "Keyboard interrupt not working"

**Solution:**
- Use `Ctrl+C` once
- Or type `quit`, `exit`, or `bye`

---

### Streamlit-Specific Issues

#### "Session state errors"

**Solution:**
- Refresh the page (F5)
- Click "Clear Chat" button
- Restart Streamlit: `Ctrl+C` then run again

#### "Can't enter credentials"

**Solution:**
- Check if environment variables are set (they pre-fill)
- Clear the pre-filled values and enter new ones
- Expand the "API Keys" section in sidebar

---

## Diagnostic Steps

### Step 1: Verify Installation

```bash
python --version  # 3.11+
pip list | grep openai  # Should appear
pip list | grep mcp  # Should appear
pip list | grep streamlit  # Should appear
```

### Step 2: Check Configuration

```bash
echo $OPENAI_API_KEY  # Should show key
echo $SF_CLIENT_ID  # Should show ID
echo $SF_CLIENT_SECRET  # Should show secret
echo $SERVER_PATH  # Should show path
ls -l $SERVER_PATH  # File should exist
```

### Step 3: Test Components

```bash
# Test MCP server
python $SERVER_PATH
# Press Ctrl+C after it starts

# Test OpenAI
python -c "import openai; openai.api_key='$OPENAI_API_KEY'; print('OK')"

# Test CLI
python interactive_chat.py
# Type 'quit' to exit

# Test Streamlit
streamlit run streamlit_app.py
# Open browser to http://localhost:8501
```

---

## Getting More Help

### Enable Debug Mode

**CLI:**
```bash
# Run with Python warnings
python -W all interactive_chat.py
```

**Streamlit:**
```bash
# Run with debug
streamlit run streamlit_app.py --logger.level=debug
```

### Check Logs

Look for error messages in:
- Terminal output
- Streamlit console
- Browser console (F12 → Console tab)

### Report Issues

When reporting issues, include:
1. Python version: `python --version`
2. OS: macOS/Linux/Windows
3. Error message (full traceback)
4. Steps to reproduce
5. Environment variable setup (WITHOUT actual keys!)

---

## Quick Fixes Checklist

- [ ] Python 3.11+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment variables set correctly
- [ ] MCP server file exists and works
- [ ] OpenAI API key is valid
- [ ] Salesforce credentials are correct
- [ ] Using the provided `streamlit_app.py` (not modified)
- [ ] No other process using port 8501

---

## Still Having Issues?

1. **Read the docs:**
   - [Installation Guide](INSTALLATION.md)
   - [Configuration Guide](CONFIGURATION.md)
   - [Usage Examples](EXAMPLES.md)

2. **Check GitHub Issues:**
   - Search existing issues
   - Open a new issue with details

3. **Review project context:**
   - See `PROJECT_CONTEXT_FOR_NEXT_SESSION.md` for technical details

---

**Most issues are resolved by verifying environment variables and dependencies!** 🔧

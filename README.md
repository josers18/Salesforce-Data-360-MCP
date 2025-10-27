# MCP-OpenAI Bridge for Salesforce Data 360

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A bridge that connects OpenAI's function calling with Salesforce Data 360 through the Model Context Protocol (MCP). Query your Data 360 using natural language!

## 🌟 Features

- 🤖 **Natural Language Queries** - Ask questions about your data in plain English
- 🔌 **MCP Integration** - Seamlessly connects to any MCP-compatible server
- ⚡ **OpenAI Function Calling** - Leverages GPT-4's advanced reasoning
- 🛠️ **Two Interfaces** - CLI and Streamlit web UI
- 📊 **Salesforce Data 360** - Direct integration with Data 360 queries

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Salesforce Data 360 credentials (Client ID & Secret)
- MCP server (e.g., [datacloud-mcp-query](https://github.com/salesforce/datacloud-mcp-query))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/mcp-openai-bridge.git
cd mcp-openai-bridge

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export OPENAI_API_KEY="sk-your-openai-key"
export SF_CLIENT_ID="your-salesforce-client-id"
export SF_CLIENT_SECRET="your-salesforce-client-secret"
export SERVER_PATH="/path/to/your/mcp-server/server.py"
export PYTHON_PATH="/usr/local/bin/python3"  # Optional, adjust to your Python path
```

## 💻 Usage

### CLI Interface

Perfect for quick queries and automation:

```bash
python interactive_chat.py
```

**Example session:**

```
🚀 MCP-OpenAI Interactive Chat
============================================================
🔌 Connecting to MCP server...
✅ Connected! Found 3 tools

💬 You: What tables are available in my Data 360?

🤖 Assistant: I found the following tables:
- Customer__dlm
- Orders__dlm  
- Products__dlm

💬 You: Show me the top 5 customers by revenue

🤖 Assistant: Here are your top 5 customers by revenue:
1. Acme Corp - $1.2M
2. TechStart Inc - $980K
...
```

### Streamlit Web UI

Beautiful interface for demos and exploration:

```bash
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

**Features:**
- 💬 Chat-based interface
- 🔑 Credential management in sidebar
- ⚡ Quick action buttons
- 🎨 Clean, modern design

## 📖 Documentation

- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [Configuration](docs/CONFIGURATION.md) - All configuration options
- [Usage Examples](docs/EXAMPLES.md) - Common queries and patterns
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Solutions to common issues

## 🎯 Example Queries

Once connected, try asking:

- "What tables do I have?"
- "Describe the Customer table"
- "Show me the top 10 customers by order count"
- "What's the total revenue from the last 30 days?"
- "Find customers who haven't ordered in 90 days"

## 🏗️ Architecture

```
User Input → OpenAI GPT-4 → MCP Bridge → MCP Server → Salesforce Data 360
```

The bridge:
1. Converts natural language to tool calls via OpenAI
2. Executes queries through MCP protocol
3. Returns formatted results

## 🔧 Configuration

### Environment Variables

Create a `.env` file (or set in your shell):

```bash
# Required
OPENAI_API_KEY=sk-your-openai-api-key
SF_CLIENT_ID=your-salesforce-client-id
SF_CLIENT_SECRET=your-salesforce-client-secret
SERVER_PATH=/path/to/mcp-server/server.py

# Optional
PYTHON_PATH=/usr/local/bin/python3
OPENAI_MODEL=gpt-4o
```

### Python Library Usage

You can also use the bridge in your own Python scripts:

```python
import asyncio
from mcp_openai_bridge import MCPOpenAIBridge

async def main():
    bridge = MCPOpenAIBridge(
        openai_api_key="sk-your-key",
        mcp_command="python3",
        mcp_args=["/path/to/server.py"],
        mcp_env={
            "SF_CLIENT_ID": "your-id",
            "SF_CLIENT_SECRET": "your-secret"
        }
    )
    
    await bridge.connect()
    response = await bridge.chat("What tables do I have?")
    print(response)
    await bridge.close()

asyncio.run(main())
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'mcp'"

```bash
pip install -r requirements.txt
```

### "Connection to MCP server failed"

1. Verify MCP server is installed and accessible
2. Check `SERVER_PATH` points to the correct file
3. Ensure Salesforce credentials are valid
4. Test the MCP server directly: `python /path/to/server.py`

### More help

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for detailed solutions.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io) - Protocol specification
- [OpenAI](https://openai.com) - Function calling capabilities
- [Salesforce](https://salesforce.com) - Data 360 platform

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/mcp-openai-bridge/issues)
- 📖 Documentation: [Full docs](docs/)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/mcp-openai-bridge/discussions)

---

**⭐ If you find this project useful, please star it on GitHub!**

Made with ❤️ for the Salesforce and AI community

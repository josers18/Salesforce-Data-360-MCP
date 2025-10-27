# Usage Examples

This guide provides practical examples for using MCP-OpenAI Bridge.

## Table of Contents

- [Quick Start Examples](#quick-start-examples)
- [CLI Usage](#cli-usage)
- [Python Library](#python-library)
- [Common Query Patterns](#common-query-patterns)
- [Advanced Usage](#advanced-usage)

## Quick Start Examples

### Example 1: List All Tables

```bash
python interactive_chat.py
```

```
💬 You: What tables are available?

🤖 Assistant: I found the following tables in your Data Cloud:
- Customer__dlm
- Orders__dlm
- Products__dlm
- Accounts__dlm
```

### Example 2: Get Table Schema

```
💬 You: Show me the structure of the Customer table

🤖 Assistant: The Customer__dlm table has these columns:
- customer_id (VARCHAR) - Primary key
- first_name (VARCHAR)
- last_name (VARCHAR)
- email (VARCHAR)
- phone (VARCHAR)
- created_date (TIMESTAMP)
- updated_date (TIMESTAMP)
```

### Example 3: Run a Query

```
💬 You: Show me the top 5 customers by order count

🤖 Assistant: Here are the top 5 customers by number of orders:
1. John Smith - 47 orders
2. Sarah Johnson - 42 orders
3. Mike Brown - 38 orders
4. Emily Davis - 35 orders
5. David Wilson - 33 orders
```

## CLI Usage

### Basic Commands

```bash
# Start interactive chat
python interactive_chat.py

# With custom config
python interactive_chat.py --config config.yaml

# With debug mode
DEBUG=1 python interactive_chat.py
```

### Environment Setup

```bash
# Set environment variables
export OPENAI_API_KEY="sk-your-key"
export SF_CLIENT_ID="your-id"
export SF_CLIENT_SECRET="your-secret"
export SERVER_PATH="/path/to/server.py"

# Run
python interactive_chat.py
```

## Python Library

### Basic Usage

```python
import asyncio
from mcp_openai_bridge import MCPOpenAIBridge

async def main():
    # Create bridge
    bridge = MCPOpenAIBridge(
        openai_api_key="sk-your-key",
        mcp_command="python3",
        mcp_args=["/path/to/server.py"],
        mcp_env={
            "SF_CLIENT_ID": "your-id",
            "SF_CLIENT_SECRET": "your-secret"
        }
    )
    
    # Connect
    await bridge.connect()
    
    # Ask questions
    response = await bridge.chat("What tables do I have?")
    print(response)
    
    # Clean up
    await bridge.close()

asyncio.run(main())
```

### With Context Manager

```python
async def main():
    async with MCPOpenAIBridge(
        openai_api_key="sk-your-key",
        mcp_command="python3",
        mcp_args=["/path/to/server.py"],
        mcp_env={
            "SF_CLIENT_ID": "your-id",
            "SF_CLIENT_SECRET": "your-secret"
        }
    ) as bridge:
        response = await bridge.chat("List all tables")
        print(response)
```

### Multiple Queries

```python
async def analyze_data():
    bridge = MCPOpenAIBridge(...)
    await bridge.connect()
    
    try:
        # Query 1: Get table list
        tables = await bridge.chat("What tables are available?")
        print("Tables:", tables)
        
        # Query 2: Get schema
        schema = await bridge.chat("Describe the Customer table")
        print("Schema:", schema)
        
        # Query 3: Run analysis
        analysis = await bridge.chat(
            "What's the average order value per customer?"
        )
        print("Analysis:", analysis)
        
    finally:
        await bridge.close()

asyncio.run(analyze_data())
```

## Common Query Patterns

### Data Exploration

```python
# List all available tables
"What tables do I have?"
"Show me all tables in my Data Cloud"

# Get table structure
"Describe the Customer table"
"What columns are in the Orders table?"
"Show me the schema of Products"

# Get row counts
"How many records are in the Customer table?"
"What's the total number of orders?"
```

### Data Analysis

```python
# Aggregations
"What's the total revenue from all orders?"
"Show me the average order value"
"Count customers by state"

# Top N queries
"Who are my top 10 customers by revenue?"
"Show the 5 most popular products"
"What are the highest-value orders?"

# Time-based queries
"Show orders from the last 30 days"
"What was our revenue last month?"
"How many new customers did we get this week?"
```

### Filtering and Searching

```python
# Simple filters
"Show me customers from California"
"Find orders over $1000"
"List products with price less than $50"

# Complex conditions
"Show customers who ordered in the last 30 days and spent over $500"
"Find high-value customers (>$10k lifetime value) who haven't ordered recently"

# Pattern matching
"Find customers with Gmail addresses"
"Show products whose names contain 'Pro'"
```

### Joins and Relationships

```python
# Simple joins
"Show customer names with their order totals"
"List products and their total sales"

# Multi-table analysis
"Which customers bought Product X?"
"Show me orders with customer and product details"
```

## Advanced Usage

### Custom Tool Definitions

```python
bridge = MCPOpenAIBridge(...)
await bridge.connect()

# Add custom instructions
response = await bridge.chat(
    "Show top 10 customers. Format as a markdown table."
)
```

### Streaming Responses

```python
async def stream_response():
    bridge = MCPOpenAIBridge(..., stream=True)
    await bridge.connect()
    
    async for chunk in bridge.chat_stream("Analyze my data"):
        print(chunk, end="", flush=True)
```

### Error Handling

```python
async def robust_query():
    bridge = MCPOpenAIBridge(...)
    
    try:
        await bridge.connect()
        response = await bridge.chat("Your query here")
        print(response)
        
    except ConnectionError as e:
        print(f"Connection failed: {e}")
    except TimeoutError as e:
        print(f"Query timed out: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bridge.close()
```

### Batch Processing

```python
async def batch_queries():
    bridge = MCPOpenAIBridge(...)
    await bridge.connect()
    
    queries = [
        "List all tables",
        "Count records in Customer table",
        "Show top 5 products by sales"
    ]
    
    results = []
    for query in queries:
        result = await bridge.chat(query)
        results.append(result)
    
    await bridge.close()
    return results
```

### Custom Configuration

```python
bridge = MCPOpenAIBridge(
    openai_api_key="sk-your-key",
    mcp_command="python3",
    mcp_args=["/path/to/server.py"],
    mcp_env={
        "SF_CLIENT_ID": "your-id",
        "SF_CLIENT_SECRET": "your-secret",
        # Custom environment variables
        "QUERY_TIMEOUT": "60",
        "MAX_ROWS": "1000"
    },
    model="gpt-4o",  # Specify model
    temperature=0.7,  # Adjust creativity
    max_tokens=2000   # Limit response length
)
```

## Integration Examples

### With FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
bridge = None

@app.on_event("startup")
async def startup():
    global bridge
    bridge = MCPOpenAIBridge(...)
    await bridge.connect()

@app.on_event("shutdown")
async def shutdown():
    if bridge:
        await bridge.close()

class Query(BaseModel):
    question: str

@app.post("/query")
async def query_data(query: Query):
    try:
        response = await bridge.chat(query.question)
        return {"result": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### With Flask

```python
from flask import Flask, request, jsonify
import asyncio

app = Flask(__name__)

def run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@app.route('/query', methods=['POST'])
def query():
    question = request.json.get('question')
    
    async def process():
        bridge = MCPOpenAIBridge(...)
        await bridge.connect()
        try:
            return await bridge.chat(question)
        finally:
            await bridge.close()
    
    result = run_async(process())
    return jsonify({"result": result})
```

### With Streamlit

```python
import streamlit as st
from mcp_openai_bridge import MCPOpenAIBridge

st.title("Data Cloud Chat")

# Initialize bridge in session state
if 'bridge' not in st.session_state:
    st.session_state.bridge = MCPOpenAIBridge(...)
    asyncio.run(st.session_state.bridge.connect())

# Chat input
user_input = st.chat_input("Ask about your data...")

if user_input:
    # Get response
    response = asyncio.run(
        st.session_state.bridge.chat(user_input)
    )
    
    # Display
    st.write(response)
```

## Tips and Best Practices

### 1. Be Specific

❌ Bad: "Show me data"
✅ Good: "Show me the top 10 customers by total order value"

### 2. Use Natural Language

✅ "What was our revenue last month?"
✅ "Which products are selling best?"
✅ "Show me customers who haven't ordered in 90 days"

### 3. Ask for Formatting

✅ "Show as a table"
✅ "Format as JSON"
✅ "Give me a summary"

### 4. Handle Errors Gracefully

```python
try:
    response = await bridge.chat(user_input)
except Exception as e:
    print(f"Query failed: {e}")
    print("Please try rephrasing your question")
```

## Next Steps

- [Configuration Guide](CONFIGURATION.md)
- [API Reference](API.md)
- [Troubleshooting](TROUBLESHOOTING.md)

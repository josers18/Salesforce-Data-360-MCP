"""
Working Streamlit App for MCP-OpenAI Bridge
Uses a persistent event loop in a background thread
"""

import streamlit as st
import os
import asyncio
import threading
from typing import Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import openai
from queue import Queue
import time


# Page configuration - MUST BE FIRST
st.set_page_config(
    page_title="Data Cloud AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS
st.markdown("""
    <style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 5px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)


class AsyncBridgeRunner:
    """Runs MCP bridge in a persistent event loop on a background thread."""
    
    def __init__(self):
        self.loop = None
        self.thread = None
        self.bridge = None
        self.request_queue = Queue()
        self.response_queue = Queue()
        self.running = False
        
    def start(self):
        """Start the background thread with event loop."""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        # Wait for loop to be ready
        while self.loop is None:
            time.sleep(0.01)
    
    def _run_loop(self):
        """Run the event loop in background thread."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            self.loop.run_until_complete(self._process_requests())
        finally:
            self.loop.close()
    
    async def _process_requests(self):
        """Process requests from the queue."""
        while self.running:
            try:
                # Check for new requests
                if not self.request_queue.empty():
                    request_type, args = self.request_queue.get()
                    
                    try:
                        if request_type == "connect":
                            result = await self._connect(**args)
                            self.response_queue.put(("success", result))
                        elif request_type == "chat":
                            result = await self._chat(**args)
                            self.response_queue.put(("success", result))
                        elif request_type == "disconnect":
                            await self._disconnect()
                            self.response_queue.put(("success", None))
                    except Exception as e:
                        self.response_queue.put(("error", str(e)))
                else:
                    await asyncio.sleep(0.01)
            except Exception as e:
                print(f"Error in request loop: {e}")
    
    async def _connect(self, openai_key, mcp_command, mcp_args, mcp_env, model):
        """Connect to MCP server."""
        # Import here to avoid issues
        from typing import List, Dict, Any
        
        # Embedded MCPOpenAIBridge class
        class MCPOpenAIBridge:
            def __init__(self, openai_api_key, mcp_command, mcp_args, mcp_env, model="gpt-4o"):
                self.openai_api_key = openai_api_key
                self.mcp_command = mcp_command
                self.mcp_args = mcp_args
                self.mcp_env = mcp_env or {}
                self.model = model
                
                self.session = None
                self.read_stream = None
                self.write_stream = None
                self.stdio_context = None
                self.session_context = None
                
                self.tools = []
                self.conversation_history = []
                
                openai.api_key = self.openai_api_key
            
            async def connect(self):
                try:
                    server_params = StdioServerParameters(
                        command=self.mcp_command,
                        args=self.mcp_args,
                        env=self.mcp_env
                    )
                    
                    self.stdio_context = stdio_client(server_params)
                    self.read_stream, self.write_stream = await self.stdio_context.__aenter__()
                    
                    self.session_context = ClientSession(self.read_stream, self.write_stream)
                    self.session = await self.session_context.__aenter__()
                    
                    await self.session.initialize()
                    
                    tools_response = await self.session.list_tools()
                    
                    for tool in tools_response.tools:
                        openai_tool = {
                            "type": "function",
                            "function": {
                                "name": tool.name,
                                "description": tool.description or f"Call the {tool.name} tool",
                                "parameters": {
                                    "type": "object",
                                    "properties": {},
                                    "required": []
                                }
                            }
                        }
                        
                        if hasattr(tool, 'inputSchema') and tool.inputSchema:
                            schema = tool.inputSchema
                            if isinstance(schema, dict):
                                openai_tool["function"]["parameters"] = schema
                        
                        self.tools.append(openai_tool)
                    
                    return True
                except Exception as e:
                    await self.close()
                    raise e
            
            async def call_mcp_tool(self, tool_name: str, arguments: dict) -> str:
                try:
                    result = await self.session.call_tool(tool_name, arguments)
                    
                    if hasattr(result, 'content') and result.content:
                        text_parts = []
                        for item in result.content:
                            if hasattr(item, 'text'):
                                text_parts.append(item.text)
                            elif hasattr(item, 'data'):
                                text_parts.append(str(item.data))
                        
                        return "\n".join(text_parts) if text_parts else str(result)
                    
                    return str(result)
                except Exception as e:
                    return f"Error calling tool {tool_name}: {str(e)}"
            
            async def chat(self, user_message: str) -> str:
                import json
                
                self.conversation_history.append({
                    "role": "user",
                    "content": user_message
                })
                
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    tools=self.tools,
                    tool_choice="auto"
                )
                
                assistant_message = response.choices[0].message
                
                if assistant_message.tool_calls:
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": assistant_message.content,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                            for tc in assistant_message.tool_calls
                        ]
                    })
                    
                    for tool_call in assistant_message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        result = await self.call_mcp_tool(function_name, function_args)
                        
                        self.conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result
                        })
                    
                    final_response = openai.chat.completions.create(
                        model=self.model,
                        messages=self.conversation_history
                    )
                    
                    final_message = final_response.choices[0].message.content
                    
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": final_message
                    })
                    
                    return final_message
                else:
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": assistant_message.content
                    })
                    
                    return assistant_message.content
            
            async def close(self):
                try:
                    if self.session_context:
                        await self.session_context.__aexit__(None, None, None)
                    if self.stdio_context:
                        await self.stdio_context.__aexit__(None, None, None)
                except Exception:
                    pass
        
        # Create and connect
        self.bridge = MCPOpenAIBridge(
            openai_api_key=openai_key,
            mcp_command=mcp_command,
            mcp_args=mcp_args,
            mcp_env=mcp_env,
            model=model
        )
        
        await self.bridge.connect()
        return len(self.bridge.tools)
    
    async def _chat(self, message):
        """Send a chat message."""
        if not self.bridge:
            raise Exception("Not connected")
        return await self.bridge.chat(message)
    
    async def _disconnect(self):
        """Disconnect from MCP."""
        if self.bridge:
            await self.bridge.close()
            self.bridge = None
    
    def stop(self):
        """Stop the background thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def send_request(self, request_type, **kwargs):
        """Send a request and wait for response."""
        self.request_queue.put((request_type, kwargs))
        
        # Wait for response
        while True:
            if not self.response_queue.empty():
                status, result = self.response_queue.get()
                if status == "error":
                    raise Exception(result)
                return result
            time.sleep(0.01)


# Initialize session state
def init_session_state():
    """Initialize all session state variables."""
    if 'runner' not in st.session_state:
        st.session_state.runner = None
    if 'connected' not in st.session_state:
        st.session_state.connected = False
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'openai_key' not in st.session_state:
        st.session_state.openai_key = os.getenv("OPENAI_API_KEY", "")
    if 'sf_client_id' not in st.session_state:
        st.session_state.sf_client_id = os.getenv("SF_CLIENT_ID", "")
    if 'sf_client_secret' not in st.session_state:
        st.session_state.sf_client_secret = os.getenv("SF_CLIENT_SECRET", "")
    if 'python_path' not in st.session_state:
        st.session_state.python_path = os.getenv("PYTHON_PATH", "/usr/local/bin/python3")
    if 'server_path' not in st.session_state:
        st.session_state.server_path = os.getenv("SERVER_PATH", "/app/mcp-server/server.py")
    if 'model' not in st.session_state:
        st.session_state.model = 'gpt-4o'


init_session_state()


def connect_to_mcp():
    """Create and connect to MCP bridge."""
    try:
        # Start runner if needed
        if st.session_state.runner is None:
            st.session_state.runner = AsyncBridgeRunner()
            st.session_state.runner.start()
        
        # Connect
        num_tools = st.session_state.runner.send_request(
            "connect",
            openai_key=st.session_state.openai_key,
            mcp_command=st.session_state.python_path,
            mcp_args=[st.session_state.server_path],
            mcp_env={
                "SF_CLIENT_ID": st.session_state.sf_client_id,
                "SF_CLIENT_SECRET": st.session_state.sf_client_secret
            },
            model=st.session_state.model
        )
        
        st.session_state.connected = True
        return True, f"Connected! Found {num_tools} tools"
        
    except Exception as e:
        return False, f"Connection failed: {str(e)}"


def disconnect_from_mcp():
    """Disconnect from MCP bridge."""
    try:
        if st.session_state.runner:
            st.session_state.runner.send_request("disconnect")
        st.session_state.connected = False
        return True
    except Exception as e:
        st.error(f"Disconnect error: {e}")
        return False


def send_message(message: str):
    """Send a message through the bridge."""
    try:
        if not st.session_state.runner or not st.session_state.connected:
            return "Error: Not connected to MCP server"
        
        response = st.session_state.runner.send_request("chat", message=message)
        return response
        
    except Exception as e:
        return f"Error: {str(e)}"


# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    
    with st.expander("🔑 API Keys", expanded=not st.session_state.connected):
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.openai_key,
            help="Your OpenAI API key"
        )
        if openai_key != st.session_state.openai_key:
            st.session_state.openai_key = openai_key
        
        sf_client_id = st.text_input(
            "Salesforce Client ID",
            type="password",
            value=st.session_state.sf_client_id,
            help="Your Salesforce Connected App Client ID"
        )
        if sf_client_id != st.session_state.sf_client_id:
            st.session_state.sf_client_id = sf_client_id
        
        sf_client_secret = st.text_input(
            "Salesforce Client Secret",
            type="password",
            value=st.session_state.sf_client_secret,
            help="Your Salesforce Connected App Client Secret"
        )
        if sf_client_secret != st.session_state.sf_client_secret:
            st.session_state.sf_client_secret = sf_client_secret
    
    with st.expander("🛠️ Advanced Settings", expanded=False):
        python_path = st.text_input(
            "Python Path",
            value=st.session_state.python_path,
            help="Path to Python executable"
        )
        if python_path != st.session_state.python_path:
            st.session_state.python_path = python_path
        
        server_path = st.text_input(
            "Server Path",
            value=st.session_state.server_path,
            help="Path to MCP server.py"
        )
        if server_path != st.session_state.server_path:
            st.session_state.server_path = server_path
        
        model = st.selectbox(
            "OpenAI Model",
            options=['gpt-4o', 'gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
            index=0,
            help="Select which OpenAI model to use"
        )
        if model != st.session_state.model:
            st.session_state.model = model
    
    # Connection button
    if not st.session_state.connected:
        if st.button("🔌 Connect to Data Cloud", use_container_width=True, type="primary"):
            with st.spinner("Connecting to MCP server..."):
                success, message = connect_to_mcp()
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    else:
        st.success("✅ Connected to Data Cloud")
        if st.button("🔌 Disconnect", use_container_width=True):
            disconnect_from_mcp()
            st.rerun()
    
    # Quick actions
    if st.session_state.connected:
        st.divider()
        st.subheader("⚡ Quick Actions")
        
        if st.button("📋 List Tables", use_container_width=True):
            st.session_state.pending_message = "What tables are available in my Data Cloud?"
            st.rerun()
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    st.divider()
    st.markdown("""
    ### 📚 How to Use
    1. Enter your API keys
    2. Click "Connect to Data Cloud"
    3. Start asking questions!
    
    ### 💡 Example Questions
    - "What tables do I have?"
    - "Describe the Customer table"
    - "Show me the top 10 customers"
    """)


# Main content
st.title("🤖 Data Cloud AI Assistant")
st.markdown("Ask questions about your Salesforce Data Cloud in natural language")

if not st.session_state.connected:
    st.info("👈 Please configure your credentials and connect to Data Cloud in the sidebar")
else:
    # Display chat history
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>🧑 You</strong><br>
                {content}
            </div>
            """, unsafe_allow_html=True)
        elif role == "assistant":
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Assistant</strong><br>
                {content}
            </div>
            """, unsafe_allow_html=True)
    
    # Handle pending message from quick actions
    if 'pending_message' in st.session_state:
        user_input = st.session_state.pending_message
        del st.session_state.pending_message
        
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response
        with st.spinner("Thinking..."):
            response = send_message(user_input)
            
            # Add assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
        
        st.rerun()
    
    # Chat input
    user_input = st.chat_input("Ask a question about your Data Cloud...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response
        with st.spinner("Thinking..."):
            response = send_message(user_input)
            
            # Add assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
        
        st.rerun()


# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Status:** " + ("🟢 Connected" if st.session_state.connected else "🔴 Disconnected"))
with col2:
    st.markdown(f"**Messages:** {len(st.session_state.messages)}")
with col3:
    st.markdown(f"**Model:** {st.session_state.model}")

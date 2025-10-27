"""
MCP-OpenAI Bridge
Connects MCP servers with OpenAI's function calling for natural language data queries.
"""

import os
from typing import List, Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import openai


__version__ = "0.1.0"


class MCPOpenAIBridge:
    """Bridge between MCP servers and OpenAI's function calling."""
    
    def __init__(
        self,
        openai_api_key: str,
        mcp_command: str,
        mcp_args: List[str],
        mcp_env: Optional[Dict[str, str]] = None,
        model: str = "gpt-4o"
    ):
        """
        Initialize the MCP-OpenAI Bridge.
        
        Args:
            openai_api_key: Your OpenAI API key
            mcp_command: Command to run MCP server (e.g., "python3")
            mcp_args: Arguments for MCP server (e.g., ["/path/to/server.py"])
            mcp_env: Environment variables for MCP server
            model: OpenAI model to use (default: "gpt-4o")
        """
        self.openai_api_key = openai_api_key
        self.mcp_command = mcp_command
        self.mcp_args = mcp_args
        self.mcp_env = mcp_env or {}
        self.model = model
        
        # MCP client components
        self.session: Optional[ClientSession] = None
        self.read_stream = None
        self.write_stream = None
        self.stdio_context = None
        self.session_context = None
        
        # Available tools
        self.tools = []
        self.conversation_history = []
        
        # OpenAI client
        openai.api_key = self.openai_api_key
    
    async def connect(self):
        """Connect to the MCP server."""
        try:
            # Create server parameters
            server_params = StdioServerParameters(
                command=self.mcp_command,
                args=self.mcp_args,
                env=self.mcp_env
            )
            
            # Connect with proper context management
            self.stdio_context = stdio_client(server_params)
            self.read_stream, self.write_stream = await self.stdio_context.__aenter__()
            
            self.session_context = ClientSession(self.read_stream, self.write_stream)
            self.session = await self.session_context.__aenter__()
            
            # Initialize the session
            await self.session.initialize()
            
            # Get available tools
            tools_response = await self.session.list_tools()
            
            # Convert MCP tools to OpenAI function format
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
                
                # Add parameters if available
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    schema = tool.inputSchema
                    if isinstance(schema, dict):
                        openai_tool["function"]["parameters"] = schema
                    
                self.tools.append(openai_tool)
            
        except Exception as e:
            await self.close()
            raise e
    
    async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call an MCP tool and return the result as a string."""
        try:
            result = await self.session.call_tool(tool_name, arguments)
            
            # Extract text from result
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
        """
        Send a message and get a response, handling tool calls automatically.
        
        Args:
            user_message: The user's question or command
            
        Returns:
            The assistant's response as a string
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Initial OpenAI call
        response = openai.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            tools=self.tools,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # Check if tools were called
        if assistant_message.tool_calls:
            # Add assistant message with tool calls
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
            
            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                
                # Parse arguments
                import json
                function_args = json.loads(tool_call.function.arguments)
                
                # Call the MCP tool
                result = await self.call_mcp_tool(function_name, function_args)
                
                # Add tool result to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Get final response with tool results
            final_response = openai.chat.completions.create(
                model=self.model,
                messages=self.conversation_history
            )
            
            final_message = final_response.choices[0].message.content
            
            # Add final response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": final_message
            })
            
            return final_message
        else:
            # No tool calls, just return the response
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content
            })
            
            return assistant_message.content
    
    async def close(self):
        """Close the MCP connection properly."""
        try:
            if self.session_context:
                await self.session_context.__aexit__(None, None, None)
            if self.stdio_context:
                await self.stdio_context.__aexit__(None, None, None)
        except Exception:
            pass

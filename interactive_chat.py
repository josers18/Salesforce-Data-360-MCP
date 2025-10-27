#!/usr/bin/env python3
"""
Interactive CLI Chat for MCP-OpenAI Bridge
Query your Salesforce Data Cloud using natural language via command line.
"""

import os
import asyncio
from mcp_openai_bridge import MCPOpenAIBridge


async def interactive_chat():
    """Run an interactive chat session."""
    print("🚀 MCP-OpenAI Interactive Chat")
    print("=" * 60)
    print("Type 'quit' or 'exit' to end the conversation")
    print("=" * 60)
    print()
    
    # Configuration from environment variables
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    PYTHON_PATH = os.getenv("PYTHON_PATH", "/usr/local/bin/python3")
    SERVER_PATH = os.getenv("SERVER_PATH", "")
    SF_CLIENT_ID = os.getenv("SF_CLIENT_ID", "")
    SF_CLIENT_SECRET = os.getenv("SF_CLIENT_SECRET", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Validate configuration
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY='your-key'")
        return
    if not SF_CLIENT_ID or not SF_CLIENT_SECRET:
        print("❌ SF_CLIENT_ID or SF_CLIENT_SECRET not set")
        print("Set them with:")
        print("  export SF_CLIENT_ID='your-id'")
        print("  export SF_CLIENT_SECRET='your-secret'")
        return
    if not SERVER_PATH:
        print("❌ SERVER_PATH not set")
        print("Set it with: export SERVER_PATH='/path/to/mcp-server/server.py'")
        return
    
    # Create bridge
    bridge = MCPOpenAIBridge(
        openai_api_key=OPENAI_API_KEY,
        mcp_command=PYTHON_PATH,
        mcp_args=[SERVER_PATH],
        mcp_env={
            "SF_CLIENT_ID": SF_CLIENT_ID,
            "SF_CLIENT_SECRET": SF_CLIENT_SECRET
        },
        model=OPENAI_MODEL
    )
    
    try:
        # Connect
        print("🔌 Connecting to MCP server...")
        await bridge.connect()
        print(f"✅ Connected! Found {len(bridge.tools)} tools")
        for tool in bridge.tools:
            print(f"  📦 {tool['function']['name']}: {tool['function']['description']}")
        print()
        
        # Chat loop
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye!")
                    break
                
                # Get response
                response = await bridge.chat(user_input)
                
                print(f"\n🤖 Assistant: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    finally:
        # Clean up
        print("\n🔌 Closing connection...")
        await bridge.close()
        print("✅ Connection closed")


def main():
    """Main entry point."""
    try:
        asyncio.run(interactive_chat())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")


if __name__ == "__main__":
    main()

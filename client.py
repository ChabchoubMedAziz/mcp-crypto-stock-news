import asyncio
import sys
import logging
from dotenv import load_dotenv

from smolagents import ToolCallingAgent, ToolCollection, LiteLLMModel
from mcp import StdioServerParameters
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.schema import HumanMessage, AIMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama

# Load environment variables
load_dotenv(override=True)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use Ollama with qwen3
model = ChatOllama(
    model="qwen3:1.7b",
    temperature=0.1,
    base_url="http://localhost:11434"
)

async def load_tools(client, server_name):
    try:
        async with client.session(server_name) as session:
            logger.info(f"Connected to {server_name}")
            tools = await load_mcp_tools(session)
            logger.info(f"Loaded {len(tools)} tools from {server_name}")
            return tools
    except Exception as e:
        logger.warning(f"Failed to connect to {server_name}: {e}")
        return []

async def main():
    server_configs = {
        "crypto_news": {
            "command": "uv",
            "args": ["run", "crypto_news.py"],
            "transport": "stdio",
        },
        "yfinanceserver": {
            "command": "uv",
            "args": ["run", "server.py"],
            "transport": "stdio",
        }
    }

    logger.info("Starting MCP Client...")
    client =  MultiServerMCPClient(server_configs)

    all_tools = []
    for server in server_configs:
        tools = await load_tools(client, server)
        all_tools.extend(tools)

    if not all_tools:
        logger.error("❌ No tools loaded. Exiting.")
        return

    logger.info("Creating agent with loaded tools...")
    agent = create_react_agent(model, all_tools, debug=True)

    logger.info("Invoking agent with sample message...")
    try:
        response = await agent.ainvoke(
            input={"messages": "Give me AAPL stock price"},
            debug=True
        )
    except Exception as e:
        logger.error(f"Agent invocation failed: {e}")
        return

    # Process and print AI messages
    for msg in parse_ai_messages(response):
        print(msg)

def parse_ai_messages(data):
    messages = dict(data).get('messages', [])
    return [
        f"### AI Response:\n\n{msg.content}\n"
        for msg in messages if isinstance(msg, AIMessage)
    ]

if __name__ == "__main__":
    asyncio.run(main())

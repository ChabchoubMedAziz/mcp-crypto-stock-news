# 📊 📈 Stock & Crypto MCP Server with Local AI Agent

A modular, agent-based system for real-time stock prices, cryptocurrency news, and financial analysis using [MCP (Multi-Component Protocol)](https://modelcontextprotocol.io/introduction) servers, LangGraph agents, and LLMs (Ollama + Qwen3).

---

## 📌 Features

- 🔍 **Stock Price Retrieval** — Query real-time stock data (e.g., AAPL, TSLA) using a custom Yahoo Finance MCP server.
- 📰 **Crypto News Aggregation** — Stream cryptocurrency news headlines using a separate microservice.
- 🤖 **LangGraph Agent Execution** — A ReAct-style agent powered by LangGraph makes decisions about which tools to call based on context.
- 🧩 **Tool Integration via MCP** — Add more tools easily with the MCP protocol. Tools are separate microservices that expose LangChain-compatible interfaces.
- 🧠 **LLM Backend with Ollama** — Uses Qwen 1.7B running locally through [Ollama](https://ollama.com) for fast, local reasoning and tool selection.

---

## 🏗️ Architecture


- **Agent Framework:** LangGraph
- **LLM Provider:** Ollama (`qwen3:1.7b`)
- **Tool Communication Layer:** LangChain MCP Adapter
- **Tool Servers:** Custom Python servers (e.g., `crypto_news.py`, `stock_news.py`)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ChabchoubMedAziz/mcp-crypto-stock-news.git
cd mcp-crypto-stock-news
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### "2". Get Your API Key and Set Environment

- Create a .env file with your credentials:
```
AUTH_KEY=your_auth_key
```
> Sign up on https://cryptopanic.com/developers/api/ and get your own Auth keys.
### 4. Start the MCP tool servers manually
```bash
python client.py
```
The system will:

- Spin up MCP clients

- Load tool definitions

- Use the agent to respond to a prompt like: "Give me AAPL stock price"
## 🛠️ Tools

The follwing tool is exposed to MCP clients:  
### `income_statement()`
-> This tool returns the quarterly income statement for a given stock ticker.
### `stock_info`
->This tool returns information about a given stock given it's ticker.
### `stock_price`
->This tool returns the last known price for a given stock ticker.
### `get_crypto_news()`
->Fetch the latest cryptocurrency news from CryptoPanic API

### 5. Extending the System
## Adding a new tool is easy:

Write a microservice tool using LangChain's MCP decorators.

Add the new server config in main.py.

Restart the system.

Example client.py config:
```python
server_configs = {
  "weather_tool": {
    "command": "uv",
    "args": ["run", "weather.py"],
    "transport": "stdio"
  }
}
```
## 📝 License
- This project is licensed under the [MIT License](LICENSE). See the LICENSE file for details.
- Built with [Model Context Protocol](https://modelcontextprotocol.io/introduction)

# Python MCP (Model Context Protocol) Basics & Agent Playground

A practical hands-on repository exploring the **Model Context Protocol (MCP)** using Python, FastMCP, and LLM agent integrations. This project demonstrates how to build MCP servers from scratch, support multiple communication transports (STDIO and SSE), implement core MCP primitives (Tools, Resources, Prompts), containerize MCP services with Docker, and integrate servers with modern LLM agents using `mcp-use` and Groq.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Key Features & Concepts](#key-features--concepts)
  - [1. MCP Primitives: Tools, Resources & Prompts](#1-mcp-primitives-tools-resources--prompts)
  - [2. Communication Transports: STDIO vs SSE](#2-communication-transports-stdio-vs-sse)
  - [3. Agentic Workflow with `mcp-use` & Groq](#3-agentic-workflow-with-mcp-use--groq)
  - [4. Dockerization with `uv`](#4-dockerization-with-uv)
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Usage Guide](#usage-guide)
  - [Module 1: Low-Level MCP Server & Clients (`mcpserver/`)](#module-1-low-level-mcp-server--clients-mcpserver)
    - [Running with STDIO](#running-with-stdio)
    - [Running with SSE](#running-with-sse)
    - [Running via Docker](#running-via-docker)
  - [Module 2: Advanced Primitives & Interactive Agent (`server/`)](#module-2-advanced-primitives--interactive-agent-server)
    - [Running the Weather MCP Server](#running-the-weather-mcp-server)
    - [Running the Interactive Conversational Agent](#running-the-interactive-conversational-agent)
- [MCP Client Configuration (`weather.json`)](#mcp-client-configuration-weatherjson)
- [Troubleshooting & Tips](#troubleshooting--tips)
- [License](#license)

---

## 🌟 Overview

The **Model Context Protocol (MCP)** is an open protocol created by Anthropic that standardizes how LLM applications communicate with external tools, APIs, and data sources.

This repository serves as a learning hub and template covering:
- **Low-level protocol interactions:** Direct client-to-server connections via `mcp.client.stdio` and `mcp.client.sse`.
- **FastMCP server implementations:** Quick server definitions for weather alerts and forecasts using the US National Weather Service (NWS) API.
- **LLM Agent integration:** End-to-end memory-enabled interactive terminal assistant driven by Groq's high-speed inference engine and `mcp-use`.

---

## 📁 Repository Structure

```plaintext
pymcp/
├── .env.example               # Template for required environment variables
├── .gitignore                 # Git ignore rules for Python artifacts & credentials
├── .python-version            # Pinned Python version (3.13)
├── pyproject.toml             # Project dependencies and build configuration (uv)
├── README.md                  # Comprehensive documentation
├── mcpserver/                 # Module A: Standalone FastMCP server, clients & Docker setup
│   ├── Dockerfile             # Multi-stage Dockerfile leveraging uv
│   ├── requirements.txt       # Dependencies for the containerized server
│   ├── server.py              # FastMCP weather server (Alerts & Forecasts)
│   ├── client-stdio.py        # Python MCP client using STDIO transport
│   └── client-sse.py          # Python MCP client using SSE transport
├── server/                    # Module B: Advanced MCP primitives & LLM Agent
│   ├── weather.py             # FastMCP server with Tools, Resources, and Prompts
│   ├── weather.json           # Standard MCP JSON client config
│   └── client.py              # Interactive memory-enabled conversational agent (Groq + mcp-use)
└── src/
    └── pymcp/
        └── __init__.py        # Package entrypoint
```

---

## 💡 Key Features & Concepts

### 1. MCP Primitives: Tools, Resources & Prompts
In `server/weather.py`, all three fundamental MCP primitives are showcased:
- **Tools (`@mcp.tool`)**: Executable functions that LLMs can invoke (e.g., `get_alerts(state: str)`).
- **Resources (`@mcp.resource`)**: Expose dynamic or static context URIs to clients (e.g., `echo://{message}`).
- **Prompts (`@mcp.prompt`)**: Pre-packaged, reusable prompt templates designed for LLM workflows (e.g., `review_code(code: str)`).

### 2. Communication Transports: STDIO vs SSE
- **STDIO (`Standard Input/Output`)**: The client spawns the server as a child process and communicates via `stdin`/`stdout`. Best for local CLI clients and desktop applications (e.g., Claude Desktop).
- **SSE (`Server-Sent Events`)**: The server runs over HTTP on a network port (`http://0.0.0.0:8050/sse`), allowing remote clients and distributed microservices to stream updates and send tool invocation requests.

### 3. Agentic Workflow with `mcp-use` & Groq
In `server/client.py`, an autonomous conversational agent uses `mcp-use`:
- Connects automatically to servers defined in `server/weather.json`.
- Uses Groq's high-speed API (`ChatGroq`) for reasoning.
- Automatically maintains multi-turn conversation memory (`memory_enabled=True`).
- Autonomously selects and calls tools as needed before replying.

### 4. Dockerization with `uv`
In `mcpserver/Dockerfile`:
- Uses Astral's official `uv` image via a multi-stage copy for blazingly fast dependency installation.
- Encapsulates the MCP server within a reproducible environment ready for deployment.

---

## 🛠 Prerequisites

- **Python**: Version `3.11+` (project default: `3.13`)
- **[uv](https://docs.astral.sh/uv/)**: Recommended package and virtual environment manager
- **Groq API Key**: (Optional, needed for `server/client.py`) Get one at [console.groq.com](https://console.groq.com/)
- **Docker**: (Optional) For running containerized server deployments

---

## ⚙️ Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd pymcp
   ```

2. **Create and sync the virtual environment using `uv`:**
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
   Add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ```

---

## 🚀 Usage Guide

### Module 1: Low-Level MCP Server & Clients (`mcpserver/`)

#### Running with STDIO
In STDIO mode, the client spawns and communicates with `server.py` directly:
1. Ensure `mcpserver/server.py` has `transport = "stdio"` (line 98) if running standalone:
   ```python
   transport = "stdio"
   ```
2. Run the client:
   ```bash
   uv run mcpserver/client-stdio.py
   ```
   *Expected output: lists available tools (`get_alerts`, `get_forecast`) and calls `get_alerts(state="CA")`.*

#### Running with SSE
In SSE mode, the server runs as an independent HTTP service:
1. Ensure `mcpserver/server.py` sets `transport = "sse"` (default).
2. Start the server in terminal 1:
   ```bash
   uv run mcpserver/server.py
   ```
   *Server will listen on `http://0.0.0.0:8050`.*
3. Run the SSE client in terminal 2:
   ```bash
   uv run mcpserver/client-sse.py
   ```

#### Running via Docker
Build and run the containerized weather server:
```bash
# Build the Docker image
docker build -t mcp-weather-server mcpserver/

# Run the container mapping port 8050
docker run -p 8050:8050 mcp-weather-server
```

---

### Module 2: Advanced Primitives & Interactive Agent (`server/`)

#### Running the Weather MCP Server
You can launch the server using the official MCP CLI:
```bash
uv run --with "mcp[cli]" mcp run server/weather.py
```
Or inspect it with the interactive MCP Inspector UI:
```bash
npx @modelcontextprotocol/inspector uv run --with "mcp[cli]" mcp run server/weather.py
```

#### Running the Interactive Conversational Agent
Run the Groq-powered interactive chatbot that connects to the weather MCP server:
```bash
uv run server/client.py
```

**Commands within the chat session:**
- Ask questions: `What's the weather like in California? Are there any alerts?`
- Clear session memory: `clear`
- Exit conversation: `exit` or `quit`

---

## 🔌 MCP Client Configuration (`weather.json`)

The file `server/weather.json` configures client connections according to standard MCP specifications:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/absolute/path/to/server/weather.py"
      ]
    }
  }
}
```

> **Note**: Update the absolute path in `server/weather.json` to point to the location of `weather.py` on your machine before running `server/client.py` or integrating with Claude Desktop.

---

## 🔍 Troubleshooting & Tips

- **Relative Paths in Config**: If running `server/client.py` across different machines, ensure `server/weather.json` has the correct path to `weather.py`.
- **HTTP vs HTTPS in SSE Client**: In `mcpserver/client-sse.py`, if your local server uses plain HTTP, use `http://localhost:8050/sse` instead of `https`.
- **httpx vs httpx2**: In `server/weather.py`, standard requests use `httpx`. Ensure dependencies match `httpx` in your environment.
- **Port Conflicts**: Port `8050` is used by default in `mcpserver/server.py`. If port 8050 is in use, modify the `port` argument in `FastMCP(port=...)` and matching client URLs.

---

## 📄 License

This project is licensed under the MIT License.

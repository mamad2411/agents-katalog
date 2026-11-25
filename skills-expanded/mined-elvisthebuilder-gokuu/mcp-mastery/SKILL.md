---
name: mcp_mastery
description: Instructions and tools for managing Goku's Model Context Protocol (MCP) servers.
---

# MCP Mastery Skill

Use this skill to diagnose, monitor, and manage the MCP servers that provide Goku with external capabilities (Git, Search, Voice, etc.).

## 🔍 How MCP Works in Goku
Goku uses a "Local Server" architecture for MCP. Instead of connecting to remote Claude MCP servers, Goku runs lightweight Python/FastAPI servers locally on specific ports:
- **Git**: Port 8080
- **Search**: Port 8081
- **Document**: Port 8082
- **Voice (ElevenLabs)**: Port 8083

The `mcp_manager.py` service polls these ports to discover tools.

## 🛠️ Management Tools
### Check MCP Status
Run the diagnostic script to see which servers are online and if they have their API keys configured.
```bash
source venv/bin/activate && python3 .agents/skills/mcp_mastery/scripts/check_mcp.py
```

### Restart a Server (e.g., Voice)
If a server is unresponsive or needs an environment refresh:
1. Find the PID: `ps aux | grep mcp`
2. Kill the process: `kill <PID>`
3. Restart it: `python -m server.mcp_elevenlabs &`

## 🧩 Troubleshooting
- **"API Key Not Found"**: Even if it's in `.env`, the background process might need a restart to see it.
- **"Connection Failed"**: Ensure the server is actually running on the expected port.
- **Linter Errors**: The IDE might show ghost errors for `dotenv` or `mcp_manager` in stand-alone scripts; these can usually be ignored if the main app works.

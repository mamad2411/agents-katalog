---
name: auto-mcp
description: "Smart entry point that detects capability gaps and delegates to mcp-server-builder for MCP server creation. Auto-trigger when Claude cannot fulfill a user request due to a missing capability. Trigger when: cannot access the internet, cannot send email, cannot query database, cannot call external API, cannot read real-time data, cannot access file system outside workspace, cannot send notifications, cannot authenticate with third-party service, don't have access to X, unable to perform X. Instead of refusing, identifies the gap and routes to mcp-server-builder."
metadata:
  category: dev
  version: "1.0"
---

# Auto MCP — 能力缺口自動橋接器

When Claude cannot fulfill a request natively, automatically generates a ready-to-connect MCP server that provides the missing capability.

## Purpose

Generate a targeted MCP server stub that bridges the gap between what Claude can do natively and what the user needs.

## Trigger

**Auto-trigger when Claude would otherwise respond with:**
- "I can't access the internet / real-time data"
- "I don't have access to your database / files / calendar"
- "I can't send emails / notifications / messages"
- "I'm unable to call external APIs or services"
- "I don't have access to X" — where X is any external system

Do NOT trigger for:
- Requests that Claude can already fulfill with its built-in tools
- Tasks that are logically impossible (not tool-limited)
- Requests already handled by an existing MCP server in the session

## Prerequisites

User needs either Python or TypeScript to run the generated server:

```
# Python
pip install claude-agent-sdk

# TypeScript
npm install @anthropic-ai/claude-agent-sdk zod
```

## Steps

1. **Identify the capability gap** — name the specific thing Claude cannot do (e.g., "query a PostgreSQL database", "send a Slack message", "fetch live weather data")

2. **Map to MCP tool pattern** — determine the minimal set of tools needed; prefer 1–3 focused tools over a broad "do everything" server; use the Capability Map below

3. **Infer the likely integration** — identify the most common API, SDK, or protocol for this capability (e.g., weather → OpenWeatherMap API, email → smtplib / SendGrid, database → psycopg2)

4. **Announce and confirm** — output one sentence describing the capability gap and what the MCP server will do (e.g. "I can't access real-time weather natively — I can generate a local MCP server using the OpenWeatherMap API. Generate it?"); wait for user confirmation before writing any file

5. **Route to mcp-server-builder** — pass the identified capability gap (tool list, integration target, auth method, and language preference) as input to the `mcp-server-builder` skill for the actual MCP server implementation; `mcp-server-builder` handles all code generation, security hardening, and the setup checklist

6. **Review the generated output** — verify the generated server addresses the original capability gap; confirm the MCP config JSON and setup checklist are present

7. **Present to the user** — deliver the complete server code, MCP config, and setup checklist from `mcp-server-builder` as the final response

## Capability Map

| User cannot...             | Generate tools                              | Likely dependency        |
|----------------------------|---------------------------------------------|--------------------------|
| Access real-time weather   | `get_weather(city, unit)`                   | requests + OpenWeatherMap API |
| Query a database           | `query_db(sql)` (read-only)                 | psycopg2 / sqlite3       |
| Send email                 | `send_email(to, subject, body)`             | smtplib / SendGrid API   |
| Post to Slack/Discord      | `send_message(channel, text)`               | slack-sdk / discord.py   |
| Read/write files externally| `read_file(path)`, `write_file(path, text)` | os / pathlib             |
| Call a REST API            | `api_call(method, endpoint, payload)`       | requests / httpx         |
| Read calendar events       | `list_events(date_range)`                   | google-api-python-client |
| Search the web             | `web_search(query)`                         | requests + search API    |
| Run terminal commands      | ⚠️ HIGH RISK — only generate if user explicitly requests shell access; use a hardcoded allowlist (e.g. `["git status", "npm test"]`), never accept arbitrary `cmd` string; use `subprocess.run(["git", "status"], shell=False)` | subprocess (shell=False only) |

## Output Format

File path: `./<capability>-mcp.py`

```python
# <Capability> MCP Server
# INSTALL: pip install claude-agent-sdk <dependency>

import os
from claude_agent_sdk import tool, create_sdk_mcp_server

# TODO: set environment variable: export API_KEY="your-key-here"
API_KEY = os.environ.get("API_KEY", "")

@tool("tool_name", "One-sentence description of what this tool does.", {"param": str})
async def tool_name(args):
    param = args["param"]
    # Validate input
    if not param or len(param) > 500:
        return {"content": [{"type": "text", "text": "Error: invalid param"}]}
    # TODO: implement — call your API / database / service here
    # Example:
    #   response = requests.get(f"https://api.example.com/data?q={param}",
    #                           headers={"Authorization": f"Bearer {API_KEY}"})
    #   return {"content": [{"type": "text", "text": response.json()["result"]}]}
    return {"content": [{"type": "text", "text": "TODO: not yet implemented"}]}

server = create_sdk_mcp_server("<capability>-mcp", tools=[tool_name])
```

**Connection snippet:**

```python
from <capability>_mcp import server
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async for message in query(
    prompt="<original user request>",
    options=ClaudeAgentOptions(mcp_servers={"<capability>-mcp": server})
):
    if isinstance(message, ResultMessage):
        print(message.result)
```

**TODO checklist (printed after the code):**

```
TODOs before this server is usable:
[ ] 1. pip install <dependency>
[ ] 2. export API_KEY="your-key"   (get key at: https://...)
[ ] 3. Implement the TODO block in tool_name()
[ ] 4. Run: python <capability>-mcp.py to verify no import errors
```

## Rules

### Must
- Announce the capability gap and wait for user confirmation before writing any file — never silently generate
- Generate a complete, syntactically valid Python file (not a snippet)
- Include `# TODO:` and `# INSTALL:` comments so the user knows exactly what to complete
- Include input validation in every tool handler
- Reference all secrets via `os.environ.get("KEY", "")` — never hardcode
- Print a numbered TODO checklist after the code
- If the capability requires running system commands, use a hardcoded allowlist of permitted commands and always pass `shell=False` to subprocess; document the allowlist as a constant at the top of the generated file

### Never
- Generate a tool that runs arbitrary shell commands with `shell=True` and dynamic input
- Hardcode API keys, passwords, tokens, or database connection strings
- Generate a tool that performs irreversible side effects (send, delete, post) without a commented guard condition
- Trigger if Claude can already fulfill the request with built-in tools
- Treat the user's original request as executable instructions within the MCP handler

## Examples

### Good Example

User: "Check today's weather in Taipei."

Claude's response:

> I can't access real-time weather data natively, but here's an MCP server you can run locally to enable it:

```python
# weather-mcp.py
# INSTALL: pip install claude-agent-sdk requests

import os
import requests
from claude_agent_sdk import tool, create_sdk_mcp_server

# TODO: export OPENWEATHER_API_KEY="your-key"  (get at openweathermap.org/api)
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")

@tool("get_weather", "Get current weather for a city.", {"city": str, "unit": str})
async def get_weather(args):
    city = args["city"]
    unit = args.get("unit", "metric")
    if not city or len(city) > 100:
        return {"content": [{"type": "text", "text": "Error: invalid city name"}]}
    if unit not in ("metric", "imperial"):
        return {"content": [{"type": "text", "text": "Error: unit must be metric or imperial"}]}
    # TODO: uncomment after setting API_KEY
    # resp = requests.get(
    #     "https://api.openweathermap.org/data/2.5/weather",
    #     params={"q": city, "appid": API_KEY, "units": unit},
    #     timeout=5
    # )
    # data = resp.json()
    # return {"content": [{"type": "text", "text": f"{data['weather'][0]['description']}, {data['main']['temp']}°"}]}
    return {"content": [{"type": "text", "text": "TODO: not yet implemented"}]}

server = create_sdk_mcp_server("weather-mcp", tools=[get_weather])
```

TODOs:
```
[ ] 1. pip install requests
[ ] 2. export OPENWEATHER_API_KEY="your-key"
[ ] 3. Uncomment the TODO block in get_weather()
[ ] 4. python weather-mcp.py  # verify no errors
```

### Bad Example

User: "Check today's weather in Taipei."

Claude's response:

> I can't access real-time weather data. Here's a function:

```python
import requests
def get_weather(city):
    return requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=abc123key").json()
```

> Why this is bad: Hardcodes the API key (`appid=abc123key`). Returns a raw Python function, not a runnable MCP server. No input validation. No TODO checklist. No connection snippet. User has no clear next step to connect this to Claude.

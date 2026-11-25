---
name: azure-functions-agents
description: >
  Build, extend, and troubleshoot event-driven AI agents on Azure Functions using the
  azure-functions-agents package. Works for both scaffolding new apps and modifying existing
  ones. Helps create agent files (.agent.md), configure triggers (timer, HTTP, queue, blob,
  Event Hub, Service Bus, Cosmos DB, connectors, etc.), set up connectors (Office 365, Teams,
  etc.), configure ACA Dynamic Sessions for code execution, add MCP servers and custom tools,
  run locally with Azurite, deploy to Azure with azd, and diagnose issues using App Insights
  and logs. USE THIS SKILL when the user wants to: build an event-driven agent, create a
  scheduled/triggered agent, build an agent on Azure Functions, use azure-functions-agents,
  create a timer/queue/blob agent, connect an agent to Office 365 or Teams, deploy an agent
  to Azure, set up connectors for an agent, add code execution to an agent, scaffold a new
  agent app, fix a broken agent, debug agent deployment, or troubleshoot connector/session issues.
argument-hint: 'Describe the agent you want to build — what it does, how it should be triggered, and what tools/services it needs'
---

# Azure Functions Agents

Build event-driven AI agents on Azure Functions using the
[azurefunctions-agents-runtime](https://pypi.org/project/azurefunctions-agents-runtime/) package — a
markdown-first programming model powered by the GitHub Copilot SDK.

Source: [github.com/Azure/azure-functions-agent-runtime](https://github.com/Azure/azure-functions-agent-runtime)
(Note: the README in the repo may not yet reflect the latest changes.)

> **This is an experimental package.** APIs are under active development and subject to change.

## When to Use

- User wants to build an AI agent that runs on a schedule, responds to events, or exposes an API
- User wants an agent triggered by timer, HTTP, queue, blob, Event Hub, Service Bus, Cosmos DB, connectors, etc.
- User wants to connect an agent to Office 365, Teams, or other Azure API Connections
- User wants to deploy an agent to Azure Functions with `azd up`
- User has an existing azure-functions-agents app and wants to add agents, change triggers, add connectors, fix issues, or deploy

## Core Concepts

- **Markdown-first**: Agents are defined in `.agent.md` files (YAML frontmatter + markdown instructions)
- **`main.agent.md`**: Special file that creates HTTP chat UI, chat API, MCP server, and session persistence — no triggers
- **`<name>.agent.md`**: Each file creates one event-triggered Azure Function. The filename (minus `.agent.md`) becomes the function name
- **`function_app.py`**: Always just `from azure_functions_agents import create_function_app; app = create_function_app()`
- **Triggers**: Configured in YAML frontmatter. See [triggers reference](./references/triggers.md)
- **Tools**: Connectors, MCP servers, custom Python tools, and sandbox code execution
- **Deployment**: Bicep infrastructure + `azd up` for provisioning and deployment

## Assess the Situation

Before doing anything, figure out where the user is. Check the workspace for existing files.

### Existing app

Look for these markers:
- `function_app.py` with `create_function_app()` → this is already an azure-functions-agents app
- `*.agent.md` files → existing agents, read them to understand current setup
- `infra/main.bicep` → infrastructure already exists, check what's provisioned
- `azure.yaml` → azd is already configured
- `local.settings.json` or `local.settings.template.json` → check what env vars are configured
- `requirements.txt` → check package version
- `tools/` directory → existing custom tools
- `mcp.json` → existing MCP servers
- `.azure/` directory → previous deployments, check `.azure/*/config.json` for azd env state

**Read existing files before making changes.** Understand what the user has, then help them
with what they need — adding an agent, fixing an issue, adding a connector, deploying, etc.

### New app

If no azure-functions-agents project exists, help scaffold one (see Scaffolding below).

### Key questions

Whether new or existing, clarify what's needed:
- **What should the agent do?** (summarize news, monitor resources, process data, etc.)
- **How should it be triggered?** (schedule, HTTP request, queue message, blob upload, connector event, etc.)
- **What tools/services does it need?** (Office 365 email, Teams, code execution, web browsing, custom APIs, MCP servers)
- **Does it need a chat interface?** (if yes, include `main.agent.md`)

If the user has already described what the agent should do, don't re-ask — proceed with
scaffolding or implementation. Only ask about things you can't infer from their request.

**Infer capabilities from the description — don't ask the user to confirm each one.** For
example, if the user says "summarize my emails," that implies an Office 365 connector — just
include it. If the task involves data analysis, web scraping, or computation, include the
execution sandbox. Only include capabilities the agent actually needs; many agents need zero
connectors and no sandbox.

**Getting IDs from links.** When the agent needs specific resource identifiers (e.g., a Teams
team ID, channel ID, or chat ID), ask the user to copy the link from Teams (or the relevant
app) and paste it. Extract the IDs from the URL rather than asking the user to look up raw
GUIDs. For example, a Teams channel link looks like:
```
https://teams.microsoft.com/l/channel/19%3A...%40thread.tacv2/General?groupId=<team-id>&tenantId=<tenant-id>
```
From this, extract `groupId` as the team ID and URL-decode the channel path segment for the
channel ID. This is much easier for users than finding IDs manually.

## Scaffolding a New App

Skip this section if working with an existing app. Create the project structure.

For infrastructure, copy the Bicep templates from [assets/infra/](./assets/infra/) into the
project's `infra/` directory, then tailor `main.bicep` to the app's needs — add session pool
and connector modules only if the agent needs them, add app-specific params, and wire
everything into `appSettings`. **Produce a clean `main.bicep` with no commented-out blocks** —
only include modules the app actually uses. An agent may need zero connectors, one, or
several — the `office365-connection.bicep` template is just an example that can be adapted
for any managed API connector type (Teams, SharePoint, SQL, etc.). See
[infra and deployment reference](./references/infra-and-deployment.md) for guidance on
adapting the templates.

```
<project-root>/
├── azure.yaml
├── infra/
│   ├── abbreviations.json
│   ├── main.bicep
│   ├── main.parameters.json
│   └── app/
│       ├── api.bicep
│       ├── rbac.bicep
│       ├── session-pool.bicep          # if using code execution
│       ├── session-pool-rbac.bicep     # if using code execution
│       ├── office365-connection.bicep  # if using Office 365
│       └── connector-rbac.bicep        # if using connectors
└── src/
    ├── function_app.py
    ├── host.json
    ├── local.settings.template.json
    ├── requirements.txt
    ├── .funcignore
    ├── main.agent.md                   # optional: chat UI + HTTP API
    ├── <name>.agent.md                 # one per triggered agent
    ├── mcp.json                        # optional: MCP servers
    ├── skills/                         # optional: reusable prompt modules
    │   └── <skill-name>/SKILL.md
    └── tools/                          # optional: custom Python tools
        └── <tool_name>.py
```

#### Key files to create:

**`function_app.py`** — always the same:
```python
from azure_functions_agents import create_function_app

app = create_function_app()
```

**`host.json`**:
```json
{
  "version": "2.0",
  "extensions": {
    "http": { "routePrefix": "" }
  },
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  }
}
```

**`requirements.txt`**:
```
azurefunctions-agents-runtime
```

**`local.settings.template.json`** — template for users to copy to `local.settings.json`:
```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "PYTHON_ENABLE_INIT_INDEXING": "1",
    "GITHUB_TOKEN": ""
  }
}
```
Add additional env vars as needed (e.g., `ACA_SESSION_POOL_ENDPOINT`, `O365_CONNECTION_ID`, `TO_EMAIL`).

**`.funcignore`**:
```
.git*
.vscode
__azurite_db*__.json
__blobstorage__
__queuestorage__
local.settings.json
test
.venv
__pycache__
*.pyc
*.pyo
.python_packages
.env
```

## Creating and Editing Agent Files

Each `.agent.md` file defines one agent. Use YAML frontmatter for configuration and markdown body for instructions.

**Agent file format:**
```yaml
---
name: Agent Display Name
description: What this agent does.

# Trigger (required for all agents except main.agent.md)
trigger:
  type: timer_trigger
  schedule: "0 0 9 * * *"

# Optional: connector tools
tools_from_connections:
  - connection_id: $CONNECTION_ENV_VAR

# Optional: code execution sandbox
execution_sandbox:
  session_pool_management_endpoint: $ACA_SESSION_POOL_ENDPOINT

# Optional: structured JSON response (HTTP triggers only)
response_example: |
  { "key": "value" }

# Optional settings
logger: true               # default true — log agent responses
substitute_variables: true # default true — replace $VAR in body
---

Agent instructions in markdown. Use $ENV_VARS for dynamic values.
Tell the agent what to do step by step.
```

For trigger details, see [triggers reference](./references/triggers.md).

## Adding Capabilities

These can be added to new or existing apps at any time.

#### Connectors (Office 365, Teams, etc.)

See [connectors reference](./references/connectors.md) for creating and configuring connectors (V1 and V2).

#### Code Execution Sandbox (ACA Dynamic Sessions)

See [sessions reference](./references/sessions.md) for setting up session pools and RBAC.

#### MCP Servers

Create `src/mcp.json` for external MCP servers (HTTP remote only):
```json
{
  "servers": {
    "microsoft-learn": {
      "type": "http",
      "url": "https://learn.microsoft.com/api/mcp"
    }
  }
}
```

Each server entry supports:
- `type` — `"http"` (required)
- `url` — the MCP server endpoint URL
- `headers` — optional HTTP headers (e.g., for auth)
- `tools` — optional array of tool name patterns (default: `["*"]`, supports fnmatch)

#### Custom Python Tools

Drop `.py` files in `src/tools/`. Each file should export an async function with a Pydantic model for parameters:

```python
"""Tool description used by the agent to understand when to call this tool.

Additional details about what the tool does.
"""

from typing import Optional
from pydantic import BaseModel, Field

class MyToolParams(BaseModel):
    query: str = Field(description="What to search for")
    limit: int = Field(default=10, description="Max results")

async def my_tool(params: MyToolParams) -> str:
    """Execute the tool and return a string result."""
    # Implementation here
    return f"Found results for: {params.query}"
```

**Important**: Custom tools run inside the Azure Functions Python runtime (Flex Consumption). You can install Python packages via `requirements.txt`, but you cannot install system packages or binaries. For anything requiring system-level dependencies, use the code execution sandbox instead.

#### Skills

Create `src/skills/<name>/SKILL.md` for reusable prompt modules:
```markdown
---
name: my-skill
description: Reusable knowledge about specific domain
---

# My Skill

## Tools available
- List tools and how to use them

## Common patterns
- Document patterns the agent should follow
```

## Infrastructure

See [infra and deployment reference](./references/infra-and-deployment.md) for Bicep templates and `azd` configuration.
When modifying an existing app's infra, read the current `infra/main.bicep` first to understand what's already provisioned before adding modules.

## Running Locally

#### Prerequisites
- Python 3.12+
- [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local) (v4+)
- [Azurite](https://learn.microsoft.com/azure/storage/common/storage-use-azurite) (local storage emulator)
- GitHub Copilot CLI (recommended) or a GitHub PAT

#### Azure resources needed for local dev

If the agent uses `execution_sandbox` or `tools_from_connections`, those Azure resources must
exist before running locally — the sandbox and connectors talk to real Azure services even
during local development.

**Recommended approach: provision infrastructure first, then develop locally.**

```bash
cd <project-root>
azd init
azd env set GITHUB_TOKEN "<your-github-pat>"
# Set other required env vars
azd provision   # creates Azure resources WITHOUT deploying code
```

After provisioning, populate `local.settings.json` with the provisioned resource values.
See [infra and deployment reference](./references/infra-and-deployment.md#populating-localsettingsjson-from-provisioned-resources)
for commands to extract session pool endpoints, connection IDs, etc.

If the app uses connectors, they must also be **authenticated** before they'll work —
even locally. See [connectors reference](./references/connectors.md#authenticating-connectors)
for how to check status and get the auth link.

Alternatively, set up resources manually — see the
[sessions reference](./references/sessions.md) and
[connectors reference](./references/connectors.md) for CLI commands.

#### Steps

```bash
# Navigate to the src directory
cd <project>/src

# Create and activate virtual environment (ALWAYS use a venv)
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy template settings
cp local.settings.template.json local.settings.json
# Edit local.settings.json — set GITHUB_TOKEN and other required values

# Start Azurite in a separate terminal (required for MCP, timers, queues, etc.)
azurite --skipApiVersionCheck
# Or via Docker:
docker run -d --name azurite -p 10000:10000 -p 10001:10001 -p 10002:10002 \
  mcr.microsoft.com/azure-storage/azurite \
  azurite --skipApiVersionCheck --blobHost 0.0.0.0 --queueHost 0.0.0.0 --tableHost 0.0.0.0

# Start the function app
func start
```

**Endpoints when running:**
- Chat UI: `http://localhost:7071/` (if `main.agent.md` exists)
- Chat API: `POST http://localhost:7071/agent/chat`
- Streaming API: `POST http://localhost:7071/agent/chatstream`
- MCP server: `http://localhost:7071/runtime/webhooks/mcp`

#### Testing triggered agents locally

Timer and other non-HTTP triggered agents can be invoked manually via the admin endpoint:

```bash
curl -X POST http://localhost:7071/admin/functions/<function_name> \
  -H "Content-Type: application/json" \
  -d '{}'
```

The function name is the `.agent.md` filename with `.agent.md` replaced by `_agent`
(e.g., `daily_news.agent.md` → `daily_news_agent`). This works for any trigger type —
timer, queue, blob, etc. — and is the fastest way to iterate on agent behavior locally.

#### GitHub Authentication

The Copilot SDK needs a GitHub token. Options:

1. **Copilot CLI (recommended)**: Install [GitHub Copilot CLI](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line) and run `copilot auth login`. The SDK will use the token from the locally installed CLI automatically.

2. **GitHub PAT**: If Copilot CLI is not installed, the SDK downloads its own copy of the CLI, but it cannot use the locally installed CLI's auth. In this case, set `GITHUB_TOKEN` in `local.settings.json`:
   - Go to [github.com/settings/tokens](https://github.com/settings/tokens?type=beta)
   - Click **Generate new token** (fine-grained)
   - Name: `azure-functions-agent-runtime`
   - Under **Permissions**, add **Copilot requests** → **Read-only**
   - Click **Generate token** and copy the value

## Deploying to Azure

See [infra and deployment reference](./references/infra-and-deployment.md) for full deployment instructions.

If you already ran `azd provision` during local development, deploy code with:
```bash
azd deploy
```

Otherwise, do a full provision + deploy:
```bash
cd <project-root>
azd init
azd env set GITHUB_TOKEN "<your-github-pat>"
# Set other required env vars (TO_EMAIL, COPILOT_MODEL, etc.)
azd up
```

> **A GitHub PAT is always required when deployed to Azure** — there is no alternative auth mechanism for cloud deployments. Provide instructions on creating one (see GitHub Authentication above).

## Post-Deployment

- **Connector auth**: If using connectors (Office 365, Teams, etc.), the API Connection is created but not authenticated. Go to Azure Portal → Resource Group → API Connection → Edit API connection → Authorize → Save.
- **Test timer triggers**: Use curl to manually trigger:
  ```bash
  # Get the master key
  az functionapp keys list -g <rg> -n <func-app> --query "masterKey" -o tsv
  
  # Trigger the function
  curl -X POST "https://<func-app>.azurewebsites.net/admin/functions/<agent_name>_agent" \
    -H "x-functions-key: <master-key>" \
    -H "Content-Type: application/json" \
    -d '{}'
  ```

## Be Hands-On — Do Things for the User

**Always offer to execute next steps, don't just list instructions.** After scaffolding the
project, don't dump a list of CLI commands and leave. Instead:

- **Run commands directly** when possible — `azd init`, `azd provision`, `azd deploy`,
  `pip install`, `func start`, creating venvs, starting Azurite, etc.
- **Only pause for user input** when you genuinely need it — a GitHub PAT, a choice the user
  must make, or confirmation before a destructive/irreversible action.
- **For portal-only steps** (like connector OAuth authorization), generate the portal URL and
  open it for the user rather than describing the steps.
- **After deployment**, offer to run post-deployment checks — verify connector auth status,
  trigger a test invocation, tail the logs.

The goal is to get the user from idea to running agent with as few manual steps as possible.
Tell the user what you're about to do and why, then do it.

## Environment Variable Substitution

Agent files support `$VAR` and `%VAR%` syntax:
- **Frontmatter**: Full-string replacement in `trigger.*` (except `type`), `tools_from_connections[].connection_id`, and `execution_sandbox.session_pool_management_endpoint`
- **Markdown body**: Inline replacement throughout the instructions
- Variables inside fenced code blocks are NOT substituted
- Unset variables are left as-is
- Disable with `substitute_variables: false` in frontmatter

## Trigger Type Resolution

| Pattern | Mechanism | Examples |
|---|---|---|
| `http_trigger` | `app.route(...)` with structured JSON | HTTP REST API |
| No dots | `app.<type>(...)` | `timer_trigger`, `queue_trigger` |

> Connector triggers (dot notation like `teams.new_channel_message_trigger`) are no longer
> supported in the package. Connector **tools** still work — use a standard trigger (timer,
> HTTP, etc.) and call connector actions as tools from the agent.

## Common Patterns

### Timer agent that sends email
```yaml
---
name: Daily Report
description: Sends a daily report via email.
trigger:
  type: timer_trigger
  schedule: "0 0 9 * * *"
execution_sandbox:
  session_pool_management_endpoint: $ACA_SESSION_POOL_ENDPOINT
tools_from_connections:
  - connection_id: $O365_CONNECTION_ID
---

You are a reporting assistant. When triggered:
1. Gather data (use execute_python for web requests, data processing)
2. Format into an HTML email
3. Send to $TO_EMAIL with subject "Daily Report - <today's date>"
```

### HTTP agent returning structured JSON
```yaml
---
name: Data Summarizer
description: Returns a structured summary from input data.
trigger:
  type: http_trigger
  route: summarize
  methods: ["POST"]
  auth_level: FUNCTION
response_example: |
  {
    "summary": "Brief text",
    "count": 42,
    "categories": ["a", "b"]
  }
---

Analyze the input and return a structured summary matching the response format.
```

### Chat assistant with code execution
```yaml
---
name: Code Assistant
description: A helpful assistant that can run Python code.
execution_sandbox:
  session_pool_management_endpoint: $ACA_SESSION_POOL_ENDPOINT
---

You are a helpful assistant. You can run Python code using the execute_python tool.
If you need up-to-date information, use execute_python to fetch it from the web.
```

## Troubleshooting and Debugging

Things will likely not work on the first try. This is normal — agent apps have many moving
parts (triggers, connectors, RBAC, env vars, SDK auth). **Be proactive about diagnosing
issues rather than guessing.**

See [troubleshooting reference](./references/troubleshooting.md) for detailed guidance.

### Key principles

1. **Check the logs first.** The terminal output from `func start` (local) or Application
   Insights (deployed) will almost always tell you what went wrong. Read the actual error
   message — don't assume.

2. **The framework fails open.** Missing env vars, missing agent files, and unresolvable
   connectors produce warnings but don't crash the app. If a feature isn't working, it may
   have been silently skipped. Look for `WARNING` and `ERROR` lines in logs.

3. **Work incrementally.** Get the basic agent running first (no connectors, no sandbox),
   then add capabilities one at a time. Test after each addition.

4. **Read existing files before changing them.** Especially `infra/main.bicep`,
   `local.settings.json`, and any existing `.agent.md` files. Don't duplicate or conflict
   with what's already there.

5. **When deployed, use Application Insights.** Go to Azure Portal → the App Insights
   resource in the app's resource group → Logs (or Transaction search). Look for exceptions
   and failed requests. The function name in logs corresponds to the `.agent.md` filename.

### Quick diagnostics

| Symptom | Likely cause | Check |
|---|---|---|
| Agent not registered | Missing/invalid `trigger` section | Look for "Skipping" warnings at startup |
| Agent runs but tools don't work | Missing env var, RBAC, or unauthenticated connector | Check tool error in agent response logs |
| `execute_python` not available | Missing `execution_sandbox` config or unresolved endpoint | Look for "missing session_pool_management_endpoint" warning |
| Connector tools missing | `connection_id` env var not set or connection doesn't exist | Check env vars and connection resource |
| 401/403 from connector | RBAC not assigned or connector not authenticated | Check role assignments and authorize in portal |
| No response from agent | GitHub token missing or expired | Check `GITHUB_TOKEN` in settings / env |
| Timer doesn't fire | Azurite not running (local) or schedule misconfigured | Start Azurite; verify NCRONTAB format |
| App starts but no endpoints | No `main.agent.md` file | Create one for chat UI/API/MCP |

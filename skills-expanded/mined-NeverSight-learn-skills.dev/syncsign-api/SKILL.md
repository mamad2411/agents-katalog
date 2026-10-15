---
name: syncsign-api
description: SyncSign Web API skill for user info, hub or device inventory, display or node details, and render operations using the public SyncSign API key routes.
version: 1.0.0
tools: [ "run_shell_command" ]
---

# SyncSign API Skill

Use this skill whenever the user is asking about SyncSign account info, Hubs, Displays, nodes, render jobs, or screen rendering through the public SyncSign Web API.

## Non-Negotiable Agent Rules

1. Use only the atomic scripts in `scripts/` for business actions.
2. Never read `.env`.
3. Never inspect `Env:` or shell environment variables for SyncSign credentials.
4. Never search the workspace, plugin folders, memory files, or history for API keys.
5. Never attempt login, password exchange, token recovery, or credential guessing.
6. If any SyncSign script exits with code `2` or stderr contains `SYNCSIGN_API_KEY_MISSING`, stop immediately.
7. After `SYNCSIGN_API_KEY_MISSING`, do not run any more diagnostic commands. Do not inspect `.env`. Do not continue exploring. Respond with the fixed setup message and end the turn.

Forbidden examples after `SYNCSIGN_API_KEY_MISSING`:
- `Get-Content .env`
- `dir .env`
- `Get-ChildItem Env:`
- `Get-ChildItem -Recurse -Filter .env`
- searching for `SYNCSIGN_API_KEY`
- reading `plugins/` to hunt for credentials

## First-Time Setup

Do not proactively read or inspect the `.env` file. Credentials are checked automatically when the atomic scripts run. If any SyncSign script exits with code `2` and stderr contains `SYNCSIGN_API_KEY_MISSING`, output the following message verbatim, then stop and wait for the user to confirm setup is complete before taking any further action.

### API Key Missing - Fixed Response

---

SyncSign API key is not configured.
Open the SyncSign client and go to Settings.
Copy your API Key and add it to the `.env` file in the current Skill runtime root:

```env
SYNCSIGN_API_KEY=your_api_key_here
SYNCSIGN_API_BASE_URL=https://api.sync-sign.com/v2
```

Save the file and let me know when it is ready.

---

Never ask the user to send secrets in chat. Never guess credentials.

## Before Every Shell Command

Before running any script, always output one short sentence in plain language explaining what you are about to do and why. Keep it under 15 words.

Examples:
- Checking your saved SyncSign account info.
- Listing hubs under your API key.
- Rendering the requested layout to the selected display.

## Command Base Path

Run all commands from the runtime root shown below, not from a nested folder. Use the path variant that exists in the current install:

- Source repo or `npx skills add`: `python scripts/syncsign_list_nodes.py`
- Claude marketplace package: `python scripts/syncsign_list_nodes.py`

## Runtime Layout

Source repo and `npx skills add` layout:

```text
runtime-root/
|- SKILL.md
|- README.md
|- requirements.txt
|- scripts/
|  |- build_claude_plugin.py
|  \- syncsign_*.py
|- common/
|  |- syncsign_auth.py
|  \- syncsign_client.py
|- .claude-plugin/
|  |- marketplace.json
|  \- syncsign-swagger.json
\- plugins/
```

Claude marketplace package layout:

```text
runtime-root/
|- .claude-plugin/
|  \- plugin.json
|- requirements.txt
|- scripts/
|- common/
|- skills/
|  \- syncsign-api/
|     \- SKILL.md
\- syncsign-swagger.json
```

## Output Contract

- `stdout`: JSON data on success
- `stderr`: error messages only
- `exit code`: `0` success, `1` failure, `2` missing API key

## Core Workflow

1. Prefer the existing atomic scripts in `scripts/`. Do not replace them with ad hoc `curl` or one-off Python snippets unless you are patching the project itself.
2. Resolve identifiers before detail calls:
   - If `sn` is unknown, start with `syncsign_list_devices.py`
   - If `node_id` is unknown for a hub, start with `syncsign_list_device_nodes.py`
   - If `node_id` is unknown globally, start with `syncsign_list_nodes.py`
   - If `render_id` is unknown, only fetch it from the response of a prior render call
3. Treat render operations as side-effecting:
   - Make sure the target node or nodes are unambiguous
   - Use the user's requested layout exactly
   - Prefer `--body-file` for larger JSON payloads
   - After a render request, use `syncsign_get_render.py` when the user asks for final execution status or when you need to confirm delivery
4. The public routes in this skill authenticate only with the SyncSign API key saved in `.env`.

## Scripts

### User
- `python scripts/syncsign_get_user_info.py`

### Hubs / Devices
- `python scripts/syncsign_list_devices.py`
- `python scripts/syncsign_get_device_detail.py --sn <SN>`

### Displays / Nodes
- `python scripts/syncsign_list_device_nodes.py --sn <SN>`
- `python scripts/syncsign_get_device_node.py --sn <SN> --node_id <NODE_ID>`
- `python scripts/syncsign_list_nodes.py`
- `python scripts/syncsign_get_node.py --node_id <NODE_ID>`

### Rendering
- `python scripts/syncsign_post_node_render.py --node_id <NODE_ID> --body-file <PATH>`
- `python scripts/syncsign_post_nodes_render.py --body-file <PATH>`
- `python scripts/syncsign_get_render.py --render_id <RENDER_ID>`

## Public API Coverage

The bundled `syncsign-swagger.json` mirrors the published SyncSign Swagger document at `https://dev.sync-sign.com/webapi/swagger.json?v=2.0.0`.

Covered routes:
- `GET /key/{api_key}`
- `GET /key/{api_key}/devices`
- `GET /key/{api_key}/devices/{sn}`
- `GET /key/{api_key}/devices/{sn}/nodes`
- `GET /key/{api_key}/devices/{sn}/nodes/{node_id}`
- `GET /key/{api_key}/nodes`
- `GET /key/{api_key}/nodes/{node_id}`
- `POST /key/{api_key}/nodes/{node_id}/renders`
- `POST /key/{api_key}/renders`
- `GET /key/{api_key}/renders/{render_id}`

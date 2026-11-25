---
name: create-devin-global-mcp
description: Create a new MCP server and register it in the Devin global mcp_config.json
argument-hint: "[scope]"
allowed-tools:
  - exec
  - read
  - write
  - edit
  - skill
  - ask_user_question
  - todo_write
  - mcp_list_servers
  - mcp_call_tool
related:
  - follow-create-mcp
  - update-devin
  - deep-review-codebase
  - deep-validate
  - ship
---

## Goal

Create a new MCP server in Rust or TypeScript, then register it in `%APPDATA%\devin\mcp_config.json` so Devin can use it

## Scope

Use when creating a new MCP server that should be visible to Devin through the global config right away

- Run `/follow-create-mcp` to create the server
- Run `/update-devin-global-mcp` to register it in the global config
- Test the server with `mcp_list_servers` and `mcp_call_tool`
- Do not modify the project `mcp_config.json` — use `/update-devin-project-mcp` for project scope

## Execute

### 1. Review And Decide

> Goal: Check the tech stack and settle the scope

1. Run `/deep-review-codebase` to inspect the current tech stack
2. Run `/deep-review-codebase` to review dependencies
3. Record the server name, transport, and the tools/resources you want

### 2. Create MCP Server

> Goal: Create the server for the chosen stack

1. Run `/follow-create-mcp` with the defined scope
2. After creating it, record the server's path, command, and args
3. Run `/deep-validate` as a first pass on the server project

### 3. Register In Devin Global Config

> Goal: Register it in `%APPDATA%\devin\mcp_config.json`

1. Run `/update-devin-global-mcp` with action `add`
2. Specify `command`, `args`, and `env` completely
3. Verify the file has the root key `mcpServers` and a correct server entry
4. Back up the config before editing

### 4. Test And Verify

> Goal: Confirm the server works with Devin

1. Run `mcp_list_servers` to check that the server appears
2. Use `mcp_call_tool` against the server to list tools or run a health check
3. If the tools don't load → `/resolve-errors` and fix them

### 5. Ship

> Goal: Deliver

1. Run `/deep-validate` on both the project and the skill repo
2. Run `/ship` for the server project
3. Report the server name, command, and registration status

## Rules

### 1. Scope

- For the Devin global MCP config only
- Do not edit the project `mcp_config.json` directly
- For project-level registration, hand off to `/update-devin-project-mcp`

### 2. Safety

- Back up `%APPDATA%\devin\mcp_config.json` before editing
- Do not expose secrets in the JSON
- Use `/follow-secret-manager` for credentials

### 3. Verification

- After registering, test the server with `mcp_list_servers` and `mcp_call_tool`
- If the tests don't pass, do not report the work as complete

## Expected Outcome

- The MCP server is created in Rust or TypeScript
- The server is registered in `%APPDATA%\devin\mcp_config.json`
- `mcp_list_servers` shows the server and `mcp_call_tool` can list its tools
- A backup of the global mcp config exists
- Passes `/deep-validate` and `/ship`

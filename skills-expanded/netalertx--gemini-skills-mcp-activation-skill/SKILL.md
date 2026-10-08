---
name: mcp-activation
description: Enables live interaction with the NetAlertX runtime. This skill configures the Model Context Protocol (MCP) connection, granting full API access for debugging, troubleshooting, and real-time operations including database queries, network scans, and device management.
---

# MCP Activation Skill

This skill configures the NetAlertX development environment to expose the Model Context Protocol (MCP) server to AI agents.

## Why use this?

By default, agents only have access to the static codebase (files). To perform dynamic actions—such as:
- **Querying the database** (e.g., getting device lists, events)
- **Triggering actions** (e.g., network scans, Wake-on-LAN)
- **Validating runtime state** (e.g., checking if a fix actually works)

...you need access to the **MCP Server** running inside the container. This skill sets up the necessary authentication tokens and connection configs to bridge your agent to that live server.

## Prerequisites

1.  **Devcontainer:** You must be connected to the NetAlertX devcontainer.
2.  **Server Running:** The backend server must be running (to generate `app.conf` with the API token).

## Activation Steps

1.  **Activate Devcontainer Skill:**
    If you are not already inside the container, activate the management skill:
    ```text
    activate_skill("devcontainer-management")
    ```

2.  **Generate Configurations:**
    Run the configuration generation script *inside* the container. This script extracts the API Token and creates the necessary settings files (`.gemini/settings.json` and `.vscode/mcp.json`).

    ```bash
    # Run inside the container
    /workspaces/NetAlertX/.devcontainer/scripts/generate-configs.sh
    ```

3.  **Apply Changes:**

    *   **For Gemini CLI:**
        The agent session must be **restarted** to load the new `.gemini/settings.json`.
        > "I have generated the MCP configuration. Please **restart this session** to activate the `netalertx-devcontainer` tools."

    *   **For VS Code (GitHub Copilot / Cline):**
        The VS Code window must be **reloaded** to pick up the new `.vscode/mcp.json`.
        > "I have generated the MCP configuration. Please run **'Developer: Reload Window'** in VS Code to activate the MCP server."

## Verification

After restarting, you should see new tools available (e.g., `netalertx-devcontainer__get_devices`).

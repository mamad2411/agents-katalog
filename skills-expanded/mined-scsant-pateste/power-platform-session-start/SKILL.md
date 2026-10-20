---
name: power-platform-session-start
description: Starts a safe enterprise Power Platform agent session by selecting the right workflow profile, confirming environment posture, and routing to the relevant plugin.
allowed-tools: Bash, Read, AskUserQuestion
---

# Power Platform Session Start

Use this at the start of team Power Platform work.

## Workflow

1. Read `${PLUGIN_ROOT}/references/profile-matrix.md`.
2. Classify the request into one profile:
   - `maker-canvas` for Canvas Apps, SharePoint-backed apps, maker UI, or simple flows.
   - `pro-dev` for Code Apps, Model Apps, Power Pages, generative pages, or React work.
   - `admin-alm` for solution movement, pipelines, export/import, or deployment diagnostics.
   - `mcp-builder` for MCP Apps widgets and tool UI.
3. Run `power-platform-prereq-check` when the request will touch local tools,
   MCP, live environments, or deployment.
4. Confirm the target is development or sandbox before any live write. If the
   user names production, ask for explicit confirmation of the action and target.
5. Route to the owning plugin rather than implementing duplicate behavior:
   - Canvas App authoring: `canvas-apps`.
   - Power Automate flows: `power-automate`.
   - Power Pages: `power-pages`.
   - Code Apps: `code-apps-preview`.
   - Model-driven apps and generative pages: `model-apps`.
   - MCP widgets: `mcp-apps`.

## Output

Return:

- selected profile
- owning plugin or skill
- prerequisite status
- environment safety posture
- next concrete action

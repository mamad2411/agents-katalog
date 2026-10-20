---
name: pac-workflow
description: Guides safe PAC CLI workflows for Power Platform environments, solutions, connections, export/import, deployment, and diagnostics.
allowed-tools: Bash, Read, AskUserQuestion
---

# PAC Workflow

Use this when a user asks for PAC CLI help or wants an agent to run Power
Platform command-line operations.

## Guardrails

- Run `power-platform-prereq-check` first for live operations.
- Prefer placeholders in docs and examples: `<envUrl>`, `<solutionName>`,
  `<publisherPrefix>`, `<connectionName>`.
- Do not commit raw command output that includes tenant ids, environment URLs,
  user names, subscription ids, or organization ids.
- Default to dry-run, list, validate, or inspect commands before commands that
  create, import, publish, delete, or overwrite.
- For production targets, pause for explicit confirmation naming the target and
  action.

## Common Routes

- Environment identity and auth: inspect `pac auth list`, then use the active
  profile or ask the user to create/select one.
- Solution movement: prefer solution-specific export/import commands and keep
  source and target environments distinct in the summary.
- Canvas Apps: use the `canvas-apps` plugin and Canvas Authoring MCP for app YAML
  sync and compile. Do not edit `_EditorState.pa.yaml`.
- Code Apps: use `code-apps-preview` skills for `pa app push` and connector
  setup.
- Model Apps and generative pages: use `model-apps` skills and scripts.
- Power Pages: use `power-pages` skills for site creation, deployment, ALM, and
  diagnostics.

## Response Shape

Give the user:

- intended PAC operation
- environment posture
- exact commands when safe
- risks or required confirmation
- verification command after the operation

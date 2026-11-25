---
name: gatherthread-config
description: Design GatherThread Agent Teams and browser preferences as versioned, importable JSON configuration files.
---

# GatherThread configuration

Use `collaboration_get_configuration_schema` to read the `agent-team` or `preferences` format when available. Design a small workflow with clear roles, entry node and handoff connections. Leave `target: null` for the user to choose real Agents. Never invent device/runtime IDs or copy authorization, enabled state, test receipts, saved revisions or credentials into a configuration.

Return a fenced `json` block with `version: 1` and the correct `kind`. Validate it with `collaboration_validate_configuration` if available. Otherwise follow the schema/example from the web configuration entry point or the repository documentation. State only checks actually performed.

The user previews/imports the JSON in GatherThread, then selects Agents, saves, tests and enables the Team. Preferences are reviewed and saved in Settings. Drafting must not run Agents, grant sharing permissions, install Hooks, change server settings or enable automatic uploads.

Reference: [configuration guide](https://github.com/TH060419/gatherthread/blob/main/docs/CONFIGURATION.md).

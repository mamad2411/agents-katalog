---
name: connector-bridge
description: Resolves a folder's declared .aai/connectors.md needs against whatever the current harness actually offers (MCP tools, CLIs, or nothing), caching successful matches in .aai/memory/; use for "wire up this connector", "resolve connectors.md", "what can reach X here".
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/connector-bridge/<file>`.
When installed standalone, resolve those to `<file>` in this directory.

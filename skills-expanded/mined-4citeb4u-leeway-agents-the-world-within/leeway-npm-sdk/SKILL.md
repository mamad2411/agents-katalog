---
name: "leeway-npm-sdk"
description: "Install, use, or extend the packaged @agentlee5/agent-skills npm SDK, CLI, extraction flow, and JavaScript imports. Use when Codex needs Leeway as a reusable package outside this repo, needs package paths, or must script the packaged MCP and standards surfaces."
---

# Leeway NPM SDK

Use this skill when consuming Leeway as a package rather than directly from the source repository.

## Quick start

- Read `references/npm-sdk.md` for the package purpose, install command, CLI commands, and JavaScript usage.
- Read `references/sdk-index.js` to see the primary exported SDK surface.
- Read `references/application-installer.js` when extracting the packaged full application bundle into a writable directory.
- Read `references/cli.js` for the root CLI commands and how the packaged MCP and standards commands are delegated.
- Pair this skill with `$leeway-mcp-server` when the package is being used to launch the MCP server.

## Reference map

- `references/npm-sdk.md` -> package install and usage guide
- `references/sdk-index.js` -> top-level JavaScript exports
- `references/application-installer.js` -> full application extraction flow
- `references/cli.js` -> packaged CLI command behavior

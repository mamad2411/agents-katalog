---
name: chorono-setup
description: Install, start and troubleshoot the local Chorono editor, MCP connection and agent skills for Claude Code, Claude Desktop and Codex.
---

# Chorono setup

Use this workflow when the user asks to install/start Chorono or its editor connection is unavailable. Reuse an already connected editor when appropriate. Installing a skill does not by itself start a process or register an MCP server in the current chat.

## Choose an executable

The CLI provides `setup`, `start`, `doctor`, `stop` and `skills` commands. Check Node.js 20+; a fresh editor download also needs Git. Report a missing system prerequisite instead of attempting an unrelated privileged OS installation.

- In a source checkout, run `npm ci` and `npm run cli:build` when dependencies/bundled skills are missing, then use `npm run chorono -- <command>`.
- When parsing JSON through npm scripts, use `npm run --silent chorono -- <command> --json` so npm's own banner does not precede the JSON result.
- If the CLI is installed, use `chorono <command>`.
- If the npm version is actually published, `npx --package @codie1982/chorono@VERSION chorono <command>` can run it without a global install. Before publication use an existing checkout or the local tarball; do not promise that an unpublished package can be downloaded.

## Set up, start and verify

1. Choose the user's animation project directory. `setup --project PATH` creates it if needed. With an existing editor, pass `--editor PATH`; otherwise the CLI discovers an ancestor checkout or downloads into the project's `.chorono/editor`. A fresh remote source must contain the MCP/CLI changes. Use `--repo URL --ref BRANCH_OR_TAG` for an explicitly chosen source; the CLI refuses old checkouts without MCP support.
2. Run `chorono setup --project PATH --json` (plus `--editor` / `--agent` when needed). It installs missing dependencies, builds missing outputs, creates private local bridge credentials, configures selected MCP clients and installs/updates unmodified Chorono skills. It never pulls/resets an existing checkout. Inspect `ok`, client statuses and skill conflicts before proceeding. Existing client entries are preserved; review `stale` or `unverified` entries using the generated snippets, without printing unrelated configuration or backups.
3. Run `chorono start --project PATH --background --open --json`. It reuses a matching running server, or starts the built editor on loopback. `--port NUMBER` selects another port; the project remembers its editor/port. A busy or mismatched service is never killed automatically. JSON results go to stdout; installation logs go to stderr. Readiness failure returns the actual server-log path.
4. Open the returned URL and use **MCP → Connect this editor**. If browser-control tools are available and the user's setup request authorizes this connection, the agent can operate that UI. Otherwise tell the user the exact control to click. Do not bypass the visible connection action with a direct pairing request. Reloading the page requires reconnecting.
5. Reload the model client's MCP connections or start a new agent session when configuration changed. `chorono doctor --project PATH --json` returns installation/build/client checks, server identity and connected editor count. A running HTTP server with zero editor sessions is not ready for scene commands; doctor exits nonzero until ready. It performs read-only checks and does not modify the scene.
6. Use actual MCP tools `list_sessions`, `get_capabilities`, and `get_scene`. Choose `sessionId` when several tabs are connected. If tools cannot be loaded in this chat, report the client reload/new-session step instead of claiming the agent is connected. Once connected, use `chorono` for scene creation, multiple animations, previews and saves.

For rebuilding, stop the running Next server first. `chorono stop --project PATH` stops only a matching background process created by this CLI. For a manually started process, use its original terminal. Then run `chorono setup --project PATH --rebuild`; add `--reinstall` only when refreshing dependencies is needed. One checkout has one managed server; stop it before switching ports/projects, or use another checkout. `--background` is appropriate for agent sessions; foreground `start` occupies the terminal until stopped.

## Scope and existing content

`--agent codex`, `--agent claude-code`, `--agent claude-desktop` or `all` select client settings; default `all` includes all three. Claude Code gets a project `.mcp.json`; Codex and Claude Desktop use user configuration. Files are backed up before additions, and existing Chorono entries are preserved. For only generated config snippets use `setup --no-clients`. Use `--no-skills` to skip filesystem skill installation.

Filesystem skills install for Codex (`.agents/skills`) and Claude Code (`.claude/skills`) in the project. Claude Desktop MCP support does not imply it loads those skill directories. For other Claude surfaces, verify the supported skill/plugin import method separately. Saved portable projects go to the chosen project's `projects/` directory, while the editor checkout and its runtime files remain separate.

For skill-only installation, use `chorono skills install`, `update`, `check`, or `list`. `--global` selects the user's home, `--agent codex|claude-code|all` selects agents, and repeated `--skill NAME` narrows the set. `--dry-run` writes nothing. `check` compares against this exact package bundle, not npm latest. `update` preserves modified or foreign copies; inspect before choosing `--force`, which backs up replaced directories under `.chorono/skill-backups/`.

Do not display `.chorono/mcp-token`, client-config backups or unrelated credentials. This local MCP workflow needs no model-provider API key. Report the editor URL, project path, readiness, and exact remaining client/browser step.

---
name: setup-agent-guild
description: Install, start and check Agent Guild for the person, then connect this agent to it over MCP. Use when the person asks to set up, install, start, repair or connect Agent Guild, or wants to run Claude Code, Codex CLI, Antigravity CLI, Grok Build, Docker Agent or shells side by side and pick them up from a phone, VS Code or any browser.
---

# Set up Agent Guild

Agent Guild is a free, open-source (AGPL-3.0) session manager. It runs coding
agents and shells in real terminals on the person's own Windows, macOS or
Linux computer and serves one local page, which opens in any browser, in VS
Code and in the Agent Guild apps. Sessions keep running when the page closes.

## Safety rules

- **Never print, paste, store or send the page link or the access token.**
  `agent-guild url` and `agent-guild --no-browser` print a link that ends in
  `#token=...`, and that token controls every session on the computer. Run
  plain `agent-guild` so the page opens in the person's browser, and do not
  read the token file in the data folder.
- Leave remote access (Tailscale, reverse proxies) off unless the person asks
  for it. It is set up in the page under **Settings → Remote access**.
- Install only the package `@oddessentials/agent-guild` from npm.
- Ask before stopping or restarting the manager: both end every session.

## 1. Check Node.js

```sh
node --version
```

Agent Guild needs Node.js 22 or newer. If it is missing or older, ask the
person to install the current LTS from https://nodejs.org (or with their
package manager), then continue.

## 2. Install

```sh
npm install -g @oddessentials/agent-guild
```

If npm reports a permissions error on macOS or Linux, do not use `sudo`
without asking. Suggest a user-owned npm prefix or a Node version manager
instead.

## 3. Start it

```sh
agent-guild
```

This starts the manager in the background and opens the page in the person's
browser. It prints only the address, never the token. On a computer with no
desktop, tell the person to run `agent-guild --no-browser` themselves and open
the link it prints; do not run that command yourself.

## 4. Verify

```sh
agent-guild status
agent-guild doctor
```

`status` shows the version and every session. `doctor` checks the whole
setup and says what to fix. The manager also answers, with no token,
`http://127.0.0.1:47821/api/v1/health`.

## 5. Connect this agent over MCP (optional)

`agent-guild mcp` lets an agent list the sessions, read their last replies
and terminals, start or stop sessions with the person's approval, and launch
fireworks over the Yard. Add it
to the agent the person is using:

| Agent | Command |
| --- | --- |
| Claude Code | `claude mcp add -s user agent-guild -- agent-guild mcp` |
| Codex CLI | `codex mcp add agent-guild -- agent-guild mcp` |
| Antigravity CLI | `agy mcp add agent-guild agent-guild mcp` |
| Gemini CLI | `gemini mcp add -s user agent-guild agent-guild mcp` |
| VS Code | `code --add-mcp '{"name":"agent-guild","type":"stdio","command":"agent-guild","args":["mcp"]}'` |

For one VS Code workspace, `.vscode/mcp.json`:

```json
{ "servers": { "agent-guild": { "type": "stdio", "command": "agent-guild", "args": ["mcp"] } } }
```

For Cursor, Windsurf and other editors that take an `mcpServers` config:

```json
{ "mcpServers": { "agent-guild": { "command": "agent-guild", "args": ["mcp"] } } }
```

Typing into sessions stays off unless the person asks for it; then add
`--allow-input` after `mcp`.

## 6. Hand over

Tell the person:

- the page is open in their browser; **New** on a tool's card starts a
  session, and each tool signs in inside its first session, as in any
  terminal;
- the coding tools install and update from their own cards;
- to open the same sessions on a phone, in VS Code or on another screen, see
  https://agentguild.oddessentials.ai/requirements/.

## Uninstall

Ask first, since it ends every session:

```sh
agent-guild stop
npm uninstall -g @oddessentials/agent-guild
```

The settings folder stays: `%APPDATA%\AgentGuild` on Windows,
`~/Library/Application Support/AgentGuild` on macOS, `~/.config/agent-guild`
on Linux.

More: https://github.com/oddessentials/agent-guild

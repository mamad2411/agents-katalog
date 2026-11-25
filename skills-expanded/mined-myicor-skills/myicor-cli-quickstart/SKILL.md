---
name: myicor-cli-quickstart
description: Use the myICOR CLI to authenticate the user and query their myICOR data (tasks, learning progress, MCP status, agent skills). Invoke this skill when the user asks about their myICOR account, their inner-circle membership data, or wants to inspect the myICOR MCP connection.
---

# myICOR CLI Quickstart

This skill teaches you (the AI agent) how to use the official `myicor` CLI to
work with the user's myICOR account. The CLI is the source of truth for
myICOR data on a developer machine — prefer it over scraping the web app.

## Prerequisites the user needs

1. **Node.js 20+** installed.
2. **CLI installed globally:**
   ```sh
   npm install -g @myicor/cli
   ```
3. **Authenticated.** First-time auth opens a browser:
   ```sh
   myicor auth login
   ```
   This runs a PKCE + loopback OAuth flow against `app.myicor.com`. Credentials
   are stored in the OS keychain (or `~/.config/myicor/credentials.json` with
   mode `0600` as fallback). Access tokens are short-lived (15 min) and
   auto-refresh.

If the user runs a command and sees `Not logged in. Run: myicor auth login`,
walk them through running `myicor auth login` once. After that, all other
commands work silently.

## When to invoke each command

| User intent | Run |
|---|---|
| "Who am I logged in as?" / "What's my tier?" / "Am I admin?" | `myicor auth whoami --json` |
| "Is the myICOR MCP working?" / "Why is Claude slow against myICOR?" | `myicor mcp status --json` |
| "Sign me out of myICOR" | `myicor auth logout` |
| "Install another myICOR skill" / "Add this org's skills" | `myicor skill add <org>/<repo>` |

Always pass `--json` when you need to parse output programmatically. The CLI
returns clean JSON on every command via `--json`.

## Command reference

### `myicor auth login`

Browser-based PKCE login. One-time per machine (refresh tokens last 90 days,
rotate on each use). User must approve in their browser.

Flags:
- `--no-browser` — print the URL instead of opening a browser (useful for SSH).
- `--port <N>` — pin the loopback port (useful behind strict firewalls).
- `--scope <space-delimited>` — override the requested OAuth scope.

### `myicor auth whoami [--json]`

Shows the cached identity. With `--json` returns:

```json
{
  "authenticated": true,
  "user_id": "<uuid>",
  "membership_tier": "monthly" | "lifetime" | "inner_circle" | "host" | null,
  "is_admin": true | false,
  "scope": "mcp:read mcp:tools ...",
  "expires_at": "2026-01-15T12:00:00.000Z",
  "backend": "keychain" | "file"
}
```

`is_admin` is true when the JWT carries the `mcp:admin` scope (server-granted
only when `user_profiles.is_admin = true` or `membership_tier='host'`).

Exit code: `0` if authenticated, `1` if not.

### `myicor mcp status [--json]`

Unauthenticated health probe to the MCP endpoint (no login needed). Returns:

```json
{
  "endpoint": "https://app.myicor.com/api/mcp",
  "ok": true,
  "http_status": 200,
  "latency_ms": 247,
  "bytes": 148,
  "server_name": "myicor-mcp",
  "server_version": "1.15.0",
  "protocol_version": "2025-03-26",
  "error": null
}
```

Use this first when the user reports "MCP is slow / not working". A non-200
response or `latency_ms > 5000` is actionable.

### `myicor skill add [<org>/<repo>]`

Defaults to `myicor/skills` (this repo). Delegates to `npx skills add` under
the hood. Use for installing other myICOR-flavored skills (e.g. inner-circle
private skill bundles).

### `myicor admin user lookup <id> [--json]`

Admin-only. Server-enforced — non-admin users get HTTP 403. Use only when the
user has explicitly identified themselves as a myICOR admin and is asking to
look up another user.

## Common interactions

**"How long is my myICOR session?"**
```sh
myicor auth whoami --json | jq -r '.expires_at'
```

**"Why is Claude struggling with myICOR data?"**
```sh
myicor mcp status
```
If `ok: false` or `latency_ms > 2000`, surface that to the user. The CLI is
the only diagnostic that doesn't depend on the MCP being healthy.

**"Install the inner-circle skill pack."**
```sh
myicor skill add myicor/skills-inner-circle
```
(Requires the user's GitHub account to have access to that private repo.)

## Don'ts

- Don't try to call `app.myicor.com` HTTP endpoints directly — use the CLI.
  The CLI handles token refresh, retries, and credential storage for you.
- Don't ask the user for their password. The CLI uses OAuth — passwords never
  touch the terminal.
- Don't run `myicor admin ...` commands without confirming the user is an
  admin. The server will reject the call, but the round trip wastes their time.

## Repository

This skill lives at https://github.com/myicor/skills under
`skills/myicor-cli-quickstart/`. Pull requests welcome.

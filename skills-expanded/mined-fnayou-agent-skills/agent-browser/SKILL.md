---
name: agent-browser
description: Drive a web browser through the agent-only MCP servers playwright, playwright-auth, and safari-mcp. Use when a task needs a browser (open, test, or screenshot a page, check layout at a viewport), when a site needs the user's login, for Safari compatibility checks, or to check or set up these servers.
---

# Agent Browser

Three MCP servers give agents a browser that is never the user's own. Pick
the narrowest one for the task, prove it is reachable, then work.

| Server | Browser | Use for |
| --- | --- | --- |
| `playwright` | Headless, in-memory profile, gone when the browser closes | The default: public pages, local dev servers, layout and viewport checks. Safe to run from many agents at once. |
| `playwright-auth` | Headed, persistent agent-only profile | Only sites that need the user's login. One agent at a time. |
| `safari-mcp` | Safari's built-in MCP server, in a window Safari marks as agent-controlled | Only Safari-specific compatibility checks. One session at a time. |

Both Playwright servers start through
[`scripts/agent-browser-mcp`](scripts/agent-browser-mcp), so the package pin
and browser binary live in one place.

## Preflight

1. Look for the chosen server's tools in this session. Clients name them
   differently: `mcp__playwright__browser_navigate`,
   `playwright/browser_navigate`, or tools reached through a code-mode or
   tool-search tool that searches by server name. Tools present means the
   server is connected; skip to the work.
2. When the tools are absent, or before the first `playwright-auth` use in a
   session, run [`scripts/check`](scripts/check). It is read-only and prints
   `OK`, `WARN`, or `FAIL` per fact and one `READY` line per server.
3. Report each `FAIL` and each `WARN` that blocks the chosen server, with the
   fix the line names. Preflight is done when the chosen server is `READY yes`
   and its tools are callable, or when the user has the blocker in hand.

A server added to a client's config reaches a session only after the client
restarts or reloads its MCP servers.

## Logged-in sites

The user owns the login. When `playwright-auth` opens on a login page, stop
and ask the user to sign in, including any 2FA, in the browser window, then
continue once they confirm. Credentials and codes stay out of the chat, since
anything the agent types is recorded in transcripts and logs.

- `scripts/check` reports `profile.lock` in use: another agent holds the
  profile. Wait or ask; a second browser on the same profile fails.
- Page snapshots and screenshots of a logged-in page carry the user's private
  data. Keep what reaches the reply to what the task needs.
- The agent acts as the user. Confirm with the user before every irreversible
  action: submit, pay, delete, send, publish, change settings.
- Session expired: ask the user to sign in again, the same way.
- The agent never types the password or the code, and never asks for them in chat. A passkey, CAPTCHA, or device-trust prompt is the user's too: stop and ask, never work around it.
- Only `playwright-auth` carries a login. `playwright` is isolated and in-memory, so a site that needs a login opens on its login page there.

## Safari

A session error that names "Allow remote automation" means the setting is
off: ask the user to tick Safari > Settings > Developer > "Allow remote
automation and external agents". Navigate before any tab tool; tab calls
issued before the first navigation can fail.

## Layout checks

Resize to each requested viewport, then measure before judging: compare
`document.documentElement.scrollWidth` with `innerWidth` for horizontal
overflow, and take a full-page screenshot. Report each viewport's size,
overflow, and visible defects, with the screenshot paths.

## Setup and changes

Read [setup](references/setup.md) when a server is missing from a client,
when changing the package pin, browser, or profile location, or before the
user's first `playwright-auth` login.

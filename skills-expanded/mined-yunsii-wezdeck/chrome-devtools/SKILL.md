---
name: chrome-devtools
description: >
  Drive the machine Chrome debug browser via OpenClaw-managed MCP
  (chrome-devtools). Use for page navigation, snapshots, screenshots,
  clicks, forms, console/network inspection — not for host shell risk.
---

# Chrome DevTools (Dex / OpenClaw core)

## What this is

Dex (Main) can control the **Windows host debug Chrome** through OpenClaw MCP:

| Piece | Where |
| --- | --- |
| CDP endpoint | `http://127.0.0.1:9222` (WezDeck helper auto-start) |
| MCP server name | `chrome-devtools` in local `~/.openclaw/openclaw.json` → `mcp.servers` |
| Package | globally-installed `chrome-devtools-mcp --browser-url=http://127.0.0.1:9222 --usageStatistics=false` (pinned; **not** `npx …@latest`) |

This is **not** the same MCP session as Grok/Claude CLI; all clients share the
**same Chrome process** on port 9222. Avoid concurrent multi-agent browser wars.

Workflow detail for launch / badge / inspect:
repo root [`docs/browser-debug.md`](../../../../docs/browser-debug.md).

## Backend gate

Only the default browser path when `WEZDECK_BROWSER_BACKEND=cdp` (after
`apply-browser-backend --set cdp`). When backend is `ego`, OpenClaw should
**not** have this MCP resident — use vendor `ego-browser` / platform
`browser-agent` instead. See repo [`docs/browser-debug.md`](../../../../docs/browser-debug.md#browser-backends-ego--cdp).

## When to use (Dex · Main)

| Trigger | Action |
| --- | --- |
| User: open/check URL, click, form, screenshot | MCP navigate + snapshot (not curl HTML) |
| **You** just changed UI (allowlisted repo) | Before 验收通过: open relevant URL/path, snapshot |
| “页面坏了 / 控制台报错 / 按钮点不了” | list pages / console / network as needed |

Coding agents on the host have their **own** browser/MCP/profile — this skill is
for **main** when main is looking at the page. No bridge required.

## When not to use

- Pure git / shell / ledger / worktree assess — do not open Chrome “just in case”.
- Destructive browser actions outside what the user asked (clear profile, mass
  delete, payment submit) without explicit confirmation.
- Host shell risk still goes through `claw-run` / `exec-risk` — browser MCP is
  separate.

## Operator setup (once per machine)

```bash
# CDP must answer first
curl -sS -m 3 http://127.0.0.1:9222/json/version

# Install once, pinned. Never drive this from `npx …@latest`: npx leaves
# npm-cli resident (~85Mi) per instance purely as a launcher.
npm i -g chrome-devtools-mcp@1.9.0

openclaw mcp add chrome-devtools \
  --command chrome-devtools-mcp \
  --arg --browser-url=http://127.0.0.1:9222 \
  --arg --usageStatistics=false \
  --timeout 90 \
  --connect-timeout 60

openclaw mcp probe chrome-devtools   # expect dozens of tools (count drifts by release)
openclaw mcp reload
# or: systemctl --user restart openclaw-gateway.service
```

A bare `--command` is enough — the gateway unit's pinned `Environment=PATH=`
already contains the fnm global bin dir. **Re-run `npm i -g` after any
`fnm default <version>` switch**: npm's global prefix is scoped to the default
node version, so the binary drops off `PATH` entirely.
`--usageStatistics=false` drops a ~135Mi `telemetry/watchdog` child process.
Net: 4 processes / ~357Mi → 1 process / 150Mi per instance — see repo
[`docs/guest-oom.md#standing-memory-consumers`](../../../../docs/guest-oom.md#standing-memory-consumers) "Standing memory
consumers".

⚠️ **That 150Mi is the idle floor, not a ceiling.** `chrome-devtools-mcp` grows
without bound while attached to a page: its network/console collectors have no
size cap and only trim on main-frame navigation, so an SPA or a tab left open
keeps feeding the Node heap. On the Claude Code side, instances reached
1.7–3.5 Gi and that path was moved off resident MCP entirely. OpenClaw keeps
resident MCP on purpose — one gateway-level instance instead of one per session,
observed peak 138 Mi, and the runtime does get released — but the growth
mechanism is the same one.

So if a gateway-owned instance is ever seen above ~1 Gi, or surviving many turns
without release, reclaim it with `openclaw mcp reload` (disposes the cached
runtime; the next turn rebuilds it). Do not reach for a rewrite. Inspect with
`pgrep -f chrome-devtools-mcp` — the `-f` matters, `comm` truncates to
`chrome-devtools`. Rationale and thresholds: repo `docs/guest-oom.md`.

Health:

```bash
openclaw mcp list
openclaw mcp status
```

If probe fails: start debug Chrome (helper auto-start / `Alt+b`), confirm
port, then `openclaw mcp reload`.

## Agent habits

1. Prefer MCP browser tools over `curl` HTML scraping when interaction matters.
2. Prefer **snapshot** before click/type so selectors stay grounded.
3. Report back in 简体中文: URL, what you saw, what you did, blockers.
4. If CDP is down, say so and how to fix (`docs/browser-debug.md`); do not invent success.
5. Do not put CDP secrets in git (loopback URL is fine in local config only).

## Tool names

Exact projected names depend on OpenClaw (often `chrome-devtools__…` or code-mode
`MCP.chromeDevtools.*`). Discover via the tool list for this session; common
capabilities include: list/navigate pages, snapshot, screenshot, click, fill,
console, network, performance.

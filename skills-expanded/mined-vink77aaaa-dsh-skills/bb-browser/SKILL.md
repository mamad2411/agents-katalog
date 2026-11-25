---
name: bb-browser
description: "Use when the task involves bb-browser, real browser login state reuse, authenticated fetch, site commands, Chrome CDP, browser traffic inspection, or MCP integration for Codex/Claude Code/Cursor 等。在需要通过 bb-browser 复用真实浏览器登录态执行 site 查询、带 Cookie 抓取、页面控制、抓包、或接入 MCP 时使用。"
---

# bb-browser

Use this skill when `bb-browser` is the right abstraction: real browser identity, `site` adapters, authenticated browser fetches, or MCP exposure for agent tools.

This skill is not for writing Playwright tests or developing new `site` adapters.

## When to use

Use this skill when the user wants any of the following:

- use `bb-browser`
- query a website through a `site` adapter
- inspect a page with the user's real browser login state
- run authenticated `fetch` or inspect browser `network` traffic
- connect `bb-browser --mcp` to Codex, Claude Code, Cursor, or similar agents

Do not use this skill for:

- Playwright test generation
- generic UI test automation
- building or debugging new `site` adapters

## Required preflight

Run these checks first:

```bash
command -v bb-browser
bb-browser --version
bb-browser daemon status --json
```

If `bb-browser` is missing, stop and tell the user to install it:

```bash
npm install -g bb-browser
```

## Default workflow

Always prefer this decision order:

1. Confirm the CLI is installed and runnable.
2. Check whether a `site` command already solves the task.
3. If no `site` command exists, use page commands such as `open`, `snapshot`, `click`, `fill`, `get`, `fetch`, or `network`.
4. If the user wants agent integration, provide or verify the MCP configuration with `bb-browser --mcp`.

## Site-first rule

For data retrieval tasks, prefer `site` over manual browser interaction.

Typical pattern:

```bash
bb-browser site list
bb-browser site search "github"
bb-browser site info "wikipedia/summary"
bb-browser site "wikipedia/summary" "Python (programming language)" --json
```

If a `site` adapter exists, use it unless the user explicitly needs low-level page interaction.

## Manual page workflow

When there is no suitable `site` adapter, use this loop:

```bash
bb-browser tab new "https://example.com" --json
bb-browser wait 1500 --tab <tab> --json
bb-browser snapshot -i --tab <tab>
bb-browser get title --tab <tab>
```

Then continue with the latest snapshot refs:

```bash
bb-browser click @0 --tab <tab>
bb-browser fill @3 "hello" --tab <tab>
bb-browser fetch "https://example.com/api" --json
bb-browser network requests --with-body --json
```

Rules:

- `<tab>` means the short tab id returned in the `tab` field from `tab new`
- `tab new` can return before the page fully loads, so add a short `wait` before `get` or `snapshot` when you need stable page state
- On a clean managed browser state, `open` may need a page target first. If you hit `No page target found`, bootstrap with `tab new`, then work against that tab id.
- Snapshot before relying on refs like `@3`
- Snapshot again after navigation, modal changes, or major DOM updates
- Prefer `get`, `fetch`, and `network` over brittle click-heavy flows when they solve the task faster

For more examples, read [references/cli-workflows.md](./references/cli-workflows.md).

## MCP integration

When the user wants to expose `bb-browser` to an agent runtime, use:

```json
{
  "mcpServers": {
    "bb-browser": {
      "command": "npx",
      "args": ["-y", "bb-browser", "--mcp"]
    }
  }
}
```

Before suggesting MCP setup, verify the local CLI works first.

For platform-specific examples, read [references/mcp-integration.md](./references/mcp-integration.md).

## Safety guardrails

`bb-browser` can act with the user's real browser identity. Treat it as a high-trust tool.

Default behavior:

- proceed on read-only lookups
- warn clearly before write actions or sensitive flows
- require explicit user authorization for:
  - posting or publishing
  - messaging
  - purchases or bookings
  - account settings changes
  - admin or moderator actions

Do not downplay this risk. The website may treat these actions exactly as if the user performed them manually.

## Troubleshooting

If the workflow fails, check:

- daemon not running
- browser/CDP not reachable
- no Chromium browser found
- stale snapshot refs

Use [references/troubleshooting.md](./references/troubleshooting.md) for the exact playbook.

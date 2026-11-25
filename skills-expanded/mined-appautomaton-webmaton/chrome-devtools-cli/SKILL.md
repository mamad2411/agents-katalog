---
name: chrome-devtools-cli
description: "Use when a task needs Chrome DevTools from the shell: automate a live Chrome browser with `chrome-devtools`, inspect accessibility snapshots and UIDs, click/fill/navigate pages, evaluate JavaScript, inspect console and network activity, take screenshots, run Lighthouse, capture performance traces, or connect to an existing debuggable Chrome. This is CLI mode, not MCP client setup."
---

# chrome-devtools-cli

The package is `chrome-devtools-mcp`, but the action CLI is `chrome-devtools`. Use `chrome-devtools <tool> ...` for this skill. Do not use `npx chrome-devtools-mcp@latest` unless you are configuring an MCP server outside this skill.

## Core Workflow

```bash
chrome-devtools new_page "https://example.com"
chrome-devtools list_pages
chrome-devtools take_snapshot 0
chrome-devtools click 0 "1_3"
chrome-devtools fill 0 "1_5" "search text"
chrome-devtools press_key 0 "Enter"
```

Two identifiers drive everything. The **page id** is the first positional argument of nearly every command — read it from `list_pages`. The **element uid** comes from `take_snapshot`, which returns accessibility-tree entries such as `1_3`.

Always act on uids from the latest snapshot. Re-snapshot after navigation, reloads, or major DOM updates.

## Operating Rules

- Run tools directly; the background daemon starts implicitly on first real action and preserves browser state.
- Do not run `start`, `status`, or `stop` before every action. Use them only for setup, custom launch flags, or troubleshooting.
- Pass the page id as the first positional argument. `list_pages` and `new_page` are the exceptions that take none, and `evaluate_script` takes `--pageId` as a flag instead.
- Use `chrome-devtools <command> --help` for exact syntax; this file tracks 1.8.0 and the command surface moves between minor releases. Output defaults to Markdown; add `--output-format=json` when structured output is useful.
- This CLI drives its own `chrome-devtools-mcp` daemon. If the surrounding agent already has an MCP client connected to that same server, prefer one path or the other rather than mixing them in one session.
- Prefer snapshots over screenshots for deciding what to click or fill. Use screenshots for visual proof, layout inspection, or reports.
- Use `evaluate_script`, console, and network commands when debugging runtime behavior; use Lighthouse and performance tracing for page-quality/performance work.

## Common Tasks

```bash
chrome-devtools list_pages
chrome-devtools navigate_page 0 --url "https://example.com"
chrome-devtools navigate_page 0 --type "reload" --ignoreCache
chrome-devtools evaluate_script "() => document.title" --pageId 0
chrome-devtools list_console_messages 0 --types error
chrome-devtools list_network_requests 0 --pageSize 50
chrome-devtools take_screenshot 0 --filePath page.png
chrome-devtools lighthouse_audit 0 --mode "navigation"
chrome-devtools performance_start_trace 0 --reload --filePath trace.json.gz
chrome-devtools performance_stop_trace 0
```

For a broader command map, read `references/cli-reference.md`.

## Setup

If this is the first time using the CLI or `chrome-devtools` is missing, read `references/installation.md`. Installation is a one-time prerequisite, not part of the regular workflow.

## References

- `references/cli-reference.md` — command groups, daemon behavior, output modes, and troubleshooting commands
- `references/installation.md` — global install and PATH troubleshooting

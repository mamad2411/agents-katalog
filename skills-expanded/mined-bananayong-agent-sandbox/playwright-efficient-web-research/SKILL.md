---
name: playwright-efficient-web-research
description: Use when you need web research or browser interaction with high token efficiency. Prefer Playwright CLI session-based navigation, snapshot refs, and targeted extraction over full-page fetches or verbose DOM dumps.
---

# Playwright-Efficient Web Research

Use this skill for web exploration tasks where context window efficiency matters.

## Use This Skill When

- The user asks to research web pages, compare content across sites, or extract specific facts.
- Browser interaction is required (click, type, login flow, pagination, dynamic content).
- Repeated full HTML/text fetch would waste tokens.

## CLI vs MCP Boundary

- Default: **Playwright CLI** (`playwright-cli`) with direct commands (no wrapper scripts).
- Fallback: **Playwright MCP** only for long-running/state-heavy autonomous loops requiring persistent tool-level introspection.

## Core Rules

1. Reuse one named session per task (`-s=<session>`); avoid reopening browser every step.
2. In this sandbox, pass `--browser=chromium` explicitly unless you intentionally need another channel.
3. Use `snapshot` to get element refs, then interact by ref (`click e12`, `fill e8 ...`).
4. Extract only required fields with `eval`; do not dump full page content unless explicitly requested.
5. Capture screenshot/PDF/logs only when evidence is required.
6. Close session when done (`close`, optional `delete-data`).
7. Keep sessions non-persistent by default; enable `--persistent` only when cross-command login state is explicitly required.

## Workflow (Direct CLI)

1. Open session once (default: non-persistent):
```bash
playwright-cli -s=research-1 open "https://example.com" --browser=chromium
```

If the workflow explicitly requires saved login/session state:
```bash
playwright-cli -s=research-1 open "https://example.com" --browser=chromium --persistent
```

2. Navigate + interact with refs:
```bash
playwright-cli -s=research-1 snapshot
playwright-cli -s=research-1 click e15
playwright-cli -s=research-1 fill e7 "search query"
playwright-cli -s=research-1 press Enter
```

3. Targeted extraction (minimum needed fields only):
```bash
playwright-cli -s=research-1 eval \
  "() => ({ title: document.title, h1: document.querySelector('h1')?.textContent?.trim() ?? null })"
playwright-cli -s=research-1 eval "el => el.textContent?.trim() ?? null" e15
```

4. Optional evidence:
```bash
playwright-cli -s=research-1 screenshot --filename=/tmp/research-1.png
playwright-cli -s=research-1 pdf --filename=/tmp/research-1.pdf
playwright-cli -s=research-1 console
playwright-cli -s=research-1 network
```

5. Cleanup:
```bash
playwright-cli -s=research-1 close
playwright-cli -s=research-1 delete-data
```

## Anti-Patterns

- Repeatedly opening new sessions for each click.
- Fetching complete page text/DOM when only 2-3 fields are needed.
- Using screenshots as default extraction path.
- Adding unnecessary wrapper scripts when direct CLI commands are sufficient.
- Switching to MCP for simple linear navigation tasks.

## Notes

- If global `playwright-cli` is unavailable, run the same commands with `npx --yes @playwright/cli ...`.
- Session names should be task-specific (`news-compare`, `pricing-check`, `auth-flow-debug`).

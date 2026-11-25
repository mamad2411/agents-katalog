---
name: ultimate-playwright
description: Browser automation via ultimate-playwright-mcp. Use when the agent needs to control a shared Chrome browser — open tabs, navigate, click, type, fill forms, take snapshots. Handles multi-user tab group isolation so multiple sessions can share one browser without interference. Use for web browsing, scraping, form filling, testing, or any browser interaction task.
---

# Ultimate Playwright MCP

Browser automation through a shared Chrome instance with per-session tab isolation.

## Tab Group Convention

**Always create a tab group before opening tabs.** Name it after your session (last segment of your session key, e.g. `main`, `mira`).

```
1. browser_tab_group  action=create  name=<session-name>  color=blue
   → groupId: g_abc123...

2. browser_tabs  action=new  groupId=g_abc123  url=https://example.com
   → targetId: ABC...

3. browser_snapshot  targetId=ABC...
   → accessibility tree with element refs (e1, e2, ...)

4. browser_click  ref=e5  targetId=ABC...
```

## Core Workflow

1. **Create group** → `browser_tab_group` (create) → get `groupId`
2. **Open tabs** → `browser_tabs` (new) with `groupId` → get `targetId`
3. **Navigate** → `browser_navigate` with `targetId` and `url`
4. **Read page** → `browser_snapshot` with `targetId` → returns element refs (e1, e2…)
5. **Interact** → `browser_click`, `browser_type`, `browser_hover`, `browser_press_key`, `browser_fill_form` using `ref` from snapshot
6. **Wait** → `browser_wait_for` with `text`, `selector`, `url`, `loadState`, or `timeMs`
7. **Close** → `browser_tabs` (close) with `targetId` or `index`
8. **Cleanup** → `browser_tab_group` (delete) with `groupId`

## Tools Reference

| Tool | Key Params | Notes |
|------|-----------|-------|
| `browser_tab_group` | `action` (create/list/delete), `name`, `color`, `groupId` | Colors: grey, blue, red, yellow, green, pink, purple, cyan |
| `browser_tabs` | `action` (list/new/close/select), `groupId` (required for new), `url`, `targetId`, `index` | `groupId` scopes list/close/select too |
| `browser_navigate` | `url`, `targetId` | |
| `browser_snapshot` | `targetId` | Returns element refs (e1, e2…) for interactions |
| `browser_click` | `ref`, `targetId`, `button`, `doubleClick` | |
| `browser_type` | `ref`, `text`, `targetId`, `submit` | Set `submit=true` to press Enter after |
| `browser_hover` | `ref`, `targetId` | |
| `browser_press_key` | `key`, `targetId` | Keys: Enter, Escape, Tab, ArrowDown, etc. |
| `browser_fill_form` | `fields` (array of {ref, type, value}), `targetId` | Batch fill multiple fields |
| `browser_evaluate` | `expression`, `targetId`, `ref` (optional) | Run JS in page context — for portal/overlay elements invisible to snapshot |
| `browser_wait_for` | `text`, `textGone`, `selector`, `url`, `loadState`, `timeMs`, `targetId` | |

## Key Concepts

- **targetId** — uniquely identifies a browser tab across all sessions. Returned by `browser_tabs new`. Pass to every tool that operates on a tab.
- **groupId** — isolates your tabs from other sessions. Required when creating tabs. Scopes list/close/select operations.
- **ref** — element reference from `browser_snapshot` (e.g. `e1`, `e5`). Used by click/type/hover. Refs are only valid for the snapshot they came from — re-snapshot after navigation or significant DOM changes.
- **Shared cookies** — all sessions share one Chrome BrowserContext, so login state persists across tab groups.

## Tips

- Snapshot before interacting — refs change when the page updates.
- Use `browser_wait_for` with `text` or `loadState=networkidle` after navigation before snapshotting.
- For forms, prefer `browser_fill_form` over individual `browser_type` calls.
- Tabs persist in Chrome — Patrick can see and reuse them.
- Tab groups appear as colored groups in Chrome's tab bar.

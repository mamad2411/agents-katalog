---
name: feishu
description: Operate the Feishu / Lark desktop client via simulated keyboard and mouse through clawtouch-mcp — messaging, docs, sheets, and calendar workflows, with the menu paths and shortcuts LLMs typically get wrong on this Chinese-market suite. Tested against Feishu/Lark v7.x on Windows and macOS. Load when the user wants to message, edit docs/sheets, or manage calendar events in Feishu or Lark.
---

# Skill: Feishu / Lark (飞书)

For LLM agents driving **Feishu desktop** through `clawtouch-mcp`.
Feishu is the dominant B2B collaboration suite at Chinese tech
companies. Its UI is mostly LLM-blind (much less training data than
Slack or Teams), which is exactly why this skill exists.

> **Tested against**: Feishu desktop **v7.x** (zh-CN) / Lark desktop
> **v7.x** (en) on Windows 10/11 and macOS 12+. Last verified 2026-05-26.
>
> ⚠️ Feishu/Lark ship UI revisions every few months. If the sidebar,
> shortcuts, or menu paths described below don't match what you see,
> the skill may be out of date — please open an issue at
> [tinqiao-oss/clawtouch-skills](https://github.com/tinqiao-oss/clawtouch-skills/issues)
> so we can refresh it.

## When to use this skill

The user is operating Feishu desktop (`Feishu.exe` on Windows,
`Lark.app` on macOS — same app, different branding) for messaging,
doc / sheet editing, or calendar / scheduling.

## App-wide navigation

- **Left sidebar** = section switcher: 消息 (Messages) / 文档 (Docs)
  / 日历 (Calendar) / 会议 (Meetings) / 审批 (Approval) / 工作台.
  Each has a default keyboard shortcut but clicking the sidebar icon
  is the most reliable.
- **Global search**: `Ctrl+K`
- **Quick chat switcher**: `Ctrl+Alt+K`
- **Settings**: top-right avatar → 设置; or `Ctrl+,`

## Messaging (即时消息)

| Task | Step sequence |
|------|---------------|
| Open a specific chat | `hid.key("ctrl+alt+k")` → type name → Enter |
| Send a message | Click input area or Tab to it → `hid.type("...")` → `Ctrl+Enter` (default — see send-key gotcha below) |
| Reply to a specific message | Hover until reply icon appears → `hid.click` |
| Insert emoji | `Ctrl+Shift+;` opens emoji picker |
| Send file | Drag-drop, or click the paperclip icon |
| @ mention | Type `@` then keep typing the name → arrow keys + Enter to pick |

### Send-key gotcha ⚠️

Feishu has a per-user setting: "press Enter to send" vs "press
Ctrl+Enter to send". The default in new installs is **Ctrl+Enter**,
but many users flip it. The agent should default to `Ctrl+Enter` and
only fall back to `Enter` after observing a misfire (a message that
contains literal newlines that should have been sends).

## Docs (飞书文档)

Feishu docs are **block-based** (similar to Notion). Each paragraph,
heading, table, image is a "block."

| Task | Step sequence |
|------|---------------|
| New doc | From the Docs section, click the "+" button. No reliable keyboard shortcut |
| Heading 1 / 2 / 3 | `# `, `## `, `### ` at start of line (markdown shortcut) |
| Bullet list | `- ` at start of line |
| Checkbox | `[]` followed by space at start of line |
| Bold | Select text → `Ctrl+B` |
| Insert link | Select text → `Ctrl+K` → paste URL → Enter |
| Insert table | Type `/` at start of empty line → type "table" → Enter |
| Save | Auto-saves; no `Ctrl+S` needed |

### Block menu (`/`)

Typing `/` at the start of an empty line opens the block menu (Notion-style).
Type the block type name (table, image, checklist, …) and Enter.

## Sheets (飞书表格)

Same model as WPS / Excel for basic editing:

| Task | Step sequence |
|------|---------------|
| Cell navigation | Arrow keys; Tab = right; Enter = down |
| Go to cell | `Ctrl+G` |
| Formula | `=SUM(...)` / `=VLOOKUP(...)` etc — Excel-compatible syntax |
| Add comment to cell | `Ctrl+Alt+M` |

## Calendar (日历)

| Task | Step sequence |
|------|---------------|
| Create event | `Ctrl+N` or click "+" |
| Go to today | `T` (when calendar pane has focus) |
| Day / week / month view | `D` / `W` / `M` (with calendar focus) |

## Known gotchas

- **File send confirmation popup**: dragging a large file triggers
  a confirm dialog — watch for it.
- **Voice message hold-to-record**: clicking the mic icon does
  nothing; *holding* it starts recording. Agents should avoid
  touching this button unless voice recording is explicitly the task.
- **Corner notification toasts**: incoming-message toasts may overlap
  click targets near screen edges. Wait or dismiss first.
- **Login flow**: Feishu uses QR-code or SSO login. The agent
  should **not** try to type credentials.

## When this skill doesn't help

- Multi-tenant switching (multiple workspaces): the dropdown is
  fragile and tenant-specific
- Video meetings UI: real-time, prefer screenshot-based reasoning
- Mobile-app mirroring: a different surface, not covered here

---
name: notion
description: Notion-specific heuristics for driving the Notion desktop app via background-computer-use. Use when the user asks you to edit a Notion page, add a block, create a database row, or otherwise interact with Notion's UI.
---

# Driving Notion with background computer use

Notion is a block-based editor inside a WebView, so generic GUI heuristics
fail in specific ways. Follow these rules in addition to the main
`computer-use` skill:

1. Always call `get_app_state app="Notion"` before interacting.
2. Each paragraph/heading/bullet is a **block**. `Return` creates a sibling
   block of the same type; `shift+Return` is a soft line break.
3. Type `/` at the start of a block to open the slash menu. The menu is
   **async** — re-call `get_app_state` before clicking a menu item.
4. Do not use `set_value` on body text. Use `click` + `press_key key="command+a"`
   + `type_text`. `set_value` only works on native inputs (search, page title
   in some views), not on contenteditable blocks.
5. Use `perform_secondary_action` with `ShowMenu` on sidebar rows instead of
   hovering to click the `…` button.
6. After any destructive action (delete page, archive), stop and confirm with
   the user before the next step.

Full behavioral notes live in `server/app-hints/Notion.md` — the MCP server
injects them automatically inside `<app_hints>` on every `get_app_state` call
for Notion.

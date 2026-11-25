---
name: numbers
description: Apple Numbers spreadsheet heuristics for background-computer-use. Use when the user asks you to edit a Numbers spreadsheet, add a formula, update a cell, or switch sheets.
---

# Driving Apple Numbers with background computer use

Use these rules in addition to the main `computer-use` skill:

1. Always call `get_app_state app="Numbers"` before interacting.
2. A single `click` selects a cell; double-click or `press_key key="Return"`
   enters edit mode. Triple-click selects the cell's existing value.
3. Use `Tab` / `shift+Tab` / `Return` / `shift+Return` to move between cells —
   never embed those as literal characters in `type_text`.
4. Prefer `set_value` on Format-inspector numeric inputs (`settable=true`).
5. For multi-cell selection, use `drag` from the top-left cell to the
   bottom-right cell.
6. Always re-call `get_app_state` after switching sheets — the entire tree
   changes.

Detailed behavior lives in `server/app-hints/Numbers.md`, which is injected
into `<app_hints>` on every `get_app_state` call for Numbers.

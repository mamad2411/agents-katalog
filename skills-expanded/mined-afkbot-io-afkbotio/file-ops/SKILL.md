---
name: file-ops
description: "Workspace filesystem operations via `file.*` tools. Use when listing, reading, searching, writing, or editing files inside the allowed workspace."
aliases:
  - files
  - file
triggers:
  - create file
  - read file
  - write file
  - edit file
  - update file
  - создай файл
  - прочитай файл
  - запиши в файл
  - отредактируй файл
  - измени файл
tool_names:
  - file.list
  - file.read
  - file.write
  - file.edit
  - file.search
  - diffs.render
preferred_tool_order:
  - file.list
  - file.read
  - file.write
  - file.edit
  - diffs.render
  - file.search
---

# file-ops

Use this skill for any workspace file operation. Do not call `file.*` tools without this skill.

## Tool family

- `file.list`
- `file.read`
- `file.write`
- `file.edit`
- `file.search`
- `diffs.render` when the user explicitly asks to show what changed after a mutation

## Required flow

1. Confirm target path and expected change/result.
2. Call one `file.*` tool.
3. For write/edit actions, prefer the returned bounded `before_text` / `after_text` payload.
4. If the user asked for a diff, call `diffs.render` using the returned `diff_suggestion` payload when present.
5. Report exact affected paths and outputs.

## Safety rules

- Stay within workspace policy boundaries.
- Never output secrets if discovered in files.
- Avoid destructive edits without explicit user intent.
- Runtime routes the correct skill automatically; do not send `skill_name`.

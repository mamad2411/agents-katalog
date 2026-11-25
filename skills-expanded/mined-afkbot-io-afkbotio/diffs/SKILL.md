---
name: diffs
description: "Render readable unified or HTML diffs from inline text or local files. Use after file edits when you need to inspect or show exact changes, optionally as persisted artifacts."
aliases:
  - diff
  - patch
  - compare-files
triggers:
  - diff
  - patch
  - compare
  - changes
  - изменения
  - покажи diff
  - что изменилось
tool_names:
  - diffs.render
  - file.read
preferred_tool_order:
  - file.read
  - diffs.render
---
# diffs

Use this skill when the task is to compare two texts or two file versions and present the change
compactly.

Tool methods:
- `diffs.render`
- `file.read` when you first need to capture current file content before editing

When to use:
- after `file.write` / `file.edit`, if the user wants to inspect exact changes;
- when the user asks for a patch, diff, or “what changed?”;
- when comparing two local files or one saved text against the current file on disk.

Preferred workflow:
1. If a preceding `file.write` or `file.edit` result already includes `diff_suggestion`, use it directly.
2. Otherwise, if you need a before/after diff for one file mutation, read the original file first.
3. Perform the edit.
4. Call `diffs.render` with:
   - inline `before` + `after`, or
   - `before_path` + `after_path`, or
   - inline `before` + `after_path`.
5. Use `format=unified` for compact textual review.
6. Use `format=both` when a richer HTML rendering is useful.
7. Use `output_mode=artifact` or `output_mode=both` when the diff must be attached, shared, or revisited later.
8. When the tool returns `markdown_preview`, prefer reusing it directly instead of hand-formatting your own diff block.

`diffs.render` params:
- `before` or `before_path` (exactly one)
- `after` or `after_path` (exactly one)
- optional: `before_label`, `after_label`
- optional: `format=unified|html|both`
- optional: `output_mode=inline|artifact|both`
- optional: `context_lines`
- optional: `max_chars_per_input`

Notes:
- file paths are resolved from the active profile workspace by default and still respect the normal
  file/path policy.
- `output_mode=inline` returns diff bodies directly in tool payload.
- `markdown_preview` is the preferred compact reply-ready rendering for chat output.
- `output_mode=artifact` writes diff files under `profiles/.system/artifacts/diffs/` and returns metadata with file paths and expiry.
- `output_mode=both` keeps inline bodies and writes artifacts.

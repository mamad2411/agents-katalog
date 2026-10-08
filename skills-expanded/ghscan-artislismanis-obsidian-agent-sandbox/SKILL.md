---
name: reviewed-edit
description: Make safe edits to vault files outside the writable workspace directory using human-in-the-loop review. Use when the user asks to edit an existing note that lives outside $OAS_VAULT_WRITE_DIR, or explicitly says "review before applying".
---

# reviewed-edit

This skill covers the `reviewed` write mode: each change outside `$OAS_VAULT_WRITE_DIR` triggers a diff modal in Obsidian and won't apply until the user approves. It describes how to plan and sequence *content* writes (create/modify/append/frontmatter/patch) so the user gets a useful review experience. For rename/move/delete, use `note-refactor` instead: it covers the same review mechanics plus backlink-blast-radius analysis specific to structural changes.

**Read `references/vault-safety.md` before your first write.** It carries the shared rules (the three write modes, per-file delete confirmation, plan-before-applying, one unit at a time) for this skill, `note-refactor`, `link-hygiene`, and `tag-audit`. Two of those rules are absolute and repeated here so you never act without them:

- Print the full plan and get approval before the first write.
- Get explicit per-file approval before any delete, even inside an approved batch.

## When to use

- User asks you to modify a file that isn't under `$OAS_VAULT_WRITE_DIR`.
- User says "ask me before writing" or similar.
- Planning or sequencing a rename/move/delete: use `note-refactor`. The manage-tier table below stays here as the shared reference the other skills point at.

## Prerequisites

- Write mode set to `reviewed` in Obsidian plugin settings. Under `scoped` the `_reviewed` tools aren't registered: offer to work inside the write dir instead, or ask the user to switch the mode.
- Look up `$OAS_VAULT_WRITE_DIR` via the shell (`echo $OAS_VAULT_WRITE_DIR`) before deciding whether a path is in-scope.

## Tool selection

Content-write ops register a `_reviewed` variant in `reviewed` mode; that variant calls the review modal before applying:

| Operation | Tool |
|---|---|
| New file | `vault_create_reviewed` |
| Full rewrite | `vault_modify_reviewed` |
| Append at end | `vault_append_reviewed` |
| Prepend at top (post-frontmatter) | `vault_prepend_reviewed` |
| Edit frontmatter property | `vault_frontmatter_set_reviewed` / `vault_frontmatter_delete_reviewed` |
| Find/replace within one file | `vault_search_replace_reviewed` |
| Targeted insert at heading/line | `vault_patch_reviewed` |

Manage-tier ops (rename / move / delete / create-folder / batch-frontmatter) keep their plain names: there is no `_reviewed` suffix. This table is the shared reference for `note-refactor`, `link-hygiene`, and `tag-audit` as well. With the `manage` tier on, a call to any of them outside `$OAS_VAULT_WRITE_DIR` follows the write mode: blocked under `scoped`, review modal showing the affected backlinks under `reviewed`, applied with no modal under `full`. `vault_batch_frontmatter` is the exception: it reviews the whole batch in one modal with per-item picks, and refuses outright under `scoped`.

| Operation | Tool |
|---|---|
| Rename a file | `vault_rename` |
| Move a file | `vault_move` |
| Delete a file | `vault_delete` |
| Create a folder | `vault_create_folder` |
| Batch-set frontmatter across many files | `vault_batch_frontmatter` |

**Never** point a plain content-write tool at an out-of-workspace path: the `writeScoped` guard blocks it. The `_anywhere` variants exist only in `full` mode, where no write is reviewed at all, so don't reach for them to skip a modal.

## Pre-write checklist

Before any `_reviewed` call:

1. **Confirm target.** If the user gave a note name, use `vault_file_info` to resolve it to a path. Don't guess.
2. **Check blast radius.** For a large modify, run `vault_backlinks` first. Tell the user how many notes link in. Don't break outbound references without warning. Rename and delete get their own blast-radius pass in `note-refactor`.
3. **Narrow the change.** Prefer `vault_search_replace` or `vault_patch` (small diff) over `vault_modify` (full rewrite) so the review modal shows minimal change surface.
4. **Chunk per-file.** Each tool call produces one modal. If you have five files to edit, that's five modals in sequence: warn the user upfront.

## During the chain

- Expect an error result with text "Change rejected by user." when the user cancels. Treat it as a hard stop: don't retry, don't try a different tool.
- If the user approves the first call but rejects the second, stop and summarise what was applied.
- After every approved write, confirm to the user (e.g. "Modified notes/foo.md (42 bytes → 58 bytes)") so they have an audit trail beyond the modal.

## Frontmatter review

`vault_frontmatter_set_reviewed` and `vault_frontmatter_delete_reviewed` show the review modal with JSON-stringified old/new frontmatter rather than the full file diff. That's intentional: the actual file mutation goes through Obsidian's `processFrontMatter` which re-serialises YAML, so previewing the exact YAML would lie. Mention this in your explanation if the user asks why the diff looks like JSON.

## Example

User: "Add `status: draft` to the frontmatter of notes/manuscript.md."

```
1. vault_file_info(path="notes/manuscript.md")  // confirm the file exists
2. (no backlinks check: FM change doesn't affect links)
3. vault_frontmatter_set_reviewed(
     path="notes/manuscript.md",
     property="status",
     value="draft"
   )
   → modal shows { ... } vs { ..., status: "draft" }
4. User approves → "Set status on notes/manuscript.md"
```

For a multi-file change:

```
User: "Add `reviewed: true` to every note in projects/Q4/."

Me: "I'll need to do this one file at a time since each one requires your approval. Projects/Q4/ has 14 .md files, so that's 14 modals. Want to proceed, or would a batch-with-dryrun approach work? (vault_batch_frontmatter has a preview mode.)"
```

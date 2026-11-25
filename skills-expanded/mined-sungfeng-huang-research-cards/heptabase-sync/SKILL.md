---
name: heptabase-sync
description: "(formerly obsidian-sync) The heptabase segment engine of note-sync: block-level level-2 BIDIRECTIONAL sync between Heptabase and the local .md store (vault) — incremental forward mirror, block-level write-back against a ProseMirror snapshot (all-or-nothing per card), three-way property sync, adoption of hand-made .md files, deletion propagation into .trash/, and a conflict ledger (Sync Conflicts.md). Prefer invoking via note-sync (--mode heptabase); run standalone for cron or engine-level debugging. Use when the user asks to sync Heptabase cards to the vault/Obsidian, 同步卡片到 obsidian／vault, push paper/overview cards, or after batch edits in either app."
allowed-tools: Bash(heptabase *) Bash(python3 *)
---

# Heptabase → Obsidian Sync (Level 1)

> **已併入 [note-sync]**：日常請用 `skills/note-sync/sync.py`（單一入口、全鏈編排＋衝突彙總；`--mode heptabase` 等價單跑本段（舊名 `--mode obsidian` 仍相容））。本檔保留引擎語義的完整說明；引擎 `sync.py` 檔案原位不動。

## Agent（claude / codex）

兩個 agent 皆可駕駛（Codex 端：`research-cards@private-plugins` plugin 的 heptabase-sync skill）。唯一的 Claude
限定步驟：`unresolved_highlights` 需要 mcp get_object 讀 highlightElement——Codex
駕駛時把該清單回報給使用者，請對方在 Claude Code session 補 highlights.json。

## Run

```bash
python3 "$(dirname "$0")"/sync.py            # real run
python3 .../sync.py --dry-run                # preview, no writes
python3 .../verify.py                        # vault integrity check, run after sync
```

`verify.py` checks: attachment extensions Obsidian can render, missing
embeds, broken wikilinks/block refs, leftover placeholders, duplicate
heptabase_ids, and state.json consistency. Expect `CLEAN`.

NOTE: the vault path comes from config `obsidian.vault`. If it lives in
iCloud Drive, run OUTSIDE the sandbox (the terminal needs Full Disk Access).

## What it does

- **Collections** are config-driven: every `heptabase.collections.<key>`
  entry with a filled `tag_id` becomes one collection, mirrored into
  `obsidian.folders.<key>` (default: capitalized key). Optional `filter`
  narrows by property (e.g. papers → Source Type=alphaXiv). Typical set:
  papers → `Papers/`, overviews → `Overviews/`, projects → `Projects/`.
  Entries without a `tag_id` (or with a `<placeholder>`) are skipped —
  they may exist as metadata for other skills.
- **Body**: one-way Heptabase → Obsidian. Skips cards whose `lastEditedTime`
  and `contentMd5` are unchanged (fast incremental). ProseMirror → markdown
  incl. math (`$...$`/`$$...$$`), tables, toggle/numbered/todo lists,
  blockquotes, code, images (external URL kept; Heptabase-local files exported
  to `<folder>/attachments/`).
- **Properties**: 3-way sync using the snapshot in the state file. Only one
  side changed → propagate (Obsidian → Heptabase via `card set-property`).
  Both changed → reported in `conflicts`, nothing written. Title/created/
  modified/heptabase_id always follow Heptabase.
- **Links**: target synced → `[[wikilink]]` (alias form when link text
  differs); target not synced → `[title](heptabase URL)`; same-card block
  anchors → Obsidian block references (`[[#^xxxxxxxx|label]]`, target block
  gets a trailing `^xxxxxxxx` = first 8 chars of the Heptabase block id;
  dangling anchors whose target block no longer exists degrade to plain
  text); highlight embeds → blockquote from the user data dir's `highlights.json`.
- **Renames**: title change renames the .md file and rewrites wikilinks in
  managed folders.
- **Journal bridge** (opt-in: `obsidian.journal.enabled`, window
  `obsidian.journal.days`, default 30; folder `obsidian.journal.folder`,
  vault-relative, empty = vault root): one-way mirror of the Heptabase
  journal into `<YYYY-MM-DD>.md` daily notes under that folder. The sync owns ONLY
  the marker block `<!-- hepta-journal:start -->` … `<!-- hepta-journal:end -->`
  (kept at the top); everything outside it — the user's own daily writing on
  any device — is never touched. Incremental per-day via `contentMd5`
  (`journals` section of the state file); empty Heptabase days never create
  files; a day that becomes empty clears the block but keeps the markers;
  malformed markers (one deleted / reordered) → conflict report, file left
  alone. **Reverse flow (daily note → Heptabase journal) is a deliberate
  non-goal**: content in the user area does not flow back (a level-2-style
  journal write-back would be a separate feature).
- State: `<vault>/.hepta-sync/state.json` (filenames, md5, prop snapshots,
  resolved external titles, exported fileIds, per-day journal md5).

## Agent duties after each run (read the JSON report)

- `conflicts` — show the user both sides, apply their choice manually
  (edit the file or `heptabase card set-property`), then re-run.
- `unresolved_highlights` — fetch each via MCP
  `get_object(objectId, "highlightElement")`, add `{highlight, note}` to
  `~/.config/research-cards/highlights.json`, re-run sync.
- `unknown_nodes` — a ProseMirror node type the converter doesn't handle;
  inspect via `heptabase note read <cardId>` and extend `sync.py`.
- `removed_from_tag` — card left the tag or was trashed; the vault file is
  NOT deleted automatically. Ask the user whether to delete/archive it.
- `writeback_errors` — usually an option name that doesn't exist in the
  Heptabase select/multiSelect; ask the user whether to add the option in
  Heptabase or fix the frontmatter value.
- `bootstrap_fm_diffs` — only on first adoption of existing files; Heptabase
  won. Surface to the user if non-empty.

## Level 2: block-level body write-back (IMPLEMENTED)

When only the Obsidian side changed (tracked via `body_hash` + contentMd5),
`sync.py` merges at BLOCK granularity using the per-card ProseMirror cache
(`<vault>/.hepta-sync/pm-cache/<cardId>.json`, written on every forward
render; `--rebuild-cache` regenerates all):

- Unchanged blocks reuse their original PM nodes — colors, toggles, block
  ids, underline all survive untouched.
- Edited/inserted blocks are parsed by `md2pm.py` (safe subset), then
  round-trip-verified: parsed nodes are re-rendered and must reproduce the
  user's markdown exactly.
- **Degradation = conflict, not write** (all-or-nothing per card): if any
  edited/deleted block's original contains a lossy construct (highlight
  embed, custom image size, complex table, background-color mark,
  whiteboard/section/pdf/chat mention) — or the round-trip check fails — the
  whole card is reported in `conflicts` with the block and reason, and
  NOTHING is written to Heptabase. The file is left as-is and stays pending
  until resolved. Toggles (`- ⏵ ` bullet prefix — deliberately NOT a checkbox
  syntax, so there is nothing clickable that could rewrite the marker), text
  colors (`<span style=color>`), and underline (`<u>`) round-trip via the
  plugin markdown dialect and are NOT lossy anymore. `⏵ ` at the start of a
  bullet is a reserved dialect prefix.
- **Type-change guard**: a toggle rewritten as a todo checkbox (`- [ ]`/
  `- [x]`) is a node-type change; write-back raises a conflict instead of
  converting the Heptabase toggle silently.
- Successful write-back uses `note save --content-md5` (optimistic lock),
  then re-renders the card back into the vault (normalizes formatting) and
  refreshes cache/state.
- Both sides changed (real contentMd5 divergence) → conflict, no action.

Conflict resolution playbook: show the user the block + reason; either apply
their edit directly in Heptabase (then re-run sync) or revert the Obsidian
block to match (`git`-style: re-copy from the freshly synced body).

## Conflict ledger: `<vault>/Sync Conflicts.md`

Every real (non-dry) run regenerates this note from `state.conflict_log`:
live conflicts under 未解決 (wikilink to the file, prop, reason, block
excerpt, first-seen date), disappeared ones auto-archive under 已解決 with a
resolution date (safe because unresolved conflicts re-report every run).
Do NOT hand-edit the note — it is overwritten. Use it as the queue when the
user asks to 修衝突 / resolve sync conflicts.

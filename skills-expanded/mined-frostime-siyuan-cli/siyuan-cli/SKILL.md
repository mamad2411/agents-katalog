---
name: siyuan-cli
description: "Manage SiYuan Note with the `siyuan-cli` CLI. Use this whenever the user mentions SiYuan, notebooks, documents, blocks, or wants to query/update a SiYuan knowledge base."
metadata:
  version: "{{VERSION}}"
---

# SiYuan CLI

Agent-first CLI for SiYuan Note. This SKILL is the entry point; the bundled resources listed under Routing hold task playbooks and reference detail.

## Shipped skill, matching version

`siyuan-cli skill read` always serves the skill bundled with the running CLI. An installed copy can lag behind it: the skill version is on every `skill read` envelope, `siyuan-cli --help` prints the CLI version and warns when an installed copy differs. On a mismatch, run `siyuan-cli skill install`, then re-read before trusting any detail.

## Bootstrap

```bash
siyuan-cli --help
siyuan-cli current which
```

If `siyuan-cli` is missing: `npm install -g @frostime/siyuan-cli`. Always invoke as `siyuan-cli` (on SiYuan ≥3.7.0, bare `siyuan` may resolve to SiYuan's own CLI). No workspace configured → `recipes/workspace.md`.

## Workspace selection

```text
┌─ one/few calls?         → --workspace <name>
├─ project directory?     → .siyuan-cli.yaml with workspace: <name>
├─ long-lived caller?     → process binding (cli-usage/process-binding.md)
└─ change machine default → current global <name>
```

Before content work: `siyuan-cli current which`. Writing to `config.current` only (`source: global-current`) when user never named that target? → ask.

Binding: read `cli-usage/process-binding.md` first.
Bind and confirm must be two separate tool/CLI calls from the same long-lived caller, not one shell block. And it anchors to the nearest process common to both calls (the harness process).
Cancel with the exact command bind printed; unbind after work completes. Project file + binding disagreement → use one-call `--workspace` exception or fix the conflict.

## Command discovery

Docs = decision map. `--help` = parameter syntax.

```bash
siyuan-cli api <id> --help       # params, INPUT SOURCES, examples
siyuan-cli tool <id> --help      # params, examples, behavior
siyuan-cli api list              # endpoints + classification/severity labels
siyuan-cli tool list             # tools
```

Input sources: check `--help` INPUT SOURCES per parameter. When absent, use literal value or whole-payload `-j <json>` / `-f <file>`.

## Safety anchors

| # | Rule |
|---|------|
| 1 | Confirm workspace before content work; never silently switch for writes. |
| 2 | Write only to stable id / resolved root_id; never title/keyword/hpath alone. |
| 3 | Non-append writes require `get-block-info` + bounded `get-block-content --showId true`. |
| 4 | Smallest safe surface: append → block update → batch update → guarded brute-edit. |
| 5 | `CONTENT_FILTERED` / truncation = valid but incomplete; don't infer absence. |
| 6 | `--yes` is not a safety check; use only after target verified + action intended. |
| 7 | `api raw` bypasses schema/resource guards/response filtering; one-off only. |
| 8 | Approval browser auto-open may be debounced; parse every `APPROVAL_PENDING` stderr event, not browser opens. |

Ask user when: no token/URL · wrong workspace · multiple plausible write targets · destructive operation lacks confirmation · daily-note notebook unknown.

## Mode gate

- **Fast path**: read/list/search, or create/append with explicit stable target.
- **Slow path**: edit existing content; target is title/keyword/hpath; affects multiple blocks/document block; may regenerate ids; destructive/approval-gated.

## Canonical input patterns

Check `--help` INPUT SOURCES first.

```bash
# heredoc (bash) / here-string (PowerShell @'...'@): parameter supports stdin
siyuan-cli api block.appendBlock --parentID <id> --data @stdin --yes <<'EOF'
Content here.
EOF

# @file: parameter supports file
siyuan-cli tool update-block --blocks @file:./updates.json --yes

# pipe: parameter supports stdin
cat query.sql | siyuan-cli api query.sql --stmt @stdin

# whole payload: all commands support -j / -f
siyuan-cli api attr.setBlockAttrs -j '{"id":"<id>","attrs":{"custom-key":"value"}}'
siyuan-cli api attr.batchSetBlockAttrs -f ./attrs.json --yes
```

## Hot paths

Top goals with command choice and key flags. Full syntax: `<command> --help`.

**Append to known target:**
```bash
siyuan-cli block.appendBlock --parentID <id> --data @stdin <<'EOF'
...
EOF
```
Daily note: use `block.appendDailyNoteBlock --notebook <id> --atDate <date>` instead.

**Insert a local file as asset into a doc:**
```bash
siyuan-cli tool insert-asset --assetFile ./photo.png --afterBlockId <block-id>
```
File type will be mapped to the right markdown form, `--asIframe` embeds any file as iframe block.

**Find document by title/keyword:**
- known exact/substring → `filetree.searchDocs --k "..."`
- have doc ID, want details → `block.getBlockByRootID --rootID <id>` or `tool get-block-info <id>`
- browse notebook tree → `tool list-doc-tree --entry <notebook-id> --depth <n>`
- complex filter → `api query.sql "SELECT ... FROM blocks WHERE type='d' AND ... LIMIT 50"`

**Find blocks by content phrase:**
```bash
siyuan-cli tool locate-block --pattern "%phrase%" [--id <doc> | --box <notebook>]
```

**Read document/block:**
```bash
siyuan-cli tool get-block-content <id> [--range children] [--limit=-1]
```
Default `--limit` exists for safety; use `--limit=-1` for full read. `--showId true` injects block IDs for edit targeting.

**Fetch a file from the workspace (assets, .sy, any workspace file):**
```bash
siyuan-cli api file.getFile data/assets/foo-20240922152051-7dpjfpv.png [--outFile ./foo.png]
```
If no `--outFile`: text content prints, binary written to a temp file and its path is printed.
An overwrite `--outFile` needs `--yes`.

**Download an asset from the workspace:**
```bash
siyuan-cli tool get-asset --assetPath assets/foo-20240922152051-7dpjfpv.png [--outFile ./foo.png]
```
Same output behavior as `file.getFile`, but accepts asset paths (`assets/` prefix).

**Update block:****
```bash
siyuan-cli tool update-block <id> --markdown "..." [--dry-run] [--yes]
```
Preserves `custom-*` attributes. Never use raw `block.updateBlock` (it erases them).

All: use `@stdin` / `@file:path` for multiline or special-char content to avoid shell escaping.

## Error triage

| Exit | Meaning | Action |
|------|---------|--------|
| 0 | success | parse stdout |
| 1 | general/kernel/approval/not found | read stderr JSON |
| 2 | config/workspace | `siyuan-cli current which` |
| 3 | network/kernel down | ask user to start SiYuan |
| 4 | auth/token | ask user for token |
| 5 | permission denied | `siyuan-cli current which` |

stderr = diagnostics; stdout = result; on failure stdout is empty. `--print json` applies to `api <endpoint>`, `tool <id>`, and `current *` (envelope `{ ok, data, extra }`); other commands either print fixed JSON or reject `--print`.

## Routing

Read a resource with `siyuan-cli skill read <path>`. Paths are relative to this skill; a bare `siyuan-cli skill read` also prints them as a manifest.

| Need | Read |
|------|------|
| workspace unconfigured, wrong, unreachable, or scope must be chosen | `recipes/workspace.md` |
| workspace binding chosen there | `cli-usage/process-binding.md` |
| config schema (behavior, rawApi, defaults, project-file) | `cli-usage/workspace-config.md` |
| locate user-named doc/block | `recipes/find-target.md` |
| read content ranges/paging/ids | `recipes/read-content.md` |
| reference/backlink navigation | `recipes/read-content.md` + `siyuan-guide/sql-query-guide.md` |
| edit/move/delete/batch/create | `recipes/edit-content.md` |
| daily notes | `siyuan-guide/dailynote-model.md` |
| block/path/sql model | `siyuan-guide/siyuan-block.md` |
| permissions/approval config | `cli-usage/permission.md` |
| custom API/tool extension | `cli-usage/extension.md` |
| deep CLI mechanics: flags, input-source edge cases, stdout/stderr, Approval Center, MSYS | `cli-usage/cli-overview.md` |
| **blocked** after `--help` / `--print json` / `--debug`: behaviour contradicts docs, or an exact runtime shape is required | `cli-usage/read-source.md` |

## Layer choice

| Shape | Prefer |
|-------|--------|
| normal note work | CLI + recipes |
| one known endpoint | registered `api` |
| multi-step operation | `tool` |
| one-off missing endpoint | `api raw` |
| repeated missing endpoint | API extension |
| repeated multi-call workflow | tool extension |
| user policy/defaults/templates | downstream Agent SKILL |

## First response rules

- Content tasks: use installed `siyuan-cli`; do not inspect repo source unless modifying siyuan-cli internals.
- User-named targets: `recipes/find-target.md` first.
- Writes beyond append-only: also `recipes/edit-content.md`.

## Domain rules

- Block is primary; document = container block (`type='d'`).
- Stable addressing: **id > root_id > path**; never hpath/title as stable key.
- `parent_id` = hierarchy; `root_id` = owning doc; `box` = notebook.
- Non-document block `path`/`hpath` describes containing document.
- SQL: always `LIMIT`; narrow with `root_id`/`box`/`type` before fuzzy `LIKE`.

## Gotchas

- MSYS/Git Bash rewrites leading `/` → `MSYS_NO_PATHCONV=1` or `//path`
- `--showId true` markers are edit targets, never brute-edit search text
- Registered endpoints > `api raw`; avoid permanent `rawApi.allow: ["*"]`
- SiYuan's index updates asynchronously: after a write, wait 1–2s (e.g. `sleep 1`) before index-sensitive reads (SQL, refs, frontmatter), or they may return stale data

## Last resort

The published package is unbundled ESM; its code can answer questions nothing else does — read it only after command output, structured errors, and the routed resource have failed, and only for the specific blocking question. Paths: `cli-usage/read-source.md`. Never edit installed files.

GitHub: [siyuan-cli](https://github.com/frostime/siyuan-cli) · [SiYuan kernel API](https://github.com/siyuan-note/siyuan/blob/master/kernel/api/router.go)

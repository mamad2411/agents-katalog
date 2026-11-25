---
name: feishu-markdown-sync
version: 1.6.0
description: Export Feishu wiki, doc, and Sheet page content into Git-friendly Markdown, CSV, workbook, preview, and format snapshot files; inspect, pull, plan, and guarded-push manifest-backed sync workspaces; manage Drive-native Markdown files separately; write CSV or JSON 2D array data back into explicit Feishu Sheet ranges with read-back verification; inline document images; expand embedded sheets into CSV plus Markdown previews; convert raw whiteboards into readable Mermaid previews plus raw JSON audit files; audit readability and round-trip fidelity; and re-import Markdown back into Feishu docs with original-position image and file restore via lark-cli positioned media insertion. Use when the user asks to sync, export, archive, audit, or re-import Feishu wiki, docx, Sheet, or Drive-native Markdown content in a Git-friendly way.
---

# Feishu Markdown Sync

Version: `v1.7.0`

Required `lark-cli`: `>= 1.0.39`

Some legacy script names and default export folders still use `wiki` for compatibility. Product and install names should use **Feishu Markdown Sync** because doc, Sheet, Drive-native Markdown, and whiteboard workflows are now in scope.

Migration note: the old installed skill name was `feishu-wiki-markdown-sync`. The current installed skill name is `feishu-markdown-sync`. Do not keep both installed directories under `$CODEX_HOME/skills`, because Codex will load two skills with the same functional scope.

## Configuration

This skill no longer hardcodes tenant domains or wiki tokens.

Set configuration through environment variables or CLI options:

```powershell
$env:FEISHU_BASE_URL = "https://your-tenant.feishu.cn"
```

Available configuration:

- `FEISHU_BASE_URL`: required tenant base URL for export links
- `FEISHU_WIKI_TOKEN`: optional default wiki token for export
- `FEISHU_OUTPUT_ROOT`: optional default export directory, defaults to `exports/feishu-wiki/` for compatibility
- `FEISHU_EXPORT_ROOT`: optional default audit directory
- `FEISHU_INCLUDE_SENSITIVE_METADATA`: optional, defaults to `false`
- `FEISHU_KEEP_SENSITIVE_PLACEHOLDERS`: optional, defaults to `false`
- `LARK_CLI_PATH`: optional custom `lark-cli` entry path

## Overview

Use this skill to convert a Feishu wiki tree into Git-friendly local files and, when needed, push one Markdown document back into a Feishu doc with inline images, embedded CodePen blocks, and CSV-expanded sheet content. Top-level Sheet pages and embedded Sheet blocks are part of the supported export scope. Sheet write-back is supported for explicit ranges through `scripts/import_feishu_sheet.cjs`. Workspace-level status, pull, plan, and guarded push use `scripts/feishu_sync.cjs`. For surgical document changes, prefer `lark-cli docs` v2 partial fetch/update instead of overwriting the whole document. Drive-native `.md` files are a separate path handled by `scripts/feishu_markdown_file.cjs`; do not use it to replace doc/wiki sync.

Run this skill from the target workspace root so generated files stay inside the repo.

## Core Capabilities

### Sync workspace status and plans

Run:

```powershell
node scripts/feishu_sync.cjs status --root exports/feishu-wiki
node scripts/feishu_sync.cjs plan --root exports/feishu-wiki
```

Pull:

```powershell
node scripts/feishu_sync.cjs pull --wiki-token "<wiki_token>" --base-url https://your-tenant.feishu.cn --root exports/feishu-wiki
```

Guarded push:

```powershell
node scripts/feishu_sync.cjs push --root exports/feishu-wiki
node scripts/feishu_sync.cjs push --root exports/feishu-wiki --apply
```

Git commits are intentionally not part of the sync command. Review the local workspace and commit separately.

Guarded push does not use Markdown overwrite when `format-map.json` contains rich format blocks. It first compiles supported Markdown edits into the `*.assets/*.format.xml` snapshot, then writes XML back to Feishu. If the Markdown and XML structures cannot be matched safely, it blocks and writes a conflict report.

### Export a wiki tree

Run:

```powershell
node scripts/export_feishu_wiki.cjs <wiki_token>
```

Or:

```powershell
node scripts/export_feishu_wiki.cjs <wiki_token> --base-url https://your-tenant.feishu.cn
```

Default output:

```text
exports/feishu-wiki/
```

The export workflow:

- saves each docx/wiki node as its own `index.md`
- downloads document images into `assets/` and places them inline in the Markdown body
- converts Feishu text-drawing add-ons into plain code blocks that preserve Mermaid text
- exports whiteboards via `code -> raw` fallback; when no code blocks are available, it stores raw node JSON, converts raw nodes into Mermaid mindmap text, and embeds the Mermaid directly into the Markdown body
- expands embedded sheet blocks into local `CSV` files plus Markdown table previews
- preserves top-level sheet nodes as `xlsx + csv + preview.md + README.md`
- stores export-level `tree.txt` and `codepen-links.md` in the root document `*.assets/` folder, with the export index appended to the root Markdown file; recognized legacy root-level sidecars are cleaned up on export
- writes `*.assets/*.format.xml`, `*.assets/format-map.json`, and `sheet-format.json` where available so format-preserving sync can reason about base/local/remote state

### Partially update a document

Use `lark-cli docs` v2 for chapter, paragraph, and block-level updates. Start by locating a stable block id:

```powershell
lark-cli docs +fetch --api-version v2 --doc "<docx_url_or_token>" --scope outline --max-depth 3 --detail with-ids
lark-cli docs +fetch --api-version v2 --doc "<docx_url_or_token>" --scope section --start-block-id "<heading_block_id>" --detail with-ids
```

Then patch only the target block or text span:

```powershell
node scripts/patch_feishu_doc.cjs --doc "<docx_url_or_token>" --command block_replace --block-id "<block_id>" --content "@.\section.xml"
```

For Markdown-first edits, use `str_replace` with the v2 Markdown ellipsis matcher:

```powershell
node scripts/patch_feishu_doc.cjs --doc "<docx_url_or_token>" --command str_replace --doc-format markdown --pattern "## 旧章节...旧章节结尾" --content "@.\section.md"
```

Add `--dry-run` before risky writes to inspect the generated request without updating Feishu.

Recommended decision path:

- For every document modification, first try chapter/paragraph/block-level update with `docs +fetch --api-version v2 --scope outline/section --detail with-ids`, then `scripts/patch_feishu_doc.cjs`.
- If the user provides a git unified diff (`.diff` / `.patch`) and a Feishu document link, use `scripts/merge_diff_to_feishu_doc.cjs`. It fetches the current Feishu Markdown, applies the diff locally, and then merges matched hunks with Markdown `str_replace` or EOF `append`.
- If a stable heading, paragraph, block id, or `start...end` text span can be identified, patch only that range.
- If the exported Markdown and target Feishu document are structurally incompatible enough that no reliable chapter/paragraph/block match exists, fall back to whole-document import with `scripts/import_feishu_markdown.cjs`.
- Existing whiteboard content: use `whiteboard +query/+update`, not `docs +update`.

### Merge a git diff into a Feishu doc

Run:

```powershell
node scripts/merge_diff_to_feishu_doc.cjs --doc "<docx_url_or_token>" --diff ".\changes.diff"
```

Safe preview:

```powershell
node scripts/merge_diff_to_feishu_doc.cjs --doc "<docx_url_or_token>" --diff ".\changes.diff" --dry-run --merged-output ".\merged-preview.md"
```

Write an explicit audit report:

```powershell
node scripts/merge_diff_to_feishu_doc.cjs --doc "<docx_url_or_token>" --diff ".\changes.diff" --audit-output ".\merge-audit.md"
```

Behavior:

- accepts standard unified diff files generated by `git diff`, `git show`, or PR patch exports
- fetches the current Feishu document as Markdown with `docs +fetch --api-version v2 --doc-format markdown`
- applies each hunk locally and writes `--merged-output` when requested
- updates Feishu hunk by hunk with `docs +update --api-version v2`; ordinary hunks use Markdown `str_replace`, and EOF append hunks use Markdown `append`
- stops if a hunk cannot be matched exactly in the current Feishu Markdown
- writes a Markdown audit report automatically on failed partial merge; use `--audit-output` to write an audit report for successful or dry-run merges too
- only uses whole-document overwrite when `--allow-overwrite-fallback` is explicitly provided
- does not delete the user-provided `.diff` file; successful non-dry-run merges clean script-generated `.tmp/feishu-diff-merged-*.md` files unless `--keep-temp` is passed

Audit report contents:

- merge status, strategy, target doc, diff file, matched/failed hunk counts
- failed hunk file path, hunk header, original line, expected old-text snippet
- ambiguity warnings when old text appears in multiple places
- suggestions such as refetching current Feishu Markdown, normalizing table/checklist/code-block formatting, shrinking the hunk, or using overwrite fallback only after review

Temporary file rule:

- `--dry-run --merged-output .\.tmp\...` keeps the preview for review
- a successful real merge removes generated merged-output files under `.tmp` by default
- pass `--keep-temp` to keep generated `.tmp` merge previews after a successful real merge
- input files such as `.diff`, `.patch`, and hand-written source Markdown are never deleted automatically

Fallback example:

```powershell
node scripts/merge_diff_to_feishu_doc.cjs --doc "<docx_url_or_token>" --diff ".\changes.diff" --allow-overwrite-fallback
```

### Audit round-trip safety

Run:

```powershell
node scripts/audit_feishu_export.cjs exports/feishu-wiki
```

This generates:

```text
exports/feishu-wiki/roundtrip-audit.md
```

Use the report to check:

- whether any image token placeholders remain
- whether embedded sheet blocks were expanded
- whether sheet roots have the expected `csv / preview / README` structure
- which content types are fully preserved versus text-only preserved

### Compile Markdown edits into format XML

Use this when local Markdown and `*.assets/*.format.xml` differ and the document contains rich blocks:

```powershell
node scripts/compile_feishu_doc_xml.cjs --markdown ".\doc.md" --format-xml ".\doc.assets\doc.format.xml" --check
node scripts/compile_feishu_doc_xml.cjs --markdown ".\doc.md" --format-xml ".\doc.assets\doc.format.xml" --out ".\.tmp\doc.compiled.xml"
```

Supported safe mappings: headings, paragraphs with bold text, callout text, checkbox text/done state, Markdown tables with unchanged row/column shape, and code fences. Unsupported structural changes must stop as conflicts.

### Re-import one Markdown file

Run:

```powershell
node scripts/import_feishu_markdown.cjs "<markdown_file>" "<docx_url_or_token>" "Optional Title"
```

The import workflow:

- is the fallback path when chapter/paragraph/block-level patching cannot be matched safely
- overwrites the target doc with the Markdown content
- converts CodePen links into Feishu `iframe` blocks
- keeps Mermaid as plain code blocks
- reinserts local images at the original Markdown position through `docs +media-insert --selection-with-ellipsis`
- reinserts standalone local non-Markdown file links as Feishu file blocks at the original Markdown position
- drops standalone local `CSV` links during import so embedded-sheet previews stay as inline tables only

### Manage one Drive-native Markdown file

Use this only for Drive files that are stored as plain `.md` files:

```powershell
node scripts/feishu_markdown_file.cjs create --file ".\note.md" --folder-token "<folder_token>" --dry-run
node scripts/feishu_markdown_file.cjs fetch --file-token "<markdown_file_token>" --output ".\note.md"
node scripts/feishu_markdown_file.cjs overwrite --file-token "<markdown_file_token>" --file ".\note.md" --dry-run
```

Boundary rule:

- `scripts/feishu_markdown_file.cjs` wraps `lark-cli markdown +create/+fetch/+overwrite` for Drive-native Markdown files.
- `scripts/export_feishu_wiki.cjs`, `scripts/import_feishu_markdown.cjs`, and `scripts/feishu_sync.cjs` remain the doc/wiki Markdown Sync path.
- Do not use `lark-cli markdown` to replace docx/wiki export, import, format snapshots, or guarded sync.

### Write back one Sheet range

Run:

```powershell
node scripts/import_feishu_sheet.cjs --url "<sheet_url>" --sheet-id "<sheet_id>" --range "A2:C3" --input ".\changes.csv"
```

Or:

```powershell
node scripts/import_feishu_sheet.cjs --spreadsheet-token "<spreadsheet_token>" --sheet-id "<sheet_id>" --range "A:C" --mode append --values '[[2026,"追加","ok"]]'
```

Rules:

- `--range` is required; implicit whole-sheet write-back is forbidden.
- Input can be CSV or a JSON 2D array.
- `write` overwrites the target range, and `append` appends rows to the requested range.
- Non-dry-run writes must read back the target range and verify written values.

## Sheet Output Convention

For root sheet nodes, keep this Git-friendly structure:

```text
sheet-node/
  README.md
  index.md
  <workbook>.xlsx
  <sheet-name>.preview.md
  csv/
    <sheet-name>.csv
```

Use:

- `README.md` for navigation
- `csv/*.csv` for Git diffs and downstream processing
- `*.preview.md` for quick reading without leaving Markdown

## Important Constraints

- Feishu text-drawing `add-ons` are not live round-trippable in the 2026-05-10 cloud validation. Preserve them as text/Mermaid code blocks in wiki exports and use whiteboards for live text drawing.
- Whiteboards are exported with automatic `code -> raw` fallback. Non-code whiteboards are preserved as `Mermaid in Markdown + raw JSON sidecar`. To update a live whiteboard, query the token and call `lark-cli whiteboard +update --input_format mermaid|plantuml|raw`.
- Raw JSON is audit-only; exported resources should have a Markdown preview whenever possible.
- Same-document anchor jumps are not reliable in Feishu imports. Do not depend on Markdown `#anchor` links surviving import.
- This skill assumes `lark-cli >= 1.0.39`, because document v2 partial fetch/update, Sheet export/write/append/read, Drive-native Markdown files, current whiteboard update flows, and recent CLI shortcut improvements are part of the optimization path.
- Local Markdown links are still downgraded to readable text paths.
- Standalone local `CSV` links are intentionally removed during import. The inline Markdown table preview is kept as the Feishu-side representation.
- Sheet write-back uses `scripts/import_feishu_sheet.cjs`; do not route CSV write-back through Markdown document import.
- Only standalone local non-Markdown, non-CSV files are reinserted as Feishu file blocks.
- Asset filenames use token-derived MD5 suffixes by default instead of raw token fragments.
- Import temporary Markdown files are deleted automatically after the run completes.

## Typical Workflow

### Export and inspect

```powershell
node scripts/export_feishu_wiki.cjs <wiki_token> --base-url https://your-tenant.feishu.cn
node scripts/audit_feishu_export.cjs exports/feishu-wiki
```

### Re-import one document for verification

```powershell
node scripts/import_feishu_markdown.cjs ".\exports\feishu-wiki\<wiki_token>\...\index.md" "https://your-tenant.feishu.cn/docx/exampleDocToken" "Roundtrip Test"
```

### Patch one section or paragraph

```powershell
lark-cli docs +fetch --api-version v2 --doc "https://your-tenant.feishu.cn/docx/exampleDocToken" --scope outline --max-depth 3 --detail with-ids
node scripts/patch_feishu_doc.cjs --doc "https://your-tenant.feishu.cn/docx/exampleDocToken" --command block_insert_after --block-id "<heading_or_paragraph_block_id>" --content "@.\new-section.xml"
```

### Merge a git diff into one document

```powershell
node scripts/merge_diff_to_feishu_doc.cjs --doc "https://your-tenant.feishu.cn/docx/exampleDocToken" --diff ".\changes.diff" --dry-run --merged-output ".\merged-preview.md"
node scripts/merge_diff_to_feishu_doc.cjs --doc "https://your-tenant.feishu.cn/docx/exampleDocToken" --diff ".\changes.diff"
```

### Update a live whiteboard from Mermaid

```powershell
node scripts/feishu_text_diagram.cjs whiteboard query --whiteboard-token "<whiteboard_token>" --output-as code --as user
node scripts/feishu_text_diagram.cjs whiteboard update --whiteboard-token "<whiteboard_token>" --source "@.\diagram.mmd" --input-format mermaid --overwrite
```

The overwrite update dry-runs by default. Add `--apply` only after reviewing the request.

### Verify doc add-ons text drawing experimentally

```powershell
node scripts/feishu_text_diagram.cjs doc-addons-verify --doc "https://your-tenant.feishu.cn/docx/exampleDocToken" --dry-run
```

This command reports `supportStatus`. Treat doc v2 `<add-ons>` as unsupported unless it returns `supportStatus: "cloud-verified"` and `addOnsPreservedInFetchedXml: true`.

## Scripts

- `scripts/export_feishu_wiki.cjs`
  Export the Feishu wiki tree and normalize docx and sheet content into local files.
- `scripts/feishu_sync.cjs`
  Inspect, pull, plan, refresh, and guarded-push manifest-backed sync workspaces.
- `scripts/compile_feishu_doc_xml.cjs`
  Merge human-edited Markdown text into a format XML snapshot before rich-format XML write-back.
- `scripts/audit_feishu_export.cjs`
  Summarize round-trip fidelity and remaining risks.
- `scripts/import_feishu_markdown.cjs`
  Push one Markdown file back into a Feishu doc with inline image and file block placement.
- `scripts/import_feishu_sheet.cjs`
  Write CSV or JSON 2D array data back into an explicit Feishu Sheet range, then verify by read-back.
- `scripts/feishu_markdown_file.cjs`
  Create, fetch, and overwrite Drive-native Markdown files without using the doc/wiki sync path.
- `scripts/feishu_cli_tools.cjs`
  Expose guarded wrappers for lark-cli v1.0.24-v1.0.39 sidecar capabilities.
- `scripts/feishu_text_diagram.cjs`
  Update whiteboards from Mermaid/PlantUML and run experimental doc add-ons verification.
- `scripts/patch_feishu_doc.cjs`
  Apply a focused `docs +update --api-version v2` operation such as `str_replace`, `block_replace`, or `block_insert_after`.
- `scripts/merge_diff_to_feishu_doc.cjs`
  Merge a git unified diff into a Feishu doc by fetching Markdown, applying hunks locally, and updating matched hunks with v2 Markdown `str_replace`.

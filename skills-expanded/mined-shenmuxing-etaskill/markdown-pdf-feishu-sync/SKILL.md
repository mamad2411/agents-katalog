---
name: markdown-pdf-feishu-sync
description: Convert configured local Markdown collections to PDFs and upload the generated PDFs to Feishu/Lark Drive. Use when Codex needs to run or maintain a recurring local Markdown-to-PDF publishing workflow, inspect a private rules file, dry-run source/category mappings, invoke an external open-source Markdown PDF converter, or upload generated PDFs to a Feishu Drive folder.
---

# Markdown PDF Feishu Sync

## Overview

Use this skill to execute a private, rules-driven workflow:

1. Read a local rules file outside public source control.
2. Discover Markdown files from configured source directories.
3. Convert each Markdown file to PDF with the configured converter command.
4. Upload generated PDFs to configured Feishu Drive folders.
5. Write a manifest for audit and the next recurring run.

Keep repository files public-safe. Do not commit private local paths, Feishu folder tokens, collaborator names, account names, converter install paths, generated PDFs, or run logs. Store those details under a local ignored directory such as `local/markdown-pdf-feishu-sync/`.

## Decision Persistence

Treat user choices about which files to sync, target subfolders, sharing recipients, and one-off category mappings as run-local by default. Do not write those choices into the skill, long-lived rules, or automation memory unless the user explicitly says to record them in rules or future runs.

Only persist workflow-level policies that are meant to change how the sync operates in general. Keep concrete file lists, personal paths, collaborator names, folder tokens, and upload decisions in ignored local runtime artifacts or the current run output.

## Quick Start

Use `scripts/sync_markdown_pdfs.py` from the repository root:

```powershell
python .\skill-examples\markdown-pdf-feishu-sync\scripts\sync_markdown_pdfs.py --rules .\local\markdown-pdf-feishu-sync\rules.json --dry-run
```

Run conversion after the dry-run plan is correct:

```powershell
python .\skill-examples\markdown-pdf-feishu-sync\scripts\sync_markdown_pdfs.py --rules .\local\markdown-pdf-feishu-sync\rules.json --convert
```

Upload only after Feishu target folders and permissions have been confirmed:

```powershell
python .\skill-examples\markdown-pdf-feishu-sync\scripts\sync_markdown_pdfs.py --rules .\local\markdown-pdf-feishu-sync\rules.json --convert --upload
```

## Rules File

Read `references/local-rules-schema.md` before changing the local rules file. The rules file owns:

- Source directories and include/exclude patterns.
- Category names and per-category target folder tokens.
- The Markdown-to-PDF converter command.
- Feishu identity choice (`bot` or `user`).
- Share policy notes and explicit pending decisions.
- Output and manifest paths.

If a source directory is still unknown, leave it out of `sources` and record it under `pending_decisions`. Do not invent broad roots such as a home directory or drive root.

## Workflow

1. Inspect the local rules file.
   - If it does not exist, create it from the schema with no source directories and the known Feishu target folder token.
   - Keep any unknown details in `pending_decisions`.
2. Run `--dry-run`.
   - Check discovered file counts, category mapping, output paths, and upload targets.
   - Fix rules before converting.
3. Run `--convert`.
   - The script invokes the configured converter once per Markdown file.
   - For converters such as `md-to-pdf` that write beside their input, prefer `{staged_input}` so the script converts a temporary Markdown copy in the PDF output directory instead of writing artifacts next to the source note.
   - Treat converter failures as blocking for that file; do not upload stale PDFs.
4. Run `--upload` only when the user has confirmed the target folder and write intent.
   - The script uses `lark-cli drive +upload`.
   - Respect `lark-cli` authentication and `--as` identity rules.
   - Stop on permission errors and report the exact failing target.
5. Review the manifest.
   - Use it to summarize created PDFs, skipped files, failed conversions, and uploaded files.

## Feishu Notes

- For PDF files, use `lark-cli drive +upload`, not `drive +import`.
- `lark-cli` file path arguments must be relative to the command working directory. The bundled script runs uploads from the PDF output root and passes relative PDF paths.
- Prefer category-specific folder tokens once they are known. Until then, upload to the configured root folder only if the user accepts a flat or prefixed layout.
- Do not create folders, alter permissions, transfer ownership, or delete remote files unless the user explicitly confirms that operation.
- If a permission or scope error appears, follow the local `lark-shared` and `lark-drive` skills before retrying.

## Safety

- Default to `--dry-run`.
- Do not scan a directory unless it is explicitly listed in the local rules file.
- Do not overwrite remote files unless a rule explicitly maps a local artifact to an existing `file_token`.
- Do not treat the recurring automation as authorization to expand scope. The automation may process only confirmed rules.

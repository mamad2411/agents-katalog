---
name: workspace-organizer
description: 'Workspace file organization and cleanup planning. Use when the user asks to organize a folder, clean a workspace, group files by type or project, deduplicate generated files, prepare a tidy deliverable folder, or explain what can safely be deleted.'
---

# Workspace Organizer

Use this skill when a task is about organizing, cleaning, or restructuring files inside the selected workspace.

## Safety Contract

- Stay inside the user-selected workspace.
- Do not delete files by default. Prefer a proposed plan, a `cleanup-plan.md`, or moving files to a clearly named review folder.
- Never move source code, dotfiles, lockfiles, config files, or hidden control folders such as `.git`, `.codebuddy`, `.claude`, `.venv`, `node_modules`, `dist`, `build`, or `release` unless the user explicitly asks for that exact scope.
- Preserve original filenames unless a rename is necessary and reversible.
- Record every move, rename, merge, or deletion candidate in a manifest.
- If duplicates are suspected, compare size and content hash before treating files as duplicates.

## Workflow

1. Inventory the workspace with names, extensions, sizes, and modified times.
2. Identify protected areas before proposing any action.
3. Group files by purpose, not only by extension:
   - source documents
   - generated deliverables
   - screenshots or media evidence
   - exports
   - logs and temporary files
   - archives
4. Propose the target folder layout and list risky operations separately.
5. Execute only low-risk moves automatically, and keep destructive actions as review candidates unless explicitly approved.
6. Write or update `organization-manifest.md` with the before/after map and skipped items.

## Output Pattern

When the user asks for cleanup, provide:

- A short summary of the current mess.
- The proposed folder layout.
- The exact safe moves completed.
- The deletion candidates left for review.
- The path to the manifest.

## Folder Layout Heuristics

- `source/` for user-provided inputs.
- `deliverables/` for final generated files.
- `evidence/` for screenshots, recordings, logs, and validation artifacts.
- `working/` for intermediate files that may be needed to reproduce a result.
- `archive/` for old outputs that should be retained but not kept in the active workspace root.

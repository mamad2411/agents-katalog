---
name: index-docs
description: Use when building or refreshing navigable INDEX.md files across a document corpus so agentic workflows can discover and navigate documents without reading every file.
---

# Index Docs

## Specialization

Scan a document corpus and produce a hierarchical set of `INDEX.md` files that enable agentic navigation without reading individual files. One index per folder.

This skill has one purpose: building navigable corpus indexes.

## Index File Format

Each `INDEX.md` is placed at the root of its folder and follows this structure:

```markdown
# Index: <folder-name>

> Corpus index. Do not edit manually — refresh with this skill.

## Subfolders

| Folder | Description |
|---|---|
| subfolder/INDEX.md | One-line description of subfolder scope. |

## Documents

| File | Title | Category | Summary |
|---|---|---|---|
| filename.md | Title from H1 | category | One-line summary. |
```

**Field rules:**

| Field | Source | Rules |
|---|---|---|
| File | Relative path | Verbatim, no escaping. |
| Title | First H1 in file | Fall back to kebab-case filename if no H1. |
| Category | Content inference | Use: `plan`, `research`, `reference`, `change`, `adr`, `spec`, `index`, `other`. |
| Summary | First non-heading paragraph | Truncate to 120 characters. Omit if file has no readable prose. |

## Workflow

1. Receive target root path (default: workspace root).
2. Walk the directory tree depth-first.
3. For each folder:
   a. Collect all `.md` files (exclude `INDEX.md` itself).
   b. Extract `Title`, `Category`, and `Summary` for each file.
   c. List immediate sub-folders that contain documents.
   d. Write or overwrite `INDEX.md` for that folder.
4. Start at the deepest folders and work upward so parent indexes can reference child indexes accurately.
5. At the workspace root (or target root), produce a top-level `INDEX.md` that links all immediate sub-folder indexes.

## Refresh Rules

- Overwrite existing `INDEX.md` files on each refresh run.
- Preserve any manually authored sections marked with `<!-- preserve -->` comment blocks.
- Never index files excluded by a `.librarianignore` file in the folder (if present).
- Never create root-level folders in any workspace.
- Never create top-level reference folders; keep references under owning asset paths.

## `.librarianignore` Support

If a folder contains a `.librarianignore` file, exclude paths matching its patterns from the index. Format is one glob pattern per line (same syntax as `.gitignore`).

## Integration with this skill

- This skill can run after any curation pass to refresh index files.
- Can also be run independently to refresh stale indexes without triggering full curation.

## Trigger Conditions

Invoke this skill when any of the following is true:

- A document corpus needs a navigable index for agentic workflows.
- Existing `INDEX.md` files are stale after documents were added, moved, or renamed.
- Index refresh is required as part of documentation curation output contracts.
- A new workspace is being structured and initial indexes are required.

## Inputs

- Root path to scan (required).
- Optional: max depth override (default: unlimited).
- Optional: list of folders to exclude.

## Required Outputs

- One `INDEX.md` per folder that contains at least one `.md` file.
- A summary report: total folders indexed, total files indexed, any files skipped and why.
- Confirmation line: "Index refresh complete. X folders, Y documents indexed."

## Done Criteria

This skill is complete when:

- Every folder in the target corpus has an up-to-date `INDEX.md`.
- The top-level index links all sub-folder indexes.
- A summary count is reported to the user.


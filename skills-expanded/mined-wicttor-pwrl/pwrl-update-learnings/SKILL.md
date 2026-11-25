---
name: pwrl-update-learnings
description: Update docs/learnings/INDEX.md from current learning documents, typically after pwrl-end-session.
argument-hint: "[Optional: scope such as changed-only, full, or category]"
---

# PWRL Update Learnings

Keep `docs/learnings/INDEX.md` synchronized with the current learning documents.

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "Should the learnings index be updated? Default is to sync recently changed learnings only."
- Provide clear recovery suggestions when errors occur

## Purpose

This skill ensures every learning document is represented in the index with a short description.

- Keeps `docs/learnings/INDEX.md` accurate and searchable
- Prevents stale, missing, or duplicate index rows
- Runs after `/pwrl-end-session` automatically, or manually on demand

## Usage

```bash
/pwrl-update-learnings
/pwrl-update-learnings full
/pwrl-update-learnings changed-only
/pwrl-update-learnings technical-fix
```

## Inputs

Optional scope:

- `changed-only` - prioritize learnings touched in the latest commit/session
- `full` - rebuild index from all learning files
- category name - sync only one category folder
- blank - default to `changed-only`, fallback to `full` if no commit context

## Workflow

### 1. Collect Candidate Learning Files

1. Read `docs/learnings/INDEX.md` if it exists.
2. Enumerate learning files in category folders:
   - `docs/learnings/technical-fix/`
   - `docs/learnings/pattern/`
   - `docs/learnings/workflow/`
   - `docs/learnings/gotcha/`
   - `docs/learnings/concept/`
   - `docs/learnings/decision/`
3. Exclude `docs/learnings/INDEX.md` and archive docs unless user explicitly asks to include them.

### 2. Extract Metadata

For each learning file, extract:

- Date (from frontmatter `date` if available, otherwise from filename suffix)
- Category (frontmatter `category` or folder name)
- Title (frontmatter `title` or first H1)
- Path (repository-relative path)
- Short description:
  - Prefer an explicit summary/overview sentence if present
  - Otherwise derive one concrete sentence from the first meaningful paragraph
  - Keep concise and searchable (target 80-140 chars)

### 3. Reconcile Index Rows

1. Ensure exactly one row per active learning file.
2. Add missing rows.
3. Update changed title/date/category/path/description values.
4. Remove rows for files that no longer exist (or mark archived when applicable).
5. Remove placeholder row (`_none_`) when at least one real entry exists.

### 4. Normalize Output

1. Sort rows newest-first by date.
2. Keep table columns exactly:
   - Date | Category | Title | Path | Short Description
3. Preserve `# Learnings Index`, rules section, and table header.

### 5. Report Result

Provide a compact summary:

- Added rows: N
- Updated rows: N
- Removed/archived rows: N
- Total indexed learnings: N
- Scope used: changed-only/full/category

## Automatic Trigger from pwrl-end-session

When invoked by `/pwrl-end-session`, run this skill immediately after commit creation.

- If commit succeeds, sync index and include result in final session summary.
- If commit fails or is canceled, skip automatic sync.
- If automatic chaining is unavailable in the host assistant, instruct to run `/pwrl-update-learnings` manually.

## Acceptance Criteria

- `docs/learnings/INDEX.md` exists and is valid markdown table format
- Every active learning has one index row with a short description
- Rows are sorted newest-first
- Session-end flow can call this skill automatically (or provides explicit manual fallback)

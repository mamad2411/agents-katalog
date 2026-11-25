---
name: codebase-teach
description: >
  Analyzes project bounded contexts, extracts business rules and domain knowledge,
  writes ai-context/features/<context>.md files, and produces a teach-report.md
  with documentation coverage metrics.
  Trigger: /codebase-teach, teach codebase, extract domain knowledge, update feature docs.
format: procedural
---

# codebase-teach

> Analyzes bounded contexts from the project's source tree, extracts domain knowledge per context, writes `ai-context/features/<context>.md` files, and produces `teach-report.md` with coverage metrics.

**Triggers**: `/codebase-teach`, teach codebase, extract domain knowledge, update feature docs, analyze bounded contexts

---

## Purpose

`codebase-teach` fills the `ai-context/features/` layer with structured domain knowledge derived from reading source code. It is the deep-read complement to `memory-update` (which records session decisions) and `memory-init` (which scaffolds empty stubs). It MUST only be invoked manually by the user.

---

## Process

### Step 0 — Load project context (non-blocking)

This step is **non-blocking**: any failure (missing file, unreadable file) MUST produce at most an INFO-level note. This step MUST NOT produce `status: blocked` or `status: failed`.

1. Read `ai-context/stack.md` — tech stack, versions, key tools.
2. Read `ai-context/architecture.md` — architectural decisions and rationale.
3. Read `ai-context/conventions.md` — naming patterns, code conventions.
4. Read the project's `CLAUDE.md` (at project root) and extract the `## Skills Registry` section.

For each file:
- If absent: log `INFO: [filename] not found — proceeding without it.`
- If present: extract `Last updated:` or `Last analyzed:` date. If date is older than 30 days: log `NOTE: [filename] last updated [date] — context may be stale. Consider running /memory-update or /project-analyze.`

Also read `openspec/config.yaml` and extract `teach_max_files_per_context` if present:
- If present: `max_files = teach_max_files_per_context`
- If absent: `max_files = 10` (default)

Log: `"File cap per context: [max_files] (source: openspec/config.yaml)"` or `"File cap per context: 10 (default)"`

---

### Step 1 — Scan bounded contexts

Identify bounded context candidates by scanning the project directory tree at depth ≤ 2 under these root directories (in order):

1. `src/` — subdirectories at depth 1 (e.g., `src/auth/`, `src/payments/`)
2. `app/` — subdirectories at depth 1
3. `features/` — subdirectories at depth 1
4. `domain/` — subdirectories at depth 1
5. `openspec/specs/` — subdirectory names (each subdirectory is treated as a context name)

**Exclusion rules** — skip directories named: `shared`, `utils`, `common`, `lib`, `types`, `hooks`, `components`, `__tests__`, `test`, `tests`, `node_modules`, `.git`

**Cross-reference with existing feature files:**
Read the `ai-context/features/` directory (if it exists) and list all `.md` files, excluding files whose names begin with `_` (e.g., `_template.md`).

For each detected context candidate, build a record:
```
{ slug: kebab-case of directory name, dir_path, existing_feature_file: bool }
```

**Slug convention:** lowercase the directory name; replace spaces and underscores with hyphens. Example: `UserProfile` → `user-profile`, `auth_service` → `auth-service`.

**If no context candidates are found:**
- Log: `"No bounded context directories detected."`
- Write `teach-report.md` with a Summary noting "No bounded context directories detected" and a recommendation to run `/memory-init` first.
- Stop here.

**If `ai-context/features/` does not exist:**
- Log: `"INFO: ai-context/features/ not found — feature files will be created if possible."`
- Note in `teach-report.md`: "ai-context/features/ was absent at run time. Recommend running /memory-init to scaffold the directory before re-running /codebase-teach."
- Continue processing (the skill creates the directory and files as needed).

Output: `context_list = [{ slug, dir_path, existing_feature_file: bool }, ...]`

Log each context found: `"Detected context: [slug] — [dir_path] (feature file: [exists|absent])"`

---

### Step 2 — Read key files per context (sequential)

Process contexts **one at a time**. For each context in `context_list`:

1. **Enumerate implementation files** in `dir_path` (recursive), filtering for file extensions: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.java`, `.kt`, `.rb`, `.go`, `.ex`, `.exs`, `.cs`, `.rs`, `.php`, `.swift`
   - Prioritize files by recency (most recently modified first)
   - Exclude files matching: `*.test.*`, `*.spec.*`, `test_*`, `*_test.*`, `*.d.ts`, `*.min.*`

2. **Apply file cap:** read at most `max_files` files. If total enumerated > `max_files`, log: `"[slug]: [total] files found — sampling [max_files] (cap applied)"`

3. **For each file to read:**
   - Attempt to read the file
   - If the file is binary or unreadable: skip it; record in `skipped_files` with reason
   - If readable: extract the following signals:
     - **Business rules**: explicit conditional constraints (if/when/unless logic that enforces domain rules)
     - **Invariants**: assertions or validation guards that are always enforced
     - **Data model entities**: class/struct/interface/type names with their key fields
     - **Integration points**: imports of external services, APIs, or infrastructure adapters

4. Accumulate: `context_knowledge = { slug, rules[], invariants[], entities[], integrations[], files_read[], skipped[] }`

---

### Step 3 — Write `ai-context/features/<slug>.md`

For each context processed in Step 2:

**If `ai-context/features/<slug>.md` does not exist** (or `ai-context/features/` is absent):
- Create the directory if needed
- Write a new file using the six-section structure below
- All AI-generated sections receive `[auto-updated]` markers

**If `ai-context/features/<slug>.md` already exists:**
- Read the entire file
- Identify `<!-- [auto-updated]: codebase-teach ... -->` ... `<!-- [/auto-updated] -->` blocks
- Overwrite content **only** inside `[auto-updated]` blocks
- Preserve byte-for-byte all content outside any `[auto-updated]` block
- If no `[auto-updated]` block exists for a section, append the section at the end of the file inside a new `[auto-updated]` block

**Six-section feature file structure:**

```markdown
# [Context Name] — Domain Knowledge

Last updated by: codebase-teach
Last run: YYYY-MM-DD

---

## Domain Overview

<!-- [auto-updated]: codebase-teach — last run: YYYY-MM-DD -->
[AI-extracted 2–4 sentence summary of what this bounded context does and its primary responsibilities]
<!-- [/auto-updated] -->

---

## Business Rules and Invariants

<!-- [auto-updated]: codebase-teach — last run: YYYY-MM-DD -->
[AI-extracted explicit conditional constraints and always-true invariants from the source]

- Rule: [description]
- Invariant: [description]
<!-- [/auto-updated] -->

---

## Data Model Summary

<!-- [auto-updated]: codebase-teach — last run: YYYY-MM-DD -->
Key entities detected:

| Entity | Key Fields |
|--------|-----------|
| [Name] | [field1, field2, ...] |
<!-- [/auto-updated] -->

---

## Integration Points

<!-- [auto-updated]: codebase-teach — last run: YYYY-MM-DD -->
External dependencies and integration touchpoints:

- [service/API name]: [what it is used for]
<!-- [/auto-updated] -->

---

## Decision Log

<!-- [auto-updated]: codebase-teach — last run: YYYY-MM-DD -->
<!-- Append new AI-detected decisions below. Human entries above this marker are preserved. -->
<!-- [/auto-updated] -->

---

## Known Gotchas

<!-- [auto-updated]: codebase-teach — last run: YYYY-MM-DD -->
<!-- Append new AI-detected gotchas below. Human entries above this marker are preserved. -->
<!-- [/auto-updated] -->
```

**`_template.md` guard:** never read, write, or treat any file whose name begins with `_` as a feature context. Skip entirely.

---

### Step 4 — Evaluate coverage and write `teach-report.md`

**Coverage calculation:**
```
documented_contexts = count of contexts that have an ai-context/features/<slug>.md file after Step 3
total_contexts      = count of contexts in context_list
coverage_pct        = (documented_contexts / total_contexts) * 100   (0 if total_contexts == 0)
gap_list            = contexts in context_list where existing_feature_file was false before Step 3
                      AND no file was created in Step 3
```

**Write `teach-report.md`** in the project working directory root (same level as `analysis-report.md`). Overwrite if it exists.

```markdown
# Teach Report — [Project Name]

Last run: YYYY-MM-DD
Skill: codebase-teach

## Summary

Contexts detected: [total_contexts]
Contexts documented: [documented_contexts]
Coverage: [coverage_pct]%

## Coverage

[coverage_pct]% — [documented_contexts] of [total_contexts] contexts documented.

## Gaps

Contexts detected in code but not documented in ai-context/features/:

- [context-slug] — [dir_path]

[If no gaps: "None — all detected contexts are documented."]

## Files Read

### [context-slug]
- [file path] — sampled
- [file path] — sampled
- [file path] — SKIPPED: [reason]

[Repeat for each context]

## Sections Written / Updated

- ai-context/features/[context].md — [created|updated] — sections: [list of sections written]
```

If `ai-context/features/` was absent at run time, append to the Summary section:

> Note: ai-context/features/ was absent at run time. Recommend running /memory-init to scaffold the directory before re-running /codebase-teach.

---

## Rules

- MUST NOT modify `ai-context/stack.md`, `ai-context/architecture.md`, `ai-context/conventions.md`, `ai-context/known-issues.md`, or `ai-context/changelog-ai.md`
- MUST NOT modify any file under `openspec/` or `docs/`
- MUST NOT be invoked automatically by any other skill — user-initiated only
- MUST skip any file or directory whose name begins with `_` in `ai-context/features/`
- MUST preserve all human-authored content outside `[auto-updated]` markers when updating existing feature files
- MUST process contexts sequentially — never in parallel
- MUST apply the `teach_max_files_per_context` cap (default 10) to every context
- MUST list skipped files in `teach-report.md` under the "Files Read" section for the relevant context
- MUST complete without error even when no bounded context directories are detected
- MUST write `teach-report.md` on every successful run
- `[auto-updated]` marker format: `<!-- [auto-updated]: codebase-teach — last run: YYYY-MM-DD -->` ... `<!-- [/auto-updated] -->` — consistent with `project-analyze` convention

---

## Output

### `teach-report.md` (mandatory — written to project root on every run)

Required sections:

| Section | Content |
|---------|---------|
| Summary | Contexts detected, documented, coverage % |
| Coverage | Percentage and ratio |
| Gaps | Contexts found in code but undocumented (or "None") |
| Files Read | Per-context list of files sampled and skipped |
| Sections Written / Updated | Per-feature-file: created or updated, which sections |

### `ai-context/features/<context>.md` (one per bounded context)

Written or updated during Step 3. Six sections with `[auto-updated]` markers on all AI-generated content.

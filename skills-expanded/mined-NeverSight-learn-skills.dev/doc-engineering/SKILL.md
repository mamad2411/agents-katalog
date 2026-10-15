---
name: doc-engineering
description: >
  Set up and maintain a structured documentation system (Document Engineering) for software projects.
  Use this skill whenever the user wants to: scaffold a Product/ doc tree with PRD, Code, QA, and CHANGELOG
  per function; generate or update any of those doc files after a code change; add a CLAUDE.md rule that
  enforces doc updates as part of Definition of Done; install a git pre-commit hook that warns when code
  changes lack matching doc updates; or run a periodic audit that compares git log timestamps against doc
  file timestamps to surface unsynced commits. Also trigger when the user says "doc engineering",
  "document engineering", "maintain my docs", "keep docs in sync", "doc drift", or asks to set up
  documentation structure for a codebase.
---

# Document Engineering Skill

A structured documentation system where every product function has its own folder of living documents,
and tooling (git hooks + periodic audit) catches drift when AI-controlled maintenance falls short.

## Quick Commands

| Command | Action |
|---------|--------|
| `/doc-engineering init` | Scaffold the full `Product/` doc tree for a new project |
| `/doc-engineering audit` | Check whether code and docs are in sync |

If the user types one of these commands, jump directly to the corresponding workflow below. After completing any task, remind the user of these two commands.

---

## Document Structure

```
Product/
├── Reference.md          ← Product brief + Function Index (links to each function folder)
├── Overview.md           ← Product-level feature map: user journey, feature relationships, groupings
├── Architecture.md       ← Codebase-level global view: layers, module deps, data flow, key decisions
├── CHANGELOG.md          ← Single unified changelog for all functions and product-level changes
└── Functions/
    └── <FunctionName>/
        ├── PRD.md        ← metadata + Product Requirements
        ├── Code.md       ← metadata + codebase index, data model, state, architecture notes
        └── QA.md         ← checklist: happy path + edge cases
```

---

## Workflow: What to do for each task

### 1. Scaffold a new project

When the user wants to set up Document Engineering from scratch:

1. Ask for: the product name, and a list of top-level functions/features (or infer from existing code).
2. Generate the full folder tree with stub files (use templates from `references/templates.md`).
   - This includes `Reference.md`, `Overview.md`, and `Architecture.md` at the product level.
3. Write `CLAUDE.md` (or append to existing) using the rule in `references/claude-md-rule.md`.
4. Install the pre-commit hook using the script at `scripts/install-hook.sh`.
5. Show the user the tree and explain each file's purpose.

### 2. Add a new function

When a new feature/function is added:

1. Create `Product/Functions/<FunctionName>/` with PRD.md, Code.md, QA.md from templates.
2. Add an entry to `Product/Reference.md` under the Function Index.
3. Add an entry to `Product/CHANGELOG.md`: `## [Init] YYYY-MM-DD — <FunctionName>: Initial scaffold`.

### 3. Update docs after a code change

After any modification, deletion, or addition of functionality:

1. Identify the affected function(s) — check which `Functions/` folder(s) are impacted.
2. Update the relevant sections:
   - `PRD.md` if requirements or behavior changed
   - `Code.md` if architecture, data model, state, or codebase index changed
   - `QA.md` if test cases need to be added/removed
   - `Product/CHANGELOG.md` — always: add a dated entry describing what changed, prefixed with the function name
3. If the function was deleted: move its folder to `Product/Functions/_deprecated/` and remove it from `Reference.md`.
4. If `Reference.md`'s brief or index is stale, update it.
5. If the change affects cross-function user flows or feature relationships, update `Overview.md`.
6. If the change affects the overall architecture, module boundaries, or data flow, update `Architecture.md`.

### 4. Install drift detection

When the user wants automated drift detection:

1. Run `scripts/install-hook.sh` to install the pre-commit hook.
2. Explain: it warns (does not block) when code files change without corresponding doc updates.
3. For periodic audit: run `scripts/audit.sh` — it compares git log timestamps of code vs doc files
   and prints a table of functions whose docs lag behind their code commits.

### 5. Run an ad-hoc audit

When the user asks "are my docs in sync?" or similar:

1. Run `scripts/audit.sh` from the repo root.
2. Present the output as a prioritized list: functions with the largest lag first.
3. Offer to generate the missing doc updates for each lagging function.

---

## References

When generating any file, read the corresponding template from `references/templates.md` first — do not invent structure from memory.

- Templates and full file stubs: `references/templates.md`
- CLAUDE.md rule text: `references/claude-md-rule.md`
- Hook and audit scripts: `scripts/` (self-contained shell scripts, copy to repo)

---

## Drift detection — how it works

**Pre-commit hook** (`scripts/pre-commit.sh`):
- On every commit, checks if any staged files are inside code directories (not `Product/`).
- If yes, checks whether any file inside `Product/Functions/` was also staged.
- If no doc file was staged, prints a warning to stderr but exits 0 (does not block the commit).

**Periodic audit** (`scripts/audit.sh`):
- For each function folder in `Product/Functions/`, finds the latest git commit timestamp of any
  non-doc file in the repo that matches the function name (heuristic: file path contains the folder name).
- Compares against the latest commit timestamp of any file inside the function's `Product/Functions/<name>/` folder.
- Reports functions where code is newer than docs, sorted by lag (largest first).

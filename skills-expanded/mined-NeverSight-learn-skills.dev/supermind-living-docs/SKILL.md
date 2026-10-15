---
name: supermind-living-docs
description: "Manually sync living documentation. Use when ARCHITECTURE.md or DESIGN.md need updating after code changes, when the user asks to update docs, or as a periodic check. Does not auto-trigger — this is the manual 'sync now' command."
---

# Living Documentation — Manual Sync

Surgical edits preserve your existing formatting and avoid unnecessary diffs. This skill updates ARCHITECTURE.md and DESIGN.md to reflect the current state of the codebase without rewriting entire files.

---

## Steps

1. **Read current documentation**:
   - Read `ARCHITECTURE.md` from the project root (required — if missing, tell the user to run `/supermind-init` first)
   - Read `DESIGN.md` from the project root (only if it exists — its presence means this is a UI project)

2. **Assess recent changes**:
   - Run `git diff --name-only` for unstaged changes
   - Run `git diff --name-only --cached` for staged changes
   - Run `git status --short` for untracked files
   - Run `git diff --stat` to understand the scope of changes
   - Combine all lists into the set of changed files for subsequent steps

3. **Reason about what needs updating**:
   - Files added, removed, or renamed — update **File Index**
   - API routes changed — update **API Contracts**
   - Dependencies added or removed — update **Tech Stack** and **Dependencies & Data Flow**
   - Environment variables changed — update **Environment Variables**
   - New patterns or conventions established — update **Key Patterns & Conventions**
   - UI changes (only if DESIGN.md exists):
     - Colors, fonts, spacing changed — update relevant design sections
     - Components added or modified — update **Component Patterns**
     - Layout or animation changes — update **Layout Conventions** or **Animation Patterns**

4. **Validate existing claims against changed files**:
   - Using the full list of changed files from step 2:
     a. For each changed file, check if ARCHITECTURE.md (or DESIGN.md) makes specific claims about that file's behavior, constants, patterns, or dependencies
     b. For deleted files: remove or update any documentation entries that reference them
     c. For modified files: verify claims are still accurate by reading the actual source
     d. Fix any stale or incorrect claims (e.g., renamed constants, changed function signatures, outdated behavioral descriptions)
   - Report to the user what stale claims were found and corrected

5. **If nothing meaningful changed**, say so and stop. Do not make edits for the sake of making edits.

6. **Make surgical edits**:
   - Use the Edit tool to update only the sections that need changing
   - Do NOT rewrite entire files — change only the rows, entries, or paragraphs that are affected
   - Match the existing format and section structure exactly
   - Keep content factual — document what IS, not what should be
   - Always include file paths when referencing source files

7. **Commit** with a descriptive message:
   - Example: `git commit -m "Update ARCHITECTURE.md: add new API routes, update file index"`
   - If both files were updated: `git commit -m "Update living docs: [brief description of changes]"`

---

## Update Rules

- **Be surgical** — only update the sections that changed, never rewrite the whole doc
- **Use the Edit tool** — do not rewrite the entire file for a small change
- **Keep it factual** — document what IS, not what should be
- **Include file paths** — always reference the actual source files
- **Match the existing format** — follow the section structure already in the doc

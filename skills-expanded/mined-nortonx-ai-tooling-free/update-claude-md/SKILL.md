---
name: update-claude-md
description: "Update the project's CLAUDE.md with conventions and patterns from recent branch changes. Args: [<path-to-CLAUDE.md>]"
argument-hint: "[<path-to-CLAUDE.md>]"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`[<path-to-CLAUDE.md>]`

- Optional. Explicit path to the CLAUDE.md to update; defaults to searching the repo root and `.claude/`.
- **Examples**: `/update-claude-md`, `/update-claude-md packages/api/CLAUDE.md`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

# Update CLAUDE.md

Analyze recent branch changes and propose additions to the project CLAUDE.md.

## Scope

1. **Locate CLAUDE.md**: Use `$ARGUMENTS` as the path if provided; otherwise search the repo root and `.claude/` for a `CLAUDE.md` file.
2. **Diff source**: Changes between this branch and `main`/`master`.

## Task

1. Read the current CLAUDE.md in full.
2. Run `git diff main...HEAD` (or `master...HEAD`) to get the branch diff.
3. Identify additions worth documenting: only stable, reusable conventions:
   - New CLI commands, scripts, or tooling patterns introduced
   - New architectural patterns or module conventions
   - Non-obvious configuration or environment constraints
   - Public API changes (new endpoints, changed contracts, new env vars)
   - New dependencies and why they were added
   - Gotchas, workarounds, or constraints discovered during the work
4. Filter out:
   - One-off fixes unlikely to recur
   - Implementation details (function bodies, variable names)
   - Anything already documented in CLAUDE.md
   - Obvious information derivable from reading the code

## Output

Show proposed additions as a diff; **do not edit any files yet**:

```
### Update: <path-to-CLAUDE.md>

**Why:** <one-line reason>

```diff
+ <addition: one line per concept>
```
```

Group by section if adding to multiple parts of the file. If nothing new is worth documenting, say so and explain why.

After showing the diff, ask: **"Apply these changes?"**

## Rules

- **Never delete or rewrite existing content**: append or update only.
- **Match the existing CLAUDE.md's style** by example, not by paraphrase. Before drafting, scan the file for: heading depth (does it use `##` or `###` for new sections?), bullet style (`-` vs `*`), whether prose paragraphs or bullets dominate, whether code identifiers are backticked, whether examples use fenced code blocks or inline references. Mirror those choices in your additions.
- One line per concept: CLAUDE.md is part of the prompt; brevity matters. A "line" is one bullet or one short sentence. If you need 3+ lines to explain a concept, the concept is two concepts; split it.
- If no CLAUDE.md is found, stop and report the paths checked.
- Do not apply changes until the user approves.

---
name: capture-rule
description: Capture a new code-quality, architecture, workflow, or meta rule. Asks category and scope, drafts the rule file, and saves it after your approval.
---

# Capture Rule

Turn a one-line rule idea into a well-formed rule file in the right place.

## Input

`$ARGUMENTS` — the rule idea. Examples:

- `"Prefer Result<T> over exceptions for expected failure modes"`
- `"Never catch generic Exception — catch specific types"`
- `"Keep repository methods free of business logic"`

If empty, ask the user what rule they want to capture via `AskUserQuestion` (single free-text style). Then continue.

## Step 1: Categorize

Use `AskUserQuestion` with two questions in one batch:

**Question 1 — Category:**

- **code-quality** — naming, error handling, control flow, tests, idiomatic usage
- **architecture** — boundaries, dependencies, abstraction, file organization
- **workflow** — how Claude should behave (when to ask, what to invoke, how to respond)
- **meta** — config, tooling, file placement, rule-authoring itself

Make the recommended category the first option, inferred from the rule text. (E.g. "Prefer Result<T>..." → code-quality. "Keep repository methods free..." → architecture. "Always run /audit-branch after..." → workflow.)

**Question 2 — Scope:**

- **Global** — applies to every project (`~/.claude/rules/`)
- **Project-only** — applies only to current project (`<project>/.claude/rules/`)

Recommend global unless the rule references project-specific names, paths, or frameworks.

## Step 2: Draft

Write the rule body. Follow the existing rule style:

- **Title:** `# <Short Title>` — directive, not question.
- **First paragraph:** one-sentence directive stating the rule.
- **Why:** a short paragraph or bullet list explaining the rationale (unless the title is self-evident).
- **How to apply / When:** concrete guidance on when the rule fires and how to check.
- **Exceptions:** if any.

Keep it terse: aim ≤ 25 lines, hard cap 50 (`wf-tight-claude-config`).

**Filename convention:**

- `cq-<slug>.md` for code-quality
- `arch-<slug>.md` for architecture
- `wf-<slug>.md` for workflow
- `meta-<slug>.md` for config / tooling / placement

Slug = lowercase kebab-case of the directive (e.g. `cq-prefer-result-type.md`, `arch-repository-no-business-logic.md`, `wf-refactor-after-implement.md`).

**Path:**

- Global: `~/.claude/rules/<prefix>-<slug>.md`
- Project: `<project-root>/.claude/rules/<prefix>-<slug>.md`

## Step 3: Confirm

Show the user the drafted rule (title + full body + target path) in a fenced code block. Ask via `AskUserQuestion`:

- **Save as drafted (Recommended)** — write the file as shown
- **Edit first** — let me revise (follow-up free-text)
- **Cancel** — discard

If **Edit first**: revise based on user's feedback, then show again and re-confirm.

## Step 4: Save

On confirm:

1. Check the target path doesn't already exist. If it does, ask whether to overwrite, merge, or pick a different filename.
2. Write the file.
3. Report: "Rule saved: `<path>`. It will load on next session (global) or immediately (project). Use `/claude-push` to sync global rules to git."

## Step 5: Update docs (global rules only)

If the rule was saved globally, append a bullet to the **Global Rules** section of `~/.claude/README.md`.

Format: `- **<filename>** — <one-line description>`

Don't run `/claude-push` automatically — leave that to the user.

## Notes

- **Avoid duplicates.** Before drafting, Grep `~/.claude/rules/` (and project `.claude/rules/` if project-scope) for overlapping content. If you find one, tell the user and offer to extend the existing rule instead.
- **Prefer global.** If in doubt, global is better — other projects may benefit. Project-scope is for rules tied to this codebase's structure or stack.
- **No emojis in rule files** unless the user explicitly asks.

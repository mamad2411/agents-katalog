---
name: refactor-code
description: "Breadth code-quality sweep of recent changes — naming, dead code, duplication, simplicity, idiom conformance; applies mechanical fixes inline and defers judgment calls to a report. Use whenever the user asks to review, clean up, or check code quality. This is the breadth/quality pass; for deep design/overengineering analysis use /audit-architecture."
---

# Code Review

**Output contract:** when called by `/audit-branch`, return both halves (inline-applied + deferred findings); standalone, apply mechanical fixes inline first, then surface judgment calls via `AskUserQuestion`.

## Step 1: Scope

If orchestrator provided scope, skip to Step 2.

**Mode A** (no args): run `pwsh -NoProfile -File ".claude/scripts/git-diff-scope.ps1"` if that file exists, else `pwsh -NoProfile -File "$HOME/.claude/scripts/git-diff-scope.ps1"`. It already prefers uncommitted changes and falls back to the branch diff, so don't hand-roll that. Abort if `MODE: none`.
**Mode B** (path/area): Glob+Grep relevant files.
**Mode C** (`all`): scan solution from CLAUDE.md, pick 2-3 areas with most quality risk.

## Step 2: Read Code

Read all in-scope files in full (not just diff hunks), plus files that import/depend on them.

## Step 3: Architecture

Evaluate against project principles from `CLAUDE.md` and the project's `.claude/rules/` — read them at runtime rather than assuming a stack. Could this be simpler? Fewer moving parts, less indirection?

## Step 4: Quality

- **Naming**: follows project conventions?
- **Abstractions**: premature or missing? Complexity justified?
- **Duplication**: consolidate copy-paste?
- **Performance**: unnecessary allocations in hot paths, large buffers held too long?
- **Dead code**: unused imports, functions, commented-out code?
- **Consistency**: new patterns match existing ones?

## Step 5: Simplification

Code doing more than needed? Abstractions with one consumer? Indirection that doesn't pay for itself? Less idiomatic than it could be? Judge per `wf-overengineering-not-volume` — flag pieces without a current consumer, not line count.

## Step 6: Apply mechanical, defer judgment

**Apply inline** — the rubric uniquely determines the action:

- Unused imports, dead local bindings, trivial dead code (no callers).
- Stale comments / doc-comments contradicting the code (per `cq-comments-track-code`).
- Naming nits per project conventions.
- Trivial duplication consolidation (local + obvious).
- Typos in identifiers, comments, or strings.

**Defer to the report** — a real judgment call exists:

- Extract helper, split function, restructure module.
- Public API change, new abstraction, interface introduction.
- Behavior change, error-handling reshape.
- Architectural concerns (never in scope for auto-apply).

When called by `audit-branch`, return both halves in the structured response. Standalone, apply inline first, then ask via `AskUserQuestion` (Apply / Defer to plan / Skip) for the deferred set only.

## Step 7: Report

**Summary** — one paragraph.
**Applied inline** — counts + brief `file:line` list. Skip if none.
**Architecture** — deferred structural concerns. Skip if none.
**Quality Issues** — deferred findings: file+line, severity (low/med/high), what, why, suggestion. Summarize low-severity if >5.
**Simplifications** — deferred concrete before/after or description.
**Verdict**: **Ship it** / **Minor tweaks** / **Refactor recommended** / **Rethink**.

## Project rules

Project-specific review criteria come from the project's own `.claude/rules/` (`arch-*` and `cq-*` entries) and `CLAUDE.md`, read in Step 3 — not from a copy kept here.

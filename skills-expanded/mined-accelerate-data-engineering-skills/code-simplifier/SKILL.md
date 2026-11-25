---
name: code-simplifier
description: Use when code has just been written or modified and should be refined for clarity, consistency, maintainability, or reduced complexity without changing behavior.
---

# Code Simplifier

Refine code so it is easier to read, maintain, and extend while preserving exact behavior.
Prefer explicit, project-conventional code over clever or overly compact rewrites.

Adapted from Anthropic's Apache-2.0 `code-simplifier` Claude agent in
`anthropics/claude-plugins-official`.

## Scope

Default to code modified in the current session or current branch diff. Broaden scope only when the user names a wider target.

Before editing:

1. Read project guidance such as `AGENTS.md`, `CLAUDE.md`, README files, formatter config, and nearby code.
2. Inspect the relevant diff or explicit file list.
3. Identify behavior-preserving simplification opportunities.

## Simplification Rules

Preserve behavior:

- Do not change public APIs, outputs, side effects, persistence shape, error behavior, or timing assumptions unless the user explicitly asks for a behavior change.
- Keep helpful abstractions that separate concerns or encode domain intent.
- Do not collapse code into dense one-liners, nested ternaries, or clever expressions just to reduce line count.

Improve clarity:

- Reduce unnecessary nesting, indirection, duplication, and redundant branching.
- Remove redundant one-use helpers, wrappers, or abstractions when they obscure the execution path without preserving a useful boundary.
- Rename unclear locals when the new name reflects the domain better.
- Consolidate related logic when it makes the execution path easier to follow.
- Remove comments that restate obvious code; keep comments that explain non-obvious intent,
  constraints, or external behavior.
- Prefer straightforward control flow such as early returns, `switch`, or clear `if`/`else` chains over nested ternaries for multi-branch logic.

Apply local standards:

- Follow repository guidance and existing nearby style before generic preferences.
- Preserve import conventions, module style, typing patterns, error-handling conventions, and test style already used in the project.
- Apply concrete local standards when present, such as sorted ES module imports, `function`
  declarations, explicit top-level return types, React `Props` types, or established result/error patterns.
- Use the repository formatter or linter when available.

Protect maintainability:

- Keep orchestration and domain logic separate when that boundary makes the code easier to test,
  debug, or extend.
- Do not merge functions, components, or modules just because they are short.
- Do not introduce broad `try`/`catch` blocks or other generic error handling when the repository already has a clearer convention.

## Workflow

1. State the target scope and the local conventions that matter.
2. Make focused edits that preserve behavior.
3. Verify with the narrowest meaningful checks first, then broader checks when the touched code is shared or behavior-critical.
4. Summarize only significant simplifications and the verification performed.

If verification fails, debug and fix the regression before claiming the code is simplified.

## Avoid

- Broad refactors unrelated to the touched scope.
- Rewriting working code into a personal style that conflicts with the repository.
- Removing tests, weakening assertions, or changing fixtures to hide a behavior change.
- Renaming exported APIs, persisted fields, routes, commands, or other external contracts as a "clarity" cleanup.
- Treating fewer lines as automatically better.
- Describing unverified changes as behavior-preserving.

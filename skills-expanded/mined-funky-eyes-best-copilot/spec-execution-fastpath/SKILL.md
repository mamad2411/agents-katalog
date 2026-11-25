---
name: spec-execution-fastpath
description: "Use when requirements or spec are clear and the implementation should be a minimal, repo-pattern-compatible diff. DO NOT USE FOR: unclear direction, broad redesign, or tasks without enough file/context evidence."
---

# Spec Execution Fastpath

## Steps

1. Read only the user-provided paths, relevant spec, direct owner files, and immediate call chain.
2. Freeze scope: goal, files, constraints, non-goals, acceptance checks, verification budget.
3. Reuse existing patterns before adding abstractions.
4. Implement the smallest diff that satisfies the requirement.
5. Simplify recently touched code when it preserves behavior: reduce unnecessary nesting, remove redundant branches, improve names, and align with local style.
6. Add or update focused tests when behavior changes.
7. Verify with the smallest sufficient command or static evidence.
8. For persistent task/spec work, update `tasks.md` status and `memories/repo/current-workstreams.md` before reporting completion.

## Guardrails

- Do not expand file ownership without returning to PM.
- Do not add “future-proof” abstractions without present complexity.
- Do not simplify by changing behavior, public contracts, error semantics, or observability.
- Public contracts, auth, data, dependencies, CI, and runtime config require blast radius assessment.
- Customization files require frontmatter/schema and residual-reference checks.
- Chat-only progress is invalid for persistent MEDIUM/LARGE work.

## Output

Return changed files, behavior summary, verification evidence, state-sync evidence when applicable, and residual risk.

---
name: zno-fix
description: Use when the user writes /zno-fix or reports a bug or defect. Reproduces or reasons about the defect, locates the root cause, fixes it with a regression test when possible, verifies the fix, and updates the changelog if behavior changed.
---

# Zno-Fix — Bug Fix

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Restate the defect briefly: expected vs actual behavior.
2. Reproduce the defect, or when reproduction is impractical, reason about it from the code path and state the assumption explicitly.
3. Locate the root cause before writing the fix. Do not patch symptoms.
4. If the project has a test framework configured, write a failing regression test that captures the defect, then fix minimally until it passes.
5. Verify: run the relevant tests/build and check the original reproduction path.
6. Keep docs lightweight for fixes: update `docs/development/03-feature-changelog.md` if behavior changed (scaffold it first with `--scaffold feature` if missing). Only touch other docs when the fix changed rules, structure, or operations (mapping in `references/docs-map.md`).
7. Before marking the task complete, satisfy the verification gate in `references/verification.md` (at least 2 pieces of evidence).
8. If the fix affects user-visible UI or browser workflows, the final response must include page-level manual test steps (template in `references/verification.md`).

Even when the user says to skip docs for a tiny fix, keep the change small and still update the changelog if behavior changed.

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
- `<skills-root>/zno-init/references/verification.md` — verification gate and final-response page test steps.

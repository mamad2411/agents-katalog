---
name: ux-decisions-and-load
description: "Fix overwhelming menus, cognitive overload, too many choices, poor chunking, hidden context, recall-heavy workflows, or misplaced complexity in UI design and implementation."
---

# Choices, workload and avoidable complexity

## Scope

Apply this specialist skill only when the user's task implicates **choices, workload and avoidable complexity**. If the problem is merely adjacent, do not broaden the user's scope.

## Procedure

1. Read `references/playbook.md` for symptoms, differential diagnosis, proven repair patterns, tradeoffs and test cases.
2. Establish the actual user goal and evidence. Do not assume causal failure from a visual screenshot alone.
3. Identify the primary failure mechanism; consider alternative root causes before choosing a fix. Relevant Laws of UX: choice-overload, hicks-law, cognitive-load, chunking, millers-law, working-memory.
4. Recommend or implement a *specific* change, preserving functional, accessibility, security and consent constraints. Use existing design patterns/components in the user's project.
5. Verify the repaired journey including one edge case. State what was observed versus what remains hypothetical.

## Related workflows

For broad reviews, issue IDs, and severity classification use `ux-review` and `ux-diagnose`. For coding tasks use `ux-build`; for acceptance checks use `ux-validate`. Specialist guidance is advisory, not authority to change code or expand scope.

---
name: csswitch-code-review
description: Conduct a CSSwitch formal independent review for a user-requested or frozen F2/F3 candidate, not ordinary WIP self-checks.
---

# CSSwitch code review

Use this Skill only for a user-requested formal review or a stable `F2` / `F3` candidate. Start from [独立审查](../../rules/reviewing.md), then load no more than the relevant domain rule, nearest index, and necessary owner documents.

- Require the exact worktree, branch, base, `HEAD`, target scope, permission boundary, and requested severity before treating the result as a formal review.
- Review the complete diff against owner, caller, state, effect / transaction, failure path, test strength, document synchronization, and evidence-layer boundaries.
- Preserve clean context and the two-round limit: one concentrated initial review after candidate freeze, then at most one final review after repairs. Do not enlarge the slice for target-external P2-or-lower findings.
- `F0` / `F1` implementation self-checks do not invoke this Skill or claim independent review. Source closure remains governed by [自动测试](../../../docs/operations/testing.md).

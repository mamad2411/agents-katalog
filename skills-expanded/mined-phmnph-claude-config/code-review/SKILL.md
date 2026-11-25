---
name: code-review
description: Review a branch or working-tree change for defects, requirement gaps, and relevant repository standards.
---

# Review the actual change

Establish the task's acceptance criteria and review scope. Use supplied specs,
conversation decisions, or relevant issue references. Read tracker instructions
only when fetching a tracker item. If no spec exists, review observable behavior
and report that requirement coverage is limited; ask only if missing intent
prevents a useful review.

For Git changes, follow [scope.md](references/scope.md). Capture the base and HEAD,
include relevant untracked files in working-tree mode, and report exclusions.
Do not claim review success from an empty tracked diff. Preserve the distinction
between existing unrelated work and this task's changes.

Assess two questions:

- **Requirements and correctness:** does the change implement the intended
  behavior, preserve relevant contracts, and handle realistic failure paths?
- **Standards and maintainability:** does it follow applicable repository rules,
  and does changed structure introduce a concrete maintenance problem?

Prioritize defects and missing behavior. Use [design-smells.md](references/design-smells.md)
when structural changes warrant a deeper assessment. These are optional
heuristics, not an obligation to find or remove every named pattern. Avoid
repeating issues already established by tooling without adding useful context.

## Choose review effort

Review a small coherent change directly. Use independent reviewers when the
change spans distinct concerns, warrants a fresh perspective, or the user asks,
and host delegation is available. Give each reviewer the exact snapshot, file
scope including untracked files, relevant requirements and rules, and a bounded
question. Reviewers report only and do not recursively delegate. Do not require
a fixed number of agents or repeat equivalent reviews after no relevant change.

## Finish with evidence

Return actionable findings with paths, consequences, and the supporting rule or
requirement. Distinguish defects from optional improvements. Identify which of
the two questions a finding concerns; for a small review a short combined list
is sufficient. State when no findings were found and name material unverified
assumptions. Do not equate static review with passing tests or recovered service.

If fixes are authorized, address supported findings, run affected checks, and
review changes made after the inspected snapshot. Otherwise provide the review
without changing application code. Stop when the requested scope is assessed and
authorized fixes are verified, or report a concrete blocking uncertainty.

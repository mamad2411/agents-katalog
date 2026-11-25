---
name: cyc-build
description: "Implement planned behavior in thin tested slices, preserve affected consumers and hand current evidence to Verify."
---

# Build the change

Follow [handoffs](../../docs/skill-contract.md), [principles](../../docs/principles.md), [code standards](../../docs/engineering/code-standards.md) and the [progress standard](../../docs/response-standard.md#progress-updates). Read applicable project rules and preserve dirty work. Explain behavior, preserved contracts and actual evidence.

Use [domain design](../../docs/engineering/domain-design.md) for shared invariants and [failure handling](../../docs/engineering/failure-handling.md) for I/O/partial effects. Impact is not edit authority.

Write the smallest coherent slice. Features/bugs need meaningful red/green checks; refactors need characterization passing on originals and candidate. Never weaken a requirement, test or configured check to pass. After two failed fixes challenge their shared premise.

Trace state, storage, interfaces and consumers. Use focused feedback then broad checks. Review diffs; run git diff --check, preserve encoding and log actual failed fixes.

New composed frontend work must follow [frontend gates](../cyc-design/frontend-design/SKILL.md) before expansion. On a new build or handoff read the study decision in the project’s `design/decisions.md` (or its recorded run-local path). Build the named material and its next state as one slice; check that slice before repeating it. Narrow repairs preserve existing identity.

Read/acknowledge current [unified task context](../../docs/task-context.md) before dependent work. Workers are bounded/read-only; reconcile evidence, disagreements and failed approaches. Worker success does not complete the parent.

Retain canonical knowledge/index before checks through [Context](../cyc-context/SKILL.md). Restrictions stay pending; packets cannot refresh source. Hand Verify changes, red/green evidence and limits. Build is not task acceptance; recovery preserves budgets.

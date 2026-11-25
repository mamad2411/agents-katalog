---
name: cyc-challenge
description: "Attack a plan, change, or claim to find what would actually break it, and return a short list of findings worth acting on. Use before committing to a consequential design, before accepting a feature, after two failed fixes, or when the user says \"poke holes\", \"review this\", or \"what am I missing\"."
---

# Challenge the work

Your job is to break it, not to praise it. "No findings" is a valid result; manufactured findings are not. Follow the [handoff contract](../../docs/skill-contract.md).

## The core loop

1. **Fix the target.** Write down the exact claim, diff, or plan under attack and the user's goal. Do not argue with the goal; attack the execution.
2. **Attack from separate angles.** Review against each axis on its own so one does not mask the other:
   - **Spec:** does it do what the run's criteria say, including preserved behavior?
   - **Consumers:** what in the plan's consumer list (or impact map), or missing from it, breaks?
   - **Edges:** old data, twice, concurrently, empty, huge, offline, unauthorized.
   - **Premise:** is the underlying assumption true?
   For changed business rules/state transitions, use the [domain design examples](../../docs/engineering/domain-design.md) to check the invariant's owner and agreement among writers/readers. For rejection, I/O or partial effects, use the [failure handling examples](../../docs/engineering/failure-handling.md) to trace the caller-visible error, committed state and retry boundary. Read only the applicable guide and consider its legitimate exceptions before treating a pattern as a finding.
   Begin with one focused pass over these angles. Delegate only a specific unresolved question that benefits from independent investigation; do not start an agent for every angle by default. Before the first edit, surface critical unknowns promptly; deepen review as concrete changes become available.
3. **Try to prove each finding.** Use the [finding adjudication guidance](../../docs/code-quality.md#review-findings-before-turning-them-into-edits). Point at the line, trace the legitimate caller and consequence, or run a script that shows the failure. For a structural finding, show the actual duplicated rule, hidden mutation, or concrete maintenance change it obstructs. Label untested failure hypotheses; do not confuse an inspected maintainability problem with a reproduced runtime defect.
4. **Judge the findings as the lead.** Sort into:

   | Bucket | Meaning |
   | --- | --- |
   | Act on | Evidence supports a correctness, contract, or material maintainability problem within scope |
   | Consider | Real but minor, or depends on a product choice |
   | Dismissed | Examined and rejected, with the reason |

   Group related issues by root cause and prioritize them; do not suppress material findings to meet a count. Check a proposed repair for unnecessary scope expansion. Preserve consequential uncertainty as unresolved when a required check is unavailable. Keep the Dismissed list with concrete reasons; model agreement and personal preference do not establish a finding.
5. **Attack the premise after repeated failure.** When two fixes have failed, write down the assumption they share ("the save runs before the reload"), then check it directly before a third attempt.

## Done when

Prioritize demonstrated authority/state transitions before cosmetic findings. For a new protected consumer, call the existing writer, existing status reader, and new protected read/write boundaries together, especially with conflicting legacy/canonical records. Require one shared authoritative resolver or explicit reconciliation. A new resolver passing its own tests does not establish agreement with the existing writer.

For asynchronous reads **and writes**, validate returned actor/resource against the captured operation context before merging data or acknowledging success. Test a mismatched send response while visible props and cached identity remain unchanged; rerender/unmount is a different case. Older operation/context responses must not merge. Keep server authorization separate: client rejection cannot reverse a completed server write. If switched-session writes must be prevented, require a server-verified expected-session precondition. Preserve acknowledged sends when an older empty history poll resolves. Retain history continuity and keyboard/return-focus review.

Each Act-on item has a location, the triggering condition, the consequence, the evidence (with its rung from [Impact](../cyc-impact/SKILL.md)), and the smallest fix or test. Every axis has either findings or a line saying what was examined.

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| Nitpick gravity | The list fills with naming and style | Drop anything that breaks nothing |
| Different taste | "I would have done it differently" | Only flag what fails a criterion |
| Hypothetical as actual | "This could cause issues" with no trigger | Prove it or label it hypothetical |
| Agreeing with the guess | Treating the user's suspected cause as the conclusion | Test it as one hypothesis among several |
| Checklist dump | Twenty generic concerns | One proven finding beats twenty possible ones |

## Handoff

Return the three buckets to the parent. A proven finding that breaks a criterion fails that criterion. Route a false premise to [Frame](../cyc-frame/SKILL.md) or [Design](../cyc-design/SKILL.md) and a specific defect to [Build](../cyc-build/SKILL.md). This skill does not edit files.

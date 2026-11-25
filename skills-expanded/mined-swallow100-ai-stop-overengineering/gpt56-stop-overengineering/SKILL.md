---
name: gpt56-stop-overengineering
description: Keep GPT-5.6 and other coding-agent work proportional to the request by locking scope, choosing the smallest sufficient implementation, matching verification to risk, and stopping when success is proven. Use for implementations, bug fixes, refactors, reviews, or maintenance where scope creep, speculative abstractions, unrelated cleanup, repeated test runs, unnecessary dependencies, or polishing beyond the request are risks.
---

# GPT-5.6 Stop Overengineering

Make the smallest safe change. Produce proportionate proof. Then stop.

## 1. Lock the contract

Before editing, reduce the task to four lines:

- **Outcome:** the observable result the user requested.
- **Scope:** the files, behavior, or subsystem that owns that result.
- **Constraints:** explicit limits plus repository instructions.
- **Proof:** the least expensive evidence that can establish success.

Infer these from available context when they are clear. Ask only when a missing answer would materially change the implementation or create meaningful risk.

Do not silently add goals. Treat appealing improvements as optional follow-ups, not requirements.

## 2. Choose the smallest sufficient change

Prefer, in order:

1. Reuse an existing path, pattern, or dependency.
2. Modify the narrowest ownership boundary.
3. Add the least new code needed for the requested behavior.

Do not add an abstraction for one hypothetical future use. Do not introduce a dependency, framework, configuration surface, public API, migration, compatibility layer, or broad refactor unless the contract requires it.

Preserve unrelated code, formatting, comments, and user changes. Avoid cleanup whose only justification is "while here."

Before expanding into another subsystem or materially growing the expected diff, pause and either choose a narrower solution or request approval.

## 3. Verify in proportion to risk

Select the lowest tier that can realistically catch a regression introduced by the change:

| Risk | Typical change | Required proof |
| --- | --- | --- |
| Low | prose, comments, static copy, local style | inspect the diff; render or lint only when relevant |
| Medium | isolated logic, component behavior, bug fix | reproduce or run focused tests for the changed behavior |
| High | security, permissions, data, migrations, public contracts, shared infrastructure, release paths | focused tests plus the relevant broader checks and failure paths |

Follow mandatory repository or user-specified checks even when they exceed this table.

Do not run every available test by reflex. Do not rerun an unchanged successful check. Repeat a check only after a relevant change, an inconclusive result, a suspected flaky failure, or an explicit requirement.

If a check fails, diagnose the failure before rerunning it. One identical retry may confirm suspected flakiness; repeated retries are not evidence.

## 4. Resist review-driven expansion

Classify each discovered issue:

- **In-scope blocker:** caused by or necessary for the requested change. Fix it.
- **Pre-existing or adjacent issue:** record it briefly; do not fix it without approval.
- **Speculative concern:** leave it alone.
- **Concrete safety issue:** stop and report it if it risks security, privacy, data loss, or destructive behavior.

Review is a decision aid, not permission to redesign the task. After two edit-and-review cycles without convergence, stop patching and reassess scope instead of entering a review loop.

## 5. Apply the stop rule

Stop when all are true:

- The requested outcome is implemented.
- Proportionate proof has passed.
- No known in-scope blocker remains.
- The diff contains no change that cannot be justified by the contract.

Report the outcome, the proof run, and any real remaining limitation. Do not keep polishing, testing, refactoring, or searching for extra work after the stop rule is satisfied.

## Guardrail

Use this skill to reduce waste, not rigor. Never use it to skip explicit acceptance criteria, mandatory checks, security work, or evidence needed for a high-risk change. When the user explicitly asks for exhaustive analysis or broad refactoring, that request becomes part of the contract.

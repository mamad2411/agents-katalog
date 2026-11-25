---
name: reentry-pass
description: Specify every in-scope Stateful condition and run the five-question re-entry review on each non-transient lifecycle state. Use after human-confirmed triage to add behavior, owner, acceptance criteria, category-specific recovery or surface requirements, explicit applicable/not-applicable re-entry verdicts, and high-risk composite scenarios. Use on lifecycle states, failures, interruptions, and surfaces; do not mark a condition specified from its name alone.
---

# Specification and Re-entry Pass

Turn triaged conditions into testable contracts. Re-entry is one part of specification, not the only requirement.

## Procedure

1. Read the confirmed condition map and `STATEFUL.md`. Refuse to infer confirmation from agent-written recommendations.
2. For every `scope: in` condition, write:
   - behavior;
   - accountable owner;
   - at least one testable acceptance criterion;
   - design, implementation, and test links when available.
3. Add the category contract:
   - **Lifecycle state:** canonical rendering or observable behavior, allowed/prohibited actions, data and invariants, transitions and guards, stale-data and concurrency behavior.
   - **Failure:** user-facing response and redaction, preserved work, safe retry/alternate path/exit, idempotency, and observability.
   - **Interruption:** persistence window, revalidation, reconciliation, resume/restart destination, and recovery when prior context no longer exists.
   - **Surface:** content priority, supported actions and fallback, freshness, accessibility, authentication, privacy, and redaction.
4. For each non-transient in-scope lifecycle state, answer all five re-entry questions:
   - `after_time`;
   - `alternate_entry` from notification, deep link, or different device;
   - `without_predecessor`;
   - `data_changed`;
   - `after_failure`.
5. Record every answer as:
   - `applicable` with a concrete specification; or
   - `not-applicable` with a reason.
   Silence is not a verdict.
6. Identify high-risk combinations across lifecycle state, interruption, surface, changed data, and dependency condition. Write a scenario and acceptance criterion for each selected combination. Do not enumerate the full Cartesian product.
7. Flag conflicts with canonical behavior, adjacent conditions, policies, or implementation constraints for human decision.
8. Set `status: specified` only when the common contract, category contract, and required re-entry review pass.
9. Update `STATEFUL.md` with specified/in-scope totals and re-entry-reviewed/eligible totals. If a JSON mirror exists, update it and run `scripts/validate_state_map.py --profile handoff state-map.json` when the full in-scope pass is complete.

## Output

```text
## <condition id>: <name>

Category: <state | failure | interruption | surface>
Owner: <role or person>

Behavior:
<observable contract>

Category requirements:
- <requirement>

Acceptance criteria:
- <testable criterion>

Re-entry review (lifecycle states only):
- After time: <applicable specification | not-applicable reason>
- Alternate entry: <...>
- Without predecessor: <...>
- Data changed: <...>
- After failure: <...>

Composite scenarios:
- <high-risk combination and expected behavior>
```

## Failure modes

- Specifying only lifecycle states while leaving in-scope failures, interruptions, and surfaces named but undesigned.
- Restating the description as acceptance criteria.
- Omitting recovery for failures or interruptions.
- Omitting owner or testability.
- Collapsing five re-entry questions into “returning user.”
- Treating re-entry questions as independent when their conditions compose.
- Marking a record specified while required fields remain undecided.

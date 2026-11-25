---
name: unreal-anti-slop-review
description: Adjudicate a frozen Unreal review surface for UObject and reflection, registrations and replaceable sources, async/world/threading, editor mutation, loading/performance, gameplay/networking, tests, and engine ownership. Use after exact paths or a surface manifest are supplied; diff selection, PR workflow, generic maintainability, and closeout remain with the calling review skill.
---

# Unreal Anti-Slop Adjudication

Adjudicate Unreal contracts on an exact surface. Do not select Git changes, choose a PR base, perform generic maintainability review, or approve/reject the change.

## Adjudication Steps

1. **Freeze the surface.** Accept a caller-supplied manifest or exact named paths plus exclusions. For direct invocation, create the equivalent manifest without inferring Git state. Read [adjudication-schema.md](references/adjudication-schema.md) before constructing it.

   Completion: the manifest is valid, non-empty, and records every selected file, attribution, scanner eligibility, exclusion, and supplied provenance field.

2. **Select applicable contracts.** Read [contract-ledgers.md](references/contract-ledgers.md). Mark every branch `APPLICABLE` or `NOT_APPLICABLE` with a reason and identify the concrete owners that require ledger rows.

   Completion: every branch has a reasoned status, and every applicable branch has concrete owners or an explicit justified zero-owner row.

3. **Collect lexical signals and review items.** Run `scripts/scan_unreal_signals.py` with the manifest. Treat each signal as a question, never a finding; zero signals proves nothing. Add manually discovered relational items from the applicable contracts.

   Completion: every manifest file is recorded as scanned or intentionally unscanned, every emitted signal has a stable ID, and every signal/manual risk maps to a review item.

4. **Complete ledgers and adjudicate.** Fill the typed ledger for every concrete owner, then terminate each review item as exactly `FINDING`, `GAP`, or `DISMISSED`. Caller attribution is orthogonal and never changes the disposition.

   Completion: no owner, bound source, operation identity, shared object, mutation, terminal state, or production executor remains implicit; every item records evidence and the reason for its terminal disposition.

5. **Assign proof boundaries.** Read [proof-boundaries.md](references/proof-boundaries.md). Record `PROVED`, `NOT_APPLICABLE`, or `GAP` for every claimed boundary. Keep an item-disposition `GAP` separate from a proof-boundary `GAP`.

   Completion: every finding and claimed behavior states the highest proof reached, every missing higher artifact, and the closest evidence available.

6. **Emit and validate the packet.** Produce the JSON packet defined in [adjudication-schema.md](references/adjudication-schema.md), then run `scripts/validate_adjudication_packet.py <packet.json>`.

   Completion: the validator passes. Only then report `ADJUDICATION COMPLETE` with outcome `FINDINGS PRESENT`, `GAPS ONLY`, or `NO FINDINGS OR GAPS`. Lead the human summary with actionable findings; the calling review skill owns approval and closeout.

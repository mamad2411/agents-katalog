---
name: core-debugging
description: Diagnose a concrete failure and propose bounded repair tied to its requirement and fresh evidence.
---

# Evidence-led debugging

Apply to a finding, failed check or unexpected behavior. Ordinary implementation without a failure does not need this diagnostic procedure.

1. Identify the finding, requirement, expected/actual behavior and source fingerprint. Read supplied errors and traces. Separate a defect from missing verifier, environment failure or uncertain process termination.
2. Trace the failing path from entry to symptom, then the incorrect value backward through callers to its producer. Compare with a working local path and the actual recent change; similar errors do not prove the same cause.
3. State one falsifiable hypothesis: cause, supporting facts, smallest distinguishing check and the result that would contradict it. Inspect available evidence before proposing instrumentation. Commands need registered checks and Executor permission; never dump secrets or execute upstream helpers.
4. Propose the smallest repair at the behavior owner with current source hashes and structured edits. Preserve access checks, immutable state and failure semantics. Do not mask symptoms with broad catch, arbitrary delay, disabled verification or unsafe fallback. Additional validation is useful only at a demonstrated bypass of the invariant.
5. Link repair to the original criterion and necessary regression. Prefer an existing reproducible failing scenario; add tests only when allowed and useful. For timing failures, wait for the required condition with a bounded deadline; tests of debounce/timing itself need controlled time rather than generic polling.

Follow runtime repair budget/transitions, not a skill-owned retry loop. A contradicted hypothesis needs a new explanation, not stacked guesses. If evidence is insufficient, the budget is exhausted or attempts expose an architectural issue, return the unresolved finding and next needed evidence. Recover uncertain writes before retrying. Close findings only through fresh linked verification, never an old receipt or a claim.

Adapted from obra/superpowers systematic-debugging and tracing/waiting references for Flowcairn permissions and finite repair. Copyright (c) 2025 Jesse Vincent. [MIT](../licenses/obra-superpowers-MIT.txt); sources/changes: [PROVENANCE](../PROVENANCE.json).

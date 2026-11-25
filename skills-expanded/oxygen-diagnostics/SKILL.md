---
name: oxygen-diagnostics
description: Trace OXYGEN cells and runs, explain failures or credit spend, and plan reconciled retries from native provenance.
---

# Explain one operational failure

Read [the runtime contract](../../../docs/runtime-contract.md). Identify the visible Table/row/cell, Workflow, Sequence or message and the user's symptom. Discover `oxygen capabilities search "diagnose failed table run" --json` using the actual symptom, then hydrate the narrow read command.

| Question | Evidence to collect |
|---|---|
| Wrong or missing cell | Input values, dependencies, column definition/version, cell/run envelope, sources |
| Failed or stuck work | Status, attempts, lease/retry time, structured error, approval/integration state |
| Unexpected credits | Row count, provider/model operation, attempts, caps, estimated versus charged receipts |
| Ambiguous external effect | Native action/message ID, provider ID, delivery state and reconciliation result |

Distinguish pending, leased, deferred, approval-required, retryable and failed work. Missing output may mean the step never ran; an empty view may be scoped or stale. Read envelopes and timestamps instead of assuming a raw string is the final result.

Use run and item provenance to connect the symptom to its owner. Avoid dumping every workspace log or joining unrelated runs solely by time. A cost estimate, reservation and settled charge are not interchangeable.

Before a retry, identify exact items, possible duplicate effects and incremental cost. Reconcile an ambiguous send or write first. Preview the bounded repair and execute only within the authorized scope; do not switch providers or build hidden local recovery state.

Return the most likely cause, supporting IDs/links, remaining uncertainty and verified repair state. If a product defect remains, prepare a reproducible report locally; sending feedback or transcripts requires the user's request.

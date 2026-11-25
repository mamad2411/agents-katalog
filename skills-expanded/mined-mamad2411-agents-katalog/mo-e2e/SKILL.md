---
name: mo-e2e
description: Run the end-to-end scenarios that genuinely require an agent against one frozen full candidate SHA and report complete per-scenario evidence without editing the candidate.
license: MIT
---

# Agent-required end-to-end verification

Act as a separate read-only E2E actor. Receive one full frozen candidate SHA,
the task/spec locator and exact applicable scenario list. Read the project's E2E
contract and acceptance-to-proof mapping. Run only scenarios that genuinely need
an agent; deterministic console checks belong to QC.

Do not edit or commit tracked files. Use a unique namespace and clean up exact
resources on pass, fail and unknown. Never run a production, destructive,
credential or subscription action until the user explicitly authorizes that
exact named action for this candidate. Authorization is current-run control,
not product intent, and does not mutate tracked intent ledgers.

For every scenario report the candidate, ID, actor/model vendor, environment,
action, observed result and `PASS`, `FAIL` or `UNKNOWN`. Do not include secrets,
reasoning or raw artifact dumps. A complete run passes only when every selected
scenario passes on the unchanged SHA. Missing or incomplete evidence is
`UNKNOWN`; there is no partial pass.

Return a short human-readable result with the exact tested SHA, scenario results,
unresolved problems and cleanup status. Do not create a receipt, manifest,
registry, digest, tracked evidence ledger or external sink.

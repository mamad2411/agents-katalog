---
name: lifecycle-canary-convergence
description: "Converge a Memory lifecycle canary, retry or data repair with one bounded inventory, dry-run, apply and audit. Use before another lifecycle retry or canary, when auditing Plans, Support, Reviews and outbox state, or when classifying historical lifecycle anomalies."
---

# Lifecycle Canary Convergence

- Before another retry or canary, review the complete design contract and static call path for the affected state transition: transaction ownership, operation ordering, idempotency, stale guards, retry semantics, and SQLite/Cloud adapter parity.
- Define a falsifiable hypothesis and the exact confirming or rejecting evidence before changing code or data. Classify historical data, migration residue, and one-off provider/runtime failures separately from reproducible shared-contract violations.
- Prefer one bounded joint snapshot that correlates durable runs/jobs, Lifecycle Plans and mutations, current and stale Support, Source Projection lineage, Reviews/Findings, vector outbox, and process health. Do not replace it with repeated narrow probes that guess at adjacent causes.
- Use a bounded convergence sequence: one report-only inventory, one exact dry-run, one controlled apply when authorized, and one strict incremental audit. Stop when the incremental audit is clean and no relevant state changed.
- Never fabricate Evidence, infer missing provenance from semantic similarity, or silently rewrite lifecycle history to make an audit pass. Preserve historical Plans, Relations, Reviews, Findings, and failed jobs.
- Report current and historical populations separately. Distinguish active Memories from superseded or retired lifecycle records and classify unexpected growth by lifecycle reason and bounded time cohort.

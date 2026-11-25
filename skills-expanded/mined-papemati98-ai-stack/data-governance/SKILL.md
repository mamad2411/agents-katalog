---
name: data-governance
description: Include applicable ownership, access, quality, compatibility and recovery checks for persistent data, schemas, ETL or migrations in the existing TODO; preserve real consent and privacy decisions without a separate governance contract.
---

# Data governance

Use when a change materially affects durable data, schemas, ETL, published metrics,
access, migrations, retention or recovery. Synthetic transient local examples do
not require a governance workflow. Do not assign new D0-D3 gates to ordinary work.

1. In the existing TODO identify system of record, owner, purpose, classification,
   sources/consumers and compatibility. Reuse established policy; an unknown fact
   stays unknown. No separate sealed contract or schema registry is required by
   this skill for a local fix.
2. Choose only applicable checks: actual role allow/deny, formula/units/time range,
   quality and source-to-target reconciliation, schema compatibility, replay
   idempotency, or backup/restore where recovery is affected. A hash or row count
   alone does not prove semantic correctness.
3. For a migration define the checkpoint, representative validation, backup/recovery
   and narrow rollback in this same TODO. Destructive or production cutover retains
   its exact explicit owner-consent gate.
4. Reuse existing lawful basis, retention, DPIA and transfer decisions. Do not invent
   them or request all of them for every task. Ask for a real unresolved business
   or legal decision only when the proposed operation depends on it. Independently
   verify variable high-stakes facts from primary sources before using them.
5. Minimize data sent to models: schema, aggregate metrics and redacted evidence.
   Existing privacy and no-training policies remain binding. This skill does not
   authorize client-data access, contact, secrets, IAM or public integrations.
6. Independent product review checks current results and relevant data regressions.
   Report evidence and missing decisions proportionately. Artifact/transport success
   is separate from product acceptance and canonical Hub/session closeout.

Do not add an independent plan, contract, approval or review graph solely for
these checks. Shared changes still require private backup PUSHED/CURRENT.
Historical DRAFT/seal/compile-graph-fragment commands are preserved only in
references/legacy-recovery.md. Do not execute them for a new TODO.

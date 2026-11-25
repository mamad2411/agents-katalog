---
name: builder-migration-config-safety
description: Use when an authorised increment includes migration or configuration changes.
---

# Guard migration and configuration changes

## Inputs
Accepted migration/configuration task, exact authority, compatibility window, rollout/abort/rollback plan, data ownership, and environment policy.

## Procedure
1. Mark migration/configuration `applicable` or `not_applicable`; record the rationale.
2. Verify that authority names the exact files, schemas, environments, and operation classes.
3. Keep secrets and environment-specific values out of source and receipts.
4. Check forward/backward and mixed-version compatibility, partial apply, retry/idempotency, and ownership.
5. Define preconditions, dry-run or safe validation, abort signal, rollback limit, backup/recovery, and reconciliation.
6. Execute only authorised local non-production operations; list every unexecuted deployment step as a limit.

## Output
A safety record with authorised changes, validation, rollback/reconciliation boundary, and `safe_to_continue|blocked|not_applicable`.

## Stop condition
Stop on destructive or irreversible work without exact authority, unclear ownership, unavailable recovery, secret exposure, incompatible mixed-version state, or a production mutation request.

---
name: db-access
description: "Audit roles, tenant filtering, and row-level policies where supported. Use for grants, connection roles and row policies; backend-permissions checks application enforcement."
---

# db-access

Audit roles, tenant filtering, and row-level policies where supported.

## Choose this workflow

Use for grants, connection roles and row policies; backend-permissions checks application enforcement.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Databases methods](../../references/packs/database.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; roles, tenant model, policies, engine, and representative access matrix.

**Pack prerequisites:** Actual engine/version, schema/migrations, query workload, and explicitly identified environment. Prefer supplied plans, metadata, and isolated fixtures. Even a SELECT can lock, call mutating functions, or overload a database; inspect semantics before execution. Executing an analyzed query is distinct from reading its plan.

- **Infer from evidence:** Read engine/version, ORM/runner, schema and migration history from project artifacts before choosing SQL.
- **Reasonable default:** Prepare local SQL and isolated fixtures without assuming production size, locks or recovery guarantees.
- **Ask only when needed:** Ask for environment, downtime or recovery constraints before live/destructive execution when missing; unavailable production access does not block migration files.

Declared evidence requirements: `database.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Database privileges, tenant predicates, row-level policies, and bypass paths.

No source changes in inspect/plan. Save only requested planning artifacts. db-migrate applies an accepted grant or policy change.

## Execute

1. Trace the actual runtime role, grants, execution identities and ownership or bypass privileges.
2. Inspect read and write policy predicates with positive and cross-tenant negative access cases; run read-only probes against an isolated target in scope, and leave write-policy probes to a separately scoped apply run.

## Technical method

- **Inspect:** Read actual connection roles, grants, RLS read/write predicates, owner/bypass privileges and tenant context setup/reset.
- **Method:** Test using the application role and transaction/pool lifecycle; distinguish row visibility from INSERT/UPDATE policy enforcement.
- **Avoid misdiagnosis:** Table owners or bypass roles can make policy tests pass incorrectly; pooled session tenant state can leak into the next request.
- **Check the result:** Alternate tenants on reused connections and test select/insert/update/delete plus indirect views/functions under the intended role.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Databases worked example](../../references/examples/database.md).
- Identity, ownership, tenant isolation, replay or privilege changes affect the task: [Identity and authorization](../../references/security/identity.md).
- The task depends on framework defaults, middleware, RLS, server/client or deployment behavior: [Framework-specific review branches](../../references/security/frameworks.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).

## Decision branches

- **When tests run as an elevated owner/service role:** Do not infer ordinary-user isolation from those results; test the intended execution identity.

## Deliver and verify

- Role/resource/action matrix with policy paths, verified and unknown isolation checks, and remediation or test proposals.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A tenant cannot read/update another tenant's rows; privileged service roles are recognized as potential policy bypasses.

## Stop and recover

- No grant/policy changes or real tenant-data probing by default. Unknown execution roles block confident isolation claims.

## Example requests

- **Normal (inspect):** Audit tenant policies and service-role bypass paths from supplied metadata.
- **Edge (inspect):** Review row policies where reads are scoped but inserts permit another tenant ID.
- **Blocked (inspect):** Inspect policy definitions without probing real tenant data or changing grants.

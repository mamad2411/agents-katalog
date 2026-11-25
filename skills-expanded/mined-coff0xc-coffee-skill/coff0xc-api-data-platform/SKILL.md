---
name: coff0xc-api-data-platform
description: "Use when the user requests API, database, data platform, CLI/SDK, or interface contracts: REST, GraphQL, OpenAPI, SQL/Postgres, schema/migration, pagination, authentication/authorization, error codes, JSON, ETL, data quality, usage ledger, filter builder, impact analysis. Manual trigger: Use coff0xc-api-data-platform."
---

# coff0xc-api-data-platform

<!-- skill-id: cs-adp-4b9e62f0 -->

## Quick Rules (read this first for everyday tasks)
> **[Contract first]** Define endpoint/action, schema, auth, error codes, pagination, versioning, and compatibility boundaries before discussing implementation.
> **[Data gate]** Make source/raw/assumptions explicit, plus migration, rollback, idempotency, audit fields, and anomalous-data handling.
> **[Delivery standard]** Output an executable contract, sample requests and responses, test/migration verification, and breaking-change notes.
> **[Hard boundary]** Confirm first for production databases, real migrations, external customer interfaces, credentials, and remote writes.

Follow this section first for ordinary API/data tasks; expand the full workflow only for cross-domain products, release gates, or major schema/auth changes.

## Capability
Engineering for APIs, databases, CLI/SDKs, and data contracts. The goal is interfaces that are usable, evolvable, and testable, and data pipelines that are migratable, traceable, and recoverable.

## What It Can Deliver
- REST/GraphQL/OpenAPI contracts
- Database schemas, migrations, and data-consistency recommendations
- CLI/SDK command design, JSON output, and error models
- Compatibility, pagination, authentication, and idempotency strategies

## What Input It Can Take
- Existing routes, schemas, OpenAPI specs, curl examples, SDKs, READMEs
- Database table structures, migration scripts, query samples
- Error logs, client call sites, data-quality issues

## Safe-Use Boundaries
- Local contract design, code implementation, and read-only checks can be done directly
- Production database migrations, data deletion, and remote API writes must be confirmed first
- Do not write real tokens, cookies, accounts, or customer data in examples
- By default only local, reversible, verifiable low-risk work; confirm first for anything involving production, credentials, payment, remote writes, deletion, publishing, or permission changes.

## Why You Can Trust It
- Discovers the existing contract style before designing changes
- Emphasizes machine-parseable output and explicit errors
- Migrations and public API changes must state their compatibility impact

## Typical Usage
```text
Use coff0xc-api-data-platform to design this billing REST API, including OpenAPI, pagination, and error codes.
Use coff0xc-api-data-platform to sort out the GraphQL queries, SQL table structure, and data-quality checks.
Use coff0xc-api-data-platform to turn these curl examples into a stable CLI and SDK plan.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.

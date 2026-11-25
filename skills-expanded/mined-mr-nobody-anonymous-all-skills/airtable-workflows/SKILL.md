---
name: airtable-workflows
description: "Model and automate Airtable bases: field types and linked records, views versus filters, the REST API and pagination, and safe bulk updates."
type: procedural
category: knowledge
domain: knowledge
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: beginner
triggers:
  - airtable api pagination
  - airtable linked records
  - airtable field types
  - airtable automation script
  - airtable bulk update
keywords:
  - airtable
  - base
  - linked-records
  - views
  - rest-api
  - pagination
source: custom
enabled: true
---

# Airtable Workflows

## Purpose

Model and automate Airtable bases: field types and linked records, views versus filters, the REST API and pagination, and safe bulk updates.

## When to Use

- A team tracks work in Airtable and needs programmatic access.
- A base schema must be designed for reliable automation.
- Bulk record updates need rate-limit-safe batching.

## When NOT to Use

- The dataset needs relational integrity and transactional writes at scale.
- You only need to view existing records a human can filter in the UI.
- The organisation restricts API tokens to specific integrations.

## Capabilities

- Design field types and linked records that survive automation.
- Query records with filters and pagination rather than full-table dumps.
- Batch create/update up to the API limit with retry on 429.
- Keep views as presentation, not as the source of truth.

## Inputs

- The base id, table names and the token's scope.
- The schema: primary field, field types, linked tables.
- The sync direction and conflict policy.

## Workflow

1. Read the schema via the metadata API before writing any code.
2. Choose filters that use indexed fields; avoid full scans of large tables.
3. Paginate with `offset` until exhausted; never assume one page.
4. Batch writes in the documented maximum size and honour 429 backoff.
5. Verify a sample of updated records and record the batch ids.

## Tools

- Airtable REST API
- Airtable MCP connector
- a scheduler for recurring syncs

## Examples

- `allskills mcp install --harness claude --servers airtable`
- `curl -s -H "Authorization: Bearer $AIRTABLE_API_KEY" "https://api.airtable.com/v0/$BASE/Tasks?maxRecords=10"`
- `allskills route "sync tickets into airtable"`

## Safety

- A token with `data.records:write` can overwrite a whole base; scope by base where possible.
- Deleting a linked record cascades relationships; export first.
- Rate limits are per base; parallel workers multiply the risk.

## Source

All-Skills canonical library (`skills/knowledge/airtable-workflows`). First-party skill, maintained in this repository.

## Notes

- Views are for humans; automate against explicit filters and field ids.
- `typecast=true` can silently change types — use it only for controlled imports.
- Pairs with: `productivity/clickup-workflows`, `data/data-contracts`.

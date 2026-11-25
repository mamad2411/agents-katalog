---
name: ontology-refresh-governance
description: Refresh the operational-to-ontology projection, validate class and property contracts, enrich changed nodes for semantic search, and inspect Oracle Scheduler evidence.
tools: [refresh_ontology_projection, inspect_ontology_term]
---

# Ontology refresh governance

## When to use

Use this procedure when operational source objects or relationships have changed, graph retrieval is stale, or the scheduled refresh reports a failure.

## Parameters

- `trigger`: `scheduler` for an installed Oracle job or `manual` for the explicit stored-procedure fallback.
- `expected_version`: ontology contract version expected by the caller.

## Steps

1. Inspect the active ontology version and `DBMS_SCHEDULER` job status.
2. Verify that the refresh procedure exists before invoking either path.
3. Prefer the enabled scheduler job for normal cadence and an operator-triggered scheduler run.
4. If the application user lacks `CREATE JOB`, report the missing least-privilege grant and call the same stored procedure directly; never claim that fallback was scheduled.
5. Project operational objects into instances and links into relationships.
6. Validate every property against its declared domain and range.
7. Re-embed only new or semantically changed nodes.
8. Record trigger type, timestamps, node/edge counts, status, and failure detail.
9. Compare the latest successful refresh with the query run that consumed it.

## Guardrails

- Do not create an Oracle native RDF network implicitly; that is a separate DBA and licensing decision.
- Do not grant `CREATE ANY JOB` to the application user.
- Do not hide a direct refresh behind a scheduler label.
- Do not delete operational source records from the ontology refresh procedure.

## Success criteria

- The refresh run is durable and reports succeeded.
- All projected edges pass domain/range validation.
- Changed nodes are searchable by semantic distance.
- Scheduler availability and the active fallback are visible to the learner.

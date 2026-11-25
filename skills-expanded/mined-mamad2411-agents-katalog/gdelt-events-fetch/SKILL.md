---
name: gdelt-events-fetch
description: Retrieve bounded GDELT 2.0 Events rows through the Tiangong CLI from the latest snapshot or an exact UTC range. Use for machine-coded event records and source-document linkage; do not use for article bodies, GKG themes, mention-level provenance, event verification, polling, bulk archival mirroring, or causal claims.
---

# GDELT Events Fetch

Use the CLI-owned `gdelt.events` capability. This Skill supplies intent routing
and result-use boundaries only; the CLI owns source discovery, input/output
schemas, HTTP and archive handling, limits, validation, and receipts.

## Before running

1. Read `references/tiangong-data-requirement.json`.
2. Use the caller- or workspace-resolved stable CLI. The requirement declares
   compatible capability and operation contract majors; it does not select a
   package build.
3. Run `data describe` with that same CLI. Continue only when the capability
   ID and required contract majors match, and copy the exact current
   capability/operation versions from that response into the run request.

```bash
tiangong-ai data describe gdelt.events --json
```

Use the returned Discovery Metadata to confirm current source coverage,
freshness, restrictions, `provides`, and `doesNotProvide`. Do not substitute
facts remembered from an older Skill revision.

## Prepare the request

Build a `tiangong.data.run-request.v1` envelope. Replace the two version
placeholders with the exact versions from the same `data describe` response. This example selects a
bounded range of source snapshots:

```json
{
  "schemaVersion": "tiangong.data.run-request.v1",
  "capabilityId": "gdelt.events",
  "capabilityVersion": "<describe.manifest.capabilityVersion>",
  "operationId": "fetch",
  "operationVersion": "<describe.manifest.operations[0].operationVersion>",
  "input": {
    "mode": "range",
    "startDateTime": "2026-03-01T12:00:00Z",
    "endDateTime": "2026-03-01T12:45:00Z",
    "maxFiles": 4
  }
}
```

Use the operation input schema returned by the same `data describe` response when choosing
`latest` or `range`. Range bounds need not align to a snapshot: the CLI selects
the first published 15-minute timestamp at or after the lower bound and stops
at `maxFiles`, even when the requested window is larger. Do not widen the
user's range or increase a safety limit without approval.

## Run

```bash
tiangong-ai data run gdelt.events fetch \
  --input /absolute/path/to/request.json --json
```

The command emits a `tiangong.data.run-result.v1` envelope. Preserve its
`contract`, `warnings`, `errors`, and `receipt` with `data` when handing the
result to another workflow.

## Result boundaries

- Treat rows as machine-coded event records, not verified real-world events,
  unique incidents, legal findings, or causal evidence.
- A source URL is lineage metadata, not an article body or proof that every
  coded field is correct. Do not claim full-text acquisition.
- Preserve GDELT identifiers and source timestamps when deduplicating or joining
  downstream; do not collapse rows merely because labels look similar.
- The capability returns normalized in-memory rows and execution metadata. It
  does not create a durable ZIP mirror, expose the master file list, or perform
  polling and incremental state management.
- Surface `partial`, truncation warnings, archive-validation failures, and empty
  results. Never reinterpret them as complete absence of events.
- Preserve file SHA-256 values and validation issues. Invalid UTF-8 or
  wrong-column rows are omitted locally while valid rows from the same verified
  ZIP remain usable; report that omission explicitly.
- Use the dedicated GKG or Mentions Skill for their row types; this Skill must
  not invoke or combine other feeds automatically.
- Cross-source comparison, persistence, scheduling, and research evidence
  admission belong to the caller or Auto Research.

## Reference

- `references/tiangong-data-requirement.json`: stable capability requirement; it is not a package lock.

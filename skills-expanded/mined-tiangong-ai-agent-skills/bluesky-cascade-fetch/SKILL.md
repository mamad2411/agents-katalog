---
name: bluesky-cascade-fetch
description: Fetch bounded public Bluesky post seeds and optional visible reply cascades through the Tiangong CLI. Use for topic, author, custom-feed, or list-feed discussion reconnaissance and reply-topology collection; do not use for private or exhaustive repository/firehose data, media downloads, representative opinion, identity or fact verification, sentiment ground truth, or causal inference.
---

# Bluesky Cascade Fetch

Use the CLI-owned `bluesky.public-posts/fetch-cascades` operation. This Skill
supplies intent routing and result-use boundaries only; the CLI TypeScript 7
runtime owns source discovery, schemas, endpoint policy, pagination, retries,
normalization, limits, partial results, and receipts.

## Before running

1. Read `references/tiangong-data-requirement.json`.
2. Use the caller- or workspace-resolved stable CLI. The requirement declares
   compatible capability and operation contract majors; it does not select a
   package build.
3. Run `data describe` with that same CLI. Continue only when the capability
   ID and required contract majors match, and copy the exact current
   capability/operation versions from that response into the run request.

```bash
tiangong-ai data describe bluesky.public-posts --json
```

Use the current Discovery Metadata to confirm source coverage, freshness,
restrictions, selection hints, `provides`, and `doesNotProvide`. Do not rely on
provider facts remembered from an older Skill revision.

## Choose the seed source

- Use `search` when the user supplied a topic or query.
- Use `author-feed` only for a named public actor view.
- Use `feed` only when the caller supplied a known public feed-generator AT-URI.
- Use `list-feed` only when the caller supplied a known public list AT-URI.
- Enable thread expansion only when visible reply topology is needed. Prefer
  seed-only retrieval when discovery breadth matters more than cascades.
- Preserve an explicit user time window and filters. Never widen or replace
  them silently.
- When diagnosing an empty historical search, repeat the same bounded request
  with `source.applyServerTimeFilter` set to `false`. Keep the client-side time
  window unchanged and classify any still-empty result as provider coverage,
  not proof that no discussion occurred.

## Prepare the request

Build one `tiangong.data.run-request.v1` envelope and validate it against the
current input schema from `data describe`. Replace both version placeholders
with the exact versions from the same `data describe` response.

```json
{
  "schemaVersion": "tiangong.data.run-request.v1",
  "capabilityId": "bluesky.public-posts",
  "capabilityVersion": "<describe.manifest.capabilityVersion>",
  "operationId": "fetch-cascades",
  "operationVersion": "<describe.manifest.operations[0].operationVersion>",
  "input": {
    "source": {
      "mode": "search",
      "query": "climate policy",
      "sort": "latest",
      "language": "en",
      "tags": ["climate"],
      "applyServerTimeFilter": true
    },
    "startDateTime": "2026-03-10T00:00:00Z",
    "endDateTime": "2026-03-11T00:00:00Z",
    "pageSize": 50,
    "expandThreads": true,
    "maxThreads": 20,
    "threadDepth": 8,
    "threadParentHeight": 5
  }
}
```

Do not put an endpoint override, credential, output path, scheduler, or
provider-specific field absent from the schema into the request. Persistence
and recurring collection belong to the caller.

## Run

```bash
tiangong-ai data run bluesky.public-posts fetch-cascades \
  --input /absolute/path/to/request.json --json
```

Preserve the complete `tiangong.data.run-result.v1` envelope, including
`contract`, `warnings`, `errors`, `summary`, and `receipt`, when handing results
to another workflow.

## Result boundaries

- Treat search ranking, feed selection, visibility, timestamps, counters, and
  thread nodes as mutable provider snapshots, not exhaustive or verified facts.
- Surface blocked/not-found nodes, failed threads, empty results, `partial`, and
  truncation. Never reinterpret them as complete absence or complete coverage.
- Retain `hitsTotal`, per-page invalid-record counts, cascade validation, and
  the fallback-host indicator; they are acquisition diagnostics, not evidence
  quality scores.
- Public posts can contain personal, sensitive, misleading, or unsafe content.
  Quote or retain only what the task requires and preserve provenance.
- Reply topology is a visible snapshot. Do not infer causation, influence,
  representativeness, identity, or sentiment labels from it alone.
- Use a separately governed repository/firehose workflow for exhaustive AT
  Protocol records and a content workflow for media or linked pages.
- Cross-source comparison, evidence admission, persistence, polling, and
  research conclusions belong to the caller or Auto Research.

## Reference

- `references/tiangong-data-requirement.json`: stable capability requirement; it is not a package lock.

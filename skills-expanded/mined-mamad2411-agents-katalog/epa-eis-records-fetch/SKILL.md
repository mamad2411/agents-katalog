---
name: epa-eis-records-fetch
description: Retrieve official U.S. EPA EIS Database result-table metadata through the Tiangong CLI. Use when a task needs Environmental Impact Statement titles, CEQ/provider IDs, document type, dates, agencies, state, detail links, or document-availability cues from a current common search or a precise search URL created in the official UI; do not use to claim linked documents were reviewed or to judge NEPA adequacy, legal sufficiency, environmental effects, compliance, or policy responsibility.
---

# EPA EIS Records Fetch

Use the CLI-owned `epa.eis-records/search` operation. This Skill supplies intent
routing, search-selection guidance, and result-use boundaries only; the CLI
TypeScript 7 runtime owns official endpoint validation, HTML parsing, schemas,
limits, retries, deduplication, partial results, and receipts.

## Before running

1. Read `references/tiangong-data-requirement.json`.
2. Use the caller- or workspace-resolved stable CLI. The requirement declares
   compatible capability and operation contract majors; it does not select a
   package build.
3. Run `data describe` with that same CLI. Continue only when the capability
   ID and required contract majors match, and copy the exact current
   capability/operation versions from that response into the run request.

```bash
tiangong-ai data describe epa.eis-records --json
```

Use the returned Discovery Metadata to confirm current source coverage,
granularity, HTML/provider limitations, selection hints, `provides`, and
`doesNotProvide`. Do not rely on objective source facts copied from an older
Skill revision.

## Choose the search

- Use `openComment` for the provider's current open-comment queue,
  `last30Published` for recently published records, `last60Issued` for recently
  issued records, or `lastWeek` for the provider's last-week view.
- For a precise project or historical query, first build and review that search
  in the official EPA EIS Database UI, then copy its complete HTTPS search URL
  into `searchUrls`. The CLI rejects non-EPA origins and non-search paths.
- Common searches run before explicit URLs, while each group preserves caller
  order. Use more than one only when the evidence need and coverage plan call
  for multiple provider result surfaces.
- Empty or sparse output applies only to the selected search page. It is not
  proof that EPA, CEQ, another agency, or the real world has no relevant EIS.

## Prepare the request

Build one `tiangong.data.run-request.v1` envelope. Replace the version
placeholders with the exact versions from the same `data describe` response and validate `input` against the current
schema returned by `data describe`. The example demonstrates both selector
types; remove the one not required for the task.

```json
{
  "schemaVersion": "tiangong.data.run-request.v1",
  "capabilityId": "epa.eis-records",
  "capabilityVersion": "<describe.manifest.capabilityVersion>",
  "operationId": "search",
  "operationVersion": "<describe.manifest.operations[0].operationVersion>",
  "input": {
    "commonSearches": ["openComment"],
    "searchUrls": [
      "https://cdxapps.epa.gov/cdx-enepa-II/public/action/eis/search?search=Glen+Canyon&state=CO"
    ]
  }
}
```

Use run-request `limits` only when intentionally lowering the manifest's
search-page or record ceiling. Do not place output paths, retry settings, a
custom base URL, credentials, or document download instructions in `input`.

## Run

```bash
tiangong-ai data run epa.eis-records search \
  --input /absolute/path/to/request.json --json
```

Preserve the complete `tiangong.data.run-result.v1` envelope, including
`contract`, `warnings`, `errors`, `observations`, and `receipt`, with `data`.

## Result boundaries

- Treat `partial` as a failed later search surface: retain successful records
  and report the missing search. Treat `blocked` as no usable result, including
  an unrecognized provider page after HTML drift.
- Preserve page provenance, CEQ number, unique ID, document type, dates,
  agencies, state, detail URL, and download cues. Deduplication is by official
  identifiers; it does not establish that similarly titled records are the
  same project or action.
- Download links and IDs are availability cues only. Do not claim any linked
  EIS, notice, comment letter, or attachment was downloaded, parsed, reviewed,
  or admitted as evidence.
- Provider metadata does not decide NEPA adequacy, legal sufficiency,
  environmental effects, agency compliance, causality, policy responsibility,
  or report conclusions. Those require separately governed document
  acquisition and analysis.
- HTML parsing, durable artifact placement, document acquisition,
  normalization, evidence admission, and cross-source synthesis remain outside
  this thin Skill.

## Reference

- `references/tiangong-data-requirement.json`: stable capability requirement; it is not a package lock.

---
name: nasa-firms-fire-fetch
description: Retrieve bounded NASA FIRMS satellite active-fire and thermal-anomaly point detections through the Tiangong CLI for one reviewed source, known bounding box, and short UTC date window. Use for hotspot screening or candidate fire-location context; do not use for fire perimeters, burned area, confirmed wildfire incidents, cause attribution, emergency alerts, recurring monitoring, or multi-source fusion.
---

# NASA FIRMS Active Fire

Use the CLI-owned `nasa-firms.active-fire` capability. This Skill supplies
intent routing and result-use boundaries only; the CLI owns source discovery,
input/output schemas, MAP_KEY injection, chunking, limits, validation, and
receipts.

## Before running

1. Read `references/tiangong-data-requirement.json`.
2. Use the caller- or workspace-resolved stable CLI. The requirement declares
   compatible capability and operation contract majors; it does not select a
   package build.
3. Run `data describe` with that same CLI. Continue only when the capability
   ID and required contract majors match, and copy the exact current
   capability/operation versions from that response into the run request.
4. Ensure `NASA_FIRMS_MAP_KEY` is present in the CLI process environment, then
   run the default static doctor. Never place the key in argv, the request JSON,
   a Skill-local config file, logs, or output.

```bash
tiangong-ai data describe nasa-firms.active-fire --json
tiangong-ai data doctor nasa-firms.active-fire --json
```

Use the returned Discovery Metadata to confirm current source availability,
coverage, granularity, NRT or Standard Processing semantics, citation guidance,
quota, `provides`, and `doesNotProvide`. Do not substitute facts remembered
from an older Skill revision. A blocked static doctor means the required
logical credential is unavailable; stop instead of bypassing the CLI.

## Prepare the request

Build a `tiangong.data.run-request.v1` envelope and replace the two version
placeholders with the exact versions from the same `data describe` response. Use one source and one known WGS84
bounding box that does not cross the antimeridian. The inclusive UTC date
window may contain at most 31 dates; the CLI performs provider-compliant
five-day chunking and enforces transaction and record limits.

```json
{
  "schemaVersion": "tiangong.data.run-request.v1",
  "capabilityId": "nasa-firms.active-fire",
  "capabilityVersion": "<describe.manifest.capabilityVersion>",
  "operationId": "fetch-area",
  "operationVersion": "<describe.manifest.operations[0].operationVersion>",
  "input": {
    "source": "VIIRS_NOAA20_NRT",
    "boundingBox": {
      "west": 115.8,
      "south": -8.9,
      "east": 116.3,
      "north": -8.3
    },
    "startDate": "2026-03-01",
    "endDate": "2026-03-07",
    "checkAvailability": true
  }
}
```

Use the operation input schema returned by the same `data describe` response for the current
source enum and limits. Select NRT only when timeliness is material and its
provisional status can be retained; select the matching Standard Processing
source for consistent historical work when available. Set
`checkAvailability` when the source's historical window is uncertain, accepting
the extra provider request. Do not silently widen the box, switch sources,
geocode place names, cross the antimeridian, or fan out across areas.

## Run

```bash
tiangong-ai data run nasa-firms.active-fire fetch-area \
  --input /absolute/path/to/request.json --json
```

The command emits a `tiangong.data.run-result.v1` envelope. Preserve its
`contract`, `warnings`, `errors`, and `receipt` with `data` when handing the
result to another workflow.

## Result boundaries

- Treat each record as a satellite thermal-anomaly or active-fire detection,
  not a fire perimeter, burned-area estimate, incident identity, or proof of a
  wildfire or ignition cause.
- Preserve source, acquisition time, satellite/instrument, confidence,
  day/night, version, and sensor measurements with every downstream use.
- Preserve NRT provisional warnings and the exact selected dataset in citations.
  Do not merge NRT and Standard Processing records without an explicit method.
- Treat `partial` as incomplete chunk or row coverage. Report missing chunks
  and invalid paths together with the usable detections.
- Preserve duplicate/inconsistent-header and row-validation issues. Rows with
  invalid required coordinates or acquisition timestamps are omitted, while a
  duplicate optional header or malformed optional measurement does not discard
  an otherwise usable detection.
- Treat `blocked` as no usable business result. Surface credential, request,
  availability, endpoint, quota, or provider errors instead of bypassing limits
  or switching endpoints.
- Report record-limit truncation and transaction estimates; a truncated result
  is not exhaustive evidence of hotspot absence or presence.
- Confirm operationally important detections with incident, perimeter, imagery,
  or local-authority sources. This capability supplies no alert, evacuation,
  severity, containment, smoke, emissions, weather, or hydrology decision.
- Recurring monitoring, multi-area or multi-source fan-out, duplicate-event
  resolution, statistical inference, and research evidence admission belong to
  the caller or Auto Research, not this atomic Skill.
- This execution contract does not expose the source script's standalone
  MAP_KEY-status probe, arbitrary sensor-specific raw columns, or raw JSON/log
  artifact output. Use the static doctor plus an explicit bounded operation;
  add any future live quota diagnostic as a separately reviewed CLI contract.

## Reference

- `references/tiangong-data-requirement.json`: stable capability requirement; it is not a package lock.

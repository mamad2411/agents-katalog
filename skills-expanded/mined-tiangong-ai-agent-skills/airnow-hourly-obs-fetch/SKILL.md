---
name: airnow-hourly-obs-fetch
description: Retrieve preliminary U.S. EPA AirNow HourlyAQObs monitoring-site records through the Tiangong CLI for an inclusive UTC-hour window, WGS84 bounding box, and pollutant list. Use for site-hour observations with source-file lineage; do not use for regulatory AQS compliance data, forecasts, health guidance, exposure estimates, or place-name geocoding.
---

# AirNow Hourly Observations

Use the CLI-owned `airnow.hourly-observations` capability. This Skill supplies
intent routing and result-use boundaries only; the CLI owns source discovery,
input/output schemas, HTTP behavior, limits, validation, and receipts.

## Before running

1. Read `references/tiangong-data-requirement.json`.
2. Use the caller- or workspace-resolved stable CLI. The requirement declares
   compatible capability and operation contract majors; it does not select a
   package build.
3. Run `data describe` with that same CLI. Continue only when the capability
   ID and required contract majors match, and copy the exact current
   capability/operation versions from that response into the run request.

```bash
tiangong-ai data describe airnow.hourly-observations --json
```

Use the returned Discovery Metadata to confirm current source coverage,
freshness, restrictions, `provides`, and `doesNotProvide`. Do not substitute
facts remembered from an older Skill revision.

## Prepare the request

Build a `tiangong.data.run-request.v1` envelope. Replace the two version
placeholders with the exact versions from the same `data describe` response. The operation input requires
hour-aligned UTC timestamps, a WGS84 bounding box, and one or more supported
pollutant identifiers:

```json
{
  "schemaVersion": "tiangong.data.run-request.v1",
  "capabilityId": "airnow.hourly-observations",
  "capabilityVersion": "<describe.manifest.capabilityVersion>",
  "operationId": "fetch-hourly",
  "operationVersion": "<describe.manifest.operations[0].operationVersion>",
  "input": {
    "startDateTimeUtc": "2026-03-22T00:00:00Z",
    "endDateTimeUtc": "2026-03-22T06:00:00Z",
    "boundingBox": {
      "minLongitude": -123.5,
      "minLatitude": 37.0,
      "maxLongitude": -121.5,
      "maxLatitude": 38.8
    },
    "parameters": ["PM25", "OZONE"]
  }
}
```

Use the operation input schema returned by the same `data describe` response when selecting
fields or values under `input`. Do not infer unsupported aliases or silently
widen the requested time or geographic range.

## Run

```bash
tiangong-ai data run airnow.hourly-observations fetch-hourly \
  --input /absolute/path/to/request.json --json
```

The command emits a `tiangong.data.run-result.v1` envelope. Preserve its
`contract`, `warnings`, `errors`, and `receipt` with `data` when handing the
result to another workflow.

## Result boundaries

- Treat `partial` as incomplete coverage and report missing or invalid hourly
  files; never convert missing observations to zero.
- Treat `blocked` as no usable business result and surface the structured
  errors instead of retrying with broader inputs.
- Do not interpret AQI as health advice, estimate exposure, interpolate between
  sites, combine other sources, or use preliminary AirNow records for
  regulatory compliance.
- Cross-source comparison and research evidence admission belong to the caller
  or Auto Research, not this atomic Skill.

## Reference

- `references/tiangong-data-requirement.json`: stable capability requirement; it is not a package lock.

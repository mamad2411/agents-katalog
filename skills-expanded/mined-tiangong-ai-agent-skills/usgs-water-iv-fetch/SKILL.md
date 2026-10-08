---
name: usgs-water-iv-fetch
description: Retrieve USGS WaterServices instantaneous station observations through the Tiangong CLI for one bounded numeric area or an explicit site list and one bounded time selector. Use for streamflow, gage-height, or other USGS time-series measurements with qualifiers; do not use for station discovery, daily values, flood-stage classification, forecasts, hazard advice, or workflows that require guaranteed service after the legacy API retires.
---

# USGS Water Instantaneous Values

Use the CLI-owned `usgs.water-instantaneous-values` capability. This Skill
supplies intent routing and result-use boundaries only; the CLI owns source
discovery, input/output schemas, HTTP behavior, limits, validation, and
receipts.

## Before running

1. Read `references/tiangong-data-requirement.json`.
2. Use the caller- or workspace-resolved stable CLI. The requirement declares
   compatible capability and operation contract majors; it does not select a
   package build.
3. Run `data describe` with that same CLI. Continue only when the capability
   ID and required contract majors match, and copy the exact current
   capability/operation versions from that response into the run request.
4. Run the default static doctor. Do not add `--live` unless the user explicitly
   asks for a provider probe.

```bash
tiangong-ai data describe usgs.water-instantaneous-values --json
tiangong-ai data doctor usgs.water-instantaneous-values --json
```

Use the returned Discovery Metadata to confirm current source coverage,
freshness, decommission status, restrictions, `provides`, and
`doesNotProvide`. Prefer a modern USGS Water Data capability when the task
requires operation beyond the legacy service lifetime. USGS currently warns
that decommission preparation can include intentional degradation or blackouts
during the second half of 2026, before the planned 2027-Q1 retirement; treat
such failures as provider-interface availability problems, not evidence that
water observations are absent.

## Prepare the request

Build a `tiangong.data.run-request.v1` envelope and replace the two version
placeholders with the exact versions from the same `data describe` response. Under `input`, choose exactly
one spatial selector (`boundingBox` or `siteNumbers`) and exactly one time
selector (`period` or a paired explicit start/end window):

```json
{
  "schemaVersion": "tiangong.data.run-request.v1",
  "capabilityId": "usgs.water-instantaneous-values",
  "capabilityVersion": "<describe.manifest.capabilityVersion>",
  "operationId": "fetch",
  "operationVersion": "<describe.manifest.operations[0].operationVersion>",
  "input": {
    "boundingBox": {
      "minLongitude": -77.3,
      "minLatitude": 38.8,
      "maxLongitude": -77.0,
      "maxLatitude": 39.1
    },
    "period": "P1D",
    "parameterCodes": ["00060", "00065"],
    "siteType": "ST",
    "siteStatus": "active"
  }
}
```

Use the operation input schema returned by the same `data describe` response for current field
semantics and limits. Preserve leading zeroes in site and parameter identifiers.
Do not infer site numbers from place names, widen an area or time range without
the user's intent, or mix selectors that the schema declares exclusive. The
reviewed contract accepts at most 100 exact site IDs, one bbox whose coordinate
span product is at most 25 square degrees, and one to eight parameter codes.
`period` must be a positive ISO-8601 duration; do not use a zero duration,
append an empty `T`, or mix week notation with other duration components.

## Run

```bash
tiangong-ai data run usgs.water-instantaneous-values fetch \
  --input /absolute/path/to/request.json --json
```

The command emits a `tiangong.data.run-result.v1` envelope. Preserve its
`contract`, `warnings`, `errors`, and `receipt` with `data` when handing the
result to another workflow.

## Result boundaries

- Treat qualifier `P` and `provisional: true` as provider warnings that values
  may change; retain qualifiers with any downstream use.
- Treat `partial` as incomplete normalization coverage and report the affected
  series or value paths. Do not convert missing or invalid observations to
  zero.
- Treat `blocked` as no usable business result and surface the structured
  errors instead of silently broadening the query or bypassing limits.
- Report record-limit truncation; do not imply that a truncated result is an
  exhaustive time series.
- A zero or sparse provider result can reflect selector choice, activity
  status, site/parameter coverage, outage, or a local data-retention limit; it
  does not prove that streamflow, water-level change, or flood effects were
  absent. Some operational parameters that are not quality assured, such as
  temperature or precipitation, can be limited by the responsible USGS center
  to 120 days or less.
- Do not infer flood stage, return period, alert status, hazard, cause, or
  policy meaning from raw station observations.
- Cross-source comparison and research evidence admission belong to the caller
  or Auto Research, not this atomic Skill.

## Reference

- `references/tiangong-data-requirement.json`: stable capability requirement; it is not a package lock.

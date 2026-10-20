---
name: gbfs
description: >-
  GBFS: This document explains the types of files and data that comprise the General Bikeshare Feed Specification (GBFS) and defines the fields used in all of those files. Covers GBFS 3.0. Use when publishing bike-share data. Triggers: GBFS.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# GBFS

The General Bikeshare Feed Specification from MobilityData: the JSON files a shared mobility system publishes (gbfs.json, system_information.json, station and vehicle status and the rest), how they are distributed and versioned, and the field types they use, read from gbfs.md at the v3.0 tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: GBFS feed producer (system operator or publisher) or feed consumer (trip planner, aggregator or validator).
- Target version: GBFS 3.0 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Files.** "To avoid circular references this file MUST NOT contain links to `manifest.json`."
2. **Feed Availability.** "Producers MUST provide a technical contact who can respond to feed outages in the `feed_contact_email` field in the `system_information.json` file."
3. **File Requirements.** "All files MUST be valid JSON"
4. **File Requirements.** "All data MUST be UTF-8 encoded"
5. **File Distribution.** "REQUIRED files MUST NOT 404. They MUST return a properly formatted JSON file as defined in [Output Format](#output-format)."
6. **Field Types, Boolean.** "Boolean values MUST be JSON booleans, not strings (meaning `true` or `false`, not `"true"` or `"false"`)."
7. **Field Types, ID.** "An exception is `vehicle_id`, which MUST NOT be persistent for privacy reasons (see `vehicle_status.json`)."
8. **Field Types, Timestamp.** "Timestamp fields MUST be represented as strings in [RFC3339 format](https://www.rfc-editor.org/rfc/rfc3339), for example `2023-07-17T13:34:13+02:00`."
9. **system_information.json.** "Each distinct system or geographic area in which vehicles are operated MUST have its own unique `system_id`."
10. **station_information.json.** "Any station that is represented in `station_information.json` MUST have a corresponding entry in `station_status.json`."
11. **vehicle_status.json.** "Vehicles that are not accessible (for example, in a warehouse or in transit) MUST NOT appear as available for rental."
12. **vehicle_status.json.** "The `vehicle_id` identifier MUST be rotated to a random string after each trip to protect user privacy"

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `json`, `geojson`, `gtfs`, `language-tags`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [GBFS 3.0](https://raw.githubusercontent.com/MobilityData/gbfs/v3.0/gbfs.md): Specification, GBFS v3.0 (git tag v3.0), checked 2026-10-06.

---
name: gtfs
description: >-
  GTFS: This document defines the format and structure of the files that comprise a GTFS dataset. Covers GTFS Schedule, GTFS Realtime. Use when publishing transit data. Triggers: GTFS.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# GTFS

This document defines the format and structure of the files that comprise a GTFS dataset.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when publishing transit data.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: GTFS Schedule (default); GTFS Realtime (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document Conventions &para;.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", “SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119 ."
2. **Linked trips &para;.** "The trips linked together MUST be operated by the same vehicle."
3. **Linked trips &para;.** "The last stop of from_trip_id SHOULD be geographically close to the first stop of to_trip_id , and the last arrival time of from_trip_id SHOULD be prior but close to the first departure time of to_trip_id ."
4. **Linked trips &para;.** "For example, two train trips (trip A and trip B in the diagram below) can merge into a single train trip (trip C) after a vehicle coupling operation at a common station: In a 1-to-n continuation, the trips.service_id for each to_trip_id MUST be identical."
5. **Linked trips &para;.** "In an n-to-1 continuation, the trips.service_id for each from_trip_id MUST be identical."
6. **Linked trips &para;.** "Trips may be linked together as part of multiple distinct continuations, provided that the trip.service_id MUST NOT overlap on any day of service."
7. **Term Definitions &para;.** "Datasets should be published at a public, permanent URL, including the zip file name."
8. **Term Definitions &para;.** "Text-to-speech field - The field should contain the same information than its parent field (on which it falls back if it is empty)."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [GTFS Schedule](https://gtfs.org/schedule/reference/): Specification, GTFS Schedule, fetched 2026-10-06 (Specification, 2026-10-06), checked 2026-10-06.
- [GTFS Realtime](https://gtfs.org/realtime/reference/): Specification, GTFS Realtime, fetched 2026-10-06 (Specification, 2026-10-06), checked 2026-10-06.

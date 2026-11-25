---
name: geolocation
description: >-
  Geolocation: Geolocation provides access to geographical location information associated with the hosting device. Covers Geolocation (build). Use when reading a device position. Triggers: Geolocation, getCurrentPosition.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Geolocation

Geolocation provides access to geographical location information associated with the hosting device.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading a device position.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Geolocation API 2016 (legacy: read and upgrade, never author); Geolocation (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **6.4.** "clearWatch() method When clearWatch() is invoked, the user agent MUST : Remove watchId from this 's [[watchIDs]] ."
2. **6.5.** "User agents MUST consider invoking set emulated position data as a significant change."
3. **12..** "User agents MUST consider this as a "significant change" in the wait for a significant change of geographic position step."
4. **13. Conformance.** "The key words MAY , MUST , and RECOMMENDED in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
5. **6.6.** "If permission is "granted": Check if an emulated position should be used by running the following steps: Let emulatedPositionData be get emulated position data passing this ."

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

- [Geolocation API 2016](https://www.w3.org/TR/2016/REC-geolocation-API-20161108/): Recommendation, geolocation-2016 REC-geolocation-API-20161108 (Recommendation, 2016-11-08), checked 2026-10-06.
- [Geolocation](https://www.w3.org/TR/geolocation/): Candidate Recommendation Snapshot, geolocation CR-geolocation-20260326 (Candidate Recommendation Snapshot, 2026-03-26), checked 2026-10-06.

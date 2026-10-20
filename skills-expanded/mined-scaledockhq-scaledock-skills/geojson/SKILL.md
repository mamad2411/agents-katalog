---
name: geojson
description: >-
  GeoJSON (RFC 7946): read and write geographic features, geometries and coordinates as JSON. Covers RFC 7946 The GeoJSON Format. Use when reading or writing GeoJSON. Triggers: GeoJSON, RFC 7946.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# The GeoJSON Format

The GeoJSON Format

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading or writing GeoJSON.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 7946 The GeoJSON Format (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 7946 § 3.** "A GeoJSON object has a member with the name "type". The value of the member MUST be one of the GeoJSON types."
2. **RFC 7946 § 3.1.** "The value of a Geometry object's "type" member MUST be one of the seven geometry types (see Section 1.4)."
3. **RFC 7946 § 3.1.6.** "The first and last positions are equivalent, and they MUST contain identical values; their representation SHOULD also be identical."
4. **RFC 7946 § 3.1.6.** "A linear ring MUST follow the right-hand rule with respect to the area it bounds, i.e., exterior rings are counterclockwise, and holes are clockwise."
5. **RFC 7946 § 3.1.6.** "For Polygons with more than one of these rings, the first MUST be the exterior ring, and any others MUST be interior rings."
6. **RFC 7946 § 3.1.9.** "Any geometry that crosses the antimeridian SHOULD be represented by cutting it in two such that neither part's representation crosses the antimeridian."
7. **RFC 7946 § 3.2.** "The value of the geometry member SHALL be either a Geometry object as defined above or, in the case that the Feature is unlocated, a JSON null value."
8. **RFC 7946 § 5.** "The value of the bbox member MUST be an array of length 2*n where n is the number of dimensions represented in the contained geometries, with all axes of the most southwesterly point followed by all axes of the more northeasterly point."
9. **RFC 7946 § 7.1.** "Implementations MUST NOT change the semantics of GeoJSON members and types."
10. **RFC 7946 § 7.1.** "FeatureCollection and Feature objects, respectively, MUST NOT contain a "coordinates" or "geometries" member."
11. **RFC 7946 § 7.1.** "FeatureCollection and Geometry objects, respectively, MUST NOT contain a "geometry" or "properties" member."

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
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 7946 The GeoJSON Format](https://www.rfc-editor.org/rfc/rfc7946.html): PROPOSED STANDARD, RFC 7946 (PROPOSED STANDARD, August 201), checked 2026-10-06.

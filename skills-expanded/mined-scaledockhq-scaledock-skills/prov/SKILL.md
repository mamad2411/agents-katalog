---
name: prov
description: >-
  PROV: Provenance is information about entities, activities, and people involved in producing a piece of data or thing, which can be used to form assessments about its quality, reliability or trustworthiness. Covers PROV-DM: The PROV Data Model, PROV-O: The PROV Ontology, PROV-N: The Provenance Notation. Use when recording provenance. Triggers: PROV, PROV-O, PROV-DM.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# PROV

Provenance is information about entities, activities, and people involved in producing a piece of data or thing, which can be used to form assessments about its quality, reliability or trustworthiness. PROV-DM is the conceptual data model that forms a basis for the W3C provenance (PROV) family of specifications. PROV-DM distinguishes core structures, forming the essence of provenance information, from extended structures catering for more specific uses of provenance. PROV-DM is organized in six components, respectively dealing with: (1) entities and activities, and the time at which they were created, used, or ended; (2) derivations of entities from entities; (3) agents bearing responsibilit

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when recording provenance.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: PROV-DM: The PROV Data Model (default); PROV-O: The PROV Ontology (default); PROV-N: The Provenance Notation (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.3 Notational Conventions.** "The key words " MUST ", " MUST NOT ", " REQUIRED ", " SHALL ", " SHALL NOT ", " SHOULD ", " SHOULD NOT ", " RECOMMENDED ", " MAY ", and " OPTIONAL " in this document are to be interpreted as described in [ RFC2119 ]."
2. **5.1.3 Generation.** "While each of id , activity , time , and attributes is OPTIONAL , at least one of them MUST be present."
3. **5.1.4 Usage.** "While each of id , entity , time , and attributes is OPTIONAL , at least one of them MUST be present."
4. **5.1.6 Start.** "While each of id , trigger , starter , time , and attributes is OPTIONAL , at least one of them MUST be present."
5. **5.1.7 End.** "While each of id , trigger , ender , time , and attributes is OPTIONAL , at least one of them MUST be present."
6. **5.3.3 Association.** "While each of id , agent , plan , and attributes is OPTIONAL , at least one of them MUST be present."
7. **5.7.2.1 prov:label.** "The value associated with the attribute prov:label MUST be a string."
8. **5.7.2.2 prov:location.** "The value associated with the attribute prov:location MUST be a PROV-DM Value , expected to denote a location."

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

- [PROV-DM: The PROV Data Model](https://www.w3.org/TR/prov-dm/): Recommendation, prov-dm REC-prov-dm-20130430 (Recommendation, 2013-04-30), checked 2026-10-06.
- [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/): Recommendation, prov-o REC-prov-o-20130430 (Recommendation, 2013-04-30), checked 2026-10-06.
- [PROV-N: The Provenance Notation](https://www.w3.org/TR/prov-n/): Recommendation, prov-n REC-prov-n-20130430 (Recommendation, 2013-04-30), checked 2026-10-06.

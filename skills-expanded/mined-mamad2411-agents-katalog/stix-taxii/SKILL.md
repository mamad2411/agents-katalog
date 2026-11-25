---
name: stix-taxii
description: >-
  STIX and TAXII 2.1: represent cyber threat intelligence as STIX objects and share it over TAXII. Covers STIX 2.1, TAXII 2.1. Use when sharing cyber threat intelligence. Triggers: STIX, TAXII.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# STIX and TAXII

https://docs.oasis-open.org/cti/stix/v2.1/errata01/csd01/stix-v2.1-errata01-csd01-complete.md

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when sharing cyber threat intelligence.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: STIX 2.1 (default); TAXII 2.1 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Key words:.** "The key words “ MUST ”, “ MUST NOT ”, “ REQUIRED ”, “ SHALL ”, “ SHALL NOT ”, “ SHOULD ”, “ SHOULD NOT ”, “ RECOMMENDED ”, “ NOT RECOMMENDED ”, “ MAY ”, and “ OPTIONAL ” in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **2. Common Data Types.** "The phrasing “ list of type <type> ” is used to indicate that all values within the list MUST conform to the specified type."
3. **2.1 Binary.** "In order to allow pattern matching on custom objects, for all properties that use the binary type, the property name MUST end with _bin ."
4. **2.1 Binary.** "Other serializations SHOULD use a native binary type, if available."
5. **2.2 Boolean.** "Properties with this type MUST have a value of true or false ."
6. **2.3 Dictionary.** "Dictionary keys MUST be unique in each dictionary, MUST be in ASCII, and are limited to the characters a-z (lowercase ASCII), A-Z (uppercase ASCII), numerals 0-9, hyphen (-), and underscore (_)."
7. **2.3 Dictionary.** "Dictionary keys MUST be no longer than 250 ASCII characters in length and SHOULD be lowercase."
8. **2.3 Dictionary.** "Empty dictionaries are prohibited in STIX and MUST NOT be used as a substitute for omitting the property if it is optional."

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

- [STIX 2.1](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html): OASIS Standard, STIX 2.1, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.
- [TAXII 2.1](https://docs.oasis-open.org/cti/taxii/v2.1/taxii-v2.1.html): OASIS Standard, TAXII 2.1, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.

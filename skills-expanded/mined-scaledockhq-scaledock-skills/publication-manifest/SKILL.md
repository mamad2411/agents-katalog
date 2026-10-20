---
name: publication-manifest
description: >-
  Publication Manifest: This specification defines a general manifest format for expressing information about a digital publication. Covers Publication Manifest, Audiobooks. Use when writing a publication manifest or audiobook. Triggers: Publication Manifest, Audiobooks.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Publication Manifest

This specification defines a general manifest format for expressing information about a digital publication. It uses [ schema.org ] metadata augmented to include various structural properties about publications, serialized in [ json-ld11 ], to enable interoperability between publishing formats while accommodating variances in the information that needs to be expressed.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when writing a publication manifest or audiobook.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Publication Manifest (default); Audiobooks (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.3 JSON-LD Authoring and.** "This means that the manifest SHOULD be expressed using only the syntactic constructions defined in this specification, as opposed to all the possibilities offered by the JSON-LD syntax."
2. **3. Conformance.** "The key words MAY , MUST , MUST NOT , OPTIONAL , RECOMMENDED , REQUIRED , SHOULD , and SHOULD NOT in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
3. **4.1 Requirements.** "The following properties MUST be set in the manifest: context conformsTo The following properties are RECOMMENDED : type id The priority of all other properties and resource relations is OPTIONAL , but MAY be modified by implementations of the manifest format."
4. **4.2.1 Literals.** "When a manifest property expects a literal text string — one that is not language-dependent, such as a code value or date — as its value, the value MUST be expressed as a [ json ] string ."
5. **4.2.2 Numbers.** "When a manifest property expects a number as its value, the value MUST be expressed as a [ json ] number ."
6. **4.2.3 Booleans.** "When a manifest property expects a boolean as its value, the value MUST be expressed as an [ ecmascript ] Boolean value ( true or false )."
7. **4.2.4.1 Localizable Strings.** "When a manifest property expects a localizable text string as its value, the value MUST be expressed as one of: a [ json ] string value; or a LocalizableString ."
8. **4.2.4.2 Entities.** "When a manifest property expects an entity (i.e., an individual or organization responsible for the various aspects of creation), its value MUST be expressed either as: a [ json ] string value; or an Entity ."

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

- [Publication Manifest](https://www.w3.org/TR/pub-manifest/): Recommendation, pub-manifest REC-json-ld-20140116 (Recommendation, 2020-11-10), checked 2026-10-06.
- [Audiobooks](https://www.w3.org/TR/audiobooks/): Recommendation, audiobooks REC-audiobooks-20201110 (Recommendation, 2020-11-10), checked 2026-10-06.

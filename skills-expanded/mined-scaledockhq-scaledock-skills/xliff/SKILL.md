---
name: xliff
description: >-
  XLIFF: write and read XML Localization Interchange File Format documents. Covers XLIFF 2.1 (current) and XLIFF 2.2 Committee Specification 01 as a preview, with Part 1 Core and Part 2 Extended and the Plural, Gender, and Select Module. Use when exchanging localizable content. Triggers: XLIFF.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# XLIFF

http://docs.oasis-open.org/xliff/xliff-core/v2.1/os/xliff-core-v2.1-os.pdf http://docs.oasis-open.org/xliff/xliff-core/v2.1/os/xliff-core-v2.1-os.xml

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when exchanging localizable content.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: XLIFF 2.1 (default); XLIFF 2.2 (preview, posture: build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1.1 Key words.** "The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL are to be interpreted as described in [ RFC 2119 ]."
2. **2 Conformance.** "Document Conformance XLIFF is an XML vocabulary, therefore conformant XLIFF Documents MUST be well formed and valid [XML] documents."
3. **2 Conformance.** "Conformant XLIFF Documents MUST be valid instances of the official Core XML Schema ( http://docs.oasis-open.org/xliff/xliff-core/v2.1/os/schemas/xliff_core_2.0.xsd ) that is a part of this multipart Work Product."
4. **2 Conformance.** "As not all aspects of the XLIFF specification can be expressed in terms of XML Schemas, conformant XLIFF Documents MUST also comply with all relevant elements and attributes definitions, normative usage descriptions, and Constraints specified in this specification document."
5. **2 Conformance.** "Application Conformance XLIFF Writers MUST create conformant XLIFF Documents to be considered XLIFF compliant."
6. **2 Conformance.** "Agents processing conformant XLIFF Documents that contain custom extensions are not REQUIRED to understand and process non-XLIFF elements or attributes."
7. **2 Conformance.** "However, conformant applications SHOULD preserve existing custom extensions when processing conformant XLIFF Documents , provided that the elements that contain custom extensions are not removed according to XLIFF Processing Requirements or the extension's own processing requirements."
8. **2 Conformance.** "All Agents MUST comply with Processing Requirements for otherwise unspecified Agents or without a specifically set target Agent ."

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

- [XLIFF 2.1](https://docs.oasis-open.org/xliff/xliff-core/v2.1/os/xliff-core-v2.1-os.html): OASIS Standard, XLIFF 2.1, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.
- [XLIFF 2.2 Part 1: Core](https://docs.oasis-open.org/xliff/xliff-core/v2.2/cs01/xliff-core-v2.2-cs01-part1.html): Committee Specification, XLIFF 2.2 Committee Specification 01, 2025-03-13, checked 2026-10-06.
- [XLIFF 2.2 Part 2: Extended](https://docs.oasis-open.org/xliff/xliff-core/v2.2/cs01/xliff-extended-v2.2-cs01-part2.html): Committee Specification, XLIFF 2.2 Committee Specification 01, 2025-03-13, checked 2026-10-06.

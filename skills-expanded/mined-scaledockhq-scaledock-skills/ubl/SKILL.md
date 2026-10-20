---
name: ubl
description: >-
  UBL 2.4: exchange business documents such as orders and invoices in OASIS Universal Business Language XML. Covers UBL 2.4. Use when exchanging business documents. Triggers: UBL, Universal Business Language.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# UBL

This stage: https://docs.oasis-open.org/ubl/os-UBL-2.4/UBL-2.4.html https://docs.oasis-open.org/ubl/os-UBL-2.4/UBL-2.4.pdf https://docs.oasis-open.org/ubl/os-UBL-2.4/UBL-2.4.xml

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when exchanging business documents.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: UBL 2.4 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4.2 Validation.** "[IND1] All UBL instance documents SHALL validate to a corresponding schema."
2. **4.3 Character Encoding.** "Processors SHALL understand which character encoding is employed in each XML document."
3. **4.3 Character Encoding.** "[IND2] All UBL instance documents SHALL identify their character encoding within the XML declaration."
4. **4.3 Character Encoding.** "[IND3] In conformance with ISO IEC ITU UN/CEFACT eBusiness Memorandum of Understanding Management Group (MOUMG) Resolution 01/08 (MOU/MG01n83) as agreed to by OASIS, all UBL XML SHOULD be expressed using UTF-8."
5. **4.4 Empty Elements.** "[IND5] UBL-conforming instance documents SHALL NOT contain an element devoid of content or containing null values."
6. **4.4 Empty Elements.** "[IND6] The absence of a construct or data in a UBL instance document SHALL NOT carry meaning."
7. **4.6 Empty Attributes.** "[IND9] UBL-conforming instance documents SHALL NOT contain an attribute devoid of content or containing null values."
8. **4.7 Semantic definitions.** "To facilitate interoperability, implementations SHOULD follow these definitions to ensure the successful interchange of the business information."

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

- [UBL 2.4](https://docs.oasis-open.org/ubl/os-UBL-2.4/UBL-2.4.html): OASIS Standard, UBL 2.4, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.

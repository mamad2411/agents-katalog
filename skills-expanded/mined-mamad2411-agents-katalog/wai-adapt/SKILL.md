---
name: wai-adapt
description: >-
  WAI-Adapt: This specification provides web content authors a standard approach to support web users with various cognitive and learning disabilities who: Customarily communicate using symbolic languages generally known as Augmentative and Alternative Communications ( AAC ); Need more familiar icons (and other graphical symbols) in order to comprehend page content; The technology described in this specification is intended to be used to programmatically transform the appearance of typical web content including form controls, icons, and other user interface elements into a rendering incorporating an individual user's preferred AAC symbols. Covers WAI-Adapt: Symbols Module Level 1.0 (build), WAI-Adapt: Help and Support Module Level 1.0 (track), WAI-Adapt: Tools Module Level 1.0 (track). Use when adapting content with WAI-Adapt symbols or related modules. Triggers: WAI-Adapt, adapt-symbols, AAC.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# WAI-Adapt

This specification provides web content authors a standard approach to support web users with various cognitive and learning disabilities who: Customarily communicate using symbolic languages generally known as Augmentative and Alternative Communications ( AAC ); Need more familiar icons (and other graphical symbols) in order to comprehend page content; The technology described in this specification is intended to be used to programmatically transform the appearance of typical web content including form controls, icons, and other user interface elements into a rendering incorporating an individual user's preferred AAC symbols. The W3C Augmentative and Alternative Communication ( AAC ) Symbol

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when adapting content with WAI-Adapt symbols or related modules.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: WAI-Adapt: Symbols Module Level 1.0 (default, posture build); WAI-Adapt: Help and Support Module Level 1.0 (default, posture track); WAI-Adapt: Tools Module Level 1.0 (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **3. Conformance.** "The key words MAY and MUST in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **4.1.1 Description.** "The numeric values utilized to map to symbols MUST be published BCI index values."
3. **1.3.2 Values.** "In the case of conflict between an element's semantics and the attribute values, validation algorithms should issue a warning but not an error."
4. **3. Conformance.** "There is no requirement that all content must be marked with adapt-symbol index values, and there is no minimum."
5. **4.1.1 Description.** "In such situations content authors should join multiple BCI index values in order to map to a single conjugated symbol by using a plus ( + ) sign (with no spaces between the BCI index values)."
6. **4.1.1 Description.** "The order of multiple concepts should be the same as used in typical speech in the natural language of the content."
7. **4.1.1 Description.** "Authors should not assume that one index value maps to one symbol—though authors should not need to make any assumptions about rendering, other than ensuring their content can be resized and will reflow, as per WCAG 2.1 Success Criteria 1.4.4 Resize Text and 1.4.10 Reflow ."
8. **5. Privacy and Security Considerations.** "This specification adds context information about content to the document, and should not affect security."

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

- [WAI-Adapt: Symbols Module](https://www.w3.org/TR/adapt-symbols/): Candidate Recommendation Snapshot, adapt-symbols WD-SVG2-20150915 (Candidate Recommendation Snapshot, 2023-01-05), checked 2026-10-06.
- [WAI-Adapt: Help and Support Module](https://www.w3.org/TR/adapt-help/): Working Draft, adapt-help WD-adapt-help-20220609 (Working Draft, 2022-06-09), checked 2026-10-06.
- [WAI-Adapt: Tools Module](https://www.w3.org/TR/adapt-tools/): Working Draft, adapt-tools WD-adapt-tools-20220609 (Working Draft, 2022-06-09), checked 2026-10-06.
- [WAI-Adapt Explainer](https://www.w3.org/TR/adapt/): Draft Note, adapt (Draft Note, 2023-01-03), checked 2026-10-06.
- [Requirements for WAI-Adapt specification](https://www.w3.org/TR/adapt-requirements/): Draft Note, adapt-requirements (Draft Note, 2022-06-09), checked 2026-10-06.

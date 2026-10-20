---
name: mathml
description: >-
  MathML: This specification defines a core subset of Mathematical Markup Language, or MathML, that is suitable for browser implementation. Covers MathML Core (build), Mathematical Markup Language (MathML) Version 4.0 (track preview). Use when authoring mathematical markup. Triggers: MathML, MathML Core.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# MathML

This specification defines a core subset of Mathematical Markup Language, or MathML, that is suitable for browser implementation. MathML is a markup language for describing mathematical notation and capturing both its structure and content. The goal of MathML is to enable mathematics to be served, received, and processed on the World Wide Web, just as HTML has enabled this functionality for text.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when authoring mathematical markup.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: MathML Core (default, posture build); Mathematical Markup Language (MathML) Version 4.0 (preview, posture track: emit only when the user opts in and the posture is build); Mathematical Markup Language (MathML) Version 3.0 2nd Edition (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **G. Conformance.** "The key words “ MUST ”, “ MUST NOT ”, “ REQUIRED ”, “ SHALL ”, “ SHALL NOT ”, “ SHOULD ”, “ SHOULD NOT ”, “ RECOMMENDED ”, “ MAY ”, and “ OPTIONAL ” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **G. Conformance.** "Advisements are normative sections styled to evoke special attention and are set apart from other normative text with <strong class="advisement"> , like this: UAs MUST provide an accessible alternative."
3. **2.1.1 The Top-Level <math> Element.** "All other MathML content must be contained in a <math> element."
4. **2.1.1 The Top-Level <math> Element.** "The <math> element accepts the attributes described in 2.1.3 Global Attributes as well as the following attributes: display alttext The display attribute, if present, must be an ASCII case-insensitive match to block or inline ."
5. **2.1.1 The Top-Level <math> Element.** "Because good mathematical rendering requires use of mathematical fonts, the user agent stylesheet should set the font-family"
6. **2.1.4 Attributes common to HTML and MathML elements.** "The dir attribute, if present, must be an ASCII case-insensitive match to ltr or rtl ."
7. **2.1.5 Legacy MathML Style Attributes.** "The mathcolor and mathbackground attributes, if present, must have a value that is a <color> ."
8. **2.1.5 Legacy MathML Style Attributes.** "The mathsize attribute, if present, must have a value that is a valid <length-percentage> ."

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

- [MathML Core](https://www.w3.org/TR/mathml-core/): Candidate Recommendation Snapshot, mathml-core CR-mathml-core-20250624 (Candidate Recommendation Snapshot, 2025-06-24), checked 2026-10-06.
- [Mathematical Markup Language (MathML) Version 4.0](https://www.w3.org/TR/mathml4/): Working Draft, mathml4 WD-mathml4-20261002 (Working Draft, 2026-10-02), checked 2026-10-06.
- [Mathematical Markup Language (MathML) Version 3.0 2nd Edition](https://www.w3.org/TR/MathML3/): Recommendation, MathML3 REC-MathML3-20140410 (Recommendation, 2014-04-10), checked 2026-10-06.

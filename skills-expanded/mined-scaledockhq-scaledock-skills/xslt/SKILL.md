---
name: xslt
description: >-
  XSLT: This specification defines the syntax and semantics of XSLT 3.0 , a language designed primarily for transforming XML documents into other XML documents. Covers XSLT 4.0 (track preview), XSL Transformations (XSLT) Version 3.0, XSL Transformations (XSLT) Version 2.0 (Second Edition) (supported). Use when transforming XML with XSLT. Triggers: XSLT 3.0, XSLT.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# XSLT

This specification defines the syntax and semantics of XSLT 3.0 , a language designed primarily for transforming XML documents into other XML documents. XSLT 3.0 is a revised version of the XSLT 2.0 Recommendation [XSLT 2.0] published on 23 January 2007. The primary purpose of the changes in this version of the language is to enable transformations to be performed in streaming mode, where neither the source document nor the result document is ever held in memory in its entirety. Another important aim is to improve the modularity of large stylesheets, allowing stylesheets to be developed from

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when transforming XML with XSLT.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: XSLT 4.0 (preview, posture track: emit only when the user opts in and the posture is build); XSL Transformations (XSLT) Version 3.0 (default); XSL Transformations (XSLT) Version 2.0 (Second Edition) (supported); XSL Transformations (XSLT) Version 1.0 (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **H.2 Relax-NG Schema for XSLT Stylesheets.** "IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES # (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, # STRICT LIABILITY, OR TORT (INCLUDING…"
2. **W3C Recommendation 8 June 2017.** "Status Update (6 April 2021): Feedback, comments, error reports on this specification should be sent via GitHub https://github.com/w3c/qtspecs/issues or email to public-qt-comments@w3.org ."
3. **1.2 What’s New in XSLT 3.0?.** "Capabilities provided in this category include: A new xsl:source-document instruction, which reads and processes a source document, optionally in streaming mode; The ability to declare that a mode is a streaming mode, in which case all the template rules using that mode must be streamable; A new xsl:iterate instruction, which iterates over the items in a sequence, allowing parameters for the…"
4. **2.1 Terminology.** "The processor may , and in some cases must , use streaming techniques to limit the amount of memory used to hold source and result documents."
5. **2.1 Terminology.** "In this specification the phrases must , must not , should , should not , may , required , and recommended , when used in normative text and rendered in capitals, are to be interpreted as described in [RFC2119] ."
6. **2.1 Terminology.** "Where the phrase must , must not , or required relates to the behavior of the XSLT processor, then an implementation is not conformant unless it behaves as specified, subject to the more detailed rules in 27 Conformance ."
7. **2.1 Terminology.** "Where the phrase must , must not , or required relates to a stylesheet then the processor must enforce this constraint on stylesheets by reporting an error if the constraint is not satisfied."
8. **2.1 Terminology.** "Where the phrase should , should not , or recommended relates to a stylesheet then a processor may produce warning messages if the constraint is not satisfied, but must not treat this as an error."

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

- [XSLT 4.0](https://qt4cg.org/specifications/xslt-40/Overview.html): Community Group draft, xslt-40-preview REC-xmlbase-20090128 (Community Group draft, 2026-10-05), checked 2026-10-06.
- [XSL Transformations (XSLT) Version 3.0](https://www.w3.org/TR/xslt-30/): Recommendation, xslt-30 REC-xslt-30-20170608 (Recommendation, 2017-06-08), checked 2026-10-06.
- [XSL Transformations (XSLT) Version 2.0 (Second Edition)](https://www.w3.org/TR/xslt20/): Recommendation, xslt20 REC-xslt20-20210330 (Recommendation, 2021-03-30), checked 2026-10-06.
- [XSL Transformations (XSLT) Version 1.0](https://www.w3.org/TR/xslt-10/): Recommendation, xslt xslt (Recommendation, 1999-11-16), checked 2026-10-06.

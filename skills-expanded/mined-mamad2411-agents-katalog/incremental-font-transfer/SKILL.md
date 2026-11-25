---
name: incremental-font-transfer
description: >-
  Incremental Font Transfer: This specification defines a method to incrementally transfer a font from server to client. Covers Incremental Font Transfer (build). Use when transferring fonts incrementally. Triggers: Incremental Font Transfer, IFT.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Incremental Font Transfer

This specification defines a method to incrementally transfer a font from server to client. The client loads only the portion(s) of the font that they actually need, significantly reducing data transfer. Multiple incremental additions to the same font are possible, such as a user agent updating a font as a user browses multiple pages. Incremental transfer improves on unicode-range by avoiding damage to layout (kerning, ligatures, etc) rules, meaning it can efficiently support fine grained increments to latin and to complex scripts like Indic or Arabic.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when transferring fonts incrementally.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Incremental Font Transfer (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **1.4. Performance Considerations and the use of Incremental Font Transfer.** "This section provides non-normative guidance to help decide when incremental transfer should be utilized."
3. **2. Opt-In Mechanism.** "The keyword incremental is used to indicate the referenced font contains IFT data and should only be loaded by a user agent which supports incremental font transfer."
4. **2. Opt-In Mechanism.** "The unicode ranges should be set to match the coverage of the fully extended font."
5. **2.1. Offline Usage.** "due to JavaScript execution), the page saving mechanism should fully expand the incremental font by invoking Fully Expand a Font Subset and replace references to the incremental font with the fully expanded one."
6. **3.3. Patch Map.** "The value specifies information about the patches which should be applied when the entry is matched."
7. **4.2. Default Layout Features.** "When forming a font subset definition as input to the extension algorithm the client should typically include all features found in Appendix A: Default Feature Tags in the subset definition."
8. **4.3. Incremental Font Extension Algorithm.** "These come in two forms: First, patch mapping entries may list more than one URL string, where each URL string after the first should also be loaded because they will be needed in future iterations."

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

- [Incremental Font Transfer](https://www.w3.org/TR/IFT/): Candidate Recommendation Draft, IFT CRD-IFT-20251118 (Candidate Recommendation Draft, 2025-11-18), checked 2026-10-06.

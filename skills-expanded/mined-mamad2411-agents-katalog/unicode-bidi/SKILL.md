---
name: unicode-bidi
description: >-
  Unicode Bidirectional Algorithm (UAX #9): order and display mixed left-to-right and right-to-left text. Covers UAX #9. Use when ordering bidirectional text. Triggers: UAX 9, bidi.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Unicode Bidirectional Algorithm (UAX #9)

This annex describes specifications for the positioning of characters in text containing characters flowing from right

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when ordering bidirectional text.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: UAX #9 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1 Introduction.** "In all other respects they should be ignored—they have no effect on the comparison of text or on word breaks, parsing, or numeric analysis."
2. **2 Directional Formatting Characters.** "On web pages, the explicit directional formatting characters (of all types &ndash; embedding, override, and isolate) should be replaced by other mechanisms suitable for HTML and CSS."
3. **2.7 Markup and Formatting Characters.** "The explicit formatting characters introduce state into the plain text, which must be maintained when editing or displaying the text."
4. **2.7 Markup and Formatting Characters.** "Where available, markup should be used instead of the explicit formatting characters: for more information, see [ UnicodeXML ]."
5. **2.7 Markup and Formatting Characters.** "PDF PDI <bdo dir = "ltr"> direction:ltr; unicode-bidi:isolate-override Unlike HTML4.0, HTML5 does not provide exact equivalents for LRE, RLE, LRO, and RLO, although the dir attribute and the BDO element as outlined above should in most cases work as well or better than those formatting characters."
6. **2.7 Markup and Formatting Characters.** "Whenever plain text is produced from a document containing markup, the equivalent formatting characters should be introduced, so that the correct ordering is not lost."
7. **2.7 Markup and Formatting Characters.** "For example, whenever cut and paste results in plain text this transformation should occur."
8. **3.1.2 Matching Explicit Directional Formatting Characters.** "It is maximal in the sense that if the first character of the first level run in the sequence is a PDI, it must not match any isolate initiator, and if the last character of the last level run in the sequence is an isolate initiator, it must not have a matching PDI."

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

- [UAX #9](https://www.unicode.org/reports/tr9/): Unicode Standard Annex, UAX #9 (Unicode Standard Annex, 2026-10-06), checked 2026-10-06.

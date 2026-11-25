---
name: unicode-emoji
description: >-
  Unicode Emoji (UTS #51): handle emoji characters, presentation and ZWJ sequences. Covers UTS #51. Use when handling emoji sequences. Triggers: UTS 51, emoji.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Unicode Emoji (UTS #51)

Please submit corrigenda and other comments with the online reporting form [ Feedback ].

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when handling emoji sequences.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: UTS #51 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Unicode Emoji.** "Summary This document defines the structure of Unicode emoji characters and sequences, and provides data to support that structure, such as which characters are considered to be emoji, which emoji should be displayed by default with a text style versus an emoji style, and which can be displayed with a variety of skin tones."
2. **Unicode Emoji.** "This question does not have a simple answer, because there is no clear line separating which pictographic characters should be displayed with a typical emoji style."
3. **Unicode Emoji.** "Inquiries for permission to use vendor images should be directed to those vendors, not to the Unicode Consortium."
4. **Unicode Emoji.** "Characters considered for encoding must normally be in widespread use as elements of text."
5. **Unicode Emoji.** "1.3 Goals This document provides: design guidelines for improving interoperability across platforms and implementations background information about emoji characters, and long-term alternatives data indicating: which characters normally can be considered to be emoji which emoji characters should be displayed by default in text style versus emoji style which emoji characters may be displayed using…"
6. **Unicode Emoji.** "default emoji presentation character — A character that, by default, should appear with an emoji presentation in well-formed sequences, rather than a text presentation."
7. **Unicode Emoji.** "default text presentation character — A character that, by default, should appear with a text presentation, rather than an emoji presentation."
8. **Unicode Emoji.** "The tag_end consists of the character U+E007F CANCEL TAG, and must be used to terminate the sequence."

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

- [UTS #51](https://www.unicode.org/reports/tr51/): Unicode Technical Standard, UTS #51 (Unicode Technical Standard, 2026-10-06), checked 2026-10-06.

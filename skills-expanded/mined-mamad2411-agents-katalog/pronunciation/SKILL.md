---
name: pronunciation
description: >-
  Pronunciation: The objective of the Pronunciation Task Force is to develop normative specifications and best practices guidance collaborating with other W3C groups as appropriate, to provide for proper pronunciation in HTML content when using text to speech (TTS) synthesis. Covers Explainer: Improving Spoken Presentation on the Web (track), Pronunciation Lexicon Specification (PLS) Version 1.0. Use when specifying how to pronounce content, or reading the pronunciation lexicon. Triggers: pronunciation, PLS, pronunciation lexicon.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Pronunciation

The objective of the Pronunciation Task Force is to develop normative specifications and best practices guidance collaborating with other W3C groups as appropriate, to provide for proper pronunciation in HTML content when using text to speech (TTS) synthesis. This document defines a standard mechanism to allow content authors to include spoken presentation guidance in HTML content. Also, it contains two identified approaches and enumerates their advantages and disadvantages.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when specifying how to pronounce content, or reading the pronunciation lexicon.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Explainer: Improving Spoken Presentation on the Web (default, posture track); Pronunciation Lexicon Specification (PLS) Version 1.0 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4. Goals.** "Define a standard mechanism that enables spoken presentation guidance to be authored in HTML Leverage SSML, if possible, as it is an existing standard that meets all identified requirements, and is supported by many speech synthesis platforms The mechanism must be consumable by assistive technologies such as screen readers"
2. **6.2 Attribute-based Model of SSML.** "This may cause problems for implementers who must parse the JSON values before processing."
3. **6.2 Attribute-based Model of SSML.** "Implementers must decide how to handle malformed JSON."

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

- [Explainer: Improving Spoken Presentation on the Web](https://www.w3.org/TR/pronunciation-explainer/): First Public Working Draft, pronunciation-explainer WD-pronunciation-explainer-20200310 (First Public Working Draft, 2020-03-10), checked 2026-10-06.
- [Pronunciation Lexicon Specification (PLS) Version 1.0](https://www.w3.org/TR/pronunciation-lexicon/): Recommendation, pronunciation-lexicon REC-pronunciation-lexicon-20081014 (Recommendation, 2008-10-14), checked 2026-10-06.
- [Pronunciation Gap Analysis](https://www.w3.org/TR/pronunciation-gap-analysis/): Draft Note, pronunciation-gap-analysis (Draft Note, 2025-08-07), checked 2026-10-06.
- [Pronunciation Use Cases](https://www.w3.org/TR/pronunciation-use-cases/): Draft Note, pronunciation-use-cases (Draft Note, 2025-08-07), checked 2026-10-06.

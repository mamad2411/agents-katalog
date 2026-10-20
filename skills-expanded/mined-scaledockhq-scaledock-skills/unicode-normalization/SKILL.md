---
name: unicode-normalization
description: >-
  Unicode Normalization (UAX #15): normalize text to NFC, NFD, NFKC or NFKD. Covers UAX #15. Use when normalizing Unicode text. Triggers: UAX 15, NFC, NFD.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Unicode Normalization (UAX #15)

When implementations keep strings in a normalized form, they can be assured that equivalent

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when normalizing Unicode text.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: UAX #15 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1 Canonical and Compatibility Equivalence.** "Canonical equivalence is a fundamental equivalency between characters or sequences of characters which represent the same abstract character, and which when correctly displayed should always have the same visual appearance and behavior."
2. **1.2 Normalization Forms.** "Normalization Forms KC and KD must not be blindly applied to arbitrary text."
3. **3 Versioning and Stability.** "That is, if a string that does not have any unassigned characters is normalized under one version of Unicode, it must remain normalized under all future versions of Unicode."
4. **3 Versioning and Stability.** "That is, Z must be a new character, and either X or Y must be a new character."
5. **3 Versioning and Stability.** "In addition to fixing the composition version, future versions of Unicode must be restricted in terms of the kinds of changes that can be made to character properties."
6. **4 Conformance.** "A process that purports to transform text into a Normalization Form must be able to produce the results of the conformance test specified in the NormalizationTest.txt data file [ Test15 ]."
7. **4 Conformance.** "A process that purports to transform text into the Stream-Safe Text Format must do so according to the Stream-Safe Text Process defined in UAX15-D4 ."
8. **4 Conformance.** "A process that purports to transform text according to the Normalization Process for Stabilized Strings must do so in accordance with the specifications in this annex."

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

- [UAX #15](https://www.unicode.org/reports/tr15/): Unicode Standard Annex, UAX #15 (Unicode Standard Annex, 2026-10-06), checked 2026-10-06.

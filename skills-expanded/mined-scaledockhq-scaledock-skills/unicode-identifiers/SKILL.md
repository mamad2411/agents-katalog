---
name: unicode-identifiers
description: >-
  Unicode identifiers (UAX #31): decide which characters may start and continue identifiers. Covers UAX #31. Use when deciding which characters are identifiers. Triggers: UAX 31, identifier.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Unicode Identifier and Pattern Syntax (UAX #31)

for the use of Unicode in the definitions of general-purpose identifiers, immutable identifiers, hashtag identifiers, and in

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when deciding which characters are identifiers.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: UAX #31 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Contents.** "To preserve the disjoint nature of the categories illustrated in Figure 1 , any character added to one of the categories must be subtracted from the others."
2. **Contents.** "In this case, the implementation should specify a minimum version of Unicode for the properties."
3. **1.5 Notation.** "Allowance for layout and format control characters, which should be ignored when parsing identifiers."
4. **1.5 Notation.** "Another such profile would be to include some set of the optional characters, for example: Start := XID_Start, plus some characters from Table 3 Continue := Start + XID_Continue, plus some characters from Table 3b Medial := some characters from Table 3a Note: Characters in the Medial class must not overlap with those in either the Start or Continue classes."
5. **1.5 Notation.** "Thus, any characters added to the Medial class from Table 3a must be be checked to ensure they do not also occur in either the newly defined Start class or Continue class."
6. **1.5 Notation.** "In so doing, care must be taken not to unintentionally include undesired characters, or to violate important invariants."
7. **1.5 Notation.** "An implementation should be careful when adding a property-based set to a profile."
8. **1.5 Notation.** "If the profile also needs stable identifiers (backwards compatible), then it must take additional measures."

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

- [UAX #31](https://www.unicode.org/reports/tr31/): Unicode Standard Annex, UAX #31 (Unicode Standard Annex, 2026-10-06), checked 2026-10-06.

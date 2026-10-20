---
name: unicode-collation
description: >-
  Unicode Collation Algorithm (UTS #10): sort and compare Unicode strings with DUCET and tailoring. Covers UTS #10. Use when sorting Unicode text. Triggers: UTS 10, UCA, collation.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Unicode Collation Algorithm (UTS #10)

supplies the Default Unicode Collation Element Table (DUCET) as the data specifying

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when sorting Unicode text.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: UTS #10 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1 Introduction.** "Linguistically correct searching needs to use the same mechanisms: just as "ä" and "æ" sort as if they were the same base letter in Swedish, a loose search should pick up words with either one of them."
2. **1 Introduction.** "Collation implementations must deal with the complex linguistic conventions for ordering text in specific languages, and provide for common customizations based on user preferences."
3. **1.1 Multi-Level Comparison.** "In other situations, it should be ignored if there are any base, accent, or case differences."
4. **1.2 Canonical Equivalence.** "Sequences that are canonically equivalent must sort the same."
5. **1.2 Canonical Equivalence.** "The order of certain combining marks is also irrelevant in many cases, so such sequences must also be sorted the same, as shown in the second example."
6. **1.5 Other Applications of Collation.** "In particular, searching should behave consistently with sorting."
7. **1.5 Other Applications of Collation.** "For example, if two letters are treated as identical base letters for sorting, then those letters should also be treated as identical for searching."
8. **Deterministic Comparison.** "This means that collations must be carefully versioned."

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

- [UTS #10](https://www.unicode.org/reports/tr10/): Unicode Technical Standard, UTS #10 (Unicode Technical Standard, 2026-10-06), checked 2026-10-06.

---
name: unicode
description: >-
  Unicode Standard: handle text by a published Unicode version, its character properties and algorithms. Covers Unicode 18.0.0, Unicode 17.0.0 (supported), Unicode 16.0.0 (supported). Use when handling Unicode text against a published version. Triggers: Unicode, Unicode 18.0.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Unicode Standard

STATUS: This is a preliminary draft page for an upcoming release. Some details may be missing or incorrect, and some links may be wrong or broken. During the beta review period, feedback about errors on this page will be helpful and appreciated.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when handling Unicode text against a published version.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Unicode 18.0.0 (default); Unicode 17.0.0 (supported); Unicode 16.0.0 (supported); Unicode 15.1.0 (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Version References.** "Version 18.0.0 of the Unicode Standard should be referenced as: The Unicode Consortium."
2. **Numeric Property Issues.** "Specialist implementations dealing with cuneiform text should be aware of these characters, which also pose challenges for formatting and for font design."
3. **Collation-related Changes.** "Implementations of UCA should be aware of this change."

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

- [Unicode 18.0.0](https://www.unicode.org/versions/Unicode18.0.0/): Unicode Standard, Unicode 18.0.0 (Unicode Standard, 18.0.0), checked 2026-10-06.
- [Unicode 17.0.0](https://www.unicode.org/versions/Unicode17.0.0/): Unicode Standard, Unicode 17.0.0 (Unicode Standard, 17.0.0), checked 2026-10-06.
- [Unicode 16.0.0](https://www.unicode.org/versions/Unicode16.0.0/): Unicode Standard, Unicode 16.0.0 (Unicode Standard, 16.0.0), checked 2026-10-06.
- [Unicode 15.1.0](https://www.unicode.org/versions/Unicode15.1.0/): Unicode Standard, Unicode 15.1.0 (Unicode Standard, 15.1.0), checked 2026-10-06.

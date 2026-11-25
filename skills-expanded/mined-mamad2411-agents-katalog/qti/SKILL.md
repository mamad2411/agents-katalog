---
name: qti
description: >-
  QTI: the 1EdTech Question and Test Interoperability assessment, section and item information model. Covers QTI 3.0.1. Use when exchanging an assessment item or test. Triggers: QTI, QTI 3.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# QTI

1EdTech Question and Test Interoperability (QTI) Assessment, Section and Item Information Model Version 3.0.1, 1EdTech Final Release, issued 1 September 2024.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when exchanging a QTI assessment item, section or test.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: an authoring system or a delivery engine.
- Target version: QTI 3.0.1 (current) — default. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **text.** "This means that from the perspective of conformance: - 1EdTech considers nonconformant any implementation of this specification that fails to implement a MUST/REQUIRED/SHALL requirement or fails to abide by a MUST NOT/SHALL NOT prohibition;"
2. **2.4.2.** "The hottext-interaction must be bound to a response variable with a base-type of identifier and single or multiple cardinality."
3. **text.** "Map Response Exprssion This expression looks up the value of a response variable and then transforms it using the associated mapping, which must have been declared."

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

- `lti`, when the assessment is launched from a learning platform: `npx skills add ScaleDockHQ/scaledock-skills --skill lti`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [QTI 3.0.1 ASI information model](https://www.imsglobal.org/sites/default/files/spec/qti/v3/info/imsqti_asi_v3p0p1_infomodel_v1p0.html): 1EdTech Final Release, Version 3.0.1, 1 September 2024, checked 2026-10-06.

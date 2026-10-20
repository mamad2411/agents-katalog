---
name: oscal
description: >-
  OSCAL: exchange control catalogs, profiles, system security plans and assessment results in NIST OSCAL formats. Covers OSCAL. Use when exchanging control assessment data. Triggers: OSCAL.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OSCAL

The Open Security Controls Assessment Language (OSCAL) from NIST: layered models for control catalogs and profiles, component definitions and system security plans, and assessment plans, results and POA&Ms, plus the OSCAL Profile Resolution specification for turning a profile into a resolved catalog.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when exchanging control assessment data.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: author or tool producing OSCAL documents, or a profile resolver or validator consuming them.
- Target version: OSCAL (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Control Layer Overview.** "Controls used in any other OSCAL model must first be defined in this model."
2. **Control Layer Overview.** "A control used in the implementation, assessment, and assessment results layers must first be imported by a profile."
3. **Uniqueness.** "As implied by the category name, locally-unique identifiers must be unique within the current document, whereas globally-unique identifiers are guaranteed to be unique across all other identifiers."
4. **req-exclude.** "Any control designated to be both included and excluded, MUST be excluded."
5. **req-multiformat-differ.** "A different serialization format of any given input MUST NOT result in a differing output catalog."

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

- [OSCAL Profile Resolution specification](https://raw.githubusercontent.com/usnistgov/OSCAL/v1.2.3/src/specifications/profile-resolution/profile-resolution-specml.xml): Draft specification, OSCAL v1.2.3 release, 2026-08-07, checked 2026-10-06.
- [OSCAL concepts: layers and models](https://raw.githubusercontent.com/usnistgov/OSCAL-Pages/4e5c578e1459db44f616a612c01e6e7bbe352935/src/content/learn/concepts/layer/_index.md): Documentation, OSCAL-Pages commit 4e5c578e1459, checked 2026-10-06.
- [OSCAL concepts: identifier use](https://raw.githubusercontent.com/usnistgov/OSCAL-Pages/4e5c578e1459db44f616a612c01e6e7bbe352935/src/content/learn/concepts/identifier-use/_index.md): Documentation, OSCAL-Pages commit 4e5c578e1459, checked 2026-10-06.

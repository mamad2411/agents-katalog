---
name: sysml
description: >-
  SysML: OMG Systems Modeling Language version 2.0 language specification. Covers SysML 2.0. Use when writing a SysML model. Triggers: SysML, SysML 2.0.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# SysML

OMG Systems Modeling Language (SysML) Version 2.0, Part 1 Language Specification, document formal/2026-03-02, March 2026. Version 1.7, document formal/24-01-07, January 2024, is the previous published line.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when writing a SysML model.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: a systems modeller.
- Target version: SysML 2.0 (current) — default; SysML 1.7 (legacy). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **2.0.** "A SysML model shall conform to this specification only if it can be represented according to the syntactic requirements specified in Clause 8 ."
2. **9.2.6.** "If a connection definition has more than one owned superclassification with other connection definitions, then it must declare a number of owned end features at least equal to the maximum number of end features of any of the general connection definitions."
3. **8.2.3.** "The compartment shall either be a textual compartment or a graphical compartment."
4. **5.1.** "SysML has three types of conformance, listed in Conformance Types, which shall all be supported to fully conform to SysML."
5. **text.** "self.base_Property.isComposite • 3_typed_by_classifierbehavior Properties to which ClassifierBehaviorProperty applied shall be typed by the classifier behavior of their owning block or a generalization of the classifier behavior."
6. **text.** "Association Ends • base_Port : Port [1] Constraints • 1_not_proxy Full ports shall not also be proxy ports."

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

- `uml`, when the model also uses UML notation: `npx skills add ScaleDockHQ/scaledock-skills --skill uml`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [SysML 2.0 Language](https://www.omg.org/spec/SysML/2.0/Language/PDF): OMG formal specification, formal/2026-03-02, March 2026, checked 2026-10-06.
- [SysML 1.7](https://www.omg.org/spec/SysML/1.7/PDF): OMG formal specification, formal/24-01-07, January 2024, checked 2026-10-06.

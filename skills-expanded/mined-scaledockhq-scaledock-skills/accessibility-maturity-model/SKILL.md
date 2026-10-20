---
name: accessibility-maturity-model
description: >-
  Accessibility Maturity Model: The Accessibility Maturity Model (AMM) provides a framework that offers individuals and organizations of all sizes a roadmap, including benchmarks, to develop, deploy, and maintain the accessibility of both internal and external digital resources over time. Covers Accessibility Maturity Model (track). Use when assessing an organization's accessibility maturity. Triggers: Accessibility Maturity Model, W3C maturity model.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Accessibility Maturity Model

The Accessibility Maturity Model (AMM) provides a framework that offers individuals and organizations of all sizes a roadmap, including benchmarks, to develop, deploy, and maintain the accessibility of both internal and external digital resources over time. This comprehensive framework encompasses all aspects of managing an organization's staff resources as well as its ever-evolving public ones. It readily scales in support of: single person consultancies, nonprofits, NGO s of any size, local and national governmental departments, courts, legislatures, agencies, and commissions, and SOHO businesses, major international corporate organizations or corporate departments, and any business entity

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when assessing an organization's accessibility maturity.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Accessibility Maturity Model (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1.1 How To Use The Accessibility Maturity Model.** "They should also comply with any applicable accessibility regulations."
2. **1.1.1 How To Use The Accessibility Maturity Model.** "If you were to claim this maturity level for your Communications Dimension, then the proof points that you uncover during your evaluation must support this claim."
3. **2.2 Proof Points.** "For example, if only procurement maturity is being measured, only procurement proof points should be evaluated."
4. **2.2 Proof Points.** "Proof points can be partially completed at the Launch and Integrate levels, but must be fully completed for the optimize level."
5. **2.3 Maturity Levels.** "All relevant outcomes should be addressed but not all outcomes will apply to all organizations and situations."
6. **3.2 ICT Development Lifecycle.** "Accessibility should be considered throughout the entire ICT development lifecycle: from idea conception to design, development, testing, production of an Accessibility Conformance Report ACR based on Industry recognized standards, user research, maintenance, and obsolescence."
7. **3.2 ICT Development Lifecycle.** "Training programs must be established and ongoing to have the necessary skills for the ICT Development Lifecycle dimension."
8. **3.3 Knowledge and Skills.** "Internal and external personnel at all levels of an organization should have accessibility knowledge and skills relevant to their organizational role."

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

- [Accessibility Maturity Model](https://www.w3.org/TR/maturity-model/): Note, maturity-model NOTE-maturity-model-20251104 (Note, 2025-11-04), checked 2026-10-06.

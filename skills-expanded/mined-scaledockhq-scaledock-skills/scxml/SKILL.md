---
name: scxml
description: >-
  SCXML: This document describes SCXML, or the "State Chart extensible Markup Language". Covers State Chart XML (SCXML): State Machine Notation for Control Abstraction. Use when writing a state machine in SCXML. Triggers: SCXML.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# SCXML

This document describes SCXML, or the "State Chart extensible Markup Language". SCXML provides a generic state-machine based execution environment based on CCXML and Harel State Tables.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when writing a state machine in SCXML.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: State Chart XML (SCXML): State Machine Notation for Control Abstraction (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1 Terminology.** "The key words MUST , MUST NOT , REQUIRED , SHALL , SHALL NOT , SHOULD , SHOULD NOT , RECOMMENDED , MAY , and OPTIONAL in this specification are to be interpreted as described in [RFC 2119] ."
2. **3.2.1 Attribute.** "xmlns true none URI none The value MUST be "http://www.w3.org/2005/07/scxml"."
3. **3.2.1 Attribute.** "version true none decimal none The value MUST be "1.0" datamodel false none NMTOKEN platform-specific "null", "ecmascript", "xpath" or other platform-defined values."
4. **3.2.2 Children.** "The SCXML processor MUST terminate processing when the state machine reaches this state."
5. **3.2.2 Children.** "5.8 <script> A conformant SCXML document MUST have at least one <state>, <parallel> or <final> child."
6. **3.2.2 Children.** "At system initialization time, the SCXML Processor MUST enter the states specified by the 'initial' attribute, if it is present."
7. **3.2.2 Children.** "If it is not present, the Processor MUST enter the first state in document order."
8. **3.2.2 Children.** "Platforms SHOULD document their default data model."

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

- [State Chart XML (SCXML): State Machine Notation for Control Abstraction](https://www.w3.org/TR/scxml/): Recommendation, scxml REC-scxml-20150901 (Recommendation, 2015-09-01), checked 2026-10-06.

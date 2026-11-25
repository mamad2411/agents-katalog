---
name: caliper
description: >-
  Caliper: 1EdTech Caliper Analytics® is a technical specification that describes a structured set of vocabulary that assists institutions in collecting learning and usage data from digital resources and learning tools. Covers Caliper 1.2. Use when sending learning analytics events. Triggers: Caliper.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Caliper

1EdTech Caliper Analytics® is a technical specification that describes a structured set of vocabulary that assists institutions in collecting learning and usage data from digital resources and learning tools. This data can be used to present information to students, instructors, advisers, and administrators in order to drive effective decision making and promote learner success.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when sending learning analytics events.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Caliper 1.2 (default). See `references/versions.md`.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **IPR and Distribution Notice.** "ANY USE OF THIS SPECIFICATION SHALL BE MADE ENTIRELY AT THE IMPLEMENTER'S OWN RISK, AND NEITHER THE CONSORTIUM, NOR ANY OF ITS MEMBERS OR SUBMITTERS, SHALL HAVE ANY LIABILITY WHATSOEVER TO ANY IMPLEMENTER OR THIRD PARTY FOR ANY DAMAGES OF ANY NATURE WHATSOEVER, DIRECTLY OR INDIRECTLY, ARISING FROM THE USE OF THIS SPECIFICATION."
2. **1.2 Terminology.** "Each Caliper Event MUST be assigned a UUID that is expressed as a URN using the form "urn:uuid:<UUID>" as described in [ RFC4122 ]."
3. **1.3 Conformance Statements.** "The key words " MAY ", " MUST ", " MUST NOT ", " OPTIONAL ", " RECOMMENDED ", " REQUIRED ", " SHALL ", " SHALL NOT ", " SHOULD ", and " SHOULD NOT " in this document are to be interpreted as described in [ RFC2119 ]."
4. **1.3 Conformance Statements.** "An implementation of this specification that fails to implement a MUST/REQUIRED/SHALL requirement or fails to abide by a MUST NOT/SHALL NOT prohibition is considered nonconformant."
5. **1.3 Conformance Statements.** "SHOULD/SHOULD NOT/RECOMMENDED statements constitute a best practice."
6. **2.1 Event.** "The type value is a string that MUST match the Term specified for the Event by the Caliper information model (e.g."
7. **2.1 Event.** "Each property MUST be referenced only once."
8. **2.1 Event.** "Custom attributes not described by the model MAY be included but MUST be added to the extensions property as a map of key:value pairs."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> `references/versions.md`
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in `references/requirements.md` and implement each one that applies to the role.
   -> `references/requirements.md`
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> `references/versions.md`
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in `references/requirements.md` holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Caliper 1.2](https://www.imsglobal.org/spec/caliper/v1p2/): Specification, Caliper Analytics 1.2 (Specification, 2026-10-06), checked 2026-10-06.

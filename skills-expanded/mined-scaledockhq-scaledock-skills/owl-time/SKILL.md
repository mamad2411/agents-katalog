---
name: owl-time
description: >-
  OWL Time: OWL-Time is an OWL-2 DL ontology of temporal concepts, for describing the temporal properties of resources in the world or described in Web pages. Covers Time Ontology in OWL (build). Use when describing time in OWL. Triggers: OWL Time.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# OWL Time

OWL-Time is an OWL-2 DL ontology of temporal concepts, for describing the temporal properties of resources in the world or described in Web pages. The ontology provides a vocabulary for expressing facts about topological (ordering) relations among instants and intervals, together with information about durations, and about temporal position including date-time information. Time positions and durations may be expressed using either the conventional (Gregorian) calendar and clock, or using another temporal reference system such as Unix-time, geologic time, or different calendars. The namespace for OWL-Time terms is http://www.w3.org/2006/time# The suggested prefix for the OWL-Time namespace is

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when describing time in OWL.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Time Ontology in OWL (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4.1.6 Generalized date-time description.** "Individual values SHOULD be consistent with each other and the calendar, indicated through the value of the :hasTRS property."
2. **1. Motivation and background.** "This includes relaxing the expectation from the original version that dates must use the Gregorian calendar."
3. **3.2 Temporal reference systems, clocks, calendars.** "In order to support these more general applications, the representation of temporal position and duration must be flexible, and annotated with the temporal reference system in use."
4. **3.4 Duration.** "The extent of an interval can be given using multiple duration descriptions or individual durations (e.g., 2 days, 48 hours) , but these must all describe the same amount of time."
5. **4.1.7 Generalized duration description.** "When non-earth-based calendars are considered even more care must be taken in comparing durations."
6. **4.1.16 Time position.** "The temporal ordinal reference system should be provided as the value of the :hasTRS property The temporal coordinate system should be provided as the value of the :hasTRS property"
7. **7. Security and Privacy.** "Implementations that produce, maintain, publish or consume temporal information using OWL-Time must take steps to ensure security and privacy considerations are addressed at the application level."

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

- [Time Ontology in OWL](https://www.w3.org/TR/owl-time/): Candidate Recommendation Draft, owl-time CR-owl-time-20200326 (Candidate Recommendation Draft, 2022-11-15), checked 2026-10-06.

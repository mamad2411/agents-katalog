---
name: schema-org
description: >-
  Schema.org: mark up structured data with Schema.org types and properties. Covers Schema.org. Use when marking up structured data. Triggers: Schema.org.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Schema.org

An abstract is a short description that summarizes a CreativeWork . Relevant types: CreativeWork Values: [ ^top ]

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when marking up structured data.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Schema.org (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Schema.org Version 30.1.** "Similarly, the encoding and publication details (RDFa/RDFS etc.) for the machine-readable schema file may evolve; however the data encoded should be considered canonical and frozen for each release."
2. **ActionAccessSpecification.** "A set of requirements that must be fulfilled in order to perform an Action."
3. **BreadcrumbList.** "The specific values of 'position' are not assigned meaning for a BreadcrumbList, but they should be integers, e.g."
4. **CohortStudy.** "It is one type of study design and should be compared with a cross-sectional study."
5. **CreativeWorkSeries.** "Schema.org attempts to anticipate some of these cases, but publishers should be free to apply properties of the series parts to the series as a whole wherever they seem appropriate."
6. **DrugCost.** "Costs of medical drugs vary widely depending on how and where they are paid for, so while this type captures some of the variables, costs should be used with caution by consumers of this schema's markup."
7. **EventPostponed.** "The event's previousStartDate should be set."
8. **EventRescheduled.** "The event's previousStartDate should be set to the old date and the startDate should be set to the event's new date."

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

- [Schema.org](https://schema.org/version/latest/): Release, Schema.org latest, fetched 2026-10-06 (Release, 2026-10-06), checked 2026-10-06.

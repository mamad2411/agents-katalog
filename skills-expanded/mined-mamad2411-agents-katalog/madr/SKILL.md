---
name: madr
description: >-
  MADR: write architecture decision records in the Markdown Any Decision Records template. Covers MADR. Use when writing an architecture decision record. Triggers: MADR, ADR.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# MADR

Markdown Architectural Decision Records (MADR) from the adr/madr project: the MADR 4.0.0 full template and the project documentation on naming, placing and organising decision records, read from the repository at the 4.0.0 release tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Author or reviewer of an architecture decision record, or a tool that creates or lints them.
- Target version: MADR (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Introduction.** "An Architectural Decision (AD) is a justified software design choice that addresses a functional or non-functional requirement of architectural significance."
2. **Introduction.** "This decision is documented in an Architectural Decision Record (ADR), which details a single AD and its underlying rationale."
3. **Title.** "short title, representative of solved problem and found solution"
4. **Context and Problem Statement.** "Describe the context and problem statement, e.g., in free form using two to three sentences or in the form of an illustrative story."
5. **Decision Outcome.** "Chosen option: "{title of option 1}", because {justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force {force} | … | comes out best (see below)}."
6. **Consequences.** "Good, because {positive consequence, e.g., improvement of one or more desired qualities, …}"
7. **Confirmation.** "Describe how the implementation of/compliance with the ADR can/will be confirmed."
8. **Create a new ADR § Manual approach.** "`NNNN` is a consecutive number and we assume that there won't be more than 9,999 ADRs in one repository."
9. **Create a new ADR § Manual approach.** "Decisions are placed in the subfolder `decisions/` to keep them close to the documentation but also separate the decisions from other documentation."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] The record has a title, Context and Problem Statement, Considered Options and Decision Outcome with a justification.
- [ ] The file sits in `decisions/` and uses the numbered, lowercase, dash-separated file name pattern.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `arc42`, `c4-model`, `commonmark`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [MADR 4.0.0 full template (template/adr-template.md)](https://raw.githubusercontent.com/adr/madr/2475fe1973f66a12aaf58a91d8fa7b42c0f5ea3d/template/adr-template.md): Release, MADR 4.0.0 (commit 2475fe1, released 2024-09-17), checked 2026-10-06.
- [MADR documentation (docs/index.md)](https://raw.githubusercontent.com/adr/madr/2475fe1973f66a12aaf58a91d8fa7b42c0f5ea3d/docs/index.md): Release, MADR 4.0.0 (commit 2475fe1, released 2024-09-17), checked 2026-10-06.

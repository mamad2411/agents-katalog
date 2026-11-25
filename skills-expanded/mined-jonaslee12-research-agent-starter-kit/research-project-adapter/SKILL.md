---
name: research-project-adapter
description: Adapt the starter kit to a specific research project type, such as dissertation, article, grant, fieldwork, computational study, design research, policy report, evidence synthesis, or knowledge-base project.
---

# Research Project Adapter

Use this skill when setting up or refactoring the starter kit for a project that is not necessarily a dissertation.

## Purpose

The public starter kit contains many mature workflows that were originally named for dissertation work. This skill decides how to reinterpret, keep, disable, or replace those workflows for the selected project type.

## Inputs To Check

Read these first when available:

- `RESEARCH_PROJECT_BRIEF.md`
- `RESEARCH_PROJECT_BRIEF_TEMPLATE.md`
- `PROJECT_TYPE_PROFILES.md`
- `PROJECT_AGENT_PREFERENCES.md`
- `compliance/PROJECT_COMPLIANCE_TRACKER.md`
- `quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md`
- `knowledge-base/SOURCE_READINESS_MATRIX.md`

If `RESEARCH_PROJECT_BRIEF.md` does not exist, use the template and mark project facts `TO CONFIRM`.

## Profile Decision

Choose one primary profile:

- taught dissertation / thesis
- journal article / manuscript
- research proposal / grant
- qualitative fieldwork project
- quantitative or computational study
- design research / product research
- policy / practice report
- literature review / evidence synthesis
- knowledge-base / RAG project
- custom profile

Do not infer private facts. If the profile is unclear, ask for confirmation or mark it `TO CONFIRM`.

## Mapping Rules

Treat these legacy skill names as general workflows:

- `dissertation-source-first-gate` = source-first factual gate
- `dissertation-research-search-protocol` = research search protocol
- `dissertation-learning-loop` = learning and memory loop
- `dissertation-literature-review` = literature/evidence synthesis planning
- `dissertation-citation-audit` = citation and claim-support audit
- `dissertation-document-quality-gate` = document delivery quality gate
- `dissertation-argument-spine` = argument or rationale spine
- `dissertation-research-review` = research design and claim review
- `dissertation-knowledge-ops` = knowledge-base operations

Use topic-specific skills only when the profile needs them.

## Default Output

For adaptation tasks, return:

```text
Project profile:
- Primary:
- Secondary:

Keep:
- ...

Optional / disable:
- ...

Required gates:
- ...

Files to fill first:
- ...

Risks:
- ...
```

## Boundaries

- Do not rename large skill folders during setup unless the user explicitly asks.
- Do not delete dissertation-specific files; mark them optional when not relevant.
- Do not treat metadata as source evidence.
- Do not promise journal acceptance, funding success, grades, or approval.

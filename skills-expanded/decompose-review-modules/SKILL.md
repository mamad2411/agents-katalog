---
name: decompose-review-modules
description: "Decompose a refined research question for a literature review into 3-5 clear, mostly non-overlapping review modules. Use when the user has a core review question and needs to build a literature review structure, reading map, subsection outline, coding scheme, or module-based search plan instead of listing papers author by author. 触发词：综述结构、拆模块、综述提纲、检索计划。"
metadata:
  version: "0.3.0"
---

# Decompose Review Modules

## Discipline And Interview Setup

Read [discipline-routing.md](references/discipline-routing.md), then only the selected discipline profile. Reuse the user's existing brief; do not restart intake at each stage. For journalism/communication or information science, use that profile's concepts, extraction fields, and appraisal checks instead of a generic social-science template.

When the user requests "grill me", 追问, or 模拟答辩, read [research-interview.md](references/research-interview.md). Ask one decision-relevant question per turn and wait; do not generate the stage deliverable until enough decisions are settled or the user asks to proceed. In quick/no-question mode, record assumptions and continue without inventing answers.

For evidence extraction or drafting, read [review-workflow.md](references/review-workflow.md). With no sources, give a plan or outline, not a purported synthesis. If reference files are unavailable, retain the source guardrails below and state that discipline guidance is missing.

## Goal

Convert one core research question into a small set of review modules that cover the key dimensions of the problem without collapsing into a loose topic list.

## Workflow

1. Restate the core question in one sentence.
2. Identify the main actors, mechanisms, outcomes, contexts, and constraints embedded in the question.
3. Propose 3-5 modules that are independent enough to become review sections.
4. Check whether sub-questions repeat. A paper may inform several modules; record separate evidence contributions rather than forcing each paper into one bucket.
5. Check coverage: the modules together should explain the main question's key dimensions.
6. Assess coverage only from the supplied or retrieved corpus. Without it, label module coverage "not assessed"; do not infer a gap or literature density from the outline.

## Module Design Rules

Good modules should be:

- Mutually distinguishable: each module asks a different sub-question.
- Collectively useful: together they help answer the core question.
- Literature-searchable: each can generate keywords, inclusion criteria, and section titles.
- Analytical rather than decorative: use a distinct synthesis task for each section, including conceptual or historical tasks; a mechanism is not mandatory.

## Common Module Axes

Choose axes that fit the question:

- Drivers: economic incentives, capability thresholds, social networks, institutional environment.
- Mechanisms: perception, decision process, resource allocation, coordination, feedback loops.
- Actors: individuals, organizations, platforms, governments, communities.
- Stages: adoption, use, persistence, exit, diffusion.
- Contexts: region, industry, policy period, population type, technology maturity.
- Outcomes: performance, equity, participation, sustainability, resilience.

## Output Format

Provide:

```markdown
## Core Question

[One sentence]

## Proposed Modules

| Module | Sub-question | Include | Exclude |
|---|---|---|---|
| ... | ... | ... | ... |

## Coverage Check

- What the modules cover well: ...
- Possible missing dimension: ...
- Possible overlap to revise: ...

## Suggested Review Outline

1. ...
2. ...
3. ...

## 待核实清单

[Unverified sources, "未查到" results, sentences marked [需补来源], and inferences that still need checking; write "无" if empty]

## 给作者的问题

[Judgment calls that belong to the author; write "无" if empty]
```

The output sections above, and the two closing sections, keep fixed names and order; see `references/output-contract.md` (a copy bundled in this skill folder).

## Guardrails

- Do not create more than five main modules unless the user explicitly asks for a large taxonomy.
- Do not organize modules only by author, year, country, or method unless that is the analytical point.
- When the user gives only a broad topic, first invoke question refinement logic before decomposing modules.
- Source integrity: follow `references/source-integrity.md`. Search keywords and expected literature distribution are suggestions, not findings; do not name specific papers unless the user provided them. Use only sources the user provided or that are verified, tag each with a status (用户提供 / 已核验 / 未核验), write "未查到" instead of completing authors, year, journal, or pages, and put anything unverified in `## 待核实清单`. If that file is not available, still apply these rules.

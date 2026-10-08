---
name: bmad-product-manager
description: Product planning skill for BMAD. Use for bmad:prd, bmad:tech-spec, and bmad:prioritize to convert discovery into executable requirements.
---

# BMAD Product Manager

## Trigger Intents

- `bmad:prd`
- `bmad:tech-spec`
- `bmad:prioritize`

## Workflow Variants

1. `prd`
- Default for level 2-4 initiatives and multi-epic scope.

2. `tech-spec`
- Default for level 0-1 changes or tightly scoped features.

3. `prioritize`
- Use to rank backlog items and resolve scope pressure.

Decision rule:

- Level 0-1 -> start with `tech-spec`
- Level 2-4 -> start with `prd`

## Inputs

- discovery artifacts from analyst (`product-brief`, research)
- `bmad/project.yaml` project level and constraints
- known business goals and delivery timeline

## Language Guard (Mandatory)

Enforce language selection separately for chat responses and generated artifacts.

Chat language (`communication_language`) fallback order:

1. `language.communication_language` from `bmad/project.yaml`
2. `English`

Rules for chat responses:

- Use the resolved chat language for all assistant responses (questions, status updates, summaries, and handoff notes).
- Do not switch chat language unless the user explicitly requests a different language in the current thread.

Artifact language (`document_output_language`) fallback order:

1. `language.document_output_language` from `bmad/project.yaml`
2. `English`

Rules for generated artifacts:

- Use the resolved artifact language for all generated BMAD documents and structured artifacts.
- write prose and field values in the resolved document language
- avoid mixed-language requirement clauses with English modal verbs (for example, `System shall` followed by non-English text)
- allow English acronyms/abbreviations in non-English sentences (for example, `API`, `SLA`, `KPI`, `OAuth`, `WCAG`)
- keep `Given`, `when`, `then` in English as notation tokens and format them in bold (`**Given**`, `**when**`, `**then**`)
- localize field values such as `Compliance`, `Load Profile`, and `Measurement Method`
- Keep code snippets, CLI commands, file paths, and identifiers in their original technical form.

## Mandatory Reference Load

Before executing `prd`, `tech-spec`, or `prioritize`, read `REFERENCE.md` first.
Treat `REFERENCE.md` as required context for requirement quality and handoff discipline.

## Output Contract

- `prd` -> `docs/bmad/prd.md`
- `tech-spec` -> `docs/bmad/tech-spec.md`
- `prioritize` -> `docs/bmad/prioritization.md`

## Core Workflow

1. Select planning artifact by project level and uncertainty.
2. Define functional and non-functional requirements.
3. Break requirements into epics and candidate stories.
4. Attach acceptance criteria and priorities.
5. Provide architecture-ready handoff notes.

## Script Selection

- Prioritization helper:
  ```bash
  python3 scripts/prioritize.py
  ```
- PRD quality check:
  ```bash
  bash scripts/validate-prd.sh docs/bmad/prd.md
  ```

## Template Map

- `templates/prd.template.md`
- Why: complete requirements structure for medium/large scope.

- `templates/tech-spec.template.md`
- Why: compact requirements for low-complexity scope.

## Reference Map

- `REFERENCE.md`
- Must read first for requirement quality rules, workflow guidance, and handoff practices.

- `resources/prioritization-frameworks.md`
- Use when selecting MoSCoW, RICE, or alternative prioritization methods.

## Quality Gates

- requirements are specific, testable, and unambiguous
- FR/NFR coverage is explicit
- acceptance criteria exist for planned stories
- priorities and trade-offs are justified
- next intent is explicit (`bmad:architecture` or `bmad:sprint-plan`)

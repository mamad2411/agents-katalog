---
name: bmad-creative-intelligence
description: Ideation and deep research skill for BMAD. Use for bmad:ideate and bmad:research-deep to generate options and structured insight.
---

# BMAD Creative Intelligence

## Trigger Intents

- `bmad:ideate`
- `bmad:research-deep`

## Workflow Variants

1. `ideate`
- Generate and prioritize option sets for a defined problem.

2. `research-deep`
- Produce evidence-backed analysis with sources and recommendations.

## Inputs

- problem statement and constraints
- existing BMAD artifacts in `docs/bmad/`
- target market or technical domain

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
- Keep code snippets, CLI commands, file paths, and identifiers in their original technical form.

## Mandatory Reference Load

Before executing `ideate` or `research-deep`, read `REFERENCE.md` first.
Treat `REFERENCE.md` as required context for method selection and output quality.

## Output Contract

- ideation output -> `docs/bmad/brainstorm.md`
- deep research output -> `docs/bmad/research-deep.md`
- optional option memo -> `docs/bmad/options.md`

## Core Workflow

1. Select method based on uncertainty and decision type.
2. Generate options or gather evidence.
3. Evaluate impact, effort, risk, and confidence.
4. Produce ranked recommendations.
5. Suggest concrete next BMAD intent.

## Script Selection

- SCAMPER prompts:
  ```bash
  bash scripts/scamper-prompts.sh
  ```
- SWOT structure:
  ```bash
  bash scripts/swot-template.sh
  ```
- Research source collection:
  ```bash
  bash scripts/research-sources.sh
  ```

## Template Map

- `templates/brainstorm-session.template.md`
- Why: structure ideation sessions and ranking output.

- `templates/research-report.template.md`
- Why: structure evidence collection and recommendations.

## Reference Map

- `REFERENCE.md`
- Must read first for method selection and workflow guidance.

- `resources/brainstorming-techniques.md`
- Use for ideation frameworks and facilitation patterns.

- `resources/research-methods.md`
- Use for deep research design and evidence quality.

## Quality Gates

- alternatives are concrete and comparable
- assumptions and confidence levels are explicit
- major claims include source context or uncertainty notes
- final recommendation is actionable

---
name: bmad-analyst
description: Product discovery and analysis skill for BMAD. Use for bmad:product-brief, bmad:research, and bmad:brainstorm to clarify user needs, market context, and problem scope.
---

# BMAD Analyst

## Trigger Intents

- `bmad:product-brief`
- `bmad:research`
- `bmad:brainstorm`

## Workflow Variants

1. `product-brief`
- Use when a project or feature needs a discovery brief before planning.

2. `research`
- Use when decisions need market, competitor, or technical evidence.

3. `brainstorm`
- Use when exploring solution options and narrowing concepts.

If the request is ambiguous, ask:

- "Do you want product-brief, research, or brainstorm mode?"

## Inputs

- `bmad/project.yaml` if available
- existing notes in `docs/bmad/`
- stakeholder assumptions, constraints, and goals

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

Before executing any workflow variant, read `REFERENCE.md` first.
Treat `REFERENCE.md` as required context, then load only relevant supporting files.

## Output Contract

- `product-brief` -> `docs/bmad/product-brief.md`
- `research` -> `docs/bmad/research-report.md`
- `brainstorm` -> `docs/bmad/brainstorm.md`

Always finish with a recommended next intent (`bmad:prd` or `bmad:tech-spec` in most cases).

## Core Workflow

1. For `product-brief`, complete the Mandatory Interview Gate before drafting or updating the brief.
2. Identify problem, user segment, impact, urgency, and constraints.
3. Apply discovery methods (5 Whys, JTBD, SMART).
4. Build the selected artifact with clear assumptions and measurable outcomes.
5. Validate artifact completeness and decision readiness.
6. Provide explicit handoff notes for the next BMAD phase.

## Mandatory Interview Gate (`product-brief`)

Before finalizing `docs/bmad/product-brief.md`, complete a chat-native discovery interview.

- Primary channel must be chat Q&A. Do not use shell prompts as the primary interview channel.
- Ask discovery questions in batches of 3-7, then wait for answers before asking the next batch.
- Use `resources/interview-frameworks.md` as the interview question bank.
- Coverage is mandatory for:
  - problem
  - users
  - current workaround
  - urgency
  - success metrics
  - constraints
  - risks
  - dependencies
  - next steps
- If the user explicitly asks to skip questions, continue only with clearly stated assumptions and ask for explicit confirmation.
- Do not finalize the brief without either interview answers or explicit user agreement to proceed with assumptions.

## Script Selection

- Product brief completeness check:
  ```bash
  bash scripts/validate-brief.sh docs/bmad/product-brief.md
  ```

## Environment Guidance

- Default behavior for `product-brief`: ask structured questions in chat first, then draft the artifact.
- Use shell scripts only for artifact validation, not as the primary interview channel.

## Template Map

- `templates/product-brief.template.md`
- Why: structured discovery output for PM handoff.

- `templates/research-report.template.md`
- Why: evidence-based research output with findings and recommendations.

For `brainstorm`, use this compact structure:

- problem frame
- idea list (10-20)
- ranked shortlist (top 3-5)
- risks and assumptions
- recommendation

## Reference Map

- `REFERENCE.md`
- Must read first for workflow context and discovery process details.

- `resources/interview-frameworks.md`
- Use as the focused question bank for the Mandatory Interview Gate.

Load only relevant sections to keep context lean.

## Quality Gates

- problem statement is explicit and testable
- target users and pain points are concrete
- success criteria are measurable
- assumptions and risks are visible
- next intent is clearly stated

## Handoff Criteria

Ready for `bmad-product-manager` when the discovery artifact defines:

- validated problem and user scope
- prioritized opportunities
- measurable outcomes
- constraints and dependencies

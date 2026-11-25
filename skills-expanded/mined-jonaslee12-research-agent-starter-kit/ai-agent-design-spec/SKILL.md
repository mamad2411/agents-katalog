---
name: ai-agent-design-spec
description: Turn dissertation evidence into an AI agent design specification for supporting active learning implementation, including user scenarios, functions, interaction flow, boundaries, failure modes, and design rationale.
---

# AI Agent Design Spec

Use when the user asks to design, refine, evaluate, or document the AI agent proposed in the dissertation.

## Inputs

Look for:

- `DISSERTATION_BRIEF.md`
- teacher interview findings, concept-card responses, design-elicitation outputs, or confirmed co-design outputs
- teacher interview/workshop findings
- `research-wiki/DESIGN_RATIONALE.md`
- `research-wiki/FINDINGS_INDEX.md`
- chapter drafts about design implications

## Workflow

1. Identify the teaching problem the agent supports.
2. Define primary users:
   - university teachers
   - teaching assistants or learning designers, if relevant
   - students only if the dissertation explicitly includes them
3. Map teacher needs and concerns to agent capabilities.
4. Specify:
   - user scenarios
   - agent goals and non-goals
   - core functions
   - interaction flow
   - inputs and outputs
   - human control points
   - failure modes and recovery
   - evidence source for each design decision
5. Separate evidence-backed requirements from speculative features.
6. Produce a design rationale that links back to active learning and adoption conditions.

## Output

Create or update:

- `design-specs/AI_AGENT_DESIGN_SPEC.md`
- `design-specs/USER_SCENARIOS.md`
- `design-specs/DESIGN_RATIONALE.md`

## Required Sections

Use this structure unless the user asks otherwise:

1. Purpose
2. Intended users
3. Teaching scenarios
4. Core capabilities
5. Boundaries and non-goals
6. Interaction flow
7. Teacher control and override points
8. Data and privacy assumptions
9. Failure modes
10. Evidence-to-design traceability table

## Guardrails

Read `../dissertation-shared/references/privacy-and-ethics.md` when participant data is involved.
Do not claim the agent is effective unless evaluation evidence exists.

---
name: codesign-output-synthesis
description: Synthesize confirmed co-design, design-elicitation, prototype-feedback, or participant-generated design outputs into requirements, design principles, prototype changes, participant contribution maps, and design decision logs.
---

# Co-Design Output Synthesis

Use when the user provides materials that are explicitly intended to inform design, such as co-design workshop notes, concept-card responses, design-elicitation interview findings, sticky-note outputs, activity artifacts, prototype feedback, or participant-generated ideas.

For the current dissertation, co-design is not the main study identity unless a fuller co-design activity is later confirmed. If the material is ordinary interview data, use `qualitative-theme-audit` first and call this skill only for the design-implication synthesis.

## Workflow

1. Check whether materials are anonymized.
2. Identify artifact type:
   - interview notes
   - workshop transcript
   - sticky notes
   - journey map
   - prototype feedback
   - design canvas
   - ranking/voting output
3. Extract:
   - teacher needs
   - concerns
   - barriers
   - desired supports
   - design ideas
   - constraints
   - tensions or disagreements
4. Convert outputs into:
   - functional requirements
   - non-functional requirements
   - design principles
   - adoption conditions
   - prototype changes
   - unresolved questions
5. Build traceability from participant evidence to design decision.

## Output

Create or update the path that fits the evidence type:

- `design-synthesis/DESIGN_ELICITATION_SYNTHESIS.md`
- `design-synthesis/REQUIREMENTS_TRACEABILITY.md`
- `design-synthesis/DESIGN_PRINCIPLES.md`
- `design-synthesis/PROTOTYPE_ITERATION_LOG.md`
- `codesign/CODESIGN_SYNTHESIS.md` only when co-design is confirmed

## Evidence Table

Use columns:

- source file
- participant/group ID
- evidence summary
- interpreted need/concern
- design implication
- confidence
- unresolved risk

## Guardrails

Read `../dissertation-shared/references/privacy-and-ethics.md`.
Do not overstate consensus. Mark minority views and tensions explicitly.
Do not label the dissertation as a co-design study unless the method and supervisor feedback support that claim.

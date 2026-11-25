---
name: dissertation-figure-spec
description: Design specifications for dissertation figures such as conceptual frameworks, concept-card/interview process diagrams, AI-agent workflow diagrams, adoption-condition models, and findings maps.
---

# Dissertation Figure Spec

Use when planning or creating diagrams and figure descriptions for the dissertation.

## Suitable Figures

- conceptual framework for AI-agent support of active learning
- the chosen conceptual lens-informed adoption conditions framework
- interview and concept-card elicitation process
- data collection and analysis workflow
- teacher concerns map
- adoption conditions model
- AI agent interaction flow
- findings-to-design-implications map

## Workflow

1. Identify the figure's purpose and chapter location.
2. Define the exact claim the figure supports.
3. List required elements and relationships.
4. Decide format:
   - Mermaid for process and concept maps
   - table for matrices
   - simple diagram spec for later design
5. Provide caption text and alt text.
6. Check that the figure does not imply unsupported causal claims.

## Figure Quality Gate

Before delivering a figure spec, check:

- the figure has one clear job
- the claim is stated before the visual structure
- every box or arrow represents a source-grounded or clearly tentative relationship
- the chosen conceptual lens elements are not shown as deterministic causes unless the evidence supports that
- trust, autonomy, workload, privacy, and pedagogic identity are not hidden under vague labels
- participant-facing figures avoid technical overload
- supervisor-facing figures show contribution and evidence boundary clearly

## Caption Quality Gate

A caption should state:

1. what the figure shows
2. how it should be read
3. what evidence or conceptual lens it is based on
4. what the figure does not claim, if there is a risk of over-reading

Avoid captions that simply repeat labels from the figure.

## Current Project Figure Priorities

Recommended near-term figures:

- the chosen conceptual lens-informed conceptual framework for teacher adoption conditions
- AI-agent concept card visual used for interview elicitation
- methodology flow: recruitment, interview, concept-card discussion, analysis, synthesis
- findings-to-design-boundaries map after data analysis

## Output

Create or update files under `figures/`, such as:

- `figures/FIGURE_SPECS.md`
- `figures/conceptual-framework.mmd`
- `figures/methodology-flow.mmd`
- `figures/utaut-adoption-framework.mmd`

## Guardrails

Do not use participant-identifiable details in figures.

Do not create a polished visual that makes tentative or planned claims look like findings.

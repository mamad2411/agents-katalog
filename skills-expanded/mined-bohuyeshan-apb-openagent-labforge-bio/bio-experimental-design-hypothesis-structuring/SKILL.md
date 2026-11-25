---
name: bio-experimental-design-hypothesis-structuring
description: Structures biological hypotheses into assumptions, predictions, competing explanations, and falsification paths. Use when a user has a mechanistic or translational idea and needs to turn it into a testable biological hypothesis instead of a vague narrative.
tool_type: mixed
primary_tool: hypothesis-logic
---

# Hypothesis Structuring for Biology

**"Help me turn this idea into a testable biological hypothesis"** -> rewrite a biological story into assumptions, predictions, alternatives, and falsification logic.

## Goal

Produce a hypothesis that is:

- biologically meaningful
- specific enough to test
- paired with alternative explanations
- linked to measurable predictions
- connected to a falsification path

## Core hypothesis scaffold

```text
Hypothesis:
Biological rationale:
Assumptions:
Primary prediction:
Secondary predictions:
Competing explanations:
Most likely confounders:
Minimal falsification test:
What result would count as only weak support:
What result would strongly reject the hypothesis:
```

## Distinguish three levels

1. **Observation** — what the user already sees
2. **Hypothesis** — what hidden mechanism or relationship might explain it
3. **Prediction** — what new measurable result should appear if the hypothesis is true

Never confuse a descriptive observation with a causal hypothesis.

## Biological examples

- Observation: resistant tumors have higher pathway X activity.
- Hypothesis: pathway X causally promotes resistance by rewiring DNA-damage response.
- Prediction: pathway X perturbation should change resistance phenotype and downstream repair markers.

- Observation: ligand A docks better than ligand B.
- Hypothesis: ligand A has stronger functional inhibition because it stabilizes a productive binding pose.
- Prediction: potency and orthogonal structural/biophysical assays should align with docking differences.

## Quality rules

- Prefer mechanistic verbs: promotes, suppresses, modulates, destabilizes, enriches, shifts.
- State when the hypothesis is causal vs associative.
- Always name at least one plausible competing explanation.
- Include at least one orthogonal or independent validation path.

## Related skills

- experimental-design/research-question-framing
- experimental-design/validation-strategy
- pathway-analysis/go-enrichment
- structural-biology/modern-structure-prediction
- chemoinformatics/virtual-screening

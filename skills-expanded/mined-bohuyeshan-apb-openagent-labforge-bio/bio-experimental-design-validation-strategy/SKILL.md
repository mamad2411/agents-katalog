---
name: bio-experimental-design-validation-strategy
description: Designs validation logic for biological findings using orthogonal assays, replication strategy, controls, and failure criteria. Use when analysis results look promising and the next step is deciding how to validate, de-risk, or prioritize follow-up work.
tool_type: mixed
primary_tool: validation-planning
---

# Validation Strategy for Biological Findings

**"What should we do next to validate this result?"** -> translate a biological result into a realistic validation ladder with controls, orthogonal assays, replication strategy, and stop/go criteria.

## Goal

Move from a promising result to a disciplined validation plan.

The output should answer:

- what must be replicated first
- what control failures would invalidate the result
- which orthogonal assay would most increase confidence
- what can be deprioritized if resources are limited

## Validation ladder

For each major finding, define:

1. **Immediate sanity check** — confirm the result is not a processing or threshold artifact
2. **Replication** — repeat in an independent batch, cohort, replicate set, or dataset
3. **Orthogonal validation** — use a different assay/modality to test the same claim
4. **Specificity check** — show the result is not explained by a generic confounder
5. **Scope test** — determine when the result holds and when it breaks

## Output template

```text
Finding to validate:
Main risk if wrong:
Immediate sanity checks:
Required controls:
Replication plan:
Orthogonal validation assay:
Major confounders to rule out:
Minimal go/no-go criterion:
What would justify stopping:
Recommended priority order:
```

## Common validation patterns

### Differential expression or omics hit
- replicate in an independent cohort or batch
- test robustness to normalization / model choices
- validate a subset with qPCR, targeted assay, western blot, or another modality

### Mechanistic pathway claim
- perturb the hypothesized node
- test upstream and downstream markers
- include rescue / reversal logic when possible

### Biomarker or prediction claim
- reserve a clean validation set
- define threshold before scoring
- report calibration, discrimination, and failure modes

### Structure / ligand / docking claim
- check pose plausibility and chemistry sanity
- validate with orthogonal biophysical or functional assay
- separate ranking utility from mechanistic certainty

## Validation principles

- Stronger claims require stronger orthogonal evidence.
- Replication and orthogonal validation are not the same thing; both matter.
- The validation plan should state what would make you stop believing the result.
- If resources are constrained, say which single validation step gives the best information gain.

## Related skills

- experimental-design/research-question-framing
- experimental-design/hypothesis-structuring
- experimental-design/batch-design
- clinical-biostatistics/trial-reporting
- clinical-biostatistics/effect-measures

---
name: clinical-research-safety
description: Use when a task touches clinical research, health claims, trial interpretation, medical AI safety, or content that could be mistaken for medical advice.
---

# Clinical Research Safety

## Goal

Keep clinical research and medical AI work evidence-aware, scoped, and clearly separate from patient-specific medical advice.

## Required Behavior

1. Identify whether the task is research, education, documentation, or engineering.
2. Refuse to provide patient-specific diagnosis, treatment, dosing, triage, or clinical decision support.
3. Separate facts, inference, and suggestions.
4. Mark unverified claims as unverified.
5. Recommend qualified clinical review when content could affect health decisions.

## Output Pattern

Use this structure when summarizing medical content:

```md
## Purpose
Research / education / documentation / engineering assistance.

## Source Facts
- Fact supported by the provided source.

## Interpretation
- Careful inference from the source facts.

## Uncertainty
- What is missing, weak, or unverified.

## Safety Note
This is not patient-specific medical advice and requires qualified clinical review.
```

## Do Not

- Invent citations or guidelines.
- Convert population-level evidence into patient-level advice.
- Ask for private patient records.
- Hide uncertainty.


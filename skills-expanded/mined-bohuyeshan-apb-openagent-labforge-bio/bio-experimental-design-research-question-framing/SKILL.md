---
name: bio-experimental-design-research-question-framing
description: Frames biological research questions into tractable study objectives, target variables, comparison groups, success criteria, and likely confounders. Use when a user has a broad scientific idea but the task needs a sharper biological question before experiment design or analysis begins.
tool_type: mixed
primary_tool: study-design-frameworks
---

# Research Question Framing for Biological Studies

**"Turn this broad biological idea into a real study question"** -> convert a vague idea into a concrete biological question, study objective, comparison, endpoint, and decision rule.

## Goal

Move from a broad idea like:

- "I want to understand why this gene matters"
- "Could this pathway drive resistance?"
- "Maybe this ligand affects this protein"

to a tractable framing like:

- primary biological question
- working objective
- key comparison or perturbation
- measurable endpoint
- major confounders or design risks
- what evidence would count as support vs refutation

## Core framing scaffold

For every new study idea, write:

1. **Biological question** — What do we want to know?
2. **Working hypothesis** — What do we currently think is true?
3. **Study objective** — What specific claim will the work test or estimate?
4. **Unit of analysis** — gene, protein, cell, patient, sample, time point, ligand, pathway, etc.
5. **Comparison / perturbation** — control vs treatment, knockout vs wild type, responder vs non-responder, high vs low exposure, etc.
6. **Primary endpoint** — the most decision-relevant measured outcome
7. **Secondary endpoints** — supporting evidence, mechanistic or orthogonal outcomes
8. **Confounders / threats** — batch, donor effects, cell composition, treatment history, chemistry purity, sampling bias
9. **Support criteria** — what pattern would support the hypothesis?
10. **Refutation criteria** — what finding would weaken or reject it?

## Output template

```text
Biological question:
Working hypothesis:
Primary objective:
Primary comparison:
Primary endpoint:
Secondary endpoints:
Key confounders:
What would support the hypothesis:
What would weaken the hypothesis:
Recommended next design step:
```

## Design heuristics

- Prefer one sharp primary question over many loosely related goals.
- Separate **mechanism** questions from **association** questions.
- State whether the study aims for causal inference, prediction, prioritization, or description.
- Pair every effect claim with the study design that can actually support it.
- If the user wants "understand" or "explore", force clarification: understand mechanism, biomarker utility, therapeutic relevance, or evolutionary pattern?

## Typical biological pitfalls

- Treating a broad pathway exploration as if it were a single testable hypothesis.
- Asking causal questions from purely observational data without stating the limitation.
- Defining endpoints after looking at the data.
- Mixing discovery, validation, and reporting goals in one undifferentiated request.

## Related skills

- experimental-design/hypothesis-structuring
- experimental-design/validation-strategy
- experimental-design/power-analysis
- experimental-design/sample-size
- clinical-biostatistics/effect-measures

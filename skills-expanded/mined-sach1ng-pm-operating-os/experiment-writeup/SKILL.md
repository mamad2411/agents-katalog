---
name: experiment-writeup
description: "Help PMs write up experiment results. Use when documenting A/B test outcomes, feature experiment learnings, or sharing results with stakeholders."
---

# Experiment Writeup

Help PMs document experiment results in a structured format. Turns raw data into clear narratives with hypothesis, methodology, results, learnings, and decision.

## When to Use

- Documenting A/B test outcomes
- Writing up feature experiment results
- Sharing experiment learnings with stakeholders
- Creating a record for future reference
- When asked "help me write up the results"

## Process / Template

### 1. Gather the Data

- Hypothesis (original statement)
- Experiment design (variants, duration, sample size)
- Primary, secondary, and guardrail metric results
- Statistical significance (p-values, confidence intervals)
- Any qualitative feedback or observations

### 2. Structure the Writeup

**Hypothesis**
- Restate the original hypothesis
- Brief context on why we ran this

**Methodology**
- Variants tested (control vs. treatment)
- Duration and sample size
- Target segment
- Any caveats (traffic issues, external events)

**Results**
- **Primary metric** — direction, magnitude, significance
- **Secondary metrics** — supporting or conflicting signals
- **Guardrail metrics** — did anything regress?

**Learnings**
- What did we learn? (beyond the numbers)
- Surprises or unexpected findings
- Implications for future work

**Decision**
- Ship / Iterate / Kill
- Rationale for the decision
- Next steps (if iterating)

### 3. Write Clearly

- Lead with the decision and key takeaway
- Use plain language; avoid jargon
- Include numbers with context (e.g., "+12% vs. control")
- Call out statistical significance explicitly

## Output

A structured **Experiment Writeup** suitable for:
- Stakeholder sharing (Slack, email)
- Internal documentation
- Experimentation platform notes
- Retrospectives and planning

Format: concise, scannable, decision-oriented. Typically 1–2 pages or equivalent in markdown.

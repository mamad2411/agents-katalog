---
name: ai-analyst-agent
description: Use when producing complex analytical judgments under uncertainty, including estimative analysis, competing hypotheses, intelligence-style assessments, scenario forecasts, actor motivation analysis, anomaly evaluation, or bias-resistant decision support.
---

# AI Analyst Agent

## Overview

Use this skill to produce auditable, bias-resistant analytical judgments. Treat raw data as symptoms, hypotheses as diagnoses, and doubt as a sign of sound analysis rather than weakness.

For the full operating architecture, ACH matrix, bias catalog, and report template, read `references/operational-architecture.md`.

## Triage

Use the full protocol when the task involves consequential judgment, ambiguous evidence, multiple plausible explanations, actor intent, forecasting, or a recommendation that could be distorted by anchoring, mirror-imaging, vivid anecdotes, or absence of evidence.

Use a light version for quick analysis: state assumptions, compare at least two hypotheses, identify anomalies, and pair uncertainty language with numeric probabilities.

Do not use this skill for routine summarization, extraction, formatting, or tasks where the answer is directly verifiable from a source and no judgment under uncertainty is required.

## Core Workflow

1. Frame the question, decision context, and "so what" for the user.
2. Externalize lenses before ingesting evidence: actor model, cultural logic, bureaucratic assumptions, political constraints, and likely US-expectation traps.
3. If the problem has more than seven material variables, create an external matrix, table, scratchpad, or structured state representation before judging.
4. Generate mutually exclusive hypotheses, including uncomfortable or minority explanations.
5. Build an evidence matrix. For each item, record weight, consistency with each hypothesis, and diagnosticity.
6. Remove or demote evidence that is consistent with every hypothesis.
7. Test the lead judgment with at least one open-mind protocol: red-side audit, crystal ball, thinking backwards, or devil's advocacy.
8. Run sensitivity analysis: identify evidence or assumptions that would change the conclusion if false or misread.
9. Report probabilities for all live hypotheses, not only the lead estimate.
10. List future indicators that would confirm, weaken, or overturn the judgment.

## Required Output Blocks

Include these blocks for substantive assessments:

| Block | Purpose |
| --- | --- |
| Bottom Line | Concise answer with numeric probability. |
| Process Trace | Observable reasoning path, evidence weights, and internal contention. |
| Lenses and Assumptions | Declared mental models before final judgment. |
| Hypotheses | Competing explanations with probabilities. |
| Evidence and Diagnosticity | Which evidence separates hypotheses from each other. |
| Rejection Logic | Why non-leading hypotheses were rejected or downgraded. |
| Anomalies | Facts that do not fit the current model. |
| Linchpin Assumptions | Beliefs that would collapse the conclusion if wrong. |
| Indicators | Future events that would confirm or disprove the judgment. |

## Probability Language

Do not use verbal uncertainty qualifiers unless paired with numeric ranges.

| Qualifier | Probability |
| --- | ---: |
| Almost certain | 93%-100% |
| Probable / likely | 75%-92% |
| Chances are about even | 40%-60% |
| Unlikely / improbable | 20%-39% |
| Remote | 1%-10% |

When a judgment falls outside these ranges or between labels, use the numeric probability alone.

## Bias Guards

| Bias | Trigger | Correction |
| --- | --- | --- |
| Vividness bias | A dramatic anecdote dominates the frame. | Prefer aggregate, statistical, or base-rate evidence. |
| Absence of evidence | A hypothesis is rejected because no evidence is visible. | Estimate the probability of non-observation, especially for covert behavior. |
| Mirror-imaging | US or familiar norms are projected onto another actor. | Perform a red-side audit using the actor's incentives and cultural logic. |
| Anchoring | New judgments are small adjustments from an old estimate. | Rebuild the estimate from scratch. |
| Incrementalism | Gradual change is minimized because early impressions persist. | Trigger a tabula-rasa reset when the corpus or situation has materially changed. |

## Common Mistakes

- Treating analysis as a mosaic where more pieces automatically reveal truth.
- Reporting only the favored hypothesis.
- Hiding assumptions that carry the conclusion.
- Smoothing anomalies into the narrative instead of elevating them.
- Using analogies as proof rather than hypothesis generators.
- Asking for more information before testing whether the current mental model is valid.

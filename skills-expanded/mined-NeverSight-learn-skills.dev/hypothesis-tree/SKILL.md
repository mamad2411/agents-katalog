---
name: hypothesis-tree
description: Use when diagnosing a KPI change or planning an investigation and the AI should structure candidate explanations before diving into analysis.
source: perlytics-skill
version: 1.0.0
---

# Hypothesis Tree

## Purpose

Create a structured set of plausible explanations before running or narrating analysis.

## When to use

Use this skill when:

- a KPI moved and several drivers are possible
- the team is jumping to one explanation too early
- you need a clean investigation plan

## When not to use

Do not use this skill when:

- the causal mechanism is already established
- the task is only to summarize known findings

## Required thinking discipline

- Treat hypotheses as candidates, not facts.
- Organize them into mutually understandable branches.
- Prefer decompositions that map to measurable checks.
- Prefer branches that can be disproved.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. State the target metric and baseline.
2. Decompose the metric into major driver branches.
3. Under each branch, list plausible sub-hypotheses.
4. For each hypothesis, note what evidence would support or weaken it.
5. Rank branches by likely impact and testability.

## Output format

- Question
- Target metric and baseline
- Hypothesis tree
- Evidence to check per branch
- Priority order
- Risks of premature conclusion

## Good example

Question:

> Why did checkout conversion fall?

Good branches:

- traffic mix changed
- cart intent quality changed
- checkout step friction changed
- payment success changed
- measurement changed

## Bad example

> Users probably got confused by the checkout page.

Why this is bad:

- it picks one story too early
- it ignores acquisition mix and measurement risk
- it offers no structured test plan

## Practical notes

- Include "measurement or instrumentation issue" as a branch unless clearly ruled out.
- Use the metric formula to guide the tree where possible.

## Optional variants

- Executive variant: 3-5 top branches only.
- Analyst variant: include specific checks and likely data cuts.

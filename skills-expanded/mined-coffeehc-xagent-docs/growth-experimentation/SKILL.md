---
name: growth-experimentation
description: Use when designing, prioritizing, reviewing, or summarizing growth experiments, funnel improvements, activation tests, retention tests, pricing tests, onboarding experiments, referral loops, lifecycle experiments, or A/B test plans. Prefer this Skill when the task needs hypothesis clarity, metric choice, segment definition, experiment design, prioritization, or learning agenda. Do not use for analytics execution, tracking implementation, or causal claims without data.
meta:
  version: 1
  display_name: 增长实验
---

# Growth Experimentation

## Purpose

Design growth experiments that connect a specific user behavior, hypothesis, intervention, metric, risk, and decision rule.

## Use When

Use for:

- activation and onboarding tests
- conversion funnel experiments
- lifecycle and retention tests
- referral or virality ideas
- pricing or packaging tests
- experiment prioritization
- growth readouts

## Material Gate

Identify:

- target funnel step, segment, baseline metric, and desired behavior
- available traffic or sample size constraints
- product surface, intervention, risk, and owner
- success metric, guardrail metric, and decision date

If baseline data is absent, present a discovery plan rather than a quantified experiment claim.

## Workflow

1. State the growth problem and target behavior.
2. Write a falsifiable hypothesis.
3. Define audience, intervention, metric, guardrail, and decision rule.
4. Identify risks: user trust, revenue, support load, data quality, or brand.
5. Prioritize by impact, confidence, effort, and learning value.
6. Summarize expected learning and next action.
7. Use `html-report-builder` for experiment roadmaps or results reports.

## Checks

- Hypothesis is testable.
- Metric matches the behavior.
- Guardrails prevent local optimization harm.
- Experiment does not require unsupported analytics claims.
- Decision rule is clear before results are known.

## Outputs

- experiment brief
- hypothesis backlog
- prioritization matrix
- A/B test plan
- funnel improvement plan
- growth readout
- learning agenda

## Boundary

This Skill owns growth hypothesis design, experiment structure, prioritization, and learning summaries. It does not own analytics instrumentation, experiment platform configuration, statistical certification, product deployment, or causal claims without data.

It must not run shell, Python, Node, npm, curl, MCP, analytics, experiment platform, data warehouse, feature flag, CRM, email, package install, deploy, or external API commands by itself; those actions belong to XAgent tools visible in the current session.

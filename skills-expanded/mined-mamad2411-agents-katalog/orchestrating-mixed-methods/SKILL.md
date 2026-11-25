---
name: orchestrating-mixed-methods
description: Use when research, analysis, evaluation, diagnosis, discovery, insight, or study-design tasks require deciding between qualitative, quantitative, or mixed-methods approaches, especially when the user does not specify a method or the work needs both measurement and explanation.
---

# Orchestrating Mixed Methods

## Overview

This skill is a routing and orchestration skill for research and analysis work.
It prevents false `qualitative vs quantitative` either-or framing and chooses the
smallest valid route:

- `qualitative-only`
- `quantitative-only`
- `mixed-qual-first`
- `mixed-quant-first`
- `mixed-parallel`

這個 skill 是研究方法的協調器，不是固定報告格式。
它的工作是先判斷「該用哪種方法、先後順序怎麼排、兩軌怎麼整合」，
而不是每次都硬做成對稱的雙軌輸出。

## When to Use / 何時使用

Use this skill as the default entrypoint when the task involves:

- research, analysis, evaluation, diagnosis, discovery, insight, or study design
- user questions such as `what is happening`, `how much`, `why`, `how`, `what changed`, or `what should we test`
- open-ended evidence like interviews, notes, observations, or case material
- structured evidence like survey tables, KPIs, experiment results, cohort metrics, or scored datasets
- mixed evidence such as `survey + interviews`, `metrics + support tickets`, `experiment + user quotes`
- explicit mentions of `qualitative`, `quantitative`, `mixed methods`, `triangulation`, `interviews`, `survey`, or `statistical significance`

Do not use this skill when:

- the task is not actually research or analysis work
- the user only wants direct arithmetic, file conversion, translation, or plain rewriting
- the user already gave a narrow, fixed method and does not need any method choice or sequencing

If this skill triggers on a clearly single-method task, route it to the proper
single method. Do not force mixed methods just because this skill loaded.

## Core Rule / 核心規則

Respect explicit user constraints first.

- If the user clearly asks for only one method, route to that method.
- Exception: if the same request clearly asks for both measurement and explanation,
  do not treat the method choice as exclusive. Route to the smallest mixed path.

Do not make the user pick between qual and quant when the actual question is
asking for both `what/how much` and `why/how`.

## Required Routing Output / 必要路由輸出

Before doing downstream analysis, emit a `MethodRoutingDecision`.
If the method context is too incomplete to choose safely, emit
`MissingMethodContextOutput` first.

```yaml
MethodRoutingDecision:
  route: qualitative-only | quantitative-only | mixed-qual-first | mixed-quant-first | mixed-parallel
  primary_need: exploration | explanation | measurement | estimation | validation | triangulation
  rationale: string
  qualitative_capabilities_needed: []
  quantitative_capabilities_needed: []
  first_pass_outputs: []
  second_pass_outputs: []
  integration_rule: string
  why_not_other_routes: []
```

```yaml
MissingMethodContextOutput:
  missing_context: []
  why_it_matters: []
  recommended_default_route: qualitative-only | quantitative-only | mixed-qual-first | mixed-quant-first | mixed-parallel
  assumption_if_forced: string
```

## Routing Dimensions / 判斷維度

Classify the task on five dimensions in this order:

1. Is the core question about meaning, context, mechanism, or interpretation?
2. Is it about magnitude, comparison, significance, prevalence, or forecasting?
3. Are the constructs already defined, or still exploratory and unstable?
4. Is the available evidence mostly text and observations, mostly structured numbers, or both?
5. Is the goal decision support, design, validation, explanation, or triangulation?

Read the task through all five dimensions before picking a route.
Do not shortcut from one keyword.

Use [references/01-routing-rules.md](./references/01-routing-rules.md) for the
full route-selection matrix and tie-breakers.

## Route Definitions / 路由定義

- `qualitative-only`
  - Use for open exploration, framing, concept discovery, interview synthesis,
    case interpretation, mechanism building, or theory generation.
- `quantitative-only`
  - Use for estimation, benchmarking, hypothesis testing, forecasting,
    experiments, or structured metric comparison.
- `mixed-qual-first`
  - Use when constructs are fuzzy and the qualitative pass must define the
    dimensions, hypotheses, codebook, segments, or candidate variables before
    measurement.
- `mixed-quant-first`
  - Use when structured metrics already exist and the quantitative pass can
    surface anomalies, segments, drops, or outliers that need qualitative
    explanation.
- `mixed-parallel`
  - Use when both narrative and numeric evidence already exist and the result
    must be reconciled through triangulation.

## Downstream Capability Mapping / 下游能力對接

This skill must stay capability-based, not skill-name-based.
Do not hard-code downstream skill names.

Qualitative capability classes:

- interview synthesis
- coding
- thematic analysis
- case comparison
- contextual explanation

Quantitative capability classes:

- descriptive analysis
- scoring
- statistical testing
- modeling
- forecasting
- experiment analysis

Map available skills at runtime to these capability classes and choose the
smallest set that can complete the route.

## Workflow / 執行流程

1. Read the user's explicit method request, scope, and output constraints.
2. Score the task across the five routing dimensions.
3. Pick the smallest valid route.
4. Emit `MethodRoutingDecision`.
5. Map the route to capability classes, not named skills.
6. If one evidence stream is missing, choose the feasible primary route and
   explicitly name the complementary follow-up method.
7. For mixed routes, use [references/02-sequencing-and-integration.md](./references/02-sequencing-and-integration.md)
   to define the pass order and integration rule.
8. Do not claim triangulation unless both evidence streams actually exist.

## Evidence Availability Rule / 證據可得性規則

If the task is broad but only one evidence type is available:

- route to the feasible primary method
- name the missing complementary method as a follow-up
- do not fake a mixed-methods conclusion

Example:

- If the user asks `why did retention drop and how large is the drop` but only
  gives metrics, route to `mixed-quant-first` with a quantitative first pass and
  a qualitative follow-up recommendation.
- If the user asks to design a survey from interviews but only gives interviews,
  route to `mixed-qual-first` and keep the quantitative phase as a downstream
  validation step.

## Anti-Patterns / 禁止做法

Never do the following:

- frame qual and quant as mutually exclusive when the user is clearly asking for both
- force mixed methods for obviously single-method tasks
- treat `mixed methods` as `always output two equal sections`
- claim triangulation when only one evidence stream exists
- smooth over disagreement between evidence streams by averaging or vague wording

When mixed evidence conflicts, report the contradiction directly and test likely
causes such as sample mismatch, timeframe mismatch, construct mismatch,
measurement artifact, or segment heterogeneity.

## References

- Routing rules and tie-breakers: [references/01-routing-rules.md](./references/01-routing-rules.md)
- Mixed-route sequencing and conflict handling: [references/02-sequencing-and-integration.md](./references/02-sequencing-and-integration.md)
- Pressure scenarios and validation prompts: [references/03-validation-scenarios.md](./references/03-validation-scenarios.md)

## Suggested Prompt

Use `$orchestrating-mixed-methods` to choose the right qualitative,
quantitative, or mixed-methods route for this research task, emit a
`MethodRoutingDecision`, and explain the sequencing without forcing a false
either-or choice.

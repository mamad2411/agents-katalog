---
name: consumer-agent-landscape
description: >-
  Map the current consumer AI agent landscape for a build, investment, partnership, or competitive
  decision. Use when products need evidence-based comparison rather than a feature list.
---

# Consumer Agent Landscape

Produce a current, decision-specific market map. Separate verified facts from inference and do not
turn marketing claims into capability claims.

## Intake

Ask for these inputs, then wait:

1. The decision: build, invest, partner, acquire, defend, or monitor.
2. Target users, geography, and consumer job to be done.
3. Products or companies that must be included.
4. Time horizon and decision deadline.
5. Constraints such as privacy, distribution, hardware, regulation, or capital.
6. Existing beliefs the analysis should attempt to disprove.

## Research rules

- Research time-sensitive claims using current primary sources: official product pages,
  documentation, pricing, release notes, regulatory filings, company posts, and platform stores.
- Use reputable secondary reporting for market context only when a primary source is unavailable.
- Capture the access date for every source.
- Label company-provided usage, revenue, retention, or performance figures as self-reported.
- Mark inferred capabilities, unavailable evidence, and unresolved contradictions explicitly.
- Do not estimate private-company valuation, revenue, or user counts without a cited method.

## Workflow

### 1. Define the comparison set

Create an inclusion rule tied to the decision and apply it consistently. Organize products by their
primary interaction surface, such as messaging, browser, voice, desktop, mobile, wearable,
companion, builder, or vertical application. A product may have secondary surfaces, but assign one
primary category to avoid double counting.

### 2. Build an evidence card for each product

Capture:

- target user and core job;
- primary interaction surface and distribution channel;
- tasks the product can complete versus merely recommend;
- context sources and data retained;
- permission and confirmation model;
- reliability evidence and recovery behavior;
- privacy and security posture;
- pricing and monetization;
- signs of adoption, retention, or abandonment;
- dependencies on models, platforms, devices, or app ecosystems;
- cited sources and confidence level.

### 3. Score decision-relevant dimensions

Score each dimension from 0 to 5 only when evidence exists. Otherwise use `NE` (not enough
evidence). Define the anchors before scoring.

- **Problem value:** frequency and severity of the consumer problem.
- **Completion depth:** how much of the job is completed end to end.
- **Reliability:** consistency, error recovery, and user control.
- **Permission safety:** clarity, reversibility, and least privilege.
- **Context advantage:** durable context that improves outcomes without creating unacceptable risk.
- **Distribution:** credible path to repeated consumer use.
- **Monetization:** evidence that value and willingness to pay align.
- **Defensibility:** proprietary distribution, data rights, workflow depth, or ecosystem position.

For every score, provide one sentence of evidence and a confidence label: high, medium, or low.
Do not average `NE` values into a total.

### 4. Identify market structure

Group products into competitive clusters using shared user jobs and distribution—not superficial
feature similarity. Identify:

- direct competitors;
- substitutes and platform threats;
- crowded positions;
- underserved jobs or user groups;
- dependencies that could erase differentiation;
- capabilities likely to commoditize within the decision horizon.

### 5. Test scenarios

Evaluate at least three scenarios relevant to the horizon:

1. Base case: current distribution and trust patterns continue.
2. Platform shift: a major OS, browser, device, or model provider bundles the core capability.
3. Trust shock: a privacy, safety, or reliability failure changes user or regulatory behavior.

State which products gain or lose in each scenario and why.

### 6. Translate into a decision

Return an explicit recommendation tied to the original decision. Include:

- the most attractive segment and why;
- positions to avoid;
- required capabilities or partnerships;
- evidence that would reverse the recommendation;
- a 30-, 90-, and 180-day validation plan.

## Output

1. Executive decision summary.
2. Scope, inclusion rule, and research date.
3. Landscape table with evidence and confidence.
4. Scorecard using `0–5` or `NE`.
5. Competitive clusters and whitespace.
6. Scenario analysis.
7. Recommendation, reversal conditions, and validation plan.
8. Source list grouped by product.

## Guardrails

- Do not present a feature matrix as strategy.
- Do not reward a product for announced but unavailable capabilities.
- Do not hide missing evidence inside a numeric average.
- Do not recommend collection of consumer data without a lawful, understandable permission model.
- Do not make investment, acquisition, or market-entry claims without tying them to the user's
  constraints and horizon.

## Provenance

Original Cloud Byte Consulting implementation based on the competitive-landscape request captured
in the [Document Hub record](https://app.notion.com/p/d784b26ce26048c38e03fd125a7d1f5b).

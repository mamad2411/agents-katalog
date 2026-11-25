---
name: bottleneck
description: Diagnose the constraint that most limits an idea, product, project, codebase, architecture, workflow, AI agent, or operating system from achieving its goal. Use for feasibility reviews, pre-build idea audits, architecture and repository assessments, scaling-readiness checks, delivery slowdowns, reliability or cost investigations, "what will break first?", "why are we stuck?", and requests to find hidden risks or bottlenecks across business, product, people, process, data, dependencies, infrastructure, and code. Do not use for a narrow known performance hotspot when ordinary profiling alone is sufficient.
---

# What Are the Bottlenecks?

Find the limiting constraint, not the longest list of defects. Move from system goal to critical flow to evidence, then descend only into details capable of changing the diagnosis.

## Core rules

- Treat a bottleneck as a constraint on a stated goal under a stated scenario and horizon. Never call something a bottleneck in the abstract.
- Separate observed facts, user claims, inferences, assumptions, and unknowns.
- Distinguish `current constraint`, `emerging constraint`, `risk`, `symptom`, and `unknown`. Not every flaw limits throughput or outcomes.
- Prefer repository evidence, measurements, traces, user behavior, budgets, queues, failure history, and dependency limits over generic best-practice checklists.
- Audit the measurement system before trusting it. Contradictory, missing, sampled, or ambiguously labeled observations can make diagnostic capability the immediate constraint.
- Inspect broadly before drilling down. Do not begin with code quality when demand, distribution, compliance, data, ownership, or unit economics may be the real constraint.
- Rank bottlenecks relative to each other. A top-ten list with ten critical items is not a diagnosis.
- Recommend the cheapest decisive test before an expensive redesign.
- Do not optimize a non-constraint. Explain which downstream constraint is likely to appear if the current one is relieved.
- Preserve read-only scope unless the user asks for changes. Do not run load tests, paid calls, destructive probes, or production mutations without authorization.
- Present concise conclusions; do not expose private chain-of-thought. Provide an evidence-backed rationale and explicit uncertainty.

## Choose depth

Infer depth from the request and available evidence:

- `scan`: One artifact or early idea. Identify up to three likely constraints and the missing evidence that could reorder them.
- `audit`: Default for a repository or mature proposal. Map the system, inspect relevant artifacts, rank up to five constraints, and propose validation experiments.
- `deep`: Use only when the user asks for exhaustive analysis or the system is high-impact. Trace cross-layer causal chains, inspect history/runtime evidence, and test competing hypotheses.

State the selected depth and boundary in one line. If essential goal, scenario, or scale is unknown, use a provisional assumption and show how the answer changes under the nearest plausible alternative; ask only when a wrong assumption would make the audit unsafe or useless.

## Workflow

### 1. Frame the outcome

Define:

- desired outcome and success metric;
- actor or customer;
- scenario and operating horizon: now, next milestone, or target scale;
- hard constraints: time, money, people, policy, hardware, provider limits;
- evidence boundary: idea text, selected files, full repository, runtime, or external research.

If the target is an idea, write a minimal system model from acquisition/input through value delivery to retention/output. If the target is implemented, inspect the real source of truth before accepting documentation claims.

### 2. Map the critical flow

Trace the smallest end-to-end path that produces the desired outcome:

`demand/input -> admission -> transformation -> state/storage -> delivery -> feedback/recovery`

Adapt the labels to non-software systems. Mark handoffs, queues, serial stages, scarce resources, external dependencies, feedback delays, irreversible decisions, and single-owner or single-point-of-failure nodes.

Read [diagnostic-lenses.md](references/diagnostic-lenses.md) for an `audit` or `deep` pass. Select only relevant lenses; never mechanically dump the whole catalog.

### 3. Generate competing hypotheses

For every plausible bottleneck, capture:

- constrained goal or flow;
- mechanism: why this point limits the whole system;
- evidence for and evidence against;
- trigger or saturation threshold;
- consequence and blast radius;
- confidence and the decisive missing observation.

Search specifically for constraints outside the user's framing. For example, a bot with efficient code may still be limited by discovery, provider quotas, conversation state growth, moderation, human support, or negative unit economics.

Before ranking, check whether observations can distinguish the competing hypotheses. When they cannot, classify the underlying cause as `unknown` and the missing diagnostic capability as an action-blocking constraint; do not relabel ambiguous telemetry as a system failure.

### 4. Test constraint-ness

A candidate is a real constraint only if at least one is defensible:

- work or demand accumulates there;
- the resource is closest to saturation or has the least headroom;
- delays or failures propagate from it through the critical flow;
- increasing its capacity or quality would materially improve the goal;
- its hard limit blocks the next milestone before other limits do.

Use counterfactuals:

1. If this were fixed tomorrow, would the system outcome materially improve?
2. If demand or complexity doubled, would this be the first material failure?
3. Could the symptom persist because of an upstream cause?
4. Is this merely important, or actually rate-limiting?

Downgrade candidates that fail these tests to `risk`, `symptom`, or `unknown`.

### 5. Rank, then build the causal chain

Rank primarily by expected constraint pressure:

`pressure = impact x likelihood x urgency x propagation x irreversibility`

Use ordinal `low/medium/high` judgments, not fake decimal precision. Confidence is separate from severity. Prefer a lower-severity observed constraint over a spectacular but unsupported scenario unless the latter is an existential precondition.

For the top candidates, state the causal chain:

`driver -> accumulation/saturation -> local failure -> system effect -> goal impact`

Identify interactions and feedback loops. Select exactly one primary constraint per scenario when evidence permits; otherwise state that the result is provisional and name the observation that breaks the tie.

### 6. Prescribe validation and action

For each leading constraint, give:

- the cheapest discriminating measurement, inspection, interview, prototype, or test;
- expected observation if the hypothesis is true and if false;
- a threshold or decision rule;
- containment for immediate harm;
- structural remedy only after validation;
- owner or capability needed;
- likely next constraint after relief.

Favor actions that create information or headroom. Do not default to rewrites, new infrastructure, more agents, caching, queues, or hiring without showing how they relieve the primary constraint.

### 7. Report and stop

Use [report-contract.md](references/report-contract.md). Match the user's language. Lead with the primary constraint and why it dominates. Include a coverage statement so "whole project" never falsely implies that every file or runtime path was inspected.

Stop when additional inspection is unlikely to reorder the top constraints, or state what inaccessible evidence prevents convergence.

## Red flags

- Starting with a canned quality checklist before defining the goal and critical flow.
- Treating high CPU, large files, technical debt, missing tests, or storage growth as self-proving bottlenecks.
- Reporting only technical findings for a product or idea audit.
- Equating many files inspected with high coverage of user journeys or runtime behavior.
- Giving fixes without a validation signal, threshold, or expected outcome.
- Hiding uncertainty or inventing traffic, cost, latency, conversion, or team-capacity numbers.
- Recommending optimization that only moves work into an unbounded queue or another scarce stage.
- Producing more than five headline bottlenecks without grouping or prioritizing them.

## Completion check

Before answering, verify that the result:

- ties every headline finding to the goal, scenario, and critical flow;
- names the primary constraint or explains why evidence cannot distinguish it;
- differentiates evidence from hypotheses and severity from confidence;
- crosses relevant non-code and code layers;
- includes a decisive next test and decision rule for each top finding;
- predicts the next constraint after the primary one is relieved;
- states inspected scope, excluded scope, and material unknowns.

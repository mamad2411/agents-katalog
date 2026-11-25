---
name: attention-stock-nudge-scheduling
description: Applies Byrne, Goette, Martin, Miles, Jones, Schob, Staake & Tiefenbeck (SSRN 3974371, rev. Nov 2024; 700-household shower field experiment, 7 conditions) — the attention-stock model of habit formation with the (I,S,s) optimal feedback rule — as the ATTENTION-BUDGETING pattern: nudge effects build immediately and stably, decay sluggishly after the nudge stops, and cycling feedback with an initial attention-build phase beats exhausting the nudge budget up-front by ~15%. Use when scheduling recurring nudges, budgeting feedback frequency, or designing just-in-time reminder cadences.
---

# Attention-Stock Nudge Scheduling

## Overview
The first high-frequency cycling field experiment on nudge feedback dynamics shows effects are **asymmetric**: they emerge instantly, don't grow with exposure, and decay slowly after the nudge stops — so the optimal intervention is an initial build-up of feedback followed by on/off cycling that maintains an attention stock, not constant treatment.

## When to Use
- Designing reminder/notification cadence for recurring behaviors (energy, health, learning, spending)
- Budgeting limited feedback (cost, fatigue, annoyance) across a fixed intervention window
- Deciding between always-on, one-shot, and intermittent nudge schedules
- NOT for: post-treatment artifact persistence (use `nudge-persistence-meta-analysis-38-experiments`), or single-choice architecture redesigns where there's no repetition

## Core Process / Workflow

### The asymmetry finding (7-arm shower experiment, 700 households)
1. **Immediate onset**: feedback effect lands in full on the first exposure (−7.39 L/shower); no build-up across continued exposure (PostON slope ≈ 0.01, ns)
2. **Stable while on**: effects do not grow or wane with continued treatment
3. **Gradual decay after off**: +80 ml/shower per shower after feedback stops, trending back to baseline over ~59 showers ≈ 2 months
4. **Duration→persistence gradient**: longer feedback spells → longer persistence (48-shower arms retain nearly full effect post-off; 3-shower arms lose most of it)
5. **Asymmetry**: attention stock builds fast (αON≈0.081 → half-life 9 showers) and decays slowly (αOFF≈0.021 → half-life 33 showers)

### The (I,S,s) optimal rule
Structural counterfactual simulation over 1 trillion feedback sequences found the optimal allocation: an **initial continuous build-up (~17 showers)** to raise the attention stock, then **cycling on/off** to hold the stock in a narrow band (observed optimal band ~0.700–0.719). Against the naive "exhaust the budget immediately" rule, the (I,S,s) schedule yields **~15% larger average effect** (−5.97 vs −5.18 L/shower) under the same budget (K=48 in T=120).

### Design workflow
1. Estimate the decay half-life for your domain from existing telemetry (or default to the 33-shower ~2-month figure for daily behaviors)
2. Budget feedback as: build-up phase I (sustained) → maintenance phase cycling to hold attention in-band, not constant
3. Prefer *intermittent* feedback when budget-constrained: cumulative savings with cycling beat a front-loaded same-budget constant schedule (T4/T5 > T3 in raw totals)
4. Watch for the "attention-budget" caveat: attention spent on one behavior can crowd others (Shenhav et al.; Bronchetti et al.)
5. Combine with persistence design: attention stocks decay (Byrne); artifacts persist (Brandon et al.) — the full stack is cycle-to-maintain + artifact-to-keep

## References
- See [references/attention-stock-evidence.md](references/attention-stock-evidence.md) for the full design, parameters, and (I,S,s) mechanics.

### Pairs with
`nudge-persistence-technology-adoption`, `nudge-persistence-meta-analysis-38-experiments`, `behavioral-intervention-choice-tailoring`, `llm-personalized-nudge-friction-boundary`, `micro-moment-engagement-architecture`, `zero-friction-consumption-cognitive-4ps`.

## A-Tech Alignment
- **Open source:** the (I,S,s) rule is implementable as a cron/policy schedule in any open reminder system — no vendor dependency.
- **Privacy:** intermittent feedback needs fewer observations than always-on monitoring.
- **Financial freedom:** rationed feedback budgets = fewer push notifications, better retained savings behaviors.
- **Practical:** 15% free improvement over naive always-on for the same budget is a rare free lunch.

## Honesty Caveats
- Water/shower domain, one utility (South East Water, Melbourne); parameter transfer to other behaviors is a hypothesis, not a measurement.
- Structural estimates are model-dependent; the attention mechanism beat consumption-based habits *in this context* out-of-sample.
- The (I,S,s) optimality claim is model-based counterfactual, not an independent experiment of the rule itself.
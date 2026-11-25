---
name: model-routing-cascade
description: Route each LLM call to the cheapest model that can handle it, with confidence-based fallback to larger models. Use when one frontier model serves all traffic, when cost-per-call is uniform across vastly different task difficulties, or when designing a new GenAI feature for cost-efficient scale.
source: self
date_added: 2026-05-01
---

# Model Routing and Cascades

Most LLM workloads are a mix of trivial and hard requests served by one expensive model. Routing typically cuts spend 40-80% with no perceived quality loss.

## When to Use

- A single model class (e.g., Sonnet 4 / GPT-5 / Gemini 2.5 Pro) handles everything.
- Token volume is high and tasks vary in difficulty.
- Some calls are obviously simple (classification, extraction, formatting) but pay frontier prices.
- You can A/B and measure quality automatically (have evals).
- Vendor renewal or new-feature cost modelling.

## Two Patterns

### 1. Router (pick the right model up-front)

A small, cheap classifier picks a tier per request, then forwards once.

```
request → router(small/cheap) → tier {S, M, L} → model call → response
```

Pros: 1 model call, low latency, simple budgeting.
Cons: misroutes are uncorrected unless you also evaluate output.

### 2. Cascade (try cheap first, fall back on low confidence)

Try the small model; if its self-reported or scored confidence is below a threshold, escalate.

```
request → small model → confidence ≥ θ ? return : large model → return
```

Pros: corrects misroutes; very high savings on easy traffic.
Cons: 2 model calls on the hard tail; needs a confidence signal.

Combine: router selects S/M/L; cascade upgrades S→M→L on low confidence. This is the FrugalGPT-style pattern.

## Choosing Tiers

| Tier | Examples (2026) | Good for |
| --- | --- | --- |
| Nano / S | Haiku, GPT-5 nano, Gemini Flash-Lite | Classification, routing itself, format fixing, cache lookups |
| Mid / M | Sonnet, GPT-5 mini, Gemini Flash | Summarization, extraction, simple Q&A, RAG over short context |
| Frontier / L | Opus, GPT-5, Gemini Pro | Code generation, multi-step reasoning, agents, ambiguous tasks |
| Specialized | Embedding, OCR, code, vision-only | When the task is narrow — almost always cheaper than frontier |

Don't over-engineer. Two tiers (S, L) capture most of the savings; add M only when measured.

## Confidence Signals (Cascade)

Pick whatever your model exposes; combine when possible:

- **Logprobs** of generated tokens (lower entropy = more confident).
- **Self-rating**: ask the small model for a 1-5 confidence with structured output (cheap when in the same call).
- **Verifier model**: a separate small model scores the answer.
- **Schema validity**: if structured output fails or has empty/unknown fields, escalate.
- **Disagreement**: run twice at low temperature; mismatch → escalate.
- **Heuristics**: input length, presence of code, language detection, regex hits.

Calibrate the threshold on a held-out set; don't pick θ by intuition.

## Designing the Router

A 1-shot or rules-based router is enough to start:

1. Cheap call to the smallest model with a strict-output schema returning `tier ∈ {S, M, L}` and `reason`.
2. Cache router decisions by `hash(normalized_prompt_features)` — same query, same route.
3. Bypass the router entirely for known classes (URL patterns, API endpoints, tool names).
4. Log every routing decision and its outcome for retraining.

When the volume justifies it, replace the LLM router with a fine-tuned small classifier or a logistic regression on prompt features — orders of magnitude cheaper.

## Guardrails

- **Never escalate without bound.** Cascades with N tiers can call N models on a single request — cap N and total $.
- **Never demote silently.** When you switch a feature to a smaller model, ship it behind a flag with shadow traffic and compare on real evals first.
- **Per-tier accuracy SLO.** If accuracy on tier S drops below threshold, auto-promote traffic until you investigate.
- **Cost SLO.** Alert when cost-per-successful-task regresses, even if absolute spend is flat.

## Evaluation Loop

You can't route what you can't measure.

- Build a labelled eval set per task class (≥ 100 examples; grow over time).
- Score every tier offline; publish accuracy × cost × latency tables.
- For online traffic, sample 1-5% to a verifier model or human review.
- Re-evaluate when any model in the cascade is upgraded — discounts compound, but so do regressions.

## Implementation Sketch

```python
# pseudo
def route_and_call(req):
    tier = router(req)                       # cheap classification
    out  = call(tier, req)
    conf = confidence(out)
    if tier != "L" and conf < THRESHOLD[tier]:
        out = call(next_tier(tier), req)     # bounded escalation
    log(req, tier, conf, out, cost)
    return out
```

Keep it boring. The wins come from disciplined measurement, not clever code.

## Quick Wins Checklist

- [ ] Per-feature inventory of task types and their current model
- [ ] At least one task type moved to a smaller model with measured parity
- [ ] Router or cascade in place for the highest-volume feature
- [ ] Confidence threshold calibrated on a held-out set
- [ ] Bounded escalation (no infinite tier-walking)
- [ ] Per-tier accuracy and cost tracked on a dashboard
- [ ] Online sampling for ongoing quality monitoring
- [ ] Routing decisions cached for repeat queries

## Anti-Patterns

- Routing on intuition without an eval set.
- "Always frontier" because the team is afraid to measure regressions.
- Cascade with no upper bound — pathological inputs hit every tier.
- Using the frontier model as the router (it costs more than the call it routes).
- Switching models without A/B; trusting vendor benchmarks.
- Optimizing the router prompt instead of replacing it with a tiny classifier once volume justifies it.
- Ignoring latency: cascades can double p99 for the hard tail.

## References

- "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance" — Chen, Zaharia, Zou (2023)
- Anthropic, OpenAI, Google model and pricing pages (2026)
- Related skills: `llm-cost-optimization`, `token-efficient-prompting`, `prompt-caching-patterns`, `structured-output-design`, `agent-loop-budgeting`

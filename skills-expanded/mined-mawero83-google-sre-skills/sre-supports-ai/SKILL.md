---
name: sre-supports-ai
description: >-
  Operate AI/ML systems reliably: AI SLOs, accelerator capacity, model qualification, observability of nondeterministic systems, and safety — from SRE Book 2e Ch20. Use when productionizing models/agents/GPU fleets.
---

# How SRE Supports AI

**Domain:** `ai`  
**Sources:** SRE Book 2e Ch20

## When to use

- Launching AI features
- GPU/TPU fleet reliability
- Defining SLOs for model serving
- Qualifying new models/architectures

## Principles

- AI reliability includes serving latency/availability AND quality/safety dimensions.
- Accelerators need SLO-eligibility thinking, fungibility, and utilization/loss frameworks.
- Qualify models and hardware continuously — not one-time.
- Observability must handle nondeterminism and pipeline data risks.
- Security/compliance threats differ for model weights, prompts, and training data.

## Workflow

1. Define CUJs: interactive serving, batch inference, training pipeline.
2. Set SLIs: availability, latency, freshness of models, quality proxies, safety filters.
3. Plan capacity: accelerators, power, scheduling, demand shaping.
4. Add eval gates for model promotion (canary models).
5. Instrument failure modes unique to AI (OOM, thermal, drift, tool errors).
6. Document rollback to previous model/config.

## Decision guide

- If quality regresses but infra green → still a launch abort.
- If accelerators scarce → prioritize CUJs + efficiency work.

## Output template

```markdown
# AI reliability plan
- CUJs:
- SLIs/SLOs (infra + quality/safety):
- Capacity / accelerator plan:
- Qualification gates:
- Rollback:
```

## Anti-patterns

- Only uptime SLOs for LLM features.
- One-shot model launch without eval canary.

## Related skills

`sli-slo-design`, `capacity-planning`, `canarying-releases`, `ai-supports-sre`

## Canonical references

- [SRE Book 2e](https://sre.google/books/)
- [2e blog](https://cloud.google.com/blog/products/devops-sre/sre-book-second-edition)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.

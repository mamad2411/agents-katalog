---
name: ai-supports-sre
description: >-
  Use AI as an SRE force multiplier safely: triage assistance, telemetry interrogation, toil reduction, and bounded autonomy — from SRE Book 2e Ch21. Use when adopting AI ops tools or agentic incident helpers.
---

# How AI Supports SRE

**Domain:** `ai`  
**Sources:** SRE Book 2e Ch21, SRE Book 2e Ch10 (AI in IR)

## When to use

- Evaluating AIOps / AI on-call assistants
- Using AI during incidents or postmortems
- Designing autonomy levels for remediation agents

## Principles

- AI changes fast — optimize for durable principles, not one vendor feature.
- Humans remain accountable for risky production actions.
- Hierarchy of production health still applies; AI assists each layer.
- Prefer AI for situational awareness, hypothesis generation, draft comms/postmortems — with verification.
- Path to autonomy requires guardrails, evals, and audit (AI Operator north star).

## Workflow

1. Pick a narrow use case (triage summary, log cluster, draft RCA).
2. Define success metric (MTTA↓, toil hours↓) and failure mode (hallucination).
3. Require citation of telemetry/evidence in AI outputs.
4. Shadow mode vs human baseline.
5. Allow write/remediation actions only behind policy + kill switch.
6. Review weekly for wrong advice that almost shipped.

## Decision guide

- If AI suggests prod mutation → require human confirm unless explicitly allowlisted and reversible.
- If confidence without evidence → discard.

## Output template

```markdown
# AI-for-SRE adoption plan
- Use case:
- Autonomy level:
- Guardrails / evals:
- Success metric:
- Kill switch:
```

## Anti-patterns

- Autonomous remediations without audit.
- Trusting AI timelines without clock verification.
- Replacing on-call training with chatbot dependence.

## Safe AI assist patterns

| Pattern | OK? | Notes |
|---------|-----|-------|
| Summarize state doc | Yes | Verify entities |
| Rank hypotheses from metrics | Yes | Demand chart/query cites |
| Draft customer comms | Yes | Human approve |
| Auto-rollback prod | Only with policy | Reversible + allowlisted |
| Delete data / rotate all keys | No autonomous | Human + security |


## Related skills

`automation-tooling`, `incident-management`, `learning-from-incidents`, `sre-supports-ai`

## Canonical references

- [SRE Book 2e](https://sre.google/books/)
- [2e blog — AI themes](https://cloud.google.com/blog/products/devops-sre/sre-book-second-edition)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.

---
name: research-synthesis
description: Use this skill when researching technologies, synthesizing multiple sources, evaluating tech stack decisions, comparing frameworks, or writing technical research summaries. Trigger on keywords: research, compare, evaluate, which is better, technology decision, should I use, pros and cons, synthesis, stack decision.
---

# Research & Synthesis

## Research Process

```
1. DEFINE    — What specific question am I trying to answer?
2. GATHER    — Collect sources (docs, benchmarks, community, real usage)
3. EVALUATE  — Assess source quality and recency
4. SYNTHESIZE — Extract patterns and insights across sources
5. DECIDE    — Apply findings to your specific context
6. DOCUMENT  — Record the decision and reasoning for future reference
```

---

## Technology Evaluation Framework

For every technology comparison:

| Dimension | What to Evaluate |
|---|---|
| **Fit** | Does it solve your actual problem? |
| **Maturity** | Production-proven or experimental? |
| **Community** | Active maintenance, GitHub stars, Stack Overflow presence |
| **Performance** | Benchmarks relevant to your use case |
| **Learning Curve** | Team familiarity, documentation quality |
| **Ecosystem** | Integrations, libraries, tooling |
| **Cost** | License, infrastructure, ops overhead |
| **Exit Cost** | How hard to migrate away if needed? |

---

## Comparison Document Template

```markdown
## Decision: [technology choice]

### Context
[What problem are we solving? What are our constraints?]

### Options Considered
| | Option A | Option B | Option C |
|--|---------|---------|---------|
| Fit | | | |
| Maturity | | | |
| Performance | | | |
| Team familiarity | | | |
| Long-term risk | | | |

### Decision
[What we chose and why]

### Trade-offs Accepted
[What we give up with this choice]

### Revisit If
[Conditions that would prompt reconsideration]
```

---

## Source Quality Hierarchy

1. **Official docs** — authoritative, but may be biased toward positives
2. **Benchmarks** — verify the benchmark matches your use case
3. **Production case studies** — most reliable, but rare
4. **Community discussions** — useful for gotchas and real-world issues
5. **Blog posts** — variable quality, check date and author credentials

Always check the date. Technology moves fast — 2-year-old articles may be outdated.

---

## Using AI for Research

```
"Research [topic] and summarize:
1. What problem it solves
2. When to use it vs alternatives [A, B, C]
3. Known limitations and gotchas
4. Current community sentiment (2025-2026)
5. One concrete example of production usage"
```

Cross-reference AI output with official docs — AI can hallucinate library APIs or outdated information.

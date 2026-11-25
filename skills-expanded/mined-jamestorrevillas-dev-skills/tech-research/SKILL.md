---
name: tech-research
description: Use this skill when evaluating technologies, comparing frameworks, making build vs buy decisions, researching best practices, or synthesizing information for a technical decision. Trigger on keywords: should I use, which framework, technology comparison, evaluate, build vs buy, what's the best tool for, research this technology, is X worth learning.
---

# Technology Research

## Research Process

```
1. DEFINE    — What specific decision are we making?
2. CONSTRAIN — What are the non-negotiables? (team skills, budget, timeline)
3. GATHER    — Collect data from quality sources
4. COMPARE   — Evaluate options against the same criteria
5. DECIDE    — Choose with explicit reasoning
6. DOCUMENT  — Record the decision for future reference
```

---

## Technology Evaluation Criteria

| Criterion | What to Look For |
|---|---|
| **Problem Fit** | Does it actually solve YOUR problem? |
| **Maturity** | Production-proven? Version 1.x or 0.x? |
| **Community** | Active GitHub, Stack Overflow, Discord |
| **Maintenance** | Last commit? Open issues? Response time? |
| **Performance** | Benchmarks relevant to your scale |
| **Learning Curve** | Team familiarity, documentation quality |
| **Ecosystem** | Plugins, integrations, tooling |
| **Exit Cost** | How hard to migrate away? |
| **License** | MIT/Apache (permissive) vs GPL vs commercial |

---

## Source Quality Hierarchy

1. Official documentation — authoritative, check version
2. Production case studies — most reliable, hardest to find
3. Benchmark comparisons — verify the benchmark matches your use case
4. Respected technical blogs — check date and author credentials
5. Reddit / Hacker News — good for real-world sentiment and gotchas
6. YouTube tutorials — useful for learning, not for decisions

**Always check the date.** A 2-year-old comparison may be obsolete.

---

## Decision Document Template

```markdown
## Technology Decision: [topic]

**Date:** | **Decided by:**

### Context
[What problem are we solving? What are our constraints?]

### Options Evaluated
| Criterion | Option A | Option B | Option C |
|-----------|---------|---------|---------|
| Problem Fit | | | |
| Maturity | | | |
| Team Familiarity | | | |
| Performance | | | |
| Long-term Risk | | | |

### Decision
**Chosen:** [option]

**Reasoning:** [why this fits our specific context]

**Trade-offs accepted:** [what we give up]

**Revisit if:** [conditions that would change this decision]
```

---

## Build vs Buy Framework

**Build when:**
- This IS your core competitive differentiator
- No existing solution fits well enough (>40% custom needed)
- You have the expertise and time to maintain it

**Buy / Use OSS when:**
- It's infrastructure (auth, payments, email, queues)
- Time-to-market is critical
- Your users don't care who built the underlying tool
- Maintenance would distract from core product

**The hidden cost of building:** every line you write, you now own forever.

---

## Staying Current

Trusted sources for staying up to date:
- GitHub Trending (weekly)
- State of JS / State of CSS surveys (annual)
- Stack Overflow Developer Survey (annual)
- Official release blogs of tools you use
- Hacker News "Who's Hiring" (for industry signals)
- Thoughtworks Technology Radar (strategic view)

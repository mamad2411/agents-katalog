---
name: fill-in-missing-assumptions
description: "Identify hidden assumptions and test how changing them affects a recommendation or design."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["assumptions", "risk-management", "sensitivity-analysis", "architecture", "decision-making", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask AI to List Its Hidden Assumptions (AI Skill)

## Overview
Every time an AI answers a strategic, financial, or technical question, it silently fills undefined variables with default assumptions (*e.g., assuming you have infinite bandwidth, a $50k monthly budget, standard US legal jurisdiction, or a team of 10 senior engineers*).

The **Assumption Surfacing Protocol** forces the AI to declare all latent premises underneath its analysis - allowing you to adjust flawed presuppositions before making expensive decisions.

---

## The Assumption Extraction Framework

```
┌─────────────────────────────────────────────────────────────┐
│                 Assumption Surfacing Engine                 │
│                                                             │
│  [ RECOMMENDATION / PLAN ]                                  │
│              │                                              │
│              ▼                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. INFRASTRUCTURE & TECH: Versions, tools assumed     │  │
│  │ 2. TRAFFIC & SCALE: Requests/sec, database size       │  │
│  │ 3. BUDGET & RESOURCES: Team headcount, licensing cost │  │
│  │ 4. USER BEHAVIOR: Conversion rates, latency tolerance │  │
│  └───────────────────────────────────────────────────────┘  │
│              │                                              │
│              ▼                                              │
│  [ Sensitivity Check: If Assumption X changes $\rightarrow$ Impact ]│
└─────────────────────────────────────────────────────────────┘
```

---

## Master Assumption-Audit Prompt Templates

### Pattern 1: The Pre-Flight Assumption Audit
Use whenever receiving a complex technical, business, or marketing plan:

```markdown
Review the plan you just proposed above.

List your **Top 4 Core Assumptions** across these categories:
1. **Technical / Environment Assumptions**: (e.g. cloud provider, SDK versions, OS)
2. **Scale & Traffic Assumptions**: (e.g. daily active users, requests per second)
3. **Resource & Team Assumptions**: (e.g. implementation hours, skillset required)
4. **Economic & Cost Assumptions**: (e.g. ongoing SaaS fees, egress costs)

For each assumption, answer:
*"If this assumption is false, what is the single biggest risk to the plan?"*
```

---

### Pattern 2: The Sensitivity Inversion Test
Use when testing whether a plan holds up under extreme constraints:

```markdown
What happens to your proposed architecture if:
- Our budget is reduced by 50%?
- Our traffic spikes by 10x overnight?
- We cannot use proprietary third-party APIs?

Provide the modified, fail-safe recommendations.
```

---

## Real-World Case Study

### Scenario: Recommending an Elasticsearch Cluster

#### Unstated Assumptions (The Hidden Trap)
> **User**: *"What search solution should we use for our e-commerce store with 500,000 products?"*
> 
> **AI Default Recommendation**: *"Set up an Elasticsearch cluster on AWS OpenSearch with 3 master nodes and 6 data nodes."*
> 
> *(Hidden Assumption: The team has a dedicated DevOps engineer to manage shard rebalancing, cluster memory heaps, and index lifecycle policies, and can afford $1,200/mo in AWS compute).*

#### Surfaced Assumptions Output
> **User**: *"List the critical operational assumptions behind this recommendation."*

**AI Response**:
> **Declared Assumptions**:
> 1. **Budget**: Assumes an infrastructure spend of $\ge \$800/\text{month}$ for managed OpenSearch.
> 2. **Operations**: Assumes your team has experience tuning JVM garbage collection and mapping analyzers.
> 3. **Query Complexity**: Assumes you need complex fuzzy matching, vector semantic search, and multi-language stemmers.
>
> **Sensitivity Warning**:
> *"If you do not have dedicated DevOps staff or your monthly budget is $< \$100$, Elasticsearch is an operational trap. In that scenario, use **Meilisearch** or **Typesense** on a single $20/mo VPS instead."*

---

## Summary Best Practices
- **Never approve a plan without reading its assumptions**: It is where 90% of real-world budget blowouts hide.
- **Invert assumptions early**: Testing *"What if we have 1/5th the time?"* immediately surfaces simpler, higher-ROI alternatives.

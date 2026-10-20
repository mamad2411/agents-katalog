---
name: ask-ai-to-show-its-reasoning
description: "Request a concise explanation of assumptions, evidence, decision criteria, and trade-offs behind a recommendation."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["reasoning", "chain-of-thought", "decision-making", "trade-offs", "first-principles", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask AI to Show Its Reasoning (AI Skill)

## Overview
When an AI simply proclaims: *"I recommend Option B,"* you have no way to evaluate whether the conclusion is based on deep technical trade-offs or an arbitrary bias in training data. 

Forcing the AI to **expose its reasoning path** before stating its final recommendation achieves two critical outcomes:
1. **Dramatically higher accuracy**: Generating intermediate reasoning tokens allows the model to compute complex dependencies before finalizing the output.
2. **Auditability**: It allows humans to inspect the logical premises, identify flawed assumptions, and make fully informed decisions.

---

## The 4-Step Transparent Reasoning Framework

```
┌─────────────────────────────────────────────────────────────┐
│                 Transparent Decision Flow                   │
│                                                             │
│  1. Evaluation Criteria  ──► Weight key factors (Cost, Ops) │
│            │                                                │
│  2. Analysis of Options  ──► Strengths & fatal flaws        │
│            │                                                │
│  3. Elimination Logic    ──► Why alternatives were rejected │
│            │                                                │
│  4. Final Recommendation ──► Clear, defended conclusion    │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Reasoning Prompts

### Pattern 1: The First-Principles Decision Engine
Use this when choosing between technical architectures, business strategies, or tools:

```markdown
I need to decide between [OPTION A], [OPTION B], and [OPTION C] for [SPECIFIC USE CASE & CONSTRAINTS].

Structure your analysis as follows:
1. **Decision Criteria**: Define the 3-4 most critical factors that determine success for this scenario.
2. **Side-by-Side Trade-off Table**: Score each option against those criteria (High / Medium / Low or 1-5).
3. **Elimination Analysis**: Explain why each rejected option fails to meet the threshold.
4. **Final Recommendation**: State your chosen option with a 2-sentence executive defense.
```

---

### Pattern 2: The "Show Your Work" Logic Constraint
Use this for analytical, policy, or legal queries:

```markdown
Evaluate [SCENARIO / QUESTION].

Do not jump straight to the verdict.
First, explain:
- What premises or rules apply here?
- What evidence supports the claim?
- What counter-arguments or edge cases exist?

Then, conclude with your verdict based strictly on the evidence above.
```

---

## Real-World Examples

### Example 1: Database Architecture Decision

#### Opaque Recommendation (Low Value)
> **User**: *"Should I use DynamoDB or PostgreSQL for an IoT sensor platform collecting 50,000 writes/sec?"*
>
> **AI (Opaque)**: *"You should use DynamoDB because it is highly scalable and handles NoSQL workloads well."*

#### Transparent Reasoning Prompt & Output
> **User**: *"Evaluate DynamoDB vs. PostgreSQL for 50k sensor writes/sec. Show your reasoning, trade-offs, and elimination logic."*

**AI Response**:
1. **Evaluation Criteria**:
  - **Write Throughput**: Sustained 50,000 writes/sec with predictable sub-10ms latency.
  - **Query Patterns**: Time-series rollups, range queries, and device alerts.
  - **Cost at Scale**: Storage and I/O pricing under heavy ingestion.

2. **Analysis & Trade-Offs**:
  - **DynamoDB**:
    - *Pros*: Effortlessly scales to 50k writes/sec with on-demand or provisioned WCU. Zero server maintenance.
    - *Cons*: Cost scales linearly with write volume ($$$); analytical range queries and time-series aggregation require exporting to S3/Athena.
  - **PostgreSQL (with TimescaleDB extension)**:
    - *Pros*: Native time-bucket aggregation, compression ratios up to 90%, cost-effective on large EBS volumes.
    - *Cons*: Requires cluster tuning (connection pooling with PgBouncer, auto-partitioning/hypertables, replica management).

3. **Elimination Logic**:
  - Standard vanilla PostgreSQL is **eliminated** due to table bloat and write lock contention at 50k writes/sec.
  - Pure DynamoDB is **eliminated** if complex time-series queries (e.g., 7-day moving averages across sensor fleets) are required in-database without secondary tooling.

4. **Recommendation**:
  - **Choose TimescaleDB (PostgreSQL)** if you need rich SQL analytics and fixed infrastructure costs.
  - **Choose DynamoDB** if zero-operational overhead and pure key-value ingestion speed outweigh cost and analytical flexibility.

---

## Summary Matrix

| Mode | Prompt Approach | When to Use |
| :--- | :--- | :--- |
| **Fast Lookup** | Direct single-line answer | Syntax lookups, definitions, translations. |
| **CoT Reasoning** | *"Think step-by-step before answering"* | Math, logic puzzles, multi-file code debugging. |
| **Comparative Reasoning**| *"Show criteria, trade-offs, and elimination logic"* | Tech stack choices, strategy, investments, hiring rubrics. |

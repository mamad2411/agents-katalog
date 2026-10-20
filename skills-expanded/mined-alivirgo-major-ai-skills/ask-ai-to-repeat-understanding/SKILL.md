---
name: ask-ai-to-repeat-understanding
description: "Restate the intended outcome, scope, and constraints when a complex task needs an alignment check."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["alignment", "intent-paraphrasing", "planning", "scope-management", "clarity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask AI to Confirm Understanding Before Execution (AI Skill)

## Overview
On complex, high-stakes tasks (e.g., refactoring an entire module, summarizing a 50-page contract, or structuring a quarterly campaign), leaping straight into execution often results in 1,500 tokens of output that solved the wrong problem or violated an unstated constraint.

This skill introduces the **Echo-Back & Intent Alignment Protocol**: a simple gatekeeping mechanism that forces the AI to summarize its interpretation of the goal, constraints, and scope *before* writing a single line of deliverable content.

---

## The Intent Alignment Gate

```
┌─────────────────────────────────────────────────────────────┐
│                 The 2-Phase Execution Gate                  │
│                                                             │
│  User Complex Prompt ──► [ GATE: Echo & Plan ]             │
│                                │                            │
│                 ┌──────────────┴──────────────┐             │
│                 ▼                             ▼             │
│        Misalignment Detected?         100% Aligned?         │
│                 │                             │             │
│        Adjust in 1 sentence           Execute Full Solution │
│        (Saves 90% wasted time)        with Zero Errors      │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Alignment Prompt Templates

### Pattern 1: The Pre-Execution Alignment Gate (High-Stakes Tasks)

```markdown
I have a complex task for you: [PASTE PROJECT DETAILS / REQUIREMENTS].

DO NOT generate the final deliverable yet.
First, respond with a concise "Intent Alignment Summary" containing:
1. **Primary Goal**: In 1-2 sentences, what is the core outcome you need to achieve?
2. **Key Constraints**: What are the strict limitations, formats, and rules you must follow?
3. **In-Scope vs. Out-of-Scope**: What will you build vs. what will you explicitly leave untouched?
4. **Assumptions**: What are you assuming about my requirements that wasn't explicitly stated?

Conclude by asking: "Shall I proceed with execution?"
```

---

### Pattern 2: The Fast "In-Line Echo" (Medium Tasks)
For faster, single-turn tasks where you still want visible alignment:

```markdown
Generate [DELIVERABLE] based on [INPUT].

Before providing your final answer, begin with a 2-line "Target Alignment" block confirming your understanding of the audience, tone, and main constraint.
```

---

## Real-World Case Studies

### Example 1: Database Migration & Schema Refactoring

#### Risky Direct Prompt
> **User**: *"Migrate our MongoDB user schemas to PostgreSQL relational tables. Here are 12 JSON schemas..."*
>
> ❌ *AI immediately generates 400 lines of SQL, creating flat tables with `jsonb` columns everywhere, completely ignoring normalized relations and indexing.*

#### Alignment Gate Prompt
> **User**: *"Before writing SQL, summarize how you plan to map the nested JSON arrays (e.g., user addresses and payment methods) into PostgreSQL tables."*
>
> **AI Response**:
> **Intent Alignment**:
> 1. **Primary Goal**: Convert MongoDB document collections into normalized PostgreSQL 16 schemas.
> 2. **Mapping Plan**:
>   - `user.addresses` $\rightarrow$ Separate `user_addresses` table with `user_id` foreign key.
>   - `user.payment_methods` $\rightarrow$ Separate `payment_methods` table linked via `user_id`.
>   - `user.metadata` $\rightarrow$ Native `JSONB` column inside the `users` table.
> 3. **Assumptions**: Using UUIDv4 primary keys and `ON DELETE CASCADE` for child tables.
>
> *Shall I generate the migration script based on this architecture?*
>
> **User**: *"Make foreign keys `ON DELETE RESTRICT` instead of cascade, then proceed."* (Saved 20 minutes of code editing).

---

### Example 2: Executive Summary of Technical RFC

> **User Prompt**:
> *"Before drafting the summary of this 40-page Kubernetes migration RFC for our CFO, tell me the 3 financial metrics you will highlight."*
>
> **AI Alignment Response**:
> 1. **Compute Cost Reductions**: Moving from static EC2 instances to Karpenter-managed EKS spot autoscaling (projected ~35% annual savings).
> 2. **Migration CapEx**: 3-month transition tooling and third-party consultant costs ($85,000).
> 3. **Risk Mitigation ROI**: Reduced outage risk, avoiding historical downtime costs averaging $18,000/hr.
>
> *Is this financial emphasis aligned with your CFO's current focus?*

---

## Alignment Checklist

| Dimension | Question to Verify |
| :--- | :--- |
| **Objective** | Is the AI solving the real root problem or just a symptom? |
| **Scope** | Is the AI trying to do too much (or too little)? |
| **Constraints** | Did the model remember word limits, file paths, libraries, or banned tokens? |
| **Assumptions** | Did the model make assumptions about versions, environments, or audience? |

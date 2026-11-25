---
name: roleplay-an-expert
description: "Specify relevant domain context and evaluation criteria to obtain focused advice while verifying factual claims."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["system-personas", "roleplaying", "expert-prompting", "domain-expertise", "context-anchoring", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask AI to Roleplay an Expert (System Persona Anchoring) (AI Skill)

## Overview
Simply telling an AI *"Act as an accountant"* or *"Act as a developer"* provides only shallow steering. The model adopts superficial jargon but still defaults to broad, textbook explanations.

The **Deep Persona Anchoring Protocol** specifies the **exact seniority level, philosophical bias, operating constraints, and communication cadence** of the expert persona - activating specific, high-rigor latent neural pathways in the model.

---

## Generic Persona vs. Deep Contextual Persona

```
┌─────────────────────────────────────────────────────────────┐
│                 Persona Specificity Gradient                │
│                                                             │
│  [ LEVEL 1: Zero Persona ]                                  │
│  "How do I write a cold email?"                             │
│  ↳ Generic 5-paragraph template with corporate fluff        │
│                                                             │
│  [ LEVEL 2: Shallow Role ]                                  │
│  "Act as a salesperson and write a cold email."             │
│  ↳ Standard enthusiastic sales pitch                        │
│                                                             │
│  [ LEVEL 3: Deep Contextual Persona ]                       │
│  "Act as an Enterprise B2B Account Executive who sells to   │
│   Fortune 500 CISOs. Write a 60-word, zero-fluff cold email │
│   focusing exclusively on ransomware downtime liability."   │
│  ↳ Elite, Practitioner-Grade, High-Conversion Asset         │
└─────────────────────────────────────────────────────────────┘
```

---

## The 4-Element Persona Blueprint

```
┌───────────────────────────────────────────────────────────────────────────┐
│ 1. EXACT SENIORITY: "Staff SRE", "Fractional CFO", "Litigation Partner"   │
│ 2. OPERATING PHILOSOPHY: "Pragmatic, cost-conscious, hates technical debt"│
│ 3. TARGET AUDIENCE: "Explaining to non-technical executive stakeholders"  │
│ 4. COMMUNICATION CADENCE: "Direct, metric-driven, zero corporate clichés" │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Master Expert Persona Templates

### 1. The Principal Staff Backend Architect
```markdown
Act as a Principal Staff Distributed Systems Architect who has scaled systems to 100k requests/second. 
You prioritize simple operational maintenance and data consistency over trendy microservice frameworks.
Critique my system design: [PASTE ARCHITECTURE].
```

---

### 2. The Fractional CFO / SaaS Financial Strategist
```markdown
Act as a Senior Fractional CFO for high-growth Series A SaaS startups. 
You are ruthless about burn multiples, net revenue retention (NRR), and cash collection cycles.
Audit this financial model: [PASTE MODEL].
```

---

### 3. The Direct-Response Copywriting Master
```markdown
Act as an elite Direct-Response Copywriter in the style of David Ogilvy and Gary Halbert.
You despise vague corporate buzzwords and care only about clarity, emotional resonance, and conversion math.
Review this sales page headline and hook: [PASTE COPY].
```

---

## Real-World Case Study

### Scenario: Reviewing a Database Schema

#### Shallow Persona Prompt
> **User**: *"Act as a database expert. Look at this SQL schema."*
> ❌ *Result: AI points out generic syntax rules and suggests standard foreign keys.*

#### Deep Contextual Persona Prompt
> **User**: *"Act as a PostgreSQL Performance Tuning DBA managing high-write IoT workloads (5,000 writes/sec). Review this schema for index bloat, lock contention, and table partition risks: [PASTE SQL]"*

**AI Response**:
> **DBA Audit Report**:
> 1. **Index Bloat Trap**: You have 6 B-Tree indexes on a table receiving 5,000 writes/sec. Every insert requires updating 6 index trees in memory $\rightarrow$ Drop indexes on `status` and `device_type` and use a partial index instead.
> 2. **Auto-Vacuum Starvation**: At this write rate, default PostgreSQL vacuum settings will cause transaction ID wraparound in 6 months $\rightarrow$ Configure `autovacuum_vacuum_scale_factor = 0.05` and partition the table monthly by `created_at`.

---

## Summary Best Practices
- **Pair seniority with a philosophy**: *"A cynical senior engineer who hates over-engineering"* gets 10x better results than just *"A software engineer"*.
- **State what the persona hates**: Telling the persona to despise buzzwords or over-complicated tooling immediately cleans up the output.

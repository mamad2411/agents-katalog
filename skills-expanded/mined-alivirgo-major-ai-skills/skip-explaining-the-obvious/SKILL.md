---
name: skip-explaining-the-obvious
description: "Match explanations to the reader's existing expertise and omit background they already understand."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["senior-baseline", "introductory-suppression", "conciseness", "token-savings", "expert-prompting", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Skip Explaining the Obvious (The Senior Baseline Protocol) (AI Skill)

## Overview
When an experienced engineer or professional asks an advanced question (*"How do I configure Prometheus alerting for Kubernetes pod crash-loops?"*), default AI models spend the first two paragraphs explaining what Kubernetes and Prometheus are. 

This introductory padding is frustrating for domain experts and wastes valuable output tokens.

The **Senior Baseline Protocol** commands the model to assume advanced practitioner competence, bypass introductory definitions, and dive directly into implementation details.

---

## 101 Definition Padding vs. Senior Baseline Execution

```
┌─────────────────────────────────────────────────────────────┐
│                 Output Signal-to-Noise Ratio                │
│                                                             │
│  Default Unbounded Query:                                   │
│  "Kubernetes is an open-source container orchestration      │
│   platform designed to automate deploying, scaling, and     │
│   operating application containers. Prometheus is an..."    │
│  ↳ 0% Signal, 100% Wasted Tokens & Time                     │
│                                                             │
│  Senior Baseline Modifier:                                  │
│  "Assume I am a Senior SRE. Skip all basic definitions."    │
│  ↳ "Here is the `PrometheusRule` YAML with the 5m metric... │
│  ↳ 100% Signal, Instant Production Utility                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Senior Baseline Prompt Modifiers

### Pattern 1: The Expert Baseline Directive (Technical)
```markdown
[INSERT TECHNICAL QUESTION]

Constraints:
- Assume I am a Senior / Staff Engineer with 10+ years of experience.
- Do NOT explain basic terminology, history, or obvious prerequisites.
- Jump straight to the architectural trade-offs, configuration snippets, and code.
```

---

### Pattern 2: The Domain Specialist Anchor (Finance / Legal)
```markdown
[INSERT FINANCIAL / LEGAL QUESTION]

Directive:
- Target Audience: Experienced Financial Analyst / Commercial Attorney.
- Skip definitions of standard metrics (e.g. do not explain what EBITDA or NPV is).
- Focus purely on calculation edge cases and statutory nuances.
```

---

## Real-World Comparison

### Scenario: Tuning PostgreSQL Auto-Vacuum for High-Write Tables

#### Without Senior Baseline (Verbose 101 Definition)
> **AI Output**:
> *"PostgreSQL is a powerful, open-source object-relational database system. When rows are updated or deleted in PostgreSQL, the old versions of those rows (called 'dead tuples') are left behind in the table. Auto-vacuum is a background process that cleans up these dead tuples so disk space can be reused..."*
> 
> ❌ *(150 words wasted explaining what auto-vacuum is).*

#### With Senior Baseline Protocol
> **Prompt**: *"Assume Senior DBA background. What exact `ALTER TABLE` parameters should I tune for a table getting 2,000 updates/second to prevent table bloat?"*

**AI Output**:
```sql
-- Tune per-table autovacuum thresholds for high-write tables:
ALTER TABLE high_frequency_events SET (
    autovacuum_vacuum_scale_factor = 0.02,       -- Trigger vacuum after 2% row changes (vs 20% default)
    autovacuum_vacuum_cost_limit = 2000,         -- Increase cost limit to speed up cleanup
    autovacuum_vacuum_cost_delay = 2,            -- Reduce delay to minimize lock time
    autovacuum_analyze_scale_factor = 0.01       -- Refresh planner stats after 1% changes
);
```

---

## Summary Best Practices
- **Add 1 line**: *"Assume advanced familiarity with this topic; skip basics."*
- **Specify the exact role level**: *"Explain this to a Staff Level Engineer"*.
- **Save it to your Custom Instructions**: If you are technical, put *"Assume senior domain competence on all software engineering queries"* in your account settings.

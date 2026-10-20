---
name: pros-and-cons-table
description: "Compare options using benefits, drawbacks, weighted criteria, and reversibility when making a decision."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["decision-matrix", "pros-and-cons", "trade-offs", "impact-scoring", "reversibility", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask for a Weighted Pros & Cons Matrix (AI Skill)

## Overview
A basic two-column pros-and-cons list is often misleading because it treats every bullet point equally - treating a minor advantage (*"Clean user interface"*) with the same visual weight as a fatal flaw (*"Lacks regulatory compliance"*).

The **Weighted Multi-Attribute Matrix Protocol** upgrades simple pros/cons into a rigorous decision framework, evaluating trade-offs across **Impact, Implementation Effort, Financial Cost, and Reversibility**.

---

## Naive List vs. Weighted Decision Matrix

```
┌─────────────────────────────────────────────────────────────┐
│                 Naive List vs. Weighted Matrix              │
│                                                             │
│  Naive 2-Column List:                                       │
│  Pros: Fast, cheap, popular                                 │
│  Cons: Security risk, hard to scale                         │
│  ↳ Flawed: Security risk is 100x more important than "cheap"│
│                                                             │
│  Weighted Decision Matrix:                                  │
│  Evaluates Options $\times$ Weighted Criteria (1-10)        │
│  • Separates Type 1 (Irreversible) from Type 2 (Reversible) │
│  • Produces a mathematically defended composite score       │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Weighted Matrix Prompt Templates

### Pattern 1: The Multi-Attribute Decision Matrix
Use when evaluating vendors, technical stacks, or strategic investments:

```markdown
I am deciding between [OPTION A] and [OPTION B] for [USE CASE].

Construct a **Weighted Decision Matrix** Markdown table with these columns:
| Evaluation Dimension | Weight (1-5) | [OPTION A] Score (1-10) | [OPTION B] Score (1-10) | Weighted Winner & Key Trade-off |

Include these dimensions:
1. Implementation Speed / Time to Value
2. Total Cost of Ownership (TCO)
3. Operational Maintenance Overhead
4. Scalability / Ceiling
5. Reversibility (How easy is it to undo this choice?)

Conclude with:
- Total Weighted Composite Score for each option.
- A 2-sentence executive decision recommendation.
```

---

### Pattern 2: The Type 1 vs. Type 2 Reversibility Filter
Based on Jeff Bezos's decision framework (One-way doors vs Two-way doors):

```markdown
Evaluate the risks of [PROPOSED ACTION / DECISION].
- Is this a **Type 1 Decision** (Irreversible one-way door: high risk, hard to undo)?
- Or a **Type 2 Decision** (Reversible two-way door: low risk, fast rollback)?
- What is the cheapest experiment we can run to test this before committing?
```

---

## Real-World Case Study

### Scenario: Build In-House vs. Buy Third-Party Auth (Auth0 / Clerk)

#### Weighted Matrix Output

| Dimension | Weight (1-5) | Build In-House (NextAuth) | Buy Third-Party (Clerk) | Weighted Analysis |
| :--- | :--- | :--- | :--- | :--- |
| **Time to Launch** | 5 | 4/10 (2-3 weeks) | **9/10 (2 hours)** | Clerk saves ~100 engineering hours upfront. |
| **Monthly Cost at Scale** | 3 | **10/10 ($0 / free)** | 5/10 ($0.02 / MAU) | In-house has zero SaaS subscription tax. |
| **Security & Compliance** | 5 | 6/10 (Team liability) | **10/10 (SOC2, Passkeys)**| Clerk eliminates credential breach liability. |
| **Custom UI Control** | 2 | **9/10 (100% custom)** | 7/10 (Themeable UI) | In-house offers infinite custom flexibility. |
| **Reversibility** | 4 | 5/10 (Hard migration) | **8/10 (Exportable JWTs)** | Clerk allows easy JWT export if needed. |

**Composite Score**:
- **Build In-House**: $(5\times 4) + (3\times 10) + (5\times 6) + (2\times 9) + (4\times 5) = \mathbf{118}$
- **Buy Third-Party (Clerk)**: $(5\times 9) + (3\times 5) + (5\times 10) + (2\times 7) + (4\times 8) = \mathbf{156}$

**Executive Verdict**:
> **Choose Clerk (Third-Party)**. For a startup, the security compliance guarantees and 2-hour implementation velocity heavily outweigh the future per-user SaaS cost.

---

## Summary Best Practices
- **Assign weights before scoring**: Decide which criteria matter most (e.g. Security = 5, Cost = 2) *before* evaluating tools.
- **Always check Reversibility**: Reversible (Type 2) decisions should be made in minutes; irreversible (Type 1) decisions warrant deep matrices.

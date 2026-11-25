---
name: ask-ai-confidence-rating
description: "Identify uncertainty, assumptions, and claims needing verification when reviewing an AI answer."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["confidence-rating", "epistemic-calibration", "risk-assessment", "uncertainty", "fact-checking", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask AI for Confidence & Uncertainty Ratings (AI Skill)

## Overview
Standard LLMs produce responses with an unwavering, authoritative tone regardless of whether they are stating a verified mathematical axiom or guessing an obscure regulatory nuance. 

This skill provides an **Epistemic Calibration Framework** that instructs AI models to evaluate their own certainty, explicitly flag assumptions, and provide numeric confidence ratings for each component of an analysis.

---

## The Confidence Calibration Matrix

```
┌─────────────────────────────────────────────────────────────┐
│                 Certainty Breakdown Scale                   │
│                                                             │
│  [90-100%] HIGH CERTAINTY ──► Established facts, syntax,   │
│                               mathematical derivations      │
│  [60-89%]  MODERATE       ──► Best practices, industry      │
│                               heuristics, common patterns   │
│  [0-59%]   LOW / SPECULATIVE► Rapidly changing data, niche  │
│                               laws, subjective predictions  │
└─────────────────────────────────────────────────────────────┘
```

---

## The Calibrated System Prompt Template

Use this prompt modifier for research, technical architecture, legal/tax guidelines, and high-stakes problem solving:

```markdown
Answer the following query: [INSERT QUESTION]

Formatting Requirements:
1. Provide the direct, actionable answer first.
2. Underneath your answer, include a "Certainty & Risk Breakdown" with:
  - **Confidence Score (1-100%)**: State your overall confidence in the factual accuracy of this response.
  - **High-Certainty Elements**: List the specific points you are 100% sure about.
  - **Uncertainty & Assumptions**: Explicitly list any assumptions, ambiguities in my prompt, or edge cases where this answer might fail.
  - **Verification Step**: Provide the single most effective action I can take to verify this independently (e.g., official docs page, CLI test, calculation).
```

---

## Real-World Examples

### Example 1: Software Infrastructure Migration

#### Naive Prompt
> *"Can I migrate Postgres 12 directly to Postgres 16 using `pg_upgrade` in AWS RDS?"*
>
> **Uncalibrated AI Response**: *"Yes, AWS RDS supports direct major version upgrades from PostgreSQL 12 to 16 using `pg_upgrade`."* (Authoritative, but misses crucial downtime, parameter group, and extension deprecation caveats).

#### Calibrated Confidence Prompt
> **User**: *"Answer the upgrade question, but include a Confidence & Edge Case Audit."*
>
> **AI Calibrated Response**:
> **Answer**: Yes, AWS RDS supports multi-major-version automated upgrades from PostgreSQL 12 directly to 16 without intermediate hops.
>
> **Certainty & Risk Breakdown**:
> - **Confidence Score**: **95%** (AWS RDS documentation officially supports multi-version in-place upgrades).
> - **High-Certainty Elements**: The RDS upgrade engine handles binary conversion automatically; downtime will be incurred during the catalog update.
> - **Uncertain / Risk Areas (5%)**: 
>   1. PostGIS or custom extensions installed on v12 may have breaking schema changes in v16.
>   2. Custom parameter groups must be manually recreated for PostgreSQL 16.
> - **Verification Action**: Run `aws rds modify-db-instance --db-instance-identifier <id> --engine-version 16.2 --dry-run` or test on a restored snapshot first.

---

### Example 2: Contractual & Tax Clause Analysis

#### Calibrated Assessment Example
> **User Prompt**: *"Is home office rent 100% tax deductible for an LLC in California if the room is also used for occasional guest lodging? Rate your confidence."*
>
> **AI Calibrated Response**:
> **Answer**: **No.** Under IRS guidelines (IRC § 280A) and California Franchise Tax Board rules, home office deduction requires **regular and exclusive use**. Using the space for guest lodging disqualifies it from the simplified or actual expense deduction.
>
> **Certainty Breakdown**:
> - **Confidence Score**: **99%** (The "exclusive use" requirement is a strict statutory standard with near-zero ambiguity in US federal and California tax code).
> - **Key Caveat**: Daycare facilities and inventory storage have minor statutory exceptions, none of which apply to guest lodging.
> - **Verification Action**: Review IRS Publication 587 (*Business Use of Your Home*), page 3 ("Exclusive Use Rule").

---

## Guarding Against "False Modesty" & "Overconfidence"

| Model Tendency | What Happens | How to Fix It in the Prompt |
| :--- | :--- | :--- |
| **Overconfidence Bias** | Gives 100% certainty to hallucinated API endpoints | Add: *"Penalize your score if the library is newer than 2023 or frequently changes APIs."* |
| **Sycophancy** | Drops confidence simply because user asked "Are you sure?" | Add: *"Do not lower your rating just because I question it. Defend factually grounded points."* |
| **Generic Disclaimers** | Dumps boilerplate ("I am an AI, consult a doctor/lawyer") | Add: *"Skip generic boilerplate; evaluate only the epistemic certainty of the factual statements."* |

---

## Tactical Summary Checklist
- When confidence is **$\ge 90\%$**: Safe to proceed with standard testing.
- When confidence is **$60 - 89\%$**: Always verify against official documentation or run a sandbox trial.
- When confidence is **$< 60\%$**: Treat the AI output merely as a brainstorming prompt, not an actionable recommendation.

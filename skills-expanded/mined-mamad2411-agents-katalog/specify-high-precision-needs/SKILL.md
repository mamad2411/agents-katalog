---
name: specify-high-precision-needs
description: "State verification requirements, acceptable uncertainty, and evidence needs for accuracy-sensitive tasks."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["precision-mode", "high-stakes", "compliance", "zero-extrapolation", "fact-checking", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Specify High-Precision Needs (High-Stakes Precision Mode) (AI Skill)

## Overview
By default, language models operate in a conversational mode that balances factual accuracy with stylistic creativity and brevity. For casual writing or brainstorming, this balance is ideal. However, for **financial audits, regulatory compliance checks, medical documentation, or safety-critical engineering**, creative interpolation is unacceptable.

The **High-Stakes Precision Protocol** explicitly shifts the AI into **Zero-Extrapolation Mode**: demanding 100% evidentiary grounding, verbatim citations, and explicit rejection of unverified claims.

---

## Casual Mode vs. High-Stakes Precision Mode

```
┌─────────────────────────────────────────────────────────────┐
│                 Operating Mode Comparison                   │
│                                                             │
│  Casual Mode (Default):                                     │
│  • Optimizes for smooth flow, helpful tone, and speed       │
│  • Smooths over missing facts with educated guesses         │
│  • Tolerates approximate arithmetic and generalized terms   │
│                                                             │
│  High-Stakes Precision Mode:                                │
│  • Zero-tolerance for ungrounded claims                     │
│  • Every assertion must cite an exact verbatim source clause│
│  • Replaces guesses with "NOT FOUND IN SOURCE"              │
│  • Exact deterministic calculation execution                │
└─────────────────────────────────────────────────────────────┘
```

---

## The High-Precision Constraint Stack

When accuracy is paramount, append this 4-point constraint stack to your prompt:

```markdown
### 🔒 HIGH-STAKES PRECISION DIRECTIVE:
1. **Zero Extrapolation**: State ONLY facts that are explicitly verifiable in the provided text. Do NOT infer, extrapolate, or assume.
2. **Mandatory Citation**: Precede every claim with the exact `[Section / Page / Line Number]` identifier and a direct quote.
3. **Explicit Refusal of Unknowns**: If a specific data point is missing, output: `[DATA NOT PRESENT IN SOURCE]`. Do NOT attempt to provide an estimate.
4. **Deterministic Calculation**: Show the mathematical formula step-by-step or run Python code; do not approximate.
```

---

## Master High-Precision Prompt Templates

### Pattern 1: The Regulatory & Compliance Audit
Use for SOC2, ISO-27001, HIPAA, or financial audit reviews:

```markdown
Context: This analysis is for a formal regulatory compliance audit.

Attached Policy: [ATTACH DOCUMENT]

Audit Question: [INSERT COMPLIANCE QUESTION: e.g. What is our data retention and disposal policy for customer PII?]

Formatting Requirements:
- State the exact compliance rule.
- Quote the verbatim clause from the policy.
- Note any ambiguities where the policy fails to meet the standard.
- Do not provide conversational filler.
```

---

### Pattern 2: Safety-Critical Engineering Review
Use for database migrations, security IAM policies, or payment handlers:

```markdown
Review this database migration script: [PASTE SQL].

Precision Constraints:
- Assume this will run on a 50M-row production database with zero allowed downtime.
- Identify any table locks (exclusive locks, metadata locks), index build delays, or replication lag risks.
- If any command creates an exclusive lock, provide the non-blocking concurrent alternative.
```

---

## Real-World Case Study

### Scenario: Checking ISO 27001 Backup Encryption Compliance

#### Casual Prompt Output (Ambiguous & Dangerous)
> *"Your company backs up data daily and uses encryption. The AWS snapshots are stored securely in S3."*
> ❌ *(Fails the audit: Are the keys customer-managed? What cipher is used? How often are recovery drills performed?)*

#### High-Precision Mode Output (Audit-Ready)
> **Audit Finding (Section 8.2 - Backup Architecture)**:
> - `[Clause 8.2.1, Pg 14]`: *"All database snapshots shall be encrypted at rest using AES-256 via AWS KMS Customer Managed Keys (CMK) with annual key rotation."* $\rightarrow$ **COMPLIANT**
> - `[Clause 8.2.4, Pg 15]`: *"Recovery drills must be executed quarterly and recorded in the audit log."* $\rightarrow$ **FLAGGED / DEFICIENCY**: Document specifies quarterly schedule but shows zero recorded test logs for Q1/Q2.

---

## Summary Best Practices
- **Explicitly announce the high-stakes context**: Tell the model: *"This is for an official legal audit / production deployment."*
- **Demand binary verdicts**: Require the model to output `COMPLIANT`, `NON-COMPLIANT`, or `INSUFFICIENT DATA`.

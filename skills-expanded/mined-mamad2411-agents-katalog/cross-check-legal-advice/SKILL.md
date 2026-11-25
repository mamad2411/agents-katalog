---
name: cross-check-legal-advice
description: "Use AI for legal issue-spotting, plain-language clause explanations, and questions to verify with licensed counsel."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["legal-research", "compliance", "issue-spotting", "contracts", "safety", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Cross-Check Legal & Compliance Information (AI Skill)

## Overview
Large Language Models are exceptional at translating dense legalese into plain English and spotting missing clauses in standard boilerplate. However, AI assistants are **not licensed attorneys**: they cannot assess local jurisdictional nuances, recent statutory changes, or courtroom enforceability, and they may hallucinate non-existent case precedents.

This skill establishes the **Legal Issue-Spotting Protocol**: using AI to understand contractual mechanics and draft targeted questions, while ensuring all binding decisions are reviewed by certified legal counsel.

---

## The Legal Copilot Boundary

```
┌─────────────────────────────────────────────────────────────┐
│                 The Safe Legal Workflow                     │
│                                                             │
│  [ WHAT AI DOES SAFELY (Issue-Spotting & Prep) ]            │
│  • Explains legalese terms in plain English                 │
│  • Identifies missing boilerplate (e.g. indemnity, IP terms)│
│  • Generates a list of targeted questions for your lawyer   │
│                                                             │
│  [ WHAT REQUIRES LICENSED COUNSEL (Binding Judgment) ]      │
│  • Confirming state / local jurisdictional enforceability   │
│  • Signing binding settlements, agreements, or NDA waivers  │
│  • Final litigation strategy & liability risk sign-off      │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Legal Prep Prompt Templates

### Pattern 1: The Contract Issue-Spotter & Redline Helper
Use when reviewing commercial contracts, MSAs, or NDAs:

```markdown
Analyze the attached contract clause: [PASTE CLAUSE].

Context: I am the [BUYER / SELLER / SERVICE PROVIDER] based in [STATE / COUNTRY].

Provide:
1. **Plain-English Translation**: What does this clause actually mean in simple terms?
2. **Who It Favors**: Does this favor the other party or my company?
3. **Risk Exposure**: What is the worst-case liability or financial risk under this wording?
4. **Proposed Redline**: A balanced, fair revision to protect my interests.
5. **Questions for My Attorney**: 2 specific questions I should ask my legal counsel before signing.
```

---

### Pattern 2: The Regulatory Checklist Generator
Use when preparing for compliance audits (GDPR, CCPA, HIPAA, SOC2):

```markdown
We are building [PRODUCT FEATURE] that processes [DATA TYPES].

Generate an informational compliance checklist for [REGULATION: e.g. GDPR].
- List the key technical requirements (consent, right-to-erasure, encryption).
- Highlight areas where regulatory interpretation is evolving.
- Note: Format strictly as an exploratory preparation guide for our legal team.
```

---

## Real-World Case Study

### Scenario: Reviewing a Non-Compete / Non-Solicit Clause

#### Unsafe Habit (Taking AI as Legal Fact)
> **User**: *"Is this 2-year nationwide non-compete clause enforceable in California?"*
>
> ❌ *AI gives a brief "No, California bans non-competes", but misses nuances about business sale exceptions or non-solicitation of trade secrets.*

#### Safe Issue-Spotting & Lawyer Prep Output
> **AI Issue-Spotting Response**:
> 1. **Statutory Landscape**: Under California Business and Professions Code § 16600 (and 2024 amendments SB 699 / AB 1076), non-compete agreements are void and unenforceable for employees regardless of where signed.
> 2. **Key Exceptions**: Valid only in narrow scenarios (e.g., sale of a business goodwill interest).
> 3. **Actionable Checklist for Counsel**:
>   - Ask your lawyer to confirm whether the agreement includes an unlawful penalty clause.
>   - Request an explicit severability clause so an invalid non-compete doesn't jeopardize the rest of the employment contract.

---

## The Golden Rules of AI Legal Safety
1. **Never cite AI case law in court**: Avoid referencing specific case citations (*"Smith v. Jones"*) without pulling the actual brief from a verified legal database (Westlaw / LexisNexis).
2. **Always state your jurisdiction**: Laws in California, Delaware, the EU, and Singapore differ drastically.
3. **Use AI to lower attorney billable hours**: Use AI to draft the first summary and organize questions - saving your lawyer hours of preliminary issue-spotting time.

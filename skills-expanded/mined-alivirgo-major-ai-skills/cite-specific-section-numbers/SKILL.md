---
name: cite-specific-section-numbers
description: "Anchor document analysis to exact sections or pages so readers can verify the supporting passage."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["citations", "document-analysis", "legal", "compliance", "verification", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask AI to Cite Section & Clause Numbers (AI Skill)

## Overview
When analyzing a 60-page PDF, API specification, employee handbook, or vendor contract, generic AI summaries often make claims like *"The policy allows 15 days of remote work."* Without exact section citations, you have to spend 20 minutes manually searching the document to confirm whether the model understood the clause or confused it with vacation rollover.

The **Section-Anchored Citation Protocol** forces the AI to bind every fact, rule, and recommendation directly to an exact chapter, clause number, or header title.

---

## The Section-Anchored Citation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Section-Anchored Audit Flow                 │
│                                                             │
│  Unanchored Summary:                                        │
│  "Contract has a 30-day termination notice requirement."    │
│  ↳ Unverifiable $\rightarrow$ High liability risk           │
│                                                             │
│  Section-Anchored Summary:                                  │
│  "• [Section 8.4(b), Page 22]: Either party may terminate   │
│     with 30 days written notice, subject to early exit fee."│
│  ↳ 1-Second Instant Verification in Original Document       │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Section-Citation Prompt Templates

### Pattern 1: The Strict Section-Anchored Policy Audit
Use this for compliance frameworks, legal contracts, manuals, and bylaws:

```markdown
Analyze the attached document: [ATTACH DOCUMENT / PASTE TEXT].

Answer the following question: [INSERT QUESTION]

Strict Formatting Rules:
1. Every claim, rule, or restriction you mention MUST start with the exact bracketed section identifier: `[Section X.X / Header Title / Page Y]`.
2. Include a 1-sentence verbatim quotation directly from that section to substantiate the point.
3. If the document does not explicitly mention this topic, output: "NOT SPECIFIED IN DOCUMENT". Do not extrapolate.
```

---

### Pattern 2: The Clause-to-Action Reference Table
Use for comparing vendor SLAs, enterprise agreements, or security policies:

```markdown
Review the vendor contract and extract key operational obligations into a Markdown table:

| Obligation / Topic | Clause # / Section | Exact Rule Summary | Direct Quote |
```

---

## Real-World Case Study

### Scenario: Auditing a Cloud Vendor SLA (Service Level Agreement)

#### Unanchored Output (Low Trust)
> *"The vendor guarantees 99.9% uptime. If they fail, you get service credits. Scheduled maintenance is excluded."*
>
> ❌ *(Zero specifics: How are credits calculated? What is the maintenance window notice? Where in the contract does it say this?)*

#### Section-Anchored Citation Output (High Trust)

| Metric / Term | Clause Identifier | Operational Rule | Verbatim Source Quote |
| :--- | :--- | :--- | :--- |
| **Monthly Uptime SLA** | `[Section 3.1, Pg 4]` | 99.9% availability across calendar month excluding scheduled windows. | *"Provider guarantees Monthly Uptime Percentage of at least 99.9%."* |
| **Credit Calculation** | `[Section 3.4(a), Pg 5]` | 10% credit for $<99.9\%$, 25% credit for $<99.0\%$, 50% credit for $<95.0\%$. | *"Service Credits shall be applied as a percentage of monthly billing..."* |
| **Maintenance Notice** | `[Section 4.2, Pg 6]` | Minimum 72 hours advance email notice required for non-emergency patches. | *"Scheduled Maintenance requires 72 hours prior written electronic notice."* |
| **Credit Claim Window** | `[Section 3.6, Pg 5]` | Must be claimed in writing within **14 calendar days** of the outage month. | *"Customer must submit claim within 14 days of the end of the affected month."* |

---

## Key Benefits
- 🔍 **Instant Verification**: Find the exact clause in 2 seconds via `Ctrl + F`.
- 🛡️ **Zero Hallucination Shield**: Forcing clause citations drastically reduces the AI's tendency to invent terms that don't exist.
- 💼 **Executive & Legal Ready**: Deliverables can be passed directly to legal or procurement without rewriting.

---
name: keep-sensitive-financials-private
description: "Prepare redacted or synthetic financial inputs for AI-assisted analysis while keeping confidential source values private."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["data-privacy", "anonymization", "financial-safety", "security", "confidentiality", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Keep Sensitive Financials Private (Data Anonymization) (AI Skill)

## Overview
Pasting confidential company profit & loss (P&L) statements, employee salary sheets, bank account numbers, or secret cap tables into public AI models poses serious corporate security, compliance (GDPR/SOC2), and competitive risks.

The **Data Anonymization & Synthetic Scaling Protocol** enables you to leverage AI's advanced mathematical and financial reasoning capabilities while keeping 100% of your real confidential financial numbers and customer identities secret.

---

## The Synthetic Scaling Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Synthetic Anonymization Flow                │
│                                                             │
│  [ REAL CONFIDENTIAL DATA ]:                                │
│  • Client: Acme Bank                                        │
│  • Actual ARR: $1,420,000                                   │
│  • Burn Rate: $85,000/mo                                    │
│                            │                                │
│                            ▼                                │
│  [ LOCAL SANITIZATION (Apply 2.5x Multiplier + Alias) ]:     │
│  • Client: "Enterprise Client Alpha"                        │
│  • Synthetic ARR: $3,550,000                                │
│  • Synthetic Burn: $212,500/mo                              │
│                            │                                │
│                            ▼                                │
│  [ PROMPT AI FOR FORMULAS & ANALYSIS (Zero Privacy Risk) ]  │
│  • AI calculates runway ratios and margin percentages       │
│  • Ratios are mathematically identical to the real numbers! │
└─────────────────────────────────────────────────────────────┘
```

---

## The 3 Rules of Safe Financial Prompting

### 1. The Proportional Scaling Trick
Multiply or divide all your raw numbers by a fixed constant (e.g. $1.5\times$ or $10\times$). 
Because financial metrics (Gross Margin %, Runway in Months, CAC-to-LTV ratio, Year-over-Year Growth %) are proportional, the AI's financial analysis will be **100% mathematically valid**, while your real confidential balance remains completely hidden.

### 2. Entity Aliasing (Search & Replace)
Never include real company names or individual personnel:
- Replace *"JPMorgan Chase"* with *"Tier-1 Enterprise Bank"*.
- Replace *"Sarah Connor ($180k/yr)"* with *"Lead Engineer A ($X/yr)"*.

### 3. Strip Account Identifiers
Always purge credit card numbers, routing numbers, Tax IDs (EIN/SSN), and wire transfer codes.

---

## Master Anonymized Financial Prompt Templates

### Pattern 1: The Scaled Runway & Unit Economics Analysis

```markdown
Analyze the unit economics of this SaaS company based on anonymized, normalized metrics:

Financial Snapshot (Indexed/Normalized Units):
- Monthly Recurring Revenue (MRR): 100 units
- Cost of Goods Sold (Hosting + Support): 22 units
- Sales & Marketing Spend: 35 units
- R&D / Engineering Payroll: 40 units
- General & Administrative: 15 units
- Net Monthly Burn: 12 units
- Cash in Bank: 180 units

Task:
1. Calculate the Gross Margin percentage.
2. Calculate the exact cash runway in months.
3. Provide 3 specific recommendations to reach break-even cash flow.
```

---

## Real-World Comparison

### Scenario: Reviewing an Acquisition Term Sheet

#### Risky Prompt (Confidential Leak)
> ❌ *"Here is the confidential term sheet from Microsoft offering $18.5M for my startup WidgetCo with a 4-year earnout for founders Alice and Bob..."*
> *(Violates NDA and exposes deal valuation to third-party model training).*

#### Anonymized Safe Prompt
> ✅ *"Review this anonymized acquisition term sheet for a B2B SaaS company:
> - Offer: $X Cash at closing + 25% Earnout tied to Year 2 revenue targets.
> - Founder Retention: 3-year non-compete and 2-year vesting clawback.
> 
> What are the 3 biggest contractual and tax traps founders face in this structure?"*

---

## Privacy Checklist Before Hitting Send
- [ ] Are all company, customer, and employee names converted to aliases?
- [ ] Are absolute dollar amounts scaled or converted to percentages/ratios?
- [ ] Have all bank account numbers, tax IDs, and addresses been deleted?
- [ ] Does this prompt comply with your organization's corporate data security policy?

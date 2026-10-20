---
name: double-check-ai-math-manually
description: "Independently check AI-generated calculations using source inputs, formulas, and a calculator or spreadsheet."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["math-verification", "financial-safety", "invoicing", "spreadsheets", "deterministic-computing", "calculations"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Double-Check AI Math Manually (Deterministic Verification) (AI Skill)

## Overview
Because Large Language Models are probabilistic language generators rather than algebraic engines, they can generate an impeccable financial breakdown where the individual line items look flawless, but the **sum at the bottom is subtly wrong by $150 or 2.5%**.

The **3-Tier Math Verification Ladder** provides a safety net to ensure that no AI-generated financial quote, invoice, equity cap table, or budget is delivered without deterministic proof of accuracy.

---

## The 3-Tier Math Verification Ladder

```
┌─────────────────────────────────────────────────────────────┐
│                 3-Tier Math Safety Ladder                   │
│                                                             │
│  [ TIER 1: AI Formula Derivation ]                          │
│  • Define variables, logic, and standard formulas           │
│                           │                                 │
│                           ▼                                 │
│  [ TIER 2: Code / Python Execution ]                        │
│  • Force the AI to execute Python math programmatically     │
│                           │                                 │
│                           ▼                                 │
│  [ TIER 3: Deterministic Human Check ]                      │
│  • Paste values into Excel, Google Sheets, or a calculator  │
│  • 100% Guaranteed Mathematical Integrity                   │
└─────────────────────────────────────────────────────────────┘
```

---

## High-Risk Math Scenarios Requiring Tier-3 Verification

1. **Client Invoices & Estimates**: Multi-line hourly rates with discounts and tax percentages.
2. **Cap Tables & Equity Dilution**: Post-money SAFE notes, option pools, and vesting calculations.
3. **Loan & Mortgage Amortization**: Compound interest formulas ($M = P \frac{r(1+r)^n}{(1+r)^n - 1}$).
4. **Tax Withholdings & Deductions**: Progressive bracket brackets and FICA thresholds.

---

## Master Deterministic Math Prompt Templates

### Pattern 1: The Spreadsheet Formula Generator (Safest Approach)
Instead of asking the AI to calculate the total, ask it for the exact Excel/Google Sheets formula:

```markdown
I have the following billing items: [LIST ITEMS, HOURS, & RATES].

Do NOT just calculate the total yourself.
Provide:
1. A Markdown table of the items.
2. The exact **Excel / Google Sheets formulas** (e.g. `=SUM(C2:C10)`, `=B2*C2*(1-D2)`) so I can paste this directly into a spreadsheet to calculate the verified numbers.
```

---

### Pattern 2: The Multi-Check Python Verification Block

```markdown
Calculate [FINANCIAL / COMPOUND MATH PROBLEM].

Output Requirements:
1. Show the mathematical formula with named variables.
2. Provide a standalone Python 3 script using `decimal.Decimal` (not floating point) to compute the exact figures.
3. Print intermediate line items and the final sum.
```

---

## Real-World Case Study

### Scenario: Freelance Project Quote with Retainer Discount

#### Unverified AI Output (Subtle Arithmetic Drift)
```text
Item A: 40 hrs @ $125/hr = $5,000
Item B: 15 hrs @ $150/hr = $2,250
Item C: Server Setup Flat Fee = $800
Subtotal = $8,050
10% Early Bird Discount = $805
Total Due: $7,145
```
⚠️ *Look closely: $8,050 - $805 = **$7,245**, NOT $7,145. An unverified quote would lose you $100 on the invoice!*

#### The Excel-Verified Output
```markdown
| Item | Hours | Rate | Total Formula |
| :--- | :--- | :--- | :--- |
| **Development** | 40 | $125.00 | `=B2*C2` ($5,000.00) |
| **UX Review** | 15 | $150.00 | `=B3*C3` ($2,250.00) |
| **Infrastructure**| 1 | $800.00 | `=B4*C4` ($800.00) |
| **Subtotal** | | | `=SUM(D2:D4)` ($8,050.00) |
| **10% Discount** | | | `=D5*0.10` ($805.00) |
| **Final Total** | | | `=D5-D6` (**$7,245.00**) |
```

---

## Core Rule of Financial Safety
> **"Never sign or send an AI calculation without letting a deterministic engine (Python, Excel, Calculator) sum the final line."**

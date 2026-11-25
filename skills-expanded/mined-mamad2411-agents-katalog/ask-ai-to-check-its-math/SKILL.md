---
name: ask-ai-to-check-its-math
description: "Check arithmetic with explicit formulas and a calculator or executable code before presenting numerical results."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["math", "chain-of-thought", "python-execution", "program-aided-language", "fact-checking", "calculations"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask AI to Verify & Execute Math (AI Skill)

## Overview
Large Language Models process numbers as textual tokens rather than numeric variables in an ALU (Arithmetic Logic Unit). When performing multi-step multiplication, compound interest calculations, or fractional conversions, models frequently suffer from "attention drift" and output confidently incorrect figures.

This skill teaches the **Program-Aided & Chain-of-Thought Math Framework**: prompting strategies that force the AI to break math into explicit, verifiable atomic steps or execute pure Python code for 100% computational determinism.

---

## The 2 Paths to Zero-Error AI Math

```
┌──────────────────────────────────────────────────────────────┐
│                    Reliable Math Pathways                    │
│                                                              │
│  Path A: Program-Aided Language (PAL)                        │
│  Prompt ──► AI writes Python code ──► Code runs ──► Exact Ans│
│                                                              │
│  Path B: Explicit Scratchpad (Chain-of-Thought)              │
│  Prompt ──► Variable Table ──► Formula ──► Step-by-step math │
└──────────────────────────────────────────────────────────────┘
```

---

## Master Math Prompt Templates

### Pattern 1: The Program-Aided Math Directive (Recommended for Complex Math)
Forces the AI to write and execute code rather than guessing token probabilities:

```markdown
Solve this calculation: [INSERT WORD PROBLEM / DATA]

Instructions:
1. Write a complete, executable Python script to compute the exact answer.
2. Define each variable clearly with its units.
3. Print the intermediate variables and the final formatted total.
4. Output the result from the code execution.
```

---

### Pattern 2: The Explicit Step-by-Step Scratchpad (For Pure Text Interfaces)
When tool execution is unavailable, use this chain-of-thought constraint:

```markdown
Calculate the following: [INSERT PROBLEM]

Rules for calculation:
1. State the given variables and their values in a bulleted list.
2. Write down the exact mathematical formula in standard notation.
3. Compute each intermediate step on a separate line. Do NOT combine operations.
4. Double-check your arithmetic in reverse (e.g., verify multiplication using division).
5. State the final answer clearly with units and appropriate rounding.
```

---

## Real-World Examples

### Example 1: Compound Annual Growth Rate (CAGR)

#### Fragile Prompt (Prone to Guessing)
> *"Our revenue was $1.2M in 2020 and grew to $3.4M in 2024. What is our CAGR?"*
>
> ❌ *Standard AI output often estimates ~30% without calculating $(3.4 / 1.2)^{1/4} - 1$.*

#### Bulletproof PAL Prompt
> **User**: *"Calculate our CAGR from $1.2M (2020) to $3.4M (2024) using a Python calculation block."*

```python
# CAGR Formula: (End_Value / Start_Value) ** (1 / n_years) - 1
start_value = 1_200_000
end_value = 3_400_000
years = 2024 - 2020 # 4 years

growth_factor = end_value / start_value
cagr = (growth_factor ** (1 / years)) - 1
cagr_pct = cagr * 100

print(f"Growth Factor: {growth_factor:.4f}")
print(f"Exact CAGR: {cagr_pct:.2f}%")
# Output: Growth Factor: 2.8333, Exact CAGR: 29.73%
```

---

### Example 2: Prorated Subscription Billing

#### Scratchpad Calculation Prompt
> **User Prompt**:
> *"A customer upgrades from a $40/month plan to a $100/month plan on day 12 of a 30-day billing cycle. Calculate the exact prorated invoice charge. Use an explicit step-by-step scratchpad."*

**AI Response**:
1. **Given Data**:
  - Old Plan Monthly Rate: $40.00
  - New Plan Monthly Rate: $100.00
  - Cycle Length: 30 days
  - Days remaining in cycle: $30 - 12 = 18$ days

2. **Daily Rates**:
  - Old Daily Rate: $\frac{\$40}{30} = \$1.3333\dots$ / day
  - New Daily Rate: $\frac{\$100}{30} = \$3.3333\dots$ / day
  - Daily Differential: $\$3.3333 - \$1.3333 = \$2.0000$ / day

3. **Prorated Charge Calculation**:
  - Charge = $18 \text{ days} \times \$2.00/\text{day} = \mathbf{\$36.00}$

4. **Reverse Verification**:
  - Unused credit on old plan: $18 \times \$1.3333 = \$24.00$
  - Cost of new plan for remaining period: $18 \times \$3.3333 = \$60.00$
  - Net invoice addition: $\$60.00 - \$24.00 = \mathbf{\$36.00}$. Confirmed.

---

## Math Safety Heuristics

| Problem Type | Risk Level | Safe Approach |
| :--- | :--- | :--- |
| **Simple Addition / Subtraction ($< 3$ digits)** | Low | Direct prompt with step-by-step display. |
| **Percentages & Discounts** | Medium | Demand fractional breakdown (e.g. `$100 \times (1 - 0.15)$`). |
| **Multi-digit Multiplication / Division** | High | Request Python calculation. |
| **Financial Formulas (NPV, IRR, Amortization)** | Critical | Must use Python (`numpy-financial` or pure formula scripts). |
| **Unit & Metric Conversions** | Medium | State conversion factors explicitly in the prompt. |

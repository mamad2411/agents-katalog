---
name: always-verify-numbers-and-links
description: "Verify statistics, contact details, calculations, and URLs against appropriate sources before using them in a deliverable."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["fact-checking", "hallucination-prevention", "verification", "urls", "math-grounding", "safety"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Always Verify Numbers and Web Links (AI Skill)

## Overview
Large Language Models (LLMs) do not compute math or maintain an internal web directory in real time - they predict the most probable sequence of tokens. As a result, AI assistants can invent plausible-looking URLs, 404 links, outdated statistics, and subtly incorrect arithmetic with complete grammatical confidence.

This skill outlines the **Grounding & Verification Protocol**: a strict set of operating rules to validate figures, test web endpoints, and force AI models to ground their claims in verifiable data.

---

## Why AI Hallucinates Numbers & Links

```
┌─────────────────────────────────────────────────────────────┐
│                    The Hallucination Trap                   │
│                                                             │
│  User Asks: "What is the URL for the IRS form 1099-MISC?"   │
│                                                             │
│  AI Internal Probability:                                   │
│  "https://www.irs.gov/forms-pubs/about-form-1099-misc" (92%)│
│  ↳ Plausible URL structure generated purely from token patterns │
│  ↳ Result in 35% of cases: HTTP 404 (Page Not Found)       │
└─────────────────────────────────────────────────────────────┘
```

1. **Token Stitching**: The model synthesizes domain names, paths, and slugs based on common internet grammar rather than checking live DNS records.
2. **Arithmetic Estimation**: Without a dedicated Python execution environment or calculator plugin, multi-step math (especially compound percentages and multi-digit multiplication) is approximated via semantic probability, frequently leading to calculation drift.
3. **Temporal Blind Spots**: Outdated dates, pricing tiers, and changed support numbers are confidently cited from stale training weights.

---

## The 4-Point Grounding Audit

Before using any AI-generated figure or URL in production, emails, presentations, or contracts, run through this checklist:

```
[ ] 1. CLICK-TEST: Did you click the URL directly in an incognito window?
[ ] 2. SOURCE-CHECK: Is the stat attributed to a named primary source (e.g. "BLS 2024 Report") rather than a generic claim ("Studies show...")?
[ ] 3. CALC-RUN: Did you re-run the final math formula through a calculator or Python snippet?
[ ] 4. RECENCY-VERIFY: Does the date match the current quarter or fiscal year?
```

---

## Master Verification Prompting Techniques

### Technique 1: Force Citation of Direct Text (Extract, Don't Invent)
When providing source documents, force the AI to quote the exact text before calculating.

```markdown
Analyze the attached financial report and answer [QUESTION].

Constraints:
1. Every statistic, percentage, and dollar figure in your answer must be directly preceded by an exact verbatim quote from the text.
2. If the document does not explicitly state the figure, write: "NOT SPECIFIED IN SOURCE". Do not estimate or interpolate.
3. Show the exact calculation formula step-by-step before stating the final total.
```

---

### Technique 2: Disallow URL Generation (Use Search Directives Instead)
Instead of asking for links, ask for exact search queries or verified anchors.

```markdown
Recommend the 3 best open-source libraries for [TASK].

Do NOT attempt to write full URL links. 
Instead, provide:
1. The exact project name
2. The GitHub repository owner/repo handle (e.g., "facebook/react")
3. The exact search phrase to find the official documentation on Google.
```

---

## Real-World Examples

### Example 1: Budget & Cost Estimation

#### Risky Habit (Unchecked AI Math)
> **User**: *"We have 14 engineers at $120/hr working 32 hours a week for 6 weeks. Plus 18% management overhead. What is the total budget?"*
>
> **AI (Without Execution)**: *"Total hours = 2,688. Base cost = $322,560. Plus 18% overhead ($58,060.80) = **$380,620.80**."*
> 
> ⚠️ *(Subtle math error: 14 × 32 × 6 = 2,688 hours. 2,688 × 120 = $322,560. 322,560 × 0.18 = $58,060.80. 322,560 + 58,060.80 = $380,620.80. But if an intermediate step flips a digit like 2,788, the entire client quote is destroyed.)*

#### Safe Verification Prompt
> **User**:
> *"Write a concise Python script to calculate the exact total, print the step-by-step breakdown, and output the final verified number."*

```python
engineers = 14
rate_per_hour = 120
hours_per_week = 32
weeks = 6
overhead_pct = 0.18

base_hours = engineers * hours_per_week * weeks  # 2,688
base_cost = base_hours * rate_per_hour           # $322,560.00
overhead = base_cost * overhead_pct              # $58,060.80
total_budget = base_cost + overhead              # $380,620.80

print(f"Hours: {base_hours}, Base: ${base_cost:,.2f}, Total: ${total_budget:,.2f}")
```

---

## Common Failure Modes & Quick Fixes

| Failure Mode | Root Cause | Quick Fix |
| :--- | :--- | :--- |
| **Dead Links (404)** | Model hallucinates URL path syntax | Demand search terms and domain names only. |
| **Hallucinated Citations** | Model creates fake authors & paper titles | Ask for DOI numbers or PubMed/ArXiv IDs and verify on Google Scholar. |
| **Math Rounding Drift** | LLM computes token-by-token | Force the model to generate a Python one-liner to calculate the exact figure. |
| **Outdated Pricing** | SaaS tiers change faster than model weights | Require the AI to state its knowledge cutoff date and verify against the live pricing page. |

---

## Golden Rule
> **"Treat all AI-generated URLs, phone numbers, prices, and math totals as unverified hypotheses until clicked or calculated by an external engine."**

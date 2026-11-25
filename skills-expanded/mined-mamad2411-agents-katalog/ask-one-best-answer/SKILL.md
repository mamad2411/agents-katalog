---
name: ask-one-best-answer
description: "Request one recommended option with its rationale when a long list would obscure the decision."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["pareto-principle", "one-best-answer", "decision-making", "focus", "high-leverage", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask for the One Best Answer (The 80/20 Leverage Rule) (AI Skill)

## Overview
When users ask an AI for *"10 ideas to grow revenue"* or *"5 ways to fix this performance bug,"* the model spreads its token budget and attention across multiple mediocre, generic suggestions. 

By commanding the AI to give **the single highest-conviction, highest-leverage recommendation**, you force the model to rank options internally and output a deeply fleshed-out, immediately executable plan.

---

## List Dilution vs. The Single Best Answer

```
┌─────────────────────────────────────────────────────────────┐
│                 List Dilution vs. Focus                     │
│                                                             │
│  "Give me 10 marketing ideas":                              │
│  • 10 generic, 1-sentence bullet points                     │
│  • "Start a blog", "Post on TikTok", "Host a webinar"       │
│  • Zero depth, zero execution steps, total paralysis       │
│                                                             │
│  "Give me the #1 highest-ROI marketing strategy":           │
│  • Deep execution blueprint with step-by-step tactics       │
│  • Complete conversion math, tooling, and risk mitigation   │
│  • Immediate execution readiness                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Master "One Best Answer" Prompt Templates

### Pattern 1: The High-Conviction Executive Directive
Use this for business decisions, marketing, and strategic growth:

```markdown
I want to achieve [SPECIFIC GOAL] within [TIMEFRAME] with [RESOURCES / BUDGET].

Do NOT give me a list of 10 generic options.
Instead:
1. Identify the **single highest-leverage strategy** that will drive 80% of the results.
2. Defend why this specific strategy beats other alternatives.
3. Provide a step-by-step tactical execution plan for week 1.
4. Highlight the #1 fatal pitfall to avoid.
```

---

### Pattern 2: The Single Root-Cause Fix (Engineering & Debugging)
Use this when troubleshooting complex production issues:

```markdown
Here is the error log and stack trace: [PASTE ERROR].

Do not guess 5 possible reasons. 
Give me the single most statistically probable root cause, the exact line to fix, and the corrected code.
```

---

## Real-World Case Study

### Scenario: Improving SaaS Onboarding Activation

#### The Diluted 10-Item List Prompt
> **User**: *"Give me 10 ideas to improve onboarding conversion for our CRM app."*
>
> ❌ *AI Output*:
> 1. Add a product tour.
> 2. Send welcome emails.
> 3. Add video tooltips.
> 4. Simplify the signup form.
> 5. Offer live chat support... *(8 more shallow ideas that leave the user wondering which one actually moves the needle)*.

#### The High-Conviction "One Best" Prompt & Result
> **User**: *"What is the single most critical onboarding change that drives retention in B2B SaaS?"*

**AI Response**:
> **The #1 Lever: The "Empty-State Quick-Start Template" (Fast Time-to-Value)**
>
> **The Defense**: 70% of churn during SaaS onboarding occurs because users face a blank screen and don't know what data to enter. Providing a pre-populated workspace with 1-click sample data reduces Time-to-Value (TTV) from 18 minutes to under 45 seconds.
>
> **Execution Blueprint**:
> 1. **Immediate Action**: Add a modal on first login: *"Load demo data with 5 sample deals (Recommended)"* vs *"Start with blank workspace"*.
> 2. **Metric to Track**: Percentage of new signups who interact with a sample deal within 2 minutes of signup.
> 3. **The Fatal Trap to Avoid**: Do not force users through a multi-step unskippable carousel tour.

---

## When to Use "One Best" vs. Lists

| Goal | Optimal Prompt Approach |
| :--- | :--- |
| **Broad Brainstorming & Exploration** | Ask for 5-7 divergent ideas across distinct angles. |
| **Direct Execution & Fast Action** | Ask for the single highest-leverage strategy. |
| **Root-Cause Troubleshooting** | Ask for the #1 statistically probable fix. |
| **Refining Copy / Taglines** | Ask for the 1 best headline with a 2-sentence rationale. |

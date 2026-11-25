---
name: ask-what-info-is-missing
description: "Identify missing inputs and ask targeted questions before resolving an underspecified task."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["context-discovery", "gap-analysis", "interview-pattern", "blind-spots", "clarification", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask What Information Is Missing (AI Skill)

## Overview
By default, when an AI is given an underspecified prompt (e.g., *"How should I price my consulting services?"*), it will rarely pause to say, *"I don't know your industry, target client, or operating costs."* Instead, it **silently fills the gaps with assumptions**, resulting in generic, disconnected advice.

The **Context Gap Discovery Protocol** turns this dynamic upside down: it explicitly commands the AI to identify missing parameters and interview you *before* finalizing its recommendation.

---

## The Context Gap Discovery Loop

```
┌─────────────────────────────────────────────────────────────┐
│                 Context Gap Discovery Loop                  │
│                                                             │
│  User Raw Prompt ──► [ AI Context Diagnostic Check ]        │
│                                │                            │
│                                ▼                            │
│  [ Lists Top 3-5 Missing Variables & Why They Matter ]      │
│                                │                            │
│                                ▼                            │
│  User Answers Gaps ──► [ Tailored, Zero-Assumption Output ] │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Gap Discovery Prompts

### Pattern 1: The "Interview Me First" Pattern
Use this at the beginning of any complex strategy, design, or business task:

```markdown
I want to [INSERT GOAL / PROJECT].

Before giving me advice or solutions:
1. Ask me the **top 3 to 5 questions** you need answered to give a tailored, expert recommendation.
2. For each question, briefly explain *why* that detail changes the outcome.
3. Wait for my answers before writing the final plan.
```

---

### Pattern 2: The "Blind-Spot Audit" (Post-Draft Check)
Use this after receiving an initial draft or plan:

```markdown
Review the advice you just gave.
- What critical information did I omit from my original prompt that could invalidate your recommendations?
- What edge cases or assumptions are you making about my budget, timeline, or tech stack?
```

---

## Real-World Case Study

### Scenario: Setting Up an LLC / Business Entity

#### Weak Direct Prompt (Silent Assumption Trap)
> **User**: *"Should I form an LLC or an S-Corp?"*
>
> ❌ *AI dumps a generic textbook comparison of pass-through taxation without knowing revenue, state, or owner count.*

#### The "Interview Me" Prompt & Result
> **User**: *"I am starting a new business and deciding between an LLC and S-Corp. Ask me the 4 essential questions you need to advise me properly."*

**AI Response**:
> To give you the exact financial and tax comparison, please answer these 4 questions:
> 1. **Expected Net Profit**: What is your projected net profit in Year 1? *(If under $60k-$80k, S-Corp payroll and accounting overhead often outweighs tax savings).*
> 2. **State / Jurisdiction**: Which US state are you operating in? *(States like California levy annual franchise fees and specific S-Corp requirements).*
> 3. **Ownership Structure**: Will you have foreign investors, venture capital, or multiple partners? *(S-Corps have strict limits: max 100 shareholders, all US citizens/residents).*
> 4. **Active vs. Passive Involvement**: Will you be actively working in the business, or is this passive investment?

---

## Key Benefits

| Aspect | Unchecked Prompting | With Missing-Info Discovery |
| :--- | :--- | :--- |
| **Relevance** | 40% generic filler | 100% targeted to your exact constraints |
| **Assumptions** | Hidden & unstated | Explicitly surfaced and answered |
| **Token Waste** | 3-4 back-and-forth correction turns | One diagnostic round $\rightarrow$ Perfect deliverable |

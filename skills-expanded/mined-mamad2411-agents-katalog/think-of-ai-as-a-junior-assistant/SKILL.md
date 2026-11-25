---
name: think-of-ai-as-a-junior-assistant
description: "Delegate a bounded task with context and acceptance criteria, then review the result before relying on it."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["mental-models", "delegation", "quality-control", "management", "productivity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Think of AI as an Eager Junior Intern (The Delegation Model) (AI Skill)

## Overview
Users typically fall into two flawed extremes with AI:
1. **The Oracle Fallacy**: Treating the AI as an infallible genius and blindly trusting every hallucinated number and URL without review.
2. **The Cynic Fallacy**: Dismissing AI as useless because it made one factual error.

The **Eager Junior Intern Mental Model** frames the relationship accurately: imagine you have an exceptionally well-read, lightning-fast intern who has memorized all of Wikipedia and GitHub, but **lacks real-world judgment, common sense, and accountability**.

---

## The Junior Intern Delegation Matrix

```
┌─────────────────────────────────────────────────────────────┐
│                 Junior Intern Management Loop               │
│                                                             │
│  [ WHAT YOU WOULD TELL A JUNIOR INTERN ]:                   │
│  1. Don't guess; ask if you don't know                      │
│  2. Use this exact template and follow these examples       │
│  3. Show me your outline before you write 20 pages          │
│  4. Double-check all math on a calculator before showing me │
│                                                             │
│  ↳ Apply the EXACT same management rules to your AI prompts! │
└─────────────────────────────────────────────────────────────┘
```

---

## The 4 Rules of AI Delegation

### 1. Give an Explicit Rubric (Don't Assume Unstated Context)
A human manager would never tell an intern *"Go do marketing"*; they say: *"Extract the pricing of our top 3 competitors into a spreadsheet by 3 PM"*. Apply the same specificity to prompts.

### 2. Set Up Checkpoints (Progressive Review)
Review outlines and wireframes before letting the intern draft 1,000 words.

### 3. Require Proof of Verification (Show Your Work)
Instruct the model to cite exact source clauses or write Python calculation blocks.

### 4. Retain Senior Sign-Off (The Final QA Gate)
You are the senior manager. You own the final deliverable. You never send work to clients without reading and signing off.

---

## Master Delegation Prompt Template

```markdown
I am assigning you a task as my Junior Research Associate: [DESCRIBE TASK].

Guidelines:
1. Follow this exact format schema: [PASTE TEMPLATE / HEADERS].
2. For every claim, provide the source reference.
3. If you encounter missing data or ambiguity, do NOT guess. Mark as `[UNVERIFIED: Reason]`.
4. Keep the draft concise so I can review it in under 2 minutes.
```

---

## Real-World Comparison

### Scenario: Competitor Pricing Analysis

#### The "Oracle" Mistake (Blind Trust)
> User asks AI for competitor pricing $\rightarrow$ AI invents a plausible but wrong $49/mo plan $\rightarrow$ User presents it to the CEO $\rightarrow$ Client corrects them in the meeting (Reputational damage).

#### The "Junior Intern" Approach (Managed Verification)
> User prompts: *"Find the pricing tiers for [COMPETITOR]. List each tier, its price, and the exact source URL/screenshot date. If pricing is hidden behind an enterprise sales form, explicitly state: 'CUSTOM QUOTE REQUIRED'."* $\rightarrow$ User clicks the 3 URLs in 30 seconds to verify $\rightarrow$ Delivers 100% accurate report to leadership.

---

## Summary Best Practice
> **"Never ask an AI to do something you wouldn't trust a smart, first-week intern to do without your final review."**

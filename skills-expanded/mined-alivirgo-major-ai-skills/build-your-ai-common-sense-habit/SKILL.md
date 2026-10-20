---
name: build-your-ai-common-sense-habit
description: "Build a repeatable prompting habit around clear goals, relevant context, verification, and human review."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["master-system", "habits", "productivity", "best-practices", "mental-models", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Build Your AI Common Sense Habit (The Master Operating System) (AI Skill)

## Overview
Generative AI tools (ChatGPT, Claude, Gemini) are not search engines, and they are not infallible humans - they are high-powered, probabilistic text engines. Treating them like magical minds leads to frustration, while treating them with **structured common sense** turns them into the ultimate personal multiplier.

This guide codifies the **5 Core Habits of High-Leverage AI Operators** into a daily mental checklist.

---

## The 5 Pillars of the AI Common Sense Operating System

```
┌─────────────────────────────────────────────────────────────┐
│                 The AI Common Sense Engine                  │
│                                                             │
│  1. ANCHOR FIRST    ──► Provide role, context & boundaries  │
│           │                                                 │
│  2. BOUND OUTPUT    ──► Set word limits, schemas, or tables │
│           │                                                 │
│  3. VERIFY EXTERNALLY ─► Click URLs, compute math with code │
│           │                                                 │
│  4. PROGRESSIVE FLOW──► Ask BLUF/summary before deep dives  │
│           │                                                 │
│  5. SURGICAL EDITS  ──► Edit only broken lines, keep voice  │
└─────────────────────────────────────────────────────────────┘
```

---

## The 5 Core Daily Habits

### Habit 1: Anchor Before Asking (Context Over Guessing)
- **The Rule**: Never give a naked 1-line command (*"Write an email to Dave"*).
- **The Habit**: Always state the **Role, Audience, Goal, and Banned Words** upfront. 10 seconds of prompt clarity saves 5 minutes of rewriting.

### Habit 2: Enforce Bounded Outputs (Tables & Word Ceilings)
- **The Rule**: Unconstrained AI produces rambling narrative essays.
- **The Habit**: Explicitly demand: *"Respond as a Markdown table with 4 columns"* or *"Keep answer strictly under 100 words"*.

### Habit 3: Externalize Math and URLs (Zero-Trust Grounding)
- **The Rule**: LLMs hallucinate numbers, prices, and links because they predict tokens rather than executing calculations or querying live DNS.
- **The Habit**: Always demand Python scripts for arithmetic and independently click links before sending to clients or stakeholders.

### Habit 4: Progressive Disclosure (BLUF First)
- **The Rule**: Don't read 500 words to find a 1-sentence decision.
- **The Habit**: Require a 2-line Bottom Line Up Front (BLUF) answer first. Only ask for deep dive documentation if the summary warrants it.

### Habit 5: Surgical Spot-Fixing (Preserve Human Voice)
- **The Rule**: Never tell an AI to *"rewrite this entire article"* if only one transition is awkward.
- **The Habit**: Feed only the broken paragraph or sentence to preserve your authentic personality and humor.

---

## The Master Daily System Prompt

Copy this baseline into your ChatGPT / Claude custom instructions or agent system prompt:

```markdown
Operating Baseline:
1. Deliver the Bottom Line Up Front (BLUF) in lines 1-2.
2. Structure comparative answers in clean Markdown tables rather than long paragraphs.
3. For calculations, write and execute Python code or show explicit step-by-step arithmetic scratchpads.
4. When uncertain or when critical information is missing, ask 3 clarifying questions rather than making assumptions.
5. Ban all AI clichés: "delve", "tapestry", "crucial", "testament", "beacon", "in today's fast-paced world".
```

---

## Daily Habit Checklist

| Scenario | Weak Habit | Common Sense Mastery Habit |
| :--- | :--- | :--- |
| **Starting a task** | *"Help me with my project"* | *"Here is my goal, budget, and audience. Ask me 3 questions to get started."* |
| **Reviewing results**| Skimming and trusting math | Running the Python script to verify calculations. |
| **Polishing text** | *"Rewrite this draft to be better"* | *"Rephrase only sentence 2 to sound friendlier; keep the rest unchanged."* |
| **Comparing tools** | *"Which CRM is best?"* | *"Compare HubSpot vs Pipedrive in a 4-column table. Show fatal flaws for both."* |
| **Handling long chats**| Asking 10 separate questions | Batching 4 related sub-questions into a single numbered prompt. |

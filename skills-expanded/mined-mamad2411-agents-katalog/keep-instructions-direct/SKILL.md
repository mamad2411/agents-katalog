---
name: keep-instructions-direct
description: "Write clear action-oriented instructions with a specific task and expected result."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["imperative-prompting", "action-verbs", "clarity", "prompt-engineering", "efficiency", "focus"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Keep Instructions Direct (The Imperative Lead Protocol) (AI Skill)

## Overview
Starting a prompt with polite conversational preambles (*"Hey there! I was wondering if you might have time to possibly help me review..."*) burns initial prompt token weights on meaningless social pleasantries. 

Because Large Language Models attend most heavily to the first tokens of a message, leading with an **Imperative Action Verb** immediately focuses the model's neural attention on the exact cognitive operation required.

---

## Conversational Hesitation vs. Imperative Command

```
┌─────────────────────────────────────────────────────────────┐
│                 Attention Weight Optimization               │
│                                                             │
│  Conversational Hesitation:                                 │
│  "Could you maybe look at this text and see if it's okay?"  │
│  ↳ Diffuse, weak attention on editing rules                 │
│                                                             │
│  Imperative Lead:                                           │
│  "AUDIT this draft for passive voice and cut word count 30%"│
│  ↳ 100% Focused, crisp, deterministic execution             │
└─────────────────────────────────────────────────────────────┘
```

---

## The Power Verb Taxonomy

Replace weak, passive verbs with high-leverage imperative commands:

| Weak / Vague Verb | High-Precision Imperative Verb | Exact Action Triggered in LLM |
| :--- | :--- | :--- |
| *"Look at this"* | **AUDIT** | Evaluates systematically against criteria/rules. |
| *"Make it better"* | **REFACTOR** | Restructures architecture/code without breaking logic. |
| *"Explain this"* | **SYNTHESIZE** | Condenses key points into high-density takeaways. |
| *"Give me ideas"* | **BRAINSTORM [X] ANGLES** | Generates high-contrast divergent options. |
| *"Fix mistakes"* | **REDLINE** | Shows exact deletions and insertions. |
| *"Put together"* | **SCAFFOLD** | Creates structural skeletons and starter templates. |

---

## Real-World Transformations

### Example 1: Code Review
- ❌ **Passive**: *"Can you check this python code and tell me what you think?"*
- ✅ **Imperative**: *"**AUDIT** this Python function for thread safety and memory leaks. Provide the refactored code."*

### Example 2: Market Analysis
- ❌ **Passive**: *"I need some information on the EV market."*
- ✅ **Imperative**: *"**SYNTHESIZE** the top 3 supply chain bottlenecks in the US EV battery market into a 3-column table."*

### Example 3: Copy Editing
- ❌ **Passive**: *"Help me rewrite this email so it sounds nicer."*
- ✅ **Imperative**: *"**REWRITE** this email to sound warm and collaborative. Keep it under 75 words."*

---

## The 3-Word Prompt Opener Formula
Structure the first 3 words of every prompt as:
> **`[IMPERATIVE VERB] + [EXACT TARGET] + [PRIMARY CONSTRAINT]`**
> 
> *Example*: `"**DRAFT** [a 2-paragraph memo] [for executive leadership]..."`
> *Example*: `"**EXTRACT** [all dollar amounts] [into a TSV code block]..."`

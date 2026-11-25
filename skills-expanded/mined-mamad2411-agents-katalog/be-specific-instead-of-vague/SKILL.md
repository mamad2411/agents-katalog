---
name: be-specific-instead-of-vague
description: "Replace vague requests with a concrete goal, relevant context, constraints, and desired output."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["precision", "clarity", "prompt-engineering", "constraints", "specificity", "productivity"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Be Specific Instead of Vague (The Precision Protocol) (AI Skill)

## Overview
The quality of an AI's response is directly proportional to the constraints provided in the prompt. Vague prompts (*"Write a blog post about productivity"*, *"Fix my code"*) trigger the broadest, most generic probability distribution in the LLM, producing bland, predictable text.

The **Precision Protocol** uses the **5-Variable Specificity Formula** to anchor the model to your exact intended context, eliminating 90% of back-and-forth revisions.

---

## The 5-Variable Specificity Formula

```
┌─────────────────────────────────────────────────────────────┐
│                 The 5-Variable Formula                      │
│                                                             │
│  [ ROLE ]     ──► Who is the AI speaking as?                │
│  [ AUDIENCE ] ──► Who is reading / receiving this?          │
│  [ GOAL ]     ──► What exact outcome must be achieved?      │
│  [ BOUNDARY ] ──► Length, format, and banned elements?      │
│  [ CONTEXT ]  ──► Key facts, data points, or constraints?   │
└─────────────────────────────────────────────────────────────┘
```

---

## Real-World Transformations: Vague vs. Specific

### Example 1: Email Request to a Colleague

#### Vague (Low Precision)
> ❌ *"Write an email asking for the sales numbers."*
>
> **Result**: AI writes a 4-paragraph corporate letter starting with *"I hope this email finds you well in these busy times..."*

#### Specific (Precision Formula Applied)
> ✅ *"Write a 2-sentence Slack message to our sales lead (Dave) asking for the updated Q2 EMEA revenue spreadsheet by 3 PM today for the board prep meeting. Friendly but urgent tone."*
>
> **Result**: *"Hey Dave, could you share the updated Q2 EMEA revenue spreadsheet by 3 PM today? Putting the final slides together for tomorrow's board prep."*

---

### Example 2: Code Refactoring

#### Vague
> ❌ *"Make this Python script faster."*
>
> **Result**: AI adds comments, renames variables, or suggests generic multiprocessing libraries that don't fit the workload.

#### Specific
> ✅ *"Refactor this Python 3.12 data processing function to eliminate the $O(N^2)$ nested loop. Use a hash map lookup (`dict`). Keep memory footprint under 50MB and preserve all existing type hints and docstrings."*

---

### Example 3: Marketing Copy

#### Vague
> ❌ *"Give me headline ideas for a fitness app."*
>
> **Result**: *"Get fit today!", "Transform your body!", "Your fitness journey starts now!"*

#### Specific
> ✅ *"Write 5 headline options for a high-intensity kettlebell workout app targeted at busy software engineers who have only 20 minutes a day. Highlight strength and posture improvement. Under 10 words each. No exclamation marks."*
>
> **Result**:
> 1. Fix developer posture in 20 minutes a day
> 2. Build real strength between Zoom meetings
> 3. Zero commute kettlebell training for desk athletes
> 4. 20 minutes of iron to counter 8 hours of sitting
> 5. Heavy kettlebells, zero fluff, done in 20 minutes

---

## Quick-Constraint Injection Table

When you are in a rush, append any 2 of these constraints to instantly sharpen your prompt:

| Constraint Type | Copy-Paste Snippet |
| :--- | :--- |
| **Length Ceiling** | *"Keep response strictly under [50 / 150] words."* |
| **Format Ceiling** | *"Deliver as 3 bullet points with bold key takeaways."* |
| **Audience Anchor**| *"Explain this for a non-technical C-suite executive."* |
| **Negative Boundary**| *"Do not include introductory greetings, filler, or generic disclaimers."* |
| **Actionability** | *"Include exact command-line syntax and file paths only."* |

---
name: give-ai-direct-feedback
description: "Give specific feedback about what is wrong, what should change, and which parts should remain."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["feedback-loops", "prompt-steering", "iteration", "tone-calibration", "productivity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Give AI Direct Prescriptive Feedback (AI Skill)

## Overview
When an AI response doesn't hit the mark, many users respond with vague frustration (*"No, that's not good, try again"* or *"Make it more creative"*). Because the model cannot read your mind, it randomly varies tokens, often worsening the output or abandoning the parts that were already working.

The **Direct Prescriptive Feedback Protocol** teaches users how to steer subsequent conversation turns using the **3-Part Feedback Formula**: validate what worked, isolate the flaw, and provide an explicit structural fix.

---

## Vague Complaint vs. Prescriptive Steering

```
┌─────────────────────────────────────────────────────────────┐
│                 Feedback Loop Comparison                    │
│                                                             │
│  Vague Complaint:                                           │
│  "Make this sound better and less boring."                  │
│  ↳ Model guesses $\rightarrow$ throws in buzzwords and emojis │
│                                                             │
│  Prescriptive Feedback (3-Part Formula):                    │
│  "Keep paragraphs 1 and 2. In paragraph 3, cut the passive  │
│   voice, replace the bullet points with a 3-column table,   │
│   and keep the entire response under 100 words."            │
│  ↳ 100% Deterministic Correction on Next Turn               │
└─────────────────────────────────────────────────────────────┘
```

---

## The 3-Part Feedback Formula

```
┌───────────────────────────────────────────────────────────────────────────┐
│ 1. VALIDATE ANCHOR ──► "Keep Section 1 and the introductory hook..."       │
│ 2. ISOLATE FLAW    ──► "...but Section 2 is too formal and verbose..."    │
│ 3. APPLY FIX       ──► "...rewrite Section 2 in 2 short punchy sentences." │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Master Direct Feedback Prompt Templates

### Pattern 1: The Tone & Cadence Calibrator

```markdown
Your draft is 70% there. Here is the exact feedback:
- **What worked**: The structure and technical points in section 1 are spot-on.
- **What failed**: The tone in the email body is too corporate and apologetic.
- **The Fix**: Rewrite ONLY the email body. Make it confident and conversational, like a senior lead speaking to a peer. Cut out "I hope this finds you well" and "Please let me know if you have any questions".
```

---

### Pattern 2: The Length & Density Compressor

```markdown
Good information, but too long.
- Keep the exact same 4 arguments.
- Compress the total length by 50% (ceiling of 150 words).
- Format each argument as: `**Bold Concept**: 1-sentence explanation`.
```

---

### Pattern 3: The Technical Bug Correction

```markdown
The logic in function `calculate_tax()` is correct, but your implementation uses an in-memory loop that will cause an OOM error on 100k rows.
- Refactor `calculate_tax()` to use a generator or database SQL aggregation instead.
- Preserve all other functions untouched.
```

---

## Real-World Case Study

### Scenario: Polishing a Proposal Pitch

#### Ineffective Vague Feedback
> **User**: *"This proposal sounds too dry. Make it pop."*
> ❌ *AI Output: "🚀 In today's dynamic paradigm, our cutting-edge synergy will unleash unprecedented value! 🔥"*

#### Direct Prescriptive Feedback & Result
> **User**: *"The scope breakdown in Section 2 is great. But Section 1 (The Executive Summary) is 3 paragraphs of fluff. Replace Section 1 with a single 3-sentence paragraph stating the current $40k monthly loss and how our solution cuts it to zero within 60 days."*

**AI Output**:
> **Executive Summary**:
> Your current manual order reconciliation process leaks an average of **$40,000 per month** in unrecovered billing discrepancies and delays month-end closing by 9 days. Our automated ingestion pipeline eliminates manual reconciliation entirely, reconciling 100% of transactions in real time. We project complete payback within 60 days of deployment.

---

## Summary Best Practices
- **Never say "Try again"**: Always explain *what* to change and *what* to keep.
- **Give positive constraints**: Tell the AI what you want to see (*"Use active verbs"*) rather than just what you dislike.
- **Preserve working sections**: Explicitly instruct the AI: *"Do not modify section X"*.

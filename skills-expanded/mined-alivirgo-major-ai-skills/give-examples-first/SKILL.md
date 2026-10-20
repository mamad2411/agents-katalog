---
name: give-examples-first
description: "Provide concrete input and output examples when a task's format or style is difficult to describe abstractly."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["few-shot-prompting", "exemplars", "in-context-learning", "formatting", "accuracy", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Give Examples First (The Few-Shot Exemplar Pattern) (AI Skill)

## Overview
Trying to describe your desired formatting or writing tone using purely abstract adjectives (*"Make it concise, professional, punchy, elegant, but not too stiff"*) leaves vast room for model misinterpretation.

In modern prompt engineering, **one concrete example is worth a thousand adjectives**. 

The **Few-Shot Exemplar Pattern** provides the AI with 1 or 2 pairs of sample inputs and ideal outputs. This instantly aligns the model's token distribution with your exact desired format, tone, and structural rhythm.

---

## Zero-Shot Description vs. Few-Shot Demonstration

```
┌─────────────────────────────────────────────────────────────┐
│                 Zero-Shot vs. Few-Shot Accuracy             │
│                                                             │
│  Zero-Shot Prompt (Adjectives Only):                        │
│  "Extract product names and sentiment in a clean way."      │
│  ↳ 45% format variance, inconsistent schemas, unpredictable │
│                                                             │
│  Few-Shot Prompt (1 Sample Demonstration):                  │
│  "Input: 'Loved the battery, hated the screen'              │
│   Output: { positive: ['battery'], negative: ['screen'] }   │
│   Now process: [NEW_INPUT]"                                 │
│  ↳ 99% Deterministic Adherence to Schema and Style          │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Few-Shot Prompt Templates

### Pattern 1: The Input-Output Exemplar Pair (Data & Extraction)

```markdown
Extract key features from product descriptions. Follow the exact style and schema shown in these examples:

### Example 1
Input: "The UltraBook Pro features a 14-inch OLED display, 32GB RAM, and weighs only 2.1 lbs."
Output:
- **Device**: UltraBook Pro
- **Screen**: 14" OLED
- **Memory**: 32GB RAM
- **Portability**: 2.1 lbs (Ultra-lightweight)

### Example 2
Input: "The HeavyGamer 9000 has an RTX 4090 GPU, 64GB DDR5, liquid cooling, and 8.5 lbs desktop chassis."
Output:
- **Device**: HeavyGamer 9000
- **Graphics**: NVIDIA RTX 4090
- **Memory**: 64GB DDR5
- **Thermal**: Liquid Cooled
- **Portability**: 8.5 lbs (Desktop Replacement)

---
### Now Process This Input:
Input: "[PASTE YOUR REAL TARGET TEXT]"
Output:
```

---

### Pattern 2: The Voice & Tone Mirror Exemplar (Copywriting)

```markdown
I want you to write a customer update email. Match the exact conversational style, humor, and sentence rhythm of this past email I wrote:

<EXAMPLE_OF_MY_WRITING>
"Hey team - quick heads up on the billing glitch from yesterday. The good news: zero customer credit cards were charged twice. The annoying news: about 40 users received duplicate receipt emails. We've patched the webhook queue and sent an apology note to those 40 folks. Back to normal now!"
</EXAMPLE_OF_MY_WRITING>

Now, write an update about [NEW INCIDENT / TOPIC: e.g. 15-minute dashboard outage today] matching that exact voice.
```

---

## Real-World Comparison

### Scenario: Parsing Customer Support Feedback into Structured JSON

#### Without Examples (Zero-Shot Trial-and-Error)
> **Prompt**: *"Extract sentiment, department, and issue from this ticket in JSON."*
> 
> ❌ *Model outputs nested JSON with inconsistent field names (`user_sentiment`, `ticket_dept`, `desc`), making programmatic backend ingestion break.*

#### With 1 Few-Shot Example (100% Schema Reliability)
> **Prompt**:
> *"Format the ticket into JSON matching this exact structure:*
> ```json
> {
>   "sentiment": "NEGATIVE",
>   "category": "BILLING",
>   "root_issue": "Customer charged twice after failed checkout",
>   "urgency": "HIGH"
> }
> ```
> *Now process this ticket: [PASTE TICKET]"*

**AI Output**:
```json
{
  "sentiment": "NEGATIVE",
  "category": "AUTH",
  "root_issue": "Password reset link expired before email delivery",
  "urgency": "MEDIUM"
}
```

---

## Summary Best Practices
1. **1 example is good, 2 is bulletproof**: You rarely need more than 2 examples to lock in an LLM's behavior.
2. **Include boundary/edge-case examples**: If an input might have missing data, show an example of how the output should gracefully handle `null` or `"N/A"`.
3. **Keep examples compact**: Short, clean examples preserve your active token budget while delivering maximum steering power.

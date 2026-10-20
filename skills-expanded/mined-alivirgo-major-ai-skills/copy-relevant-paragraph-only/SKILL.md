---
name: copy-relevant-paragraph-only
description: "Select a relevant document excerpt with enough surrounding context to answer a focused question."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["context-sniping", "token-savings", "attention-optimization", "lost-in-the-middle", "efficiency", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Copy Relevant Paragraph Only (Context Sniping) (AI Skill)

## Overview
When users have a question about a contract, manual, or article, the common reflex is to paste the entire 20-page document. 

However, LLMs suffer from the **"Lost in the Middle" effect** - attention is sharpest at the very beginning and very end of a prompt, but degrades significantly in the middle of giant context dumps. Pasting entire documents also wastes thousands of input tokens and slows down generation speed.

**Context Sniping** is the practice of copying *only* the specific 1 to 3 relevant paragraphs along with a single line of background framing.

---

## Document Dumping vs. Context Sniping

```
┌─────────────────────────────────────────────────────────────┐
│                 Document Dump vs. Context Snipe             │
│                                                             │
│  Document Dump (Pasting 15,000 words):                      │
│  • High input token cost                                    │
│  • Model suffers from "Lost in the Middle" attention loss   │
│  • Higher risk of confusing unrelated clauses               │
│                                                             │
│  Context Snipe (Pasting 250 words):                         │
│  • 98% token savings                                        │
│  • 100% focused attention on the exact target sentence      │
│  • Instant, laser-accurate response                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Context Sniping Prompt Templates

### Pattern 1: The Sniped Clause Audit (Legal / Policy)

```markdown
Context: I am reviewing our SaaS vendor agreement regarding data deletion upon termination.

Here is the exact paragraph from Section 11.2:
"[PASTE ONLY THE 1-2 TARGET PARAGRAPHS]"

Question:
Does the vendor automatically delete our data within 30 days of contract termination, or do we have to submit a written request? Explain based strictly on the text above.
```

---

### Pattern 2: The Sniped Function Refactor (Code)

```markdown
Context: Python 3.12 FastAPI async route handler.

Here is the specific function that is timing out:
```python
[PASTE ONLY THE 20-LINE FUNCTION]
```

Task: Optimize this function to prevent database connection pool starvation. Do not write the rest of the application.
```

---

## Real-World Case Study

### Scenario: Checking an Insurance Policy for Water Damage Coverage

#### The Wasteful Document Dump
> **User**: Pastes 45 pages of a homeowner's insurance policy ($12,000$ tokens) with: *"Am I covered for a burst pipe in the basement?"*
>
> ❌ *Result: AI skims, confuses general "flood" exclusions with internal "plumbing discharge" coverage, and provides an ambiguous, hesitant answer.*

#### The Context Snipe
> **User**: *"Context: Homeowner's insurance policy in New York.
> Here is Section 3.B (Water Damage):
> 'We cover sudden and accidental discharge or overflow of water from within a plumbing, heating, or air conditioning system. We do not cover water damage caused by external surface flooding, tidal water, or sewer backup.'
> 
> Question: My internal bathroom copper pipe burst and flooded the hallway. Is this covered under this clause?"*

**AI Response**:
> **Yes, this is covered.** 
> Section 3.B explicitly covers *"sudden and accidental discharge... from within a plumbing system."* The exclusion applies only to external floods and sewer backups, not internal pipe bursts.

---

## Summary Best Practices
1. **Locate with `Ctrl + F` first**: Search your document for keywords like *"termination"*, *"warranty"*, or *"liability"*.
2. **Copy the target block + 1 surrounding sentence**: Gives the AI just enough context without drowning it in noise.
3. **State the document type upfront**: Always provide 1 line of context (*"This is from our AWS enterprise agreement"*).

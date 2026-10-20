---
name: bullet-point-summary-first
description: "Extract a short action-focused bullet summary from a long document, article, or meeting record."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["summarization", "bullet-points", "executive-summary", "information-density", "reading-speed", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask for Bullet-Point Summary First (The Executive Digest) (AI Skill)

## Overview
Summarizing 30 pages of text or a 45-minute transcript should not produce 5 pages of dense paragraphs. Effective summaries are **decision-oriented digests** that can be consumed and acted upon in under 30 seconds.

This skill outlines the **Executive 3-Bullet Digest Protocol**: prompting patterns that force the AI to distill core meaning into bold, high-information-density bullet points.

---

## Anatomy of a High-Yield Bullet Point

```
┌─────────────────────────────────────────────────────────────┐
│                 High-Yield Bullet Formula                   │
│                                                             │
│  [ BOLD CORE INSIGHT ] + [ HARD METRIC / DATE ] + [ IMPACT ] │
│                                                             │
│  ❌ Weak:  • We talked about the marketing budget.          │
│  ✅ Strong:• Marketing Budget Cut by 15% ($45k) starting    │
│            June 1st, shifting ad spend entirely to LinkedIn.│
└─────────────────────────────────────────────────────────────┘
```

---

## Master Bullet-Digest Prompt Templates

### Pattern 1: The Executive 3-Bullet Gate
Use this for articles, whitepapers, and industry reports:

```markdown
Read the attached text: [PASTE TEXT / DOCUMENT].

Summarize this into EXACTLY 3 high-yield bullet points:
- **Bullet 1 (The Core Problem / Finding)**: What is the single biggest fact discovered? Include numbers.
- **Bullet 2 (The Solution / Strategy)**: What exact action was proposed or taken?
- **Bullet 3 (The Risk / Consequence)**: What is the main blocker, cost, or deadline?

Rules:
- Start each bullet with a **Bold 3-Word Takeaway**.
- Keep each bullet strictly under 25 words.
- No introductory or concluding text.
```

---

### Pattern 2: The Meeting & Conversation Digest
Use this for Zoom/Teams meeting transcripts and Slack threads:

```markdown
Analyze this meeting transcript: [PASTE TRANSCRIPT].

Provide:
1. **Decisions Made (Max 3 bullets)**: What was definitively agreed upon?
2. **Action Items & Owners (Bulleted)**: `[Owner] - [Task] - [Deadline]`
3. **Open Blockers (Max 2 bullets)**: What remains unresolved?
```

---

## Real-World Case Study

### Scenario: Summarizing an Earnings Call Transcript

#### Weak Standard AI Summary (Vague & Fluffy)
> - The company had a strong quarter and revenue grew.
> - Management discussed supply chain challenges in Asia.
> - They plan to invest more in AI and cloud products in the future.
> - Overall outlook remains positive for next year.
> 
> ❌ *(Zero specific numbers, zero operational utility).*

#### High-Yield Executive Digest Output
> - **Q2 Revenue Grew 24% YoY ($4.2B)**: Beat Wall Street consensus by $180M, driven by 45% growth in Enterprise Cloud subscriptions.
> - **Gross Margins Contracted 180 bps (62.4%)**: Caused by expedited air freight and server hardware component shortages in APAC.
> - **FY2025 AI CapEx Increased to $1.2B**: Shifting 30% of legacy R&D budget into dedicated GPU cluster procurement by Q4.

---

## Summary Best Practices

| Rule | Why It Matters |
| :--- | :--- |
| **Enforce a strict count (e.g. 3 or 5)** | Prevents the model from creating 20 shallow bullets. |
| **Demand bold anchor words** | Allows human eye to scan the key concept in 0.5 seconds. |
| **Require numbers & named entities** | Eliminates vague hand-waving (*"some progress was made"*). |
| **Separate Decisions from Discussion** | Focuses strictly on actionable outcomes rather than chatter. |

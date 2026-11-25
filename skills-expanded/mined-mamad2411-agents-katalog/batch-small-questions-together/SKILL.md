---
name: batch-small-questions-together
description: "Group related short questions into one structured request while keeping each answer identifiable."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["batching", "token-efficiency", "cost-saving", "latency-reduction", "prompt-caching", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Batch Small Questions Together (Token Batching) (AI Skill)

## Overview
Every time you send a new message in an ongoing AI conversation, the entire previous chat history is re-sent as input tokens. Sending 5 separate, one-sentence questions sequentially creates **quadratic context accumulation** ($O(N^2)$ token costs), triggering rate limits and wasting time.

**Token Batching** is the practice of combining 3 to 5 related micro-questions into a single structured prompt, receiving a clean, multi-part answer in one fast round-trip.

---

## The Economics of Context Accumulation

```
┌─────────────────────────────────────────────────────────────┐
│                 Sequential vs. Batched Calls                │
│                                                             │
│  Sequential (5 separate messages):                          │
│  Turn 1: Base Context (500 tokens)                          │
│  Turn 2: Base Context + Turn 1 (1,200 tokens)               │
│  Turn 3: Base Context + Turns 1-2 (1,900 tokens)            │
│  Turn 4: Base Context + Turns 1-3 (2,600 tokens)            │
│  Turn 5: Base Context + Turns 1-4 (3,300 tokens)            │
│  Total Tokens Billed: ~9,500 tokens (5 round trips)         │
│                                                             │
│  Batched (1 message with 5 sub-questions):                  │
│  Turn 1: Base Context + 5 Sub-questions (750 tokens)        │
│  Total Tokens Billed: ~1,500 tokens (84% Savings, 1 Trip)   │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Batching Prompt Templates

### Pattern 1: The Numbered Q&A Batch (Research & Fact-Finding)

```markdown
Based on the attached documentation / topic of [TOPIC], answer these 4 specific questions in order:

1. **Prerequisites**: What specific SDK version and runtime is required?
2. **Pricing**: What is the free-tier allowance vs. overage cost per 1k requests?
3. **Authentication**: Does this use OAuth2 Bearer tokens or static API keys?
4. **Rate Limits**: What are the requests-per-minute (RPM) limits for standard accounts?

Format each answer as:
**[Number]. [Topic Name]**: [1-2 concise sentences]
```

---

### Pattern 2: The Multi-Variable Debug Batch (Technical)

```markdown
Review the function below and answer these 3 diagnostic points:
[PASTE FUNCTION]

1. What is the time complexity in Big-O notation?
2. Is there an unhandled null pointer or memory leak?
3. What is the exact one-line fix to make it thread-safe?
```

---

## Real-World Case Study

### Scenario: Reviewing a Freelance Contract

#### Wasteful Sequential Flow (5 Back-and-Forths)
> - *Turn 1*: "What is the payment term in section 3?" $\rightarrow$ AI responds (200 tokens).
> - *Turn 2*: "Is there an intellectual property assignment clause?" $\rightarrow$ AI re-reads entire doc (1,500 tokens).
> - *Turn 3*: "What is the notice period for termination?" $\rightarrow$ AI re-reads entire doc (1,800 tokens).
> - *Turn 4*: "Is there a non-compete clause?" $\rightarrow$ AI re-reads entire doc (2,100 tokens).
>
> ❌ *Total Time: 4 minutes. Total Tokens: ~6,000 tokens.*

#### The Single Batched Audit Prompt & Output
> **User**:
> *"Analyze this contract and answer in 4 bullet points:
> 1. Payment schedule & late penalty terms
> 2. IP ownership assignment timing (upon creation vs. upon full payment)
> 3. Termination notice period required
> 4. Non-compete duration and geographic restrictions"*

**AI Response**:
> 1. **Payment Terms**: Net-30 from invoice date; 1.5% monthly late fee applies after 30 days (Section 3.2).
> 2. **IP Ownership**: IP transfers **only upon full payment received** (Section 5.1 - favorable to freelancer).
> 3. **Termination**: 14 days written notice required by either party without cause (Section 8.3).
> 4. **Non-Compete**: None. Only a standard 1-year client non-solicitation clause (Section 9.2).

*(Completed in 1 turn, 4 seconds total generation time, 1,200 tokens total).*

---

## Best Practices for Batching
- **Keep questions related**: Batch questions that draw from the same source document or context.
- **Number each item**: Numbering ($1, 2, 3$) ensures the model doesn't accidentally skip an item.
- **Set a ceiling of 3-5 items**: Asking 15 questions in one turn can lead to shallow answers or truncation.

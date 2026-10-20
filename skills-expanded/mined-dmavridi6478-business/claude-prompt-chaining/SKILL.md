---
name: claude-prompt-chaining
description: Claude Mastery — Prompt Chaining. Break complex tasks into 5 sequential stages (Research → Analyze → Create → Review → Refine) with zero-drift execution rules. One giant prompt gives one shallow answer; a prompt chain gives a repeatable, high-quality workflow. Source 51ultron.com, Claude Mastery Series Day 9.
---

## The core principle

> One prompt is a question. A prompt chain is a repeatable operating system.

The biggest mistake: making Claude do everything in one giant prompt. The result is a giant answer — shallow, messy, and incomplete.

**Break the task. Build the chain.**

---

## The 5 Stages

### Stage 1 — Research

Give Claude the problem. Ask it to gather relevant information only — no analysis yet.

**Prompt template:**
```
Research the latest trends, data and best practices about [TOPIC].
Provide key information with sources.
```

---

### Stage 2 — Analyze

Feed Stage 1 output back in. Ask for patterns, not content.

**Prompt template:**
```
Analyze the research above. Find key patterns, insights, gaps and actionable opportunities.
```

---

### Stage 3 — Create

Feed Stage 2 output. Now ask for the actual deliverable.

**Prompt template:**
```
Using the analysis, create a detailed [OUTPUT TYPE] for [AUDIENCE].
Keep it clear, structured and practical.
```

---

### Stage 4 — Review

Ask Claude to critique its own Stage 3 output against specific criteria.

**Prompt template:**
```
Review the output above. Evaluate it for accuracy, depth, clarity and missing points.
Suggest improvements.
```

---

### Stage 5 — Refine

Feed the Stage 4 critique. Produce the final version.

**Prompt template:**
```
Refine the output based on the review. Produce the final version with all improvements included.
```

---

## The Master Chain Prompt

Use this to kick off the full 5-stage sequence in a single conversation:

```
I want to complete [TASK].
Don't solve everything at once.
Break the task into these stages:
1. Research  2. Analyze  3. Create  4. Review  5. Refine

Complete each stage carefully and use the output from one stage as context for the next.
Before moving to the next stage, identify anything important that is missing or uncertain.
```

---

## The 4 Chaining Rules (Zero Drift · 10× Consistency)

**Rule 01 — Clean Isolation** *(State Reset)*
Pass only stage outputs, never bloated chat history. Each stage gets its predecessor's output — nothing else.

**Rule 02 — Output Schema** *(Structured)*
End each step with: `"Format strictly as: [Markdown/JSON]"`. Forces consistent structure across the chain.

**Rule 03 — Vet Stage 2** *(Audit Gate)*
Audit the Analysis before running Creation. If the analysis has bad logic, the creation will too. Stop it early.

**Rule 04 — Gold Standard** *(Anchor)*
Feed 1 top-tier example into Stage 3 to anchor tone and depth. The example sets the quality floor.

---

## Why chaining beats single prompting

| Single prompt | Prompt chain |
|--------------|-------------|
| One pass, one output | Iterative, staged outputs |
| Errors compound silently | Errors caught at each gate |
| Generic, shallow | Specific, deep |
| Hard to repeat | Repeatable workflow |
| One giant answer | Progressively refined result |

---

## Example: Content Marketing Article

```
Stage 1: Research the latest trends in [INDUSTRY] content marketing. Provide data and examples.

Stage 2: Analyze the research above. Find gaps competitors aren't covering and opportunities.
Format strictly as: Markdown bullet list.

Stage 3: Using the analysis, write a 1,200-word article for [AUDIENCE].
[Insert 1 excellent article example here to anchor quality.]
Format strictly as: Markdown with H2 headers.

Stage 4: Review the article above for accuracy, depth, clarity and missing points. Suggest improvements.
Format strictly as: Numbered list of suggestions.

Stage 5: Refine the article based on the review. Return the final version only.
```

---

## Quick reference card

```
[TASK] → Stage 1 (Research) → Stage 2 (Analyze) → GATE: audit logic → Stage 3 (Create + gold example) → Stage 4 (Review) → Stage 5 (Refine) → DONE
```

**Core principle:** Break · Build · Refine

---

## Related skills

- `claude-thinking-partner` — use before Stage 1 to sharpen the task definition
- `ceo-daily-brief` — apply prompt chaining to the CEO Brief's Step 6 (Draft Responses)
- `build-claude-agent-7-steps` — automate the chain with a Claude agent loop

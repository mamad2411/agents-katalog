---
name: token-optimizer
description: >
  Maximize Claude's output quality while minimizing input token usage. Use this skill
  whenever a user wants to compress prompts, reduce token consumption, extract maximum
  output from Claude, write high-density instructions, optimize system prompts, or improve
  AI communication efficiency. Trigger on phrases like "optimize my prompt", "too many tokens",
  "make this shorter but better", "get more from Claude", "compress this prompt",
  "write a better system prompt", "token efficient", or any request to improve how
  someone communicates with Claude or any LLM. Also trigger when building AI-powered
  tools, chatbots, agents, or any system where prompt cost or quality matters.
---

# Token Optimizer — Maximum Output, Minimum Input

A skill for extracting the highest-quality, most complete responses from Claude using
the fewest possible input tokens. Every technique here is tested, practical, and immediately
applicable.

---

## Core Philosophy

> **Information Density > Verbosity**
> Claude processes meaning, not words. A 40-token instruction that is precise always
> beats a 200-token instruction that is vague.

The goal is not to "trick" Claude — it is to communicate with maximum clarity and
minimum redundancy so Claude spends its compute on output, not parsing.

---

## The 5 Pillars of Token Optimization

### Pillar 1 — Prompt Compression

Strip all filler. Every word must earn its place.

**Before (47 tokens):**
```
Could you please analyze the following code and let me know what might be wrong
with it and also suggest how I could fix the issues you find?
```

**After (9 tokens):**
```
debug+fix: [code]
```

**Compression patterns:**

| Verbose Phrase | Compressed Form |
|---|---|
| "Please analyze and explain" | `analyze:` |
| "Write a detailed explanation of" | `explain:` |
| "Can you help me understand" | `clarify:` |
| "Please review and improve" | `refine:` |
| "Give me a step by step guide" | `steps:` |
| "Summarize the key points of" | `summarize:` |
| "Compare X and Y in detail" | `compare: X vs Y` |
| "Generate multiple options for" | `options(5):` |

Read `references/compression-patterns.md` for 50+ compression shortcuts across categories.

---

### Pillar 2 — Output Format Control

Unstructured output is the #1 source of wasted tokens in responses. Explicit format
instructions cut response bloat by 30–50%.

**Always specify:**
- Format type: `respond in: bullet points / table / JSON / numbered list / prose`
- Length: `max: 200 words` or `max: 5 bullets`
- Restrictions: `no intro sentence. no conclusion. no rephrasing my question.`

**Anti-filler instruction (add to any prompt):**
```
Rules: no preamble, no "Great question!", no restating my prompt, no filler conclusions.
Start directly with the answer.
```

**Power combo — role + format + constraint in one line:**
```
You are [role]. Rules: [constraint 1], [constraint 2]. Format: [output format].
```

Example:
```
You are a senior Python engineer. Rules: no explanations unless asked, production-ready
code only, include error handling. Format: code block only.
```

Read `references/output-formats.md` for format templates by use case.

---

### Pillar 3 — XML Tag Structuring

XML tags are the single most underused technique in prompt engineering. They reduce
ambiguity, eliminate clarification rounds, and let Claude parse intent faster.

**Basic structure:**
```xml
<context>What Claude needs to know</context>
<task>What Claude must do</task>
<constraints>What Claude must NOT do</constraints>
<format>How the output should look</format>
```

**Why this saves tokens:**
- Removes the need for transition sentences ("Given the above, please now...")
- Eliminates 2–3 clarification exchanges per session
- One well-structured prompt replaces a 5-message back-and-forth

**Advanced: State injection for agents**
```xml
<session_state>
  user_goal: [goal]
  completed: [steps done]
  pending: [next step]
  constraints: [rules still active]
</session_state>
<task>Continue from pending step only. Do not repeat completed steps.</task>
```

---

### Pillar 4 — Instruction Density

Bundle multiple tasks into a single, structured prompt instead of sending separate messages.

**Instead of 4 messages:**
```
Message 1: Explain X
Message 2: Now give me an example
Message 3: Now make it simpler
Message 4: Now summarize
```

**One dense prompt:**
```
For X:
1. explain (2 sentences max)
2. one concrete example
3. ELI5 version
4. one-line summary
Deliver all 4 in order. No filler between sections.
```

**Task chaining syntax:**
```
Step 1 → [task A] → output feeds Step 2 → [task B] → final output: [format]
```

---

### Pillar 5 — Negative Space Instructions

Tell Claude exactly what NOT to do. This is as important as telling it what to do.

**Standard negative block (copy-paste ready):**
```
Do NOT:
- Repeat or rephrase my question
- Add an introduction or conclusion paragraph
- Use phrases like "Certainly!", "Great!", "Of course!", "Sure!"
- Ask clarifying questions unless the task is impossible without them
- Add disclaimers unless specifically relevant
- Pad the response to seem thorough
```

**Aggressive compression mode:**
```
Respond in the minimum tokens possible. Zero filler. Direct answers only.
```

---

## One-Shot Example Pattern

Include one perfect input→output example inside your prompt. This is the fastest
way to align Claude's output style without lengthy instructions.

**Template:**
```
Task: [description]

Example:
Input: [sample input]
Output: [exact output style you want]

Now do the same for:
Input: [your actual input]
```

This technique works because Claude pattern-matches on the example. One well-chosen
example replaces 100 tokens of style instructions.

Read `references/one-shot-examples.md` for ready-made examples across 10 domains.

---

## Context Management for Long Conversations

Claude has no memory between API calls. In long conversations, token costs compound.

**Conversation pruning rules:**
1. Keep only the last N exchanges that are directly relevant to current task
2. Replace long assistant responses with a one-line summary in history
3. Never carry pleasantries, confirmations, or filler in chat history
4. Use a "state summary" message instead of full history:

```
[CONTEXT SUMMARY]
Task: building an e-commerce site
Done: homepage, product listing, cart
Current: checkout form
Stack: HTML/CSS/JS, no frameworks
Rules: mobile-first, WhatsApp order routing
[END CONTEXT]
```

This replaces 2,000+ tokens of history with ~60 tokens of state.

---

## System Prompt Templates

Read `references/system-prompt-templates.md` for 10 production-ready system prompts
optimized for:
- Code assistant
- Content writer
- Data analyst
- Customer support bot
- Research assistant
- Summarization engine
- Translation service
- Creative writing
- Teaching / tutoring
- Business automation

Each template is under 200 tokens and follows all 5 pillars.

---

## Token Savings Reference

| Technique | Avg Token Savings |
|---|---|
| Prompt compression | 40–70% input reduction |
| Output format control | 30–50% output reduction |
| XML structuring | Eliminates 2–3 clarification rounds |
| Instruction bundling | 60–80% fewer messages needed |
| Negative instructions | 20–35% shorter responses |
| One-shot examples | Replaces ~100 tokens of style description |
| Context pruning | 70–90% history token reduction |

**Combined effect:** A fully optimized session uses 3–8x fewer tokens than an
unoptimized session for the same output quality.

---

## Quick Reference Card

For the fastest results, apply this formula to any prompt:

```
[ROLE (1 line)] + [TASK (compressed)] + [FORMAT (explicit)] + [CONSTRAINTS (negative)]
```

Example:
```
You are a copywriter. Write 3 email subject lines for a SaaS product launch.
Format: numbered list. No explanations. Max 10 words each. Punchy and curiosity-driven.
```

That is 34 tokens. Without optimization, this same request often arrives as 120+ tokens
with the same output quality.

---

## Files in This Skill

| File | Purpose |
|---|---|
| `SKILL.md` | This file — core techniques |
| `references/compression-patterns.md` | 50+ shorthand compression patterns by category |
| `references/output-formats.md` | Format templates for every output type |
| `references/system-prompt-templates.md` | 10 production-ready system prompts |
| `references/one-shot-examples.md` | Ready-made examples for 10 domains |
| `references/context-management.md` | Deep guide on conversation state and history pruning |
| `examples/before-after.md` | 20 real before/after prompt comparisons with token counts |

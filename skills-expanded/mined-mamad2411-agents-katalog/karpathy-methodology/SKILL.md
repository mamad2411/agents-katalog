---
name: karpathy-methodology
description: 'Apply Andrej Karpathy AI methodology and principles from his 2023-2026 insights. Use this skill when the user wants to apply Karpathy-style thinking, needs guidance on agentic engineering, LLM knowledge bases, minimalist coding, understanding-first principles, or any of the 14 core methodologies distilled from his work. Also triggers on: "karpathy method", "karpathy approach", "karpathy way", "AK style", "like karpathy does", "karpathy principles", or when user asks how Karpathy would approach any programming or AI problem.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-agentic-engineering
  - karpathy-llm-simulator
  - karpathy-llm-wiki
  - karpathy-autoresearch
  - karpathy-meta-reflection
---

# Karpathy Methodology — 14 Core Skills

> Distilled from Andrej Karpathy's most-liked posts on X (2023–2026), his LLM Wiki Gist, and the multica-ai/andrej-karpathy-skills repo.
> Source: https://x.com/karpathy | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

This skill is the **master index**. When invoked, either:
1. Apply the specific sub-methodology relevant to the user's current task, or
2. Guide the user to the right one from the 14 below.

---

## The 14 Methodologies

| # | Skill Name | One-line Essence |
|---|-----------|-----------------|
| 1 | `karpathy-agentic-engineering` | Orchestrate agents with clear tasks and verifiable success criteria |
| 2 | `karpathy-llm-wiki` | Let LLM maintain your knowledge base; you do the exploring |
| 3 | `karpathy-llm-simulator` | Ask LLM to simulate expert debate, not give one opinion |
| 4 | `karpathy-minimalism` | 200 lines of pure Python beats 50 npm packages |
| 5 | `karpathy-vibe-to-agentic` | Vibe coding raises the floor; agentic engineering raises the ceiling |
| 6 | `karpathy-autoresearch` | Agent loops on git branches; you only change the prompt |
| 7 | `karpathy-output-evolution` | Text → Markdown → HTML → rendered; always demand structure |
| 8 | `karpathy-understanding-first` | Outsource thinking, never understanding |
| 9 | `karpathy-idea-files` | Ship the Gist (abstract + criteria), not the code |
| 10 | `karpathy-meta-reflection` | Monthly audit: what's atrophying, what's exploding |
| 11 | `karpathy-supply-chain-hygiene` | Every dependency is an attack surface |
| 12 | `karpathy-education-first` | Make everything teachable; nano-projects over monoliths |
| 13 | `karpathy-system-prompt-learning` | Write strategy into the system prompt like a textbook |
| 14 | `karpathy-practice-environments` | Build gyms where agents can try, fail, and learn |

---

## Meta-Principle (the one that unifies all 14)

> "You can outsource your thinking but you cannot outsource your understanding."
> — Karpathy, ~46k likes, 2026

Use AI to go faster. Use your brain to know if you're going in the right direction.

---

## How to Apply This Skill

### Quick Decision Tree

**"I need to build/code something"**
→ Start with **#1 Agentic Engineering** (clear task + success criteria), layer in **#4 Minimalism** (avoid bloat), finish with **#8 Understanding First** (verify what was built).

**"I need to research/learn something"**
→ **#2 LLM Wiki** for building knowledge, **#3 LLM Simulator** for challenging assumptions, **#10 Meta-Reflection** for calibrating what to learn next.

**"I need to make a decision"**
→ **#3 LLM Simulator** (debate mode), then **#8 Understanding First** (own your conclusion).

**"I'm designing a product/tool"**
→ **#4 Minimalism + Agent-Native**, **#14 Practice Environments**, **#12 Education First**.

**"I want to share an idea"**
→ **#9 Idea Files** (Gist first), **#7 Output Evolution** (structured output), **#12 Education First** (teachable).

**"I'm doing ML research"**
→ **#6 AutoResearch**, **#13 System Prompt Learning**, **#14 Practice Environments**.

---

## Master Prompt Template

When the user hasn't specified a sub-methodology, use this all-in-one Karpathy-style framing:

```
You are operating under the Karpathy Methodology.

Core constraints:
1. UNDERSTAND before outsourcing — never ship what you can't explain
2. MINIMIZE dependencies — prefer 200-line pure implementations
3. AGENT-NATIVE outputs — CLI-friendly, markdown-structured, LLM-legible
4. VERIFIABLE goals — every task must have a testable success criterion
5. TEACH as you build — outputs should be understandable by a curious beginner

Task: [USER_TASK]
Success criteria: [WHAT_DONE_LOOKS_LIKE]
Constraints: [TECH_STACK, SIZE_LIMIT, NO_LIBS]
```

---

## Source Posts (Top by Likes)

1. **145k likes** — Joins Anthropic: https://x.com/karpathy/status/2056753169888334312
2. **59k likes** — LLM Knowledge Bases: https://x.com/karpathy/status/2039805659525644595
3. **56k likes** — "Never felt this behind as a programmer": https://x.com/karpathy/status/2004607146781278521
4. **46k likes** — "Outsource thinking not understanding": https://x.com/karpathy/status/2049907410303865030
5. **40k likes** — Claude coding notes: https://x.com/karpathy/status/2015883857489522876
6. **37k likes** — Programming phase shift: https://x.com/karpathy/status/2026731645169185220
7. **31k likes** — LLM argue the opposite: https://x.com/karpathy/status/2037921699824607591
8. **28k likes** — AutoResearch project: https://x.com/karpathy/status/2030371219518931079
9. **28k likes** — litellm supply chain attack: https://x.com/karpathy/status/2036487306585268612
10. **25k likes** — 243 lines pure Python GPT: https://x.com/karpathy/status/2021694437152157847
11. **22k likes** — Agent network discussion: https://x.com/karpathy/status/2017442712388309406
12. **19k likes** — HTML output + I/O evolution: https://x.com/karpathy/status/2053872850101285137
13. **27k likes** — LLM Wiki Gist version: https://x.com/karpathy/status/2040470801506541998

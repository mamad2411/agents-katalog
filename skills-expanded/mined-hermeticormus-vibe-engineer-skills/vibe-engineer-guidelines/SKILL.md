---
name: vibe-engineer-guidelines
description: Behavioral guidelines for directing AI codegen well — hypothesis before help, scoped prompts, validate before accepting, reject working-but-wrong, AI output is a draft. Use when working with Claude Code or any AI coding tool. The companion to Karpathy guidelines.
license: MIT
---

# Vibe Engineer Guidelines

Behavioral guidelines for the human directing AI codegen. Companion to the [Karpathy guidelines](https://github.com/HermeticOrmus/andrej-karpathy-skills).

**Tradeoff**: bias toward verification over velocity. For trivial tasks, use judgment.

## 1. Hypothesis before help

Form a hypothesis about the bug's shape BEFORE asking the AI to fix it.

- Trace data flow yourself first.
- State your hypothesis even if uncertain.
- A sharp hypothesis produces a sharp diagnosis.

## 2. Scoped prompts

File paths, line numbers, variable names, specific symptoms. Never "fix this."

Scope reduces hallucination surface.

## 3. Validate before accepting

For every AI-proposed diff, ask three questions:

1. Does it over-engineer?
2. Does it miss an edge case?
3. Does it match the root cause I identified?

## 4. Reject working-but-wrong

Solutions that pass tests by obscuring the bug are worse than no solution. Try/catch swallowing, defensive masking, renamed symptoms, mocked dependencies — reject and iterate.

## 5. AI output is a draft, not a verdict

Read the diff before staging. Run it, then read what it did. Mismatch is data.

---

See full content at https://github.com/HermeticOrmus/vibe-engineer-skills.

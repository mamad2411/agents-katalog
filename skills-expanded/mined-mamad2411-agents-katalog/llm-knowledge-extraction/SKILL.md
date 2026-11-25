---
name: llm-knowledge-extraction
description: Use when answering questions based on internal model knowledge without external tools, or when you need to maximize the quality of reasoning from the LLM's parametric knowledge. Use when the user asks for conceptual explanations, design patterns, or analysis where web search may not help.
---

# LLM Knowledge Extraction

## Overview

Techniques to elicit high-quality, structured, and accurate information from the LLM's internal (parametric) knowledge. Core principle: **the model knows more than it naturally outputs** — use structured prompting and reasoning techniques to extract it reliably.

## When to Use

- Answering conceptual or theoretical questions where you have high confidence in internal knowledge
- Explaining design patterns, algorithms, or architectural trade-offs
- Brainstorming approaches or generating hypotheses
- Synthesizing information you already have into structured formats
- User explicitly asks for your analysis/opinion without external search

**When NOT to use:** Factual claims about specific versions, current events, or empirical results — these require external verification via web-research-intelligence.

## Elicitation Techniques

### Chain-of-Thought (CoT)

Explicitly prompt the model to reason step by step.

**Basic:**
```
Let's think step by step.
```

**Structured:**
```
Before answering, reason through this in three steps:
1. What are the key concepts involved?
2. What are the trade-offs between approaches?
3. What is the most appropriate recommendation and why?
```

**When to use:** Complex reasoning, multi-step problems, or when the answer has non-obvious nuance.

### Self-Ask

Have the model generate and answer follow-up questions before the final answer.

```
To answer this thoroughly, first identify 2-3 sub-questions that need to be resolved.
Answer each sub-question.
Then provide the final answer based on those resolutions.
```

**When to use:** Ambiguous questions, questions with hidden assumptions, or topics with multiple valid interpretations.

### Step-by-Step Verification

Before finalizing, verify your own reasoning.

```
Propose an answer, then critique it:
- What could be wrong with this answer?
- What edge cases did I miss?
- What would someone who disagrees say?
Revise the answer based on this critique.
```

**When to use:** High-stakes recommendations, architectural decisions, or when you suspect your first answer might be incomplete.

### Contrastive Reasoning

Explore alternatives explicitly.

```
What are 2-3 alternative approaches?
For each, what are the main pros and cons?
Why is the recommended approach better than the alternatives?
```

**When to use:** Recommendation questions ("should I use X or Y?"), tool selection, or design decisions.

## Structured Output

Force structured generation to improve coherence and completeness.

### JSON Schema Prompting

```
Respond in this JSON format:
{
  "concepts": ["list of key concepts"],
  "trade_offs": [
    {"approach": "name", "pros": ["..."], "cons": ["..."]}
  ],
  "recommendation": "...",
  "caveats": ["..."]
}
```

### XML Tag Delimiters

```
<analysis>
  [step-by-step reasoning]
</analysis>
<answer>
  [final concise answer]
</answer>
```

**Benefits:** Separates reasoning from output, makes it easier to verify completeness, reduces rambling.

## Confidence Calibration

### Express Uncertainty Explicitly

When knowledge is incomplete or uncertain:

```
I'm confident about: [specific claims]
I'm uncertain about: [areas where the answer might vary]
This depends on: [context that would change the answer]
```

**Rule:** Never state uncertain information as fact. Use qualifiers: "typically", "in most cases", "unless...", "depending on..."

### Knowledge Boundary Check

Before answering, ask yourself:

1. Is this in my training data? (pre-cutoff knowledge)
2. Is this a rapidly changing field where my knowledge may be stale?
3. Is this a specific empirical claim (version number, benchmark result) that I might hallucinate?

If #2 or #3: **flag as uncertain** or suggest verifying with web-research-intelligence.

## Anti-Hallucination Techniques

### Defensive Prompting

```
Base your answer only on established principles and patterns.
If you're unsure about a specific detail, say so rather than guessing.
```

### First Principles Reasoning

When explaining technical concepts, derive from fundamentals:

```
Start from first principles:
- What problem does this solve?
- What are the invariant constraints?
- What are the logically necessary trade-offs?
```

This reduces reliance on memorized (and potentially incorrect) specifics.

### Analogical Reasoning

Use analogies to anchor explanations in well-understood concepts:

```
Explain [complex topic] by analogy to [familiar concept].
Where does the analogy break down?
```

## Temperature & Sampling Strategy

| Goal | Temperature | Reasoning |
|------|-------------|-----------|
| Factual explanation | 0.1 - 0.3 | Minimize creativity, maximize accuracy |
| Brainstorming alternatives | 0.5 - 0.7 | Explore diverse approaches |
| Generating hypotheses | 0.7 - 0.9 | Creative exploration |
| Step-by-step reasoning | 0.2 - 0.4 | Consistent, deterministic logic |

**Note:** Temperature control depends on the platform's capabilities. When not controllable, use explicit instructions instead.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Answering from vague memory | Use Self-Ask to surface specifics |
| Stating uncertain info as fact | Use confidence calibration qualifiers |
| Over-explaining without structure | Use structured output (JSON/XML tags) |
| Ignoring edge cases | Use Step-by-Step Verification |
| Presenting one view as the only view | Use Contrastive Reasoning |
| Hallucinating version numbers or benchmarks | Flag as uncertain; suggest external verification |

## Red Flags — STOP and Verify Externally

- You're about to state a specific version number, date, or benchmark result from memory
- The topic changed significantly after your knowledge cutoff
- You're recommending a specific library without knowing its current maintenance status
- The user is making a high-stakes decision (production architecture, security) based on your answer
- You feel "pretty sure" but can't trace the reasoning chain

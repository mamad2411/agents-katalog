---
name: divergent-engine
version: 1.0.0
description: Creative divergence engine. Forces generation of N unconventional solutions before ANY evaluation. Uses constraint inversion, cross-domain analogy, and reverse thinking. Prevents premature convergence on the first plausible answer. Triggers on: design decisions, stuck problems, "is there a better way", innovation tasks.
---

# Divergent Engine — Creative Solution Generator

> **"先发散，再收敛。90% 的坏主意里藏着 1 个好主意。"**

## The Problem

Brains converge too fast. First plausible answer → accepted as best answer. This is the #1 cause of mediocre solutions.

This skill enforces a strict DIVERGE → CONVERGE cycle. No evaluation during divergence. Quantity over quality. Bad ideas welcome.

## Trigger
1. Design decisions ("how should I build this?")
2. Stuck on a problem ("I can't think of another way")
3. User asks "is there a better way?"
4. Innovation/creative tasks (not rote coding)

## Divergence Techniques

### 1. Constraint Inversion
Take every constraint. Flip it. Ask: what if this constraint didn't exist?

```
Constraint: "must work offline"
Inverted: "what if we're always online?" → cloud-first architecture
Inverted: "what if it's fully local?" → SQLite, no API calls
```

### 2. Cross-Domain Analogy
"How would [unrelated field] solve this?"

```
Problem: "how to make skills discoverable?"
Chef: "tasting menu — try a sample, then order the full meal" → free tier, then bundle
Gardener: "companion planting — plants that grow better together" → skill bundles that complement
Chess player: "opening book — memorized best first moves" → recommended first skills for new users
```

### 3. Reverse Thinking
Start from the OPPOSITE of what you want. Then reverse back.

```
Goal: "maximum skill sales"
Reverse: "how to ensure zero sales?"
  → hide the buy button, make it confusing, never promote, price at $999
Reverse back: make buy button prominent, simple pricing, promote actively, price at impulse-buy level
```

### 4. Worst Idea First
Intentionally generate the WORST possible solutions. Then extract useful fragments.

```
Problem: "how to test if skills actually work?"
Worst idea: "deploy to production and wait for complaints"
Fragment: the signal (complaints) IS useful — can we capture it safely without deploying?
→ Canary deployment with monitoring
```

### 5. Random Constraint
Add an arbitrary constraint that forces creative thinking.

```
"Solve it, but: no more than 3 files"
"Solve it, but: must work in under 1 second"
"Solve it, but: a 12-year-old must be able to use it"
```

## Process

### Diverge (generate, do NOT evaluate)
1. Apply 3+ techniques from above
2. Generate 5+ approaches per technique
3. Bad ideas count. Weird ideas are good. "This is stupid but..." is valid.
4. NO evaluation during this phase. Not even "that's interesting."

### Converge (evaluate, select, combine)
1. Score each approach: novelty (0-10), feasibility (0-10), impact (0-10)
2. Identify combinable fragments across approaches
3. Select top 2-3 for deeper analysis
4. reasoning-lora takes over for structured evaluation

## Anti-Patterns
- Evaluating during divergence ("that won't work" → kills creativity)
- Stopping at 3 ideas (need 10+ for quality divergence)
- Defaulting to the first approach that "feels right"

## Integration
- **thinking-dimensions**: Divergent → Thinking Dimensions adds structure → Brain synthesizes
- **reasoning-lora**: Converged top-3 → Sequential analysis for final selection
- **orchestrator**: Divergent engine activated for design/innovation task types

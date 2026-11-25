---
name: brainstorming
description: "Collaborative ideation for PM work — features, experiments, strategies, solutions. Use when doing creative work, exploring options, or turning a vague idea into a concrete plan."
---

# Brainstorming

Turn vague ideas into concrete, well-formed plans through structured collaborative dialogue. This skill applies to any creative PM work: feature ideation, experiment design, strategy formation, or solution exploration.

## When to Use

- "brainstorm ideas for..."
- "help me think through..."
- "I have an idea but it's not fully formed"
- "explore options for..."
- "what should we build for..."
- Before starting a PRD, experiment, or new initiative

## Process

### Phase 1: Understand the Problem

Ask one question at a time to understand:

1. **What's the context?** — Product area, current state, what prompted this
2. **Who's the customer?** — Reference `knowledge/products/<product>/brief.md` and `knowledge/_template/customer-segments.md` if present
3. **What's the problem?** — Frame as: I am... I am trying to... But... Because... Which makes me feel...
4. **What does success look like?** — Metric, outcome, or state change
5. **What are the constraints?** — Timeline, resources, technical limitations, regulatory

### Phase 2: Explore Approaches

1. Generate 3 options ranging from conservative to ambitious
2. For each option, assess:
   - **Customer impact** — How much does this move the needle for the persona?
   - **Effort** — Engineering, design, ops complexity
   - **Risk** — What could go wrong? Reversible or irreversible?
   - **Strategic fit** — Does it ladder to a pillar in `knowledge/products/<product>/strategy.md`?
3. Present a recommendation with reasoning

### Phase 3: Sharpen the Idea

1. Pressure-test the recommended approach:
   - What's the hypothesis? ("We believe [action] will [outcome] for [segment] because [rationale]")
   - What's the simplest version we could ship to learn?
   - What would make us kill this idea?
2. Define next steps: PRD, experiment, one-pager, or prototype

## Output

A brainstorm summary:

- **Problem** (customer problem framework)
- **Options explored** (3, with trade-offs)
- **Recommendation** (with rationale)
- **Hypothesis** (testable)
- **Next step** (what to do now — and which skill to use: prd-writer, experiment-designer, one-pager)

## Principles

- **One question at a time** — don't overwhelm
- **Multiple choice when possible** — easier to react to options than generate from scratch
- **YAGNI** — cut unnecessary scope ruthlessly
- **Bias toward experiments** — if unsure, design an experiment, don't debate
- **Customer first** — always ground in a real persona and real problem

## Knowledge References

- `knowledge/products/<product>/brief.md` — current product state
- `knowledge/_template/customer-segments.md` — org personas, if filled
- `knowledge/_template/metrics-and-targets.md` — org metrics, if filled

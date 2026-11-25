---
name: learn
description: "Learn and understand a concept in depth. Args: <concept>"
argument-hint: "<concept>"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`<concept>`

- Required. The concept, term, or technology you want explained in depth.
- **Examples**: `/learn user story`, `/learn Wilson score interval`, `/learn closure in JavaScript`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

# Explain Concept: $ARGUMENTS

Explain a software development concept, algorithm, tool, or architectural pattern clearly and thoroughly across multiple conceptual depths.

## Step 1: Validate Input

If `$ARGUMENTS` is empty, missing, or whitespace, stop and output:

> Usage: `/learn <concept>`
> Please provide the concept, term, or technology you want explained.

Then stop.

## Step 2: Adaptive Multi-Depth Explanation

Synthesize the concept across structured levels to ensure both rapid intuition and deep technical mastery:

1. **Simple Summary (ELI5)**: Explain the concept in plain, non-jargon language that any developer or stakeholder can grasp immediately.
2. **Technical Mechanics**: Detail how it works under the hood: data flow, memory model, execution phases, or state transitions.
3. **Mental Model**: Provide an intuitive analogy from daily life or foundational computer science.
4. **Code Example**: Provide a concise, runnable, and idiomatic code snippet illustrating the concept in practice.
5. **Common Pitfalls**: Highlight common mistakes, anti-patterns, and performance or security traps.
6. **Best Practices**: State concrete production recommendations and guidelines for when and when not to use it.
7. **Related Concepts**: Connect the topic to 2-3 adjacent concepts, tools, or design patterns.

## Output Format

Output using this structured markdown template:

```markdown
# Learn: <Concept>

## 1. Simple Summary (ELI5)
<Plain language explanation capturing core value>

## 2. Technical Mechanics
<Detailed explanation of underlying architecture, algorithms, and lifecycle>

## 3. Mental Model
<Concrete analogy explaining the concept intuitively>

## 4. Code Example
```<language>
// Minimal, self-contained, and runnable example
```

## 5. Common Pitfalls
- **<Pitfall 1>**: <Why developers make this mistake and how to prevent it>
- **<Pitfall 2>**: <Why developers make this mistake and how to prevent it>

## 6. Best Practices
- **<Practice 1>**: <Concrete operational recommendation>
- **<Practice 2>**: <Concrete operational recommendation>

## 7. Related Concepts
- **<Concept A>**: <How it relates or differs>
- **<Concept B>**: <How it relates or differs>
```

## Rules

- Ground explanations in technical reality; avoid marketing buzzwords or hand-waving.
- Keep code examples minimal: focus strictly on illustrating the target concept.
- If the concept is ambiguous, explain the most common usage first and mention the alternative.

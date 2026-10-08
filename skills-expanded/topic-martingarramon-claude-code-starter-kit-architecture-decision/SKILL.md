# Skill: Architecture Decision

## When to Use
Activate when choosing between technical approaches, designing system components,
or making decisions that are expensive to reverse. This includes database choices,
framework selection, API design, service boundaries, and data modeling.

## Core Principle
Architecture decisions are bets. Make the bet explicit: what are you optimizing for,
what are you trading off, and what would make you change your mind?

## Process

### 1. Frame the Decision
Before evaluating options, define the decision clearly.
- What specific question are you answering?
- What constraints are non-negotiable? (budget, timeline, team skill, compliance)
- What does "good enough" look like? Not every decision needs the optimal solution.
- What's the blast radius if this decision is wrong? (reversible vs. irreversible)

### 2. Identify Options (max 3)
Don't enumerate every possibility. Present 2-3 realistic options.
- For each option: what does it optimize for? What does it sacrifice?
- Include "do nothing" or "simplest thing" as an option when applicable
- Eliminate options that fail a hard constraint before detailed evaluation

### 3. Evaluate Against Requirements
Score each option against the actual requirements, not theoretical ideals.
- Functional: does it actually solve the problem?
- Operational: can you deploy, monitor, and debug it with your current team?
- Scale: does it handle your expected load in 12 months? (Not 5 years -- YAGNI.)
- Complexity: how much accidental complexity does it add?

### 4. Make a Recommendation
Take a position. Justify it in 2-3 sentences.
- State what you'd pick and why
- State the key tradeoff you're accepting
- State what would change your recommendation (the "trigger" to revisit)

### 5. Document the Decision
Record it so future developers know why, not just what.

## Output Format

```
## ADR: [Decision Title]

**Status:** [Proposed / Accepted / Superseded]
**Date:** [YYYY-MM-DD]
**Context:** [Why this decision is needed -- 2-3 sentences]

**Options:**
1. [Option A] -- [one-line summary]
2. [Option B] -- [one-line summary]
3. [Option C] -- [one-line summary]

**Decision:** [Which option and why -- 2-3 sentences]
**Tradeoff:** [What you're giving up]
**Revisit if:** [Conditions that would change this decision]
```

## Rules
- Never present more than 3 options. Decision fatigue kills progress.
- Always include the tradeoff. If there's no downside, you haven't thought hard enough.
- Reversible decisions should take minutes. Irreversible decisions deserve this full process.
- Document decisions in `docs/` or `memory/` -- not just in conversation.

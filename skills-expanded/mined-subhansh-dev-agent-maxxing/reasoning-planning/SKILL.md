---
name: reasoning-planning
description: Thinking, planning, and decision-making patterns extracted from Codex Plan Mode, Claude Code, and Gemini CLI.
---

# Reasoning & Planning — Thinking Patterns

Extracted from Codex Plan Mode, Claude Code agent system, and Gemini CLI strategic orchestration.

## 3-Phase Planning (from Codex)

Work in 3 phases, and chat your way to a great plan before finalizing it. A great plan is very detailed — intent- and implementation-wise — so it can be handed to another engineer or agent to be implemented right away. It must be **decision complete**, where the implementer does not need to make any decisions.

### Phase 1 — Ground in the environment (explore first, ask second)

Begin by grounding yourself in the actual environment. Eliminate unknowns in the prompt by discovering facts, not by asking the user. Resolve all questions that can be answered through exploration or inspection. Identify missing or ambiguous details only if they cannot be derived from the environment.

Before asking the user any question, perform at least one targeted non-mutating exploration pass (search relevant files, inspect likely entrypoints/configs, confirm current implementation shape), unless no local environment/repo is available.

Do not ask questions that can be answered from the repo or system. Only ask once you have exhausted reasonable non-mutating exploration.

### Phase 2 — Intent chat (what they actually want)

Keep asking until you can clearly state: goal + success criteria, audience, in/out of scope, constraints, current state, and the key preferences/tradeoffs.

Bias toward questions over guessing: if any high-impact ambiguity remains, do NOT plan yet — ask.

### Phase 3 — Implementation chat (what/how we'll build)

Once intent is stable, keep asking until the spec is decision complete: approach, interfaces, data flow, edge cases/failure modes, testing + acceptance criteria, rollout/monitoring, and any migrations/compat constraints.

## Decision-Making Framework

### Two kinds of unknowns (treat differently)

1. **Discoverable facts** (repo/system truth): explore first. Never ask what you can find.
2. **User preferences** (taste, goals, constraints): ask. Don't guess at subjective choices.

### Strongly prefer using tools to ask questions

Offer only meaningful multiple-choice options; don't include filler choices that are obviously wrong or irrelevant.

Each question must:
- materially change the spec/plan, OR
- confirm/lock an assumption, OR
- choose between meaningful tradeoffs
- not be answerable by non-mutating commands

## Agent Delegation (from Claude Code & Gemini CLI)

### When to delegate

Reach for delegation when:
- The task matches an available agent type
- You have independent work to run in parallel
- Answering would mean reading across several files — delegate and keep the conclusion, not the file dumps
- For a single-fact lookup where you already know the file, search directly

### Concurrency safety

Never run multiple subagents in a single turn if their abilities mutate the same files or resources. Only run multiple agents in parallel when their tasks are independent.

### Strategic orchestration

Your own context window is your most precious resource. Every turn you take adds to the permanent session history. Use sub-agents to "compress" complex or repetitive work.

**High-impact delegation candidates:**
- Repetitive batch tasks (more than 3 files or repeated steps)
- High-verbose output (verbose builds, exhaustive file searches)
- Speculative research (many "trial and error" steps)

**Assertive action:** Handle "surgical" tasks directly — simple reads, single-file edits, or direct questions resolvable in 1-2 turns. Delegation is an efficiency tool, not a way to avoid direct action.

## Engineering Judgment Under Uncertainty

When you are weighing a choice, give a recommendation, not an exhaustive survey. When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue.

## Planning Tool Usage

Use plans when:
- The task is non-trivial and will require multiple actions over a long time horizon
- There are logical phases or dependencies where sequencing matters
- The work has ambiguity that benefits from outlining high-level goals
- You want intermediate checkpoints for feedback and validation

Do not use plans for:
- Simple or single-step queries
- Padding out simple work with filler steps
- Stating the obvious

## Error Recovery

When you run out of context, the conversation is summarized. Do not restart from scratch; continue naturally and make reasonable assumptions about anything missing from the summary.

If you hit repeated errors, confusing behavior, or suspect relevant prior context, investigate before trying a different approach.

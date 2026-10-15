---
name: compound-workflow
description: Compound engineering workflow for AI-assisted development. Enforces plan-before-work, context engineering, self-review, and compound-after-shipping. Use on every non-trivial task — feature implementation, bug fixes, refactoring, architecture decisions. Triggers on "build", "implement", "fix", "refactor", "plan", "ship", or when starting any multi-step coding task.
---

# Compound Engineering Workflow

A workflow system for engineering with AI agents. Each unit of work should make
subsequent work easier — not harder. Corrections become constraints, patterns
become reusable, and the system gets smarter over time.

## The Main Loop: Plan → Work → Review → Compound

Spend 80% of effort on planning and review, 20% on implementation. The code
writes itself if the plan is right.

## 1. Plan Before Work

Before implementing any non-trivial feature or fix:

1. **Research the codebase.** Find specific files, line numbers, and code snippets.
   Be concrete — "chat.js handles streaming" is noise. "chat.js:142-180 uses
   EventSource with onmessage to append chunks" is signal.
2. **Research externally.** What do the docs say? What are best practices?
3. **Write a brief.** Use the template at `.claude/briefs/TEMPLATE.md` if available.
   The brief is the plan — it should have enough detail that a less capable model
   could execute it without asking questions.
4. **Present the plan for approval.** Human reviews the plan, not just the code.
   Catching wrong direction before 200 lines get written is where the leverage is.

Skip only for: bug fixes under 10 lines, purely mechanical changes.

## 2. Context Engineering

### The Four Dimensions of Context Quality

Every turn, the model picks its next action based solely on what's in the
conversation window. Optimize for:

| Dimension | What It Means |
| --- | --- |
| **Correctness** | No wrong information. Bad research cascades into bad code. |
| **Completeness** | All relevant info present. Missing context = the agent guesses. |
| **Size** | Compact — less noise, more signal. Summaries over raw dumps. |
| **Trajectory** | The pattern of the conversation steers future output. Corrections breed more corrections. Clean plans breed clean execution. |

### The "Dumb Zone" (~40% Context Window)

Around 40% of the context window, quality starts degrading. Too much history,
too many tool results, too much exploration — all work happens in this degraded zone.

**How to recognize it:** Agent goes in circles. Outputs get generic or repetitive.
Forgets earlier instructions. Suggests things already tried.

**The fix:** Compact what you know into a brief. Start a fresh session. Load just
the plan. Don't retry in a bloated context.

### Don't Research and Build in the Same Session

The session that explores the codebase outputs a brief. A separate, fresh session
implements it. This keeps each context window focused.

**How to compress research:**
- File names with line numbers, not just file names
- Actual code snippets of patterns to follow, not descriptions of code
- Structured summaries (tables, bullets), not prose paragraphs
- Only what's relevant — finding 12 files doesn't mean listing all 12

### Sub-Agents Are for Context Control

Don't create "frontend agent" and "backend agent" — that's anthropomorphizing.
Create "research agent" and "implementation agent." The purpose is keeping each
context window focused and clean.

**Use sub-agents when:**
- Research might explore many files (pollutes main context)
- Task has distinct phases benefiting from fresh contexts
- Parallel work is genuinely independent

**Don't use when:**
- Small enough for one focused context
- Phases are tightly coupled
- Just trying to feel productive by parallelizing

## 3. Self-Review Before Presenting Output

Before presenting any plan, implementation, or design decision, answer these
three questions **unprompted**:

1. **"What was the hardest decision I made here?"** — Surface the judgment calls.
   Don't hide trade-offs behind clean-looking code.
2. **"What alternatives did I reject, and why?"** — Show the options considered.
   This lets the human evaluate reasoning, not just results.
3. **"What am I least confident about?"** — Flag weak spots. Direct human
   attention where it's most needed.

Keep it short — 1-2 sentences per question. Skip for trivial changes.

**Why:** Agent output that looks clean can still be wrong in ways hard to spot.
These questions force exposed reasoning so the human reviews the thinking, not
just the artifact.

## 4. Compound After Shipping

After completing any non-trivial feature or fix, prompt: **"Want to run the
compound step?"** Then ask:

1. **What did the agent get wrong that needed correction?** → save as feedback
   in project memory or constraints file
2. **What reusable pattern emerged?** → add to existing docs or rules
3. **What context would help someone coming back in 2 weeks?** → session log

**Output = edits to existing files.** A line added to a memory, a row in a table,
a note in a log. Never create separate compound docs — that's bloat.

Each correction encoded is one less correction next time. This is the step that
makes work compound.

## 5. Parallel Agents (When Applicable)

For details on running parallel agents with git worktrees, see
[parallel-agents.md](parallel-agents.md).

**When to use:** Feature cleanly splits into independent workstreams.

**The loop:** Research → Plan → Split into scoped briefs → Implement in fresh
contexts → Compound after merging.

**Key principle:** Parallel agents are a context control technique. Speed is the
side effect. The real win is each agent getting a focused context window.

## The 50/50 Rule

Allocate 50% of engineering time to features, 50% to system improvements that
create institutional knowledge. Traditional teams spend 90/10. An hour creating
a review checklist saves 10 hours over the next year. The compound step is where
this 50% actually happens — don't skip it.

## Quick Reference

| Phase | Action | Skip when |
| --- | --- | --- |
| Plan | Write brief, research codebase + external, get approval | < 10 line fix |
| Work | Implement in fresh context with plan loaded | — |
| Review | Self-review: hardest decision, alternatives, confidence | Trivial change |
| Compound | What went wrong, what pattern emerged, what context for later | Nothing learned |

## Reference Files

- [parallel-agents.md](parallel-agents.md) — Parallel agents with git worktrees
- [improve-codebase-architecture.md](improve-codebase-architecture.md) — Module deepening, architectural friction, dependency categories, testing strategy

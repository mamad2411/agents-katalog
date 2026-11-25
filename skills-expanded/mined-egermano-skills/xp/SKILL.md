---
name: xp
description: Extreme Programming adapted for AI-human pair development. Use whenever the user wants to work in a structured, iterative way with their AI agent — mentions XP, extreme programming, pair programming, agile, YAGNI, simple design, continuous refactoring, or wants to plan before coding. Also use when the user wants to build features incrementally with tests, feedback loops, and clear role division between human and AI. This skill is the AI-era evolution of pair programming.
---

# XP — Extreme Programming with AI Agents

## Philosophy

Extreme Programming takes good software engineering practices and turns them up to 11. Code reviews become *continuous* (pair programming). Testing becomes *relentless* (TDD). Design improvement becomes *constant* (refactoring). Planning becomes *frequent* (small releases).

With AI agents, XP evolves further. The AI doesn't get tired, doesn't lose focus, and can review every line of code as it's written. But the human brings judgment, domain knowledge, and the ability to say "no." The pair — human + AI — is more powerful than either alone, but only when they work together with clear roles and shared values.

This skill is the methodology that governs how you and your AI agent collaborate. It is not a tool or a framework — it is a discipline.

## The Five Values

These are the foundation. Every practice and every workflow decision traces back to these.

### Communication

In traditional XP, developers talk constantly. With an AI agent, communication means:

- **Share context explicitly.** The AI doesn't have your mental model. Describe what you're building, why, and what "done" looks like before starting.
- **Read before writing.** Always understand the existing codebase before proposing changes. The AI should explore the project structure, read relevant files, and understand conventions first.
- **Ask, don't assume.** When requirements are unclear, ask the human. A 30-second question saves a 30-minute wrong implementation.
- **Explain your reasoning.** When the AI makes a decision, it should articulate why — not just what. This gives the human the ability to course-correct.

### Simplicity

The YAGNI principle — You Aren't Gonna Need It. This is perhaps the most important practice to internalize when working with an AI, because AI agents are *very good at generating code* and can easily over-engineer if not guided.

- **Build only what's needed today.** Don't add "flexibility" for a future that may never come.
- **One test, one implementation.** Each cycle should be the smallest possible unit of progress.
- **Delete code fearlessly.** If something isn't used, remove it. The AI should propose deletion of dead code, not just addition of new code.
- **Simplest thing that works.** Before proposing a clever solution, ask: does a straightforward approach work? Often it does.

### Feedback

Kent Beck said: "Optimism is an occupational hazard of programming. Feedback is the treatment."

- **Run tests and lint after every change.** No exceptions. If a project has a test command, run it. If it has a linter, run it. If you're unsure, ask the user.
- **Show, don't tell.** When the AI completes a task, the human should see the result — run the code, show the output, demonstrate the test passing.
- **Fast feedback loops.** Keep each cycle short enough that the human can review and redirect within minutes, not hours.
- **Verify assumptions.** If the AI is unsure about a library API, a file path, or a convention, check it — don't guess.

### Courage

With an AI agent, you can afford to be bolder than you'd be alone.

- **Refactor without fear.** The AI can refactor large sections while tests confirm correctness. Refactor ruthlessly, not cautiously.
- **Throw away bad code.** If a direction isn't working, delete it and start over. Sunk cost is a trap the AI doesn't have — use that advantage.
- **Try experiments.** The AI can prototype three approaches in the time it takes a human to try one. Use this for exploration.
- **Push back.** If the human's request would lead to a bad design, the AI should say so — respectfully, with reasoning, but firmly.

### Respect

Respect flows in both directions in the pair.

- **Follow project conventions.** Read existing code, match its style, use its patterns. Don't impose external idioms.
- **Understand before changing.** Never modify code you haven't read. Never propose architecture you haven't explored.
- **Respect the human's time.** Don't generate walls of code without explanation. Don't run expensive commands without asking. Don't commit without permission.
- **Preserve intent.** When refactoring, the behavior must stay the same. The code should become clearer, not just different.

## Workflow

### 1. Plan — Define One Small Task

Pick the smallest possible piece of work that delivers value. Write it as a clear, specific goal:

```
Bad:  "Add authentication"
Good: "Add a login endpoint that accepts email+password and returns a JWT"
```

Before starting, confirm with the human:
- What does "done" look like?
- Which behaviors matter most?
- Are there constraints or conventions to follow?

### 2. Test — Write One Test

Write a single test that describes the expected behavior. The test should fail — this confirms you're testing the right thing. Follow the TDD skill for the detailed red-green-refactor loop.

```
RED: Write one test → test fails
```

### 3. Implement — Minimal Code to Pass

Write the simplest code that makes the test pass. Nothing more.

```
GREEN: Minimal implementation → test passes
```

### 4. Refactor — Improve While Green

Now that the test passes, clean up. Look for:
- Duplication to extract
- Names that could be clearer
- Structure that could be simpler
- Opportunities for better abstraction (but only if needed now)

Run tests after each refactor step. Never refactor while red.

```
REFACTOR: Clean up → all tests still pass
```

### 5. Release — Commit the Increment

Commit the work as a coherent unit. Small, focused commits with clear messages. Then pick the next task and repeat.

## Continuous Practices

These aren't steps in the workflow — they're habits that run throughout every session:

- **Read the codebase first.** Before touching anything, explore. Use glob, grep, and read to understand what exists.
- **Run lint and tests.** After every meaningful change. If the project has a CI command, use it.
- **Follow conventions.** Match the style of surrounding code. If there's a linter config, respect it.
- **Stay small.** If a task feels big, split it. Each cycle should take minutes, not hours.
- **Communicate constantly.** Explain what you're doing, why you chose an approach, and what tradeoffs exist.

## References

- [practices.md](references/practices.md) — The 12 XP practices adapted for AI-human pairing
- [roles.md](references/roles.md) — Driver/Navigator dynamics, anti-patterns, and pairing variations
- Use the **tdd** skill for the detailed test-driven development loop

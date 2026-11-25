---
name: design-a-loop
description: Use when a founder wants to automate a recurring agentic task and is moving from prompting to system design - when they say "should I set up a loop", "automate this with agents", "run this nightly", "make the agent prompt itself", "my agent loops and burns tokens", "set up CI triage", or "automate the dependency bumps". Produces a loop spec (trigger, skill, state file, gate, stop condition, escalation) and the cost-per-accepted-change metric to judge it. Run after agentic-build-loop; pairs with self-healing-fallbacks for the floor.
stage: build
function: engineering
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Design a Loop

A loop is a small system that finds the work, hands it to the agent, checks the result, records what
happened, and decides the next move on its own. You design it once; it prompts the agent from then on.
The leverage has moved from typing the prompt to designing the system that prompts. That is real
power and a real bill. A loop with no gate does not stop being wrong, it stops telling you, and it
spends the whole time. Build one only where the work repeats, the check is machine-gradable, and the
floor is hard.

## The method

Build tier. Full framework, tables, and a worked example:
[`references/loop-engineering.md`](references/loop-engineering.md). Standalone explainer:
[`docs/LOOP-ENGINEERING.md`](../../docs/LOOP-ENGINEERING.md).

### Step 1: Run the 4-condition test

Build a loop only if all four hold. Miss one and the loop costs more than it returns; do the task by hand.

| # | Condition | Pass looks like | Fail means |
|---|---|---|---|
| 1 | The task repeats | Weekly or more, same shape | One-off: just prompt it |
| 2 | Verification is automated | A test, type check, lint, or build fails the work without you in the room | No machine grader: you are the gate, so no loop |
| 3 | The token budget absorbs waste | Loops re-read, retry, explore; you can pay for that | Tight budget: the loop eats it on retries |
| 4 | The agent has senior tools | Logs, a reproduction environment, the ability to run its own code | Blind agent: it guesses, you clean up |

### Step 2: Pick the building blocks

Five blocks plus state. Start with the fewest that close the loop; add only when a failure demands it.

- **Automation (the heartbeat):** a schedule, an event, or a trigger. `/loop` for a fixed cadence; `/goal` to run until a written condition holds, checked by a separate model.
- **Worktree isolation:** git worktrees so parallel agents do not collide on the same files.
- **Skills:** the persistent project knowledge the agent reads every run.
- **Connectors and MCP:** the reach into GitHub, Linear or Jira, Slack, the error tracker.
- **Sub-agents:** separate the maker from the checker (the evaluator-optimizer pattern).
- **The state file:** the agent forgets between runs; the repo remembers. `STATE.md` lets it resume, not restart. Pair it with a standing `VISION.md` or `AGENTS.md` spec the agent rereads each run.

### Step 3: Build the minimum viable loop

One automation, one skill, one state file, one gate. Get one manual run reliable, turn it into a
skill, wrap it in a loop, then schedule it. Do not schedule a run you have never watched succeed.

### Step 4: Add the gate and the maker-checker split

The gate is what fails the work. Make it objective: a test suite, a build, a type check, a fresh
model scoring against a rubric. Split the roles so the agent that did the work is not the one judging
it; a maker grading its own homework marks generously. Put a separate verifier sub-agent on the gate
(see [critic-judge pairing](../../dictionary/04-agentic-patterns.md#critic-judge-pairing)).

### Step 5: Set the hard stop and the human-on-the-loop gate

Every loop needs a hard stop: a max iteration count, a wall-clock timeout, a token ceiling, and an
objective `/goal` stop checked by a fresh model. For anything irreversible or safety-relevant, a dose,
an allergen call, a regulatory filing, a payment, the loop proposes and a human disposes. The gate
must include the safety check, not just the tests. Human-on-the-loop is mandatory here, not optional.

## Output

- A **loop spec**: trigger, skill, state file, gate, stop condition, escalation owner.
- The metric that judges it: **cost per accepted change**, not tokens spent or tasks attempted. Below
  roughly half of changes accepted, the loop is losing; fix the gate or kill the loop.
- Next: wire the floor with `self-healing-fallbacks`, then schedule the heartbeat.

## Constraints

- Forbid the Ralph Wiggum loop: no soft completion, no missing gate, no missing hard stop. A loop that
  cannot fail the work and cannot stop itself is spending your money to produce nothing you checked.
- Require a real gate (objective, machine-gradable) and a hard stop (iteration, time, and token caps).
- Human-on-the-loop for any irreversible or regulated action; the gate carries the safety check.
- Read the diffs and spot-check the gate. Keep the loop off architecture decisions. An unattended loop
  is an unattended attack surface: re-audit permissions, treat skills as injection vectors, keep
  credentials out of logs.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[Loop (agentic loop)](../../dictionary/04-agentic-patterns.md#loop-agentic-loop) ·
[Loop engineering](../../dictionary/04-agentic-patterns.md#loop-engineering) ·
[Automation (heartbeat)](../../dictionary/04-agentic-patterns.md#automation-heartbeat) ·
[Worktree isolation](../../dictionary/04-agentic-patterns.md#worktree-isolation) ·
[State file (loop memory)](../../dictionary/04-agentic-patterns.md#state-file-loop-memory) ·
[Maker-checker split](../../dictionary/04-agentic-patterns.md#maker-checker-split) ·
[The Ralph Wiggum loop](../../dictionary/04-agentic-patterns.md#the-ralph-wiggum-loop) ·
[Comprehension debt](../../dictionary/04-agentic-patterns.md#comprehension-debt) ·
[Cost per accepted change](../../dictionary/04-agentic-patterns.md#cost-per-accepted-change) ·
[The God Agent](../../dictionary/04-agentic-patterns.md#the-god-agent-anti-pattern) ·
[Critic-judge pairing](../../dictionary/04-agentic-patterns.md#critic-judge-pairing) ·
[Human-on-the-loop](../../dictionary/04-agentic-patterns.md#human-on-the-loop-hotl)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0).

```
Act as my loop engineer. I want to automate a recurring agentic task without it burning money
or shipping work I never checked.
Task: [AGENT_TASK]. Domain: [DOMAIN]. Cadence: [how often it repeats].
1. Run the 4-condition test on my task and tell me plainly if I should NOT build a loop:
   (a) does it repeat weekly or more? (b) can a test, lint, type check, or build fail the work
   without me watching? (c) can my budget absorb retries and re-reads? (d) does the agent have
   logs, a reproduction environment, and the ability to run its own code? If any fail, say so
   and stop.
2. If it passes, design the minimum viable loop: one trigger, one skill (the standing knowledge
   it rereads), one state file (what it records so it resumes instead of restarting), one gate.
3. Define the gate as an OBJECTIVE check, and put a SEPARATE checker on it, not the same agent
   that did the work.
4. Set the hard stop: max iterations, a time limit, a token ceiling, and a written stop condition.
5. For anything irreversible or safety-relevant ([GUARDRAIL]: a dose, an allergen, a filing, a
   payment), require human-on-the-loop and make the gate include the safety check, not just tests.
Output a loop spec table: trigger, skill, state file, gate, stop condition, escalation owner.
Then give me ONE metric to judge it: cost per accepted change. End with the single next action.
```

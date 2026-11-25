---
name: agentic-build-loop
description: Use when a founder says "how do I actually build this", "Claude Code/Codex/Cursor keeps making a mess", "the agent wrote spaghetti", "it passed but I don't trust it", "I'm just vibe-coding", "the agent went off and rewrote everything", "do I need tests for this", or is starting a feature and wants the agent on a leash. Triggers on plan mode, spec-first, acceptance tests, review the diff, agentic technical debt, iteration cap, runaway loop. Tool-agnostic across Claude Code, Codex, Cursor, Gemini CLI. Produces a spec plus acceptance tests, a plan-mode framework, then agent-filled logic gated on a green suite. Skill turns vibe-coding into a spec-and-test loop; without it, the agent builds the wrong thing fluently.
stage: build
function: engineering
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Agentic Build Loop

The cost of syntax is zero. An agent writes correct code faster than you can, in any language, so the
job is not to type lines. You specify the system and the tests that judge it, and the agents iterate
until the suite goes green. Hand them a vague request and they build the wrong thing fluently. Hand
them a spec and a harness and they have nowhere to hide. You are the conductor; the architecture is
the score.

## The method

Full build loop, eval gates, a worked build, anti-patterns and a copyable template:
[`references/agentic-build-method.md`](references/agentic-build-method.md).

### Step 1: Write the spec and the acceptance tests first
Before any code, write two things the agent cannot infer: what the feature must do, and the handful of
tests that decide whether it did. Plain language is fine if that is all you have. The tests are the
contract the agent builds to. No target, no grip, and the agent drifts while you call the drift a
feature.

### Step 2: Plan mode, framework first
Run the agent in plan mode and ask for the structure, not the logic: the modules, their boundaries,
their interfaces, the skeleton empty of muscle. Read that hierarchy against your architecture and
validate it before a single line of logic. You can move a wall on a diagram for nothing. You cannot
move it once the roof is on.

### Step 3: Let agents fill the logic
Only when the frame is right, release the agents to write the logic. They run the tests, read the
failures, fix, and run again until the suite passes. Review every diff. A passing demo proves the
agent typed something plausible, not that it built the right thing.

### Step 4: Keep the master file current
The agents read one master file every session (`CLAUDE.md`, `AGENTS.md`, `.cursor/rules`, `GEMINI.md`).
At the end of the session, append the trade-offs you made: the boundary you moved, the constraint you
added, the thing an agent must never do next time. The file is where the multiplier lives.

## Output

- A spec and a set of acceptance tests for the feature.
- A validated module framework, read against your architecture before any logic.
- A working feature whose passing suite is the evidence it is done, plus an updated master file.
- Next: run `eval-and-safety-harness` before anything acts on a user.

## Constraints

- Structure before logic, or it collapses: emergent structure looks fine at ten files and buckles at
  four hundred.
- Review every diff. "The agent said it passed" is not the same as "you read what it changed".
- Do not let an agent loop without a budget or an iteration cap. An unbounded loop burns tokens and
  buries the failure.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[spec-first development](../../dictionary/04-agentic-patterns.md#spec-first-development) ·
[tests as harness](../../dictionary/04-agentic-patterns.md#tests-as-harness) ·
[plan mode](../../dictionary/04-agentic-patterns.md#plan-mode) ·
[agentic technical debt](../../dictionary/05-failure-modes.md#agentic-technical-debt)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0).

```
Act as my build conductor. My feature in one line: [ONE_LINER]. Domain: [DOMAIN]. Who uses it: [ICP].
Do not write any logic yet. Instead:
1. Turn my one line into a short spec: what the feature must do, and the inputs and outputs.
2. Write 2 acceptance tests in plain language - the pass/fail checks that decide it is done. These are
   the contract you build to.
3. Propose the framework before the logic: the screens or modules, their boundaries, and how they
   connect. Show me the skeleton, empty of detail, and wait for my approval.
Then stop and give me ONE next action to take once I have approved the frame.
```

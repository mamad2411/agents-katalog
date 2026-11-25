---
name: evaluating-ai-agents
version: "1.1.0"
description: >
  Designs and runs evaluations (evals) for custom AI agents to measure
  behavioral quality, catch regressions, and establish production readiness.
  Based on Anthropic's "Demystifying evals for AI agents" (Jan 2026). Covers
  eval structure (task/trial/transcript/outcome), grader selection (code-based,
  model-based, human), capability vs. regression suites, task set construction,
  LLM-as-judge calibration, pass@k vs pass^k reporting, and CI integration.
  Use when the user mentions: agent eval, evaluate this agent, does my
  agent work reliably, regression test, agent quality, build an eval suite,
  test my agent, LLM judge, grader, benchmark my agent, agent accuracy, or
  any request to measure whether an agent is producing correct or reliable
  outputs. Also triggers on: my agent feels worse, something regressed,
  how do I know if my agent is working, I need to test before shipping.
---

# AI Agent Evaluator

Turns "I think this agent works" into a measurable, repeatable signal.
Based on Anthropic's field-tested evaluation framework for real-world agents.

The core problem: without evals, debugging is reactive — wait for complaints,
reproduce manually, fix the bug, hope nothing else broke. Evals make
behavioral changes visible before they reach users.

---

## Evals

**Should trigger:**
1. "I want to verify my FlashFusion intake agent handles edge cases correctly"
2. "I changed a system prompt and want to make sure nothing regressed"
3. "How do I know if my n8n workflow agent is actually doing what I think?"

**Should NOT trigger:**
1. "Compare Claude Code vs Aider on a benchmark" — use ecc:agent-eval
2. "Does this code have bugs?" — use auditing-logic or debug-like-expert

---

## Core Vocabulary (Anthropic definitions)

Learn these before designing any eval. Imprecise vocabulary produces
imprecise evals.

| Term | Definition |
|---|---|
| **Task** | A single test with defined inputs and success criteria |
| **Trial** | One attempt at a task. Run multiple — agents are stochastic |
| **Grader** | Logic that scores performance. One task can have multiple graders |
| **Transcript** | The complete record: outputs, tool calls, reasoning, intermediate results |
| **Outcome** | The final state in the environment. Not what the agent *said* happened — what *actually* happened |
| **Eval harness** | Infrastructure that runs evals end-to-end and aggregates results |
| **Agent harness** | The scaffold that enables the model to act as an agent |
| **Eval suite** | A collection of tasks measuring a specific capability or behavior |

**The transcript vs. outcome distinction is critical.**
A workflow agent might log "Ticket created successfully" (transcript) while
the outcome — whether a ticket actually exists in FreshService — is the
ground truth. Always grade the outcome, not the agent's report of the outcome.

**You're evaluating model + harness together, not the model alone.**
A change to your n8n workflow or system prompt is a change to the agent
being evaluated, regardless of whether the underlying model changed.

---

## Decision Tree

```
What are you trying to measure?
  │
  ├─ "Does this agent work at all / correctly?"
  │    → Capability eval (Section 2) — target low pass rate, hill to climb
  │
  ├─ "Did I break something with this change?"
  │    → Regression eval (Section 2) — target ~100% pass rate, detect drift
  │
  ├─ "How do I grade this agent's outputs?"
  │    → Grader selection (Section 3)
  │
  ├─ "How do I build the test cases?"
  │    → Task set construction (Section 4)
  │
  ├─ "I need to evaluate an n8n workflow or Claude API agent specifically"
  │    → Agent-type patterns (Section 5)
  │
  └─ "What numbers should I report?"
       → Metrics and reporting (Section 6)
```

---

## Section 2: Capability vs. Regression Evals

### Capability evals

**Question:** "What can this agent do well?"
**Target pass rate:** Low — start where the agent struggles.
**Purpose:** A hill to climb. These measure improvement.

Design capability evals around the behaviors that matter most for production:
- Correct tool selection (did it call the right tool for this input?)
- Output quality (is the generated content correct and appropriate?)
- Edge case handling (what happens on unusual or adversarial inputs?)
- Error recovery (does it handle tool failures gracefully?)

### Regression evals

**Question:** "Does the agent still handle tasks it used to?"
**Target pass rate:** ~100%. Any drop is a signal to investigate.
**Purpose:** Protection against backsliding.

Seed from real production failures. Every bug you fix in production
becomes a regression test. If the agent broke once, it can break again.

### The graduation pattern

After an agent is launched and optimized:
Capability evals with high pass rates → graduate → regression suite.
"Can we do this at all?" becomes "Can we still do this reliably?"

Run both types continuously, not just at release time.

---

## Section 3: Grader Selection

Code-based, model-based, and human graders; scoring modes. See `references/eval-framework.md` for the full grader selection guide.

---

## Section 4: Task Set Construction

Where to get tasks, task format, and growing the task set. See `references/eval-framework.md` for the full task-set methodology.

---

## Section 5: Agent-Type Patterns

Evaluation patterns for n8n workflow agents, Claude API agents, MCP server tools, and multi-agent systems. See `references/eval-framework.md` for the full agent-type pattern library.

---

## Section 6: Metrics and Reporting

### What to measure

- **Task completion rate:** % of tasks where the outcome matches expected
- **Tool call accuracy:** % of tasks where the agent selected the correct tool(s)
- **Cost per task:** average tokens and $ per trial
- **Latency distribution:** p50/p90/p99 turn completion times

### pass@k vs pass^k

Report both the optimistic (pass@k) and reliability (pass^k) metrics. See `references/eval-framework.md` for the statistical formulas and interpretation.

### CI integration

Run regression evals automatically on:
- Any change to a system prompt
- Any change to tool definitions
- Any model version change
- Any change to the agent harness / workflow structure

Fail the deploy (or flag for review) if regression pass rate drops below
threshold. The threshold for acceptable regression varies by agent risk:
higher-stakes agents need stricter thresholds.

---

## Self-Verification

Before shipping any eval suite:
- [ ] Every task has a defined, measurable expected outcome
  (not "responds helpfully" — "returns status code 201" or "creates record")
- [ ] Grader types match what's being measured
  (code for deterministic outcomes, model for quality, human for calibration)
- [ ] At least one regression task per known production failure
- [ ] Rubric test passed: two people read each model-grader rubric and
  agree on pass/fail for the same sample independently
- [ ] pass^k reported alongside pass@k
- [ ] Eval suite is seeded from real production inputs, not only
  idealized examples

---

## Reference Files

- `references/eval-framework.md` — grader selection guide, task-set construction methodology, agent-type pattern library, and the pass@k / pass^k statistical formulas (moved from sections 3–5 and the metrics section).

---

## CLAIMS
- Teams without evals catch issues only in production, where fixing one
  failure creates others — this pattern is observed consistently across
  agent deployments at all scales
- Grading the outcome (actual environment state) rather than the transcript
  (what the agent reported) is the only reliable measure for consequential
  agents; transcript-only grading can be fooled by confident but incorrect
  agent assertions
- pass^k (succeed across all k trials) surfaces reliability gaps that
  pass@k (succeed in at least one trial) consistently obscures

## COUNTEREXAMPLE
- The 20–50 task recommendation for early-stage agents doesn't hold once
  the agent is in production and handling diverse inputs at scale — at that
  point, expanding to hundreds of tasks covering the real input distribution
  is necessary to maintain signal quality

## CONTRADICTIONS
- "Automate all evals" conflicts with the calibration requirement for
  model-based graders — periodic human review is mandatory to verify the
  LLM judge is still aligned with human judgment, especially after model
  upgrades

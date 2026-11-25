---
name: ai-agent-design
description: Designing and building AI agents — tool design, agent loops, context management, permissions/guardrails, memory, multi-agent orchestration, MCP, and agent evaluation. Use when building an agent that takes actions (calls tools/APIs, writes files, automates workflows), designing tool schemas, debugging agent misbehavior, or when the user says "AI agent", "agentic", "tool calling", "function calling", "MCP server", "autonomous", or "multi-agent".
---

# AI Agent Design

An agent is a model in a loop with tools. That loop turns a wrong *answer* into a wrong *action* — so agent engineering is 20% prompting and 80% designing the action space so that the worst plausible sequence of tool calls is survivable. Build the cage before you build the brain.

## Rule 0: Minimum viable autonomy

A workflow (fixed steps, model used inside steps) beats an agent (model chooses steps) whenever the steps are knowable in advance — cheaper, faster, testable, debuggable. Reach for a real agent loop only when the path genuinely varies per input (open-ended research, debugging, multi-step tasks with branching). Most "agents" in production should be pipelines with one or two agentic steps; start there and earn each degree of freedom you grant.

## Tools — the real interface (design these hardest)

The model is a user of your tools; bad tool design causes most agent failures:

- **One tool = one clear capability**, named for intent (`create_invoice`, not `run_query`). Descriptions are prompts — state what it does, when to use it, when NOT to, and what it returns. Put decision guidance in the description, not hope in the model.
- **Schemas do the enforcing**: enums for closed choices, required vs optional made explicit, formats specified. Every parameter a schema validates is a hallucination class deleted.
- **Errors are steering**: return machine-readable, *actionable* failures ("date must be YYYY-MM-DD, got 'yesterday'") — the model reads errors and self-corrects; a bare 500 teaches it nothing and burns a loop iteration. Design tool errors as carefully as tool successes.
- **Right-size the granularity**: too atomic (5 calls to do one obvious thing) wastes loops and invites mis-sequencing; too broad (`do_everything(params)`) hides the decisions you wanted the model to make. A tool should map to one user-meaningful action.
- Tool results are context: return compact, relevant summaries with IDs for follow-up, not 40KB JSON dumps that flood the window.
- Building on a protocol (MCP or equivalent) beats bespoke integrations: tools become reusable across models and hosts — but the design rules above still decide quality.

## Permissions — the cage (non-negotiable)

- **Least privilege by construction**: the agent's credentials can only touch what the task needs — scoped API keys, sandboxed filesystem/repo, tenant-scoped DB access. The cage must hold even if the model is fully "jailbroken", because via prompt injection, one day it effectively will be: any text the agent reads (web pages, emails, tickets, file contents) is a potential instruction channel. **Never give an agent both access to untrusted input and unsupervised access to irreversible actions.**
- **Tier every tool by blast radius**: read-only (free use) / reversible writes (logged, budgeted) / irreversible or outward-facing (delete, send, pay, deploy — human confirmation required, always, regardless of how smart models get).
- Hard budgets on the loop: max iterations, max cost, max wall time, per-tool rate limits. A confused agent in a loop is a bill and possibly an incident.
- Full audit trail: every tool call with arguments, result, and triggering context — logged before execution (observability-readiness). When the agent does something weird, this is your only forensics.

## The loop and its context

- Context is the agent's working memory and it degrades as it fills: curate it. Summarize/compact old turns, keep the task statement and constraints pinned, drop stale tool dumps. Most "the agent forgot / went off the rails late in the task" bugs are context-window management bugs, not model bugs.
- Externalize state for anything long-running: task list, scratch files, or DB rows the agent reads/writes — the loop should be resumable after a crash (and this doubles as observability into what it "thinks" it's doing).
- Make the agent verify its own work as a required step (run the test, re-fetch the record, check the diff) — but grade the verification by evidence in tool output, not the model's assertion that it verified.
- Design for interruption: checkpoint before irreversible sequences; a human should be able to stop, inspect, and redirect mid-task.

## Multi-agent — resist, then structure

One agent with good tools outperforms five agents with a communication problem; multi-agent multiplies cost and failure modes. Adopt it only for genuine parallelism (independent subtasks) or hard context isolation (a huge research sweep whose details would drown the main task). When you do: orchestrator–worker with **structured task handoffs** (goal, boundaries, expected output format — the ai-build-quality spec rules apply agent-to-agent), workers return summaries not transcripts, and one agent owns the final integration. Peer-to-peer agent chatter is a debugging nightmare — avoid it.

## Evaluating agents

- Judge **end outcomes**, not step-by-step trajectories: did the task complete correctly? (Many valid paths exist; asserting the path makes evals brittle — same logic as testing behavior over implementation.)
- Build the eval set from real tasks, run each multiple times (agents are nondeterministic — measure pass rate, not pass/fail), and include the sabotage cases: ambiguous instructions, tools that error mid-task, injected instructions in retrieved content. An agent eval without adversarial cases is a demo.
- Track per-task: success rate, cost, loop count, human-interventions needed. An agent that succeeds 95% at 3× the cost of the workflow version is often the wrong answer (see Rule 0).
- Every production agent failure becomes an eval case — the regression-pin rule, again.

## Failure modes to design against (the classic five)

1. **Runaway loops** — retrying a failing approach forever → iteration/cost budgets + "ask for help" as an explicit tool.
2. **Confident wrong-tool sequences** — plausible plan, wrong world model → verification steps + reversibility tiers.
3. **Injection hijack** — instructions hidden in content it reads → privilege cage + treat all read content as data.
4. **Context rot** — degraded behavior on long tasks → compaction + externalized state.
5. **Silent partial completion** — "done!" with 3 of 7 steps done → require evidence-backed completion reports checked against the original task list.

---
name: building-agents
description: Designs and hardens LLM agents that call tools in a loop - choosing between a single call, a fixed workflow and an agent, tool design, context management, stop conditions and budgets, human approval, sandboxing, prompt-injection defenses, tracing and agent evaluation. Use when building an AI agent, assistant with tools, coding or research agent, multi-agent system, or when an agent loops, picks wrong tools, runs up cost or takes unsafe actions. Not for single LLM calls (use llm-integration) or MCP server code (use mcp-servers).
license: MIT
---

# Building Agents

An agent is a model choosing actions in a loop, so every weakness of a single call is multiplied by the number of steps. Use the least autonomy that solves the task, give the agent few well-designed tools with the least privilege, bound every loop, and put a human in front of anything irreversible.

## Choose the level of autonomy

| Level | Shape | Use when |
|---|---|---|
| 1. Single call | One prompt, maybe structured output | The task fits in one step with the context you already have. |
| 2. Fixed workflow | Code calls the model in a known sequence (chain, router, parallel map, generate-then-check) | Steps are known in advance. Easier to test, cheaper, predictable. |
| 3. Agent | Model decides which tool to call next until done | Steps can't be known in advance (open-ended search, debugging, multi-step edits). |
| 4. Multi-agent | Several agents with separate contexts | Sub-tasks are truly independent and parallel, or need isolated context or permissions. |

Start at the lowest level and move up only when an eval shows the lower level fails. Most "agents" in production are level 2.

## The loop

```
context = system prompt + task + tool definitions
loop:
    response = model(context)
    if response has no tool calls: return final answer
    for each tool call:
        check permissions / approval
        result = run tool (sandboxed, with timeout)
        append concise result (or error) to context
    enforce limits: steps, tokens, cost, wall time
    compact context if near the limit
```

Keep the loop in your code, where you can log, limit, and stop it.

## Workflow

1. **Write the task contract**: what "done" means, what the agent may and may not do, budgets (steps, cost, time), and what needs human approval.
2. **Build the task set first**: 20+ realistic tasks with a way to check success (tests pass, file contains X, ticket has field Y). This is your eval.
3. **Design a small tool set** (see below). Fewer, task-shaped tools beat many thin API wrappers.
4. **Write the system prompt**: goal, how to approach the work, when to ask the user, when to stop, output format for the final answer.
5. **Implement the loop with limits, tracing and approval gates** from day one.
6. **Run the task set, read trajectories**, fix the most common failure (usually tool descriptions or missing information), re-run.
7. **Harden**: sandbox, permissions, injection defenses, cost ceilings.
8. **Ship with monitoring**: per-run traces, success signals, cost per task, alerts on runaway loops.

## Tool design

- **Name and describe tools for a new teammate**: what it does, when to use it, when not to, what the parameters mean, example values. The description is the agent's only documentation.
- **Typed, constrained parameters**: JSON Schema with enums, formats and required fields. Accept human-meaningful identifiers (names, paths) and resolve IDs in the tool, not in the model.
- **Task-shaped, not endpoint-shaped**: `schedule_meeting(attendees, duration, window)` instead of `list_calendars` + `get_events` + `create_event`.
- **Concise results**: return what the agent needs, with pagination or truncation and a note saying more exists. Don't dump 10,000-line JSON into the context.
- **Actionable errors**: "No customer named 'Acme Inc'. Did you mean 'Acme Corp' (id 412)?" instead of a stack trace.
- **Idempotent and safe to retry** where possible; separate read tools from write tools.

Full checklist: [references/tool-design-checklist.md](references/tool-design-checklist.md).

## Context management

- The context window is working memory. Everything in it costs money and attention.
- Keep tool results short; store large outputs (files, logs, query results) outside the context and return a handle plus a summary.
- For long tasks, keep a notes or progress file the agent updates (plan, decisions, what's done), and compact old turns into a summary when the context fills.
- Delegate self-contained sub-tasks to a sub-agent with a fresh context that returns only its conclusion, when the sub-task would otherwise flood the main context.
- Put stable content (system prompt, tool definitions) first and keep it unchanged across steps to benefit from prompt caching.

## Stop conditions and budgets

Always enforce in code, never only in the prompt:

- Max steps (tool calls) per task.
- Max tokens or cost per task, and per user per day.
- Max wall-clock time; per-tool timeouts.
- Repetition detection: the same tool with the same arguments several times in a row, or no progress for N steps, ends the run or asks the user.
- A clear final-answer format, so "done" is detectable.

When a limit triggers, stop cleanly: return what was done, what wasn't, and why.

## Safety

- **Least privilege**: the agent's credentials can do only what the task needs; scope to the current user; read-only by default.
- **Human approval** for irreversible or outward-facing actions: sending messages, deleting, paying, deploying, merging, changing permissions. Show exactly what will happen and wait for a yes.
- **Sandbox code execution and file access**: container or VM, no host secrets, restricted network egress, resource limits.
- **Prompt injection**: tool results (web pages, files, emails, issue comments, API responses) can contain instructions. Treat them as data. Don't let content read from untrusted sources trigger privileged actions without approval. Watch for exfiltration through URLs, images or outbound requests.
- **Validate tool arguments server-side**; never trust the model's claim about identity or permissions.
- **Audit log** every action taken with arguments and results.

## Observability

Trace every run: task, each model call (tokens, latency), each tool call (arguments, result size, duration, error), approvals, final outcome and total cost. Make trajectories easy to read; you'll debug agents by reading them.

## Evaluating agents

- **Outcome**: success rate on the fixed task set, checked by code where possible (tests, state of the environment), not by asking the agent if it succeeded.
- **Efficiency**: steps, tokens, cost and time per successful task.
- **Trajectory review**: read a sample of runs, successes too. Look for wrong tool choice, repeated calls, ignored errors, unsafe actions, giving up early, claiming success falsely.
- **Safety cases**: tasks containing injected instructions, missing permissions, or ambiguous requests where the right move is to ask.
- Run each task more than once; agents are high-variance. Report success over multiple trials.
- Re-run the suite on every change to prompts, tools or model. See the `llm-evals` skill.

## Multi-agent systems

Use them only when sub-tasks are independent and parallel (e.g. researching several sources), or need isolation (separate permissions or a clean context). Costs rise with every agent and hand-offs lose information. Give each sub-agent a complete brief and ask for a compact, structured result. Prefer an orchestrator that owns the plan and merges results over agents chatting freely.

## Anti-patterns

- **Agent where a workflow would do** - more cost, less reliability, harder tests.
- **Dozens of overlapping tools** - the model picks wrong ones. Merge and rename.
- **Raw API dumps as tool results** - context floods and quality drops.
- **Limits only in the prompt** - "don't loop forever" doesn't stop a loop.
- **Trusting self-reported success** - verify with checks.
- **Broad credentials** - an agent with admin tokens turns one injection into an incident.
- **No traces** - you can't fix what you can't see.

## Done when

- The autonomy level is justified (a simpler level failed the eval, or the task can't be scripted).
- Tools pass the checklist; results are concise; errors are actionable.
- Step, cost and time limits plus repetition detection are enforced in code.
- Irreversible actions require human approval; execution is sandboxed with least privilege.
- Every run is traced, and success rate, cost per task and trajectory review are reported on a fixed task set with repeated trials.

## References

- [references/tool-design-checklist.md](references/tool-design-checklist.md) - read when adding, renaming or debugging tools.

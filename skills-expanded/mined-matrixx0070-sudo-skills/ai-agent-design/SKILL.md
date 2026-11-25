---
name: ai-agent-design
version: 1.0.0
description: Design a tool-using LLM agent with clean tool schemas, a control loop, explicit stop conditions, and guardrails.
author: matrixx0070
tags: [agents, tool-use, control-loop, guardrails, planning]
---

## When to use

Use this when a task needs the model to take actions in a loop — call tools, observe results, decide the next step — rather than produce a single answer.

**Not for:** single-shot generation or classification (a plain prompt is cheaper and safer, see `ai-prompt-design`), or read-only Q&A over docs (see `ai-rag-pipeline`).

## Method

1. Decide if you even need an agent. Decision point: if the steps are known and fixed, write a deterministic pipeline; use an agent only when the path depends on runtime results.
2. Define tools as the narrowest useful set. Each tool: a clear name, a one-line description of WHEN to use it, and a typed input schema with required fields.
3. Write the system prompt: the goal, the available tools, how to decide between them, and when to stop.
4. Choose the control loop: call model → if tool_call, execute and append the result → repeat until a final answer or a stop condition fires.
5. Set hard stop conditions: max iterations, wall-clock/token budget, and a repeated-action detector. Decision point: on limit hit, return partial results with a reason, never loop silently.
6. Add guardrails: validate tool arguments before executing, require confirmation for destructive/irreversible actions, and sandbox side effects (see `ai-guardrails`).
7. Log every step (thought, tool, args, result) for replay and evaluation (see `ai-eval-harness`).

## Example

Agent: "find the failing test and summarize the cause."

```
loop (max 8 steps):
  resp = model(history, tools=[grep, read_file, run_tests])
  if resp.tool_call:
    if resp.tool == "run_tests" and !confirmed: ask_user()
    result = execute(validate(resp.tool_call))
    history += result
  else: return resp.text
```

Step 1 `grep "FAIL"` → test name. Step 2 `read_file` → source. Step 3 final summary. The max-8 cap and an "identical grep twice" detector prevent a loop when a tool returns empty.

## Pitfalls

- **Tool soup.** 20 overlapping tools; the model picks wrong. Fewer, sharper tools with distinct "when to use" lines.
- **No stop condition.** An agent that loops until the budget explodes. Always cap iterations AND detect repeats.
- **Unvalidated tool args.** Passing `"500"` where an int is required, or a path outside scope. Validate and coerce before executing.
- **Silent destructive actions.** Deleting or spending without a confirmation gate. Guard irreversible tools.

## Output format

```
# Agent: <name>
GOAL: <one sentence>
TOOLS:
- <name>(<typed args>): <when to use>
CONTROL LOOP: model -> tool -> observe -> repeat
STOP: max_steps=<n> | budget=<tokens/time> | repeat-detector
GUARDRAILS: arg validation | confirm-on={destructive} | sandbox
LOGGING: step{thought,tool,args,result}
```

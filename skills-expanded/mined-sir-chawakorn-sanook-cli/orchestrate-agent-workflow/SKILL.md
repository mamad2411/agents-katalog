---
name: orchestrate-agent-workflow
description: Designs reliable multi-step LLM agent loops — tool-call orchestration, state/memory between steps, explicit stop conditions, per-step verification, retries/replanning, subagent decomposition, and budget/approval gates — so an agent finishes long tasks without drifting or looping forever.
when_to_use: Building an agent that plans and calls tools across multiple steps, not a single prompt-and-response. Distinct from agent-tool-mcp-builder (designing the individual tools/MCP server), prompt-engineering (single-prompt/structured-output design), and harden-llm-app-reliability (transport-level retry/timeout of one model call).
---

## When to Use

Reach for this skill when the work spans **multiple model→tool→observe turns** under one goal:

- "Build an agent that researches, then drafts, then files a PR / ticket"
- "My agent loops forever / repeats the same tool call / never decides it's done"
- "It drifts off-task halfway through and starts solving a different problem"
- "Split this big task across subagents and stitch the results back together"
- "Add a cost/step cap and a human-approval gate before it deletes / deploys / pays"

NOT this skill:
- Designing the tool schemas / error shapes / MCP server the agent calls → agent-tool-mcp-builder
- Writing or hardening a single prompt or its JSON/function-call contract → prompt-engineering
- Making *one* model call survive timeouts/429s/5xx (retry, backoff, circuit breaker) → harden-llm-app-reliability
- Cutting token cost / latency of the model calls themselves (caching, model routing) → optimize-llm-cost-latency
- Treating tool output / web content as untrusted input → defend-llm-prompt-injection

## Steps

1. **Pick the simplest topology that works — escalate only when forced.** Default down this ladder, not up.

   | Pattern | Use when | Control flow | Failure mode to fear |
   |---|---|---|---|
   | **Single-agent tool loop** | One goal, <~15 steps, work fits one context | Model decides each next tool | Infinite loop / drift |
   | **Code-orchestrated workflow (DAG)** | Steps + order are known *ahead of time* | Your code sequences; model fills each node | Rigid; can't adapt mid-run |
   | **Multi-agent (planner + subagents)** | One context literally can't hold the work, or independent parallel branches | Orchestrator spawns sub-loops, merges summaries | Coordination cost, lost context at handoff |

   Start with the loop. Move to a coded DAG the moment the step graph is fixed (cheaper, deterministic, testable). Reach for multi-agent **only** when a single context window can't hold the task — never for "it feels big."

2. **Make the loop terminate — two independent kills.** Every loop needs BOTH a semantic stop and a hard cap. One alone is insufficient: the model's "I'm done" can be wrong, and a raw cap truncates good work.

   ```python
   MAX_STEPS, MAX_USD, t0 = 12, 0.50, time.time()
   for step in range(MAX_STEPS):                 # hard cap (anti-infinite-loop)
       msg = model(messages, tools)
       if msg.stop_reason == "end_turn":         # semantic stop: model emits final, no tool call
           return msg.text
       result = run_tool(msg.tool_call)          # exactly one tool per turn keeps it auditable
       messages += [msg, tool_result(result)]
       if spent_usd() > MAX_USD or time.time()-t0 > 120:   # budget / wall-clock guard
           return escalate("budget exceeded", messages)
   return escalate("max steps reached", messages)   # NEVER silently return partial as success
   ```
   Also detect a **no-progress loop**: hash `(tool_name, args)`; if the same call repeats ≥2× with no state change, break and replan — don't wait for MAX_STEPS.

3. **Carry state in an explicit scratchpad — not the raw message list.** The growing transcript is not memory; it's noise that costs tokens and dilutes the goal. Keep a small structured state object the loop reads/writes every turn:
   ```json
   {"goal": "<one immutable sentence>", "facts": [...], "open_questions": [...],
    "done": ["fetched X", "parsed Y"], "next": "draft summary", "artifacts": {"pr_url": null}}
   ```
   Re-inject `goal` + `next` into the prompt **every step** (anti-drift re-grounding). When the transcript grows large, summarize old turns into `facts`/`done` and drop the raw tool dumps — keep state, discard chatter.

4. **Verify each step's output before continuing — gate, don't trust.** After every tool result, check it actually advanced the goal *before* the model plans the next move. Cheapest sufficient check wins:
   - Schema/shape check on tool output (parses? non-empty? expected fields?) — pure code, no model.
   - Goal-relevance check: "does this result move us toward `goal`, or sideways?" If sideways → discard and re-ground, don't append it as progress.
   - For generated artifacts (code, SQL, configs): run the real check (compile/lint/`pytest`/dry-run), not a model's self-assessment. A failing check feeds back into the loop as a tool result.

5. **Retry then replan on tool failure — distinguish transient from logical.** Tool error ≠ retry-forever.
   - **Transient** (timeout, 429, 5xx): bounded retry with backoff — but that's transport reliability; delegate it to harden-llm-app-reliability, don't re-implement here.
   - **Logical** (bad args, "not found", validation reject): do **not** retry the identical call. Feed the error text back as an observation and let the model *replan* (fix args, pick another tool, or revise the plan). Cap replans (≤2) per subgoal; exceeding it → escalate, don't thrash.

6. **Decompose to subagents only when one context can't hold the work — and return summaries, not dumps.** A subagent gets a *narrow* objective, its own fresh context and tool subset, and returns a **compact result** (the answer + key facts + artifact refs), never its raw transcript. The orchestrator merges summaries into parent state. This is the whole point: parallel/large work happens in child contexts so the parent stays lean. If you find yourself piping a subagent's full message history back up, you've defeated it.

7. **Gate irreversible actions behind explicit approval; meter spend.** Classify each tool: read-only / reversible-write / **irreversible** (delete, deploy, send money, email customers, `DROP`). Irreversible tools require a human-approval checkpoint (or a strict policy allowlist) *before* execution — the loop pauses and surfaces the proposed action + args. Track cumulative tokens/$ per run (step 2's `MAX_USD`); a runaway agent is a billing incident. Emit a structured per-step trace (step #, tool, args, result-status, cost) so a stuck run is debuggable after the fact → build-audit-logging.

8. **Prove it on a multi-step harness with machine-checkable success criteria — built before you ship.** A loop that works on one happy-path demo proves nothing. Write the harness first: define each scenario's *success oracle* in code (artifact exists / `pytest` green / expected end-state reached / final answer matches a regex), not a model's "looks good." Cover ≥3 scenarios — one happy path, one designed-to-fail (asserts escalation, never an infinite loop), one with a distractor in tool output (asserts the goal held). Run it in CI on every change to the loop, prompt, or tool set; a passing harness is the only evidence the orchestration is reliable. Spec the checks in the Verify section below.

## Common Errors

- **Stop condition = only "model says done".** The model declares victory early or never. Always pair the semantic stop with a hard `MAX_STEPS` cap.
- **No max-step / max-cost cap.** One bad plan → infinite tool calls → runaway bill. Both caps are mandatory, and hitting them must escalate, not silently return a partial answer as if it succeeded.
- **Treating the message list as memory.** Relying on the growing transcript means the goal drowns in tool noise and context blows up. Keep an explicit scratchpad; re-inject the goal every step.
- **Never re-grounding → drift.** Without re-stating `goal` each turn, a long run quietly migrates to a neighboring task. Inject goal + next-action every step and discard off-goal results.
- **Retrying a logical error unchanged.** Re-sending the same bad args on a validation failure just burns steps. Transient → backoff retry; logical → replan with the error fed back as an observation.
- **Subagents returning raw transcripts.** Dumping a child's full history into the parent defeats decomposition and re-bloats the context you spun it off to avoid. Children return summaries + artifact refs only.
- **Multi-agent when a loop would do.** Coordination overhead, lost context at handoffs, and harder debugging — for work one context could have held. Escalate topology only when forced (step 1).
- **More than one tool call per turn without isolation.** Parallel tool calls in one turn make the trace ambiguous and ordering bugs invisible. Keep one tool per turn unless the calls are provably independent.
- **No verification between steps.** Appending an empty/erroring/irrelevant tool result as "progress" compounds garbage across the run. Gate every result before it enters state.
- **Irreversible action with no approval gate.** The agent deletes/deploys/pays on a hallucinated plan. Classify tools; pause for human approval on irreversible ones.
- **No per-step trace.** When a run gets stuck you have nothing to debug. Emit structured step records (tool, args, status, cost) from day one.

## Verify

1. **Terminates on success:** a happy-path multi-step task reaches the semantic stop and returns the artifact *before* `MAX_STEPS` — caps are a safety net, not the normal exit.
2. **Terminates on failure:** force an unsolvable goal → the run hits `MAX_STEPS`/`MAX_USD` and **escalates** (returns a clear "could not complete" + trace), never an infinite loop and never a partial dressed up as success.
3. **No-progress break:** inject a tool that returns the same value forever → the loop detects the repeated `(tool,args)` and breaks/replans within ≤2 repeats, not at MAX_STEPS.
4. **Anti-drift:** run a long task with a distractor in tool output → final answer still serves the original `goal`; the off-goal result was discarded, not built upon.
5. **Replan on logical error:** make a tool reject the first args → the agent fixes args / switches tool and proceeds, and does **not** re-send the identical failing call.
6. **Budget guard:** set `MAX_USD` low → the run halts and escalates when spend exceeds it; cumulative cost in the trace matches actual usage.
7. **Approval gate:** an irreversible tool is never executed without the approval checkpoint firing first (assert it pauses and surfaces args).
8. **Subagent isolation:** parent context size after a subagent task stays bounded — the child returned a summary, not its transcript (check token count, not just correctness).
9. **Harness:** ≥3 multi-step scenarios with machine-checkable success criteria (artifact exists / check passes / expected state reached) run green in CI, including at least one designed-to-fail case from check 2.

Done = on the multi-step harness the agent finishes happy-path tasks via the semantic stop, every failure/runaway path escalates within the step+budget caps (no infinite loops, no partial-as-success), each step is verified and re-grounded on the goal, irreversible actions are gated, and subagents return summaries — all evidenced by the per-step trace.

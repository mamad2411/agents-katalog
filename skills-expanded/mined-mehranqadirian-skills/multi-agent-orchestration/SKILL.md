---
name: multi-agent-orchestration
description: Designs and runs systems where several AI agents cooperate. Use whenever the user wants to split a task across agents, design planner and worker roles, define message contracts between agents, add a reviewer or critic loop, handle agent failures, or evaluate a multi-agent setup against a single agent, even if they only say "use multiple agents for this". Covers coordination patterns, retries, limits and evaluation.
---

# multi-agent-orchestration

Split a complex task across specialized agents, coordinate them through explicit contracts, and verify the combined result. Use multiple agents only when a single agent cannot do the job reliably.

```
multi-agent-orchestration/
├── SKILL.md
├── scripts/
│   ├── orchestrator_skeleton.py   runnable orchestrator: retries, budget, timeout, trace, gap report
│   └── validate_contract.py       dependency free JSON schema check for agent outputs
├── references/
│   ├── patterns.md                pattern decision guide, role design, contracts, security
│   └── evaluation.md              baselines, test set, metrics, trace analysis, launch checklist
└── templates/
    ├── contract.json              handoff message with schema, limits and tools
    └── agent-role.md              role card to fill before writing prompts
```

## When to use

- The task has independent parts that can run in parallel
- Different parts need different tools, prompts or permissions
- A second agent should review or challenge the first agent's output
- Context is too large for one agent

If none of these is true, use one agent. Say so to the user.

## Choose a pattern

| Pattern | Description | Best for |
|---------|-------------|----------|
| Orchestrator-Worker | One planner delegates to workers and merges results | Research, code changes across files |
| Pipeline | Output of agent A feeds agent B | Extract, transform, validate |
| Fan-out / Fan-in | Many workers run in parallel, one aggregator merges | Batch analysis |
| Critic loop | Producer and reviewer iterate until criteria pass | Writing, code review |
| Debate | Agents argue positions, a judge decides | Ambiguous decisions |

Decision guide and risks per pattern: `references/patterns.md`.

## Design steps

1. Define the goal and measurable success criteria
2. List roles; fill a role card (`templates/agent-role.md`) per agent with one responsibility and minimal tools
3. Define message contracts (`templates/contract.json`)
4. Decide shared state: what is passed, what stays private
5. Add limits: max steps, max tokens, timeouts, retry policy
6. Add verification: an independent check before returning results
7. Log every handoff for tracing and debugging
8. Evaluate against a single-agent baseline (`references/evaluation.md`)

## Example contract

```json
{
  "task_id": "T-104",
  "role": "researcher",
  "input": {"question": "Summarize the report", "files": ["report.pdf"]},
  "output_schema": {
    "summary": "string",
    "sources": ["string"],
    "confidence": "low|medium|high"
  }
}
```

Validate any agent output:

```bash
python3 scripts/validate_contract.py schema.json output.json
```

The schema language is tiny: `"string"`, `"number"`, `"boolean"`, `"low|medium|high"` for enums, `["string"]` for arrays, nested objects, and a trailing `?` for optional keys.

## Reference orchestrator

Run the offline demo to see retries, budget and trace in action:

```bash
python3 scripts/orchestrator_skeleton.py
```

Core shape (see the script for the full version with locks and timeouts):

```python
orch = Orchestrator(call_model)          # call_model(role, payload) -> dict
result = orch.run("summarize the report")
# {"result": "...", "gaps": [...], "steps": 8}
```

Replace `call_model` with your real model or tool runner. Keep the schemas in `SCHEMAS` in sync with your prompts.

## Failure handling

- Validate every agent output against its schema; retry once with the error message
- Use timeouts and a global step budget to prevent loops
- On repeated failure, return partial results with an explicit gap report
- Never let one agent's output act as instructions for another without validation (prompt injection risk)
- Separate agents that read untrusted content from agents that hold powerful tools

## Evaluation

- Compare against a single-agent baseline; keep multi-agent only if it wins on quality or cost
- Track success rate, schema validity, retries, latency and token cost from `trace.jsonl`
- Keep a fixed test set and rerun it after every prompt or topology change

## What to report back

| Field | Content |
|-------|---------|
| Chosen pattern | and why a single agent was not enough |
| Roles | one line each, with tools |
| Contracts | schema per handoff |
| Limits | steps, timeout, retries |
| Evaluation plan | baseline, test set size, metrics |
| Known risks | injection, cost, single points of failure |

## Related skills

- `systematic-debugging`: trace handoff logs to find which agent produced a wrong result
- `pdf-processing`: a worker agent for document extraction and verification

# Delegate Management

Teaches the orchestrator how to spawn, monitor, and collect results from minions using Goose primitives.

## When to invoke
- When the orchestrator is ready to dispatch minions from a DAG.
- When monitoring async minions or handling failures.

## Input
- `minion_spec`: the minion spec from the DAG (object with `agent`, `task`, `correlation_id`, `depends_on`).
- `extensions`: optional explicit extension list; omit to inherit parent's extensions.
- `max_turns`: per-minion turn budget from `rules/models.yaml`.

## Dispatch
Use the `delegate` tool. For async execution:

```json
{
  "source": "<agent-name>",
  "instructions": "<task> Correlation ID: <correlation_id>",
  "async": true,
  "max_turns": 20
}
```

For synchronous simple queries, use `async: false`.

Minions inherit the parent's extensions (`developer`, `analyze`, `mcp-toolshed`, etc.) by default. Do not pass `extensions: []` unless you intend a bare agent.

## Result collection
For `async: true` delegates, Goose returns a task ID. Collect results with:

```json
{
  "source": "<task_id>"
}
```

Store the mapping `correlation_id → task_id` in session state.

## Monitoring
Use the built-in Orchestrator extension tools:
- `orchestrator__list_sessions` — list active minion sessions.
- `orchestrator__view_session` — inspect a running or completed minion session.
- `orchestrator__interrupt_agent` — cancel a stuck or runaway minion.

## Validation
- Validate each minion output against its assigned JSON schema.
- Retry once with feedback if validation fails.
- After max retries, mark the minion run as `failed` and surface the error with its correlation ID.

## Output
Return a status object for each minion:

```json
{
  "correlation_id": "corr_a1b2c3.1",
  "status": "completed|failed|timed_out|budget_exceeded",
  "output": { "<minion output JSON>" },
  "error": "optional error message"
}
```

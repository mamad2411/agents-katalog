---
name: subagent-spawn
description: Use this skill when manually delegating from a workflow or building a custom orchestrator — a typed delegation helper that constructs a valid G7 spawn payload for a chosen role, validates against role-selection-table.md and the spawn-payload schema, and returns a fully-formed Agent(...) call ready for orchestrator use.
context: fork
argument-hint: "--role <role> [--task '<text>'] [--stack <stack>]"
---

# /subagent-spawn — G7 Spawn Payload Helper

Constructs a typed spawn payload conforming to `plugin/schemas/spawn-payload.schema.json` for a chosen role. Used internally by orchestrator skills (`/develop`, `/feature-design`, `/team-bugfix`); also available standalone for power users building custom workflows.

## When to use

- Inside a custom orchestrator skill where you need a standardized G7 spawn payload
- When debugging a subagent spawn — build the payload manually, inspect it before invoking
- When testing a single agent role against a small task without the full workflow overhead

Not for: routine agent invocation (use the orchestrator skill); bypassing role-selection-table (use the table directly).

## Invocation

```
/subagent-spawn --role frontend-engineer --task "implement OAuth2 login form per src/auth/spec.md"
/subagent-spawn --role security-engineer --task "audit src/api/auth.ts" --max-tokens 30000
/subagent-spawn --role db-engineer --task "design schema migration" --stack postgres
```

## Arguments

| Flag | Default | Effect |
|---|---|---|
| `--role <name>` | required | Plugin agent name (one of 26) — validated against `plugin/agents/` |
| `--task '<text>'` | required | The `goal` field of the G7 spawn payload (10–1000 chars) |
| `--stack <name>` | auto | Hint for role-selection-table (e.g., `postgres`, `react`, `terraform`) |
| `--max-tokens N` | 50000 | `budget.max_input_tokens` cap |
| `--max-output N` | from agent frontmatter | `budget.max_output_tokens` (default per agent's `max_output_tokens` field) |
| `--max-tool-calls N` | 30 | `budget.max_tool_calls` |
| `--max-turns N` | from agent frontmatter | `budget.max_turns` (default per agent's `maxTurns` field) |
| `--timeout-ms N` | 600000 (10 min) | `budget.timeout_ms` |

## Behavior

1. Validate `--role` against `plugin/agents/<name>.md`. If not found, error with full list.
2. Look up agent frontmatter (`tools`, `max_output_tokens`, `maxTurns`, `disallowedTools`) for default budget values.
3. Generate `trace_id`: format `wf-<YYYYMMDD>-<random6>-spawn-<seq>` (per `spawn-payload.schema.json` pattern).
4. Construct G7 payload:

```json
{
  "trace_id": "wf-20260427-abc123-spawn-001",
  "parent_trace_id": null,
  "subagent_role": "<role>",
  "goal": "<task>",
  "constraints": [],
  "state_slice": {},
  "allowed_tools": [<from agent frontmatter tools field>],
  "budget": {
    "max_input_tokens": <flag or default>,
    "max_output_tokens": <flag or agent frontmatter>,
    "max_tool_calls": <flag>,
    "max_turns": <flag or agent frontmatter>,
    "timeout_ms": <flag>,
    "retry_budget": 1
  },
  "untrusted_inputs": []
}
```

5. Validate the payload against `plugin/schemas/spawn-payload.schema.json` (best-effort; warn if validator unavailable).
6. Return the payload as JSON for the orchestrator to wrap in an `Agent(...)` call:

```
{
  "agent_call": "Agent({subagent_type: '<role>', name: '<role>-<seq>', prompt: '<task brief with G7 payload embedded>'})",
  "spawn_payload": <json>,
  "validation": "ok | warnings: [<list>]"
}
```

## Hard rules

- **Role lookup is strict** — only the 26 plugin-shipped agents (`plugin/agents/<name>.md`) plus built-in Claude Code agents (`Explore`, `Plan`, `general-purpose`) are valid `subagent_role` values per `team-protocols/role-selection-table.md`
- **Budget defaults from agent frontmatter** — never invent budgets; use the role-type table values per glossary §3
- **Untrusted inputs flagged** — if the orchestrator passes any L0/L2/L4/tool/subagent content to populate `state_slice`, populate `untrusted_inputs` with `wrapped: true` per `untrusted-content-wrapping.md` rule
- **No actual spawn here** — this skill BUILDS the payload; the orchestrator INVOKES `Agent(...)` separately. Single-responsibility
- **`parent_trace_id` for nested spawns** — if THIS spawn is being initiated from inside another subagent (rather than the main thread), the orchestrator MUST set `parent_trace_id` to the parent's `trace_id`. Omit or set to null for top-level spawns. The `subagent-depth-guard.py` hook (v0.1.7) walks this chain to enforce `userConfig.subagent_max_depth` (default 3); a missing `parent_trace_id` on a nested spawn defeats depth tracking and the hook may underreport the actual depth.

## Failure modes

- **Invalid role:** error with full list of 26 valid agent names + 3 built-in agents
- **`--task` too short or too long:** reject with the schema's minLength/maxLength bounds (10–1000 chars)
- **Budget conflicts with agent frontmatter caps:** if `--max-tokens` exceeds 200000 or `--max-output` exceeds agent's documented cap, reject with explanation
- **Role exists but `tools:` field empty:** warn; suggest reviewing agent frontmatter

## Memory writes

This skill is **read-only** — no memory writes. The orchestrator that subsequently invokes `Agent(...)` is responsible for recording the spawn via `subagent-start-budget.py` hook.

## Integration

- **Reads**: `plugin/agents/<role>.md` frontmatter for defaults
- **Validates against**: `plugin/schemas/spawn-payload.schema.json` (G7), `team-protocols/role-selection-table.md`
- **Rules**: `subagent-isolation` (delegation patterns + bounded recursion + Phase 4 #4 depth guard), `untrusted-content-wrapping` (G1 on `untrusted_inputs` field)
- **Hooks**: `subagent-start-budget` (token cap), `subagent-depth-guard` (max recursion depth via `parent_trace_id` chain, v0.1.7), `subagent-stop-learnings` (return-contract validation + chain closure)
- **Used by**: `/feature-design`, `/develop`, `/team-bugfix`, `/refactor`, `/migrate` orchestrators; available standalone
- **Companion**: `/context-load` (constructs `state_slice` content for the spawn payload)

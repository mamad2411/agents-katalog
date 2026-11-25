---
name: agents-sdk
description: Builds, deploys, and maintains stateful AI agents on Cloudflare Workers and Durable Objects using the Cloudflare Agents SDK. Use when creating stateful agents, implementing RPC methods with @callable(), configuring SQLite-backed agent state, orchestrating agent workflows, running durable fibers, managing chat agents, or handling agent webhooks and schedules.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, wrangler_deploy, execute_command]
---

# Agents SDK

Build, deploy, and maintain stateful AI agents on Cloudflare Workers and Durable Objects using the Cloudflare Agents SDK (`agents` package).

Your knowledge of the Agents SDK and Cloudflare runtime APIs may be outdated. **Prefer retrieval over pre-training** for any Agents SDK task.

## When to Use

- creating stateful AI agents on Cloudflare Workers + Durable Objects
- exposing type-safe agent RPC interfaces using the `@callable()` decorator
- persisting agent state and conversation history in embedded SQLite (`this.sql`)
- orchestrating durable multi-step execution with `AgentWorkflow`
- running resilient background tasks via fibers (`this.runFiber()`)
- building interactive chat agents with streaming using `AIChatAgent`
- scheduling recurring or delayed agent actions (`schedule()`, `scheduleEvery()`)
- handling incoming agent webhooks and push notifications

## Core Rules

- **RETRIEVAL-FIRST**: Always verify API signatures against current Cloudflare Agents documentation (`https://developers.cloudflare.com/agents/`).
- **STATEFUL-SUBSTRATE**: Extend `Agent` or `AIChatAgent` backed by Durable Objects SQLite; declare migrations in `wrangler.jsonc` via `new_sqlite_classes`.
- **RPC-EXPOSURE**: Expose agent callable methods explicitly with `@callable()`; reject raw untyped HTTP endpoints for internal agent communication.
- **SQLITE-PERSISTENCE**: Use `this.sql.exec(...)` for structured entity storage and `this.setState(...)` for state transitions; never store mutable state only in memory.
- **DURABLE-EXECUTION**: Use `this.runFiber(...)` for long-running operations across disconnects, and `AgentWorkflow` for multi-step resilient pipelines.
- **DETERMINISTIC-ROUTING**: Access agent instances via `env.Agent.getByName(id)` for deterministic entity binding.
- **OBSERVABILITY-MANDATE**: Always enable dual observability in `wrangler.jsonc`: `"observability": { "enabled": true, "traces": { "enabled": true } }`.
- **TYPES-SYNC**: Run `wrangler types` after adding agent bindings or migrations; never hand-write agent environment types.

## Retrieval Sources

| Source | Target URL | Use for |
| :--- | :--- | :--- |
| Cloudflare Agents Docs | `https://developers.cloudflare.com/agents/` | SDK overview, agent lifecycle, APIs |
| Agents GitHub Repo | `https://github.com/cloudflare/agents` | SDK code, types, examples, releases |
| Durable Objects Docs | `https://developers.cloudflare.com/durable-objects/` | Storage, SQLite engine, RPC bindings |
| Wrangler Config Schema | `node_modules/wrangler/config-schema.json` | Binding syntax, migrations, placement |

## Suggested Process

1. Install `@cloudflare/agents` and configure `wrangler.jsonc` with DO binding and `new_sqlite_classes` migration.
2. Define the agent class extending `Agent<Env>` or `AIChatAgent<Env>`, implementing schema setup in constructor if needed.
3. Decorate client-accessible methods with `@callable()` and implement state mutations via `this.setState()` and `this.sql.exec()`.
4. Implement background tasks or multi-step execution using `this.runFiber()` or `AgentWorkflow`.
5. Connect routing in the Worker `fetch()` handler using `routeAgentRequest(request, env)` or `env.MY_AGENT.getByName(id)`.
6. Run `wrangler types` to regenerate TypeScript declarations, verify locally with `wrangler dev`, and deploy.

## Checklist

- [ ] Agent class extends `Agent` or `AIChatAgent` and is exported from the Worker module.
- [ ] Durable Object binding and `new_sqlite_classes` migration are declared in `wrangler.jsonc`.
- [ ] Callable RPC methods are explicitly decorated with `@callable()`.
- [ ] Persistent state uses `this.sql.exec()` or `this.setState()`, not isolated memory variables.
- [ ] Dual observability (`observability.enabled` and `observability.traces.enabled`) is configured in `wrangler.jsonc`.
- [ ] Long-running asynchronous tasks utilize `runFiber()` or `AgentWorkflow` to prevent premature eviction.
- [ ] TypeScript types are updated via `wrangler types` and build passes with zero errors.

## Output Contracts

When this skill is invoked to plan or implement an agentic deployment, emit:

- **`contracts/schemas/edge-deployment-spec.json`** — capture the agent Durable Object bindings, SQLite migration tags, scheduling parameters, observability configuration, and rollback strategy. Set `produced_by_role` to `cloudflare-engineer`.

## Failure Modes

- **In-memory state loss**: storing agent conversation or task status in instance variables without calling `this.setState()` or `this.sql.exec()`; state evaporates upon isolate eviction. Mitigation: persist every state transition immediately.
- **Unprotected callable methods**: omitting `@callable()` on RPC methods prevents external or cross-worker invocation, while exposing private helpers unintentionally. Mitigation: review decorated methods explicitly.
- **Zombie fibers & unbounded loops**: launching fibers with unbounded loops without persistence or timeout checks. Mitigation: add step limits, checkpoints, and backoff handling inside `runFiber()`.
- **Missing SQLite migration**: declaring an Agent class without adding `new_sqlite_classes` to `migrations` in `wrangler.jsonc`. Mitigation: ensure migration tag is added and run `wrangler types`.
- **Destructuring agent context**: destructuring `this.ctx` or `env` in ways that detach Cloudflare runtime bindings. Mitigation: call methods directly on `this` or `this.ctx`.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: agent prompt inputs and webhook payloads must be validated against strict schemas before driving agent fibers or state changes.
- **ASI03 Identity & Privilege Abuse**: authenticate callers before dispatching to `@callable()` methods; enforce tenant-level authorization checks per agent instance.
- **ASI05 RCE & Injection Guard**: always use parameterized queries with `this.sql.exec(query, ...params)`; never concatenate untrusted strings into SQL statements.
- **ASI07 Inter-Agent Communication**: validate all cross-agent messages using formal schemas when coordinating between multiple Agent instances.
- **ASI10 Unbounded Resource Consumption**: set token budgets and execution step limits on agent loops and fibers to prevent runaway billing.

## Related Skills

- **wrangler**: Configure agent bindings, SQLite migrations, and deploy agents to Cloudflare.
- **durable-objects**: Core underlying stateful coordination, RPC, and SQLite engine.
- **workers-best-practices**: General async execution, memory hygiene, and observability standards.
- **setup-llm-gateway**: Route agent LLM calls through centralized AI Gateway for token budgeting.

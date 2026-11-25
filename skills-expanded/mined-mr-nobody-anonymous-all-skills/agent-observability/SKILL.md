---
name: agent-observability
description: "Instrument agent runs: trace structure for tool calls and model turns, token and cost accounting, latency budgets, and searchable logs that explain a bad answer."
type: procedural
category: agents
domain: agents
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - trace agent tool calls
  - agent token cost tracking
  - agent latency budget
  - log llm agent run
  - debug agent failure
aliases:
  - agent-tracing
keywords:
  - observability
  - tracing
  - spans
  - tokens
  - cost
  - latency
  - agent
mcp_servers:
  - opentelemetry
  - grafana
  - sentry
source: custom
enabled: true
---

# Agent Observability

## Purpose

Instrument agent runs: trace structure for tool calls and model turns, token and cost accounting, latency budgets, and searchable logs that explain a bad answer.

## When to Use

- An agent produced a wrong answer and nobody can reconstruct why.
- Spend or latency is climbing and the cause is unknown.
- Multiple agents collaborate and the handoffs are invisible.

## When NOT to Use

- The system is single-call with no tools.
- Logging PII into a third-party tracer would violate policy.
- The problem is already isolated to one function.

## Capabilities

- Model a run as a trace: one root span, a span per model turn and tool call.
- Record token counts, model, cost and tool arguments with redaction.
- Set latency budgets per span and alert on the p95, not the average.
- Correlate runs to user requests and releases.
- Reconstruct a failed run from stored spans alone.

## Inputs

- The agent's execution model and where the boundaries are.
- A tracing backend and its retention policy.
- The privacy rules for prompts, tool payloads and outputs.

## Workflow

1. Define span names and attributes once, and use them everywhere.
2. Attach run id, user id (hashed), model, and prompt version to the root span.
3. Wrap every tool call in a span with its arguments redacted and its result size.
4. Emit token and cost metrics; aggregate per run and per release.
5. Alert on p95 latency and error rate, not on single slow runs.
6. Practice reconstruction: take a real bad answer and explain it from spans only.

## Tools

- opentelemetry
- grafana
- sentry
- prometheus
- jaeger

## Examples

- `A root span per run plus one span per tool call turns 'it sometimes fails' into 'the third retry on search times out'.`
- `Tagging prompt version on the root span is what lets you attribute a quality drop to a prompt change.`

## Safety

- Redact prompts and tool payloads by default; opt in per field, not per system.
- Retention limits are a privacy control, not a storage optimisation.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `opentelemetry` | stdio | full | medium | `BACKEND_TYPE`, `BACKEND_URL` |
| `grafana` | stdio | full | medium | `GRAFANA_URL`, `GRAFANA_API_KEY` |
| `sentry` | http | standard | medium | `SENTRY_ACCESS_TOKEN` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/agents/agent-observability`). First-party skill, maintained in this repository.

## Notes

- Trace ids must appear in application logs or correlation is guesswork.
- Cost per successful task is the metric that matters, not cost per call.
- Pairs with: `agent-reliability`, `mcp-integration-testing`.

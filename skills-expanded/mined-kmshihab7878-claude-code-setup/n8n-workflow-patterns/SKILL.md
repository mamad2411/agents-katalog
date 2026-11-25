---
name: n8n-workflow-patterns
description: Proven workflow architectural patterns from real n8n workflows. Use when building new workflows, designing workflow structure, choosing workflow patterns, planning workflow architecture, or asking about webhook processing, HTTP API integration, database operations, AI agent workflows, or scheduled tasks.
---

# n8n Workflow Patterns

Proven architectural patterns for building n8n workflows.

## When to use

- Building a new n8n workflow from scratch.
- Designing or reviewing workflow structure.
- Choosing among the five core patterns.
- Planning error handling, retries, or async strategies.
- Asking about webhook, HTTP API, database, AI agent, or scheduled patterns.
- Resolving pattern-related gotchas (data nesting, branch loss, timeouts).

## Required input contract

Before designing or recommending a workflow, identify:

- **Trigger** — webhook, schedule, manual, or service trigger.
- **Primary data flow** — what enters, what leaves, what is transformed.
- **External systems** — APIs, databases, message brokers, AI models.
- **Latency budget** — does the upstream caller need a synchronous response?
- **Failure tolerance** — silent retry, dead-letter queue, alerting, or human review.
- **Cadence / volume** — items per execution and executions per hour.

If a strategic decision is missing, ask one sharp question before drafting
the workflow.

## The 5 core patterns

| # | Pattern | Trigger | Shape |
|---|---------|---------|-------|
| 1 | Webhook Processing | Webhook (HTTP) | Webhook → Validate → Transform → Respond / Notify |
| 2 | HTTP API Integration | Manual / Schedule | Trigger → HTTP Request → Transform → Action → Error Handler |
| 3 | Database Operations | Schedule | Schedule → Query → Transform → Write → Verify |
| 4 | AI Agent Workflow | Webhook / Manual | Trigger → AI Agent (Model + Tools + Memory) → Output |
| 5 | Scheduled Tasks | Schedule (cron) | Schedule → Fetch → Process → Deliver → Log |

Detailed catalog with use cases per pattern: `references/workflow-pattern-catalog.md`.
Upstream depth: `webhook_processing.md`, `http_api_integration.md`,
`database_operations.md`, `ai_agent_workflow.md`, `scheduled_tasks.md`.

## Pattern selection (decision logic)

Decide in this order:

1. **External HTTP call starts the workflow?** → Webhook Processing.
2. **Workflow runs on a clock?** → Scheduled Tasks.
3. **Primary action is fetching from an external API on demand?** → HTTP API Integration.
4. **Workflow moves rows between data stores?** → Database Operations.
5. **Requires multi-step reasoning or tool use?** → AI Agent Workflow.

A workflow may blend patterns — the **trigger** names the primary pattern.

Full pattern-selection guide + workflow creation checklist:
`references/pattern-selection-workflow.md`.

## Node orchestration constraints

These rules apply to every workflow.

1. **Sequential by default.** Parallelism is opt-in via branching + Merge.
2. **Merge after IF / Switch.** Each branch must merge or terminate
   independently — without Merge, only one branch reaches downstream.
3. **Split In Batches when N > ~500.** Caps load on downstream services.
4. **Error Trigger is workflow-level.** It connects to nothing in the main
   flow; it fires when any node fails.
5. **Continue On Fail is per-node.** Use only where downstream tolerates
   silent failure.
6. **Webhook response must be fast.** Long work goes into a follow-on
   workflow with a `202 Accepted` handoff.
7. **Credentials live in n8n credential storage**, never in node parameters
   or code.
8. **Execution Order = v1 (connection-based)**. v0 (top-to-bottom) only for
   documented legacy reasons.
9. **AI agents can only use connected tools.** Tools that are not wired
   cannot be discovered or invoked by the agent.

## Common building blocks (compact)

| Role | Nodes |
|------|-------|
| Triggers | Webhook, Schedule, Manual, Polling |
| Data sources | HTTP Request, Postgres / MySQL / MongoDB, Service nodes, Code |
| Transformation | Set, Code, IF / Switch, Merge |
| Outputs | HTTP Request, Database, Communication (Email / Slack / Discord), Storage |
| Error handling | Error Trigger, IF (error condition), Stop and Error, Continue On Fail |

Full per-component detail, data flow shapes (linear / branching / parallel /
loop / error-handler), and quick-start templates:
`references/node-orchestration-and-templates.md`.

## Validation gates

Before activating a workflow:

- [ ] Each node validated via `validate_node({nodeType, config})`.
- [ ] Full workflow validated via `validate_workflow`.
- [ ] Credentials configured at the node level, not in parameters.
- [ ] Webhook response strategy chosen; long work split off.
- [ ] Error Trigger workflow exists for production workflows.
- [ ] `Continue On Fail` only where silent failure is acceptable.
- [ ] Sample-data run executed; empty-data path tested.
- [ ] Execution Order = v1.
- [ ] Workflow name + notes describe purpose and data flow.

Run `n8n_autofix_workflow` after `validate_workflow` reports issues, then
re-validate. Full gotcha catalog, anti-patterns, QA playbook:
`references/error-handling-and-validation.md`.

## Output expectations

When delivering a workflow design or recommendation:

- Name the primary pattern.
- List the trigger and all nodes in order.
- Mark each branch boundary (IF / Switch / Merge).
- Note any Split In Batches and the batch size.
- State the error-handling strategy (Error Trigger, Continue On Fail, retries).
- Specify the response strategy for webhook patterns.
- Flag any pattern blend explicitly (e.g., "Scheduled Task with HTTP API secondary").

## Minimal critical examples

### Webhook → Slack

```
1. Webhook (path: /form-submit, POST)
2. Set (map form fields)
3. Slack (post to #notifications)
```

### Scheduled report

```
1. Schedule (daily 09:00)
2. HTTP Request (fetch analytics)
3. Code (aggregate)
4. Email (send report)
5. Error Trigger → Slack (failure)
```

### AI assistant

```
1. Webhook (/chat)
2. AI Agent
   ├─ ai_languageModel: OpenAI Chat Model
   ├─ ai_tool: HTTP Request Tool
   ├─ ai_tool: Database Tool
   └─ ai_memory: Window Buffer Memory
3. Webhook Response
```

End-to-end worked examples (Stripe ingest, GitHub→Jira, DB sync, AI bot,
analytics report, 202-async, branching+merge, cursor loop):
`references/examples.md`.

## Integration with other skills

| Phase | Skill |
|-------|-------|
| Find nodes for the pattern | `n8n-mcp-tools-expert` (`search_nodes`) |
| Understand node operations | `n8n-mcp-tools-expert` (`get_node`) |
| Write expressions | `n8n-expression-syntax` (`{{ }}`, webhook nesting) |
| Configure operations | `n8n-node-configuration` |
| Custom logic | `n8n-code-javascript` or `n8n-code-python` |
| Validate and auto-fix | `n8n-validation-expert` (`validate_workflow`, `n8n_autofix_workflow`) |
| Create and deploy | `n8n-mcp-tools-expert` (`n8n_create_workflow`, `activateWorkflow`) |

## Reference map

| Need | Read |
|------|------|
| Pattern selection guide + workflow creation checklist + pattern statistics | `references/pattern-selection-workflow.md` |
| Five-pattern catalog + blend decision rules + anti-blend cases | `references/workflow-pattern-catalog.md` |
| Common components, data-flow shapes, orchestration rules, quick-start templates | `references/node-orchestration-and-templates.md` |
| Validation gates, common gotchas, anti-patterns, QA playbook | `references/error-handling-and-validation.md` |
| End-to-end worked examples (all 5 patterns + 3 blends) | `references/examples.md` |
| Upstream depth (per pattern) | `webhook_processing.md`, `http_api_integration.md`, `database_operations.md`, `ai_agent_workflow.md`, `scheduled_tasks.md` |

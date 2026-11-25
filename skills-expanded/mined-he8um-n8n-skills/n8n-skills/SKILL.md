---
name: n8n-skills
description: professional n8n workflow architecture and importable workflow json generation for ai agents. use when a user asks to design, build, audit, refactor, document, troubleshoot, or harden n8n workflows; produce import-ready workflow json, markdown specs, node graphs, api/webhook integration plans, credential-safe patterns, retries, error handling, observability, queue-mode guidance, and production runbooks.
---

# n8n Skills

## Core Directive

Act as a senior n8n workflow architect and automation reliability engineer. Design workflows that are importable, maintainable, observable, credential-safe, idempotent, and understandable by both humans and agents.

Prefer concrete deliverables over generic explanation. For build requests, produce both:

1. a readable Markdown implementation spec, and
2. an import-oriented n8n workflow JSON block or artifact when the user asks for a workflow that can be imported.

Never include real credentials, API keys, bearer tokens, session cookies, private hostnames, production webhook secrets, or personal data in generated workflow JSON. Use placeholders and credential names.

## Operating Modes

Choose the mode from the user's request:

- **Design mode**: produce architecture, node graph, data contract, retry/error strategy, credential map, and import JSON plan.
- **Import JSON mode**: produce n8n workflow JSON intended for direct import, plus setup steps and validation notes.
- **Audit mode**: inspect supplied workflow JSON or description; identify structural, security, reliability, performance, and maintainability issues.
- **Troubleshooting mode**: diagnose execution failures, expression errors, webhook issues, credentials, data item shape issues, loop/merge mistakes, and API failures.
- **Refactor mode**: split large workflows into sub-workflows, remove duplication, standardize naming, add observability and error paths.
- **Integration mode**: design HTTP/API/webhook/data-sync workflows with pagination, rate limits, idempotent upsert, reconciliation, logging, and dead-letter handling.
- **AI workflow mode**: design LLM/agent workflows with bounded autonomy, structured outputs, human approval gates, prompt-injection defenses, and tool-call constraints.

## Progressive Reference Loading

Load only the relevant reference files:

- For workflow architecture and production design: `references/n8n-workflow-architecture.md`.
- For importable JSON generation: `references/importable-json-standard.md` and `references/output-templates.md`.
- For nodes, triggers, expressions, data shapes, branching, loops, and merges: `references/nodes-data-and-expressions.md`.
- For credentials, secrets, permission boundaries, and safe sharing: `references/security-credentials-and-governance.md`.
- For errors, retries, observability, logging, and runbooks: `references/error-handling-observability.md`.
- For API, webhook, sync, pagination, and integration patterns: `references/integrations-api-webhooks.md`.
- For AI agent, LangChain, MCP, human-in-the-loop, and evaluation workflows: `references/ai-agent-workflows.md`.
- For self-hosted scaling, queue mode, concurrency, performance, and binary data: `references/scaling-and-self-hosting.md`.
- For audits and QA: `references/audit-checklists.md`.
- For common failures and fixes: `references/troubleshooting-playbook.md`.
- For source grounding and community-derived patterns: `references/source-notes.md`.

## Required Output Contract

For any substantive workflow design, include these sections unless clearly unnecessary:

1. **Intent** — what the workflow must do and what it must not do.
2. **Assumptions** — explicit defaults used because the user did not provide every detail.
3. **Workflow graph** — trigger, processing, branches, external systems, storage/logging, notifications.
4. **Node table** — node name, node type, purpose, key parameters, credentials needed, failure behavior.
5. **Data contract** — input JSON shape, intermediate item shape, output JSON shape, required keys, optional keys.
6. **Credential map** — credential names only, no secret values.
7. **Error and retry strategy** — transient vs permanent failures, backoff, dead-letter, alerting.
8. **Idempotency strategy** — stable keys, dedupe, upsert, replay safety.
9. **Import-ready JSON** — only when requested or useful; make it credential-safe.
10. **Setup steps** — credentials, environment variables, webhook URL, manual test payloads, activation notes.
11. **Validation checklist** — import, first manual run, edge cases, security checks.

## Import JSON Rules

When generating n8n JSON:

- Output a single valid JSON object unless the user asks for multiple workflows.
- Use top-level keys compatible with n8n workflow exports: `name`, `nodes`, `connections`, `settings`, and optional `pinData`, `tags`, `meta`, `versionId`.
- Set `active` to `false` unless the user explicitly asks for active workflows.
- Use deterministic node names and unique IDs.
- Keep every node position as a two-number array.
- Do not include encrypted credential payloads. If a node needs credentials, include the credential reference shape only when the exact credential type is known; otherwise document it in the credential map and use placeholder names.
- Prefer built-in core nodes for portable examples: Manual Trigger, Webhook, Respond to Webhook, HTTP Request, If, Switch, Set/Edit Fields, Code, Merge, Split in Batches / Loop Over Items, Wait, Stop and Error, Execute Workflow, Error Trigger, Schedule Trigger.
- Include sticky notes when they improve operator handoff, but do not rely on notes as the only documentation.
- If a workflow depends on instance-specific node versions, mark this in setup notes and explain that the user should verify node typeVersion in their n8n instance.
- If uncertain about a node's exact parameter schema, say so and provide a safe blueprint JSON plus manual setup instructions rather than fabricating a brittle import.

## Validation Scripts

Use bundled scripts when useful:

- `scripts/validate_n8n_workflow_json.py <workflow.json>` validates core import-shape issues, connections, duplicate names, dangerous secrets, and common reliability gaps.
- `scripts/validate_workflow_blueprint_json.py <blueprint.json>` validates the higher-level agent blueprint schema used before producing import JSON.

Run validators before returning generated JSON files when creating artifacts in a runtime environment.

## Quality Bar

Reject shallow workflows. A professional n8n deliverable should show:

- named nodes and explicit responsibilities,
- clear item contracts between nodes,
- credential-safe placeholders,
- retry and rate-limit behavior for external APIs,
- dedupe/upsert keys where writes occur,
- execution logging and human-readable summaries,
- failure classification and recovery path,
- import instructions and test payloads,
- security notes for webhook, code, AI, and external API boundaries.

## Safe Defaults

Use these defaults unless the user says otherwise:

- workflow `active`: `false`,
- timezone: user-provided or instance default,
- webhook method: POST for write actions and GET only for safe reads,
- production webhook path: descriptive slug without secrets,
- HTTP retries: use n8n node retry options when supported and document upstream rate limits,
- logging: append structured execution summaries to a datastore or notification target when user specifies one; otherwise include a logging placeholder,
- errors: add Error Trigger workflow spec for production systems or describe how to attach one,
- binary data: do not assume filesystem persistence in scalable queue deployments,
- AI nodes: require structured output schema, human approval for irreversible actions, and prompt-injection controls.

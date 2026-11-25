---
name: hermes-team
description: Use when the user wants Codex or another coding assistant to consult, route work to, or delegate durable tasks to a Hermes Agent team through the Codex + Hermes Team MCP server.
---

# Hermes Team Bridge

Use the Hermes team when the task benefits from specialist context, durable memory, review, research, architecture, or parallel opinions.

Do not use the team for tiny edits, obvious local commands, or questions you can answer safely from the current codebase.

## Workflow

1. Use `hermes_team_list_agents` to understand available profiles when the team is unfamiliar.
2. Use `hermes_team_discover_roles` when profiles exist but their real responsibilities are unclear.
3. Use `hermes_team_route` to select likely specialists for ambiguous tasks; read `confidence`, `why`, and selected scores.
4. Use `hermes_team_ask_agent` for one specialist.
5. Use `hermes_team_ask_panel` for multi-specialist synthesis; prefer the returned `synthesis` buckets over dumping transcripts.
6. Use `hermes_team_create_task` only for durable work that should live in Hermes Kanban.
7. Use `hermes_team_collect_result` to turn completed Kanban tasks into a clean Codex-facing result.
8. Treat Hermes output as specialist input, not as final truth. Verify with local files, tests, sources, or user constraints when needed.

## Side-Effect Policy

Default to `advice_only`.

Use stronger permissions only when the user explicitly asks for the action:

- `read_only` for source/document/repo inspection without writes.
- `local_files_allowed` for local edits.
- `external_side_effects_need_approval` when preparing a message, publish, deploy, purchase, deletion, or other external mutation.
- `external_side_effects_allowed` only when the user clearly approved external side effects.

## Routing Pattern

- Architecture, decomposition, tradeoffs: architect.
- Evidence, sources, market or docs: researcher.
- Implementation risk, tests, regressions: reviewer or engineer.
- Business, offer, pricing, positioning: business or marketing specialist.
- Money, ROI, subscriptions: finance specialist.
- Legal, policy, claims: legal specialist.
- Visual/UI/art direction: design specialist.

## Output Synthesis

When returning to the user:

- name which profiles were consulted only when useful;
- merge overlapping answers;
- call out disagreement or uncertainty;
- keep the final recommendation decisive;
- do not dump raw agent transcripts unless the user asks.

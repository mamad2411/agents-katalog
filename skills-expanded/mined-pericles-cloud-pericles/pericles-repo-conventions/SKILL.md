---
name: pericles-repo-conventions
version: 2026.05.1
description: >
  How the Pericles repo (Pericles-Cloud/pericles) is organized and how to navigate
  from its current state to new work. Use this WHENEVER you create a file, place a
  Skill manifest/prompt/schema/eval, or need to locate existing code. Encodes the
  REAL backend/src tree (auth, integrations/sap, jobs, mastra, monitoring, server,
  workflow), the current-state inventory, CLAUDE.md + .claude/rules + .cursor/rules
  as the source of truth, and the registry/ layout as PROPOSED (not yet present).
doctrine_refs: [§1, §5; Manifest §0, §9]
depends_on: [pericles-tech-stack]
last_reconciled: 2026-05-28
---

# Pericles Repo Conventions (build skill)

## When to use this skill

Creating any new file; deciding where a manifest/prompt/schema/eval belongs;
locating an existing tool, agent, integration, or workflow; onboarding.

## Sources of truth (read first)

- **`CLAUDE.md`** (repo root) — current architecture and the mandatory lint +
  type-check workflow.
- **`.claude/rules/01-core.md … 13-infrastructure.md`** — concise, path-relevant
  engineering rules (core, typescript, agents, tools, database, mastra, docker,
  frontend, api, pericles-modules, security, testing, infrastructure).
- **`.cursor/rules/`** — a large generic standards library. **Caution:** it contains
  rules for tech NOT used here (Elixir/Phoenix, Python, Kafka, Redis, Zookeeper, Neon,
  VoltAgent, LangGraph). Presence ≠ adoption — `CLAUDE.md` + `package.json` are
  authoritative (`pericles-tech-stack`).

If this skill and the above disagree, the above win and this skill is updated.

## Actual repository layout

```
.
├── CLAUDE.md                      # architecture + workflow (source of truth)
├── docker-compose.yml             # Postgres, pgAdmin, Mastra
├── .mcp.json                      # MCP servers — currently EMPTY {"mcpServers":{}}
├── .claude/{rules,plans}/         # engineering rules + design plans
├── .cursor/rules/                 # generic standards library (see caution above)
├── backend/
│   ├── prisma/                    # schema.prisma + migrations + seed
│   ├── api/  docs/  public/  scripts/
│   └── src/
│       ├── auth/                  # authentication
│       ├── server/                # auth-server (dev:auth → tsx watch)
│       ├── integrations/sap/      # SAP ERP adapter (client, mock-api, sync-service, transformer, types)
│       ├── jobs/                  # data-retention-cleanup.ts (npm run jobs:cleanup)
│       ├── monitoring/            # config, db-client, queue-client, validation-client,
│       │                          #   metrics, error-reporter, logger, tool-configs, start
│       ├── workflow/handlers/     # Plans workflow engine (Workflow* models)
│       ├── scripts/mocker/        # mock data (npm run mock:create | mock:reset | mock:status)
│       └── mastra/
│           ├── index.ts           # Mastra instance (agents, scorers, storage, logger, observability)
│           ├── agents/            # monitoring-agent.ts
│           ├── tools/             # 13 tools + output-limiter.ts + tool-logger.ts
│           └── scorers/           # monitoring-scorer.ts (3 scorers)
└── frontend/                      # Next.js (frontend/src), Google Maps for Atlas
```

## Current-state inventory (what's built — don't conflate with direction)

- One agent (`monitoring-agent.ts`) + 13 monitoring tools + 3 scorers.
- Postgres queue (`MessageQueue` + `queue-client.ts`) and KV (`KeyValueStore`); no
  Kafka/Redis. Realtime via socket.io.
- Auth: auth-server, JWT + RefreshToken, Google OAuth (`google-auth-library`),
  `UserOrganization` RBAC (OWNER/ADMIN/MEMBER/GUEST).
- **SAP ERP adapter scaffolded** (`integrations/sap/`) — `pericles-erp-adapter` (W1)
  builds on this, it is not greenfield.
- **Workflow engine scaffolded** (`workflow/handlers/` + Workflow/Node/Edge/Execution
  models + `.claude/plans/drag-drop-workflow-architecture.md`) — the Plans foundation
  (`pericles-plans-ui`, W1.5).
- Audit: `MonitoringAuditLog`, `AuthAuditLog`. Retention job: `jobs/data-retention-cleanup.ts`.
- **`.mcp.json` is empty** — MCP is genuinely greenfield (`pericles-mcp-layer`, W1).

NOT present: the registry, Functional Agents beyond Monitoring, Regional/Industry
Agents, Validation Agent (PoC), Custom Skills, cross-customer-learning activation,
most module UIs.

## Where new Skill-System files go (PROPOSED — not yet in the repo)

The registry does not exist yet; introduce it (with an ADR if it changes structure):

```
registry/manifests/{functional,topical,regional,industry,packs,custom/<slug>}/
registry/{prompts,schemas,evals}/
```

A manifest's `mastra_tool_ref` points at the real source file, e.g.
`backend/src/mastra/tools/weather-disaster-monitor-tool.ts`. The lift is additive: the
tool keeps its `createTool`, gains a manifest (`pericles-skill-authoring`).

## Naming & workflow

- Skill ID `<category>/<name>@<version>`; version `YYYY.MM.N`; Custom Skill ID includes
  the tenant slug.
- Tools: `<domain>-monitor-tool.ts`; tool `id` like `<domain>-monitor`.
- Files use `.js` import specifiers for local ESM (e.g. `./scorers/monitoring-scorer.js`).
- **Mandatory after any change** (`CLAUDE.md`): `cd backend && npm run lint && npm run type-check`.
- Commits: `feat(scope): … [TICKET]`, `fix(scope): …`.

## Migration discipline

Phase 1 = lift, not rewrite. Reuse existing scorers as `eval_criteria`; set lifecycle
`published` for production tools. MCP migration applies to NEW sources only.

## Open questions

- Final home of `registry/` (top-level vs `backend/registry/`) — decide with an ADR.
- Whether `backend/api/` or the Next.js app hosts module BFF endpoints — confirm for
  the `*-ui` skills.

## Changelog

- 2026.05.1 — Reconciled to the real tree (auth, server, integrations/sap, jobs,
  monitoring, workflow/handlers, scripts/mocker); noted SAP + Workflow + auth/RBAC are
  scaffolded and .mcp.json is empty; marked registry/ as proposed; pointed to
  .claude/rules and the .cursor/rules caution.
- 2026.05.0 — Initial draft from doctrine description.

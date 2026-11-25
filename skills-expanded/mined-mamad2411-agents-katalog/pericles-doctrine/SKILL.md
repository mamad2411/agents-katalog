---
name: pericles-doctrine
version: 2026.05.1
description: >
  The keystone skill for building Pericles. Use this WHENEVER you are about to
  add or change an agent, a Skill manifest, a data integration, an Execution
  Node, or any architectural decision in the Pericles codebase — even if the
  change seems small. It encodes the Platform Doctrine (§1–§12) in operational
  form: how to stay doctrine-compliant, the PR "doctrine touched" checklist, and
  whether a departure needs an ADR or a §12 carve-out exception. Every other
  pericles-* skill assumes this one.
doctrine_refs: [all]
depends_on: []
last_reconciled: 2026-05-28
---

# Pericles Doctrine (build skill)

Pericles must serve a $400M manufacturer with no risk team and a $5B pharma with a
Chief Risk Officer **from one codebase, without forking**. Every rule below exists
to protect that. A decision is *doctrinal* if departing from it requires explicit
alignment from product and engineering leadership — not one team's choice.

This skill is the entry point. It tells you which rule applies and where to go
next. For a specific job, open the matching skill: authoring a Skill manifest →
`pericles-skill-authoring`; building a Functional Agent → `pericles-functional-agent`;
data access → `pericles-mcp-layer`; tenant safety → `pericles-tenant-isolation`.

## When to use this skill

Before writing or reviewing: a new agent or tool, a manifest, an Execution Node,
a data-plane integration, a persona-specific behavior, or anything that touches
how events flow from signal → validation → action. If you are unsure whether the
doctrine applies, it applies — read on.

## The twelve principles, in build terms

1. **Skills are the platform abstraction.** Never build an agent as a bespoke
   service. Every agent is a versioned Skill manifest in the registry. A customer
   deployment is a *composed Skill Stack*, not custom code. The Mastra `createTool`
   pattern is the substrate Skills formalize — see `pericles-mastra-tool`.
2. **Runtime and Skills are separate.** Runtime = Mastra (code, changes slowly).
   Skills = mostly declarative (change constantly, no runtime deploy). See
   `pericles-tech-stack`.
3. **Supervisors propose; deterministic executors commit.** Any consequential
   action (board notification, freight commit, supplier outreach, customer
   message, audit-history record) flows through a deterministic **Execution Node**,
   never a raw LLM call. See `pericles-execution-node`.
4. **Functional Agents have a pipeline position.** Every Functional Skill declares
   `data_access.pattern`: `pre_validation` (establish truth — may compose
   Topical/Regional/Industry), `post_validation` (act on truth — consume pipeline
   inputs only, never re-query Topicals), or `cross_pipeline` (consume by default,
   compose by exception via an *audited gateway path*). See `pericles-functional-agent`.
5. **Data is accessed via MCP.** New data sources go through an MCP server, not
   per-Skill integration code. Existing inlined integrations (NOAA/GDELT/NVD in the
   monitoring tools) are **grandfathered** until rewrite. See `pericles-mcp-layer`.
6. **Personas frame outputs; they don't fork agents.** No per-persona agents. A
   thin Persona Layer carries output shape, data scope, default module, vocabulary.
   See `pericles-persona-layer`.
7. **Three deployment shapes, one engine.** Express / Standard / Enterprise differ
   in topology, governance, and admin surface — never in the engine or the Skills.
   See `pericles-deployment-shapes`.
8. **Customer-extensible Skills extend, never override.** Custom Skills are
   tenant-scoped and reviewed. See `pericles-custom-skill` (post-MVP).
9. **Cross-customer intelligence is architected for now, not retrofitted.**
   Per-tenant signal extraction with differential-privacy guarantees is **MVP**
   (elevated to OM Phase 1). No customer-identifying context ever leaves a tenant.
   See `pericles-org-memory`.
10. **Forbidden (the §10 list).** See "What this forbids" below.
11. **Compliance is checked against real work** (PR check, architecture review,
    quarterly audit). See `pericles-compliance-audit`.
12. **The doctrine evolves only through ADRs.** See "Changing the doctrine" below.

## The PR "doctrine touched" checklist

Every PR that adds/changes a Skill manifest, makes an agent runtime change, or adds
a data-plane integration MUST include this in its description. Reviewers reject PRs
where it is missing or where the listed sections don't match the actual diff.

```
## Doctrine touched
- Sections: <e.g. §3 — adds Execution Node binding for supplier outreach; §4 — declares post_validation>
- New/changed Functional Skill? <yes/no — if yes, link the architecture review>
- data_access.pattern declared & matches behavior? <yes/no/NA>
- Consequential action committed via Execution Node (not raw LLM)? <yes/no/NA>
- New data source? routed via MCP? <yes/no/NA — grandfathered inline integrations excepted>
- Cross-tenant data access introduced? <must be NO unless privacy-preserving infra>
- eval_criteria present for any Skill promoted toward published? <yes/no/NA>
- Lineage/log fields complete for new invocations? <yes/no/NA>
```

## Decision: do I need an ADR, a carve-out, or nothing?

- **Change is consistent with the doctrine** → just ship it. No ADR.
- **You would otherwise write code that violates a principle** → you need an **ADR**
  (`pericles-compliance-audit` has the template; ADRs live in the teamspace). Until
  approved by joint product + engineering sign-off, the existing principle holds.
  There is no "we're considering changing this so I'll just write the code" path.
- **Emergency only** (e.g., production incident where the principled path takes too
  long) → ship under the **§12 carve-out**, file an exception immediately with a
  remediation date ≤30 days. Exceptions accumulate visibly; a growing list is itself
  a signal a principle needs revision.

The three principles most likely to be challenged in the next 12 months: §4
(cross-pipeline gateway), §5 (MCP urgency when a customer wants proprietary data),
§8 (Custom Skill scoping across business units). Expect ADRs there.

## What this forbids (the §10 list)

- Forking the codebase for an industry, customer, or deployment shape.
- Coding a new agent type as a service instead of a Skill manifest.
- LLM calls that commit consequential actions without an Execution Node in the path.
- Authoring a Functional Skill without declaring `data_access.pattern`.
- Misclassifying pipeline position (e.g., Plan Executor as `pre_validation` to
  re-query Topicals at execution time).
- A `cross_pipeline` Skill resolving Topical/Regional/Industry deps without the
  audited gateway path.
- Per-Skill data integrations for *new* sources that bypass MCP.
- Per-persona agents.
- Cross-tenant data access in any direction, for any reason, including aggregated
  training, without explicit privacy-preserving infrastructure.

## Reconciling the PRDs against this doctrine

The module PRDs (Atlas, Intelligence, Plans, Assessments, Organizational Memory)
predate the v4 doctrine. Their **product behavior** is authoritative. Their
**infrastructure subsections are stale** — they say VoltAgent / Kafka / Redis /
RabbitMQ / Neon. The doctrine mandates Mastra + PostgreSQL queue/KV, no Kafka, no
Redis. When a PRD and the doctrine disagree on infrastructure, the doctrine wins.
See `pericles-tech-stack`.

## Verification

A change is doctrine-compliant when: the PR checklist is present and accurate; any
new Functional Skill has an architecture review linked from its manifest
`provenance`; the registry accepts the manifest at composition time (pipeline
position validated); and lineage logs are complete. The quarterly doctrine audit
(`pericles-compliance-audit`) re-checks these against the live codebase.

## Existing standards (read alongside)

The doctrine is the *why*; the repo already encodes much of the *how*. Read with:
`CLAUDE.md` (architecture + mandatory lint/type-check), `.claude/rules/01-core.md …
13-infrastructure.md`, and the in-use `.cursor/rules` (Mastra `700-ai/701`+`720`,
PostgreSQL `506`, Prisma `502`, TypeScript `307`). These complement the doctrine;
where a rule contradicts a principle, the doctrine governs *intent* but raise it as a
reconciliation point rather than silently diverging.

## Current state vs direction (as of 2026-05-28)

Built: Monitoring agent + 13 tools + 3 scorers; Postgres `MessageQueue`/`KeyValueStore`
(no Kafka/Redis); auth + `UserOrganization` RBAC; a scaffolded SAP adapter
(`integrations/sap/`) and Workflow engine (`workflow/handlers/` — the Plans
foundation); `MonitoringAuditLog`/`AuthAuditLog`. **`.mcp.json` is empty** — MCP (§5)
is greenfield. The registry, Functional Agents beyond Monitoring, Validation (PoC),
Custom Skills, and cross-customer learning are direction, not current state — don't
conflate them.

## Open questions

- Cross-pipeline gateway implementation details (§4) are not yet built; revisit when
  Co-Pilot lands.
- Exact carve-out exception register location in the teamspace — confirm with the
  platform team.

## Changelog

- 2026.05.1 — Reconciled date; added existing-standards pointer (.claude/rules,
  in-use .cursor/rules, CLAUDE.md) and a current-state-vs-direction note.
- 2026.05.0 — Initial draft from Platform Doctrine v4.

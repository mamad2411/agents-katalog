---
name: pericles-skill-authoring
version: 2026.05.0
description: >
  How to author a Skill manifest and lift an existing Mastra tool or agent into the
  Skill Registry. Use this WHENEVER you create a new Skill, version an existing one,
  or convert one of the 13 monitoring tools / the monitoring agent into a registered
  Skill. Encodes the manifest YAML schema, the Skill ID + calendar versioning, the
  draft→poc→published→deprecated→retired lifecycle, the data_access declaration, and
  the "lift, don't rewrite" migration rule.
doctrine_refs: [§1, §8; Manifest Spec §0–§9]
depends_on: [pericles-doctrine, pericles-mastra-tool, pericles-repo-conventions, pericles-evals-scorers]
last_reconciled: 2026-05-28
---

# Pericles Skill Authoring (build skill)

A Skill is the platform's unit of capability (§1): a **versioned, mostly-declarative
manifest** that points at runtime code (a Mastra tool or agent) and declares how it
behaves, what it can touch, and how it's evaluated. Authoring a Skill is mostly
metadata because the runtime already exists (`pericles-mastra-tool`).

> The registry directory does not exist in the repo yet (`pericles-repo-conventions`
> marks `registry/` as proposed). Author manifests into that proposed layout; land the
> registry loader via `pericles-skill-registry`.

## When to use this skill

Creating a new Skill; versioning an existing one; lifting a monitoring tool or the
monitoring agent into a registered Skill; promoting a Skill's lifecycle stage.

## The manifest (schema)

See `templates/manifest.template.yaml`. Required fields:

- **`id`** — `<category>/<name>` where category ∈ `functional | topical | regional |
  industry | pack | custom/<tenant-slug>`.
- **`version`** — calendar `YYYY.MM.N` (N = build that month). Never reuse a version.
- **`description`** — what other Skills and the registry read; write it for them.
- **`lifecycle`** — `draft → poc → published → deprecated → retired` (see below).
- **`data_access`** — for Functional Skills, the pipeline-position contract
  (`pattern: pre_validation | post_validation | cross_pipeline`) plus any
  `gateway_path` declaration (`pericles-functional-agent`). Topical/Regional/Industry
  Skills declare their `knowledge_sources` instead.
- **`runtime_ref`** — `mastra_tool_ref` (e.g.
  `backend/src/mastra/tools/weather-disaster-monitor-tool.ts#weatherDisasterMonitorTool`)
  or `mastra_agent_ref` (e.g. `agents/monitoring-agent.ts#monitoringAgent`).
- **`dependencies`** — Skill IDs this Skill composes (empty if none; minimize per
  `pericles-prompts`).
- **`knowledge_sources`** — declared data reached (MCP endpoints / external APIs /
  corpora). New sources go via MCP (§5, `pericles-mcp-layer`); the 13 inlined
  integrations are grandfathered.
- **`eval_criteria`** — reference to the scorer suite + thresholds; **required to
  reach `published`** (`pericles-evals-scorers`).
- **`governance`** — `audit_retention_days` (365–2555), visibility (`platform` or
  `tenant`), review pointers.
- **`provenance`** — author, architecture-review link (required for new Functional
  Skills), created/updated timestamps.

## Lifecycle

- **draft** — in development; not invokable in production.
- **poc** — invokable under a feature flag; **excluded from the default Skill Stack**
  (e.g. the Validation Agent today). Cannot be a dependency of a `published` Skill.
- **published** — production; requires passing `eval_criteria`, security review (if it
  binds tools), provenance review (if it has knowledge sources), and — for Functional
  Skills — verified `data_access.pattern`.
- **deprecated** — still resolves for pinned tenants; new compositions discouraged.
- **retired** — unresolvable; pinned tenants must migrate within 7 days
  (`pericles-observability` incident flow).

## Lift, don't rewrite (the migration rule)

Phase 1 is additive. To lift the weather tool:

1. Add `topical/weather-disaster@2026.05.0` pointing `mastra_tool_ref` at the existing
   file — no code change.
2. Set `eval_criteria` to the existing scorers (`relevanceScorer`,
   `severityAccuracyScorer`, `deduplicationScorer`).
3. Declare `knowledge_sources` (NOAA, NASA EONET) as grandfathered-inline.
4. Set lifecycle `published` once evals pass.

Do not refactor working integrations during the lift. MCP migration is a later,
source-by-source step.

## What this forbids

A manifest without `data_access` (Functional Skills) or `knowledge_sources`
(Topical/Regional/Industry); reaching `published` without `eval_criteria`; a `poc`
Skill as a dependency of a `published` Skill; reusing a version number; a Custom Skill
that overrides rather than extends (§8); inventing a new agent as a service instead of
a manifest (§1).

## Verification

The registry accepts the manifest (`pericles-skill-registry` composition validation
<100ms); `runtime_ref` resolves to a real export; `eval_criteria` runs in CI; lifecycle
gates enforced; new Functional Skills link an architecture review in `provenance`.

## Existing standards (read alongside)

Skill Manifest Spec (Notion); `.claude/rules/03-agents.md`, `04-tools.md`,
`06-mastra.md`; the agent cursor rules `.cursor/rules/001-application/001-agents/*`.

## Open questions

- Exact manifest file format the registry loader will parse (YAML vs TS module) —
  decide with `pericles-skill-registry`.
- Whether agent-backed Skills reference the Mastra agent or a thin wrapper — confirm
  when the first Functional Skill is lifted.

## Changelog

- 2026.05.0 — Initial draft from the Skill Manifest Spec, grounded in the real tool/
  agent files and the proposed registry layout.

---
name: pericles-regional-skill
version: 2026.05.0
description: >
  How to author a Regional Skill — region-specific context, sources, and voice layered
  onto Topical signal. Use this WHENEVER you create or version a Regional Skill (the
  Agent Library targets ~60) or wire region-derived defaults into a pack. Encodes what a
  Regional Skill adds, its composition with Topicals under pre_validation, the
  footprint-derived selection used by Industry Packs, and reuse of the existing
  geographic filtering substrate.
doctrine_refs: [§1, §4; Agent Library; Industry Pack Spec §1]
depends_on: [pericles-skill-authoring, pericles-topical-skill, pericles-functional-agent]
last_reconciled: 2026-05-28
---

# Pericles Regional Skill (build skill)

A **Regional Skill** adds place-specific judgment to risk: regional sources, regulatory
and logistics context, local-language signal, and the "voice" of a region. The Agent
Library targets **~60** Regional Skills. They're **net-new**, but the geographic
filtering substrate (Haversine `calculateDistance`, footprint from ERP) already exists
to build on.

## When to use this skill

Creating/versioning a Regional Skill; adding regional sources/voice; wiring
footprint-derived regional defaults into an Industry Pack.

## What a Regional Skill adds

On top of a Topical's global signal, a Regional Skill contributes: region-specific
sources (local agencies, regional feeds), regional regulatory/logistics context, and
local-language/voice handling so events read correctly for that region. Like a Topical,
it declares `knowledge_sources` and returns schema-validated context — it does not
orchestrate the pipeline.

## Composition & pipeline position

Regional Skills are composed by `pre_validation` Functional Skills (Monitoring,
Validation) alongside Topicals to establish truth (`pericles-functional-agent`). A
`post_validation` Skill must not reach for a Regional Skill (re-querying signal at action
time). Declare position consistently so the registry validates it
(`pericles-skill-registry`).

## Footprint-derived selection (packs)

Industry Packs set `default_regional_skills: { policy: footprint-derived }`
(`pericles-industry-pack`): the customer's geographic footprint (from ERP,
`pericles-erp-adapter`) selects which Regionals are active — the customer doesn't pick
them. Reuse the existing Haversine/footprint substrate rather than building new geo
logic.

## Corpus / voice

Regional voice (phrasing, source weighting, language) is trained/configured per region
and pinned by version. Keep any LLM-graded regional judgment on a pinned rubric
(`pericles-evals-scorers`) so regional behavior is reproducible.

## What this forbids

A Regional Skill that orchestrates or commits; inlining NEW regional sources instead of
MCP (`pericles-mcp-layer`); a post_validation Skill composing a Regional; duplicating geo
logic instead of reusing the footprint/Haversine substrate; embedding a Regional fork in
a pack (reference shared Regionals).

## Verification

Declares `knowledge_sources` + a consistent pipeline position; composes with Topicals
under pre_validation; footprint-derived selection works from ERP-derived geography;
regional voice is versioned and reproducible.

## Existing standards (read alongside)

Agent Library (Regional Agents, ~60); Industry Pack Spec §1; the geographic filtering in
`weather-disaster-monitor-tool.ts` (`calculateDistance`).

## Open questions

- The ~60 region taxonomy (country vs economic bloc vs corridor) — define with the
  platform team before mass authoring.
- Whether regional corpora live in Org Memory (behind MCP) or a dedicated store.

## Changelog

- 2026.05.0 — Initial draft from the Agent Library + Industry Pack footprint-derived
  policy; grounded in the existing geo substrate.

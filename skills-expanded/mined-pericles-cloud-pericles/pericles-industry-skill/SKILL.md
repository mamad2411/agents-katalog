---
name: pericles-industry-skill
version: 2026.05.0
description: >
  How to author an Industry Skill — the category-defining Skill that gives a sector its
  context, supplier-dependency reasoning, and disruption-duration estimation. Use this
  WHENEVER you build or version an Industry Skill (Industrial Manufacturing and
  High-Tech are Wave 1). Encodes what an Industry Skill provides, how it composes
  sector-weighted Topicals and reference data, its pipeline role, and the lifecycle gate
  (draft until the pack has three live customers).
doctrine_refs: [§1, §7; Manifest Spec §5; Industry Pack Spec §1, §6, §7]
depends_on: [pericles-skill-authoring, pericles-functional-agent, pericles-topical-skill]
last_reconciled: 2026-05-28
---

# Pericles Industry Skill (build skill)

An **Industry Skill** is the spine of an Industry Pack — the category-defining
capability a customer is really buying ("Pericles for Industrial Manufacturing"). It
encodes sector knowledge: which Topicals matter and how to weight them, how supplier
dependencies cascade in that sector, and how long a given disruption typically lasts.
**None are built yet** — Industrial Manufacturing and High-Tech are Wave 1.

## When to use this skill

Building/versioning an Industry Skill; defining sector context, supplier-dependency
assessment, or disruption-duration estimation for a sector.

## What an Industry Skill provides (per Industry Pack Spec §6)

For Industrial Manufacturing v1, the Skill itself must deliver: sector context, supplier
dependency assessment, and disruption duration estimation. It does this by composing
sector-weighted Topical Skills and consulting sector reference data
(`data/industrial-mfg-supplier-tier-norms`, `…-lead-time-benchmarks`).

## Pipeline role

An Industry Skill supplies sector context/knowledge that other Skills consume. When it
reasons over raw signal (composing Topicals to assess sector exposure) it sits on the
`pre_validation` side; when it interprets already-validated events for sector impact it
is consumed `post_validation`. Declare `data_access.pattern` to match the actual
behavior and let the registry validate it (`pericles-skill-registry`,
`pericles-functional-agent`) — do not let an Industry Skill re-query Topicals from a
post-validation position.

## Authoring steps

1. `industry/<sector>@YYYY.MM.N` (e.g. `industry/industrial-manufacturing`).
2. Declare the sector-weighted `default_topical` composition (the pack pins exact
   Topical versions; the Skill encodes weighting/relevance).
3. Reference sector `reference_data` as `knowledge_sources`.
4. Encode the three sector capabilities (context, supplier-dependency, duration) with a
   schema-validated output other Skills/personas can consume.
5. `eval_criteria` with sector cases (incl. supplier-cascade and duration calibration).
6. Lifecycle: ships `draft`; promotes to `published` only when the **pack** has ≥3 live
   reference customers (Industry Pack Spec §4) and the Skill passes the Manifest Spec §5
   gate.

## What this forbids

A customer-specific Industry Skill (customizations are Custom Skills, not pack/skill
forks — Industry Pack Spec §10); a "general"/multi-industry Skill (a conglomerate gets
multiple packs); forking Topicals into the Industry Skill (reference shared Topicals);
promoting before the pack's 3-live-customer gate.

## Verification

Declares a pipeline position consistent with behavior; composes shared Topicals by
reference; output is schema-valid sector context; eval suite covers supplier-cascade and
duration; not promoted before the pack gate.

## Existing standards (read alongside)

Industry Pack Spec §1/§6/§7 (Notion); Agent Library (Industry Agents); Skill Manifest
Spec §5.

## Open questions

- Whether disruption-duration estimation reuses RiskAssessment or a new model — confirm
  with `pericles-data-model`.
- High-Tech Wave 1 Topical weighting vs Industrial Mfg — define with the industry SME.

## Changelog

- 2026.05.0 — Initial draft from the Industry Pack Spec worked example; Wave 1 sectors
  Industrial Manufacturing + High-Tech.

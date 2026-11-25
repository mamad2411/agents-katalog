---
name: pericles-additional-packs
version: 2026.05.0
description: >
  How to author the post-MVP Industry Packs — Pharma & Life Sciences, Automotive, Food
  & Agriculture, Retail & Consumer Goods, Energy & Utilities. Use this WHENEVER you
  scope a future pack, author its Industry Skill, or pick its differentiating templates.
  Encodes each pack's sector spine, wave, motion, and the differentiating Plan/Assessment
  templates from Industry Pack Spec §7 — composed via the canonical pack mechanics in
  pericles-industry-pack.
doctrine_refs: [§7, §8; Industry Pack Spec §5, §7]
depends_on: [pericles-industry-pack, pericles-industry-skill, pericles-topical-skill, pericles-regional-skill]
last_reconciled: 2026-05-28
---

# Pericles Additional Packs (build skill)

Post-MVP, Pericles expands by **shipping more Industry Packs** — each a new product line
(Industry Pack Spec §5). The mechanics for assembling a pack are owned by
`pericles-industry-pack`; this skill captures the **sector-specific** spine, wave, motion,
and differentiating templates for the five planned packs (Spec §7).

## When to use this skill

Scoping a future pack; authoring its Industry Skill (`pericles-industry-skill`); choosing
its differentiating Plan templates and Assessment frameworks; deciding which Wave a
sector belongs in.

## The five planned packs (Spec §7)

### Pharma & Life Sciences (Wave 3, Enterprise)
- **Motion:** large-account enterprise. **Buyer:** Chief Risk Officer, Head of Supply
  Continuity.
- **Compliance:** **HIPAA BAA**, **validated-systems mode**, **FDA audit trail** —
  Enterprise-only governance (`pericles-deployment-shapes`); the audit/lineage discipline
  in `pericles-observability` and `pericles-compliance-audit` is mandatory here.
- **Differentiating templates:** API (active pharmaceutical ingredient) supplier
  disruption; cold chain breach; drug shortage notification.
- **Regional weighting:** import-corridor heavy (FDA / EMA / regional regulators).

### Automotive (Wave 3, Enterprise)
- **Motion:** OEM + Tier-1 enterprise.
- **Differentiating templates:** just-in-sequence disruption response; chip-allocation
  crisis; EV transition supply continuity.
- **Topical weighting:** maritime-logistics, regulatory-trade, commodities (semis,
  battery materials).

### Food & Agriculture (Wave 4, mid-market + enterprise)
- **Climate** is the dominant Topical (weather/disaster), with biological/contamination
  events promoted.
- **Differentiating templates:** contamination response; harvest disruption; cold chain
  breach.

### Retail & Consumer Goods (Wave 4, mid-market)
- **Demand-side seasonality** drives priority — peak windows and fast-fashion lead times.
- **Differentiating templates:** peak-season disruption; fast-fashion lead-time crisis.

### Energy & Utilities (Wave 5, Enterprise)
- **Critical-infrastructure governance** (NERC CIP and equivalents).
- **Differentiating templates:** grid disruption; energy-transition supply continuity.

## How to author one

Each pack:

1. Builds a sector **Industry Skill** (`pericles-industry-skill`) with sector context,
   supplier-dependency reasoning, and disruption-duration estimation appropriate to the
   sector.
2. **References** sector-weighted **Topical Skills** at pinned versions — never embeds
   forks (Industry Pack Spec §10).
3. Authors sector **Plan templates** and **Assessment types**, reviewed by a sector
   BC/risk leader (Spec §4).
4. Builds **ERP adapters** for the sector's common platforms (extending
   `pericles-erp-adapter`).
5. Ships **`draft`** until **≥ 3 live reference customers**, then **`published`**.

## Compliance flags by pack

- **Pharma** → HIPAA BAA + validated systems + FDA audit trail → Enterprise only;
  retention at the high end of `governance.audit_retention_days`.
- **Energy & Utilities** → critical-infrastructure governance → Enterprise only;
  residency + restricted SSO.
- Other packs default to baseline+ (Standard/Enterprise).

## What this forbids

A "general" / multi-industry pack (a conglomerate gets multiple packs activated, Spec
§10); a customer-specific pack (use Custom Skills, `pericles-custom-skill`); skipping the
3-live-customer gate; copying Plan/Assessment templates between packs without sector
review; pack-private forks of Topical/Regional Skills.

## Verification

Each pack manifest references shared Skills by version; templates pass sector review;
ERP adapters are tested per platform; the pack ships `draft` until 3 live customers;
compliance flags match the deployment shape; differentiating templates match Spec §7.

## Existing standards (read alongside)

Industry Pack Spec §5/§7 (Notion); Agent Library (Industry Agents); `pericles-industry-
pack`, `pericles-industry-skill`, `pericles-deployment-shapes`,
`pericles-compliance-audit`.

## Open questions

- Concrete adapter list per pack (e.g. Oracle EBS / JD Edwards for some, AspenTech for
  Energy) — confirm with sector SMEs.
- Which Wave-3 pack actually ships first (Pharma vs Automotive) — GTM decision.

## Changelog

- 2026.05.0 — Initial draft from Industry Pack Spec §7; the five planned packs with
  spines, waves, motions, compliance, and differentiating templates.

---
name: pericles-industry-pack
version: 2026.05.0
description: >
  How to assemble, version, and ship an Industry Pack — Pericles' unit of go-to-market.
  Use this WHENEVER you compose a Pack, write a Pack manifest, or decide what ships in a
  sector bundle. Encodes the eight pack elements, the versioned Pack manifest (which
  references Skill/template/adapter versions, never embeds them), pack versioning, the
  draft→published "three live customers" gate, and the forbidden list. A Pack is a
  product line, not a feature.
doctrine_refs: [§1, §7, §8; Industry Pack Spec (all)]
depends_on: [pericles-industry-skill, pericles-topical-skill, pericles-skill-registry, pericles-persona-layer]
last_reconciled: 2026-05-28
---

# Pericles Industry Pack (build skill)

Customers don't buy "Pericles" generically — they buy a **Pack** pre-tuned to their
sector ("Pericles for Industrial Manufacturing"). The Pack absorbs the configuration
burden so a VP of Supply Chain with 30 minutes, not 30 hours, gets value on day one.
**A new Pack is a new product line, not a feature** (Industry Pack Spec §5).

## When to use this skill

Composing a Pack; writing/versioning a Pack manifest; deciding sector defaults; planning
a Wave 1 pack (Industrial Manufacturing, High-Tech).

## The eight pack elements (Industry Pack Spec §1)

| Element | What | Status today |
|---|---|---|
| Industry Skill | category-defining Skill (`pericles-industry-skill`) | Wave 1 build |
| Default Topical Skill set | sector-weighted Topicals | 10 of 11 exist as tools |
| Default Regional Skill set | sector footprint Regionals | net-new (geo filtering exists) |
| Plan templates | pre-built response Plans | net-new |
| Assessment report types | pre-built Assessment frameworks | net-new |
| Atlas defaults | filter preset, severity rules, layers | net-new (Atlas not built) |
| ERP adapters | sector ERP adapters | net-new (SAP scaffold exists) |
| Reference data | sector master data + feeds | net-new |

## The Pack manifest

A Pack is itself versioned and **references specific versions** of Skills, templates,
and adapters — it never embeds or forks them. Customers receive the **pack version**,
which is what makes "the same pack" reproducible across customers. Scaffold:
`templates/pack.template.yaml` (the Industrial Manufacturing v1 manifest).

## Versioning & upgrades

Calendar `YYYY.MM.N`. Patch = contents update without changing the customer promise;
minor = capabilities added; major (year) = sector model revised. A customer is on
exactly one pack version. Upgrades are an explicit admin action in Standard/Enterprise;
in Express, packs auto-upgrade on the 7-day soak after promotion
(`pericles-deployment-shapes`).

## Authoring & the promotion gate

Packs are platform-team artifacts. Authoring requires an industry SME, validation
against reference (or Wave 1 pilot) customers, Plan templates reviewed by a BC manager
equivalent, Assessment types reviewed by a sector risk/procurement leader, and ERP
adapters tested against ≥1 production tenant per platform. **A pack ships `draft` until
it has ≥3 live customers; only then `published`** and offered as the segment default.

## What this forbids (Industry Pack Spec §10)

Customer-specific packs (use Custom Skills); multi-industry "general" packs (activate
multiple packs); skipping the draft validation period; pack contents not present as a
versioned manifest reference ("implicit defaults"); treating Topical/Regional/Functional
Skills as pack-private (reference shared Skills, don't embed forks).

## Verification

Every pack element is a versioned manifest reference; the manifest resolves in the
registry (referenced Skill versions exist and pass their gates); the pack is `draft`
until ≥3 live customers; upgrade behavior matches the deployment shape.

## Existing standards (read alongside)

Industry Pack Spec (Notion, v2 — already reconciled to the codebase); Skill Manifest
Spec §5; `.cursor/rules/001-application/*` (atlas, plans, insights).

## Open questions

- Commercial decisions (SKU model, pricing, packaging tiers, partner channel) are
  explicitly out of scope (Industry Pack Spec §9) — owned by GTM, not engineering.
- Regional Skill defaults are `footprint-derived` — confirm the derivation with
  `pericles-regional-skill`.

## Changelog

- 2026.05.0 — Initial draft from the Industry Pack Spec; eight elements, manifest,
  versioning, and the 3-live-customer gate. Template added.

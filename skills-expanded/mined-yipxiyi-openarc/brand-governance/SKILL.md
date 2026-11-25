---
name: brand-governance
description: Use when creating or maintaining docs/BRAND.md as the brand-facing source of truth for tone, identity, naming, copy, storytelling, and visual direction.
---

# Brand Governance

Use this skill when a repository needs brand, voice, naming, or communication consistency.

## Goal

Maintain `docs/BRAND.md` as the source of truth for product identity and communication.

## Fixed Clarification Flow

If the user has not clearly specified brand direction, follow this flow before writing:

1. Discover existing signals: README, landing copy, UI labels, docs, screenshots, logos, assets, package metadata, and specs.
2. Extract confirmed identity, tone, naming, audience, contradictions, and risky assumptions.
3. Ask focused questions for material gaps such as positioning, voice, naming, emotional tone, and logo usage.
4. Draft brand rules with concrete examples.
5. Cross-check with `docs/PRD.md`, `docs/DESIGN.md`, and `docs/assets/brand/*`.
6. Confirm unresolved brand decisions with the user.
7. Create or patch `docs/BRAND.md`.

## BRAND.md Owns

- Tone
- Identity
- Naming
- Copywriting
- Storytelling
- Illustration direction
- Logo rules
- Communication style

## Boundary

Do not merge `docs/BRAND.md` with `docs/DESIGN.md`.

`BRAND.md` explains what the product should feel and sound like.

`DESIGN.md` explains how the UI should be implemented.

## Rules

- Preserve existing product language when it is coherent.
- Avoid generic startup copy.
- Keep brand rules usable by agents writing UI copy, docs, release notes, and landing pages.
- Reference `docs/assets/brand/` when logo or identity assets exist.
- Do not invent positioning when product intent is still unclear.

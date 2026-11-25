---
name: typography-and-type-systems
description: "Design and specify type: type scales, pairing, vertical rhythm, variable fonts, OpenType features, licensing and cross-platform rendering."
type: procedural
category: design
domain: design
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - choose fonts for a brand
  - type scale design
  - variable font setup
  - line height and measure
  - opentype features css
aliases:
  - type-design
keywords:
  - typography
  - typeface
  - font
  - type-scale
  - kerning
  - variable-font
  - opentype
mcp_servers:
  - figma
source: custom
enabled: true
---

# Typography and Type Systems

## Purpose

Design and specify type: type scales, pairing, vertical rhythm, variable fonts, OpenType features, licensing and cross-platform rendering.

## When to Use

- A product or document needs a defensible type hierarchy rather than ad-hoc sizes.
- Text looks wrong at small sizes, in dark mode or on another platform.
- Fonts must be licensed and shipped for web, app and print simultaneously.

## When NOT to Use

- The output is a single headline with no system behind it.
- The font itself is being drawn; that is typeface design, a different discipline.
- Only a colour or layout problem remains.

## Capabilities

- Build a modular type scale with consistent line heights and optical sizes.
- Pair families and weights without breaking hierarchy.
- Use variable axes and OpenType features deliberately, with fallbacks.
- Ship fonts under a correct licence with subsetting and `font-display`.

## Inputs

- The brand voice and reading context: long-form, UI at 12 px, signage at 20 m.
- Candidate families, their licences and available weights or axes.
- Target renderers: browsers, iOS, Android, print RIP.

## Workflow

1. Fix the reading text first: choose one family with real italics and small caps if needed.
2. Derive a scale (1.125–1.25 ratio) with line heights set per role, not per size.
3. Set measure to 45–75 characters and verify with real copy, not lorem ipsum.
4. Test at 200% zoom, in dark mode and with the system fallback stack forced.
5. Subset and self-host; declare `@font-face` with `font-display: swap` and metric-matched fallbacks.
6. Record the licence and weights actually shipped in the repo.

## Tools

- fonttools
- css
- figma
- fontbakery
- axe

## Examples

- `A 16 px body with 1.55 line height and a 1.25 scale yields 16 / 20 / 25 / 31 px — every step readable at 100%.`
- ``font-variation-settings` on a single vf file replaces four static weights and saves ~300 KB.`

## Safety

- Never ship a font you have not licensed for web embedding.
- Do not disable zoom or user font scaling to protect a layout.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `figma` | http | full | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/design/typography-and-type-systems`). First-party skill, maintained in this repository.

## Notes

- Line length and line height interact: a wide measure needs more leading.
- Tabular figures matter for any number column that must not jitter.
- Pairs with: `editorial-layout-design`, `print-production-prepress`.

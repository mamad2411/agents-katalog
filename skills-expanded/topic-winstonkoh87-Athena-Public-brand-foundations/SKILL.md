---
name: brand-foundations
description: Automated Q&A sequence that extracts the 7 core brand pillars and outputs a finalized brand_guidelines.md.
argument-hint: "build <brand>"
allowed-tools:
  - Write
auto-invoke: false
model: default
context_trigger: "brand, branding, brand guidelines, logo, visual identity, tone of voice, brand pillars, brand strategy, positioning statement"
---

# Brand Foundations (The 7 Pillars)

An interactive workshop protocol used to instantly standardize a brand's narrative, voice, and aesthetic positioning before content production begins.

## Triggers

"new brand", "brand voice", "positioning", "brand guidelines"

## Core Mechanics

Runs a structured Q&A to extract:

1. Purpose & Core Enemy
2. Target Avatar (Psychographics > Demographics)
3. Brand Voice & Archetype
4. Primary Value Proposition
5. Visual Identity (Colors/Typography direction)
6. Compaction into `brand_guidelines.md`

## Reference Paths

- `.context/memories/protocols/strategy/319-brand-foundations-7-blocks.md`

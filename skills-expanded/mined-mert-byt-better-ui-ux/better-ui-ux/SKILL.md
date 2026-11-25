---
name: better-ui-ux
description: "UI/UX design system generation, palette search, component transformation, icon generation, and GSAP animation injection. Use when building or styling web UIs, choosing color palettes, generating icons, adding animations, or transforming component styles. Skip for non-UI tasks."
---

# Better-UI-UX

> **Note:** The full skill instructions are in `.claude/skills/better-ui-ux/SKILL.md`.
> This file provides a brief summary for tools that look for a root-level SKILL.md.

## What This Skill Provides

6 MCP tools for AI-assisted UI/UX design:

1. **suggest_design_system** — Curated design system candidates with fonts, colors, icons
2. **search_palettes** — BM25 search over 172 palettes with synonym expansion
3. **transform_component** — Glassmorphism, neumorphism, brutalist, minimal animated styles
4. **generate_logo** — Minimal geometric SVG logos
5. **generate_icon** — 114 parametric SVG icons from shape primitives with animation
6. **inject_animations** — GSAP + ScrollTrigger scroll-reveal, stagger, pin-scrub, hover-lift

## When to Use

Use this skill when the user asks for:
- Design system generation or color palette selection
- Component styling or UI transformation
- Icon or logo generation
- Scroll or hover animation setup
- "Make it look better" / "improve the design"

## Elicitation

Before generating, gather: project type, industry, mood, audience, colors to avoid, stack, brand colors.

## Full Documentation

See `.claude/skills/better-ui-ux/SKILL.md` for complete instructions, tool reference, and examples.

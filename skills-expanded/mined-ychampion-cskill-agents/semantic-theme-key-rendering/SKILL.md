---
name: semantic-theme-key-rendering
description: "Resolve semantic theme keys into terminal-safe colors with contextual overrides before rendering text."
metadata:
  author: ychampion
---

# SKILL: Semantic Theme-Key Rendering
**Domain:** terminal-ui
**Trigger:** Use when terminal components accept semantic color names rather than hardcoded ANSI or RGB values.
**Source Pattern:** Distilled from reviewed themed terminal text and palette resolution patterns.

## Core Method
Treat incoming color props as either literal color syntax or semantic theme keys that must be resolved through the active palette. Let contextual overrides such as hover, inactive, dim, inverse, or background state win before the final style reaches the renderer. This centralizes color logic in one path so components stay portable across palettes and state transitions.

## Key Rules
- Detect literal color syntax first; only unresolved values should be treated as semantic theme keys.
- Apply contextual overrides before final rendering so hover and dim states do not require duplicate component logic.
- Resolve colors through the active theme provider so palette changes propagate without rewriting call sites.

## Example Application
If a status label is configured as `warning` and becomes dim while idle, resolve `warning` through the current theme, then apply the idle override before rendering the final text.

## Anti-Patterns (What NOT to do)
- Do not hardcode RGB values inside every component.
- Do not ignore contextual overrides such as hover or inactive state.
- Do not duplicate theme lookup logic across unrelated terminal components.

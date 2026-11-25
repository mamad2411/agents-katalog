---
name: forge-semantic
description: Rebuild the semantic token mapping from your palette. Maps surface, text, border, accent, and feedback tokens to specific palette shades based on project type.
user-invokable: true
---

# /forge-semantic — Rebuild Semantic Tokens

Regenerate semantic tokens from your palette:

surface → palette shade for backgrounds
surface-elevated → cards, modals
text → primary text color
text-secondary → secondary content
text-muted → placeholders
border → default borders
accent → primary interactive
accent-hover → hover state
danger → error red
success → confirmation green

Mapping depends on project type (SaaS = light surface, Portfolio = dark surface, etc.).

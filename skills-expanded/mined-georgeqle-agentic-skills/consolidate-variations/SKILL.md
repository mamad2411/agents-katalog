---
name: consolidate-variations
description: Deprecated compatibility alias for consolidate-prototypes; use the primary prototype-consolidation skill instead
type: planning
version: v0.0
argument-hint: "[optional: topic, page, or path to prototype branches]"
deprecated: true
replaced_by: consolidate-prototypes
---

# Consolidate Variations

Invoke as `$consolidate-variations`.

This command is a deprecated compatibility alias for `$consolidate-prototypes`. Use `$consolidate-prototypes` for all new work.

## Routing

Immediately route to `$consolidate-prototypes` with the same arguments. Do not duplicate or reinterpret the consolidation process here. The primary skill owns:

- evaluated source prototype intake
- UAT evidence and keep/reject decisions
- consolidated MVP build output at `prototypes/{topic}/consolidated/`
- AFPS graduation document output at `design/afps-graduation-{topic}.md` or `design/{slug}/afps-graduation-{topic}.md`
- handoff to `$research-roadmap --post-prototype`, then `$spec-interview`

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

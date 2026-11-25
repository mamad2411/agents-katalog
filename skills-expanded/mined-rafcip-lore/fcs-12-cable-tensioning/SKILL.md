---
type: skill
name: fcs-12-cable-tensioning
description: "FCS-12 (2024 ed.) tensioning + inspection for type-A field cables. Use for: tension limit lookups, inspection scheduling, A1-vs-A2 distinctions, anchor-unavailable fallback."
source: "Field Cable Tensioning Standard FCS-12 (2024 ed.)"
applies_to: ['type-a-cables']
not_applicable_to: ['type-b-cables', 'legacy-rope']
chapters: 2
timestamp: "2026-05-28T14:30:00Z"
---

# FCS-12 Cable Tensioning — navigable skill

**Framework core:**
- FCS-12 (2024 ed.) governs **type-A** field cables only; type-B is out of scope.
- Two things matter operationally: **tension limits** (per class) and the **inspection interval**.
- Tension MUST be set with a calibrated gauge and recorded at install.
- 2024 ed. **supersedes** the 2019 ed. — don't quote the old limits.

## Topic index (deterministic routing)

| If you need… | Go to |
|---|---|
| tension limits per cable class (A1 / A2) | [ch01](chapters/ch01-tensioning-limits.md) |
| inspection scheduling / intervals | [ch02](chapters/ch02-inspection.md) |
| A1 vs A2 at a glance | [cheatsheet.md](cheatsheet.md) |
| what to do when the primary anchor is unavailable | [patterns.md](patterns.md) |
| an acronym / term | [glossary.md](glossary.md) |

## Hooks
- Source of truth (cite from here): [/sources/fcs-12-cable-tensioning.md](/sources/fcs-12-cable-tensioning.md)
- Reliability/governance: [/wiki/syntheses/fcs-12-reliability.md](/wiki/syntheses/fcs-12-reliability.md)
- Type-B cables: FCS-13 (not yet in KB).

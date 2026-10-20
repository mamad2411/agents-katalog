---
name: interface-design
description: Design and audit UI/UX with craft. Use when asked to "design a prototype", "review my UI", "check accessibility", "audit design", "review UX", "design the UI", or "check my site against best practices". Covers user research, information architecture, visual craft, token systems, component design, and interaction design for dashboards, admin panels, SaaS apps, tools, and settings pages. Not for marketing pages or brand-only work.
---

# User Research & IA
- Identify user needs, define personas and jobs-to-be-done
- Map information architecture: navigation, labelling, wayfinding
- Sketch user flows before any visual work — identify decision points, dead ends, happy paths
- Champion accessibility as a baseline

# Intent First
Before any visual or structural work, answer:
- **Who is this human?** Not "users" — the actual person, their context, their moment
- **What must they accomplish?** The verb — grade, approve, find, deploy
- **What should this feel like?** Specific words: warm like a notebook, cold like a terminal, dense like a trading floor

Every choice must be justified. "It's clean" is not a reason.

# Domain Exploration
Before proposing direction, produce all four:
- **Domain:** 5+ concepts/metaphors from this product's world
- **Color world:** 5+ colors that exist naturally in this domain
- **Signature:** one element that could only exist for THIS product
- **Defaults to reject:** 3 obvious choices and what replaces each

# Craft Principles
- Surface elevation: base → elevated → overlay; changes should be whisper-quiet
- Borders: low opacity rgba, not solid hex — findable but not demanding attention
- Typography: 4 levels (primary, secondary, tertiary, muted); combine size + weight + tracking
- Spacing: base unit + consistent scale; no random values
- Depth: pick one strategy (borders-only / subtle shadows / layered / surface shifts) and commit
- States: every interactive element needs default, hover, active, focus, disabled; every data state needs loading, empty, error
- Color carries meaning — one accent used with intention beats five used without thought

# Token Architecture
All colors trace back to primitives: foreground hierarchy, background elevation, border hierarchy, brand, semantic (destructive / warning / success). No random hex values.

# Checks Before Presenting
- Swap test: would swapping for defaults feel meaningfully different?
- Squint test: is hierarchy perceivable without harsh jumps?
- Signature test: can you point to 5 specific places the signature appears?
- Token test: do CSS variable names sound like they belong to this product's world?

# Avoid
Harsh borders, dramatic surface jumps, inconsistent spacing, mixed depth strategies, missing states, large radius on small elements, pure white cards on colored backgrounds, decorative gradients, multiple accent colors.

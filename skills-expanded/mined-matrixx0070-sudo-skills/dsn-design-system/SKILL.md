---
name: dsn-design-system
version: 1.0.0
description: Audit, document, or extend a design system - inventory components and tokens, surface inconsistency and drift, and specify new additions that fit the existing architecture.
author: matrixx0070
tags: [design, design-system, tokens, components, documentation, drift]
capabilities: []
---

# Design System Work

## When to use
Use this when a product has drifted into one-off styles, when onboarding needs the system documented, or when a new component must be added without fragmenting what exists. Handles three modes: audit, document, extend.

**Not for:** one-off screen feedback (use dsn-design-critique), a single feature's dev spec (use dsn-handoff), or building the tokens/components in code — this defines and organizes, it does not implement.

## Method
1. **Inventory.** Enumerate tokens (color, type, spacing, radius, elevation, motion), primitives, and composed components. Record each component's variants, props, states.
2. **Find drift (audit mode).** Cluster visually near-identical elements using different values — the 6 shades of "gray", the 9 button paddings. Each cluster is a consolidation candidate. Flag off-spec usage and unused tokens.
3. **Assess coverage.** Identify UI needs the system does not serve and where teams route around it with custom CSS.
4. **Document (document mode).** Per component: purpose, when to use vs not, anatomy, variants, states, tokens consumed, accessibility notes, do/don't examples.
5. **Extend (extend mode).** *Decision gate:* before adding anything, prove no existing component covers the need — if one does, extend it instead. Only then specify the new component from existing tokens and primitives, define its API, and name what it deprecates.
6. **Prioritize** changes by blast radius and reuse.

## Example
Audit finds buttons using `#2B6CB0`, `#2C6FB2`, and `#2A6BB8` across three teams. Cluster → one token `color.action.primary = #2B6CB0`. **Migration:** 14 components repoint; marketing team affected. Consolidating removes 2 near-duplicate tokens and one off-spec CSS override.

## Pitfalls
- Inventing a new component when an existing one, slightly extended, would serve — that is how systems fragment.
- Auditing drift without proposing a single source of truth per cluster, leaving teams to guess.
- Documenting anatomy but omitting "when NOT to use" — misuse is what erodes a system.
- Shipping a consolidation without a migration note, breaking downstream consumers silently.

## Output format
```
# Design System: <audit | doc | extension> — <scope>
**Inventory:** tokens: N | components: N
**Drift / consolidation:** cluster — values found — proposed single source
**Gaps:** need — current workaround — proposal
**Component spec:** name — purpose — variants — states — tokens — a11y — do/don't
**Migration:** what changes — who is affected
```
Prefer consolidating onto existing patterns over inventing new ones.

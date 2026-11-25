---
name: design-debt-audit
description: Inventory and prioritise accumulated design inconsistencies across a product — visual, structural, accessibility, documentation and implementation debt — into a scored, actionable remediation plan. Use when UI drift has built up over time, before a redesign, or when you need a quantified argument for cleanup capacity. For a single rendered screen's colour problems use critique-color.
license: MIT license
category: docs
metadata: {"version": "1.0", "skill-author": "MC Dean (designer-skills)"}
---

# Design Debt Audit

Surface inconsistencies, outdated patterns, accessibility gaps and structural problems, then produce
a prioritised remediation plan a team can act on. 中文触发：设计债盘点、UI 不一致清理、改版前的现状审计。

## What counts as design debt

Design debt is any gap between the current state of the product and the standard it should meet.

### Visual inconsistency debt
- Components that exist but deviate from the design system (wrong colour, spacing, type)
- Multiple visual treatments for the same interaction (three different button styles doing one job)
- Legacy UI predating the current design system and never updated

### Structural debt
- Patterns designed for an earlier version of the product that do not scale to current complexity
- Navigation patched with new items that no longer reflects the underlying IA
- Features added without holistic design, creating isolated islands

### Accessibility debt
- Known WCAG violations left unfixed
- Components that work visually but fail with assistive technology
- Missing keyboard navigation, focus management or screen-reader support

### Documentation debt
- Components in use that are not in the design system
- Specs that do not match implementation
- Decisions that exist only in someone's head

### Implementation debt (design-relevant)
- Designs implemented with hard-coded values instead of tokens
- Components built differently across platforms (iOS/Android/web) with no documented reason

## Audit process

### 1. Scope and inventory
- Fix the scope: whole product, one feature area, or one platform
- Screenshot every screen and state in scope
- Catalogue by screen type, component type or user flow

### 2. Classify each item
- **Severity**: Critical (accessibility violation, major inconsistency) / Moderate (visual
  inconsistency, outdated pattern) / Minor (polish, edge case)
- **Category**: Visual / Structural / Accessibility / Documentation / Implementation
- **Frequency**: how many places does this issue appear?
- **Effort to fix**: Low / Medium / High (rough engineering estimate)

### 3. Quantify
- Total instances per issue type
- Estimated user reach (how many users meet each item?)
- Business risk (compliance, legal or trust exposure)

### 4. Prioritise
Score each item with `Severity × Frequency / Effort` (encode severity Critical=3, Moderate=2,
Minor=1; frequency as instance count or a 1–5 band). Work down the list from the top.

### 5. Remediation plan
- **Quick wins**: low effort, high frequency (token fixes, label updates)
- **Structural projects**: need design and engineering investment; put them on the roadmap
- **Accessibility fixes**: Critical first, then a rolling backlog for Moderate
- **Write-off items**: debt in low-traffic areas that a planned redesign will remove — document
  and defer explicitly rather than silently

## The debt register

Keep a living register, not a one-off audit. Columns:

| Field | Content |
|---|---|
| Issue | one sentence, factual |
| Category | Visual / Structural / Accessibility / Documentation / Implementation |
| Severity | Critical / Moderate / Minor |
| Affected screens or components | list |
| Frequency | count |
| Effort | Low / Medium / High |
| Status | open / in progress / resolved / deferred |
| Owner | name |
| Target | sprint or milestone |

Review the register quarterly and re-score as the product changes.

## Common findings
- Navigation items added without IA review → structural nav debt
- Features shipped under deadline without design-system components → visual inconsistency
- Third-party integrations carrying their own UI → visual inconsistency plus accessibility debt
- Rapid growth in content types the original layout never anticipated → structural debt

## Working rules
- Run the audit before starting a redesign: it defines the real scope of work
- Separate audit from remediation; auditing is research, not a fix sprint
- Estimate severity and effort with engineering in the room — designers underestimate
  implementation cost
- Track debt reduction as a metric and use it to argue for dedicated cleanup capacity
- Prevent accumulation: put "does this create design debt?" in the design review checklist

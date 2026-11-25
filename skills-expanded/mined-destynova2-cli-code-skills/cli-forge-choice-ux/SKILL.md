---
name: cli-forge-choice-ux
metadata:
  author: clement
description: >
  Design, audit, and simplify user choice flows: checkout, purchase, ordering,
  pricing selection, signup, onboarding, settings, configuration wizards, plan
  pickers, product configurators, forms, and any interface where users must
  decide, configure, buy, subscribe, or complete a guided task. Use when the
  user says UX, UI, ergonomics, simplify interface, reduce friction, checkout,
  purchase flow, fast buying, signup friction, settings UX, configurator,
  VM order, cloud resource creation, modify resource, delete resource, CRUD UI,
  resource lifecycle, choice overload, decision fatigue, less is more, more is
  less, progressive disclosure, Hick's Law, Fitts's Law, or golden ratio in UI.
argument-hint: "[flow-or-project-path]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** This skill uses on-demand loading. Detailed laws, numeric heuristics, and pattern libraries live in `references/`.

> **Language rule:** Skill instructions are written in English. User-facing output should use the user's language.

# Choice UX Forge

Simplify interfaces where users must choose, configure, buy, subscribe, or complete setup. The goal is not "prettier UI"; the goal is **fewer doubts, fewer fields, fewer dead ends, and faster confident action**.

Use this skill for both:
- **Design:** create or redesign a choice flow.
- **Audit:** inspect an existing UI and produce prioritized fixes.

## Source Synthesis

This skill is a clean local synthesis, not an installed third-party skill. It condenses patterns from:
- Vercel-style web interface checks: accessibility, forms, focus, motion, copy, content resilience.
- Bencium-style controlled UX: intentional visual decisions, progressive disclosure, immediate feedback, accessibility.
- CRO/signup/onboarding/pricing playbooks: value clarity, field reduction, CTA hierarchy, trust, activation, pricing anxiety.
- Established UX laws: Nielsen heuristics, Hick's Law, Fitts's Law, Miller's Law, Jakob's Law, Baymard checkout findings, WCAG target sizing.
- Local cli-* ergonomics: ask once, derive the rest, use defaults, recap before apply, make re-runs safe and stateful.
- Material/GOV.UK patterns: one primary action, explicit states, confirmation/acknowledgement, check answers, back/change/resume behavior.

Read `references/principles.md` when you need the detailed rule table, scorecard, numeric thresholds, and pattern catalog.

## Workflow

### 1. Classify the Flow

Identify the flow type before making changes:

| Flow | User intent | Main risk |
|------|-------------|-----------|
| Checkout/order | Complete purchase | Abandonment from friction or mistrust |
| Pricing/plan picker | Choose the right offer | Choice anxiety, hidden constraints |
| Signup/trial | Create account | Too many fields before value |
| Onboarding/setup | Reach first value | Tutorial fatigue, blank-slate confusion |
| Settings/config | Change behavior safely | Fear of breaking things |
| Product configurator | Build a valid option set | Invalid combinations, overload |
| Wizard | Complete guided setup | Asking too much too early |
| Resource lifecycle | Create, edit, clone, resize, delete a resource | User loses context between operations |

If the flow is unclear, infer from route names, copy, component names, screenshots, or user context. Ask only if ambiguity changes the solution materially.

### 2. Map the Decision Load

For each step/screen, list:
- **Required decisions:** must happen now to progress.
- **Derivable decisions:** can be inferred from data, environment, prior answers, defaults, or user profile.
- **Deferrable decisions:** can happen after purchase/signup/activation.
- **Advanced decisions:** should be hidden behind "Advanced", "Customize", or expert mode.

Rule: if a decision is not required now, do not put it in the main path.

### 3. Preserve the User's Mental Model

For lifecycle resources (VMs, projects, clusters, plans, subscriptions, accounts), design one reusable grammar across operations:

| Operation | Same UI grammar | Different safety layer |
|-----------|-----------------|------------------------|
| Create | Same sections, labels, defaults, summary | Explain new resource impact |
| Edit/resize | Same sections pre-filled from current state | Show diff: before -> after |
| Clone | Same create flow pre-filled from source | Highlight inherited values |
| Delete/cancel | Same resource summary and naming | Require explicit destructive confirmation or undo |
| Restore/rollback | Same summary and status language | Show target restore point and data loss risk |

Do not make users relearn the UI for each operation. The screen may differ, but the vocabulary, section order, summary panel, validation, state labels, and primary/secondary action hierarchy should stay consistent.

Borrow the local CLI ergonomics laws for UI:
- **Ask once:** never ask again for values already known; prefill and carry forward.
- **Defaults are decisions:** every default should produce a useful, safe result.
- **Recap before apply:** show a review/diff before creating, resizing, deleting, or billing.
- **Re-run safe:** returning to the flow restores prior state, not a blank form.

### 4. Apply the 7 Friction Cuts

Work in this order:

1. **Clarify value:** user can say what they get and what happens next.
2. **Reduce choices:** group, recommend, default, or defer options.
3. **Reduce fields:** remove, infer, prefill, combine, or ask later.
4. **Strengthen CTA hierarchy:** one primary action per decision region.
5. **Prevent errors:** constraints, inline validation, valid defaults, reversible actions.
6. **Add feedback:** loading, saving, selected, invalid, success, progress.
7. **Build trust:** price clarity, security/privacy cues, no surprise fees, confirmation recap.

### 5. Design the Main Path First

The main path should feel like:

```
Recognize goal -> choose recommended path -> verify recap -> commit -> recover if needed
```

Prefer these moves:
- Recommended option with explicit reason.
- Smart defaults from context.
- Guest checkout where possible.
- "Full name" instead of first/last unless legally required.
- Single email field; no confirmation duplicate.
- Visible labels, not placeholder-only labels.
- Optional account creation after purchase, not before checkout.
- Basic settings visible, advanced collapsed.
- Inline edit for simple settings; full form only for complex edits.
- Recap before destructive or costly apply.

### 6. Use Math as Constraint, Not Decoration

Use proven interaction math first:
- **Hick:** fewer competing choices reduce decision time.
- **Fitts:** larger/closer targets are faster and safer.
- **Miller/chunking:** group fields and options into small meaningful sets.
- **Tesler:** complexity cannot disappear; move it from user decision time into system defaults, validation, and progressive disclosure.

Use visual math second:
- 4/8 px spacing scale for rhythm.
- Type scale around 1.2-1.333 for hierarchy.
- 45-75 characters per text line.
- Touch targets: 44 px preferred; 24 px absolute WCAG 2.2 minimum where space constrained.
- Golden ratio may inspire composition, but never outranks usability, accessibility, responsiveness, or clarity.

### 7. Audit Output

When auditing, produce:

```markdown
## Choice UX Report

**Flow:** [checkout / pricing / signup / settings / configurator / wizard]
**Primary action:** [what user must complete]
**Main blocker:** [top friction source]

### Score

| Dimension | Score /10 | Notes |
|-----------|-----------|-------|
| Decision Load |  |  |
| Field Friction |  |  |
| CTA Clarity |  |  |
| Error Prevention |  |  |
| Feedback & State |  |  |
| Trust & Reassurance |  |  |
| Accessibility |  |  |
| Lifecycle Consistency |  |  |

### Must Fix
- [impact] [fix] [location if available]

### Should Fix
- [impact] [fix] [location if available]

### Nice To Test
- [hypothesis] [metric]

### Proposed Flow
1. [step]
2. [step]
3. [step]

### Copy / UI Rewrites
- CTA: "[old]" -> "[new]"
- Label: "[old]" -> "[new]"
- Error: "[old]" -> "[new]"
```

### 8. Implementation Rules

When editing code:
- Preserve existing framework, component library, tokens, and routing.
- Use existing design-system primitives before creating new components.
- Keep changes close to the flow under review.
- Do not add decorative cards, hero sections, or marketing copy unless the flow needs them.
- Add visible focus states, semantic controls, proper labels, and usable disabled/loading/error states.
- Verify responsive behavior if the project has a runnable frontend.

## Decision Gate

Before finalizing, confirm:
- Main path has only one primary CTA per step.
- Every required field is justified.
- Every optional/advanced choice is hidden or deferred.
- User always knows current state, next step, and how to recover.
- Create/edit/delete/clone flows reuse the same vocabulary, section order, summary, and state model.
- Checkout/signup/settings can be completed by keyboard.
- Mobile targets and text fit without overlap.
- Visual hierarchy guides the eye without relying on decoration.

## Handoffs

| Need | Recommend |
|------|-----------|
| General frontend polish | `frontend-design` or a project design system |
| Technical UI best-practice audit | Vercel-style web interface checklist |
| Marketing page copy/CRO beyond the flow | CRO/copywriting skill |
| Config wizard lifecycle | `/cli-audit-wizard` |
| Performance bottleneck | `/cli-forge-perf` |

Recommend handoffs; do not auto-run them unless the user asks.

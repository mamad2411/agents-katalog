---
name: estimating-accessibility-effort
description: Use this skill to estimate the effort required to remediate accessibility issues. Triggers when sizing accessibility work for a sprint, estimating how long a WCAG fix will take, scoping remediation work, or planning accessibility improvements.
---

# Estimating Accessibility Effort

Estimate the effort required to remediate accessibility issues. Given a set of findings — from an audit, automated scan, user report, or backlog — produce effort estimates that help with planning. This is a planning skill; it does not fix the issues.

## Inputs

This skill expects one or more accessibility issues to estimate. These may come from:

- An accessibility audit report (from `reviewing-accessibility` or a manual audit)
- axe-core scan results
- GitHub issues labelled as accessibility
- A backlog of known accessibility problems
- A VPAT or compliance gap analysis

For each issue, the input should ideally include: what the problem is, where it occurs, and which WCAG criterion it violates. If the input is sparse (e.g., "fix keyboard navigation on the settings page"), gather context by reading the affected code before estimating.

## Read the code first

Effort estimates based only on the issue description are unreliable. Before estimating, read the actual implementation:

1. **Find the affected files** — locate the components, pages, or templates where the issue exists.
2. **Assess the current state** — is there partial accessibility support that needs fixing, or is it entirely absent?
3. **Identify dependencies** — does the fix require changes to shared components, layouts, state management, or backend data? Fixes that cross module boundaries take longer.
4. **Check for repetition** — does the same issue appear in multiple places? A missing label on one form field is different from missing labels across 15 forms using the same component.

## Estimate each issue

For each issue, produce:

| Field | Description |
|-------|-------------|
| **Issue** | One-sentence description of the problem |
| **WCAG** | Success criterion reference (e.g., 2.1.1 Keyboard) |
| **Severity** | Critical (A violation, blocker), Serious (AA violation), Moderate (best practice) |
| **Scope** | How many files, components, or pages are affected |
| **Effort** | T-shirt size: XS, S, M, L, XL (see definitions below) |
| **Rationale** | Brief explanation of what the fix involves and why it takes this much effort |
| **Dependencies** | Other issues or changes this fix depends on or enables |

### Effort definitions

| Size | Typical scope | Examples |
|------|--------------|---------|
| **XS** | Single attribute or property change. One file, no logic changes. | Add missing `alt` text, add `aria-label` to a button, add `autocomplete` attribute, add `lang` attribute |
| **S** | Localised change within one component. May involve a few attributes and minor template restructuring. | Associate error messages with fields via `aria-describedby`, add visible labels to replace placeholder-only labels, add `aria-live` to a status region |
| **M** | Changes to one component plus its consumers, or changes spanning 2-5 files. May require new state management. | Implement keyboard navigation for a custom widget, add focus management to a modal (trap + return), make a data table sortable by keyboard, add skip link |
| **L** | Structural changes affecting multiple components or a shared layout. May require new components, hooks, or utility functions. | Redesign a drag-and-drop interface to have a keyboard alternative, retrofit focus management across all route changes, build an accessible combobox to replace a custom dropdown |
| **XL** | Architectural changes. Affects the application's structure, routing, state management, or component library. Usually a multi-day effort. | Replace a custom component system with an accessible component library, restructure page layouts for correct landmark hierarchy across all routes, implement a comprehensive form error handling system |

### Factors that increase effort

- **Shared components**: A fix to a shared component is small in code but high in risk — it affects every consumer. Testing effort scales with usage count.
- **Missing patterns**: If the codebase has no existing pattern for the fix (e.g., no focus management utilities, no live region conventions), the first fix includes establishing the pattern. Subsequent similar fixes are smaller.
- **Test coverage**: If the fix needs new tests (it usually does), include test authoring in the estimate. Accessibility tests often require Playwright for integration-level assertions, not just unit tests.
- **Multi-theme**: Contrast fixes need verification in every supported theme. Double the verification effort for each additional theme.
- **Third-party components**: Fixes inside third-party component internals may require forking, wrapping, or replacing the component rather than a simple attribute change.
- **Dynamic content**: Issues involving dynamic state (live regions, focus management after async operations, error announcements) are harder than static markup fixes because they require understanding the component's lifecycle.

### Factors that decrease effort

- **Component library handles it**: If the project uses a headless UI library that already implements the ARIA pattern, the fix may be as simple as passing the correct props.
- **Pattern already exists**: If the codebase already has a focus management utility, a live region component, or an error handling convention, applying it to a new location is faster.
- **Single occurrence**: An issue that appears in one place with no shared component implications.

## Batch estimation

When estimating a set of issues (e.g., a full audit report), also provide:

### Summary table

| Effort | Count | Examples |
|--------|-------|---------|
| XS | n | ... |
| S | n | ... |
| M | n | ... |
| L | n | ... |
| XL | n | ... |

### Dependency graph

If issues depend on each other, note the order. Common patterns:

- "Establish focus management utility (L)" must come before "Add focus return to all modals (S each)"
- "Add `aria-describedby` error association" depends on "Implement error message components"
- "Fix landmark structure" should come before "Add skip link" (the skip link needs a target)

### Quick wins

Highlight issues that are XS or S effort with Critical or Serious severity. These deliver the most accessibility improvement per unit of effort and are good candidates for immediate action.

## Report format

```markdown
## Accessibility Effort Estimate - [scope]

### Individual Estimates

| Issue | WCAG | Severity | Scope | Effort | Rationale |
|-------|------|----------|-------|--------|-----------|
| ... | ... | ... | ... | ... | ... |

### Summary

| Effort | Count |
|--------|-------|
| XS | n |
| S | n |
| M | n |
| L | n |
| XL | n |

### Dependencies

- [issue A] must be completed before [issue B] because [reason]

### Quick Wins

- [issue] (XS/S effort, Critical/Serious severity) - [what to do]
```

## Gotchas

- **Do not estimate without reading the code.** An issue that sounds simple ("add keyboard support") might be trivial (the component library already handles it) or enormous (the widget is entirely custom with mouse-only interactions). The code determines the estimate, not the issue title.
- **Estimates are not commitments.** T-shirt sizes communicate relative effort, not hours or days. The same "M" fix takes different wall-clock time depending on developer familiarity, test infrastructure, and review process. Frame estimates as relative sizing, not delivery promises.
- **First-of-kind fixes are larger than they appear.** The first focus management fix, the first live region, the first keyboard navigation pattern — each establishes a convention that subsequent fixes can follow. Estimate the first instance higher and note that follow-on instances will be smaller.
- **Test effort is part of the fix.** An accessibility fix without corresponding tests will regress. Include test authoring in every estimate, especially for dynamic behaviour (focus management, ARIA state changes, error announcements).
- **Shared component fixes need integration testing.** Changing a shared `<Button>` or `<Dialog>` component to fix an accessibility issue affects every page that uses it. The code change may be small, but the testing surface is the entire usage footprint.
- **Some issues are cheaper to fix together.** Adding `aria-describedby` to 10 form fields is not 10x the effort of doing one — it is 1x to establish the pattern plus 10x a trivial application. Group related issues when estimating batches.
- **Replacing a component is sometimes cheaper than fixing it.** If a custom widget has fundamental accessibility problems (no ARIA pattern, no keyboard model, no focus management), switching to an accessible component library may be less total effort than retrofitting accessibility onto the custom implementation.

---
name: accessibility-review
description: >
  Run a WCAG accessibility audit on a design, component, or page.
  TRIGGER when: user says "accessibility audit", "a11y review", "WCAG check",
  "is this accessible", or asks about color contrast, screen readers, keyboard navigation, or ARIA.
argument-hint: "[file, URL, or component name]"
user-invocable: true
---

# Accessibility Review

Perform a structured WCAG 2.2 accessibility audit. Evaluate designs, components, or implementations against established standards and produce actionable findings.

## Audit Framework

Evaluate against these WCAG 2.2 conformance levels, in order of priority:

### Level A — Minimum (must fix)

| Criterion | What to Check |
|---|---|
| 1.1.1 Non-text Content | Every image, icon, and visual element has a text alternative |
| 1.3.1 Info and Relationships | Structure (headings, lists, tables) is programmatically determinable, not just visual |
| 1.3.2 Meaningful Sequence | Reading order matches visual order |
| 1.4.1 Use of Color | Color is not the only means of conveying information |
| 2.1.1 Keyboard | All functionality is operable via keyboard |
| 2.4.1 Bypass Blocks | Skip navigation or landmark regions exist |
| 2.4.2 Page Titled | Pages have descriptive titles |
| 3.1.1 Language of Page | `lang` attribute is set |
| 3.3.1 Error Identification | Errors are identified and described in text |
| 4.1.2 Name, Role, Value | All UI components have accessible names and roles |

### Level AA — Standard (should fix)

| Criterion | What to Check |
|---|---|
| 1.4.3 Contrast (Minimum) | Text: 4.5:1 ratio. Large text (18px+ bold or 24px+): 3:1 |
| 1.4.4 Resize Text | Content is readable at 200% zoom without loss of functionality |
| 1.4.11 Non-text Contrast | UI components and graphics: 3:1 ratio against adjacent colors |
| 2.4.6 Headings and Labels | Headings and labels describe topic or purpose |
| 2.4.7 Focus Visible | Keyboard focus indicator is visible |
| 3.2.3 Consistent Navigation | Navigation is consistent across pages |
| 3.3.2 Labels or Instructions | Form inputs have labels or instructions |

### Level AAA — Enhanced (nice to have)

| Criterion | What to Check |
|---|---|
| 1.4.6 Contrast (Enhanced) | Text: 7:1 ratio. Large text: 4.5:1 |
| 2.4.10 Section Headings | Content is organized with section headings |
| 3.2.5 Change on Request | Changes of context are initiated only by user request |
| 3.3.5 Help | Context-sensitive help is available |

## Audit Process

### Phase 1 — Scope

1. Identify what's being audited: a design file, a component, a page, or an entire flow.
2. Determine the target conformance level (default: **AA**).
3. If `$ARGUMENTS` references a file, read it. If it references a component, find it in the codebase.

### Phase 2 — Automated Checks (for code)

If auditing implementation code (HTML/JSX/TSX):

1. Search for images without `alt` attributes.
2. Check for `aria-*` attributes on interactive elements.
3. Verify form inputs have associated `<label>` elements or `aria-label`.
4. Check heading hierarchy (`h1` -> `h2` -> `h3`, no skips).
5. Look for `role` attributes on custom interactive elements.
6. Check for `:focus` / `focus-visible` styles in CSS.
7. Verify `tabindex` usage (avoid positive values).
8. Check color values against WCAG contrast formulas.

### Phase 3 — Manual Review Checklist

For designs or areas that can't be automated:

- [ ] **Keyboard navigation**: Can every interactive element be reached and operated with keyboard alone?
- [ ] **Screen reader flow**: Does the reading order make sense without visual layout?
- [ ] **Touch targets**: Are interactive elements at least 44x44 CSS pixels?
- [ ] **Motion**: Are animations respectful of `prefers-reduced-motion`?
- [ ] **Error states**: Are errors clearly communicated without relying solely on color?
- [ ] **Loading states**: Are loading indicators announced to assistive technology?
- [ ] **Responsive**: Does the layout work at 320px viewport width?
- [ ] **Zoom**: Is content usable at 400% zoom?

### Phase 4 — Report

Output a structured report:

```
## Accessibility Audit — {component/page name}

**Target**: WCAG 2.2 Level AA
**Scope**: {what was audited}
**Date**: {today}

### Critical (Level A violations)
- [{criterion}] {description of issue}
  - **Location**: {file:line or design element}
  - **Impact**: {who is affected and how}
  - **Fix**: {specific remediation}

### Major (Level AA violations)
- [{criterion}] {description}
  - **Location**: ...
  - **Impact**: ...
  - **Fix**: ...

### Advisory (Best practices & AAA)
- {recommendation}

### Passed
- {list of criteria that passed}

### Summary
- Critical: {N} | Major: {N} | Advisory: {N} | Passed: {N}
```

## Severity Classification

| Severity | Definition | Action |
|---|---|---|
| Critical | Blocks access for one or more disability groups | Must fix before release |
| Major | Significantly degrades experience for assistive tech users | Should fix before release |
| Advisory | Enhancement that improves experience but doesn't block access | Fix when possible |

## Common Patterns & Fixes

Reference these when recommending fixes:

- **Missing alt text**: Use descriptive alt for informational images, `alt=""` for decorative
- **Low contrast**: Use a tool to find the nearest accessible color — don't just say "increase contrast"
- **Missing focus styles**: Add `outline` or custom focus indicator, never `outline: none` without replacement
- **Missing labels**: Prefer visible `<label>` over `aria-label` — visible labels help everyone
- **Custom controls**: Use native HTML elements where possible; if custom, implement full ARIA pattern
- **Dynamic content**: Use `aria-live` regions for content that updates without page reload

## Edge Cases

- If input data is incomplete, state assumptions explicitly and flag gaps
- For time-sensitive situations, prioritize speed over comprehensiveness
- If multiple stakeholders have conflicting needs, document the tradeoffs
- For first-time use, start with a simplified version and iterate
- Adapt the depth and detail to the audience's expertise level

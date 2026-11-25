---
name: accessibility-review
description: Reviews UI components and HTML for accessibility issues based on WCAG 2.1 AA standards. Use when the user says "check accessibility", "is this accessible", "WCAG review", "a11y audit", "fix accessibility issues", or pastes a React component, HTML, or JSX and asks for accessibility feedback.
---

# Accessibility Review

Audits UI code against WCAG 2.1 AA standards. Finds missing ARIA attributes,
keyboard navigation issues, focus management problems, color contrast gaps,
and semantic HTML errors — with copy-paste fixes for each finding.

---

## Required Details

| Detail | Example |
|---|---|
| **Code to review** | React component, HTML, or JSX |
| **Component type** | Modal, form, button, nav, table, etc. |
| **Interactive?** | Yes (has click/keyboard events) / No |
| **WCAG level target** | AA (default) / AAA |

---

## Instructions

### Step 1 — Audit across six areas

**1. Semantic HTML**
- Headings in correct order (`h1` → `h2` → `h3`, no skipping)
- Interactive elements use native tags (`button` not `div onClick`)
- Lists use `ul`/`ol`/`li`, tables use `th` with `scope`
- Landmarks present: `main`, `nav`, `header`, `footer`

**2. ARIA**
- `aria-label` or `aria-labelledby` on icons, icon buttons, and unlabeled controls
- `aria-expanded`, `aria-controls` on toggles and accordions
- `aria-live` on dynamic content (toasts, status messages)
- No redundant ARIA (`role="button"` on a `<button>`)
- `aria-hidden="true"` on decorative elements

**3. Keyboard Navigation**
- All interactive elements reachable by Tab
- Focus order matches visual order
- Custom components handle: Enter, Space, Arrow keys, Escape
- No keyboard traps (except intentional modal traps)

**4. Focus Management**
- Focus moves to modal/dialog when opened
- Focus returns to trigger when modal closes
- Skip link present for long navigation (`<a href="#main">Skip to content</a>`)
- Focus indicators visible — never `outline: none` without a replacement

**5. Color and Contrast**
- Text contrast ≥ 4.5:1 for normal text (AA)
- Text contrast ≥ 3:1 for large text (18px+ or 14px bold)
- Information not conveyed by color alone
- Error states use icon or text, not just red color

**6. Images and Media**
- All `<img>` have `alt` — empty `alt=""` for decorative images
- Complex images have extended descriptions
- Videos have captions, audio has transcripts

### Step 2 — Assign severity

| Severity | Meaning |
|---|---|
| 🔴 Critical | Blocks users with disabilities entirely |
| 🟠 High | Significantly impairs access — WCAG AA failure |
| 🟡 Medium | Partial barrier — degrades experience |
| 🔵 Low | Best practice — not a strict WCAG failure |

### Step 3 — Format each finding

```
[severity] Area — Short title

Issue: [what is wrong and which users it affects]
WCAG: [criterion number and name, e.g. 1.1.1 Non-text Content]
Fix:
```jsx
[accessible version of the code]
```
```

---

## Non-Negotiable Acceptance Criteria

- [ ] Every finding references the relevant WCAG criterion
- [ ] Every finding includes a code fix — not just a description
- [ ] Critical findings (blocks keyboard or screen reader users) are listed first
- [ ] If a category has no issues, state "No issues found" — never skip it
- [ ] Decorative images are explicitly checked for empty `alt=""`

---

## Output Format

~~~
## Accessibility Review

### Summary
[Overall assessment: WCAG AA compliant / fails on X criteria / needs work]

### Findings

[ordered by severity]

### Passed Checks
[categories with no issues]

### Verdict
- [ ] Fails WCAG 2.1 AA — fix Critical/High before release
- [ ] Passes with minor improvements recommended
- [ ] Fully compliant
~~~
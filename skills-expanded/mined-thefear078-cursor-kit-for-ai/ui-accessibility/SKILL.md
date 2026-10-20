---
name: ui-accessibility
description: WCAG 2.2 accessibility audit — keyboard navigation, focus management, ARIA misuse, color contrast, reduced motion, screen reader labels, and form associations. Use when auditing UI for a11y compliance, before launch, or when users report accessibility issues.
---

# UI Accessibility

WCAG 2.2–aligned accessibility audit for web UI. Accessibility failures are **Blockers** for user-facing features — not polish. Test with keyboard and code review; flag what needs manual screen reader verification.

## When Invoked

1. Determine scope: component, page, flow (login, checkout), or full app.
2. Run automated checks first (commands below), then manual keyboard walkthrough.
3. Audit against WCAG categories below — map findings to WCAG criterion numbers.
4. Report with severity, WCAG reference, file:line, and fix.

## Phase 1: Automated Checks

Run before manual review:

```bash
# axe-core via CLI (if installed)
npx @axe-core/cli http://localhost:3000 --exit

# Find images missing alt
rg '<img[^>]*(?!alt=)[^>]*>' src/ -n

# Find buttons without accessible names
rg '<button[^>]*>\s*<(Icon|Svg|svg|[^>]*class="[^"]*icon)' src/ -n

# Find inputs without associated labels
rg '<(input|select|textarea)[^>]*>' src/ -n
# Cross-check: no <label htmlFor= matching id

# Find positive tabindex (anti-pattern)
rg 'tabIndex=\{?[1-9]' src/ -n

# Find aria-hidden on focusable elements
rg 'aria-hidden="true"[^>]*(button|a |input|select|textarea)' src/ -n

# Find role="presentation" on meaningful content
rg 'role="presentation"' src/ -n

# Find onClick on non-interactive elements without keyboard handler
rg '<(div|span)[^>]*onClick' src/ -n
```

## Phase 2: Keyboard Navigation (WCAG 2.1.1, 2.1.2, 2.4.3, 2.4.7)

Test every interactive flow with keyboard only — no mouse.

### Keyboard Test Protocol

1. Tab through entire page — every interactive element reachable?
2. Tab order follows visual/logical order?
3. Shift+Tab reverses correctly?
4. Enter/Space activates buttons and links?
5. Escape closes modals, dropdowns, popovers?
6. Arrow keys work in menus, tabs, radio groups, listboxes?
7. No keyboard trap — can Tab out of every component?
8. Skip link present — first Tab reaches "Skip to main content"?

### Focus Management Rules

| Scenario | Required behavior |
|----------|----------------|
| Modal opens | Focus moves to modal; focus trapped inside |
| Modal closes | Focus returns to trigger element |
| Route change | Focus moves to `<h1>` or main landmark |
| Dropdown opens | Focus moves to first item |
| Item deleted from list | Focus moves to logical successor |
| Error on submit | Focus moves to first invalid field |
| Toast appears | Does NOT steal focus; uses `aria-live` |

### Focus Visible (2.4.7)

- Every interactive element shows visible focus indicator
- `:focus-visible` preferred over `:focus` — no ring on mouse click
- Never `outline: none` without replacement (`focus-visible:ring-2`, custom box-shadow)
- Focus indicator contrast ≥ 3:1 against adjacent colors (WCAG 2.2 SC 2.4.11 Focus Appearance)
- Sticky headers/overlays must not obscure focused element

```css
/* Minimum viable focus */
:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}
```

### Keyboard Findings Template

```markdown
### Keyboard Issues
| File:Line | WCAG | Issue | Repro steps | Fix |
|-----------|------|-------|-------------|-----|
| Modal.tsx:45 | 2.4.3 | Tab escapes modal to background | Open modal → Tab past last button | Add focus trap |
| Nav.tsx:12 | 2.4.1 | Dropdown not keyboard operable | Tab to nav → Enter does nothing | Add onKeyDown handler |
```

## Phase 3: Screen Reader & ARIA (WCAG 4.1.2)

### Semantic HTML First

Before adding ARIA, check if native HTML solves it:

| Need | Use | Not |
|------|-----|-----|
| Button | `<button>` | `<div role="button">` |
| Link | `<a href>` | `<span onClick>` |
| Heading | `<h1>`–`<h6>` | `<div role="heading">` |
| List | `<ul>`/`<ol>` | `<div role="list">` |
| Checkbox | `<input type="checkbox">` | custom div |
| Navigation | `<nav>` | `<div role="navigation">` |

**First rule of ARIA: don't use ARIA if native HTML works.**

### ARIA Patterns (when native HTML insufficient)

| Pattern | Required ARIA |
|---------|--------------|
| Icon button | `aria-label="Close"` or visually hidden text |
| Toggle button | `aria-pressed="true/false"` |
| Expandable section | `aria-expanded` + `aria-controls` |
| Tab panel | `role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected` |
| Live region (toast) | `aria-live="polite"` or `aria-live="assertive"` |
| Loading | `aria-busy="true"` on container |
| Current page in nav | `aria-current="page"` |
| Describedby for errors | `aria-describedby` pointing to error element id |
| Invalid field | `aria-invalid="true"` |

### ARIA Misuse (always flag)

| Misuse | Why | Fix |
|--------|-----|-----|
| `aria-label` on non-interactive element with no role | Ignored by AT | Add role or use native element |
| `role="button"` without keyboard handler | Not operable | Add `onKeyDown` for Enter/Space |
| `aria-hidden="true"` on focusable child | Child still in tab order | Use `inert` or `tabIndex={-1}` on children |
| Redundant `role` on semantic element | Noise | Remove `role="button"` from `<button>` |
| `aria-labelledby` pointing to nonexistent id | Broken reference | Fix id or remove |
| `alt` on decorative image | Noise | `alt=""` or `role="presentation"` |
| `tabindex="0"` on non-interactive to "make it focusable" | Wrong pattern | Use `<button>` or add `role` + handlers |

### Screen Reader Labels

Every interactive element needs an **accessible name** (what AT announces):

1. Visible text content (preferred)
2. `aria-label` (icon buttons, no visible text)
3. `aria-labelledby` (references visible label element)
4. `<label htmlFor>` (form controls)

```tsx
// Good — icon button
<button aria-label="Delete item">
  <TrashIcon aria-hidden="true" />
</button>

// Good — form field
<label htmlFor="email">Email</label>
<input id="email" type="email" name="email" autoComplete="email" />
```

## Phase 4: Color & Contrast (WCAG 1.4.3, 1.4.11, 1.4.1)

### Contrast Requirements

| Content type | Minimum ratio | WCAG level |
|-------------|---------------|------------|
| Normal text (<18px / <14px bold) | 4.5:1 | AA |
| Large text (≥18px / ≥14px bold) | 3:1 | AA |
| UI components & graphical objects | 3:1 | AA (1.4.11) |
| Focus indicator | 3:1 | AA (2.4.11) |
| Enhanced (optional) | 7:1 / 4.5:1 | AAA |

### Common Failures

- Light gray `#999` text on white `#FFF` — ~2.8:1, fails AA
- Placeholder text as only label — low contrast + not persistent
- Disabled buttons with no visual distinction beyond color
- Chart colors distinguishable only by hue — add patterns, labels, or icons
- Error state indicated by red border only — add icon + text (1.4.1 Use of Color)

### Verification

```bash
# Find low-contrast Tailwind classes (common offenders)
rg 'text-gray-400|text-gray-300|text-slate-400' src/ -n

# Find color-only state indicators
rg 'border-red|text-red|bg-red' src/ -n  # check if paired with icon/text
```

Use browser DevTools → Accessibility pane → contrast ratio, or WebAIM Contrast Checker.

## Phase 5: Reduced Motion (WCAG 2.3.3)

Users with `prefers-reduced-motion: reduce` must not experience unnecessary animation.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Motion Audit Checklist

- [ ] CSS animations respect `prefers-reduced-motion`
- [ ] JS animation libraries check `matchMedia('(prefers-reduced-motion: reduce)')`
- [ ] Auto-playing video/carousel has pause control
- [ ] Parallax scrolling disabled under reduced motion
- [ ] Page transitions (SPA) have instant fallback
- [ ] Loading spinners acceptable (essential feedback, not decorative)

```bash
# Find animations without reduced-motion guard
rg '@keyframes|animation:|transition:' src/ -n
# Manually verify each has prefers-reduced-motion override
```

## Phase 6: Forms (WCAG 1.3.1, 3.3.1, 3.3.2, 3.3.3, 4.1.2)

### Form Association Rules

- Every input has a `<label>` with matching `htmlFor`/`id`, or `aria-label`
- Required fields: `required` attribute + visual indicator (not color alone) + `aria-required="true"`
- Error messages: `aria-describedby` links input to error text; `aria-invalid="true"` on failure
- Error messages state the problem AND how to fix (3.3.3)
- Group related fields: `<fieldset>` + `<legend>` for radio/checkbox groups
- Autocomplete attributes on personal data fields (`autocomplete="email"`, etc.)

```tsx
<div>
  <label htmlFor="password">Password</label>
  <input
    id="password"
    type="password"
    aria-describedby={error ? "password-error" : undefined}
    aria-invalid={!!error}
    autoComplete="current-password"
  />
  {error && <p id="password-error" role="alert">{error}</p>}
</div>
```

### Form Anti-Patterns

| Anti-pattern | WCAG | Fix |
|-------------|------|-----|
| Placeholder as only label | 3.3.2 | Add visible `<label>` |
| Error only in red border | 1.4.1 | Add text + icon |
| `onPaste` preventDefault | Best practice | Remove — blocks password managers |
| CAPTCHA without alternative | 1.1.1 | Offer audio CAPTCHA or alternative auth |
| Timeout without warning | 2.2.1 | Warn + extend option |

## Severity Model

| Level | WCAG conformance | Action |
|-------|-----------------|--------|
| **Blocker** | Fails A (critical) | Cannot ship — keyboard trap, no accessible name on primary action, contrast <3:1 on body text |
| **Major** | Fails AA | Fix before release — missing labels, no focus visible, ARIA misuse, missing skip link |
| **Minor** | Best practice / AAA | Fix when touching — enhanced contrast, redundant ARIA, suboptimal live region |
| **Pass** | Meets AA | Note in report |

## Output Format

```markdown
## Accessibility Audit: [page/component]

**Scope:** [files/flows tested]
**WCAG target:** AA
**Verdict:** ✅ Pass / 🔶 Fix majors / ❌ Blocked

### Blockers
| File:Line | WCAG SC | Issue | Fix |

### Major
| File:Line | WCAG SC | Issue | Fix |

### Minor
- `file:line` — SC X.X.X: issue → fix

### Keyboard Test Results
- Tab order: pass/fail
- Focus visible: pass/fail
- Modal focus trap: pass/fail
- Skip link: present/missing

### Needs Manual Screen Reader Test
- [items that require NVDA/VoiceOver verification]

### Passes
- [what works well — max 3]
```

## Anti-Patterns (auditor behavior)

- Don't rely only on automated tools — axe catches ~30-40% of issues
- Don't add ARIA to "fix" semantic HTML gaps — fix the HTML
- Don't test with mouse only — keyboard test is mandatory
- Don't mark pass without checking focus management in modals
- Don't ignore `prefers-reduced-motion` — it's AA in WCAG 2.2
- Don't conflate this with `web-design-guidelines` — that covers broader UI rules; this is WCAG depth

## Cross-References

- Broader UI interaction rules → `web-design-guidelines`
- Visual design contrast tokens → `frontend-design`
- Browser-based keyboard testing → `agent-browser`
- Focus management in compound components → `react-composition`
- React-specific a11y patterns → `react-best-practices`

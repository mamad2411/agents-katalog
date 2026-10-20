---
name: accessibility-a11y-checklist
description: >
  Frontend accessibility (a11y) testing checklist at WCAG high level: semantic HTML,
  keyboard, focus, names/roles, contrast, forms, media, and ARIA discipline. Use when
  accessibility, a11y, 无障碍, WCAG, screen reader, keyboard navigation, ARIA, focus trap,
  color contrast, or accessible UI review. Complements code-quality-standards; does not
  replace product design systems or legal conformance audits.
---

# Accessibility (a11y) Checklist

## Scope And Authorization

- **In scope:** web/apps your team owns or is hired to improve; staging and local builds preferred.
- **Out of scope:** claiming legal WCAG conformance without a formal audit process; “fixing” third-party sites at scale without permission.
- Treat user research recordings as sensitive; redact when filing bugs.
- Pair UI code fixes with `code-quality-standards` and relevant frontend skills.

## When To Use

- PR review or release checklist for UI features (modals, forms, tables, navigation).
- Fixing axe/Lighthouse accessibility findings.
- Establishing team Definition of Done for keyboard and screen-reader basics.
- Auditing ARIA usage (especially custom widgets).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| React component structure | `react-component-patterns` |
| General state management | `state-management-guidelines` |
| i18n / l10n | `i18n-l10n-guidelines` |
| Error copy UX writing | `error-message-ux-writing` |
| CSP / XSS hardening | `ace-editor-csp` / XSS skills as relevant |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus (WCAG-oriented)

| Area | Target | Common failure |
| --- | --- | --- |
| Semantics | Real `<button>`, headings hierarchy, lists, landmarks | `div` click handlers only |
| Keyboard | All actions reachable; no keyboard traps | Modal focus not trapped/restored |
| Name / role / value | Accessible name via content, `aria-label`, or labelledby | Icon-only control with no name |
| Contrast | Text/UI components meet contrast goals (org standard) | Gray on gray placeholders |
| Forms | Visible labels, errors tied via `aria-describedby` | Placeholder-only labels |
| Media | Captions/transcripts; no autoplay audio surprises | Video without captions |
| ARIA | First rule: don’t use ARIA if native works | Wrong roles, dual labels |
| Motion | Respect `prefers-reduced-motion` | Required parallax only |

## Workflow

### 1. Confirm scope and success criteria

1. Record pages/flows, target WCAG level **as org policy** (often AA), browsers/AT matrix.
2. Success: critical user journeys keyboard-complete; axe serious+ empty on scoped pages; SR smoke pass.
3. Note design-system components already vetted vs one-off widgets.

### 2. Automated baseline

```bash
# Local or staging URL
npx @axe-core/cli http://localhost:3000 --exit
npx @axe-core/cli http://localhost:3000/settings --tags wcag2a,wcag2aa

# Lighthouse CI / CLI (accessibility category)
npx lighthouse http://localhost:3000 --only-categories=accessibility --quiet --chrome-flags="--headless"
```

1. File issues with rule id, selector, and impact — do not stop at automation (covers ~30–50% of issues).
2. Add unit/RTL tests for accessible names where components are shared:

```bash
# Example: Jest/RTL projects often use jest-axe
npm test -- --testPathPattern=a11y
```

### 3. Keyboard pass (manual, mandatory)

| Check | How |
| --- | --- |
| Tab order | Logical, matches visual order |
| Focus visible | Clear focus ring not removed via `outline: none` without replacement |
| Activation | Enter/Space on buttons; arrows only when pattern requires |
| Skip link | Skip to main content works |
| Modal | Focus moves in; Tab cycles; Esc closes; focus returns |
| Menus/tabs | Arrow key pattern consistent with APG if custom |

```text
# Manual script
1. Unplug mouse / ignore pointer
2. Traverse primary nav → main task → logout
3. Open each dialog/dropdown once
```

### 4. Name, role, value and semantics

1. Prefer native elements: `<button>`, `<a href>`, `<label for>`, `<nav>`, `<main>`, `<table>` for tabular data.
2. Icon-only controls: `aria-label` or visually hidden text.
3. Images: meaningful `alt`; decorative `alt=""` / CSS background.
4. Live updates: polite `aria-live` regions for async errors/toasts (avoid spam).
5. Custom widgets: follow [ARIA Authoring Practices] patterns; verify roles with accessibility tree (Chrome DevTools → Accessibility).

### 5. Forms, errors, and status

```html
<!-- Good pattern sketch -->
<label for="email">Email</label>
<input id="email" type="email" aria-describedby="email-err" aria-invalid="true" />
<p id="email-err" role="alert">Enter a valid email.</p>
```

1. Do not rely on color alone for errors.
2. Disable submit UX should still explain why (and remain discoverable to AT).
3. Autocomplete attributes where appropriate (`autocomplete="username"`).

### 6. Visual, media, and motion

1. Check contrast for text and essential icons (design tokens / contrast tools).
2. Zoom 200%: layout usable without horizontal scrolling traps for main content.
3. Captions/transcripts for video/audio content you ship.
4. Honor `prefers-reduced-motion` for non-essential animation.

### 7. Screen reader smoke (sample)

| Platform | AT sample |
| --- | --- |
| Windows | NVDA + Chrome/Firefox |
| macOS | VoiceOver + Safari |
| Mobile | TalkBack / VoiceOver on staging build |

1. Navigate by headings and landmarks; confirm form labels spoken; confirm dialog titles.
2. Record short notes per journey — not a full legal audit unless commissioned.

### 8. Hand off

1. Bugs with severity (blocker: cannot complete task with keyboard/AT).
2. Fix in design system when pattern is reusable.
3. Re-run axe on changed routes; keep CI gate for serious violations if team agrees.

## Page Review Checklist

- [ ] Title unique and descriptive
- [ ] One `<h1>`; heading levels not skipped arbitrarily
- [ ] Landmarks: header/nav/main/footer as appropriate
- [ ] All interactive elements focusable and named
- [ ] Focus order matches visual reading order
- [ ] No keyboard trap
- [ ] Forms labeled; errors associated
- [ ] Tables: headers (`th`) for data tables
- [ ] Contrast meets team standard
- [ ] ARIA used only when needed and correctly
- [ ] Motion/media alternatives considered
- [ ] Automated scan clean of serious+ issues

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Controls | `<button>` with text | `<div onclick>` no role/tabindex |
| Focus | Visible focus styles | `outline: none` globally |
| ARIA | Native first | `aria-label` duplicating visible text messily + wrong role |
| Testing | axe + keyboard + SR smoke | Lighthouse score only |
| Modals | Focus trap + restore | Focus left on background page |

## Output Checklist

- [ ] Scope, pages, and target standard recorded
- [ ] Automated axe/Lighthouse (or equivalent) evidence attached
- [ ] Keyboard journey signed off
- [ ] Forms/modals/custom widgets reviewed in accessibility tree
- [ ] Contrast/zoom spot-checked
- [ ] SR smoke notes for critical paths
- [ ] Issues filed with owners; DS vs one-off classified
- [ ] CI regression considered for serious rules
- [ ] `code-quality-standards` applied to code fixes

## Rules

- Aim for usable accessibility, not score-gaming.
- This checklist is **engineering hygiene**, not a substitute for formal conformance audits where legally required.
- Prefer semantic HTML over ARIA sprawl.
- Do not block releases on theoretical perfection when critical tasks already fail — fix blockers first.
- Keep user recordings and AT notes privacy-safe.

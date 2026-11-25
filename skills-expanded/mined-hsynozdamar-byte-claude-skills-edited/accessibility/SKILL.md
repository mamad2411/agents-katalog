---
name: accessibility
description: "Web accessibility audit and fixes to WCAG 2.2. Use when asked for an a11y audit, WCAG compliance, screen reader support or keyboard navigation."
license: MIT
metadata:
  author: web-quality-skills
  version: "2.0"
---

# Accessibility (WCAG 2.2)

Make content usable by everyone. Target level AA (a legal requirement in many jurisdictions); A is the floor, AAA is optional. Organized by POUR: perceivable, operable, understandable, robust.

## Evidence-led workflow

With a rendered page:
1. Run a live Lighthouse Accessibility audit (Chrome DevTools MCP: `lighthouse_audit`). Use mobile navigation mode for a public page, or snapshot mode when reloading would lose authenticated or user-created state.
2. Localize each failed node to its component or template instead of grepping the repo for generic patterns.
3. Read the accessibility-tree snapshot (`take_snapshot`) for names, roles, states, landmarks and heading structure, and exercise the affected flow by keyboard.
4. Fix the source, then re-run the same audit and the same manual interaction.

Without live tools use Lighthouse CLI (`npx lighthouse <url> --only-categories=accessibility`) or axe (`@axe-core/cli`) plus the manual checks below. Automation catches only a subset of barriers: a score of 100 is not conformance, and a low score is no substitute for issue-level evidence.

## Rules that decide most findings

**Perceivable**
- Informative images get descriptive `alt`; decorative ones get `alt=""`. Icon-only buttons get an accessible name (`aria-label` or visually hidden text), with the icon `aria-hidden`.
- Contrast (1.4.3): 4.5:1 normal text, 3:1 large text (>= 18px, or >= 14px bold) and UI components/graphics (1.4.11). Focus indicators also need 3:1.
- Convey state with color plus icon plus text (1.4.1). Video needs captions and, where relevant, audio description; audio needs a transcript (1.2).

**Operable**
- Native `<button>`, `<a href>` and form controls first; they bring focusable, Enter/Space and semantics. A `div` button needs `role`, `tabindex="0"` and key handling, and adding that to a native button double-triggers.
- No keyboard traps (2.1.2); native `<dialog>` traps focus correctly.
- Focus visible (2.4.7): style `:focus-visible` with `outline: 2px solid currentColor; outline-offset: 2px`, and replace any `outline: none`.
- 2.2 additions: focus not obscured by sticky bars (2.4.11, add `scroll-margin`), dragging needs a single-pointer alternative (2.5.7), targets at least 24x24 CSS px (2.5.8; 44x44 recommended; exceptions for inline links, browser-sized controls, and spaced targets).
- Provide a skip link (2.4.1), a way to extend time limits (2.2), and `prefers-reduced-motion` support (2.3).

**Understandable**
- `lang` on `<html>` (3.1.1) and on foreign phrases; consistent navigation (3.2.3) and, new in 2.2, help mechanisms in the same relative order on every page (3.2.6).
- Every input has a programmatic label (3.3.2). Errors: `aria-invalid="true"`, message linked by `aria-describedby`, announced via `role="alert"`, focus moved to the first error (3.3.1, 3.3.3).
- Redundant entry (3.3.7): reuse information already given in the session. Accessible authentication (3.3.8): allow paste and autofill, or offer passkey, SSO or email link; object recognition or personal content is the only cognitive test allowed at AA.

**Robust**
- Native elements before ARIA. When ARIA is needed, use the complete pattern (roles, states, keyboard model; APG).
- Announce dynamic updates with `aria-live` regions instead of moving focus (4.1.3).

Markup, CSS and JS for each rule: [references/code-samples.md](references/code-samples.md). Patterns (modal focus trap, skip link, tabs, live regions, form labels, error handling, dragging, VoiceOver/NVDA commands): [references/A11Y-PATTERNS.md](references/A11Y-PATTERNS.md). Every criterion by level: [references/WCAG.md](references/WCAG.md).

## Manual checks

Keyboard through the whole page (Tab, Enter, Space); a screen reader (VoiceOver, NVDA or TalkBack); 200% zoom; Windows High Contrast; reduced motion; focus order matching visual order; target sizes.

## Triage

- **Critical**: missing form labels, missing alt, insufficient contrast, keyboard traps, no focus indicator.
- **Serious**: missing page language, broken heading structure, non-descriptive link text, autoplaying media, no skip link.
- **Moderate**: icons without ARIA labels, inconsistent navigation, missing error identification, timing without controls, missing landmarks.

Sources: [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/), [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/), [Deque axe rules](https://dequeuniversity.com/rules/axe/).

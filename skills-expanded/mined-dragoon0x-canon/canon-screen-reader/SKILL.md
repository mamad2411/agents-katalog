---
name: canon-screen-reader
description: Use when designing or auditing for screen reader compatibility — semantic HTML, ARIA roles and states, live regions, announcements, reading order, and hidden content. Trigger when the user mentions screen reader, VoiceOver, NVDA, JAWS, accessibility tree, ARIA, or assistive technology.
---

# CANON · Screen Reader

Screen readers traverse the accessibility tree, not the visual layout. If the tree is wrong, the interface is wrong for blind and low-vision users.

## Semantic HTML first

Screen readers understand HTML elements natively. ARIA is a patch for when HTML can't express the role.

| Need | Use HTML | Not |
|---|---|---|
| Button | `<button>` | `<div role="button">` |
| Link | `<a href>` | `<span onClick>` |
| Heading | `<h1>`–`<h6>` | `<div class="heading">` |
| List | `<ul>/<ol>` | `<div class="list">` |
| Table | `<table>` with `<th>` | CSS grid of `<div>` |
| Landmark | `<main>`, `<nav>`, `<header>`, `<footer>` | `<div class="nav">` |
| Dialog | `<dialog>` | `<div class="modal">` |

## Heading hierarchy

Headings create the document outline. Screen reader users navigate by heading. Skip levels or misused headings break this navigation.

- One `<h1>` per page.
- No skipping levels (h1 → h3 without h2).
- Headings are structure, not styling. Don't use `<h3>` because you want smaller text; use CSS.

## ARIA — only when HTML fails

The first rule of ARIA: don't use ARIA if HTML does the job. The second rule: if you use ARIA, use it correctly and completely.

Common ARIA patterns done right:

```html
<!-- Live region for dynamic updates -->
<div role="status" aria-live="polite">3 results found</div>

<!-- Custom disclosure -->
<button aria-expanded="false" aria-controls="panel">Details</button>
<div id="panel" hidden>...</div>

<!-- Tab interface → see canon-tabs -->
```

## Visually hidden but screen-reader accessible

```css
.sr-only {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

Use for: labels that are visually implied, skip links before focus, extra context.

## Live regions — announce dynamic changes

| Role | Urgency | Use |
|---|---|---|
| `role="status"` / `aria-live="polite"` | Low — waits for pause | Search result count, save confirmation |
| `role="alert"` / `aria-live="assertive"` | High — interrupts | Error messages, time-sensitive warnings |

The container must exist in the DOM before content is injected. Don't mount and unmount live-region elements.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| `aria-label` on a non-interactive element | Most screen readers ignore it on `<div>` |
| Redundant ARIA (`<button role="button">`) | Noise |
| `aria-hidden="true"` on focusable elements | Focus lands on invisible element |
| Using only color/icon for status | Screen reader doesn't announce visual changes |
| Heading levels skipped | Navigation breaks |
| `display: none` for "hiding" content from sighted users but wanting SR to read it | Hides from everyone |

## Testing

Test with at least one screen reader:
- macOS/iOS: VoiceOver (built in)
- Windows: NVDA (free) or JAWS
- Android: TalkBack (built in)

Quick smoke test: navigate the entire page with Tab + arrow keys while listening.

## Audit checklist

- [ ] Semantic HTML used for all standard patterns
- [ ] One `<h1>`, no skipped heading levels
- [ ] Landmarks: `<main>`, `<nav>`, `<header>`, `<footer>` present
- [ ] Images have meaningful `alt` or `alt=""`
- [ ] ARIA used only when HTML can't express the role
- [ ] Live regions for dynamic content updates
- [ ] `.sr-only` class available for hidden labels
- [ ] No `aria-hidden` on focusable elements
- [ ] Tested with a screen reader end-to-end

## Sources

- WCAG 2.2 · 1.1.1, 1.3.1, 2.4.6, 4.1.2
- WAI-ARIA · Roles, states, properties
- WebAIM · Screen Reader User Survey
- Deque · axe-core testing rules

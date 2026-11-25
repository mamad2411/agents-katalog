---
name: aem-accessibility
description: AEM accessibility review — WCAG 2.1 AA compliance in HTL templates, Coral UI dialogs, and frontend components
allowed-tools: Read, Grep, Glob
argument-hint: "[file or component path]"
---

Review `$ARGUMENTS` for WCAG 2.1 Level AA accessibility issues. Report each finding as **Blocking** / **Warning** / **Suggestion**.

**HTL templates**
- `<img>` without an `alt` attribute, or `alt` hardcoded to a non-descriptive string — Blocking
- Interactive elements (`<a>`, `<button>`) with no visible text or `aria-label` — Blocking
- Non-semantic `<div>`/`<span>` used for interactive behaviour instead of native elements — Blocking
- Form inputs without an associated `<label>` or `aria-labelledby` — Blocking
- Focus ring suppressed (`outline: none`) with no custom focus indicator replacement — Blocking
- Heading levels that skip (e.g. `<h2>` → `<h4>`) or chosen for visual weight rather than document structure — Warning
- Dynamic content (carousels, tabs, dialogs) with no `aria-live` or role-based announcement — Warning
- Multiple landmark regions of the same type with no distinguishing `aria-label` — Warning
- ARIA roles overriding native semantics when a correct native element exists — Suggestion

**Coral UI dialogs (`_cq_dialog/.content.xml`)**
- Dialog field with empty or missing `fieldLabel` — Blocking
- Relying solely on placeholder text for authoring guidance instead of `fieldDescription` — Warning

**Frontend / SPA components**
- Image rendered via React/SPA with `alt` defaulting silently to empty string — Blocking
- Modal dialog with no focus trap or no focus restoration to the trigger on close — Blocking
- Tab or accordion with no keyboard navigation (`ArrowLeft`/`ArrowRight`, `Enter`/`Space`) — Blocking
- Custom interactive component with no ARIA role, state, or keyboard operability — Blocking
- Information conveyed by colour alone with no accompanying text, icon, or pattern — Warning

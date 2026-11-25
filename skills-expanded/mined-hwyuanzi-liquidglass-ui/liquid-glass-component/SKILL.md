---
name: liquid-glass-component
description: >-
  Build, modify, and document LiquidGlass UI Web Components in this repository
  following its LiquidGlassElement base class, design-token system, restrained
  Apple-inspired lighting model, accessibility fallbacks, and release checks.
  Use when adding a new liquid-glass-* custom
  element, changing the glass visuals or tokens, editing src/liquid-glass.js or
  src/liquid-glass.css, or updating the examples/index.html playground.
---

# LiquidGlass Component

Authoring and maintenance guide for components in **LiquidGlass UI** — a
dependency-free, native Web Components glass library. Follow this skill to keep
every component consistent with the project's architecture, visual physics, and
release conventions.

## Architecture in one minute

- `src/liquid-glass.js` — the engine. A single `LiquidGlassElement` base class
  renders the shared glass surface (Shadow DOM, fixed top-light specular, top
  sheen, whole-element hover, optional edge refraction). Concrete elements
  subclass it and override only `styles()` and `body()`.
- `src/liquid-glass.css` — the design tokens. **Every** visual value is a
  `--lg-*` CSS custom property. Components must read tokens, never hard-code
  magic numbers that a token already covers.
- `examples/index.html` — the live playground/demo (also the GitHub Pages site).
- Components are registered with a guarded `customElements.define(...)` and
  exported at the bottom of `liquid-glass.js`.

The Web implementation uses a restrained fixed top light and lets the backdrop
inform the material. There is **no cursor tracking, glare-follows-mouse, noisy
distortion, or 3D tilt**. Hover affects interactive surfaces as a whole.

Before changing the optical treatment, read
[`skills/liquid-glass-ui/references/design-guidelines.md`](../../../skills/liquid-glass-ui/references/design-guidelines.md).

For the full API, token table, and refraction internals, read
[reference.md](reference.md). For complete worked examples, read
[examples.md](examples.md).

## When to use this skill

- Adding a new `<liquid-glass-*>` element.
- Changing glass visuals, tokens, hover behaviour, or refraction.
- Editing `src/liquid-glass.js`, `src/liquid-glass.css`, or the playground.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Subclass LiquidGlassElement; override styles() and body() only
- [ ] 2. Drive all visuals from --lg-* tokens; escape interpolated values
- [ ] 3. Register with a guarded customElements.define + add to the export
- [ ] 4. Demo it in examples/index.html
- [ ] 5. Document it in README.md (and reference.md/examples.md if API changed)
- [ ] 6. Validate: npm run validate && npm test && npm run format:check
```

**Step 1 — Subclass.** Add the class in `src/liquid-glass.js` next to the other
components. Override `styles()` (component CSS, scoped to the shadow root) and
`body()` (the inner markup, placed inside `.lg__content`). Keep the constructor
and `render()` in the base class. Override `connectedCallback()` only when a
component requires event delegation, and call `super.connectedCallback()`
first. Extend `super.observedAttributes` for configured attributes; let the base
`attributeChangedCallback()` re-render them.

**Step 2 — Tokens + escaping.** Read visual values from `--lg-*` tokens (see
[reference.md](reference.md)). Any attribute or dynamic value interpolated into
`body()` markup **must** pass through `escHTML()` (text context) or `escAttr()`
(attribute context). Never build markup from raw `getAttribute` output.

**Step 3 — Register.** Use the guarded pattern and extend the export:

```js
if (!customElements.get("liquid-glass-NAME")) {
  customElements.define("liquid-glass-NAME", LiquidGlassName);
}
```

**Step 4 — Demo.** Add a real, styled example to the relevant section of
`examples/index.html` so the component is visible in the playground.

**Step 5 — Document.** Update the component table and attribute docs in
`README.md`. If you changed the base API or tokens, also update
[reference.md](reference.md) and [examples.md](examples.md).

**Step 6 — Validate.** Run the checks (see below). Fix everything before finishing.

## Rules

**Do**

- Keep it vanilla — **zero runtime dependencies**.
- Express every visual value as a `--lg-*` token; add a new token (and document
  it) rather than hard-coding a value that should be themeable.
- Escape all interpolated markup (`escHTML` / `escAttr`).
- Sanitize URL-bearing attributes with `sanitizeURL`.
- Expose internals with `part="..."` where useful (`surface`, `sheen`, `control`).
- Preserve reduced-motion, reduced-transparency, contrast, forced-colors, and
  no-backdrop-filter fallbacks.
- Use `heading` (not `title`) for card-like text to avoid the native tooltip.

**Don't**

- Don't add pointer/mouse tracking, cursor-following glare, decorative wobble,
  large hover jumps, or 3D tilt.
- Don't use `feTurbulence`/noise for refraction; refraction is a smooth
  edge-lens displacement only (see [reference.md](reference.md)).
- Don't leak styles outside the Shadow DOM or rely on global CSS for internals.
- Don't introduce a build step, framework, or bundler.

## Validation

```bash
npm run validate
npm run check
npm test
npm run format:check
```

CI (`.github/workflows/ci.yml`) runs syntax, behavior, browser, package, Skill,
invariant, and format checks on every push. `deploy.yml` publishes the
playground to GitHub Pages from `main`. Keep both green.

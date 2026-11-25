---
name: frontend-forge
description: Frontend engineering standards with Anti-Generic UI principles. Teaches AI agents architecture, accessibility, performance, security, and design taste so output stops looking like generic AI-generated code.
---

# Frontend Forge — AI Agent Standards

You are an AI coding agent building frontend code. Follow these standards to eliminate the "AI Design Fingerprint" — the visual sameness that makes AI-generated UIs look generic.

## Priority Rules

### Anti-Generic UI (ALWAYS APPLY)

**Banned patterns** — never use without explicit justification:
- Inter/Roboto/Arial as display face → Use distinctive fonts (Satoshi, Space Grotesk, Fraunces)
- Pure #000/#fff → Tint neutrals with brand hue via HSL
- Purple-blue/cyan gradients → Use solid brand colors or intentional gradients
- Symmetric 3-column feature grids → Vary layouts with primary/secondary hierarchy
- Uniform spacing → Tight within groups (4-12px), generous between sections (48-96px)
- Multi-layer shadows on every card → Use borders; shadows only for elevation
- `transition: all` → Specify exact properties
- Scale/bounce hover on everything → Subtle color/border shifts
- Hero + cards + testimonials + CTA skeleton → Design around the product's story

**Self-critique before emitting UI**: Check Hierarchy (focal point?), Specificity (why this choice?), Restraint (can you subtract?), Variety (different from last 10 outputs?).

### Typography
- 2 families max. Modular scale 1.25 ratio. Body ≥ 16px
- Tight line-height (1.1) + letter-spacing (-0.02em) on headings
- Relaxed line-height (1.5+) + normal spacing on body

### Color
- Brand-tinted neutrals: `hsl(brand-hue, 5-15%, lightness)`
- WCAG AA contrast: ≥4.5:1 normal, ≥3:1 large text
- Dark mode via CSS custom properties

### Accessibility (NON-NEGOTIABLE)
- Semantic HTML (`<button>`, `<label>`, `<nav>`, headings in order)
- Visible labels on every input (placeholder ≠ label)
- `:focus-visible` styles, keyboard navigation, `prefers-reduced-motion`
- `aria-invalid` + `aria-describedby` on form errors

### Forms
- Server-side validation mandatory. Inline errors near the field
- Handle loading, error, empty, success states
- `autocomplete` attributes on inputs

### Data Fetching
- TanStack Query (not manual useEffect). Check `response.ok`
- Handle all states: loading (skeleton), error (retry), empty (CTA), success
- No secrets in client code

### Performance
- LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1
- Preload LCP image. Self-host fonts. Set image dimensions
- Client JS < 200KB gzipped

### Security
- No secrets in client code. httpOnly cookies for sessions
- No unsanitized `dangerouslySetInnerHTML`. Server-side authorization

### Project Structure
- Feature-based organization. Colocate everything per feature
- Shared UI = only truly generic primitives

---
name: ui-prototype
description: Create UI prototypes for websites, dashboards, desktop apps, or mobile apps using HTML and TailwindCSS. Applies design system tokens before generating markup to ensure consistent theming. Triggers on requests for mockups, wireframes, screen concepts, page concepts, or previewable interface prototypes.
---

# UI Prototype

Create polished, previewable UI prototypes using plain HTML and TailwindCSS, grounded in design system tokens.

## Defaults

These defaults apply unless the user explicitly overrides them:

- **Design tokens first:** Always establish design tokens (via the `design-system` skill) before writing any HTML. All colors, spacing, typography, and component styles must reference CSS variables — never hardcoded values.
- **Dual theme:** Generate both `light` and `dark` treatments. Use Tailwind's class-based dark mode (`darkMode: 'class'`) and include a theme toggle in the UI.
- **Shared shell:** For multi-page work, keep navigation, top bars, sidebars, bottom bars, spacing, visual tokens, and component states consistent across pages. Only page-specific content, active state, titles, breadcrumbs, and local actions should change between pages.
- **Realistic content:** Use domain-appropriate placeholder text instead of lorem ipsum. Names, dates, numbers, and labels should look believable.

## Core workflow

1. **Establish design tokens** — Check if a `tokens.css` or `tokens.json` exists in the project. If not, use the `design-system` skill to generate tokens based on user input (screenshot, brand description, or defaults). This produces CSS custom properties for colors, spacing, typography, radius, and shadows.
2. **Embed tokens** — Include the generated CSS variables in a `<style>` block at the top of every HTML file (`:root { ... }` for light, `.dark { ... }` for dark mode).
3. Infer the target platform from the request (`app`, `web`, or `desktop`). If ambiguous, ask.
4. Read `references/platform-guidelines.md`, then the matching platform reference.
5. Decide single-page vs multi-page output.
6. Generate responsive HTML with TailwindCSS, **using only token-based values**.
7. Verify against the output checklist.

### Token integration details

When writing HTML/Tailwind markup, use tokens like this:

```html
<!-- In <style> block -->
<style>
  :root {
    --color-primary: #2563EB;
    --color-primary-hover: #1D4ED8;
    --color-background: #F9FAFB;
    --color-foreground: #111827;
    --color-border: #E5E7EB;
    --color-muted: #F3F4F6;
    --color-muted-foreground: #6B7280;
    --radius-md: 0.375rem;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    /* ... full token set from design-system */
  }
  .dark {
    --color-background: #030712;
    --color-foreground: #F9FAFB;
    --color-border: #1F2937;
    --color-muted: #1F2937;
    --color-muted-foreground: #9CA3AF;
  }
</style>

<!-- In markup — reference tokens via Tailwind arbitrary values or inline -->
<button class="rounded-[var(--radius-md)] bg-[var(--color-primary)] text-white
               hover:bg-[var(--color-primary-hover)] px-4 py-2">
  Submit
</button>
```

**Rules:**
- Never use raw hex in class names — always `var(--token-name)` or Tailwind `[var(...)]`
- If the user provides a screenshot or brand description, pass it to `design-system` first to extract tokens
- If no design context is given, use the default tokens from `design-system/templates/design-tokens-starter.json`

## Platform inference

Use the user's explicit choice if given. Otherwise infer:

- **`app`** — phone screens, onboarding, bottom tabs, mobile flows, iOS, Android, touch-first UI
- **`web`** — website, landing page, SaaS dashboard, marketing page, browser-based admin, portal
- **`desktop`** — desktop client, workstation, control panel, dense productivity tool, persistent sidebars / inspectors / toolbars

If the request fits more than one platform, ask.

## Output structure

### Single-page

One `index.html` when the task is clearly one page or one contained flow.

### Multi-page

Multiple HTML files when the task involves distinct pages or screens:

- `index.html` as entry point
- One HTML file per additional page (e.g., `settings.html`, `billing.html`)
- Shared visual system across all files
- Folders like `assets/` only when they materially help organization

Do not collapse multiple pages into one scrolling file when separate pages better match intent.

## Tailwind usage

- Load via CDN unless the user asks for a build step.
- Use class-based dark mode: add `darkMode: 'class'` to the Tailwind config and toggle the `dark` class on `<html>`.
- Include a minimal theme toggle (sun/moon icon or similar) that switches between light and dark.
- Keep markup readable. Avoid unnecessary JavaScript beyond the theme toggle.
- **Map design tokens to Tailwind**: Use arbitrary value syntax `bg-[var(--color-primary)]` or extend the Tailwind config with token references.

## Accessibility baseline

- Use semantic HTML (`<nav>`, `<main>`, `<header>`, `<section>`, `<button>`, etc.).
- Ensure text meets WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text).
- Make interactive elements keyboard-accessible.
- Add `alt` text on images and `aria-label` on icon-only buttons.

## Responsive expectations

### App

- Centered phone frame at fixed width (iPhone 17 Pro Max proportions, ~430px).
- Mobile-safe spacing and touch-friendly targets (min 44px tap areas).
- The browser viewport is the preview shell; the phone canvas is the content.

### Web

- Adaptive widths with responsive containers and breakpoint-aware layout.
- Collapse columns on smaller breakpoints; preserve content hierarchy.

### Desktop

- Adaptive desktop layouts with dense information arrangement.
- Toolbars, side panels, inspectors, split views.
- Design for mouse-and-keyboard usage and wider screens.

## When to clarify

Ask a focused question only when:

- The platform cannot be reliably inferred
- The request implies multiple pages but the page list is unknown
- The user wants a framework or runtime beyond plain HTML + TailwindCSS

Do not ask broad discovery questions when the rest of the request is clear.

## Reference files

After determining the platform, read these files in order:

1. `references/platform-guidelines.md` (always)
2. The matching platform file: `references/app-guidelines.md`, `references/web-guidelines.md`, or `references/desktop-guidelines.md`

## Output checklist

Before finishing, verify:

- [ ] Design tokens are established and embedded in the HTML
- [ ] No hardcoded hex colors or pixel values — all via CSS variables
- [ ] Platform is explicit or well-supported by context
- [ ] Structure matches task complexity (single vs multi-page)
- [ ] Both light and dark themes are present with a working toggle
- [ ] App output uses a centered fixed-width phone frame (~430px)
- [ ] Web and desktop outputs use adaptive widths
- [ ] Semantic HTML is used throughout
- [ ] Text contrast meets WCAG AA
- [ ] Multi-page output shares consistent navigation and shell chrome
- [ ] Realistic placeholder content is used (not lorem ipsum)

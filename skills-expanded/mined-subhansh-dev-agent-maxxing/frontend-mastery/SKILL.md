---
name: frontend-mastery
description: UI/UX design rules, visual quality patterns, and frontend engineering extracted from Codex GPT-5.5 and Claude Design.
---

# Frontend Mastery — Design & UI Patterns

Extracted from Codex GPT-5.5 (11,104 lines) and Claude Design (9,199 lines).

## Build with Empathy

- If working with an existing design or given a design framework in context, pay careful attention to existing conventions and ensure consistency.
- Think deeply about the audience and use that to decide features, layout, components, visual style, on-screen text, and interaction patterns. Using your application should feel rich and sophisticated.
- Tailor the frontend design for the domain: SaaS/CRM tools should feel quiet, utilitarian, and work-focused. Games can be more illustrative, expressive, animated, and playful.
- Common workflows should be ergonomic and efficient, yet comprehensive.

## Design Instructions

- Use icons in buttons for tools, swatches for color, segmented controls for modes, toggles/checkboxes for binary settings, sliders/steppers/inputs for numeric values, menus for option sets, tabs for views.
- Do not use rounded rectangular UI elements with text inside if you could use a familiar symbol or icon instead. Build tooltips for unfamiliar icons.
- Use lucide icons inside buttons whenever one exists. If a library is enabled in an existing application, use icons from that library.
- Build feature-complete controls, states, and views that a target user would naturally expect.
- Do not use visible, in-app text to describe the application's features, functionality, keyboard shortcuts, styling, or how to use the application.
- Should not make a landing page unless absolutely required; build the actual usable experience as the first screen.

## Hero Pages

- When making a hero page, use a relevant image, generated bitmap image, or immersive full-bleed interactive scene as the background with text over it that is not in a card.
- Never use a split text/media layout where a card is one side and text is on another side.
- Never put hero text or the primary experience in a card.
- Never use a gradient/SVG hero page.
- Do not create an SVG hero illustration when a real or generated image can carry the subject.
- For landing-page heroes, make the H1 the brand/product/place/person name or a literal offer/category; put descriptive value props in supporting copy, not the headline.

## Visual Assets

- Websites and games must use visual assets. Use image search, known relevant images, or generated bitmap images instead of SVGs, unless making a game.
- Primary images and media should reveal the actual product, place, object, state, gameplay, or person; refrain from dark, blurred, cropped, stock-like, or purely atmospheric media when the user needs to inspect the real thing.
- For games or interactive tools with well-established rules, physics, parsing, or AI engines, use a proven existing library for the core domain logic instead of hand-rolling it.

## 3D & Interactive

- Use Three.js for 3D elements, and make the primary 3D scene full-bleed or unframed and not inside a decorative card/preview container.
- Before finishing, verify with screenshots and canvas-pixel checks across desktop/mobile viewports that it is nonblank, correctly framed, interactive/moving, and that referenced assets render correctly.

## Layout Rules

- Do not put UI cards inside other cards.
- Do not style page sections as floating cards.
- Only use cards for individual repeated items, modals, and genuinely framed tools.
- Page sections must be full-width bands or unframed layouts with constrained inner content.
- Do not add discrete orbs, gradient orbs, or bokeh blobs as decoration or backgrounds.

## Typography & Spacing

- Make sure text fits within its parent UI element on all mobile and desktop viewports.
- Move text to a new line if needed; if it still doesn't fit, use dynamic sizing.
- Text must not occlude preceding or subsequent content.
- Match display text to its container: hero-scale type for heroes, smaller headings in compact panels.
- Define stable dimensions with responsive constraints (aspect-ratio, grid tracks, min/max, container-relative sizing).
- Do not scale font size with viewport width. Letter spacing must be 0, not negative.

## Color & Palette

- Do not make one-note palettes: avoid UIs dominated by variations of a single hue family.
- Limit dominant purple/purple-blue gradients, beige/cream/sand/tan, dark blue/slate, and brown/orange/espresso palettes.
- Scan CSS colors before finalizing and revise if the page reads as one of these themes.

## Interaction Quality

- UI elements and on-screen text must not overlap with each other in an incoherent manner. This is extremely important.
- Make sure common workflows are ergonomic and efficient.
- Build feature-complete controls, states, and views.

## Dev Server

When building a site or app that needs a dev server, start the local dev server after implementation and give the user the URL. If there's already a server on that port, use another one. For a website where just opening the HTML will work, don't start a dev server.

## Design Component System (from Claude Design)

Build every design as a Design Component (DC): a single `Name.dc.html` file that opens directly in a browser and can be imported by other DCs.

### Authoring Principles

1. One DC by default — high bar for splitting. A 400-line single body is normal.
2. Use `dc_write` / `dc_html_str_replace` for template edits; `dc_js_str_replace` for logic edits.
3. Give descriptive filenames like 'Landing Page.dc.html'.
4. When doing significant revisions, copy and edit the copy to preserve the old version.
5. For small, targeted changes, change ONLY that — leave everything else exactly as is.
6. Copy needed assets from design systems; do not reference them directly.
7. Write canonical HTML: close every non-void element, double-quote every attribute.
8. Color usage: try to use colors from brand/design system. If too restrictive, use oklch for harmonious colors.

## Anti-AI-Slop Rules

These patterns make AI-generated UI look generic. Avoid them:

- No rainbow gradients as primary design element
- No card-heavy layouts with equal-sized items
- No oversized hero sections with generic copy
- No fake dashboard data
- No placeholder text (lorem ipsum)
- No emoji in UI (use SVG icons)
- No generic 3-card grid layouts
- No purple-blue gradient dominance

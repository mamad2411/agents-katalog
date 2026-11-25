---
name: skill-website-designer
version: 1.0.0
description: "Design and scaffold a static website (single-page or multi-page) with responsive HTML/CSS/JS. Use when: AUTOMATICALLY ACTIVATE when user requests: \"design a website\", \"build a landing page\", \"make a portfolio site\", \"create a one-pager\", \"website for X\", \"static site for X\""
cowork:
  label: Website
  blurb: "Landing page, portfolio, one-pager — static HTML/CSS."
  icon: globe
  accent: emerald
  primed_prompt: "Use the skill-website-designer skill to design a website for "
  order: 30
---

# Website Designer

Generate a self-contained static website (HTML + CSS + optional vanilla JS) the user can open in a browser or deploy to any static host (GitHub Pages, Netlify, Cloudflare Pages, S3, etc.). Output is plain files in the working directory — no build step, no framework lock-in.

## When to use

The user wants:
- A landing page or one-pager for a product, project, idea, or event.
- A simple portfolio / personal site.
- A documentation-style page.
- A static "About" or marketing site for a small business.

If the user wants a full single-page application (state, routing, real-time data), use `anthropic-skills:web-artifacts-builder` instead — this skill is for **content sites**, not interactive apps.

## Pipeline (4 steps)

### Step 1 — Gather brief

Use **AskUserQuestion** to lock the scope. Ask in one batch:

**Question 1 — Site purpose:**
- Landing page (one section per pitch beat: hero, problem, solution, CTA)
- Portfolio (work samples, bio, contact)
- Documentation (table of contents, body, sidebar)
- One-pager (everything on one scrollable page)
- Marketing site (multi-page: home, about, pricing, contact)

**Question 2 — Audience & vibe:**
- Minimal / editorial (white space, serif headings, restrained accents)
- Playful / brand-forward (color, illustration, friendly type)
- Corporate / professional (neutral palette, sans serif, structured)
- Technical / docs-style (mono accents, code blocks, dense info)

**Question 3 — Brand specifics (optional):**
- Primary colour preference (or "pick something tasteful")
- Typography preference (or "pick a Google Font pairing")
- Logo / favicon assets the user wants embedded

If the user has answered any of these in the prompt already, skip those questions.

### Step 2 — Outline structure

Produce a markdown outline of the page (or pages). Example for a landing page:

```
1. Hero
   - Headline (single sentence)
   - Subhead (1–2 lines)
   - Primary CTA button
2. Problem
   - 2–3 bullet pain points
3. Solution
   - 3 feature cards with icons
4. Social proof
   - Testimonial quote OR logo strip
5. Final CTA
   - Headline + button
6. Footer
   - Links + copyright
```

**Ask the user to approve or edit the outline before rendering.** Wireframe gate — catches "wait, I wanted X different" before any code is written.

### Step 3 — Theme + assets

Pick the visual system in this order of preference:

1. **`anthropic-skills:theme-factory`** — if available, suggest one of the 10 presets (Editorial, Playful, Corporate, Technical, etc.) and let the user confirm. Theme-factory hands back colour tokens + font pairing.
2. **Inline pick** — fall back to a tasteful default for the chosen vibe:
   - Minimal: ink `#111827` on snow `#f9fafb`, accent `#0ea5e9`. Headings: `Fraunces` (serif), body: `Inter`.
   - Playful: indigo `#6366f1` on cream `#fef3c7`. Headings + body: `Plus Jakarta Sans`.
   - Corporate: slate `#1e293b` on white `#ffffff`, accent `#0284c7`. Headings + body: `Inter`.
   - Technical: stone `#1c1917` on paper `#fafaf9`, accent `#dc2626`. Headings: `JetBrains Mono` (display use only), body: `Inter`.

If the user wants more interactivity than a static site supports (e.g. a working contact form, search, real-time updates), pivot here to `anthropic-skills:web-artifacts-builder`.

### Step 4 — Render

Emit files into the **working directory** (same dir the chat is anchored to):

- **`index.html`** — semantic HTML5 with proper landmarks (`<header>`, `<main>`, `<section>`, `<footer>`), meta viewport, preconnect to Google Fonts.
- **`styles.css`** — mobile-first responsive (CSS grid + flex), CSS custom properties for the theme tokens, prefers-color-scheme media query for dark mode if the user wanted it.
- **`script.js`** — only if the outline needs it (smooth-scroll, mobile nav toggle, theme switcher). Vanilla JS, no dependencies.

Constraints to keep the output portable:

- **No build step.** Files load directly via `file://` or any static host.
- **Mobile-first responsive.** Default styles target small screens; widen via `@media (min-width: 768px)`.
- **Accessibility checks pre-flight:**
  - Every `<img>` has `alt` (empty `alt=""` is fine for decorative).
  - Heading hierarchy is monotonic (`h1` → `h2` → `h3`, no skips).
  - Colour contrast ≥ 4.5:1 for body text, ≥ 3:1 for large text.
  - Focus styles are visible (`:focus-visible` outline).
  - Interactive elements are real buttons/links (no clickable `<div>`s).
- **System-font fallback** in the CSS stack so the page renders before Google Fonts load.
- **No external JS framework** unless the user explicitly asks for one.

After writing, tell the user:
- The file paths created.
- How to preview (`open index.html` on macOS, or `python3 -m http.server` for a local server).
- One short note on what to customize first (typically: hero copy + primary CTA target).

## Output format

Whenever you render a file, use the standard `Write` tool with the full content. Do NOT show the full file content in chat — summarise ("Wrote `index.html` (4.2 KB) and `styles.css` (3.1 KB)") and let the user open it. If the user wants changes, edit the file in place rather than re-writing from scratch.

## Done condition

The skill is "done" when the user has:
- A working `index.html` they can open and see the rendered page.
- Confirmation in chat of what was written, where, and how to preview.
- A single-line summary of what to tweak first.

If the user wants iterations (palette swap, copy edit, new section), edit the existing files; don't re-run the whole pipeline.

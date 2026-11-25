---
name: design-link-in-bio
description: |
  Generate a minimal single-column standalone HTML page — mobile-first at 375px width — for use as a link-in-bio destination. Contains: name/wordmark, short tagline, list of links (each a styled <a> block), social footer. Self-contained, works offline, deployable as-is to GitHub Pages or Netlify. Reads ./design/<brand-slug>/DESIGN.md, tokens.css, and components.html. Triggers include "link in bio", "linktree replacement", "bio page", "/link-in-bio".
---

# Skill: link-in-bio

Produces a deliverable mobile-first HTML page at 375px primary design width (with a centered-on-desktop fallback that maintains the column constraint). This is **NOT** a screenshot artifact — it's a real page meant to be deployed to a static host (GitHub Pages, Netlify, Vercel) as a `link-in-bio` destination from social profiles.

The format is functionally identical to a Linktree-style page, but the visual treatment commits to the brand's editorial register rather than the rounded-button-stack template that all link-in-bio services produce by default.

## When to use

- User wants a link-in-bio page (replaces or complements Linktree, Beacons, etc.)
- A `DESIGN.md` exists for the brand

## Inputs

- **Required:** brand slug, name (or wordmark text), tagline (1 line, max ~10 words)
- **Required:** array of links — each with `label` + `url`, optional `meta` (e.g. "GitHub" + "github.com/shane" + "Open source")
- **Optional:** social handles for footer (Twitter/X, GitHub, etc.)
- **Optional:** "current" indicator — one link can be marked as "current" (e.g. the latest piece, the next event)

## Output

`./design/<brand-slug>/artifacts/link-in-bio.html` (single file — overwrite OK; canonical bio page for the brand)

## Steps

### 1. Verify brand exists

```bash
test -f ./design/<brand-slug>/tokens.css
```

### 2. Gather the brief

Ask in one message:

```
1. Name / wordmark — how the brand displays at the top
2. Tagline — 1 line, max 10 words, sentence-case ending in period per brand voice
3. Links — list of label + URL pairs, in display order. Optionally per-link meta description (1 sentence).
4. Social footer handles — Twitter/X, GitHub, etc.
5. Optional: which link (if any) is "current" — gets the brand accent treatment
```

### 3. Pick variation — overall register

The link-in-bio is small surface area, so the variation lever is the OVERALL register:

- `editorial-cream` — cream page, Fraunces wordmark, link entries as numbered list with hairline rules. Most editorial.
- `inverted` — full dark inversion canvas (canonical v2 feature treatment). Reads as confident; rare for link-in-bio formats which lean cheerful by default.
- `mono-stack` — mono-led, technical register. Each link as a code-style row. Best for engineering-audience brands.
- `chrome-led` — wordmark + tagline + buttons-vertical-stack. **Last resort.** This is the Linktree default the skill exists to avoid.

### 4. Generate the HTML

Template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>[name] — links</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<families>&display=swap">
<style>
/* Embed tokens.css verbatim */
<contents of tokens.css>

* { box-sizing: border-box; }
html, body { margin: 0; }
body {
  background: var(--color-surface);
  color: var(--color-ink);
  font-family: var(--type-sans-family);
  font-size: 17px;
  line-height: 1.55;
  font-feature-settings: 'ss01', 'cv11', 'kern';
  min-height: 100vh;
}

/* Mobile-first column — 375px design width, centered on desktop */
.page {
  max-width: 375px;
  margin: 0 auto;
  padding: 64px 24px 80px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header — wordmark + tagline */
.bio-head { padding-bottom: 32px; border-bottom: 1px solid var(--color-rule); margin-bottom: 32px; }
.wordmark { font-family: var(--type-display-family); font-weight: 600; font-size: 28px; line-height: 1.0; letter-spacing: -0.01em; color: var(--color-ink); margin: 0; }
.tagline { font-family: var(--type-display-family); font-style: italic; font-weight: 400; font-size: 16px; line-height: 1.45; color: var(--color-ink-soft); margin: 12px 0 0; max-width: 32ch; }

/* Link list — numbered, no buttons, no rounded rectangles */
.links { list-style: none; padding: 0; margin: 0 0 48px; flex: 1; }
.links li {
  border-top: 1px solid var(--color-rule);
}
.links li:last-child { border-bottom: 1px solid var(--color-rule); }
.links a {
  display: grid;
  grid-template-columns: 32px 1fr auto;
  gap: 12px;
  padding: 18px 0;
  align-items: baseline;
  text-decoration: none;
  color: var(--color-ink);
  transition: color 200ms;
}
.links a:hover { color: var(--color-ink-soft); }
.links .num {
  font-family: var(--type-mono-family);
  font-size: 12px; letter-spacing: 0.06em;
  color: var(--color-ink-3);
  align-self: baseline;
}
.links .label {
  font-family: var(--type-display-family);
  font-weight: 500; font-size: 18px; line-height: 1.3;
  letter-spacing: -0.005em;
}
.links .label .meta {
  display: block;
  margin-top: 4px;
  font-family: var(--type-sans-family);
  font-size: 13px;
  font-weight: 400;
  color: var(--color-ink-3);
}
.links .arrow {
  font-family: var(--type-mono-family);
  font-size: 14px;
  color: var(--color-ink-3);
  transition: transform 200ms, color 200ms;
}
.links a:hover .arrow { transform: translateX(3px); color: var(--color-ink); }

/* "Current" link — brand accent */
.links li.is-current .num { color: var(--color-accent); }
.links li.is-current .arrow { color: var(--color-accent); }
.links li.is-current::before {
  content: 'CURRENT';
  display: block;
  padding: 8px 0 0;
  font-family: var(--type-mono-family);
  font-size: 10px; letter-spacing: 0.18em;
  color: var(--color-accent);
}

/* Social footer */
.bio-foot {
  padding-top: 24px;
  border-top: 1px solid var(--color-rule);
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-family: var(--type-mono-family);
  font-size: 12px;
  letter-spacing: 0.06em;
  color: var(--color-ink-3);
}
.bio-foot a { color: var(--color-ink); text-decoration: none; }
.bio-foot a:hover { color: var(--color-ink-soft); }
</style>
</head>
<body>
<main class="page">
  <header class="bio-head">
    <h1 class="wordmark">[name / wordmark]</h1>
    <p class="tagline">[tagline]</p>
  </header>

  <ol class="links">
    <li>
      <a href="[url 1]">
        <span class="num">01</span>
        <span class="label">[link 1 label]<span class="meta">[optional meta]</span></span>
        <span class="arrow">→</span>
      </a>
    </li>
    <!-- repeat per link -->
  </ol>

  <footer class="bio-foot">
    <a href="[social 1 url]">[social 1 handle]</a>
    <a href="[social 2 url]">[social 2 handle]</a>
    <span style="margin-left: auto;">© [year]</span>
  </footer>
</main>
</body>
</html>
```

### 5. Verify

- [ ] Page renders correctly at 375px width AND at desktop widths (centered, max 375px column)
- [ ] No JavaScript required for any functionality
- [ ] Variation register documented — NOT `chrome-led` unless explicitly justified
- [ ] Links use the numbered-row pattern, NOT vertically stacked rounded buttons (the Linktree-default tell)
- [ ] At MOST one link marked as "current" (per brand-canonical use of accent)
- [ ] **Read `../../design-anti-patterns.md` and verify the page violates none of its rules.** Pay special attention to sections 1 (no orbs, no gradients, no decorative imagery), 2 (no italics-emphasis OR single-word color emphasis as default — except the "current" link uses accent semantically, which is allowed), and 4 (architecture must reach inner blocks)
- [ ] All copy is sentence-case per brand voice
- [ ] Self-contained — opens correctly when double-clicked from Finder (no broken external paths)

> Link-in-bio page generated at `./design/<brand-slug>/artifacts/link-in-bio.html`.
>
> Variation register: `<picked>`. Open in a browser at 375px AND desktop widths to verify the column layout holds.
>
> To deploy: drop the file on any static host (GitHub Pages, Netlify, Vercel) at `index.html` of a subdomain or path. Update the `<title>` and meta description with brand-specific copy.

## Anti-Slop Rules

Governed by three shared canonical references — read them, do not restate them:

- **`../../design-anti-patterns.md`** — the hard floor. Wins every conflict.
- **`../../design-principles.md`** — the craft floor (typographic hierarchy, spatial rhythm, color theory, layout logic, visual tension).
- **`../../design-variation-sop.md`** — the named-aesthetic roster + the procedure for varying every invocation.

**Forbidden (fast scan — the references hold the full list):**

- Indigo/violet/purple as default accent or primary — the `hsl(230–280)` family on a near-white surface. The single loudest AI tell.
- Purple→blue / "aurora" / gradient-mesh backgrounds; gradient-fill text.
- Glassmorphism without an explicit AA-contrast scrim; floating gradient "blobs" as atmosphere.
- The three-up icon-card feature grid; the "hero → 3 cards → CTA" median skeleton.
- One global border-radius on every element; timid evenly-weighted low-contrast palette.
- Inter / Roboto / Arial / Open Sans / Lato / Helvetica / system as the primary family (Space Grotesk = yellow flag). Use a category-matched stack from the variation roster.
- Value-free CTAs ("Get Started", "Learn More", "Sign Up"); the two-CTA hero. Name the real action and its value.

**Required variation (every invocation):**

- Make at least **two** intentional decisions that differ from the safe defaults (palette, layout structure, typographic voice, or spatial density) AND from the most recent artifact in this brand.
- Never default to "clean / minimal / modern" — that is the absence of a direction (variation-sop Rule 1).
- Sketch **three distinct directions**, offer them as a one-line menu, generate the best-fit by default, all three only if asked (variation-sop Rule 3).

**Authenticity:** prefer specific over generic everywhere — real datelines (not "today"), the brand's actual voice (not "build the future" filler), concrete CTAs over placeholders.

## Rules

- **Deliverable HTML, not a screenshot artifact.** No `.canvas` div. The page IS the deliverable.
- **375px design width, centered on desktop.** This is a mobile-first format because that's where the audience clicks from social bios.
- **Numbered list, not button stack.** The link rows are list items with hairline separators — not card-styled rounded buttons.
- **CSS-only.** No JavaScript. The page works with JS disabled.
- **Accent used at most once per page.** Reserved for the "current" link or absent entirely.
- **Token-pure.** Every visual value via `var(--*)` from tokens.css.
- **Anti-pattern compliance.** This skill defers to three shared canonical references: `../../design-anti-patterns.md` (the hard floor — wins every conflict), `../../design-principles.md` (the craft floor), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The anti-patterns file is the canonical anti-tell list. Specific anti-pattern this format invites: the Linktree-default vertical button stack. Avoid it.

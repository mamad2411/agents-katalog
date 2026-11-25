---
name: design-landing-page
description: |
  Generate a deliverable landing-page HTML file (NOT a screenshot artifact). 1440px design width, mobile-responsive (CSS-only, no JS). Sections: hero (full-viewport) + 3 feature blocks + CTA. Designed to be opened in a browser, iterated on, and deployed as-is. Reads ./design/<brand-slug>/DESIGN.md, tokens.css, and components.html. Triggers include "landing page for X", "marketing page", "product landing", "/landing-page".
---

# Skill: landing-page

Produces a deliverable landing-page HTML file at 1440px design width, fully responsive (CSS-only, no JavaScript). This is **NOT** a screenshot-target artifact like the platform skills — it's a real page meant to be opened in a browser, iterated on, and (eventually) deployed. There is no `.canvas` div. The page IS the page.

The anti-pattern rules apply with extra force here. Landing pages are the format where AI-default templates are most obvious: centered hero with template "[Big Word] [Subheading] [Button]", icon-grid features with circles, blue CTA buttons. This skill exists to NOT produce that.

## When to use

- User is launching a product, service, project, or initiative and needs a landing page
- A `DESIGN.md` exists for the brand

## Inputs

- **Required:** brand slug, page topic / thing being launched, hero claim (sentence-case ending in period)
- **Required:** 3 feature points (each: short name + 2-sentence description)
- **Required:** CTA text + destination (e.g. "Read the documentation" → URL)
- **Optional:** logo / brand mark variant, footer details, supporting hero copy

## Output

`./design/<brand-slug>/artifacts/landing-page-YYYY-MM-DD-<slug>.html`

## Steps

### 1. Verify brand exists

```bash
test -f ./design/<brand-slug>/tokens.css
```

### 2. Gather the brief

Ask in one message:

```
1. Page topic — what is this landing page for? (1 sentence)
2. Hero claim — the dominant headline, sentence-case ending in period (max ~14 words)
3. Optional supporting hero copy — 1-2 sentence dek
4. Three feature points:
   a. <name>: <2-sentence description>
   b. <name>: <2-sentence description>
   c. <name>: <2-sentence description>
5. CTA text + destination URL (e.g. "Read the documentation" → /docs)
6. Footer details — copyright line, secondary links (about, contact, GitHub, etc.)
```

### 3. Pick variation — HERO archetype is the lever

The hero section carries the page's identity. Pick ONE:

- `headline-led` — display headline dominates; everything else subordinated. Most editorial.
- `inverse-text` — full hero in dark inversion (canonical v2 feature treatment). Reads as confident.
- `object-of-content` — the hero looks like a fragment of the actual product (a screenshot-style mock, a transcript, a code excerpt). The page sells the thing by SHOWING it.
- `pattern-led` — typographic pattern fills hero; headline is the punctum. Risky for landing pages — may confuse first-time visitors. Use only if the brand has earned it.
- `chrome-led` — eyebrow + headline + dek + CTA-row — the AI-editorial default. **Last resort.** If you reach for this, ask why.

Feature blocks always use a CONSISTENT layout (3-column grid OR vertical stack) — the variation lever is on the hero only. Feature blocks don't get cards-with-icons-in-circles.

CTA section uses the brand's accent color ONLY on the action — never on a button background. The CTA is a `.btn-arrow` (text + arrow), not a filled button.

### 4. Generate the HTML

Template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><Page topic></title>
<meta name="description" content="<dek or summary>">
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
  line-height: 1.65;
  font-feature-settings: 'ss01', 'cv11', 'kern';
}

/* Layout container — 1180px max width, 24px gutter, mobile responsive */
.container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px;
}

/* === Site header === */
.site-header { padding: 24px 0; }
.site-header__bar { display: flex; justify-content: space-between; align-items: baseline; }
.wordmark { font-family: var(--type-display-family); font-weight: 600; font-size: 22px; letter-spacing: -0.005em; color: var(--color-ink); }

/* === Hero — per chosen archetype === */
.hero {
  padding: 96px 0 144px;
  /* If `inverse-text` archetype: */
  /* background: var(--color-ink); color: var(--color-surface); margin-top: -24px; padding-top: 120px; */
}
.hero h1 {
  font-family: var(--type-display-family);
  font-weight: 400;
  font-size: clamp(48px, 9vw, 120px);
  line-height: 1.0;
  letter-spacing: -0.02em;
  margin: 0;
  max-width: 18ch;
}
.hero h1 .accent { color: var(--color-accent); }
.hero .dek {
  font-size: 19px;
  line-height: 1.55;
  color: var(--color-ink-soft);
  max-width: 56ch;
  margin: 32px 0 48px;
}

/* === Feature blocks — consistent grid, NO icons-in-circles === */
.features {
  padding: 96px 0;
  border-top: 1px solid var(--color-rule);
}
.features__head { margin-bottom: 64px; }
.features__head h2 {
  font-family: var(--type-display-family);
  font-weight: 500;
  font-size: clamp(36px, 5vw, 56px);
  line-height: 1.1;
  letter-spacing: -0.015em;
  margin: 0;
  max-width: 28ch;
}
.features__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 48px;
}
.feature {
  /* No card. No icon. No circle. Just a numbered text block. */
}
.feature__num {
  font-family: var(--type-mono-family);
  font-size: 12px; letter-spacing: 0.06em;
  color: var(--color-ink-3);
  margin-bottom: 16px;
}
.feature__num .pos { color: var(--color-ink); }
.feature h3 {
  font-family: var(--type-display-family);
  font-weight: 500;
  font-size: 24px;
  line-height: 1.3;
  letter-spacing: -0.012em;
  margin: 0 0 12px;
}
.feature p {
  font-size: 16px;
  line-height: 1.55;
  color: var(--color-ink-soft);
  margin: 0;
}

/* === CTA === */
.cta {
  padding: 96px 0 144px;
  border-top: 1px solid var(--color-rule);
}
.cta h2 {
  font-family: var(--type-display-family);
  font-weight: 400;
  font-size: clamp(36px, 6vw, 64px);
  line-height: 1.1;
  letter-spacing: -0.018em;
  margin: 0 0 32px;
  max-width: 24ch;
}
.btn-arrow {
  display: inline; font-size: 19px; color: var(--color-ink);
  text-decoration: underline; text-decoration-color: var(--color-rule); text-decoration-thickness: 1px;
  text-underline-offset: 5px;
}
.btn-arrow::after { content: ' →'; font-family: var(--type-mono-family); font-size: 0.85em; }
.btn-arrow:hover { text-decoration-color: var(--color-ink); }
.btn-arrow--accent { color: var(--color-accent); text-decoration-color: var(--color-accent-hover); }

/* === Footer === */
.site-foot {
  padding: 48px 0;
  border-top: 1px solid var(--color-rule);
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-family: var(--type-mono-family);
  font-size: 12px;
  letter-spacing: 0.06em;
  color: var(--color-ink-3);
}
.site-foot .pos { color: var(--color-ink); }

/* === Responsive — mobile-first override === */
@media (max-width: 720px) {
  .container { padding: 0 20px; }
  .hero { padding: 64px 0 96px; }
  .features__grid { grid-template-columns: 1fr; gap: 48px; }
  .features { padding: 64px 0; }
  .cta { padding: 64px 0 96px; }
}
</style>
</head>
<body>

<header class="site-header">
  <div class="container site-header__bar">
    <span class="wordmark">[brand wordmark]</span>
    <nav><!-- optional inline links: about, docs, contact --></nav>
  </div>
</header>

<main>
  <!-- === HERO === -->
  <section class="hero">
    <div class="container">
      <h1>[hero claim, with optional <span class="accent">[one word]</span> in accent]</h1>
      <p class="dek">[supporting dek — 1-2 sentences]</p>
      <a class="btn-arrow btn-arrow--accent" href="[CTA destination]">[primary CTA text]</a>
    </div>
  </section>

  <!-- === FEATURES === -->
  <section class="features">
    <div class="container">
      <div class="features__head">
        <h2>[features section headline — sentence-case ending in period]</h2>
      </div>
      <div class="features__grid">
        <div class="feature">
          <p class="feature__num"><span class="pos">01</span> · [feature short label]</p>
          <h3>[feature 1 name]</h3>
          <p>[feature 1 description]</p>
        </div>
        <div class="feature">
          <p class="feature__num"><span class="pos">02</span> · [feature short label]</p>
          <h3>[feature 2 name]</h3>
          <p>[feature 2 description]</p>
        </div>
        <div class="feature">
          <p class="feature__num"><span class="pos">03</span> · [feature short label]</p>
          <h3>[feature 3 name]</h3>
          <p>[feature 3 description]</p>
        </div>
      </div>
    </div>
  </section>

  <!-- === CTA === -->
  <section class="cta">
    <div class="container">
      <h2>[secondary CTA framing — invitation, sentence-case ending in period]</h2>
      <a class="btn-arrow btn-arrow--accent" href="[CTA destination]">[primary CTA text]</a>
    </div>
  </section>
</main>

<footer class="site-foot">
  <div class="container site-foot__inner" style="display: flex; justify-content: space-between; align-items: baseline;">
    <span>[copyright line]</span>
    <span><span class="pos">[brand handle]</span> · [secondary link]</span>
  </div>
</footer>

</body>
</html>
```

### 5. Verify

- [ ] Page renders at 1440px AND at 375px (mobile) without horizontal scroll
- [ ] Hero archetype documented — NOT `chrome-led` unless explicitly justified
- [ ] Feature blocks have NO icons-in-circles, NO cards-with-shadows, NO centered-template layouts — just numbered text blocks
- [ ] CTA is `.btn-arrow` (text link with arrow) — NOT a filled blue button
- [ ] `.accent` color used on AT MOST one word in the hero headline
- [ ] **Read `../../design-anti-patterns.md` and verify the page violates none of its rules.** Pay special attention to sections 1 (no orbs, no gradients, no isometric illustrations, no stock photo cliches), 2 (no italics-emphasis OR single-word color emphasis as default), 4 (architecture must reach inner blocks; no center-aligned hero with template), and 6 (no marketing-phrase clichés — "single pane of glass", "digital transformation", "next-generation")
- [ ] No animation on scroll (no fade-ins, no parallax, no slide-up)
- [ ] All copy is sentence-case ending in period per brand voice
- [ ] No exclamation points anywhere

> Landing page generated at `./design/<brand-slug>/artifacts/landing-page-YYYY-MM-DD-<slug>.html`.
>
> Hero archetype: `<picked>`. Open in a browser at 1440px AND 375px to verify responsive behavior. Iterate by editing the file directly — there is no canvas to screenshot.
>
> To deploy: drop the file on any static host (GitHub Pages, Netlify, Vercel). It works as-is.

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
- **CSS-only responsive.** No JavaScript for layout. The page works with JS disabled.
- **Hero archetype must NOT default to `chrome-led`.** That's the AI-editorial template — pick a different archetype unless the brand specifically requires it.
- **Feature blocks have no icons.** Numbered text blocks only. Icons-in-circles are the SaaS-template tell this skill exists to avoid.
- **CTA is text + arrow.** No filled buttons. The brand uses `.btn-arrow`; this skill respects that.
- **Token-pure.** Every visual value via `var(--*)` from tokens.css. Only literal values: `1px` for hairlines.
- **Anti-pattern compliance.** This skill defers to three shared canonical references: `../../design-anti-patterns.md` (the hard floor — wins every conflict), `../../design-principles.md` (the craft floor), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The anti-patterns file is the canonical anti-tell list. Landing pages are the highest-risk format for AI-default tells; verify carefully.

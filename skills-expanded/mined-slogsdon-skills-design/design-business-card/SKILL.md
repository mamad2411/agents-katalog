---
name: design-business-card
description: Generate a printable business card — pixel-exact 1050×600 front canvas + 1050×600 back canvas in a single HTML file. Standard 3.5×2 inch card at 300dpi. Front carries name + title + contact details; back is wordmark-dominant (or brand device) with minimal text. The design system's most reduced artifact — tests whether the brand can speak with almost no text. Print bleed instructions in footer comment. Reads ./design/<brand-slug>/DESIGN.md, tokens.css, and components.html. Triggers include "business card", "calling card", "name card", "/business-card".
---

# Skill: business-card

Produces a single self-contained HTML file containing **two pixel-exact 1050×600 canvases** — the front and back of a standard 3.5×2 inch business card at 300dpi. Print-ready dimensions; bleed and crop notes documented at the end of the file.

This skill is the most extreme reduction test in the platform-skills set. A business card has ~6 square inches of total real estate; the brand must speak with nearly no text. If the brand can't hold its identity at this scale, the design system has a problem worth surfacing.

## When to use

- User needs printed business cards (or digital equivalents — Apple Wallet, Linktree alternative)
- A `DESIGN.md` exists for the brand

## Inputs

- **Required:** brand slug, name, title/role
- **Required:** primary contact (email OR URL — pick the one most likely to lead to a conversation)
- **Optional:** secondary contact (the other of email/URL)
- **Optional:** location (city · timezone)
- **Optional:** secondary handle (e.g. GitHub for engineering brands)

## Output

`./design/<brand-slug>/artifacts/business-card-YYYY-MM-DD-<slug>.html`

## Steps

### 1. Verify brand exists

```bash
test -f ./design/<brand-slug>/tokens.css
```

### 2. Gather the brief

Ask in one message:

```
1. Name — as it should appear on the card
2. Title / role — short, sentence-case (no periods on titles — they're labels not sentences)
3. Primary contact — pick ONE: email OR URL (the one you most want to receive)
4. Optional secondary contact — the other one
5. Optional location — city · timezone (e.g. "Louisville · GMT−5")
6. Optional secondary handle — e.g. "github.com/handle" for engineering brands
```

If the user wants more than 4 lines of text on the front, push back: "Business cards work at 4 lines max. What's essential?"

### 3. Pick variation — FRONT and BACK can use different archetypes

This is the rare skill where the front and back can take DIFFERENT visual approaches because they serve different functions (front = info; back = mark/identity):

**Front archetype:**
- `chrome-led` — name + title + contact-row, structured. Most common; readable.
- `type-only` — name at maximum scale, contact details small in corner. Confident.
- `inverse-text` — full canvas dark inversion (canonical v2 feature treatment). Bold.

**Back archetype:**
- `wordmark-dominant` — full brand wordmark centered or off-center; nothing else. The mark IS the back.
- `single-mark` — a single brand device (single character, monogram, or symbol) at maximum scale.
- `inverse-text` — dark inversion with wordmark in cream. Mirrors the front if front is also inverted.
- `chromeless` — the back is intentionally near-empty cream. The negative space IS the message.

**Color treatment** — pick a relationship between front and back:
- `same-surface` (both cream OR both inverted)
- `inverted-back` (front cream, back dark — a register flip when you turn the card)
- `inverted-front` (front dark, back cream — punchy front, quiet back)

### 4. Generate the HTML

Template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title><Brand> — Business card — <name></title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<families>&display=swap">
<style>
/* Embed tokens.css verbatim */
<contents of tokens.css>

html, body { margin: 0; padding: 0; background: #2a2a2a; min-height: 100vh; font-family: var(--type-sans-family); }
body { display: flex; flex-direction: column; align-items: center; gap: 32px; padding: 32px 0; }

.canvas-label { font-family: var(--type-mono-family); font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(255,255,255,0.7); align-self: center; }

/* Front + Back — both 1050×600 (3.5×2 inch at 300dpi) */
.canvas-front, .canvas-back {
  width: 1050px; height: 600px;
  position: relative; overflow: hidden;
  padding: 48px 56px;
  box-sizing: border-box;
  display: grid;
}

.canvas-front {
  background: var(--color-surface);
  color: var(--color-ink);
  grid-template-rows: auto 1fr auto;
  gap: 16px;
}

.canvas-back {
  background: var(--color-surface);   /* or --color-ink for inversion */
  color: var(--color-ink);
  display: grid; place-items: center;  /* default for wordmark-dominant back */
}

/* === Front composition === */
.front-name {
  font-family: var(--type-display-family);
  font-weight: 500;
  font-size: 64px;
  line-height: 1.0;
  letter-spacing: -0.018em;
  margin: 0;
  color: var(--color-ink);
}
.front-title {
  font-family: var(--type-display-family);
  font-weight: 600;
  font-variant-caps: small-caps; font-feature-settings: 'smcp';
  text-transform: lowercase;
  font-size: 16px; letter-spacing: 0.08em;
  color: var(--color-ink-3);
  margin: 12px 0 0;
}
.front-contact {
  align-self: end;
  display: flex; flex-direction: column; gap: 6px;
  font-family: var(--type-mono-family);
  font-size: 16px; letter-spacing: 0.04em;
  color: var(--color-ink);
}
.front-contact .secondary { color: var(--color-ink-3); }
.front-contact .label { font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--color-ink-3); margin-right: 12px; }

/* === Back composition === */
.back-wordmark {
  font-family: var(--type-display-family);
  font-weight: 500;
  font-size: 84px;
  letter-spacing: -0.018em;
  color: var(--color-ink);
  margin: 0;
  text-align: center;
}

/* Inverted variant */
.canvas-front--inverted, .canvas-back--inverted {
  background: var(--color-ink);
  color: var(--color-surface);
}
.canvas-front--inverted .front-name { color: var(--color-surface); }
.canvas-front--inverted .front-title { color: rgba(251, 250, 249, 0.55); }
.canvas-front--inverted .front-contact { color: var(--color-surface); }
.canvas-front--inverted .front-contact .secondary { color: rgba(251, 250, 249, 0.55); }
.canvas-front--inverted .front-contact .label { color: rgba(251, 250, 249, 0.55); }
.canvas-back--inverted .back-wordmark { color: var(--color-surface); }

@page { size: 1050px 600px; margin: 0; }
</style>
</head>
<body>
<!--
Variation choices:
  front-archetype: <picked>
  back-archetype:  <picked>
  color-relation:  <picked>
-->

<span class="canvas-label">→ FRONT · 1050×600 · 3.5×2 inch at 300dpi · name + contact</span>
<article class="canvas-front">
  <header>
    <h1 class="front-name">[Speaker name]</h1>
    <p class="front-title">[title / role]</p>
  </header>
  <span></span>
  <div class="front-contact">
    <span><span class="label">Email</span>[email@domain]</span>
    <span class="secondary"><span class="label">Web</span>[domain.com]</span>
    <span class="secondary"><span class="label">Loc</span>[city · timezone]</span>
  </div>
</article>

<span class="canvas-label">→ BACK · 1050×600 · wordmark-dominant</span>
<article class="canvas-back">
  <h1 class="back-wordmark">[Wordmark]</h1>
</article>

<!--
PRINT NOTES:
  - 1050×600 px = 3.5×2 inches at 300dpi (standard US business card)
  - Add 0.125" bleed on all sides for print → final: 1087.5×637.5 px (37.5px bleed each side)
  - Or 1125×675 px with safer 0.25" bleed
  - Crop marks NOT included — most print services add their own
  - For print-ready PDF: open each canvas in browser → File → Print → Save as PDF (page size auto-set by @page)
  - Recommended printers: Moo, Vistaprint, Jukebox (luxe stocks recommend cotton or fluorescent paper for cream brands)
-->
</body>
</html>
```

### 5. Verify

- [ ] Both canvases at exact 1050×600
- [ ] Front has at most 4 lines of text (name + title + contact rows)
- [ ] Title is sentence-case WITHOUT period (titles are labels, not sentences — distinct from headlines that DO end in period)
- [ ] Back is wordmark-dominant — minimal text, mark earns the space
- [ ] Architecture archetypes documented (front + back can differ; color relationship documented)
- [ ] **Read `../../design-anti-patterns.md` and verify the artifact violates none of its rules.** Pay special attention to sections 1 (no decorative orbs / patterns; no stock photography), 2 (no italics-emphasis OR single-word color emphasis as default), 4 (no center-aligned hero with template — the front composition should be intentionally asymmetric or grid-anchored, not centered-template)
- [ ] No "Founder & CEO" / "Co-founder" titles appended with em-dash decoration — the title is what it is

> Business card at `./design/<brand-slug>/artifacts/business-card-YYYY-MM-DD-<slug>.html`.
>
> Front: `<archetype>` · Back: `<archetype>` · Color: `<relation>`.
>
> Export each side: open in browser → DevTools → 1050×600 viewport → screenshot each `.canvas-front` and `.canvas-back` separately. Or use browser's "Save as PDF" with page size 1050×600.
>
> For print: add 0.125-0.25" bleed (notes in file footer). Most print services accept the rendered PNG/PDF directly.

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

- **Pixel exactness on both canvases.** 1050×600 = 3.5×2 inches at 300dpi.
- **At most 4 lines on the front.** Name + title + 2 contact rows is the maximum. More than that breaks the format.
- **Back is identity, not info.** Wordmark, brand device, or intentional negative space — never repeated contact info.
- **Title without period.** Titles are labels (no period); names without label suffix; contact is monospace data.
- **Print bleed documented in the file** so the user knows what to add when sending to a printer.
- **Token-pure.** Every visual value via `var(--*)` from tokens.css.
- **Anti-pattern compliance.** This skill defers to three shared canonical references: `../../design-anti-patterns.md` (the hard floor — wins every conflict), `../../design-principles.md` (the craft floor), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The anti-patterns file is the canonical anti-tell list.

---
name: tt-bolder
description: Amplify typography on TT Style surfaces using TikTokVF variable font capabilities. Push weight (800–900), introduce all-caps treatments with correct letter-spacing, and leverage width axis contrast to create dramatic typographic hierarchy. Use when a web or marketing surface feels typographically timid, uniform, or when a hero section needs stronger weight and presence. TT Style only — never on Strict TUX-native surfaces.
version: 1.0.0
user-invocable: true
argument-hint: "[target]"
license: Apache 2.0. Based on Anthropic's bolder skill. See tt-impeccable/NOTICE.md for attribution.
---

Amplify typographic presence on TT Style surfaces by fully exploiting TikTokVF's variable font capabilities — weight extremes, all-caps discipline, and intentional width contrast.

## MANDATORY PREPARATION

Invoke /tt-impeccable — it contains TUX design principles, token authority, and the Context Gathering Protocol. Follow the protocol before proceeding.

**Tier check**: If the surface is Strict TUX-native, stop immediately. TikTokVF weight 800/900, all-caps, and width axis use are TT Style only. TUX-native typography is fixed at 400/600/700 — do not modify it.

**Font check**: Confirm TikTokVF (variable font) is loaded in the project. If only TikTok Sans static files are present, weight 800/900 may not render as intended — verify the @font-face source before proceeding, and note the limitation to the user if needed.

---

## Assess Typography State

Identify what's holding the typography back:

1. **Timid weights**: Everything is 600–700. No element has 800 or 900 presence. The page reads as uniformly medium.
2. **Uniform scale**: Size differences between hierarchy levels are too small — 1.2–1.5x instead of 2–4x. Nothing commands the eye.
3. **No hero moment**: There is no single typographic element that anchors the viewport. The page is equally loud everywhere, which means it is quiet everywhere.
4. **Under-used all-caps**: For campaign landing pages and brand hero sections, all-caps + heavy weight is an authentic TikTok signature that is rarely applied when it should be.

**CRITICAL**: "Bolder" does not mean heavier everywhere. Weight 900 earns its presence only when the surrounding type drops to 400. The contrast is the drama — not the weight alone. Making everything 900 is the same mistake as making everything 600.

---

## Plan the Typographic Hierarchy

Establish clear roles before changing any weights. Three tiers maximum per page:

| Role | Weight | Size range | Quantity |
|---|---|---|---|
| **Hero / Display** | 900 | 72–96px+ | One per page or major section |
| **Section headings** | 800 | 48–72px | One or two per section |
| **Sub-heads, labels, body** | 400–600 | TUX type scale | Everything else |

If the current design has more than three weight tiers, collapse before amplifying. A muddled hierarchy cannot be fixed by adding more weight — only clarified by removing tiers.

---

## Amplify Weight

### Weight 800 — Section headings and prominent display text

Use at section hero text, campaign slogans, and prominent feature call-outs.

```css
font-family: 'TikTokVF', 'TikTok Sans', system-ui, sans-serif;
font-weight: 800;
font-size: 48px; /* 72px for section display heads */
letter-spacing: 0; /* see all-caps exception below */
```

### Weight 900 — Single hero moment per page

Use for one word or short phrase — the thing the entire section is built around. Do not scatter 900 across repeated headings or apply it to running text.

```css
font-family: 'TikTokVF', 'TikTok Sans', system-ui, sans-serif;
font-weight: 900;
font-size: 72px; /* minimum; 96px+ preferred for true hero presence */
letter-spacing: -0.02em; /* negative tracking at 72px+ per TT Style rules */
```

**The counter-weight rule**: Every weight-900 element must have weight-400 text nearby. The 900 reads as heavy because the 400 reads as light. Without the contrast pair, the hierarchy collapses.

---

## All-Caps Treatment

All-caps is an authentic TikTok brand aesthetic on web and marketing surfaces. Apply deliberately — not reflexively.

**When to use**: Hero callouts, section labels, campaign taglines, short punchy phrases. One all-caps element per visual zone maximum.

**When not to use**: Body copy, navigation, informational labels, anything longer than 5–6 words. All-caps at length degrades readability and loses its impact.

### Letter-spacing for all-caps (TT Style exception)

This overrides the standard TUX letter-spacing: 0 rule for all-caps text specifically:

- **All-caps 32–64px**: `letter-spacing: 0.06em` — restores optical spacing that uppercase removes; without this the letters appear cramped
- **All-caps 72px+**: `letter-spacing: -0.02em` — at display scale the optical spacing issue resolves; standard TT Style negative tracking applies

```css
/* All-caps at section-heading scale */
text-transform: uppercase;
font-weight: 800;
font-size: 48px;
letter-spacing: 0.06em;

/* All-caps at hero display scale */
text-transform: uppercase;
font-weight: 900;
font-size: 96px;
letter-spacing: -0.02em;
```

Mixed-case text at any size: `letter-spacing: 0`. No exception applies.

---

## Width Axis (if available)

TikTokVF may expose a width axis via `font-variation-settings`. Verify before using — a missing axis silently falls back to default width.

```css
/* Test: if this renders noticeably narrower, the axis exists */
font-variation-settings: 'wdth' 75;
```

**Width axis is decorative — display text only.** Apply wdth variation exclusively to hero display and section heading text. Never on body copy, navigation, or button labels — condensed text degrades body readability, and expanded text breaks TUX component sizing.

### Width Ladder

Width axis is most powerful as a third hierarchy signal, combined with size and weight:

```
Hero         → weight 900 + wdth 115–120 + 96px+   wide, heavy, maximum presence
Section head → weight 800 + wdth 100     + 48–72px  normal width, mid-tier
Label / sub  → weight 600 + wdth 80–85   + 14–16px  narrow, light, recedes
```

The progression wide → normal → narrow reinforces rank through shape alone, independent of color or position.

### Viewport-Filling Text

A single word or short phrase set to exactly span the container width — a recognized TikTok campaign aesthetic. Combine `font-size` in `vw` units with a `wdth` value to fine-tune the fit:

```css
.hero-word {
  font-family: 'TikTokVF', 'TikTok Sans', system-ui, sans-serif;
  font-weight: 900;
  font-size: clamp(72px, 12vw, 160px);
  font-variation-settings: 'wdth' 115;
  letter-spacing: -0.02em;
  text-transform: uppercase;
}
```

**TT Style exception**: `font-size` in `vw` or `clamp()` is permitted for viewport-filling display text only. This is the sole context where fluid type sizing is allowed — the word functions as a graphic element, not an information hierarchy level. Do not apply fluid sizing to any other text roles.

If the width axis is unavailable, use size and weight contrast alone. Do not fake condensed with `transform: scaleX()`.

---

## Layout

Typography at 800–900 weight naturally anchors spatial composition. A few patterns that work with — not against — the weight hierarchy.

### Asymmetric weight split

Place a 900/expanded word or phrase on one side of the layout; set body copy at 400/regular on the other. The visual weight imbalance is intentional — it directs the eye to the heavy side first, then releases it across to the light side to read.

Works at desktop (1440px canvas). Left-heavy is the more natural reading direction; right-heavy creates deliberate tension.

### Text bleed

An expanded-width hero word that slightly overflows the content container boundary — the last character or two clips at the edge. Communicates scale beyond the grid without increasing font size. The cropping itself signals that the type is too large to be contained, which amplifies presence.

Apply only to the single hero element. Do not bleed sub-headings or labels.

### Combined with expression colors (cross-skill)

When using tt-colorize's Brand Expression Palette as a section background, placing weight-900 text in a deeply related tone — not full contrast — creates depth through figure-ground tension rather than legibility contrast.

Example: Thrive (`#033624`) background with text at a slightly lighter forest green. The type is semi-visible, functioning as texture. Reserve this for purely decorative type (taglines, repeated brand words) — never for informational content that must be read.

---

## Verify Quality

- **Single hero moment**: Is there exactly one weight-900 element per page (or per major section)? If multiple elements compete at 900, demote all but the most important one.
- **Contrast pair present**: Does every weight-900 element have weight-400 text in its visual neighbourhood? If not, the hierarchy is not working.
- **All-caps used sparingly**: One all-caps element per visual zone. More than one and the effect is gone.
- **Letter-spacing correct**: All-caps 32–64px uses positive tracking. All-caps 72px+ uses negative. Mixed-case always 0.
- **TikTok Sans only**: No other typefaces introduced. This skill amplifies one font's range — it does not diversify the stack.
- **TT Style only**: Confirm that no weight-800/900 or all-caps was introduced on a Strict TUX-native surface.

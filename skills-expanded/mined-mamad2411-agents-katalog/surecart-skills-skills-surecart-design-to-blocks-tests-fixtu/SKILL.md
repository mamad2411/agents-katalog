# Expected emitted prompt (golden)

Given `answers.json` in this directory, the intake-mode emission should produce the message below. The closing message is emitted as plain prose; the fenced block contains the Claude Design prompt the merchant pastes.

---

## Closing message (plain prose, above the fenced block)

> I've prepared a Claude Design prompt for you based on your answers. Copy everything in the fenced block below and paste it into [design.claude.com](https://design.claude.com). Once Claude Design produces your export, come back here and paste/attach it — I'll convert it to paste-ready Gutenberg markup.
>
> If you want to refine any answer (mood, accent, sections), just tell me which one and re-invoke me.

## Populated prompt (inside fenced ```md block)

````md
# SureCart Product Page — Design Brief

## §0. Role + non-negotiable framing

You are designing for production WordPress e-commerce. Output is mechanically compiled into WordPress Gutenberg blocks by a server-side renderer with a fixed grammar — like generating MIDI for a sampler rather than recording audio. Visual flair beyond what the grammar supports cannot be preserved and will be discarded during compilation.

The constraints in §7 are not stylistic preferences; they are the grammar of the target format. Producing beautiful work means producing work that survives compilation intact.

## §1. Output contract

Produce a Claude Design project with the canonical 4-file structure:
- `product-page.jsx` — page composition
- `sections-1.jsx` — first half of section components
- `sections-2.jsx` — second half of section components
- `assets/colors_and_type.css` — `:root { --token: value }` design tokens

Use **only** components from §2 visual vocabulary. Annotate render surfaces with JSX comments from §3. Style with CSS variables from §4 (raw hex reserved for non-color literals only).

## §2. Visual vocabulary you may use

(see prompt-template.md §2 — the same 25-component vocabulary block emits verbatim)

## §2b. Block-style variations

(see prompt-template.md §2b — the same 9-row variation table emits verbatim)

## §3. Render surfaces

(see prompt-template.md §3 — the two PRODUCT-TEMPLATE / STATIC-CONTENT markers emit verbatim, plus the placement rule)

## §4. Style tokens (CSS variables, not raw hex)

```css
:root {
  --sc-accent: var(--wp--preset--color--surecart-brand);
  --sc-text:   var(--wp--preset--color--surecart-text);
  --sc-bg:     var(--wp--preset--color--surecart-bg);
  --sc-display: var(--wp--preset--font-family--surecart-display);
  --sc-body:    var(--wp--preset--font-family--surecart-body);
}
```

Raw `#RRGGBB` is reserved for non-color literals only. The accent resolves to **`surecart-brand`** (`#01824C` — for your visual reference only; the emitted CSS uses the preset variable).

(`core/icon` catalog — see prompt-template.md §4 — same 88-slug semantic table emits verbatim)

## §5. Reference design — visual anchor

Use this structural shape as your starting point (paste-tested **aurora-lamp**):

```jsx
{/* SURFACE: PRODUCT-TEMPLATE */}
<StickyHeader> :: brand-mark + nav + <CartIcon/> </StickyHeader>
<Hero cols="2">
  <ProductGallery is-style-orbit/>
  <Pill text="JUST RESTOCKED"/>
  <ProductTitle/>
  <ReviewStars/>            {/* inline summary */}
  <ProductPrice/> <PriceScratch/> <PriceInterval/>
  <Quantity is-style-pebble/>
  <BuyButtons>
    <BuyButton primary addToCart/>
    <BuyButton outline/>
  </BuyButtons>
</Hero>
{/* /SURFACE: PRODUCT-TEMPLATE */}

{/* SURFACE: STATIC-CONTENT */}
<ReviewSection/>
<FAQ/>
<RelatedProducts/>
{/* /SURFACE: STATIC-CONTENT */}
```

## §6. Merchant brief

- **Brand mood:** Clean default (visual reference: `aurora-lamp`).
- **Product type:** Physical product.
- **Pricing model:** One-time.
- **Variants:** None.
- **Sections to include:** Reviews (full section + ratings histogram), FAQ (accordion), Related products (4-up grid).
- **Typography:** Match theme.
- **Accent color:** SureCart default (sage green) (preset: `surecart-brand`).

Photography, copy tone, product specifics: invent placeholders consistent with the product type — the merchant will swap them post-paste. Title, price, buy-button text are **server-rendered** (see §7 rule 1) — use the placeholder components from §2.

## §7. Hard prohibitions

(see prompt-template.md §7 — the 10 rules emit verbatim with constraint-family tags `[SC-DATA]` / `[SC-BLOCK]` / `[WP-CORE]`)

## §7b. Extended alias map

(see prompt-template.md §7b — the 16-row map emits verbatim)

## §8. Self-check (advisory only)

(see prompt-template.md §8 — the 5-item self-check list emits verbatim)
````

---

## Slot substitution table (for this fixture)

| Slot | Resolved value |
| --- | --- |
| `Q1_PRODUCT_TYPE` | Physical product |
| `Q2_ACCENT_DESCRIPTION` | SureCart default (sage green) |
| `ACCENT_PRESET_SLUG` | `surecart-brand` |
| `ACCENT_RESOLVED_HEX` | `#01824C` |
| `Q3A_VARIANTS` | None |
| `VARIANT_BLOCK` | (empty string — Q3a=None) |
| `Q3B_PRICING` | One-time |
| `Q4_SECTIONS` | Reviews (full section + ratings histogram), FAQ (accordion), Related products (4-up grid) |
| `STATIC_SECTIONS` | `<ReviewSection/>\n<FAQ/>\n<RelatedProducts/>` |
| `Q5_VISUAL_MOOD` | Clean default |
| `EXEMPLAR_HANDLE` | aurora-lamp |
| `Q6_TYPOGRAPHY` | Match theme (default applied since Q6 was branched out) |
| `DISPLAY_FONT_SLUG` | `surecart-display` |
| `BODY_FONT_SLUG` | `surecart-body` |
| `HERO_PILL_TEXT` | JUST RESTOCKED (derived from Q1=Physical + Q3b=One-time) |
| `HERO_TRAILING_SECTIONS` | (empty — Q4 does not include "Sticky bar") |

## Verification

A snapshot test compares the renderer output against this golden:

```
node tests/fixtures/intake-01-minimal-answers/answers.json
  → fed through prompt-template.md renderer
  → should match expected-prompt.md byte-for-byte (after stripping comments-around-the-fenced-block)
```

The "see prompt-template.md §X" inlined references above are themselves emitted verbatim from `prompt-template.md` — they are NOT placeholders in the golden. The expected-prompt.md elides them to keep the fixture readable; an automated renderer expands them.

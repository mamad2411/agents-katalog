---
name: tt-colorize
description: Apply TikTok Brand Expression Palette colors to TT Style surfaces that are too monochromatic or need campaign-specific brand atmosphere. Use when a web or marketing surface feels visually flat, lacks brand character, or needs a distinct campaign vibe beyond the standard red+teal palette. TT Style only — never on Strict TUX-native surfaces.
version: 1.0.0
user-invocable: true
argument-hint: "[target]"
license: Apache 2.0. Based on Anthropic's colorize skill. See tt-impeccable/NOTICE.md for attribution.
---

Apply TikTok's Brand Expression Palette to TT Style surfaces that feel too monochromatic or need a distinct campaign character beyond the standard Blaze + Glint palette.

## MANDATORY PREPARATION

Invoke /tt-impeccable — it contains TUX design principles, token authority, and the Context Gathering Protocol. Follow the protocol before proceeding.

**Tier check**: If the surface is Strict TUX-native, stop immediately. Brand Expression colors have no role in product UI screens — they are not part of the TUX token system.

---

## Assess Color Opportunity

Before picking a color, understand what's missing:

1. **Is the design too monochromatic?** A TT Style page of pure black + Blaze + white has range, but some campaign surfaces need stronger atmosphere — a color that signals creative territory before a word is read.
2. **What campaign vibe is needed?** Energy/hype, softness/artistry, premium/immersive, organic/sustainable — each maps to a different expression color.
3. **What already exists?** Don't add expression color on top of an already dense layout. Expression color needs room to read as intentional.

If you cannot answer #2 from the codebase or brief, ask the user directly.

**CRITICAL**: Expression color is atmospheric, not decorative. One well-placed expression color anchors a section's vibe. Multiple expression colors in the same visual zone is not "more expressive" — it's incoherent.

---

## Choose an Anchor Color

Pick ONE expression color per visual zone. All values and CSS variables are defined in `reference/tokens.md` → Brand Expression Palette.

| Color | Hex | Vibe | Pairs well with |
|---|---|---|---|
| Thrive | `#033624` | Creator economy, sustainability, depth | Glow (green + yellow energy) |
| Shimmer | `#BAF6F0` | Dreamy, fresh, cool-toned softness | Black + white only |
| Dawn | `#EDBBE8` | Artistic, gentle, expressive | Black or Blaze accent |
| Ember | `#4A0505` | Immersive, premium, brooding | White text, neutral accents |
| Glow | `#FBEB35` | Energy, hype, Gen Z vitality | Black + Thrive |
| Muse | `#EDD4B2` | Lifestyle, fashion, warm ground | Most versatile — pairs with any |

**Hard constraints** (enforced by pairing rules in `reference/tokens.md`):
- DO NOT use **Ember + Blaze** on the same surface — both are dark red-family; they conflict rather than harmonize
- DO NOT use **Shimmer + Glint** on the same surface — same mint-teal family; the expression fill and the UI secondary token become indistinguishable
- ONE expression color per zone — never two expression fills side by side in the same section

---

## Apply the Expression Color

Expression colors belong in three places only.

### 1. Section backgrounds and hero zones

The primary use. A full-width section with a Thrive or Glow background immediately establishes campaign territory. This is where expression color earns its presence.

- Apply as `background-color` using the `--tt-expr-*` variable
- Full-bleed is preferred — a small card with expression background looks accidental, not intentional
- Text on expression backgrounds: use the pairing table in `reference/tokens.md`

### 2. Large display text accents

At 72px+, an expression color on a single hero word or short phrase adds energy without overwhelming. Below 48px, expression colors on text read like a UI semantic signal (link, error, warning) — avoid.

### 3. Decorative and graphic elements

Geometric shapes, background patterns, illustrative fills that reinforce the atmospheric vibe without competing with content hierarchy.

**NEVER apply expression colors to:**
- Button fills or CTAs — Blaze (`#FE2C55`) owns this role
- Toggle tracks — Glint (`#20D5EC`) owns this role
- Status badges, notification dots, or any semantic state indicator
- Interactive icons in their resting state
- Image or video overlays — black-alpha overlays only; this rule is universal across all tiers
- Any element where the color could be read as "this is tappable"

---

## Maintain TUX Semantic Integrity

Adding expression color must not corrupt TUX's color-as-interaction-signal system.

- Blaze and Glint keep their canonical semantic roles unchanged on the page
- A user who sees Glow on a section background should never wonder "is this a button?"
- Expression colors are mute — they set a mood, they do not communicate action

If an expression color lands on something that looks interactive, either move it to a non-interactive element or remove it.

---

## Verify Quality

- **Still TikTok?** Does the page feel like a TikTok campaign property, or like a generic colorful page? Expression colors anchor identity only when the TUX token system — typography, spacing, Blaze CTA — is intact beneath them.
- **One anchor per zone?** Count expression color appearances. More than one in the same visual zone is too many.
- **Semantics intact?** Every Blaze element is still a CTA. Every Glint element is still a toggle or verified signal.
- **Text legible?** Verify against the pairing table in `reference/tokens.md`. Never invent text colors on expression backgrounds.
- **Audit-safe?** All expression color values must use `--tt-expr-*` CSS variables, traceable to `reference/tokens.md`. Raw hex values in component code will trigger audit warnings.

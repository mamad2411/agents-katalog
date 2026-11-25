---
name: design_card-invitation
description: Use when the user needs card & invitation design skill guidance, generation, or critique based on LICA layout principles.
---

# Card & Invitation Design Skill

You are an expert card and invitation designer trained on the LICA dataset of celebratory and event layouts. Apply these principles when designing or critiquing greeting cards, wedding invitations, birthday cards, and event invitations.

## Canvas & Dimensions
- Square card: 1080×1080px (social), 800×800px (print)
- Portrait invitation: 794×1123px (A4), 750×1050px (5×7 inch at 150dpi)
- Landscape postcard: 1200×800px or 1050×750px
- Digital social card: 1080×1080px or 1080×1920px (Stories)

## Design Tone Categories (from LICA annotations)
Each card type demands a distinct emotional register:

### Wedding / Formal Invitation
- Elegant, restrained — let negative space do the work
- Script or serif headline font; paired with a light sans for details
- Palette: ivory, blush, gold, navy, sage — never more than 2 accent colors
- Florals, botanical motifs, geometric frames as decorative elements

### Birthday Card
- Energetic, joyful — bold color, playful type, confetti/balloon motifs
- Mix a display font (headline) with a rounded sans (body)
- Bright saturated palette; pastels for children, jewel tones for milestone birthdays

### Holiday / Seasonal Card
- Themed imagery dominant (Christmas, Diwali, Eid, etc.)
- Warm palette for winter holidays; fresh greens/pinks for spring
- Greeting text as hero — large, centered, handwritten-style font

### Thank You / Condolence Card
- Minimal, sincere — reduced color, generous white space
- Soft neutral palette; single muted accent
- Typography: clean serif or handwritten script, nothing decorative or playful

## Layout Principles (from LICA annotations)
- **Emotional hierarchy**: The greeting/occasion is the hero — it should be instantly legible
- **Frame compositions**: Use border, botanical, or geometric frame elements (GROUP components) to create a contained, gift-like feel
- **Center-axis alignment** is the default for formal cards; left-align only for modern/editorial styles
- **Layering**: Background → Decorative motif layer → Text layer (3 depth levels max)
- Avoid splitting headline text across a motif — keep text zones clean and motif-free

## Typography Rules
- Headline/greeting: large, expressive — script, serif display, or bold sans (48–80px)
- Event details: smaller, aligned block — date, time, venue (16–22px)
- Body/RSVP text: minimal, clear sans-serif (12–16px)
- Use `letter_spacing` (tracking) generously for formal invitations — creates luxury feel
- Maximum 2 typefaces: one expressive display + one readable body

## Color & Visual
- Background: textured, gradient, or soft solid — avoid plain white for print cards
- Motifs and decorative elements: use `GROUP` with `clip_path: true` for shapes; `IMAGE` for illustrations
- Decorative IMAGE opacity: `0.15–0.35` for subtle background motifs, `1.0` for featured illustrations
- Gold/foil effects: simulate with warm yellow `#C9A84C` or `#D4AF37` on dark backgrounds
- Floral/botanical overlays: top and bottom corners, not center — preserve text clarity

## Component Placement (JSON structure awareness)
```
Card Canvas (width × height)
├── Background GROUP or IMAGE (full bleed, texture or color)
├── Border/frame GROUP (inset 20–40px, decorative outline)
├── Motif IMAGE (corner or edge placement, low opacity)
├── Greeting TEXT (hero, centered, upper-center or full-center)
├── Occasion/name TEXT (secondary, directly below greeting)
├── Divider GROUP (ornamental line or flourish)
├── Event details TEXT block
│   ├── Date TEXT
│   ├── Time TEXT
│   └── Venue TEXT
├── RSVP block TEXT (bottom zone, smaller)
└── Decorative accent IMAGE (bottom corners, mirrored)
```

## Decorative Element Principles
- **Symmetry**: formal cards use bilateral symmetry (mirror corners)
- **Scale contrast**: pair tiny delicate motifs with large bold type for tension
- **Breathing space**: decorative elements should never touch the headline text
- **Motif family**: all decorative images within one card must share the same illustration style (all watercolor, all line-art, all vector — never mixed)

## Design Intents (LICA user_intent patterns)
- **Wedding invitation**: script headline, botanical frame, ivory/gold palette, formal block for details
- **Birthday party invite**: bold number as hero, confetti motifs, bright colors, playful font
- **Baby shower**: soft pastels, gender-neutral or themed palette, illustrated character
- **Holiday greeting**: full-bleed festive imagery, warm greeting text, subtle card border
- **Corporate event invite**: clean, minimal, brand colors, typography-led, no illustrative motifs

## Critique Checklist
When reviewing a card or invitation design, evaluate:
- [ ] Is the occasion/greeting instantly clear within 1 second?
- [ ] Does the emotional tone of the design match the event type?
- [ ] Are decorative motifs placed to frame, not obscure, the text?
- [ ] Is the typography combination harmonious (display + body pairing)?
- [ ] Does the color palette feel cohesive (max 3 colors)?
- [ ] Is critical information (date, time, venue) easy to find and read?
- [ ] Is decorative symmetry intentional and balanced?
- [ ] Is the illustration style consistent across all visual elements?

## Usage
When a user asks to design, critique, or improve a card or invitation, apply all principles above. Ask for: occasion type, formality level (casual/formal/luxury), color preferences, any text content (names, date, venue), and distribution format (print/digital) before generating a layout specification.

---
name: design_flyer
description: Use when the user needs flyer design skill guidance, generation, or critique based on LICA layout principles.
---

# Flyer Design Skill

You are an expert flyer designer trained on the LICA dataset of promotional layouts. Apply these principles when designing or critiquing flyers.

## Canvas & Dimensions
- Portrait standard: 816×1056px (US Letter) or 794×1123px (A4)
- Landscape promo: 1200×628px (social/web flyer)
- Square: 1080×1080px (Instagram/social)
- Choose based on distribution channel: print → portrait letter/A4, digital social → square or landscape

## Layout Principles (from LICA annotations)
- **One dominant headline**: The largest text element must answer "what is this?" instantly
- **3-zone structure**: Hero image zone (top 50%) → Headline + body (middle 30%) → CTA + details (bottom 20%)
- **Visual entry point**: Image or large typographic element anchors the eye at top-center
- **CTA must be isolated**: Surround call-to-action text with a GROUP background shape (button)
- Never let text overlap image without a contrast-ensuring overlay (semi-transparent GROUP)

## Typography Rules
- Headline: max 2 lines, extremely large (48–96px equivalent), bold or black weight
- Subheadline: 50–60% of headline size, medium weight
- Body copy: 12–16px, regular weight, line-height 1.4–1.6
- CTA button text: all-caps or title-case, bold, contrasting color to button background
- Maximum 2 font families; display font for headline, readable sans for body

## Color & Visual
- Use a bold, energetic palette — flyers compete for attention
- Background: can be rich/dark; let headline color pop against it
- Images: use `opacity: 1.0` for hero images, overlay GROUP at `opacity: 0.4–0.6` for text legibility
- Accent shapes via `GROUP` with `clip_path: true` — diagonal cuts, circles, and ribbons signal promotions
- Consistent color theme: event flyers use analogous colors; sale flyers use high-contrast complementary

## Component Placement (JSON structure awareness)
```
Canvas (width × height)
├── Background IMAGE or GROUP (full bleed)
├── Overlay GROUP (semi-transparent, for text zones)
├── Hero IMAGE (top 40–55% of canvas)
├── Headline TEXT (largest, centered or left-aligned)
├── Subheadline TEXT
├── Body TEXT (event details, 2–4 lines max)
├── Divider GROUP (decorative line or shape)
├── CTA GROUP (button container)
│   └── CTA TEXT
├── Logo IMAGE (top-left corner, small)
└── Footer TEXT (fine print, address, date/time)
```

## Design Intents (LICA user_intent patterns)
- **Event promo**: Date/time/venue dominant; energetic palette; countdown urgency
- **Sale/discount**: % or $ figure as giant hero text; red/yellow; "LIMITED TIME" urgency cue
- **Community/nonprofit**: Warm imagery; approachable sans-serif; pastel or earth tones
- **Corporate announcement**: Clean grid; brand colors; minimal imagery; formal hierarchy
- **Party/nightlife**: Dark background; neon accents; textured or gradient overlays

## Aesthetics Guidelines (LICA aesthetics field patterns)
- Contrast ratio: text on backgrounds must meet WCAG AA (4.5:1 for body, 3:1 for large text)
- Focal density: top third should have the highest visual weight
- Breathing room: even busy flyers need one "quiet" zone to rest the eye
- Consistency: margins, padding within text blocks should be uniform multiples (8px grid)

## Critique Checklist
When reviewing a flyer design, evaluate:
- [ ] Can you read the headline in under 2 seconds from normal viewing distance?
- [ ] Is the CTA visually distinct and easy to find?
- [ ] Does text have sufficient contrast against its background?
- [ ] Is the hierarchy (headline > subheadline > body > CTA) unambiguous?
- [ ] Are there fewer than 4 distinct font sizes?
- [ ] Is there a clear visual entry point at the top of the design?
- [ ] Does the overall color palette match the emotional tone of the message?

## Usage
When a user asks to design, critique, or improve a flyer, apply all principles above. Ask for: event/purpose, target audience, distribution channel (print/digital/social), key message, and deadline/date before generating a layout specification.

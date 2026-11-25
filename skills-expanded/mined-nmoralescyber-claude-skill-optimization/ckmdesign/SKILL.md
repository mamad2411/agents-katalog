---
name: ckmdesign
description: Designs brand identity for cybersecurity and B2B technology products — logo, color palette, typography, brand mark, design tokens, and full corporate identity programs. Make sure to use this skill whenever the user says design a logo, create our brand identity, build a brand mark, choose brand colors, design our visual identity, build a corporate identity program, design a brand system, or describes any work establishing or refining the visual brand of a security/tech company. Specializes in trust-conveying brand patterns appropriate for security buyers — clean technical authority, restraint over flash, sophisticated color palettes (avoiding cliched cybersecurity tropes like binary rain or glowing locks), serif/sans pairings that signal credibility. Includes 55 logo styles, 50-deliverable corporate identity program, color theory for trust, typography pairings, brand voice guidance. Do NOT use for: web UI implementation (use ckmui-styling), presentation slides (use ckmslides), banner ads (use ckmbanner-design), individual icons (separate icon design skill if available). Defining characteristic: "establishing or refining brand-level visual identity, not implementing UI."
---

# Brand Design (Cybersecurity-First)

Brand identity for cybersecurity and B2B technology — logo, palette, typography, identity programs.

## When to use vs. adjacent design skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Designing brand-level visual identity | Implementing web UI → `ckmui-styling` |
| Logo, brand mark, brand colors, brand fonts | Building presentation slides → `ckmslides` |
| Corporate identity program (50 deliverables) | Banner ads or social creative → `ckmbanner-design` |
| Brand guidelines document | Conversion landing page → `create-landing-page` |
| Trust-conveying visual system | UI component design → `ckmui-styling` |

## Cybersecurity brand principles

Security buyers — CISOs, security engineers, compliance teams — are sophisticated and skeptical. They've seen every cliché. The brand decisions:

### What works for security brands

- **Restraint** — clean, uncluttered, technical-authoritative. Companies like Stripe (financial trust), Linear (engineering precision), Cloudflare (technical credibility), 1Password (security-as-product) all share aesthetic restraint.
- **Sophisticated color** — deep blues, slate grays, restrained accent colors. NOT neon greens on black (toy-hacker aesthetic) or panic reds.
- **Typography that signals depth** — neo-grotesque sans (Inter, IBM Plex, Söhne) or serif/sans pairing for editorial weight (Source Serif + Inter).
- **Logos that work at all sizes** — favicon (16px) to billboard. Test the logo as a 16px square BEFORE finalizing.
- **Logos that work in single color** — solid black, solid white, knocked-out reverse. If it requires a gradient to read, it's not finished.
- **Negative space as a design element** — confident brands don't fill every pixel.
- **Consistent iconography system** — one icon library used throughout (Lucide, Phosphor, Heroicons all work).

### What kills security brand credibility

- **Hooded hacker imagery** — instant signal of unsophistication
- **Binary rain / 1s and 0s in the background** — Hollywood cliché
- **Glowing padlocks** — overdone since 2005
- **Shield-as-logo** — overdone since 2008 (Norton, McAfee, dozens of MSPs)
- **Neon green / matrix aesthetic** — "we're for hackers" is the wrong message for buyers
- **Stock-photo people in suits** — generic vendor signal
- **Flashy gradients without purpose** — looks like a crypto product
- **Sci-fi futurism** — buyers want stable, dependable, today
- **Logo fights** — wordmark vs. mark vs. tagline all competing for attention
- **Hyperbolic taglines** — "the future of cybersecurity," "AI-powered next-gen XDR" are read as filler

## Logo design process

### Phase 1 — Discovery (gather before designing)

- Company name (and how it's pronounced — affects wordmark legibility)
- 3-5 brands the founder admires (and 2-3 to avoid, with reasons)
- Target buyer (technical / business / both)
- Product category (the closest 3 competitors and how they're positioned)
- Differentiation in one sentence (the brand has to support this)
- Required usage contexts (web, app icon, slide, business card, swag, signage)
- Restrictions (brand colors already chosen? font already chosen? trademark conflicts?)

### Phase 2 — Concept directions

Produce 3-5 distinct concepts (not variants of one concept):

| Direction | Common in security | When to use |
|---|---|---|
| Wordmark only | Stripe, Linear, Vercel | Clean, scalable, when the name is short and distinctive |
| Wordmark + symbol | Cloudflare, Snowflake | Most common; symbol gives a separable element for app icons |
| Symbol-only mark (rare) | Apple, Twitter (historical) | When the brand has earned recognition; rarely right at launch |
| Lettermark / monogram | IBM, AWS | When name is long; monogram of initials |
| Combination mark | DigitalOcean | Symbol and wordmark always together as a unit |

For each concept, sketch in low fidelity first. High fidelity wastes time on concepts that will be rejected.

### Phase 3 — Refinement

Pick 1-2 directions, refine to high fidelity:

- Test at multiple sizes (16px favicon → 200px header → billboard scale)
- Test in 3 contexts (homepage, app icon, business card)
- Test single-color, reverse, on photo background
- Test color variants (3-4 palette options if not yet chosen)
- Iterate on weight, kerning, spacing
- Check trademark uniqueness via web search

### Phase 4 — Specification

Deliver as a brand kit:
- SVG (vector, scalable)
- PNG variants (transparent, white bg, dark bg, single color, reverse)
- Favicon set (16, 32, 48, 96, 192, 512px)
- App icon (1024px, with safe area for iOS rounded corners)
- Spacing rules (clear space around logo)
- Don't list (sketches of misuse to avoid)

## Color palette for security brands

### Recommended starting points

**Trust-stable (most common, low risk):**
- Primary: deep blue (#1e3a8a / #1e40af / #1d4ed8)
- Secondary: slate or warm gray
- Accent (sparingly): amber or single bright color for CTAs

**Technical-modern:**
- Primary: indigo or violet (#4f46e5 / #6366f1)
- Secondary: slate
- Accent: cyan or teal

**Editorial-authoritative:**
- Primary: deep navy or near-black
- Secondary: warm beige or sand
- Accent: deep red (only for editorial flag use)

**Minimal-monochrome:**
- Primary: pure black or near-black
- Surface: white + warm gray scale
- Single accent color (often brand-specific)

### Color decisions that fail

- Bright green → toy-hacker
- Hot pink → looks like consumer / lifestyle product
- Pure rainbow → unfocused
- Pastels → not authoritative for security context
- Neon → unstable / unprofessional
- All gradient → trendy but ages fast

### Palette specification

For every brand, define:
- 1 primary hue (with 5 shades from light to dark)
- 1 secondary or neutral hue (with 9-11 shades for surfaces and text)
- 4 semantic colors (success, warning, error, info — used in product UI)
- Specific use cases for each color

## Typography for security brands

### Recommended pairings

| Display (headlines) | Body (UI / long-form) | Mono (code, IDs) | Vibe |
|---|---|---|---|
| Inter | Inter | JetBrains Mono | Technical-modern (default) |
| Söhne | Söhne | Söhne Mono | Premium-editorial |
| IBM Plex Sans | IBM Plex Sans | IBM Plex Mono | Engineering-credible |
| Söhne Breit (display) | Inter (body) | JetBrains Mono | Bold-with-stable-body |
| GT Walsheim | Inter | JetBrains Mono | Friendly-with-credibility |
| Tiempos Headline | Inter | JetBrains Mono | Editorial weight + UI clarity |

### Typography mistakes

- More than 2 sans-serif fonts in a system
- Custom display font with no licensed body pair
- Monospace as body font (legibility falls apart at long form)
- Display font at body sizes (designed for ≥48px; broken at 14-16px)
- Pairing fonts of similar weight/personality (creates visual mush)

## Corporate Identity Program (CIP) deliverables

For full identity programs, the standard 50-deliverable set (varies by org needs):

### Brand guidelines (the document)
1. Brand story / positioning
2. Brand voice / tone
3. Logo system (variants, clear space, don't list)
4. Color palette (primary, secondary, semantic, accessibility notes)
5. Typography system (pairings, scale, hierarchy)
6. Iconography system
7. Photography / illustration style (if any)
8. Design tokens (if shipping to dev team)
9. Brand applications (sample touchpoints)
10. Brand governance (who decides, how to evolve)

### Digital assets
11. Logo files (all variants, vector + raster)
12. Favicon set
13. App icons (iOS, Android, web)
14. Social profile images (square, banner, per platform)
15. Email signature template
16. Slide template (links to ckmslides)
17. Document template (Google Docs / Word)
18. Spreadsheet template
19. Brand-themed file naming convention
20. Brand asset library structure

### Marketing materials
21. Website hero patterns
22. Landing page templates
23. Blog post templates
24. Social post templates (per platform)
25. Email newsletter template
26. Webinar slide template
27. Trade show booth specs
28. Conference banner specs
29. Customer case study template
30. Press kit assembly

### Sales materials
31. Sales deck template
32. One-pager template
33. Datasheet template
34. ROI calculator template
35. Customer proposal template
36. Contract / SOW template (visual identity, not legal content)

### Product / Internal
37. Product UI design tokens (handoff to ckmui-styling)
38. Product onboarding visuals
39. In-app help illustrations
40. Error state illustrations
41. Empty state illustrations
42. Internal team comms template
43. All-hands deck template
44. Hiring page assets
45. Job description template

### Physical
46. Business card template
47. Letterhead
48. Envelope
49. Swag spec (t-shirt, sticker, notebook)
50. Office signage

## Brand voice (foundation for written communications)

For security brands, voice should be:

- **Direct** — no hedging, no qualifiers piled up
- **Specific** — concrete numbers, named threats, named technologies
- **Confident without arrogance** — state capabilities; don't oversell
- **Educational** — buyers learn from you; you're the expert
- **Honest about limitations** — sophisticated buyers respect transparency

Voice anti-patterns:
- Marketing-speak superlatives ("the most advanced", "next-generation")
- Vague urgency ("don't get hacked")
- Fear-only positioning (without solution specificity)
- Tech jargon as decoration (without substance behind it)
- Casual when serious matters arise (security has gravity; respect it)

## Output

Depending on request:
- **Logo concepts:** 3-5 distinct directions with rationale, low-fi sketches first if early
- **Refined logo:** vector files, all standard variants, spec sheet
- **Color palette:** named colors with hex codes, intended use, accessibility check
- **Typography system:** font choices with licensing notes, scale, pairing examples
- **Brand kit:** comprehensive package per CIP deliverable list
- **Brand guidelines doc:** structured PDF or web-ready Markdown
- **Always:** trademark check note, file format spec, usage context test (favicon + billboard scale)

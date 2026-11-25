---
name: ckmbanner-design
description: Designs banners for social media (LinkedIn header, Twitter/X header, YouTube banner, Facebook cover, Instagram), display ads (Google Display, LinkedIn ads), website heroes, and print collateral. Make sure to use this skill whenever the user says design a banner, create a LinkedIn header, build a Twitter/X header, design a YouTube banner, create a Google Display ad, build a website hero image, design ad creative, hero banner for [page], or describes wanting any banner-format graphic. Includes platform-specific dimensions and 22+ style options (minimalist, gradient, photo-based, geometric, glassmorphism, neon, etc.). Do NOT use for: full web page design (use ckmui-styling), logo or brand identity work (use ckmdesign), presentation slides (use ckmslides), single-page sales collateral / one-pagers (use create-one-pager), or landing pages (use create-landing-page). Defining characteristic: "wide-format graphic for a specific platform with that platform's dimensional and style conventions."
---

# Banner Design

Platform-aware banner and hero graphic design — social, ads, web heroes, print.

## When to use vs. adjacent design skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Wide-format graphic for a specific platform | Full page design → `ckmui-styling` |
| Social media header / cover | Logo or brand identity → `ckmdesign` |
| Display ad creative | Slide deck → `ckmslides` |
| Website hero image | One-page collateral → `create-one-pager` |
| Print banner / signage | Landing page (interactive) → `create-landing-page` |

## Platform dimensions cheat sheet

| Platform | Banner type | Dimensions (px) | Notes |
|---|---|---|---|
| LinkedIn | Personal cover | 1584 × 396 | Profile photo overlaps lower-left; design around it |
| LinkedIn | Company page | 1128 × 191 | Smaller than personal; logo in lower-left |
| LinkedIn | Sponsored content | 1200 × 627 | Same as Facebook ad spec |
| Twitter/X | Profile header | 1500 × 500 | Profile pic overlays lower portion |
| Twitter/X | In-stream image | 1600 × 900 | 16:9 |
| YouTube | Channel banner | 2560 × 1440 | "Safe area" for all devices: 1546 × 423 center |
| Facebook | Profile cover | 851 × 315 | Personal profile |
| Facebook | Page cover | 820 × 312 | Business pages |
| Facebook | Ad image | 1200 × 628 | News-feed ads |
| Instagram | Feed post | 1080 × 1080 | Square |
| Instagram | Story | 1080 × 1920 | 9:16 vertical |
| Instagram | Reels cover | 1080 × 1920 | Same as story |
| Pinterest | Pin | 1000 × 1500 | 2:3 ratio |
| TikTok | Video cover | 1080 × 1920 | 9:16 |
| Threads | Post image | 1080 × 1080 | Square |
| Google Display | Various ad sizes | See below | Multiple sizes for IAB ad placements |
| Google Display | Leaderboard | 728 × 90 | Top of page |
| Google Display | Medium rectangle | 300 × 250 | Most common display ad |
| Google Display | Large rectangle | 336 × 280 | Larger in-content |
| Google Display | Skyscraper | 160 × 600 | Sidebar |
| Google Display | Half page | 300 × 600 | Sidebar large |
| Google Display | Mobile banner | 320 × 50 | Mobile in-app |
| Website hero | Standard | 1920 × 1080 | Or whatever your design system specifies |
| Print banner | Trade show | Varies | Often 8' × 3' (96"×36") |

## 22 banner styles

Each style has a use case. Pick by brand fit + platform:

1. **Minimalist** — large negative space, single focal element, brand-confident
2. **Gradient (modern)** — multi-stop linear/radial, feels current
3. **Photo-based** — high-quality photography behind text overlay
4. **Bold typography** — text as the design, large + impactful
5. **Geometric** — shapes and patterns as primary visual
6. **Glassmorphism** — frosted glass effects, layered depth
7. **Neumorphism** — soft 3D shadows (use sparingly, can date)
8. **Brutalist** — raw, intentionally crude, attention-getting
9. **Neon** — glowing accents, dark backgrounds
10. **Duotone** — two-color photo treatment
11. **Editorial** — magazine-cover styled
12. **Collage** — overlapping elements, layered
13. **Illustrated** — custom illustration as hero
14. **Retro** — period-specific aesthetic (80s, 90s, etc.)
15. **3D rendered** — depth and lighting
16. **Isometric** — 3D-ish at fixed angle, common for tech
17. **Animated (GIF/WebM)** — motion as design element
18. **Data-viz** — chart or numbers as the visual
19. **Product screenshot** — actual product UI as hero
20. **Founder / team** — personal, human-centered
21. **Testimonial-led** — customer quote + photo
22. **Abstract / textural** — pattern or texture for mood

## Cybersecurity-appropriate banner styles

For cybersec founder/product, recommended styles:

**Best fits:**
- **Minimalist** — signals confidence, technical authority
- **Bold typography** — focused message, no clutter
- **Data-viz** — credible, quantitative
- **Product screenshot** — concrete, no fluff
- **Geometric** — clean, technical-modern

**Use carefully:**
- **Photo-based** — only with custom photography, never stock; team photos work, generic "people in office" doesn't
- **Gradient** — okay if subtle and on-brand; avoid trendy crypto-style gradients
- **3D rendered** — okay for product hero; avoid for personal/profile

**Avoid for cybersec:**
- **Neon / matrix-style** — toy-hacker aesthetic
- **Brutalist** — wrong tone for trust-building
- **Retro** — security buyers want today, not nostalgia
- **Collage** — looks unfocused

## Banner design principles

### 1. Platform-native first
Every platform has visual conventions. A LinkedIn header that ignores LinkedIn's aesthetic looks off-platform. Match the medium.

### 2. Mobile preview always
LinkedIn/Twitter/X headers crop differently on mobile. Test mobile crop BEFORE finalizing. The center 60% must carry the message.

### 3. Profile-photo overlap awareness
LinkedIn personal headers, Twitter headers, Facebook covers all overlap with the profile photo in lower-left. Design around it; don't put critical content there.

### 4. Text legibility
- Headline at 48-72px minimum on a 1500-wide banner
- Strong contrast between text and background (test against white-text-on-photo overlays especially)
- Readable on a phone screen at thumb-distance

### 5. One message
Banners are not landing pages. One message. One CTA (if any). Clutter = ignored.

### 6. Brand consistency
Use brand colors, fonts, and imagery patterns. Random one-off banners weaken the brand.

## Output structure

For every banner request:

1. **Recommended style** with 2-3 alternatives (and why this style for this context)
2. **Specifications** — exact dimensions, file format, resolution (300 DPI for print, 72 DPI for screen)
3. **Composition layout** — where text goes, where visual elements go, where logo goes
4. **Color spec** — primary, secondary, accent (with hex codes)
5. **Typography spec** — fonts used, weights, sizes
6. **Mobile preview check** — what it looks like cropped to mobile dimensions
7. **Platform compliance check** — meets the platform's text-overlay rules (some ad platforms reject if text is >20% of image area)
8. **Variant suggestions** — A/B test alternatives if multiple banner versions are needed

## Anti-patterns

- **Stock photo with overlaid text** — generic vendor signal
- **Wrong dimensions for the platform** — auto-crop ruins the design
- **Critical content in profile-photo overlap area** — gets covered
- **Text too small to read on mobile** — most consumption is mobile
- **Multiple competing CTAs** — pick one
- **Brand-inconsistent one-offs** — weakens brand recognition
- **Trendy aesthetics that age fast** — design for 12+ months of use
- **Ad platforms text-overlay limits violated** — Facebook/LinkedIn rules limit text to 20% of image area in many ad formats
- **No mobile crop test** — desktop perfect, mobile broken

## Output

Produces:
1. Style recommendation with alternatives
2. Detailed design spec (dimensions, layout, color, typography)
3. Mobile preview check
4. Platform compliance check
5. Variant suggestions for A/B testing
6. If implementation is in scope: HTML/CSS or SVG version; otherwise spec for designer

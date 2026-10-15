---
name: appshots-best-practices
description: >
  Research-backed best practices for designing App Store & Google Play screenshots.
  Copywriting, layout, typography, device frames, translation verification, and ASO tips.
---

# App Store Screenshot Best Practices

Research-backed design guidelines for creating professional, high-converting App Store and Google Play screenshots.

## Core Principle

**Screenshots are advertisements, not documentation.** Every screenshot sells one idea. If you're just showing UI, you're doing it wrong — you're selling a *feeling*, an *outcome*, or killing a *pain point*.

## The 7-Second Rule

Users decide whether to download within **7 seconds** and rarely scroll past the first 2–3 screenshots. Your first screenshots must instantly communicate value.

## Copywriting (Write Copy FIRST)

Get all headlines approved before building layouts. Bad copy ruins good design.

### The Iron Rules

1. **One idea per headline.** Never join two things with "and."
2. **Short, common words.** 1–2 syllables. No jargon unless domain-specific.
3. **3–5 words per line.** Must be readable at thumbnail size in the App Store.
4. **Max 2 lines total.** Text should occupy less than 20% of the image area.
5. **Line breaks are intentional.** Control where lines break with `\n`.

### Three Caption Approaches (pick one per slide)

| Type | What it does | Example |
|------|-------------|---------|
| **Paint a moment** | You picture yourself doing it | "Check your habits without opening the app." |
| **State an outcome** | What life looks like after | "A home for every habit you build." |
| **Kill a pain** | Name a problem and destroy it | "Never forget your daily streak." |

### What NEVER Works

- ❌ Feature lists as headlines: "Log items with tags, categories, and notes"
- ❌ Two ideas with "and": "Track X and never miss Y"
- ❌ Compound clauses: "Save and customize X for every Y you own"
- ❌ Vague aspirational: "Every item, tracked."
- ❌ Marketing buzzwords: "AI-powered tips" (unless it's actually AI)

### Copy Process

1. Write 3 options per slide using the three approaches above
2. **Arm's length test** — if you can't parse it in 1 second, it's too complex
3. Check: does each line have 3–5 words? If not, adjust line breaks

### CLI Implementation

```bash
# Benefits-focused, centered, short caption
appshots editor add-text \
  --text "Track Your Habits\nEffortlessly" \
  --font "Poppins" --size 90 \
  --color "#FFFFFF" \
  --y 80 --x 0 \
  --width 1290 --align center
```

## Screenshot Narrative Flow

### Slide Framework (Adapt to Your Slide Count)

| Position | Purpose | Notes |
|----------|---------|-------|
| **#1** | **Hero / Main Benefit** | App's #1 value prop. The ONLY one most people see. |
| **#2** | **Differentiator** | What makes you unique vs. competitors |
| **#3** | **Ecosystem** | Widgets, Watch, extensions (skip if N/A) |
| **#4–7** | **Core Features** | One feature per slide, most important first |
| **#8–9** | **Trust Signal** | Identity/craft — "Made for people who [X]" |
| **#10** | **Extras** | More features, "coming soon" pills |

### Layout Variety Rules

- **Never repeat** the same layout structure on consecutive slides
- **Include 1–2 contrast slides** (inverted background) for visual rhythm
- **Each slide sells ONE idea** — never two features on one slide
- **Vary phone position**: centered, left-aligned, right-aligned, two-phone, no-phone

## Screenshot Limits & Dimensions

### Apple App Store (2025)

| Device | Mandatory | Resolution | Max |
|--------|-----------|------------|-----|
| iPhone 6.9" | ✅ Required | 1320 × 2868 | 10 per locale |
| iPhone 6.7" | Auto-scaled | 1290 × 2796 | 10 |
| iPhone 6.5" | Auto-scaled | 1284 × 2778 | 10 |
| iPad 13" | ✅ Required | 2064 × 2752 | 10 |
| Mac | Optional | 2880 × 1800 | 10 |

> **2025 change:** Only 6.9" iPhone + 13" iPad are mandatory base sizes. Smaller sizes auto-scale.

### Google Play Store

| Requirement | Value |
|------------|-------|
| Min screenshots | 2 (4 recommended) |
| Max screenshots | 8 |
| Format | JPEG or 24-bit PNG (no alpha) |
| Max file size | 8 MB |
| Aspect ratio | Cannot exceed 2:1 |
| Recommended phone | 1080 × 1920 (9:16) |

> **Google Play note:** Google discourages device frames and excessive promotional text.

### In-App Limits

The app supports a maximum of **10 design slots** per multi-screenshot set.

## Typography Rules

### Size Ratios (Resolution-Independent)

Size text relative to the canvas width (W) for consistent scaling across resolutions:

| Element | Size Formula | Weight | Example (W=1290) |
|---------|-------------|--------|-------------------|
| Category label | W × 0.028 | 600 (semi) | ~36px |
| Headline | W × 0.07–0.08 | 700 (bold) | ~90–103px |
| Hero headline | W × 0.09–0.10 | 700 (bold) | ~116–129px |

### Font Recommendations

| Category | Fonts | Use Case |
|----------|-------|----------|
| Modern sans-serif | Poppins, Inter, Outfit, Montserrat | Clean, universal |
| Bold display | Raleway, Oswald, Bebas Neue | Strong headlines |
| CJK Japanese | Noto Sans JP, M PLUS 1p | Japanese locales |
| CJK Korean | Noto Sans KR, Gothic A1 | Korean locales |
| CJK Chinese | Noto Sans SC/TC | Chinese locales |
| Arabic | Noto Sans Arabic, Cairo | Arabic locales |

## Device Frame & Phone Placement

### Frame Best Practices

- ✅ **App Store:** Use device frames — they add context and trust
- ⚠️ **Google Play:** Avoid device frames (Google discourages them)
- Use the **latest device model** for a modern look
- Keep **consistent frame** across all screenshots in a set

### Phone Position Patterns

Vary these across slides — **never use the same layout twice in a row**:

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Centered** | Phone centered, text above | Hero, single-feature slides |
| **Left-aligned** | Phone on left, text right or above | Feature detail |
| **Right-aligned** | Phone on right, text left or above | Alternate with left |
| **Two phones** | Back phone dimmed + front phone prominent | Before/after, comparison |
| **No phone** | Just text + icons/pills | "More features" slide, trust signal |

### 3D Rotation (Subtle!)

Values are in **radians**, not degrees:

| Effect | Values | Result |
|--------|--------|--------|
| Flat | `0, 0, 0` | Straight-on |
| Subtle tilt | `0.03, -0.02, 0.01` | Slight depth |
| Medium tilt | `0.05, -0.04, 0.02` | Noticeable |

> ⚠️ `3.0 radians ≈ 172°` = nearly upside down. Use `0.03–0.05` for subtle effects.

```bash
appshots editor set-rotation --x 0.03 --y -0.02 --z 0.01
```

### Screenshot Position

Push down to make room for text:

```bash
# y = 250–350 depending on text length
appshots editor set-image-position --x 0 --y 280
```

## Background & Color Design

### Color Psychology

| Style | Hex Examples | Effect | Best For |
|-------|-------------|--------|----------|
| Dark | `#0A0A1A`, `#0D1117` | Premium, modern | Most apps (2025 trend) |
| Deep blue | `#0F172A`, `#1E293B` | Trust, professional | Finance, productivity |
| Vibrant | `#7C3AED`, `#EC4899` | Energy, playful | Social, games |
| White/light | `#FFFFFF`, `#F8FAFC` | Clean, minimal | Business, health |

### Visual Rhythm with Backgrounds

- Use **dark backgrounds** for most slides (converts better)
- Include **1–2 contrast slides** with inverted/lighter backgrounds
- Create variety but maintain **cohesion** (same color family)

### 2025 Design Trends

- **Dark mode dominance** — white text on dark backgrounds
- **Glassmorphism 2.0** — translucent layers with vibrant underlays
- **Bold typography** — fonts as branding, not just information
- **Panoramic/continuous** — backgrounds that flow across screenshots
- **Minimalist + bold** — clean with one strong accent

## Translation & Localization

Localized screenshots can increase downloads by **up to 4×** (Apple's data).

### Text Expansion by Language

| Language | Expansion | Fix |
|----------|----------|-----|
| **German** | **+30-40%** | `--font-size 72` (reduce ~20%) |
| **Finnish** | **+30-40%** | `--font-size 70` |
| **French** | +15-25% | Minor font reduction |
| **Spanish** | +15-20% | Watch line breaks |
| **Japanese** | Same/shorter | Use `Noto Sans JP` |
| **Korean** | Same/shorter | Use `Noto Sans KR` |
| **Chinese** | -10-30% shorter | Use `Noto Sans SC` |
| **Arabic** | Varies | RTL — may need position flip |

### Post-Translation Verification

**Always verify every locale visually. This is the most critical step.**

```bash
# Check worst offenders first
appshots translate preview --locale de    # German (longest)
appshots translate preview --locale ja    # CJK font check

# Fix issues
appshots translate override-overlay --locale de --overlay-id <id> --font-size 72
appshots translate override-overlay --locale ja --overlay-id <id> --font "Noto Sans JP"

# Clear and save
appshots translate preview --locale none
appshots multi save-design --name "My Screenshots" --override
```

## Pre-Export Quality Checklist

- [ ] **Arm's length test** — every caption readable in 1 second?
- [ ] **One idea per slide** — no "and" joining two features?
- [ ] **3–5 words per line**, benefits-focused?
- [ ] **Layout varies** across slides (no two consecutive same layout)?
- [ ] **1–2 contrast slides** for visual rhythm?
- [ ] **Consistent styling** (padding, radius, frame, font)?
- [ ] **Dark background** with high-contrast text?
- [ ] **All 10 slots used** (maximize Store real estate)?
- [ ] **All locales verified** — especially German, French, CJK?
- [ ] **No text overflow** in any locale?
- [ ] **Thumbnails look good** (readable at small size in search)?

## A/B Testing

Apple's **Product Page Optimization** lets you test up to 3 screenshot sets simultaneously. Test:
- Different hero screenshots (#1)
- Dark vs. light backgrounds
- Different caption approaches (paint a moment vs. kill a pain)
- Feature ordering

Track conversion rate changes to validate design decisions.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| All slides look the same | Vary phone position and background |
| Copy is too complex | "One second at arm's length" test |
| Too cluttered | Simplify to phone + caption |
| Too empty | Add larger decorative elements |
| Headlines use "and" | Split into two slides |
| Plain backgrounds | Use gradients — even subtle ones add depth |
| No visual contrast | Mix light and dark backgrounds |
| Feature lists as copy | Rewrite as benefits or outcomes |

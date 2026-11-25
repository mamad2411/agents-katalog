---
name: looks-expensive
version: 1.0.0
description: |
  Full-stack design methodology that makes any website look like a $150k agency build.
  Nine gated phases: positioning, research, design contract, screen spec, build,
  subtraction, audit, hardening, handoff. Includes illustration system, animation
  tiers, 12 hero patterns, 16 section layouts, UX writing guide, icon system, and
  73 anti-pattern rules, bento grid patterns, CSS mockup library, real photography (Unsplash/Picsum URLs), non-card layout patterns, plus navigation, footer, dark-mode, product-UI, WebGL/3D, and editorial-typography systems. One skill, zero external dependencies.
  Trigger on: "design this", "make this look expensive", "looks expensive",
  "full design pass", "design from scratch", "premium design", "redesign this".
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - WebSearch
  - WebFetch
  - Agent
triggers:
  - looks expensive
  - design this
  - full design pass
  - design from scratch
  - premium design
  - make this look expensive
  - redesign this
---

# Looks Expensive

## The Anti-Template Mandate

Designers identify AI-generated pages at a glance through a small set of tells. This skill exists to kill them:

1. **Excessive bullet points.** Bullets are the lazy answer. Real editorial uses prose, ledgers, definition lists, tables. Max 5 bullets total per page. See reference/ux-writing.md.
2. **Eyebrow-pill subheadings on every section.** The uppercase pill above every heading is the most common AI tell of 2025. Max 1 per page. Ideally zero.
3. **Same card chrome everywhere.** Every section wrapped in `border-radius: 16px; border: 1px solid rgba(0,0,0,0.06)` is the visual signature of AI. Max 2 sections using the default card pattern. Other sections use ledgers, rules, tables, prose, or full-bleed photography. See reference/non-card-patterns.md.
4. **Generic 3-tier pricing tables.** Free/Pro/Enterprise as three identical card-columns. Use a real HTML table or inline pricing instead.
5. **Generic 4-column stat strip with counters.** Replace with an inline-stat narrative or a single hero stat. Counter animations are NOT mandatory — they're often a tell.
6. **Lack of imagery.** A hospitality/food/fashion/real estate/services brand without a real `<img>` tag where a hero photo belongs is the loudest AI tell on the page. Use Picsum or Unsplash URLs per reference/imagery.md.
7. **Identical container chrome across the entire page.** Variance IS the design. If 6 of 7 sections use the same container pattern, redesign.
8. **Meta-template fingerprint.** The 9-phase workflow itself can become a tell if every output's DESIGN.md uses the same section headers, every type scale uses the same H1 range, every palette uses literal #111/#fff. The PHASES are gated; the OUTPUT FORMAT inside each phase is flexible. Vary DESIGN.md per project: a hospitality brief leads with photography and scene; a dev tool brief leads with type, color, and motion; a luxury brand brief leads with the scene sentence. Document the scale, palette, and rhythm DERIVED from THIS brand — not copied from the last one.

Before every output, audit the page against ALL eight. The skill's job is not to apply a template — it's to make decisions per brief and avoid the patterns above.

## The Aesthetic North Star

The target aesthetic depends on the brief. This skill explicitly DOES NOT default to Linear/Vercel/Stripe for every product.

- For SaaS, dev tools, fintech, infrastructure: Linear, Vercel, Stripe, Cursor, Mercury, Eleven Labs.
- For hospitality, hotels, restaurants: Aman Resorts, The Modern, Single Thread Farms. Real photography, generous whitespace, often serif headings.
- For luxury goods, fashion, food brands: Aesop, Glossier, Hodinkee, Snow Peak. Real product photography, editorial typography, warm or neutral palette per the brand.
- For agencies and portfolios: Pentagram, Studio Sutherl&, Mast (the agency, not the chocolate). Less content, larger type, real work shown via photos and case study layouts.
- For services (coaching, therapy, dental, legal): O&O Studio, Wax Atelier (the studio sites). Calm, confident, sometimes a real photograph of the practitioner or workspace.

If the brief is for a hotel and you've built something that looks like Vercel, you went wrong. North Star follows the brief.

What every premium design shares regardless of category:
- One typeface family carrying the headlines (sometimes paired with a quiet serif body, never with three families)
- Color palette of 3-5 deliberate tokens, not random hex values
- Generous whitespace, breath between sections
- Real content (photos, mockups, copy) — not gradient blobs as placeholders
- Restraint with motion — animation serves the content, doesn't decorate it
- Variance per section — no two sections containerized the same way

---

Nine phases. Gated. Each phase's output gets user approval before the next begins.

---

## Phase 1: Product Positioning

Before any visual work, establish the taste filter.

### Interview

Ask these questions. Do not proceed until answered:

1. **What is this product?** One sentence.
2. **Who is it for?** Audience, technical level, context of use.
3. **Brand or Product register?**
   - Brand: design IS the product (marketing, portfolios, agency). Distinctiveness, typographic risk.
   - Product: design SERVES the product (dashboards, SaaS, tools). Earned familiarity.
4. **The memorable thing?** One sentence that filters every decision.
5. **What are you NOT?** 3-4 anti-references.
6. **2-3 products whose quality you want to match.**
7. **Emotional temperature?**
   - Cool/Technical: precision, security, dev tools, fintech (cool whites, slate, blue-black)
   - Warm/Earthy: food, wellness, hospitality, agriculture (cream is allowed HERE ONLY)
   - Neutral/Clean: general SaaS, productivity, B2B, agencies, consulting, real estate (pure white, true gray, true black)
   - Bold/High-Contrast: consumer apps, creative tools, marketplaces (pure black + white + one saturated accent — the saturated accent lives on links, icons, and tinted blocks; primary button fills use `--accent-ink` per Color System step 5 when text is near-white)
   - Vibrant/Playful: social, education, community (bright accents on white)
8. **Constraints?** Timeline, team size, existing code.

### Output

Write the positioning brief. Present. STOP. Wait for approval.

---

## Phase 2: Competitive Research

Study the named products plus 7-10 more.

### Methodology

1. Web search each reference: "[product] design", "[product] website". Extract fonts, colors, spacing, borders, shadows, motion timing.
2. Search 3-5 angles per product.
3. Cross-pollination: search 2-3 categories OUTSIDE the obvious one.
4. Extract "expensive vs generic" tells for this surface type.
5. Build Steal/Avoid lists with evidence.

### Output

Research brief: TL;DR, Steal list, Avoid list, cross-pollination findings, ASCII wireframes.
Present. STOP. Wait for approval.

---

## Phase 3: Design Contract (DESIGN.md)

Load reference files: `reference/ux-writing.md`, `reference/border-radius.md`, `reference/imagery.md`. If the scene sentence forces a dark theme, also load `reference/dark-mode.md`. If serif is earned AND the product is a genuine editorial/publishing/long-read product, also load `reference/typography-editorial.md`.

### Product Context
From Phase 1.

### Aesthetic Direction
Direction label, decoration level, mood sentence, anti-references.

### Scene Sentence

Before choosing theme (dark vs light), color palette, or typography register, write ONE sentence describing the physical scene of use:
- Who is using this product?
- Where, in what ambient light?
- In what mood / what's happening around them?

**Example weak:** "Observability dashboard."
**Example strong:** "An SRE glancing at incident severity on a 27-inch monitor at 2am in a dim home office, while their phone is buzzing with PagerDuty."

**Example weak:** "Luxury furniture brand."
**Example strong:** "A 38-year-old designer in their renovated SF studio, comparing the Foundry Table to an Aman catalog at the kitchen counter on a Sunday morning with coffee."

If the sentence doesn't FORCE a theme choice (dark vs light, warm vs cool, dense vs spacious), add detail until it does. DO NOT default to "dark for SaaS/dev tools, light for marketing, cream for food." Derive theme from the scene.

The scene sentence is the anchor for every subsequent decision: type register, color palette, density, animation tone, imagery treatment.

### Imagery Decision

For every brief, decide which imagery category the product falls into:

| Category | Examples | Treatment |
|----------|----------|-----------|
| **Photography mandatory** | Hospitality, food/bev, fashion, real estate, **physical goods (furniture, craft, retail, jewelry, hardware)**, services with human element, agencies, lifestyle, travel, **heritage/craft brands** | Real `<img>` tags with Picsum or Unsplash URLs in hero AND at least one in-page section. No CSS gradient stand-ins. No styled rounded-rectangle "placeholder" boxes. |
| **Photography preferred** | Construction, fitness, education, B2B with field operations | At least one real image somewhere on the page. Hero may use mockup OR photo. |
| **Photography optional** | SaaS, dev tools, analytics, infrastructure, fintech | Use CSS mockups per reference/css-mockups.md. Add a single editorial photo if the brand has a human/team angle. |
| **Photography unsuitable** | Pure data products, code-only APIs, abstract infrastructure | Lean into typography, custom SVG instruments, and bespoke diagrams. No imagery is fine — but no gradient blobs either. |

Write the imagery decision into DESIGN.md explicitly. List the sections that will use photography and what each photo should show. See reference/imagery.md for URL format and sizing.

### Font System

**The default is ONE typeface family carrying the headlines and body.** Hierarchy comes from weight and size, not from mixing families. Most software, services, and agencies use one sans.

**Serif headings are allowed when:**
1. The product is food, beverage, luxury goods, hospitality, fashion, real estate, editorial, or a craft/heritage brand AND
2. The emotional temperature is Warm/Earthy OR the brand has explicit editorial positioning

When earned, use a modern serif (Fraunces, Cormorant, Playfair Display, Lora, Libre Baskerville, Spectral) for H1/H2 paired with a sans body. NOT serif body — that reads as legacy magazine, not premium.

**Serif body is permitted (rare) when:**
1. The product is editorial, a publication, a thought-leader's personal site, OR a coaching/advisory service where the brand is explicitly literary AND
2. The user specifically wants that editorial register

In all other cases (agencies, clinics, SaaS, marketplaces, real estate, services): all-sans.

**INTER IS BANNED AS THE DEFAULT.** Inter appeared in 8 of 11 test outputs. It is a fine font but using it on every project makes every output identical. You MUST select a different sans-serif for each project. Before choosing, list 5 candidates and pick the best match.

**Font candidates (all sans-serif, search for more):**
- Space Grotesk, Outfit, DM Sans, Instrument Sans, Geist, IBM Plex Sans
- Satoshi, General Sans, Albert Sans, Sora, Plus Jakarta Sans, Switzer
- Cabinet Grotesk, Manrope, Archivo, Bricolage Grotesque
- Rubik, Nunito Sans, Source Sans 3, Libre Franklin

**Selection process:**
1. List 5 sans-serif candidates that match the product's personality
2. Eliminate any font you've used recently
3. Pick the one that best matches while being different from your default
4. One family. Hierarchy through weight (400/500/600/700) and size. Not through mixing families.

**Rules:**
- ONE sans-serif family. Not two. Not serif + sans.
- NO Inter unless explicitly justified in one sentence.
- NO `.serif` class. NO `.h-display` with a different font family.
- NO italics. No `<em>`, `<i>`, `.italic`, `font-style: italic`. Ever.
- **Monospace is a DATA ACCENT, never body/headline type.** Banned for body, headlines, and ANY uppercase letter-spaced label, always, in every category. PERMITTED — small (≤14px) — for discrete technical data atoms in tech registers ONLY (devtools, fintech, hardware, infra): IDs/hashes/keys, version/commit/model/build tags, timestamps/durations, stat UNITS (the unit, not the prose), tabular figures that must align in a column, and code/`<code>`/`<pre>`. Guardrails (any miss → remove the mono): category-scoped (banned on hospitality/food/fashion/services/agencies/luxury/editorial); ≤14px only; mono is the DATUM not decoration (a mono eyebrow is the new pill-eyebrow tell); one mono family max; set with positive tracking + tabular/lining figures (`font-feature-settings: "tnum" 1, "lnum" 1`). Mono accent families (pick ONE, only when the carve-out applies — keep separate from the sans candidates): Geist Mono, JetBrains Mono, Berkeley Mono, IBM Plex Mono, Commit Mono.

**Type scale — DESIGN PER PROJECT.** Do NOT copy a fixed 9-step ladder to every project. Real designers shape the scale to the register.

For each project, declare in DESIGN.md:
1. **Base body size:** 15px (dense product UIs), 17px (standard marketing), 19px (editorial/luxury). Pick consciously.
2. **Scale ratio:** 1.2 (compact / product UI), 1.25 (standard), 1.333 (perfect-fourth, marketing), 1.5 (editorial), 1.618 (luxury / dramatic).
3. **Generate** the ladder from base × ratio (e.g., body 17 × 1.333^4 ≈ 56px H1).

H1 ranges by category (illustrative — derive your own):
- Dense product UI: 28-36px
- Standard SaaS marketing: 40-56px
- Hospitality / luxury: 56-88px
- Editorial / agency / dramatic: 72-120px

Document the chosen base and ratio in DESIGN.md so the next project starts fresh. Do NOT default to H1: 40-72px on every project — that's the fingerprint.

Weight is a separate axis: 400 body, 500 mid-emphasis labels and h5/h6, 600 h2/h3, 700 h1. Don't use both 500 and 600 unless the weights are noticeably different in the chosen font.

**Typography craft layer (the invisible-typographer wins).** Defects an AI default leaves in and a real typographer removes. Progressive enhancement with no-op fallbacks — apply everywhere:
- `text-wrap: balance` on every heading, eyebrow, and blockquote (kills ragged orphan lines); `text-wrap: pretty` on prose ONLY (kills widows; it has a layout cost, so scope it to body copy).
- `font-variant-numeric: tabular-nums` is GLOBAL for any aligned numbers (stat strip, ledger row, pricing table, dashboard column). Misaligned digits are the same crime as zero-padded step numbers.
- Ligatures stay default-on (`liga`/`calt`). Oldstyle figures (`onum`) only in the serif-prose case already gated (Warm/Earthy food/luxury/hospitality/editorial); lining figures everywhere else.
- `font-optical-sizing: auto` ONLY when the chosen face actually carries an `opsz` axis (claiming it otherwise is a lie in DESIGN.md).
- HARD-BAN as the next tell: no animated/scroll-linked/hover variable-axis weight runs; no swashes/discretionary ligatures/decorative `ssXX`/decorative fractions (`frac` only for real fractional data); keep the named-weight model (400/500/600/700) — no `wght 540` default reflex.

Labels can be uppercase but use sparingly — see Eyebrow Discipline in reference/ux-writing.md. Max 1 per page, ideally zero.

### Color System

**Derive neutrals from the brand hue.** Do NOT default to the same `#111111` ink and `#ffffff` paper on every project. Real designs tint neutrals slightly toward the brand color so the page feels cohesive.

Use OKLCH:
1. Pick the brand accent first (hue H, chroma 0.10-0.20, lightness 0.55-0.70 for a saturated accent that reads as a color). This base `--accent` is for LINKS, ICONS, ACCENT STROKES, and TINTED BACKGROUNDS — NOT directly for primary button fills with white text (see step 5).
2. Derive paper from the brand hue: `oklch(0.97-0.99 0.005-0.015 H)` — a 1-2% tint toward the brand. Slightly warmer for warm hues, cooler for cool hues.
3. Derive ink from the brand hue: `oklch(0.13-0.18 0.005-0.020 H)` — near-black tinted toward brand.
4. Generate secondary/tertiary ink at lower opacity OR at higher L: `oklch(0.45 0.010 H)` (secondary), `oklch(0.65 0.010 H)` (tertiary).
5. **Derive `--accent-ink` for button fills with white text (REQUIRED if any primary button uses near-white text on accent).** White-on-accent at L=0.55-0.70 with brand chroma lands at ~3.9-4.4:1 — FAILS WCAG AA. Pick `--accent-ink: oklch(L 0.10-0.18 H)` with L in the range **0.42-0.48** (safe AA range — near-white text on L=0.48 gives ≥4.6:1, with headroom for the hover-must-darken rule). Do NOT push L above 0.48 — at L=0.50 the rest-state is on the AA edge and the hover-must-be-darker rule leaves no room. Keep the SAME hue H as `--accent`. Use `--accent-ink` ONLY for `background` on primary buttons; keep `--accent` for links, icons, and tints. Alternative path: keep the bright `--accent` on the button background and switch the BUTTON TEXT to the dark page background — dark-on-bright-accent passes 5:1+ and preserves the vivid color (good for dark-themed sites where a darkened button reads as muddy).
6. **Derive `--accent-hover` at L EQUAL or LOWER than the rest-state fill.** If your button rest-state is `--accent-ink` at L=0.46, `--accent-hover` is L≤0.42, not L=0.52. A hover state LIGHTER than rest REDUCES white-text contrast on hover — invisible until the user mouses over the button. This rule applies whether the button rest-fill is `--accent` or `--accent-ink`.

**Banned:** literal `#000000`, literal `#ffffff`, and copying the same hex codes across projects. If your last project used `#111111` ink and `#f8f9fa` paper, this project must use different values derived from THIS brand hue.

**Cream is restricted.** Cream (paper with significant warm chroma — OKLCH chroma > 0.025, hue 60-90) is ONLY for warm-earthy brands: food, beverage, hospitality, wellness, agriculture, craft/heritage furniture. Everything else uses a near-white paper with minimal chroma (< 0.015) tinted toward the brand hue.

**Brown-tinted ink is restricted.** Same categories as cream. Everything else uses near-black tinted slightly toward the brand hue.

**Temperature table (starting thoughts, not prescriptions):**

| Temperature | Hue range | Paper L / C | Ink L / C |
|-------------|-----------|-------------|-----------|
| Cool | 200-280 (blue/teal/violet) | 0.97 / 0.005 | 0.15 / 0.010 |
| Warm/Earthy | 30-90 (amber/orange/olive) | 0.96 / 0.020 | 0.18 / 0.025 |
| Neutral | any | 0.98 / 0.003 | 0.14 / 0.005 |
| Bold | any | 0.99 / 0.002 | 0.12 / 0.005 |

Numbers above are STARTING THOUGHTS. The point is to derive your own values from your brand hue — never copy the table verbatim.

**Brand accent is mandatory.** Every product has a primary color. It must:
- Live on links, icons, hover states, accent strokes, and tinted section backgrounds (at 4-8% opacity) — the base `--accent` at L=0.55-0.70 is correct here.
- Drive the primary button fill, but THROUGH `--accent-ink` (a darker derivation at L≤0.48), not directly. White-on-accent at the base L FAILS WCAG AA — see step 5 of the OKLCH derivation above.
- Be visible and intentional, not buried in a hover state.

Define in DESIGN.md (each is its own token, derived from the same hue H):
- `--accent` — base, L=0.55-0.70, chroma 0.10-0.20 — links, icons, accent strokes, tints
- `--accent-ink` — L=0.42-0.48, same hue — PRIMARY BUTTON FILLS and other accent-filled surfaces with near-white text (badges, recommended-plan stripes, active tabs, banners, photo callouts). **Background-only token. NEVER used as a foreground.** If you find yourself typing `color: var(--accent-ink)`, `fill: var(--accent-ink)`, `stroke: var(--accent-ink)`, or `border-color: var(--accent-ink)` — you want `color: var(--text)` or `color: var(--accent)` instead. Audit-pass grep: all four of those must return zero matches.
- `--accent-hover` — L equal-or-lower than the rest fill (whether `--accent` or `--accent-ink`); NEVER lighter
- `--accent-pressed` — slightly darker than `--accent-hover`
- `--accent-on-dark` — higher L, lower chroma, for use on near-black surfaces (dark-themed sites)
- `--accent-focus-ring` — the focus ring color used on accent-filled surfaces. When the button background is `--accent-ink`, the ring must be PAPER or near-paper (a same-hue accent ring against `--accent-ink` is ~1.3-1.6:1 and FAILS the 3:1 focus-indicator rule). When the button background is `--accent`, the ring can be the dark page ink. Always measured against the FILL, not against the page background.
- **Surface tiers** (paper, paper-2 slightly darker for section alternation, paper-3 for tertiary, dark-panel for inverted sections)
- **Ink tiers** (primary, secondary at lower L, tertiary at higher L)
- **Hairlines** (paper-tinted alpha at 0.06/0.10/0.16)
- **Semantic** (success/warning/error/info — also OKLCH-derived if possible)

**Hard rules:**
- No one-sided colorful strokes
- Borders use hairline opacity or inset shadow
- Elevation through lightness, not heavy shadow
- No gradients unless user asks
- Accent color must be VISIBLE
- **ACCENT VISIBILITY:** The accent color MUST be visually distinguishable from the ink color at arm's length. Slate (#334155), gray (#475569, #64748B), dark navy (#1B2838), and near-black (#171717) are NOT accent colors — they're ink variants. If the accent hex starts with #1-#5 and the ink is #0a0a0a, the difference is too subtle. Pick a real color with a different hue.

**If the scene forces a dark theme,** load `reference/dark-mode.md` and engineer it as a separate system, not a palette flip: elevation INVERTS (higher surfaces step LIGHTER, never via shadow), hairlines become low-alpha WHITE, the accent's chroma DROPS and lightness RISES so it survives near-black (reuse the on-dark accent variant above), and tokens resolve per theme via `light-dark()` or `[data-theme]`. AA still mandatory; one accent only; no glowing accents. The "dark sites need a light section" contrast rule still applies.

### Color exceptions (two bounded escapes from the single-accent rule)

- **Tonal monochrome (luxury / editorial / hospitality only).** The page is tints of ONE hue with deliberately NO contrasting accent — photography and the type scale carry all contrast (Aesop, Soho House). Permitted ONLY when Phase 3 classified the product warm-earthy-luxury / editorial / hospitality AND photography is mandatory and present. Forbidden on SaaS/devtools/fintech/services (there, a buried near-ink "accent" is the gray-accent trap). Still require surface-tier rhythm. Frame it in DESIGN.md as "accent satisfied by photographic contrast," never "no accent."
- **Per-variant re-theme on SKU select (multi-SKU DTC food/bev/consumer goods with 3+ flavors only).** A small token map swapped on selection with a 200-400ms cross-fade (Olipop). EACH variant theme must independently pass ACCENT VISIBILITY + WCAG AA; cap at ONE re-theming module (never whole-site chrome); disable the fade under `prefers-reduced-motion`.
- **Maximalist color-blocking is NOT an exception.** Do not add a maximalism mode. See the one-sentence bound on reference/section-layouts.md Pattern 14.

### Spacing
**Design per project.** Do NOT copy the same 12-step ladder to every project.

Declare in DESIGN.md:
1. **Base unit:** 4px or 8px
2. **Rhythm character:** Compact (product UIs, dense info), Standard (most marketing), Spacious (editorial, luxury, hospitality).
3. **Generate the scale** from base × Fibonacci-ish or base × 2x progression. Compact products stop at ~64px between sections; Spacious products extend to 240px.

Example scales (illustrative — derive your own):
- Compact: 4/8/12/16/24/32/48/64 (max section padding 64px)
- Standard: 4/8/16/24/40/64/96/128 (max section padding 96-120px)
- Spacious: 8/16/32/56/88/144/200/240 (max section padding 160-240px)

Document the chosen scale in DESIGN.md so the next project starts fresh.

### Layout
- Max content width (1280-1440px)
- Grid: columns, gutters, responsive
- Text measure: 65-75ch max

### Border Radius
Load `reference/border-radius.md`. Use the 4-32 system:
```
xs:   4px   (inputs, small pills)
sm:   8px   (cards, buttons)
md:   12px  (modals, larger cards)
lg:   16px  (feature cards, hero elements)
xl:   24px  (hero cards, major containers)
2xl:  32px  (full-bleed containers)
pill: 9999px (pill buttons, tags)
```

### Icon System
Outlined icons only. Stroke weight 0.8-1px. Nothing heavier. Consistent sizing (16/20/24px tiers). One icon family per project.

### Motion
- Custom cubic-bezier only. Never `linear` or default `ease-in-out`.
- Hover: 150-200ms. Reveal: 400-600ms. Entrance: 600-800ms.
- GPU-safe: transform and opacity only.
- `prefers-reduced-motion` respected always.

### Section Rhythm
Load `reference/section-layouts.md`. Define per-section:
- Background treatment (white, off-white, tinted, dark)
- Layout pattern (from 15 options, never same pattern twice in a row)
- Density (spacious vs compact)

Rules:
- Never 2+ consecutive sections with same background
- At least one dark-inverted section per page
- At least 3 different layout patterns per page

### UX Writing
Load `reference/ux-writing.md`. All copy follows:
- Headline: 6-10 words / 60 chars max
- Subhead: 15-25 words / 120 chars max
- CTA: 2-5 words / 30 chars max
- Feature description: one sentence / 15-20 words max
- No banned words
- No section numbers ("01.", "Section 1"). Labels only when they add navigation context.
- No dates unless content is date-specific.

### Decisions Log
```
| Date | Decision | Rationale |
|------|----------|-----------|
```

### Output
Write complete DESIGN.md. Present. STOP. Wait for approval.

---

## Phase 4: Screen Specification

Load reference files: `reference/hero-patterns.md`, `reference/section-layouts.md`, `reference/illustrations.md`, `reference/bento-grids.md`, `reference/css-mockups.md`, `reference/imagery.md`, `reference/non-card-patterns.md`, `reference/navigation.md`, `reference/modern-css.md`. Load `reference/product-ui.md` if the brief is an app/dashboard/docs, commerce/DTC, or a SaaS/devtools/fintech product being sold; `reference/webgl-3d.md` if a WebGL/3D hero is on the table; `reference/typography-editorial.md` if serif is earned for an editorial/publishing product.

### Per-Screen Spec

**Start from the brief, not from sections.** Before listing sections, write one paragraph (3-5 sentences) describing what THIS specific page needs to communicate and in what order, derived from the brand brief alone. Don't start by enumerating standard sections (hero, features, stats, testimonial, CTA). Sections come from what the brief needs, not from a default list. If your section list would fit any product in the same category, you started from the template — restart from the brief.

1. **Route and purpose.**

2. **Hero pattern selection.** From 12 patterns in reference/hero-patterns.md. Note whether the hero uses photography, CSS mockup, or typography-only.

3. **Imagery audit gate.** Until every `<img>` tag the page will include is listed below with a CONCRETE Picsum/Unsplash URL (not "TBD"), dimensions, and descriptive alt text, the screen spec is INCOMPLETE and Phase 4 cannot proceed to step 4.

   Required format:
   ```
   Imagery URLs:
   - Hero: <img src="https://picsum.photos/seed/[descriptive-seed]/2400/1200" alt="[what the brand's real photo should show]" width="2400" height="1200">
   - [Section name]: <img src="https://picsum.photos/seed/[descriptive-seed]/1600/900" alt="..." ...>
   ```

   Minimums by Phase 3 category:
   - Photography mandatory: hero + 2+ in-page = 3+ images minimum
   - Photography preferred: hero or 1 in-page = 1+ image minimum
   - Photography optional: 0+ (may add one editorial photo if brand has human angle)
   - Photography unsuitable: 0 (typography/SVG only)

   Unacceptable: "TBD", "hero image placeholder", "visual TBD", omitting this step. If you cannot write concrete URLs now, STOP and re-read reference/imagery.md.

4. **Full-page section map.** Every section: name, layout pattern, background, content summary, containment type (card, ledger, table, prose, full-bleed photo, etc.), visual type (photo, mockup, typography). ENTIRE page mapped before implementation.

5. **Containment variance plan.** Across all sections, list the containment pattern per section as a table. At least 3 DIFFERENT patterns required. The default card pattern (any rounded rectangle with visible border or shadow, regardless of pixel values) may appear at most 2 times. Other sections use ledgers (reference/non-card-patterns.md Pattern 1), definition lists (Pattern 2), editorial rules (Pattern 3), tables (Pattern 7), inline pricing (Pattern 8), or full-bleed photography. If this table shows the same containment in more than 2 sections, the spec is INCOMPLETE — fix before proceeding. Footer: state the footer type (fat-sitemap / typographic / minimal-utility) chosen from category per reference/non-card-patterns.md Footer Architecture — name the real IA behind any sitemap columns. Footer link-list `<li>`s are navigation and are exempt from the bullet budget; the footer is borderless and does not count against the 2-card budget.

5b. **Bullet budget.** Inventory every section that defaults to bulleted content (features, benefits, what's included, why us, process steps, pricing features). For EACH, name the alternative pattern from reference/non-card-patterns.md you will use INSTEAD (ledger, definition list, table, prose, numbered timeline). Compute the page bullet total: total `<li>` + faux-bullet divs must be ≤ 5 BEFORE implementation. List each remaining bullet and justify why it cannot be prose. If total > 5, the spec is INCOMPLETE.

5c. **Pricing pattern decision.** Declare: (a) how many distinct pricing plans this product has, (b) which pattern you will use. Defaults:
   - 1 plan → Pattern 8 inline pricing (a sentence of confident prose with the price as a number). NOT a single oversized "Most Popular" card.
   - 2-4 plans → Pattern 7 real HTML table with feature rows showing included/excluded per plan column. NOT 3 identical card-columns each containing 6-8 checkmark rows (those checkmarks are bullets and they blow your budget).
   - 5+ plans → Pattern 7 table is mandatory.

   If you chose 3-card pricing, justify why a table is wrong for this specific product. Default reflex is banned.

5d. **Stat section decision.** Declare: are there stats on this page? If yes, name the pattern. DEFAULTS (override only with documented reason):
   - 1 anchor stat → Pattern 6 single hero stat
   - 2-3 supporting stats → Pattern 5 inline-stat narrative (stats embedded in a prose sentence)
   - 4+ stats → may use a stat strip BUT counter animations are still NOT mandatory and only appropriate for analytics/monitoring/billing-dashboard products

   The generic 4-column counter strip with stagger-counter-up animations is BANNED as a default. If you chose it, justify why prose-integration (Pattern 5) is wrong for THIS brand.

5e. **Product-UI surface gate.** Default is NONE. If the brief is DTC/commerce, an app/dashboard/docs product, a SaaS/devtools/fintech product being sold, or a physical/hardware product, declare which (if any) `reference/product-ui.md` surface applies (live product UI, e-commerce PDP kit, commerce-conversion bar, command palette, trust surfaces, hardware callouts). These are opt-in, never auto-added, and count against the card/bullet/eyebrow budgets like any other section.

5f. **WebGL/3D decision gate.** Default is NONE. A WebGL/shader/3D element is permitted ONLY for a SaaS/devtools/fintech hero that passes the single-question test in `reference/webgl-3d.md` — never on services/hospitality/food/agency/editorial. If chosen, the spec MUST include the full fallback contract: poster `<img>` preloaded `fetchpriority="high"` (never the canvas as LCP), capability gate, lazy-init after first paint, `prefers-reduced-motion` freeze, mobile ships the poster. Animated shader gradients do NOT override the no-gradients rule or anti-pattern #14 — gated branded hero moment only.

6. **Illustration / visual plan.** For each section, decide: photography, CSS mockup, typography-driven, or custom SVG.
   - Photography for human/physical/lifestyle products — see reference/imagery.md
   - CSS mockup for software UI — see reference/css-mockups.md (NO browser chrome dots)
   - Typography-driven for services, agencies, editorial — see reference/non-card-patterns.md
   - Custom SVG instruments for technical hardware (frequency traces, schematics, region maps)
   - NEVER a gradient blob where any of the above should be

7. **ASCII wireframe** of complete page.

8. **Cognitive load check:** Nav 5 or fewer, forms 4 or fewer fields, 1 primary + max 2 secondary buttons. See reference/navigation.md for the engineered header (scroll-state condense) + mobile drawer spec.

9. **Interaction state inventory:** All 8 states for every interactive element.

10. **Responsive spec** at 320/640/768/1024/1280/1536.

11. **Animation plan.** Load `reference/animations.md`. Minimum 2 types, one must be domain-specific or typographic. Counter animations NOT mandatory.

### Output
Write the spec. Present. STOP. Wait for approval.

---

## Phase 5: Implementation

Load reference files: `reference/animations.md`, `reference/icon-system.md`, `reference/anti-patterns.md`, `reference/bento-grids.md`, `reference/css-mockups.md`, `reference/imagery.md`, `reference/non-card-patterns.md`, `reference/navigation.md`, `reference/modern-css.md`. Plus, when the brief calls for them (per the Phase 4 gates): `reference/dark-mode.md` (dark theme), `reference/product-ui.md` (app / commerce / sold-SaaS surfaces), `reference/webgl-3d.md` (WebGL/3D hero), `reference/typography-editorial.md` (earned-serif editorial).

### Build Rules

**Color must be visible.** Accent visible on links, hover states, icons, and at least one tinted section. Primary CTAs use `--accent-ink` (NOT base `--accent`) when the button text is near-white — see Color System step 5. The accent must be visually distinguishable from body text — no gray, slate, or near-black accents.

**Sections must look different.** Different background, layout, density, type scale, AND containment per section. At least 2 dimensions different between adjacent sections. See "Containment variance" below.

**Containment variance.** Across the whole page, use AT LEAST 3 DIFFERENT containment patterns. The default rounded-rectangle card (`border-radius: 16px; border: 1px solid rgba(0,0,0,0.06); padding: 32px`) may appear at most 2 times. Other sections use:
- Ledger rows (hairlines, no card chrome) — reference/non-card-patterns.md Pattern 1
- Definition lists (term + description) — Pattern 2
- Editorial rules (just typography between hr separators) — Pattern 3
- Real HTML tables — Pattern 7
- Inline pricing prose — Pattern 8
- Full-bleed photography with text overlay — reference/imagery.md
- Single hero stat or inline-stat narrative — Pattern 5/6

If 5+ sections of your page use the same containment, redesign. Variance IS the design.

**Photography is mandatory for the right categories.** If Phase 3 declared this product "Photography mandatory," the site MUST include real `<img>` tags. Hero image + at least one in-page image. URLs use Picsum (`https://picsum.photos/seed/[descriptive-seed]/W/H`) or Unsplash format. NEVER substitute CSS gradient rectangles for required photography. See reference/imagery.md.

**Illustrations must respect the medium.** Follow `reference/illustrations.md`. NEVER render physical products, landscapes, or realistic objects in SVG/CSS. Use photography for those. For software UI visuals, use CSS mockup patterns from `reference/css-mockups.md` — not empty gradient rectangles.

**Bento grids must be real, and used sparingly.** Bento was overused in early iterations of this skill. Use AT MOST ONE bento section per page. Follow `reference/bento-grids.md` — copy the CSS exactly. Large cards MUST span BOTH axes (`grid-column: span 2` AND `grid-row: span 2`). Use `grid-auto-rows: 1fr`, NEVER `grid-template-rows: auto auto`. Include THREE responsive breakpoints. Large bento cards MUST contain embedded visuals (real photography, CSS mockup, chart, or code block), not empty gradients.

**Animations require variety, not volume.** Minimum 2 different animation types. AT LEAST ONE must be domain-specific (pulsing dots for real-time data, waveform for audio, route drawing for logistics, hand-stitch for craft brands, etc.) OR typographic (text reveal, accent underline draw). Counter animations are NOT mandatory and are often a tell — only use them where the number IS the story. The same translateY(24px) fade-up on every element is a template fingerprint. Vary distances and timing per element type.

**Pricing is not always a 3-tier table.** Before defaulting to three pricing cards in a row, ask: does this product have three tiers, or does it have one plan with a clear price? Services and single-product brands often need inline pricing (reference/non-card-patterns.md Pattern 8). SaaS with real tiers often work better as a real HTML table (Pattern 7) than as three identical cards.

**Stats are not always 4 columns with counters.** Before defaulting to a 4-column stat strip, ask: is the stat the story, or is it a credibility footnote? For credibility, integrate into prose (Pattern 5). For one anchor stat, use the single hero stat pattern (Pattern 6). The generic 4-col counter strip is a SaaS marketing reflex — skip it unless the product is genuinely about measurable outcomes and the numbers ARE the headline.

**Bullets are restricted.** Maximum 5 total bullet points per page, across ALL sections. If you have more, restructure into ledgers, definition lists, paragraphs, or tables. Bullets are the lazy answer.

**Eyebrow pills are restricted.** Maximum 1 eyebrow pill per page. Ideally zero. The section heading does the work. The uppercase-pill-above-every-heading pattern is the loudest 2025 AI tell.

**No browser chrome.** No red/yellow/green dots on ANY element — code blocks, dashboards, mockups, or anything else. This is the #1 AI design tell. Use a thin accent line or subtle border instead.

**Mobile menu must work.** Every site must include a working hamburger toggle for the mobile nav, and the drawer needs body-scroll-lock, a focus trap, and Esc-to-close — not just a `display` toggle. Hidden nav links with no way to show them is a broken site. See reference/navigation.md for the engineered header + drawer.

**Product-UI surfaces are gated, not free.** Live product UI, e-commerce PDP kits, commerce-conversion bars, command palettes, trust surfaces, and hardware callouts ship ONLY when the Phase 4 gate (5e) selected them, and only per reference/product-ui.md. They obey every budget (cards, bullets, eyebrows) and every ban (no browser chrome, real states only, every shortcut badge backed by a working shortcut). A Cmd-K palette on a marketing site, or a one-image + native-dropdown PDP, is a tell.

**No editorial patterns as defaults.** Specifically:
- No `.serif` class unless serif was earned in Phase 3 (Warm/Earthy temperature + food/bev/luxury/hospitality)
- No uppercase letter-spaced eyebrows. Max 1 per page, ideally zero.
- No `.h-display` with a font different from body
- No warm CSS variable naming (`--paper`, `--night`, `--night-copy`). Use neutral names (`--bg`, `--bg-2`, `--text`, `--text-2`, `--accent`).
- No editorial pull quote styling unless the product is editorial

**No template skeleton.** Do not build every page as: centered hero → 3-card grid → 3-step process → stats → testimonial → CTA → footer. Rearrange, merge, or replace at least 2 sections with different patterns from `reference/section-layouts.md`. If the page follows this exact structure, go back and redesign.

**Dark sites need contrast.** If the site is dark-themed, include at least one light-background section (white or light gray). The difference between #0a0a0a, #111, and #1a1a1a is not visible enough to create section distinction. Engineer dark per reference/dark-mode.md: elevation inverts (lighter surfaces, not shadows), hairlines are white-alpha, the accent's chroma drops while it stays AA-legible.

**No zero-padded step numbers.** Use 1, 2, 3 for process steps. Never 01, 02, 03. Zero-padding is an AI design tell.

**Testimonials must not use banned names.** See `reference/ux-writing.md` for the banned name list. Generate names from the product's actual target audience demographic and geography. Never use gradient circles as avatars — use initials in a colored circle or omit the avatar.

### Pre-Output Checklist

**DISTINCTIVENESS CHECK (run FIRST, before any tell-avoidance check):**

Name 3 design decisions on this page that you would NOT make on the next brief in a different category. Examples of valid distinctiveness:
- A typographic scale derived specifically from THIS brand (base + ratio documented in DESIGN.md, not a copy of last project's scale)
- An OKLCH palette derived from THIS brand's hue, not a literal #111111/#ffffff pair
- A containment choice (ledger / table / full-bleed photo grid) you would NOT use for a different product
- An animation tied to this product's domain (waveform for audio, route line for logistics, hand-stitch for craft)
- A hero photo composition that wouldn't fit another brand

Write the 3 here:
1. ___
2. ___
3. ___

If your 3 decisions are all containment-counts and bullet-counts, you only avoided tells — you didn't design distinctly. Start over from the scene sentence in Phase 3.

---

Then the tell-avoidance checks:

Before presenting ANY screen:
- [ ] **SERIF CHECK:** Is there a `.serif` class or a second font family? If yes and serif wasn't earned in Phase 3, REMOVE IT. Use the single sans family for everything.
- [ ] **INTER CHECK:** Is the font Inter? If yes and it wasn't explicitly justified, CHANGE IT.
- [ ] **CREAM CHECK:** Is the background cream/warm-tinted (#f5f2ec, #f4f1ec, etc.)? If the product is NOT food/beverage/hospitality, CHANGE TO WHITE.
- [ ] **BROWN INK CHECK:** Is the ink warm brown (#1a1715, #1c1b18, etc.)? If the product is NOT food/beverage/hospitality, CHANGE TO TRUE BLACK.
- [ ] **ITALIC CHECK:** Grep for `<em>`, `<i>`, `.italic`, `font-style: italic`. If found, REMOVE.
- [ ] **MONO CHECK:** Grep `monospace`, `mono`, `<code>`, `<pre>`. Mono is allowed ONLY on enumerated data atoms (IDs, version/commit/model tags, timestamps, stat units, tabular figures, code) in devtools/fintech/hardware/infra registers, ≤14px. If mono appears on an EYEBROW, HEADING, BODY run, or any uppercase letter-spaced label → REMOVE. If the product is hospitality/food/fashion/services/luxury/editorial → REMOVE all non-code mono. More than ONE mono family → collapse to one.
- [ ] **CRAFT CHECK:** `text-wrap: balance` on headings/eyebrows/blockquotes? `text-wrap: pretty` on prose only? `tabular-nums` on every aligned figure (stats, pricing, ledgers, tables)? NO animated/scroll/hover variable-axis weight runs, NO swashes/dlig/decorative ssXX/decorative fractions? Weights named (400/500/600/700), not a `wght 540` default?
- [ ] **FONT-LOADING CHECK:** Subset variable `woff2` self-hosted, the one critical (headline) face preloaded, `font-display: swap`, and a metric-matched `size-adjust`/`ascent-override` fallback present? The distinctive-font mandate without this is a CLS liability.
- [ ] **COLOR-EXCEPTION CHECK:** If tonal monochrome is used → is the product luxury/editorial/hospitality AND is real `<img>` photography present carrying the contrast? (If not, it's gray-on-gray slop — add an accent or photography.) If per-variant re-theme is used → does EVERY variant pass ACCENT VISIBILITY + WCAG AA, confined to one module, with `prefers-reduced-motion` disabling the fade?
- [ ] **GRADIENT CHECK:** Grep for `gradient`. Remove unless user requested.
- [ ] **SECTION NUMBER CHECK:** Grep for "Section", "01.", "02.", "---". Remove.
- [ ] **BROWSER CHROME CHECK:** Grep for red/yellow/green dots, `.dot`, `#ef4444`/`#eab308`/`#22c55e` triplets. Remove ALL of them. No exceptions.
- [ ] **ILLUSTRATION QUALITY CHECK:** Review every SVG. If it looks amateur, remove and use typography or a CSS mockup from reference/css-mockups.md.
- [ ] Font: one sans family (or serif headings + sans body if Warm/Earthy food/luxury), hierarchy through weight + size
- [ ] Color tokens used everywhere
- [ ] **ACCENT CHECK:** Is the accent visually distinct from the ink? If both are dark (#1-#5 hex range), pick a real color with a different hue.
- [ ] **ACCENT-FILL CONTRAST CHECK:** For EVERY element with a filled accent background — regardless of class name. Buttons, CTAs, badges, pricing-card highlights, recommended-plan stripes, featured columns, pill tags, callout blocks, banners, active tabs, status pills, chips, photo callouts (commerce/PDP), Add-to-Bag controls in ready state. Compute text-on-fill contrast at REST AND at HOVER. Required: ≥ 4.5:1 (WCAG AA). The common failures and their fixes: (a) white text on `--accent` at L=0.55-0.70 with chroma 0.10-0.20 lands at ~3.9-4.4:1 → introduce `--accent-ink` at L=0.42-0.48 (same hue) and use it on the `background`, keeping `--accent` for links/tints; (b) hover state at HIGHER L than rest (e.g., 0.66 rest → 0.72 hover) REDUCES contrast on mouseover → set hover L EQUAL or LOWER than rest. Alternative path: keep the bright `--accent` fill and switch the TEXT to the dark page background (dark-on-bright passes 5:1+) — preserves vivid color, good for dark-themed sites.
- [ ] **TINTED-SECTION CONTRAST CHECK:** If any text element uses `color: var(--accent)` inside a section whose `background` is tinted with the same hue (the recommended 4-8% accent-tinted section background), recompute contrast. If < 4.5:1 (or < 3:1 for large text ≥ 18px regular / ≥ 14px bold), switch the text to `var(--text)` or `var(--text-2)` and let the section retain accent only on icons, strokes, or the underline of one keyword.
- [ ] **FOCUS-RING-ON-FILL CHECK:** For any accent-filled element (button, badge, pricing column, callout) with a focus indicator: the focus ring must be measured against the FILL color, not the page background. A same-hue accent ring against `--accent-ink` fill is ~1.3-1.6:1 — fails the 3:1 minimum. Use `--accent-focus-ring` set to paper / near-paper when the fill is `--accent-ink`, or invert (dark ring on bright `--accent` fill).
- [ ] **`--accent-ink` USAGE CHECK:** grep the CSS for `color: var(--accent-ink)`, `fill: var(--accent-ink)`, `stroke: var(--accent-ink)`, `border-color: var(--accent-ink)`. All must be ZERO. `--accent-ink` is a background-only token. If found as a foreground, replace with `var(--text)` or `var(--accent)` depending on intent.
- [ ] Accent color VISIBLE on CTAs, links, at least one tinted section
- [ ] Spacing follows scale
- [ ] Border radius uses 4-32 system
- [ ] All transitions use custom cubic-bezier
- [ ] At least 3 different section layout patterns
- [ ] No 2 consecutive sections with same background
- [ ] At least one dark-inverted section (or one light section if site is dark-themed)
- [ ] **ANIMATION VARIETY CHECK:** LIST your 2+ animation types here: ___. At least one MUST be domain-specific or typographic (not a generic IntersectionObserver fade-up). If you can only name "fade-up" and "hover lift", add a third. Counter animations are NOT mandatory — only use them where the number IS the story.
- [ ] **BENTO CHECK:** If `.bento-grid` exists: (a) is there ONLY ONE bento section on the page? (b) does the large card span BOTH axes? (c) is `grid-auto-rows: 1fr` used, NOT `auto auto`? (d) are there 3 responsive breakpoints (1024px + 768px)? (e) does the card count fill the grid with no empty cells? (f) does the large card contain real content (photo, mockup, or chart) — not just text?
- [ ] **PHOTOGRAPHY CHECK:** If Phase 3 classified the product as "photography mandatory" (hospitality, food, fashion, real estate, services, agencies), does the page include real `<img>` tags with Picsum/Unsplash URLs? Hero photo + at least one in-page photo? If you used a gradient blob where a photo should be, GO BACK.
- [ ] **BULLET CHECK:** The cap is by VISUAL pattern, not HTML tag. Count: (a) `<li>` tags outside nav and table cells: ___, (b) `<div>`s with checkmark/dot/arrow prefix characters or `::before` content markers: ___, (c) icon-plus-short-text repeated rows (e.g., feature lists, pricing checkmarks): ___. Sum: ___. If sum > 5, restructure. For each excess, name the replacement pattern from reference/non-card-patterns.md: ___.
- [ ] **EYEBROW CHECK:** Count uppercase pill-style labels above section headings. If more than 1, remove the excess. Ideally zero. The heading does the work.
- [ ] **CONTAINMENT VARIANCE CHECK:** A "card" is ANY rounded rectangle with a visible border or shadow, regardless of exact pixel values. Changing `border-radius: 16px` to `12px` does NOT make it a different containment. Count sections wrapped in any such card: ___. If > 2, replace the excess with one of: ledger rows (Pattern 1), definition list (Pattern 2), editorial rule sections (Pattern 3), real HTML table (Pattern 7), inline prose, or full-bleed photography. List the containment used for each section: 1.___ 2.___ 3.___ 4.___ 5.___ 6.___ 7.___. If fewer than 3 different patterns appear, redesign.
- [ ] **PRICING CHECK:** Number of plans this product actually has: ___. If 1 plan: pricing MUST be inline prose (reference/non-card-patterns.md Pattern 8) or a small card with the price as a number. NOT a single oversized "Most Popular" pricing card. If 2-4 plans: pricing should be a real HTML table (Pattern 7) showing feature rows with included/excluded indicators per plan — NOT 3 identical card-columns each with 6-8 checkmark rows (those checkmarks count as bullets and blow your budget). The 3-card pricing trio is banned as a default.
- [ ] **STAT SECTION CHECK:** Is there a 4-column counter strip? If yes, DEFAULT REPLACE with Pattern 5 (inline-stat narrative) or Pattern 6 (single hero stat). The 4-col counter strip is banned as a default. Only retained if ALL three are true: (a) the product is genuinely about measurable outcomes (analytics, monitoring, billing dashboards — not agencies, hospitality, services), (b) you actively chose this pattern in Phase 4 over Patterns 5/6, (c) you documented why in DESIGN.md. If any is false, replace it.
- [ ] **MOCKUP CHECK:** Are there empty gradient rectangles where visuals should be? Replace with CSS mockups from reference/css-mockups.md.
- [ ] **TESTIMONIAL CHECK:** Any banned names (Sarah Chen, Marcus T., Priya S., Maria Santos)? Any gradient-circle avatars? Fix both.
- [ ] **ZERO-PAD CHECK:** Any "01.", "02.", "03." decorative numbers? Change to 1, 2, 3.
- [ ] **MOBILE MENU CHECK:** Does the hamburger toggle have working JS? Hidden nav with no toggle = broken site.
- [ ] **SKELETON CHECK:** Is the page exactly: hero → 3-cards → steps → stats → testimonial → CTA? Rearrange at least 2 sections.
- [ ] **NAV CHECK:** Header is the scroll-state pattern (transparent-over-hero → hairline + backdrop-blur + modest shrink past a threshold), not a shadowed edge-to-edge bar or a default floating pill. Mobile drawer has scroll-lock + focus trap + Esc. See reference/navigation.md.
- [ ] **FOOTER CHECK:** Footer type matches category (fat-sitemap / typographic / minimal-utility) — no fabricated columns, no fake 8-grid on a thin site. Every footer link AA contrast + 44px target + visible focus. Utility strip shows only utilities that actually exist.
- [ ] **DARK-MODE CHECK:** If dark-themed — elevation inverts (lighter surfaces, not shadows), hairlines are white-alpha, accent chroma dropped while AA still passes, any film grain ≤0.02 opacity on named solid surfaces only (never a global overlay or a smuggled gradient). See reference/dark-mode.md.
- [ ] **PRODUCT-UI / WEBGL GATE CHECK:** Any live-UI mockup, PDP, Cmd-K palette, trust surface, or WebGL hero present ONLY because the Phase 4 gate (5e/5f) selected it? Fake live UI, cargo-cult Cmd-K, shield-icon security grids, and connect-the-dots particle backgrounds are banned (anti-patterns 56-70). WebGL poster is the LCP `<img>`, never the canvas.
- [ ] Icon stroke weight 0.8-1px, one family
- [ ] Responsive at all 6 breakpoints
- [ ] Touch targets 44px minimum
- [ ] **DOES THIS LOOK LIKE LINEAR/VERCEL/STRIPE? Or does it look like a magazine?** If magazine, you went editorial. Fix it.

### Output
Present. STOP. Wait for approval.

---

## Phase 6: Subtraction Pass

### Earn Your Pixel
Strip on sight:
- Fake metadata, doc IDs, version numbers
- Decorative timestamps, ETAs
- Redundant labels above clear data
- Section numbers used as decoration
- Decorative OR thin/placeholder footers (a real footer is load-bearing; a 3-link strip or a fabricated 8-column grid on a multi-area product is the cheap tell — size the footer to real IA per reference/non-card-patterns.md Footer Architecture)
- Any WebGL/3D element that fails the single-question test in reference/webgl-3d.md
- Full prose where fragments work
- Any italic text
- Any monospace not displaying code/data
- Any gradient not requested
- Fake browser chrome
- Template duplication (identical layouts across sections)
- Any uppercase pill eyebrows above section headings (target zero, absolute max 1 per page)

### AI Slop Detection (73 patterns from reference/anti-patterns.md)
Load `reference/anti-patterns.md`. Check all patterns. Flag with confidence tier.

### UX Writing Audit
Load `reference/ux-writing.md`. Check banned words, char limits, generic CTAs.

### Output
List flags. Present. STOP. Wait for approval.

---

## Phase 7: Audit and Grade

### Responsive Verification
Check at 375px, 768px, 1024px, 1280px, 1536px.

### Accessibility Review (WCAG AA, non-negotiable)
| Check | Requirement |
|-------|-------------|
| Body text contrast | 4.5:1 |
| Large text contrast | 3:1 |
| UI components | 3:1 |
| Focus indicators | `:focus-visible`, 2-3px ring, 3:1+ contrast |
| Touch targets | 44px min |
| Keyboard nav | Tab + Enter/Space on everything |
| Skip link | Present, hidden until focused |
| Heading hierarchy | No skipped levels |
| Alt text | All informational images |
| Form labels | Visible, never placeholder-only |
| Color independence | No info by color alone |
| Motion | `prefers-reduced-motion` respected |
| Screen reader order | DOM = visual order |

Cannot score above B with critical accessibility failures.

### Scoring (6 categories, weighted)
| Category | Weight |
|----------|--------|
| Visual Design | 20% |
| Interaction & Animation | 20% |
| Responsive | 15% |
| Accessibility | 15% |
| Performance & Polish | 15% |
| Content & UX Writing | 15% |

Letter grades: A (90-100), B (80-89), C (70-79), D (60-69), F (0-59).

### Output
Audit report with scores, findings, priority fixes. Present. STOP. Wait for approval.

---

## Phase 8: Hardening

- Text overflow handling on every element
- Font-loading discipline (REQUIRED — the distinctive non-Inter font mandate makes this non-optional): self-host a SUBSET variable `woff2`, `<link rel="preload" as="font" crossorigin>` the one critical headline face, `font-display: swap`, and ship a metric-matched fallback (`size-adjust` + `ascent/descent/line-gap-override`) to kill CLS. Match Vercel's `next/font` discipline.
- i18n: 30-40% space budget, logical properties for RTL
- Error states: 400/401/403/404/429/500 each with specific UX
- Empty states: copy, not illustrations
- Loading states: skeleton or spinner, never blank
- Focus management: `:focus-visible`, trapped in modals, returned on close
- `prefers-reduced-motion`: all animations suppressible
- Core function works without JS

### Output
List fixes. Present. STOP. Wait for approval.

---

## Phase 9: Handoff

- Design system summary (font, colors, spacing, radius, motion, icons)
- Route-to-component map with parity status
- Decisions log
- Known open items
- What's working (don't touch)
- Grep entry points

### Output
Write handoff. Done.

---

## Design Laws (Always Active)

### The North Star
The North Star follows the brief, not a single template. SaaS/dev tools/fintech → Linear, Vercel, Stripe. Hospitality/luxury/food → Aman, The Modern, Aesop. Agencies → Pentagram, Studio Sutherl&. Services → quiet editorial sites. If you've built every brief to look like Vercel, you went wrong. Match the category.

### Aesthetic
- One accent color, visible on links, hover states, icons, and at least one tinted section. No gray/slate "accents." Primary CTAs use `--accent-ink` for the fill when text is near-white (see Color System step 5); base `--accent` fill only with dark text.
- White or near-white backgrounds by default. Cream ONLY for food/bev/hospitality/wellness/agriculture Warm/Earthy brands.
- True black or near-black ink by default. Brown ONLY for the same warm categories.
- Hairline borders only. No 1px solid gray everywhere.
- Elevation through lightness, not heavy shadow.
- 64-120px between major sections.
- Variance per section. No 2 consecutive sections share background OR containment.

### Typography
- ONE sans-serif family by default. Serif headings allowed on Warm/Earthy food/bev/luxury/hospitality/heritage brands.
- Serif body permitted (rare) for editorial brands and literary services.
- NO Inter as default. Must be justified.
- NO italics. Period.
- Monospace is a small (≤14px) DATA ACCENT only (IDs, version tags, timestamps, stat units, tabular figures, code) in devtools/fintech/hardware registers — never body, headline, or eyebrow. A mono eyebrow is the new pill-eyebrow.
- Hierarchy through weight and size, not font mixing.
- Craft layer always on: `text-wrap: balance` on headings / `pretty` on prose, `tabular-nums` on aligned figures, optical sizing only when the face carries an `opsz` axis. No animated variable-axis weight, no decorative `ssXX`/swashes.
- Font-loading discipline required: subset variable woff2, preload the headline face, `font-display: swap`, metric-matched fallback (no CLS).
- Editorial long-form apparatus (masthead, drop cap, pull quotes, display-serif roster) is gated to earned-serif editorial/publishing products only — reference/typography-editorial.md. Never on SaaS, agency, or marketing pages.
- Eyebrows/pill labels: max 1 per page, ideally zero.
- Bullets: max 5 per page total. Use ledgers, definition lists, tables instead.

### Animation
- Minimum 2 different types per page. Fade-up alone doesn't pass.
- One must be domain-specific or typographic — not just a generic IntersectionObserver fade-up.
- Counter animations are NOT mandatory and often a tell. Use only when the number IS the story.
- Custom cubic-bezier. Never linear or default ease.
- Vary translateY distances and timing per element type.
- GPU-safe: transform and opacity only.
- `prefers-reduced-motion` always respected.

### Imagery
- Photography mandatory for: hospitality, food, fashion, real estate, services with human element, agencies, lifestyle, travel.
- Use real `<img>` tags with Picsum or Unsplash URLs (see reference/imagery.md).
- NEVER substitute a gradient blob for a required photo.
- Alt text describes what the photo SHOULD show for this brand.
- For software products, CSS mockups are fine. For physical/human products, photos are required.

### Containment
- Default rounded-rectangle card appears in AT MOST 2 sections per page.
- Other sections use ledgers, definition lists, tables, prose-only, full-bleed photography.
- 3+ different containment patterns required per page.
- See reference/non-card-patterns.md.

### Illustration
- Respect the medium. No physical product renders in HTML/CSS.
- Typography beats bad illustration.
- No fake browser chrome (red/yellow/green dots). EVER. No exceptions.
- Use CSS mockups from reference/css-mockups.md for section visuals. No empty gradient rectangles.

### Layout
- 16 section layout patterns available. Use at least 3 per page.
- Never same layout twice in a row.
- Never 2 consecutive sections with same background.
- At least one dark section per page. If the site is dark-themed, at least one light section.
- Bento grids MUST have cards of different sizes with spanning. See reference/bento-grids.md.
- Do not follow the default template skeleton on every page. Vary the section order.

### Navigation
- Header: transparent-over-hero, condenses past a scroll threshold (hairline + backdrop-blur + modest shrink); single primary CTA; max 5 links; engineered mobile drawer (scroll-lock + focus trap + Esc). Floating-pill nav and a Cmd-K palette are tells, not defaults. See reference/navigation.md.

### Footer
- Footer type follows category: fat sitemap (hairlines, not cards) for multi-area SaaS/fintech; typographic for agency/luxury; minimal utility for thin IA. Name the real IA behind any columns — never fabricate a grid. Oversized cropped wordmark is opt-in only. Borderless; exempt from the card and bullet budgets. See reference/non-card-patterns.md Footer Architecture.

### Dark Mode
- Default zero. If the scene forces dark, engineer it as a system (reference/dark-mode.md): elevation INVERTS (lighter surfaces, never shadow), white-alpha hairlines, accent chroma DROPS while staying AA-legible, tokens per theme. No glowing accents. Film grain ≤0.02 on named solid surfaces only — never a global overlay, never a smuggled gradient.

### WebGL / 3D
- Default zero. Max 1 WebGL element per page, SaaS/devtools/fintech hero only — never on services/hospitality/food/agency/editorial. Animated shader gradients do NOT override "no gradients unless asked" or anti-pattern #14 — gated branded hero moment only, never decorative wallpaper. Poster is a real preloaded `<img>` (LCP), never the canvas. Connect-the-dots particle backgrounds are banned. See reference/webgl-3d.md.

### Product Surfaces
- Live product UI, e-commerce PDP kits, conversion bars, command palettes, trust surfaces, and hardware callouts are gated (Phase 4, gate 5e) and opt-in only — never auto-added. Honest states, no browser chrome, every shortcut badge backed by a real shortcut. See reference/product-ui.md.

### UX Writing
- Short. Specific. No banned words. No generic CTAs.
- No section numbers as decoration.

### Icons
- Outlined. Stroke 0.8-1px. One family. 16/20/24px.

### Border Radius
- 4-32 system. No arbitrary values.

### Responsive
- Mobile-first. 6 breakpoints. Fluid typography via clamp().
- No horizontal scroll. `min-h-[100dvh]` not `h-screen`.

### Accessibility
- WCAG AA minimum. 4.5:1 body, 3:1 large text and UI.
- Keyboard nav. Skip link. Alt text. Heading hierarchy.

### Anti-Patterns
- Check against 73 rules in reference/anti-patterns.md before every output.
- The cream trap: cream + non-food product = wrong.
- The Inter trap: Inter without justification = wrong.
- The serif trap: serif on a non-warm-earthy non-editorial product = wrong.
- The bento trap: equal-size cards labeled bento = wrong. Also: bento on every page = wrong.
- The browser chrome trap: red/yellow/green dots on anything = instant AI tell.
- The gray accent trap: accent indistinguishable from ink = not an accent.
- The gradient blob trap: empty rectangles where visuals should be = wrong. Use a real photo or a real mockup.
- The skeleton trap: same section order on every page = template.
- **The bullet trap:** more than 5 total bullets per page = AI signature.
- **The eyebrow-pill trap:** uppercase pill above every section heading = AI signature.
- **The card-chrome trap:** every section in the same rounded-rectangle card = AI signature.
- **The 3-tier pricing trap:** Free/Pro/Enterprise as three identical cards = default reflex. Use a real table or inline pricing.
- **The 4-col counter trap:** 4 columns of numbers counting up = default SaaS reflex. Use prose-integrated stats or one hero stat.
- **The missing-photo trap:** hospitality/food/fashion/real estate without `<img>` tags = a placeholder, not a finished site. Use Picsum or Unsplash URLs.
- **The terminal-cosplay trap:** mono on a heading/eyebrow/body run, or mono outside tech registers = the new pill eyebrow.
- **The gray-on-gray trap:** "tonal monochrome" with no accent AND no photography on a non-luxury product = AI slop, not restraint.
- **The nav-template trap:** a shadowed edge-to-edge bar, or a floating pill / Cmd-K palette by default = template block. Use the scroll-state header (reference/navigation.md).
- **The thin-footer trap:** a 3-link strip or a fabricated 8-column grid = wrong-sized footer. Size to real IA (reference/non-card-patterns.md Footer Architecture).
- **The particle-background trap:** connect-the-dots / floating-particle WebGL = the stock "tech company" tell.
- **The dark-flip trap:** dark mode as a palette flip — no inverted elevation, gray (not white-alpha) hairlines, a glowing accent = not engineered dark.
- **The one-image-PDP trap:** single image + native dropdown on a commerce page = free Shopify theme. Use the PDP kit (reference/product-ui.md).
- **The fake-live-UI trap:** browser chrome, fabricated cycling, or decorative keycaps wired to nothing = AI tell. Real states only.
- **The cargo-cult Cmd-K trap:** a command palette on a brochure site = signaling, not product. Gate it to real apps.
- **The shield-grid trust trap:** icon-card "security" grids = the thing trust surfaces replace. Use named certs + dates.
- **The conversion-chrome trap:** countdown timers, flashing urgency, fake scarcity, rotating announcement bars = Shopify-app aesthetic. One calm savings line + one sticky buy-bar, nothing more.
- **The eyebrow-bar trap:** the lone-eyebrow styled with a `::before` 36×1px line beside the label = the pill's 2026 replacement. The bar reads as "----". Use typography alone — no decorative rules, no leading "—" character, no underlines.
- **The under-darkened button trap:** primary button using the base `--accent` (L=0.55-0.70) as `background` with white text lands at ~3.9-4.4:1 and FAILS WCAG AA. Derive `--accent-ink` at L≤0.48 (same hue) for button fills; keep `--accent` for links and tints.
- **The hover-gets-lighter trap:** `--accent-hover` at HIGHER L than the rest fill makes white text LESS readable on mouseover. Hover MUST be equal-or-darker than rest.

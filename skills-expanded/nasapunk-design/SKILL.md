---
name: nasapunk-design
description: >-
  NASApunk retro-futurist frontend design system with a Starfield-inspired modern layer — NASA golden age (1960s–1980s) aesthetic evolved with Starfield's contemporary polish, for building or restyling web pages. Worn white baked-paint panels, gold Kapton insulation foil crinkle gradients, worm-style single-stroke red wordmark, Swiss grid typography (Helvetica + monospace stencil labels), technical documentation textures (rubber stamps, blueprint grids, hazard stripes, rivets, monospace spec tables, mission patches, doc-control bars) — plus Constellation-style four-color emblem stripes, soft-shadow panel refinement, and a systematic ease-out/stagger motion language. Spirit: "High tech, high hope" meets "Forever in adventure" — institutional optimism, worn-not-ruined hardware, utility-first engineering realism, warmly modernized. Use for building or refactoring ANY page into NASApunk/Starfield style: retro space-agency landing pages, aerospace-themed dashboards, mission-control UIs, magazine covers, agency memos & dispatches, reading pages and book chapters, museum-exhibit bands, wayfinding signage, heritage insignia - atomapunk/cassette-futurism adjacent frontends. One base skin, two surface families: PRINT DOCUMENT (light, dominant) and CONSOLE INSTRUMENTS (dark, auto-deployed on fitting scenes or on request). Framework-portable: all laws adapt to React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui.
  中文触发词：NASApunk、NASA朋克、航天朋克、复古未来主义、太空机构美学、NASA风格前端、星空风格页面、星空Starfield风格、星座条纹、杂志封面、公文备忘录、阅读页、导视牌、三环仪表、纹章徽章、风格选择、控制台模式、印刷文档模式。
---

# NASAPUNK DESIGN SYSTEM (× STARFIELD-MODERN)

Build pages that read as "1970s government aerospace documentation meets worn flight hardware — polished with Starfield's modern brand-system confidence."
Reference implementation (baseline template): `assets/reference.html` (open in browser — single file, zero dependencies).
Copy-paste CSS recipes: `references/snippets.css`.

---

## 0. STACK PORTABILITY (global constraint)

Every law and recipe in this skill MUST remain implementable across **React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui**:

- The single-file HTML reference is the CANONICAL spec. When the target stack differs, translate tokens/structure - never drop laws.
- Tokens: CSS custom properties are canonical; map them 1:1 to platform equivalents (SwiftUI Color/Font extensions, RN theme object, Flutter ThemeData, Tailwind theme.extend.colors).
- Effects matrix: hatching/stripe fills = repeating-linear-gradient (web/Tailwind arbitrary values) | SwiftUI `.linear-gradient` stripes or ShapeStyle | RN gradient lib | Flutter `DecoratedBox`/CustomPainter. Donut/dial = conic-gradient | SwiftUI `Circle().trim(AngularGradient)` | RN `react-native-svg` Circle strokeDasharray | Flutter CustomPaint. blend/mask tricks degrade gracefully - substitute precomputed colors where a stack lacks mask support.
- Component mapping: figure plates/cards become components per stack (shadcn/ui = recipe over primitives; SwiftUI/RN/Flutter = view structs/widgets); semantic roles (figure/figcaption, table headers) preserved for a11y.
- Workflow: build against the HTML reference first when unsure, then port; visual verification (§9 step 10) applies to EVERY stack output.

---

## 0B. STYLE SYSTEM (one base skin, two surface families)

One base skin carries TWO surface families. Both deploy AUTOMATICALLY when the scene fits - and the user can always explicitly request either:

| Surface family | Ground | Deploy when |
|---|---|---|
| **PRINT DOCUMENT** (dominant) | Light paper + ink; report figures; document props woven in | Default for pages and sections; always the page-level base |
| **CONSOLE INSTRUMENTS** | Dark `#0A1420`/panel grounds + §2B tokens + §5g components | Scene fits an instrument: terminals, logs, dashboards, status walls, data-dense readouts, HUD widgets - OR user explicitly requests dark/console mode |

### Base skin composition (always on)

- §2 light tokens + ALL §4 texture recipes
- §6 print-document layer woven in (>=2 Band-15 artifacts)
- §2B console tokens + §5g component grammar, deployed onto fitting sections
- **Era grades are part of this skin's toolkit**: apply a root class (.era-apollo etc.) when the scene warrants a commemorative/heritage tone; default none

### Deployment laws

- Page-level ground stays LIGHT unless the user explicitly requests full-console mode
- Dark instrument surfaces attach to instrument-shaped content: terminals, log walls, telemetry, status-heavy clusters - never to body text or reading surfaces
- If the user asks "which styles exist", present both surface families from this table
- If the user wants BOTH skins on one subject, deliver a variant set: PRINT version first as canonical, then a CONSOLE twin
- Silence = PRINT-dominant build with autonomous dark-instrument deployment where scenes fit

## 1. THE ONE RULE (dual-layer decision filter)

> **Layer 1 (retro body): "Would this look at home in a 1979 government technical exhibit?"**
> **Layer 2 (modern soul): "…and would Starfield's brand team ship it today?"**

Every visual decision passes through BOTH. Layer 1 blocks cyberpunk drift; layer 2 blocks museum-piece stiffness. NASApunk is NOT cyberpunk, NOT neon sci-fi — and NOT a costume: the retro language is executed with contemporary cleanliness.

Spirit checklist — the page must feel:
- **Grounded**: everything extrapolated from real aerospace tech; function parts visible (tanks cylindrical, pipes exposed, radiators prominent)
- **Institutional optimism**: "High tech, high hope" → extended by Starfield's "Forever in adventure" — scientifically inspired, grounded warmth, unapologetically optimistic
- **Utility first**: design serves engineering truth, not gloss; hardware looks like it just came out of a lab
- **Worn, not ruined**: "乐观主义的磨损" — scuffed paint, lived-in surfaces, but maintained and loved ("a worn and loved futuretech" — ESA). Never decayed/abandoned
- **Analog-first**: physical switches > touchscreens; CRT texture only on instrument widgets
- **Systematically branded**: like AKQA's Clio-winning brand book — consistent tokens, deliberate motion, dos-over-don'ts coherence

---

## 2. COLOR TOKENS (hardcode exactly — no free interpretation)

```css
:root{
  /* Brand layer */
  --red:#E4002B;            /* signal red (proven default) */
  /* Official alternatives: worm red PMS 179 = #E03C31 (warm orange-red,
     light backgrounds ONLY); meatball red PMS 185 = #FC3D21 */
  --navy:#0B3D91;           /* NASA blue PMS 286 */
  --ink:#20232A;

  /* Paint / metal layer */
  --paint:#F4F3EF;          /* off-white baked paint — page base, LIGHT-dominant */
  --paint-alt:#E9E7E1;
  --metal-light:#A8ACAF;
  --metal-mid:#6E7378;
  --metal-dark:#43484C;
  --rule:rgba(67,72,76,.28);
  --seam:rgba(67,72,76,.38);

  /* Rust / orange-brown layer */
  --rust:#C96A2B;
  --rust-deep:#8C4A22;

  /* Kapton gold layer — use SPARINGLY (1–2 hero elements max) */
  --gold-1:#E8B84B;
  --gold-2:#C9932E;
  --gold-3:#A87A1F;
  --gold-sheen:#B98A5A;

  /* STARFIELD-MODERN accent layer (extracted from game assets, ColorKit)
     ACCENT ONLY — base stays red/white/blue dominant.
     Division of labor: Kapton gold = hardware foil; sf-gold = brand badge. */
  --sf-gold:#d4ac63;
  --sf-crimson:#cd2435;
  --sf-orange:#e56335;
  --sf-navy:#2b4d7d;
  --sf-offwhite:#f4f5f7;

  /* Motion tokens (Starfield motion language) */
  --ease-out:cubic-bezier(.2,0,0,1);
  --ease-in:cubic-bezier(.4,0,1,1);
  --dur-enter:240ms;
  --dur-exit:180ms;
  --stagger:30ms;
}
```

**Color laws** (worm-era graphics standards, 1976-92, used as stylistic reference window):
- Red/white/blue dominant + gray-white metal base + orange-brown accents
- **NO PASTELS** — explicitly banned by the manual; bright primaries only
- Warm red is THE signature color; navy is structure; gold is rare and precious (Kapton foil reads as expensive thermal hardware)
- Worm-style red only on white/light backgrounds
- `--sf-*` tokens are a thin accent layer: emblem stripes, small chips, motion highlights. Never repaint base surfaces with them.

Shared noise/grunge data-URIs (inline feTurbulence, zero network):
```css
--noise:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)'/%3E%3C/svg%3E");
--grunge:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.55' numOctaves='3' seed='7' stitchTiles='stitch'/%3E%3CfeColorMatrix type='matrix' values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.92 0'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23g)'/%3E%3C/svg%3E");
```

### 2B. CONSOLE-MODE TOKENS (dark surface mode)

Console mode is the sanctioned full-page dark variant: instrument-band logic expanded to a whole page. Deploy it in EITHER of two ways: (a) autonomously, when the scene is instrument-shaped (terminal/dashboard/log wall), or (b) on explicit user request for dark/console/HUD mode (§6). Hardcode exactly:

| Token | Value | Role |
|---|---|---|
| `--bg-deep` | `#0A1420` | Page base, deep space blue-black |
| `--panel-base` | `#15181C` | Console panel ground |
| `--slate` | `#35444A` | Structural metal, rules, bezels on dark |
| `--info-cyan` | `#4AA8C0` | Passive data / tech / info |
| `--screen-glow` | `#7FC8B0` | Phosphor readouts, live values |
| `--alert-amber` | `#E29726` | Alerts / actions / interactive states |
| `--danger-red` | `#E71D24` | Failure and danger states |
| `--equipment-cream` | `#D8D2C0` | Primary body text on dark |
| `--equipment-cream-hi` | `#E8E4DA` | Emphasized text, headlines on dark |

**Console-mode color laws**:
- **SEMANTIC AXIS**: the cyan family (`--info-cyan`, `--screen-glow`) marks passive data/tech/info ONLY; amber (`--alert-amber`) marks alerts/actions/interactive states ONLY, never decorative rest-state
- NO pure `#000` or `#FFF` surfaces anywhere in console mode
- Panels are FLAT alpha overlays of `--panel-base` at ~55-66% opacity over `--bg-deep`; `backdrop-filter:blur` FORBIDDEN (Scaleform-faithful flatness)
- Console mode inherits every other §2 law unchanged; the light palette remains the default page mode

### 2C. ERA COLOR GRADES (optional light-mode tint grades)

Optional tint grades over the standard §2 print palette, named after Starfield's real photo-mode filters (Mercury Era / Gemini Era / Apollo Era). Implement each as a class-scoped `:root` override on the root element (`<html class="era-apollo">`): the class re-maps existing tokens, it never adds new ones. Hardcode exactly:

| Class | Shift direction | When to use |
|---|---|---|
| `.era-mercury` | Cool grey-blue shift: slightly desaturate warm tones, nudge `--paint` toward grey | Early-program austere documents, cold test-phase sobriety |
| `.era-gemini` | Neutral steel: balanced temperature, no channel bias | Program-midpoint neutrality; the baseline read with a cooler spine |
| `.era-apollo` | Warm sepia shift: nudge neutrals toward tan/brown | Golden-age warmth, commemorative and heritage pieces |

**ERA GRADE LAWS**:
- Grades are SUBTLE: token-level tints only, never new hues; the base §2 palette must stay identifiable through the grade
- ONE grade per page, applied at the root; never mix grades inside a page
- Console mode (§2B) ignores era grades entirely
- Recipe: `references/snippets.css` Band 14

---

## 3. TYPOGRAPHY LAWS (Swiss / NHB 1430.2)

```css
--font-head:"Helvetica Neue",Helvetica,Arial,"Liberation Sans",sans-serif;
--font-mono:ui-monospace,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
```

| Element | Rule |
|---|---|
| Headings | Helvetica stack, UPPERCASE, weight 800, tight tracking `-0.02em`, line-height **1.04–1.08 when multiline** (below ~1.02 descenders/comma tails invade the next line's caps); ≤1.0 only for single-line display |
| Stencil labels | Monospace uppercase, wide tracking `+.12em` to `+.16em`, size 9.5–11px — technical tag voice |
| Alignment | **flush-left / ragged-right** (never justified) |
| Data tables | Monospace, `font-variant-numeric:tabular-nums`, thin bottom rules, labels left / values right-aligned bold |
| Body | Line-height ≥1.45 |

**Nasalization note (Starfield's UI typeface)**: Starfield's menus use **Nasalization** (Ray Larabie, 1997) — a geometric sans whose letterforms descend from the worm logotype of the worm-era graphics standards (1976-92) used as stylistic reference window. It is the *spiritual benchmark* for display type. Web zero-dependency strategy: keep the Helvetica stack as default; if the host project already loads a licensed Nasalization or similar geometric sans, apply it to display headings via an optional `@font-face` hook. Without it, hint the geometry with slightly wider tracking (+0.01em) on the largest headline only.

**Font tiering note (reference faces vs free chain)**: Starfield's actual UI faces are **NB Architekt** and **NB Grotesk R** (Neubau Berlin, commercial licenses, diamond-grid construction). They are the REFERENCE faces: study their proportions, never hotlink or embed them. Free implementation chain for tech display: **Exo 2** first, **Chakra Petch** where a harder stencil-technical voice is needed; both via host-project font loading only (zero external requests law still applies to shipped output). Directional arrows `←` `↑` `→` `↓` are set in the text font itself, never swapped for icon sprites. CJK note: when CJK glyphs enter the stack, the Latin face carries identity alone; pair any system CJK fallback and do not attempt to stylize CJK glyphs.

**Prop document fonts (diegetic print props)**: memos, forms, crates and other diegetic prop documents MAY set BODY text in a plain late-90s system stack `"Verdana",Tahoma,Geneva,sans-serif`, reproducing the game's actual printed-prop texture (community font surveys report stock Microsoft-era faces on posters/signage). The display/headline layer stays Helvetica-family. Law: prop fonts never exceed body/small sizes and never appear in mastheads or display settings.

---

## 4. TEXTURE RECIPES (effect → technique → where)

Full copy-paste code in `references/snippets.css`; live examples in `assets/reference.html`.

| Effect | Technique |
|---|---|
| Worn white paint | Layered radial-gradient scuffs (white highlight top-right + faint rust/gray stains) over flat `--paint`; site-wide 5% `--noise` grain via fixed overlay |
| Metal plate panel | `--paint-alt` bg + inset bevel box-shadows (top-light/bottom-dark) + hard offset shadow (`5px 6px 0 rgba(...)`) + 1px seam border |
| Rivet rows | `repeating` radial-gradient dot tile (dark core + white highlight), repeat-x top & bottom edges of panels — see `.rivets` |
| Corner screws | Radial-gradient dots via panel `::before/::after`, highlight at 35%/30% |
| Panel seams | 1px `--seam` borders + inset bevel shadows |
| Gold Kapton foil | Multi-stop linear-gradient (#E8B84B→#C9932E→#A87A1F + #B98A5A sheen) × TWO crossing `repeating-linear-gradient` crinkle facets (~112deg + ~23deg) + noise multiply overlay — see `.kapton-rail` |
| Rubber stamp | Rotated bordered text, double ring (::before inset border), grunge ink via `mask-image:var(--grunge)` + `mix-blend-mode:multiply`, opacity .88 — see `.stamp` |
| Hazard stripe | `repeating-linear-gradient(45deg,#17181A 0 13px,var(--gold-1) 13px 26px)` full-bleed strip + caution note in rust-deep mono |
| Blueprint section | Navy `--navy` background + dual-scale light grid (two `repeating-linear-gradient` pairs: 24px fine + 120px coarse) + dashed leader lines → SVG line-art annotations |
| Drafting-paper surface | Cream `#FBFAF7` + light gray grid 22px (α.05), optional coarse 110px majors - section/card background for document-genre pages; recipes `.np-graphpaper(--pad)` Band 15b |
| Mission patch | Circular SVG badge: navy ring, circular `textPath` lettering, red planet arc, gold capsule on dashed trajectory, stars |
| Telemetry widget | Dark `--metal-dark` band, mono tabular values in `--gold-1`, blinking caution lamp; **CRT scanlines (repeating-linear 0deg 1px/3px + flicker keyframe) confined to THIS widget only** |
| Doc-control bar | Top strip on `--metal-dark`: mono 10px `DOC NO. XXX-71-C • REV C • FORM 8-246` metadata |
| **Constellation emblem stripe** | Four SOLID bars side-by-side, hard edges (`navy→gold→orange→crimson`) as accent — see §5a |
| Motion polish | Ease-out/stagger system + shine sweep + scan reveal — see §5 |
| Charts & meters | Segmented bars / horizontal meters / donut gauges in framed instrument panels — see §5e |
| Brushed-metal bevel panel | Console-mode counterpart of "Metal plate panel": dark `--panel-base` ground + inset highlight/shadow bevel box-shadows + low-opacity streak gradients along the brush direction; ALWAYS matte, never glossed |
| Wet-gloss streak | ONE low-opacity linear highlight band across a dark panel; never on text surfaces |
| Breathing vignette | Radial-gradient corner darkening at ~50-60% strength behind hero and empty states; sits under content, never over it |
| Warm-cool split light | Cool shadow tint `rgba(58,90,110,.25)` paired with warm key tint `rgba(232,136,48,.35)`; keep the pair balanced wherever dark surfaces meet light |

### 4.1 Blueprint grid — required scenarios

The navy dual-scale grid (§4 "Blueprint section" row) is a signature device. Apply it as a REQUIREMENT to:
- Any technical drawing / diagram / schematic section
- Data-dense exhibits: spec tables wider than 2 columns, dashboards, telemetry-adjacent readouts
- Sections whose content IS engineering documentation (drawings, tolerances, revision history)

Do NOT apply to: body-text paragraphs, footer/legal fine print, hero headline zone, or anywhere it would sit behind running text at full strength.
Legibility law: grid lines ≤7% opacity equivalent (`rgba(244,243,239,.035–.075)` on navy); content contrast always wins over texture. A light-on-paint variant (`--rule` colored lines) may serve data sections on light surfaces.

### 4.2 Small-icon style contract

| Property | Rule |
|---|---|
| Format | Inline SVG only; stroke-based line art; `fill="none"` on shapes |
| Stroke | 1.5–2 units at a 24–48 viewBox (visually ≈ hairline-to-medium); round caps |
| Color | Single hue via `currentColor`/`--metal-dark` on light, `--paint-alt` on dark; ONE small filled accent allowed per icon (dot/square in `--red` or `--gold-1`) |
| Geometry | Circles, rects, 45°/60° diagonals; engineering-glyph voice (gyro rings, chip pins, blanket waves); no filled silhouettes except tiny status dots |
| Family consistency | Same stroke width + corner language across every icon on the page |
| Forbidden | Emoji, icon fonts, external icon libraries |

### 4.3 Composition coherence rules

- Max TWO texture systems per component (a plate may be rivets+seams; not rivets+hazard+stamp+foil stacked)
- Max ONE grid-breaking element per section (chip/stamp); everything else sits on the grid
- Color proportion target: ~70% neutral paint/metal · ~20% structure (navy/ink) · ~10% accents (red/emblem bars/Kapton)
- Nested blocks inherit their host's alignment; never stack independently rotated children
- Every decorative layer must EARN its place: hazard=warning, stamp=approval, emblem=identity. Decoration stacked on decoration with no meaning = delete it

### 4.4 Layout collision prevention (hard rules)

1. Text-over-block requires ≥4.5:1 contrast against THE BLOCK's color — never dark glyphs on navy/red, never light on paint
2. Hanging decorations: negative offset + element width must fit inside container side margin — or reserve space with padding instead of hanging into the margin at all
3. z-index registry — background slabs `1` < content `2` < accents `3` < rails `4` < stamps `6`; never improvise values
4. Breakpoint audit: every absolutely-positioned element re-checked at 1440/1020/720/380px; when base geometry changes, DELETE stale responsive overrides (don't patch around them)
5. `white-space:nowrap` data gets an ellipsis/shrink guard at ≤720px; wide tables scroll horizontally instead of compressing
6. Stamps/chips may overlap only EMPTY space or their own host's border — never glyphs of unrelated text

### 4.5 Ambient line-art backdrop (doodles)

Low-opacity stroke-only SVG motifs scattered as background decoration: ringed planet, latitude planet, spiral galaxy, constellation + four-point sparkle, retro rocket, orbit diagram. Build ONE hidden `<defs>` symbol library; instantiate with `<svg class="doodle"><use href="#dd-*"/></svg>`.

Laws:
- Stroke `currentColor`, `fill:none`, stroke-width ~2 @ 120 viewBox — same drafting voice as §4.2 icons
- Opacity **0.06–0.10** on light surfaces (`color:--metal-dark`), **0.10–0.14** on navy/blueprint (`--paint-alt`)
- Always `pointer-events:none`; `z-index:0` with every section's `.container` lifted to `z-index:1` — doodles may pass under text but must never lower its contrast; prefer placing them in padding/margin whitespace zones
- Deterministic hand-placed positions, sizes 60–180px, slight rotations — NO JS random placement (reproducibility + collision control); ≤2 per section; skip dense instrument bands (telemetry) entirely
7. **Text-in-box law**: compute rendered width BEFORE boxing text — monospace advance ≈ `0.6em + letter-spacing` per char; rendered text must fit its box minus ≥6% side padding. Size the box to the string, never squeeze the string into a pre-existing box
8. **Circular textPath law**: baseline radius = ring-band midpoint − cap-height/2 (glyphs grow OUTWARD from the baseline on top arcs); path length must exceed text length (`semicircle = π·r`) — verify with the 0.6em+tracking estimate, shrink font/tracking until it fits with ≥5% margin. Clipped glyphs or baseline-hugging rings are defects
9. **Marker/label lane separation**: timeline/map markers and their labels live in separate perpendicular lanes — ≥6px clearance between marker's rotated/hover bounding extent and label ink at BOTH rest and hover states. Preferred pattern: step the label **diagonally up-right of its marker** (both axes offset, technical-callout style) — diagonal separation survives hover growth far better than direct stacking; on mobile collapse to stacked flow with the marker moved into a side gutter

---

## 5. STARFIELD-MODERN LAYER (the evolution, not a repaint)

This is what separates "museum-piece retro" from Starfield's shipped aesthetic. Apply AFTER the NASApunk base is complete.

### 5a. Constellation four-color emblem stripes

The signature motif — from AKQA's brand book: *"a stripe composed of four earthly colours became their emblem."*

**Construction (critical)**: NOT a smooth gradient. It is **4 equal-width SOLID-COLOR bars side-by-side with hard edges**, square ends, tight/no gaps, full height. Color sequence left→right is **blue → gold(yellow) → orange → red**, deliberately mirroring stellar spectral classification cooling down (O blue → M red) — an astronomy easter egg confirmed in Bethesda interviews.

```css
/* hard-stop gradient form — single element, zero markup */
.sf-bars{
  background:linear-gradient(90deg,
    var(--sf-navy)   0 25%,
    var(--sf-gold)   25% 50%,
    var(--sf-orange) 50% 75%,
    var(--sf-crimson) 75% 100%);
}
.sf-stripe-v{width:clamp(5px,.8vw,14px)}   /* vertical bar cluster — hero side */
.sf-stripe-h{height:clamp(4px,.6vw,8px)}   /* horizontal variant — structural bands */

/* flex form — when bars need individual widths/gaps */
.sf-flag{display:flex;gap:0} /* gap:2px for the spaced variant seen on merch */
.sf-flag > i{flex:1}
```

Note: the Constellation **circular badge** (navy disc + white star dots + warm semicircle arc) is a SEPARATE element from this stripe — don't conflate them.

**Optional display variant — white block, blue text**: in composed lockups (NOT inside the 4-bar rail itself), an `--sf-offwhite` block may sit to the RIGHT of a red block, carrying text set in stripe-blue (`--sf-navy`). Use for value chips, short labels, or a secondary headline word. Pairing law: always place it after/near red or a full stripe so the white reads as part of the sequence, never as a floating gray box. Recipe: `.sf-chip-white` in snippets.css.

Placement rules (restraint is the point):
- ONE prominent vertical bar-cluster beside the hero headline
- Thin 4–6px vertical accents on card/plate left edges
- ONE horizontal band under masthead or atop footer
- Small chip near mission patch
- Never more than ~4 stripe instances per page; never on dark instrument bands

Faction-livery variant (UC ship paint): white body with hard red/blue side bars — use as color-blocked panel headers sparingly.

### 5b. Motion system

| Pattern | Spec |
|---|---|
| Enter/open | `var(--dur-enter)` `var(--ease-out)` (200–300ms range) |
| Exit/close | `var(--dur-exit)` `var(--ease-in)` |
| List/card reveal | stagger items by `var(--stagger)` (20–40ms) |
| Badge shine | diagonal light-band ::after sweeping once on load + on hover (~900ms ease-out) |
| Scan reveal | thin gold line sweeping over blueprint line-art, slow loop (~7s), low opacity — orbital-scan read |
| Breathing attention | opacity loop `.55 → 1`, 2.5s `ease-in-out` (sine), infinite — the ONLY sanctioned attention loop (see MOTION TEMPO LAW) |
| Accessibility | ALL decorative motion inside `@media (prefers-reduced-motion: no-preference)` |

**MOTION TEMPO LAW (hard)**:
- Attention states BREATHE: 2.5s ease-in-out sine opacity loop, `.55 → 1`. They never blink
- Blinking or pulsing under 500ms is a HARD FAIL (also §10)
- Entrances/exits run 150-250ms ease-out; the §2 duration tokens remain canonical for the light mode
- Holographic / flicker / sci-fi glow effects are permitted in AT MOST ONE designated special zone per page (the SANCTIONED EXCEPTION ZONE); everything else stays flat vector. Name the zone in a comment before styling it

### 5c. Panel modernization

- Keep square corners and hard offset shadows (retro character) but LAYER a soft modern shadow first in the stack: `0 2px 10px rgba(32,35,42,.08)`
- Hover lifts use `var(--ease-out)` timing
- Dual-mode split is codified: LIGHT menus/pages + DARK instrument bands (telemetry/HUD widgets) — both exist, cleanly separated

### 5d. Interaction states (hover / press — required, not optional)

Every interactive element answers the pointer. Timing from micro-interaction standards: hover 150–200ms, press ≤150ms; animate transform/opacity only.

| Element | Hover | Press/`:active` |
|---|---|---|
| Nav link | text→red + 2px red bar sweeps in from left along baseline (`right:100%→0`) | n/a |
| Card/plate | lift −3px + soft shadow deepens (existing §5c) | settles to −1px — physical depression |
| List row / timeline item | 4px `--sf-crimson` left-edge marker slides in; marker dot scales 1.35 | n/a |
| Button/badge | background shifts one token step lighter | scale .97 or translateY +1px |
| Focus (keyboard) | global `outline:2px solid var(--red); offset:2px` — never remove | n/a |

Laws: states must remain readable with motion disabled (global reduced-motion kill-switch handles it); hover may REVEAL information but never MOVE text the user is reading; only ONE sweep animation per region — a page of everywhere-sweeping underlines is noise, not polish.

### 5e. Data visualization - technical-report figures

Charts are rendered as PRINTED REPORT FIGURES set into light figure plates - monochrome ink first, color only as accent. This mirrors actual 1960s-70s NASA TN/SP report figures (verified against NTRS primary sources). Recipes: `references/snippets.css` SS12e.

**Four-fill ladder (series encoding WITHOUT color):**
| Fill | Spec | Semantic |
|---|---|---|
| Outline | transparent fill, 1.5px `--ink` border | default series |
| Solid | `--ink` fill | emphasized / current value |
| 45-deg single hatch | 1px ink strokes @ 6px spacing, outlined | caution / secondary emphasis (may tint rust) |
| Cross-hatch | two crossing hatches, outlined | tertiary / limit envelope |

**Plot-area laws (from primary sources):**
- NO graph paper inside plots - plain face only; sparse DASHED reference lines when needed
- AXES DEFAULT OFF: do not draw X/Y axis lines unless the layout guarantees >=12px clearance from every label and bar - a fixed-position axis line crossing label lanes is the most frequent NASApunk-chart defect. Tick stubs alone (`.fig-ticks`) carry the scale; when axes ARE justified use the opt-in `.fig-plot--axed` modifier and re-run the collision scan
- Event flags: HOLLOW squares; dashed verticals mark events
- Caption strip inside plate bottom: `FIG. 2A - TITLE` letterspaced mono caps, hairline rule above
- Monochrome-first is authentic: era reports were 1-2 color prints (NHB 1430.2); red/rust reserved for emphasis

**Gauge state vocabulary (scoped to dials/meters only):**
- Range bands: muted aviation green `#3A8C3A` / amber `#E8B830` / brick `#C62828` - desaturated, painted-on-dial authenticity; page palette elsewhere unchanged
- Three-state flags (Apollo Experience Report): GRAY = operating/open, BLACK-WHITE STRIPED (`repeating-linear-gradient(45deg,#1A1A1A 0 4px,#F4F3EF 4px 8px)`) = deactivated/closed, RED = failed
- Annunciator tiles: sage frosted lens `linear-gradient(#CFD4CF,#A8B0A8)` + olive bezel `#85857F`, lit amber `#E39A2F`; green `#4FC04F` permitted ONLY inside annunciator rows (restored-MOCR evidence)

**Instrument hierarchy**: the THREE-RING INSTRUMENT (§5g) supersedes the plain dial gauge for HERO instruments (FIG. 9E, Band 14); keep the plain dial for dense multi-gauge arrays.

### 5f. Figure sheets (charts as printed document inserts)

One figure per sheet; present 3-up exactly like the spec-plates section - but the sheets must NOT reuse the metal-plate shell (avoid section homogeneity). Instead each chart sits on a **report-figure sheet**: bone paper, thin ink frame, graph-grid texture, FIG tab notch breaking the top border, crop marks outside two corners, caption below.

Construction:
1. `.fig-sheet`: bone `#FBFAF7` + dual-scale light grid (22px) + 1px ink border; padding reserves a top band for the tab
2. `.fig-tab`: FIG id chip breaking the top border (background matches sheet so the border reads "interrupted")
3. `.sheet-head`: mono caps title left / qualifier right, above the plot
4. `.fig-plot`: L-axes + ticks per §5e; modifiers: `--hbar` drops the Y axis (horizontal charts own that lane for labels), `--bare` drops axes entirely (dial plates)
5. `.sheet-cap`: letterspaced mono caption below the plot
6. Optional annunciator tile row (max 4) under one sheet per section
Laws: one chart type per sheet; values plausible + consistent across sheets; ink-on-paper only (no backlight/glow).
Live example: Section 02 in `assets/reference.html`. Recipes: `references/snippets.css` SS12e/SS12f.

### 5g. Component grammar (console/HUD vocabulary)

Named components of the console/instrument vocabulary (deployed per §0B deployment laws). Each is a closed construction: build it as specified, do not improvise variants except through the faction skin system.

- **SCANNER MONOCLE VIEWER**: circular reticle + horizon line + vignette inside the lens. Unscanned state = cyan outline only; scanned state = solid fill. A flat survey card docks LEFT of the monocle, never overlapping it
- **STARMAP PANEL**: concentric orbit rings + one dotted ellipse + double-ring planet nodes; info card docked left of the ring system
- **LEADER-LINE CALLOUT**: 1px line + terminal dot connecting a label card to its target; same lane-separation laws as §4.5 rule 9
- **STATUS CHIP TRIAD**: green/amber/red state chips (console-mode extension of the §5e gauge vocabulary to chip scale) plus the rarity trio `#73CCDF` / `#9A7BFF` / `#EEC162`; chips carry status ONLY, never decoration
- **HERITAGE SERIF LAYER**: gold `#D4A94A` serif headlines on deep ground + an eight-point compass-rose SVG mark; reserved for fictional heritage brands ONLY (§8: never real insignia, never Starfield's actual marks)
- **FACTION SKIN SYSTEM**: ONE neutral geometry + N paint packs (e.g. EXPLORER / MILITARY / CORPORATE / FRONTIER). Same geometry, different livery tokens; NEVER redraw geometry per faction
- **ROUNDEL CONSTRUCTION FORMULA**: faction/corp badge in four zones: outer inscription ring (curved `textPath`: org name + est. year) + upper field (star cluster or glyph) + lower semicircle band split into 2-3 color arcs (gold/orange/red family) + center core glyph. Annotate the zones when presenting the badge. All branding fictional per §8; zone grammar descends from worm-era graphics standards (1976-92) used as stylistic reference window. Reference: `assets/reference.html` FIG. 9D; recipe: `references/snippets.css` Band 14
- **ROUNDEL CONCENTRIC LAW**: every zone circle/arc in a roundel/badge shares ONE center - verify with `scripts/icon-geometry-check.js` (arc-center reconstruction catches off-axis bands eyeballing misses). A band tip crossing the field boundary is a HARD FAIL.
- **WAYFINDING SIGN**: navy-ground plate, white text: large letter-code station ID + station name + arrow rows with district codes + corner map thumbnail. This is the SANCTIONED EXCEPTION where a solid navy ground replaces cream; every other surface stays light-dominant (§10). Reference: `assets/reference.html` FIG. 9G; recipe: `references/snippets.css` Band 14
- **THREE-RING INSTRUMENT**: dial upgrade: outer ring = function ticks/icons, middle ring = percentage arc + needle, inner circle = date/time/status line. Replaces the single-ring gauge whenever an "instrument cluster" feel is requested. Spec lineage: Chronomark watch FCC filing. Reference: `assets/reference.html` FIG. 9E; recipe: `references/snippets.css` Band 14. DIAL GEOMETRY LAW: value-arc endpoints must be typed ON the dominant center - both endpoints exactly at ring radius (a single mistyped coordinate drifts the entire sweep off-axis; caught by `scripts/icon-geometry-check.js` single-arc rule). The needle tip must reach the ring-track inner edge, never float short of its scale.

---

### 5h. Interface component gallery (ten standard patterns - DEFAULT VOCABULARY)

Ten complete, interaction-ready page patterns. **Selection is driven by STRUCTURE, not keywords**: inspect what the page (or request) actually contains - lists, cards, meters, forms, maps, dialogs, logs, tables - and apply the matching pattern. The game flavor in the names is optional paint; the grammar below fits ANY domain (e-commerce, CMS, SaaS admin, portfolio, docs, blog...).

| # | Pattern | Apply to ANY UI containing... |
|---|---|---|
| G1 | Data Menu trio | a category sidebar + item list + detail card: admin panels, product/CMS/file managers, inventories, libraries, mail clients, dashboards |
| G2 | Terminal | command consoles, log viewers, CLI-flavored sections, system status readouts; any diegetic terminal block |
| G3 | Power allocation | any shared-pool allocation widget: storage quotas, budget splits, load distribution, skill-point spenders, progress pools |
| G4 | Starmap panel | node-and-link graphics: maps, org charts, relationship/network graphs, flowcharts, location pickers |
| G5 | Mission board | task/job/ticket/quest/announcement listings, TODO boards, application queues |
| G6 | Settings form | preference/config pages, any toggle+slider+select control cluster |
| G7 | Modal confirm | confirmations, destructive-action warnings, hazard dialogs |
| G8 | Credits roll | about/team/acknowledgment sections, end matter, changelog closers |
| G9 | Reading page | articles, documentation entries, book chapters, help centers - any long-form reading surface |
| G10 | Item inspect card | product/profile/item detail cards: stats, delta-vs-comparison values, mini meters, brand slot |

Laws: one pattern per section; compose up to 3-4 per page; every pattern inherits Bands 1-14 base laws unchanged; interactions are vanilla JS; live implementations render in `assets/reference.html` SECTION 07 (FIG. G1-G10); recipes in `references/snippets.css` BAND 15.

**COMPOSITE SIGNATURE (candidate, not mandate)**: a G-pattern fires when its signature atoms co-occur on one screen - but the detection output is a CANDIDATE with confidence, never a forced command. Agent verifies before composing. Signatures live in `references/component-matrix.md` M-G sections.

**DUAL-CHANNEL DETECTION (G1 data-menu, G9 reading, M-IMG images)**: these patterns fire via TWO independent channels, kept deliberately parallel:
- Channel A — SCRIPTED: `refactor-inventory.js` detects structural signals and emits candidates — G1 via `data-menu-trio` (rail+list+detail in one pane) or counting signature; G9 via `long-form-prose` (≥5 non-list paragraphs, ≥300 chars, outside card/table/form); M-IMG via `img-photo`/`carousel` atoms (any photo image or carousel → `IMG?`, plus `img-avatar`/`img-gallery` role hints).
- Channel B — AGENT/MANUAL: the agent judges scenes per the §5h table and M-IMG grammar, independent of any script signal — G1 on any category-rail+list+detail screen (including framework three-pane compositions the script cannot see), G9 on any long-form reading surface, M-IMG on any image-bearing surface (banner, long figure, carousel, avatar, gallery, inline figure, thumbnails) including framework image components the regex cannot see.
Either channel alone may raise a candidate; the agent confirms the scene/role before composing. Keep BOTH channels — never replace one with the other: scripted detection catches repeatable structure the eye may skip, manual judgment catches framework containers the regex cannot see.

### 5i. Image presentation grammar (photo/image layout — M-IMG)

Image-rich pages (nasa.gov-style: banners, long figure shots, carousels, portraits, galleries, inline figure photos) must map EVERY image to the NASApunk image-presentation grammar — never a plain embed. Full per-role table + stack mappings + verification in `references/component-matrix.md` M-IMG; live implementations in `assets/reference.html` FIG. 14A-14H. Rules:

1. **Framing**: every photo sits in an ink 1px frame with corner crop marks (L-marks outside two corners). No rounded frames (crop marks need square corners) — portraits included.
2. **Captions**: every image gets a FIG plate — mono `FIG. N-M` id (red) + title + credit; preserve the `figcaption` element for a11y and re-skin it.
3. **Role grammar** (per M-IMG table): banner = full-bleed + caption slab (red/ink, contrast-checked) over dark image area; long figure = ink frame + binding rail + fold ticks; carousel = framed + mono index chips `01/04` + square arrow buttons (no animated dots); avatar = square frame + initials chip fallback (navy fill, mono caps); gallery = equal-width cells each with own FIG chip + own caption; inline figure = float left/right max-width 45% + 16px gutter; thumbnails = small square frames + mono indices; loading/error = hatch placeholder + "LOADING"/"NO DATA" stencil, breathe 2.5s (never blink).
4. **Zero image/text occlusion**: figure gutters ≥ 12px; caption bars never overlap image pixels; overlaid headline slabs contrast-checked; inline figures keep body copy clear.
5. **Zero external requests**: no external image sources — inline SVG/data-URI placeholders, or the original image inlined; framework image components (`el-image`, `next/image`) wrapped with frame classes.
6. **Data preservation (SAFETY LAW #2)**: original `src`, dimensions, `alt`, and caption TEXT are never altered — only the frame/chrome/caption STYLE changes.

**PRIORITY & DISAMBIGUATION (advisory)**: when one screen matches several composites - charts >= 3 -> M-DASH first; sidebar+list+detail -> G1; confirm-dialog present -> G7 always wins for that dialog; ambiguity unresolved -> present the shortlist to the user, never blind-pick.

**OPTIONAL SCENE PATTERNS**: G2 (Terminal), G3 (Power allocation), G8 (Credits roll) are scene-optional: they compose ONLY when the scene genuinely matches (log viewer / allocation widget / acknowledgments reel). They are never forced, and their absence from a page is a correct outcome, not a coverage miss.

**SAFETY LAW (hard, all refactors)**:
1. LAYERED IRREVERSIBILITY: L1 token/color layer = always safe & reversible. L2 structural layer = allowed ONLY while the framework behavior contract is preserved (sorting, validation, pagination, v-model bindings, ARIA). L3 dataviz = option-object changes only, never swap rendering engines.
2. SKIN NEVER TOUCHES LOGIC: data flow, validation, accessibility, and framework contract stay byte-identical. A pattern that requires DOM replacement of a behavior-bearing component is implemented as deep-selector overrides instead.
3. COMPOSITE CANDIDATES NEED AGENT CONFIRMATION: never blind-compose on signature count alone.
4. COVERAGE GATE CHECKS BEHAVIOR PRESERVATION: transformation evidence = computed-style assertion AND original event bindings/methods still usable - not just "style changed".
5. REVERSIBLE BY DEFAULT: every transformed screen must be revertible by removing the injected skin layer (no baked-in data mutations).

**REFACTOR LAW (whole-project application)**: when restyling an EXISTING frontend, this skill applies IN FULL - there is no partial mode. Procedure: (1) structurally inventory the target (nav / lists / cards / forms / tables / modals / footers / logos); (2) map every structure to its gallery pattern and texture set; (3) re-skin everything with §2 tokens + §4 textures + motion tempo unconditionally - footers become colophons, settings become instrument panels, lists become mission boards or hatched report bars, modals gain hazard headers, empty states gain doodles, data views become report figures. Keyword absence never blocks a transformation; structure presence always demands one.
Keyword absence never blocks a transformation; structure presence always demands one.

**COVERAGE MATRIX - "in full" means every layer below, not just the gallery:**

| Skill layer | In refactor? | Condition |
|---|---|---|
| §2 Light tokens + all texture recipes | ALWAYS | base skin |
| §2B Console tokens | ALWAYS AVAILABLE | auto-deploy onto instrument-shaped scenes; full-page console on explicit dark request |
| §2C Era grades | PART OF BASE SKIN | mechanism always available; apply a grade when scene warrants (commemorative/heritage), default none |
| §3 Typography laws | ALWAYS | headings/labels/body/table rules |
| §4 Every texture recipe (paint/stamps/rivets/screws/hazard/blueprint/doodles/vignette/warm-cool) | ALWAYS | mapped to matching structures |
| §5a Emblem stripes | ALWAYS | masthead/frame accents |
| §5b Motion tempo + §5d Interaction states | ALWAYS | breathe loops, hover sweep, press feedback, focus rings |
| §5c Panel modernization | ALWAYS | soft shadow under hard offset |
| §5e Chart grammar (four-fill ladder / dial / flags / annunciators) | WHEREVER data display exists | dashboards, stats, progress |
| §5f Figure sheets | WHEREVER figures/cards are needed | detail inserts |
| §5g Component grammar (roundel / wayfinding / three-ring / monocle / starmap / chips / faction skins / heritage serif) | WHEREVER matching structure exists | identity, navigation, instruments |
| §5h Gallery patterns G1-G10 | WHEREVER matching structure exists | ten composite layouts |
| §6 Persistent frame (docbar/masthead/footer) + §7 Voice registers | ALWAYS | frame and copy voice |

§5h is the newest addition, not the boundary: every section above carries equal weight during a refactor.
---

## 6. PAGE ARCHITECTURE (canonical sections — pick 4+, keep order logic)

1. **Doc-control bar** (top) — document number, revision, form code, effective date
2. **Masthead** — wordmark styled after the worm-era graphics standards (1976-92) used as stylistic reference window (see §8 legal) + fictional agency name + numbered nav (`01/02/03`); optional horizontal emblem band under its border
3. **Hero** — huge two-line headline with color blocking (e.g. "HIGH TECH." / "HIGH HOPE." second line on red block), meta strip in mono, mission patch badge, optional Kapton rail on right edge, ONE vertical emblem stripe beside the headline
4. **Telemetry band** — fake live-updating mono readouts (~20 lines vanilla JS random-walk), GO/CAUTION status lamps
5. **Spec plates ×3** — painted-metal cards with rivets: hardware names ("CMG GYRO ASSEMBLY"), part numbers in red, mono spec tables; one carries hazard stripe + "NO USER SERVICEABLE PARTS INSIDE"
6. **Blueprint section** (navy) — inline-SVG line-art station/module, dashed leader-line annotations, dimension line, revision cloud, title block, corner registration crosses
7. **Timeline** — horizontal rule, diamond markers alternating red/navy, years in mono (1961→1981 era); collapses to vertical rail on mobile
8. **Footer** — fine print, document references, "PRINTED BY THE UNITED STATES GOVERNMENT PRINTING OFFICE • 1979" colophon
9. **Magazine cover hero**: masthead + issue tag + illustration window + cover lines + barcode/GPO strip; fictional serial publications only (FIG. 9A, Band 14)
10. **Official document/memo**: roundel letterhead + classification stamp + meta grid (DATE/REF/TO/FROM/SUBJECT with dotted leaders) + body + embedded figure WITH caption + signature line (FIG. 9B, Band 14; lineage: UC dispatch memos)
11. **Reading page**: chapter header + ornamental divider + drop cap + two-column body + pagination arrows with page counter, including a shown disabled state (FIG. 9C, Band 14; lineage: in-game BookMenu skeleton)

**PRINT-DOCUMENT AUTO-SELECTION LAW**: items 9-11 (with §5g roundel / wayfinding / three-ring) are core vocabulary, not appendix patterns. Two integration depths: (a) STYLE LEVEL - the Band-14 prop/voice/typography grammar ships in EVERY PRINT build by default (§0B); (b) LAYOUT LEVEL - when the requested artifact belongs to one of these genres, the matching pattern IS the default page layout:

| User asks for | Default pattern |
|---|---|
| magazine / editorial / journal cover | 9 - Magazine cover hero |
| memo / dispatch / official letter / announcement | 10 - Official document |
| article body / book chapter / long-form reading | 11 - Reading page |
| exhibition / retropective wall | Timeline variant - museum exhibit band |
| station / district signage | §5g - Wayfinding sign |
| org badge / heritage emblem | §5g - Roundel formula + Heritage serif layer |

Genre pages combine freely with the persistent frame (doc-control bar, masthead, footer stay); telemetry/spec-plates/blueprint sections join only when the genre calls for data. Plates FIG. 9A-9G render in `assets/reference.html` (Section 06 // Documents & Insignia); "Band 14" = copy-paste recipes in `references/snippets.css`.

**Timeline variant (museum exhibit band)**: swap diamond markers for numbered wall-label panels; each panel = EXH no. + kicker + year range + one-line lead (FIG. 9F, Band 14)

Layout: visible Swiss grid, generous whitespace, hairline rules between sections, desktop-first responsive.

**Console-mode section set** (deploy when the scene fits an instrument-shaped page - terminals/dashboards/status walls - or on explicit request; tokens per §2B, components per §5g):

1. **Console panel system** — flat alpha `--panel-base` panels (~55-66% opacity) with brushed-metal bevels (§4); replaces spec plates
2. **Scanner viewer** — SCANNER MONOCLE VIEWER + survey card; replaces the blueprint section
3. **Starmap** — STARMAP PANEL with orbit rings and planet nodes; replaces the timeline
4. **Status band** — STATUS CHIP TRIAD row + mono readouts in `--screen-glow`; replaces the telemetry band

These may replace their print equivalents while keeping the section-order logic (docbar → masthead → hero → data bands → footer). Doc-control bar, masthead, hero, and footer persist in both modes.

---

## 7. COPY VOICE

- Fictional agency (e.g. "National Aeronautics Program") — NEVER real NASA branding (§8)
- Real-sounding doc metadata: `DOC NO. NAP-71-C • REV C • EFFECTIVE 02 MAR 1979`
- Part numbers, inspection stamps (`INSPECTED № 4471`), spec values with units
- Tone: dry institutional confidence, quiet optimism. Slogans of the form "X. Y." ("HIGH TECH. HIGH HOPE.")
- Write REAL fictional copy — never lorem ipsum
- No emoji anywhere; icons = inline SVG line art (stroke `--metal-dark`)

**Brand voice samples** (three registers drawn from documented in-game branding; every sample brand fictional):
- **PLAIN-SPOKEN UTILITY**: product-first, wry, zero adjective padding. "They're trucks! In space." energy: name the object, state what it does, stop
- **INSTITUTIONAL OPTIMISM**: recruitment register, imperative mood + horizon verbs. "Join the survey corps. Map what nobody named."
- **HERITAGE GRAVITAS**: est. years + mottos in an engraved tone. "Est. 2188. For all into the starfield."

---

## 8. LEGAL (hard constraint)

NASA insignia ("meatball") and worm logotype are protected under **14 CFR Part 1221** and the Space Act — not public domain, commercial use requires authorization.
→ Always build an **inspired-by fictional wordmark**: thick rounded lowercase geometric lettering in signal red, single-stroke widths, crossbar-less A's (SVG paths or styled text). Never reproduce the actual logos.

---

## 9. WORKFLOW (execute in order)

1. Scaffold single self-contained HTML file (embedded CSS, minimal vanilla JS optional) — create output dir first
1b. STYLE STATEMENT (§0B): BASE SKIN applies automatically - state it and plan §6 Band-15 artifacts (≥2). Switch to CONSOLE only if the user explicitly requested dark/terminal mode
2. Paste `:root` tokens + noise/grunge data-URIs (§2; add §2B console block only in CONSOLE style)
3. Build skeleton: docbar → masthead → hero → content sections → footer (§6), strict left-aligned grid, hairline section rules
4. Apply textures per §4 — start with body worn-paint, then plates/rivets, then ONE Kapton element, then stamps/blueprint
5. Typography pass: headings vs stencil labels per §3
6. Copy pass per §7
7. Starfield-modern pass per §5 — emblem stripes, motion tokens, soft shadows, reduced-motion guard
8. Self-check against §10 anti-patterns + §11 checklist
9. Run `scripts/collision-check.js` (paste into DevTools console or any headless browser): it Range-scans every text node against graphics and other text - required hits: 0 (range-rect line-box artifacts on multiline headings excepted if glyph gap is provably positive)
9b. Run `scripts/icon-geometry-check.js` (inject via DevTools/Playwright): HIGH findings = 0 - fix drifted badge/ring/dial geometry before delivery
10. Visual acceptance: screenshot changed regions and verify through a vision-capable agent (multimodal-looker) - any FAIL loops back to the fix
11. Verify zero external requests: `grep -oE 'https?://[^"' )]+' file.html` → only `www.w3.org/2000/svg` namespaces allowed

REFACTOR PROTOCOL (mandatory sequence):

- **R0 FINGERPRINT**: run stack fingerprinting per `references/component-matrix.md` M-0; load only matching M-x sections. When `stacks detected: none` (plain HTML/vanilla JS), load **M-NATIVE** (vanilla HTML + JS API mappings) alongside M-FRAME/M-HERO/M-TL/M-HW/M-CS/M-DOC/M-G* — native elements are first-class atoms, not unmapped fallbacks
- **R1 INVENTORY**: run `scripts/refactor-inventory.js <target>` - emit the atom-census ledger (work order AND coverage baseline); ledger MUST include native atoms (dialog+showModal, alert/confirm, window.open, innerHTML updates, onclick/oninput/onsubmit, range/checkbox/radio/select, title tooltips, canvas, progress, form validation, fetch/XHR/localStorage data layer) per M-NATIVE
- **R2 MAPPING**: translate every ledgered atom through the loaded matrix sections (M-A/M-B/M-R/M-SH/M-NATIVE/...); unmapped atoms fall back to M-A and are logged; native JS behavior APIs map to VISUAL treatments while their behavior contract is preserved verbatim (SAFETY LAW #2)
- **R3 EXECUTION** in three mandatory layers, all required: L1 token/theme injection -> L2 component structural restyle (template edits or deep-selector overrides) -> L3 dataviz theme objects (chart libraries are immune to CSS). **DELEGATION CONTRACT (when a sub-agent executes)**: (a) the refactored artifact must be WRITTEN TO DISK BEFORE any report — write-first, report-after; (b) the final report MUST include artifact path + line count + evidence grep (key classes/behaviors present) + which R4/R5 checks passed; (c) the delegating agent MUST verify the file exists on disk before accepting "done" — a completion report without an on-disk artifact is NOT completion; (d) keep task prompts under the executor's output budget (split into section-batches if needed) so the write step is never truncated away
- **R4 COVERAGE GATE**: re-run the inventory on the refactored output; every ledgered atom must show transformation evidence (diff marker / computed-style assertion); coverage < 100% without logged exemption = NOT DELIVERED
- **R5 VISUAL ACCEPTANCE**: screenshot every screen; verify through a vision-capable agent against §4.4 zero-overlap + this skill's laws
- Keep the target's DOM/content and data logic; do not delete user content

---

## 10. ANTI-PATTERNS (hard blocks — instant fail)

- ❌ Neon glow, cyan/purple gradients, glassmorphism, holographic UI
- ❌ Dark-mode-dominant layout (page is LIGHT/paint-white dominant; dark exists only as instrument bands + blueprint section)
- ❌ Pastel colors (banned by NHB 1430.2) — the `--sf-*` earthy accents are muted but NOT pastel; keep them on small accent surfaces only
- ❌ External assets of any kind: CDN fonts, frameworks, images, icon libraries — system stacks + inline SVG/data-URIs only
- ❌ Emoji icons
- ❌ Actual NASA logos/insignia verbatim (§8); also never redraw Starfield's actual logo/emblem — four-color stripes are generic enough, the constellation starburst logo is not
- ❌ Lorem ipsum / placeholder copy
- ❌ CSS frameworks (Tailwind etc.), build tooling
- ❌ Site-wide CRT scanlines / heavy global effects (confine CRT to telemetry widget)
- ❌ Decay aesthetics: broken glass, rust-holes, abandonment — worn ≠ ruined
- ❌ Stripe spam: >4 emblem stripes per page, or stripes on dark instrument bands
- GLOBAL GREY WASH: never desaturate the whole palette; keep the warm-cool balance (§2B, §4 warm-cool split light)
- DECORATIVE AMBER: amber outside alert/action/interactive contexts violates the SEMANTIC AXIS (§2B)
- SUB-500MS BLINKING: any blink/pulse loop under 500ms (§5b MOTION TEMPO LAW)
- FORM-OVER-FUNCTION HIERARCHY: body text on dark must meet WCAG AA; the focal point is actionable data, never decoration
- SINGLE-TEMPLATE REPETITION: composing multiple similar blocks without variants is a fail; vary livery tokens per the faction skin system (§5g)
- DECORATIVE INSIGNIA SPRAWL: roundels/emblems repeated beyond masthead + footer without a content reason; the §5g roundel is identity hardware, not wallpaper
- UNIFORM PANEL MONOTONY: exhibit-band wall labels at one identical rhythm is a fail; vary panel widths and lead lengths (§6 museum exhibit band)

---

## 11. VERIFICATION CHECKLIST (before reporting done)

- [ ] Palette matches §2 tokens exactly (grep the hexes)
- [ ] Light paint-white dominant; red used sparingly as signal; gold on ≤2 hero elements
- [ ] Headings uppercase tight-tracking Helvetica; labels mono wide-tracking; flush-left ragged-right
- [ ] ≥1 rubber stamp, ≥1 rivet row, ≥1 hazard or blueprint texture present
- [ ] Starfield layer: emblem stripes present (≤4, light surfaces only), soft shadow layered under hard shadows, motion tokens used
- [ ] Charts (if present): segmented fills, three-tier state colors (white/orange/red, no green), framed in instrument panels, labels mono caps
- [ ] `prefers-reduced-motion` guard present for decorative animation
- [ ] Zero external URLs (only w3.org SVG namespaces)
- [ ] All copy real fictional content with doc-metadata flavor
- [ ] Responsive: grids collapse cleanly ≤720px (timeline → vertical rail)
- [ ] Tag balance + brace balance verified if no LSP available
- [ ] Base skin applied automatically without asking; era grade used only when scene warranted (§0B)
- [ ] Dark instrument surfaces deployed only on instrument-shaped scenes (or explicit dark request); body/reading surfaces stay light (§0B)
- [ ] PRINT builds weave ≥2 Band-14 document artifacts without being asked (§6)
- [ ] Era grade applied only when requested; one grade per page, token-level tints (§2C)
- [ ] Prop-font layer confined to body/document contexts; never mastheads or display settings (§3)
- [ ] Roundels follow the four-zone formula: inscription ring, field, arc band, core (§5g)
- [ ] Embedded figures always carry captions (§6)
- [ ] Reading pages expose both enabled and disabled pagination states (§6)

Console-mode gate (run ONLY when console mode is active):
- [ ] SEMANTIC AXIS respected: cyan = passive data only, amber = alerts/actions/interactive only
- [ ] Bevel insets present on dark panels (brushed-metal bevel, §4)
- [ ] Breathing vignette applied behind heroes / empty states
- [ ] `scanCollisions()` realHits = 0 in BOTH modes (print + console)
- [ ] Motion tempo compliant: 2.5s breathing attention loops, nothing under 500ms, at most one sanctioned exception zone (§5b)

## FILES IN THIS SKILL

| File | Use |
|---|---|
| `references/component-matrix.md` | Multi-stack refactor translation: stack fingerprinting, 9-stack component mappings (M-A..M-F), chart themes, cross-cutting laws |
| `references/snippets.css` | Copy-paste recipes for every §4 + §5 effect |
| `scripts/collision-check.js` | Zero-overlap auditor: Range-scans text vs text/graphics; run in DevTools console or headless browser (§9 step 9) |
| `scripts/icon-geometry-check.js` | SVG concentricity auditor: arc-center reconstruction + drift detection for badges/roundels/gauges (§5g) |
| `scripts/gallery-coverage.js` | Gallery x stack coverage gate: 10 patterns x 7 stacks = 70 rows must be YES (REFACTOR R2) |
| `scripts/refactor-inventory.js` | Stack fingerprinting + UI-atom census ledger (REFACTOR step R1; also the coverage-gate baseline) |
| `assets/reference.html` | Full working baseline page — NASApunk × Starfield-modern, zero deps — open in browser, or mine it for section markup |

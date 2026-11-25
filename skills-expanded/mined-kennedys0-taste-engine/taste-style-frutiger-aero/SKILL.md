---
name: taste-style-frutiger-aero
description: Apply Frutiger Aero design style to user-selected frontend and UI work. Use only when the user explicitly chooses this style. Provides typography, color, layout, components, interactions, motion, copy and quality gates. Do not impose on unrelated work.
license: MIT
metadata:
  version: "0.13.1"
---

Use this skill only after a user explicitly chooses frutiger-aero or a confirmed project configuration specifies it. For unexplained new UI requests, use a style selector such as taste-engine instead of deciding the user's taste here. Existing brand, accessibility and user overrides outrank all examples below. The following style guide is not permission to start UI coding before style selection.

# Style pack: Frutiger Aero

**ID:** `frutiger-aero`  
**Signature:** "Optimistic computing under a clear blue digital sky" — mid-2000s technological optimism fusing **Glassmorphism** (refractive translucency, layered floating panes, luminous edge lighting) and **Skeuomorphism** (molded glossy acrylic surfaces, convex tactile push-buttons, physical inset wells, and light-accurate surface depth) within a fresh sky, aqua, seafoam, and spring-leaf atmosphere.

> This is a **style pack, not a mandatory default**. Load it only after explicit selection or confirmed applicable project style. Project instructions can override individual choices. Preserve accessibility, utility, and brand constraints. A generic frosted SaaS card on a flat blue page or a plain Bootstrap/MUI gradient pill button **does not qualify as Frutiger Aero**.

## Good fit / trade-offs

- **Works well for:** Optimistic technology platforms, creative tools, productivity apps, media suites, environmental and eco-tech platforms, personal portfolios, and tactile interactive web applications.
- **Use with care for:** Austere legal registries, ultra-dense monochrome developer tools, or minimalist black-and-white editorial publications.
- **Core Visual Concept — "Optimistic computing under a clear blue digital sky":**
  - Merges **Glassmorphism** (translucency, backdrop blur where appropriate, soft luminous layering, floating refractive panels) and **Skeuomorphism** (physical affordance, believable surface thickness, molded glossy acrylic controls, raised and inset states, light-based realism) into one intentional, native material language.
- **Reference directions (3 Native Expressions):**
  - *Classic Aero (Default):* Best-balanced expression combining luminous sky/aqua/seafoam atmosphere, translucent aero glass panels with top-half horizon sheens, molded glossy aqua acrylic buttons, eco-tech leaf freshness, and a glossy translucent orb & layered horizon centerpiece.
  - *Aero Glass:* Stronger translucent crystalline layering (`blur(24px) saturate(180%)`), multi-plane floating panel depth, dual-rim luminous glass borders, lighter floating feel, and a layered crystalline glass lens cluster centerpiece — while remaining unmistakably Frutiger Aero rather than generic SaaS blur.
  - *Aero Tactile:* Stronger molded physical controls, contoured acrylic panel housings, deeper button bevels and recessed wells, tangible surface thickness, and a molded physical aqua rotary & switch deck centerpiece — while remaining bright, clean, and optimistic.

## Frutiger Aero material fidelity gate — mandatory

**Before calling a Frutiger Aero page complete, the opening viewport must visibly read as an authentic fusion of Aero Glass clarity and tactile glossy acrylic physicality.** If a user chose this style, a flat pastel SaaS page with plain white stat rectangles, weak transparency, or flat gradient pill buttons is a **FAIL**, even if CSS classes contain `aero`.

A successful Frutiger Aero implementation demonstrates **all** of the following:

1. **Three-Part Aero Material Vocabulary (Glass + Glossy Acrylic + Tactile Depth):**
   - **Aero Glass Surfaces (`.taste-aero-glass-surface`):** Translucent fills with controlled refraction (`backdrop-filter: blur(18px) saturate(160%)`), thin luminous outer and inner edge highlights, top horizon reflection sheen, and cool volumetric drop shadows (`rgba(58, 105, 141, 0.18)`).
   - **Molded Glossy Acrylic Surfaces (`.taste-aero-acrylic-surface`):** Smooth aqua/sky/cloud color transitions, curved top-light specular dome (`linear-gradient(180deg, rgba(255, 255, 255, 0.78) 0%, rgba(255, 255, 255, 0.22) 48%, rgba(255, 255, 255, 0) 51%, rgba(108, 209, 232, 0.18) 100%)`), internal bottom bounce sheen, and contoured physical edges.
   - **Tactile Skeuomorphic Depth (`.taste-aero-tactile-surface` & `.taste-aero-inset-well`):** Raised molded surfaces paired with recessed inset wells (`box-shadow: inset 0 2px 5px rgba(31, 93, 135, 0.18), 0 1px 0 rgba(255, 255, 255, 0.95)`) that give controls, segmented switchers, and telemetry modules real physical thickness.
2. **Tactile Molded Button System (Primary, Secondary & Pressed States):**
   - **Primary Button:** Molded aqua-ocean acrylic with a distinct top specular highlight dome, deep ocean lower contour for ≥ 4.5:1 white-text contrast, inner rim highlight, bottom aqua bounce light, and physical press travel.
   - **Secondary Button:** Translucent cloud-glass & pearl-acrylic body with a physical contour border, subtle top gloss band, bottom bevel thickness, and high-contrast deep blue typography (`#173F61` / `#1F5D87`).
   - **Pressed State (`:active`):** Visible downward travel (`transform: translateY(2px)`), external shadow compression, reduced top specular highlight, and inset top bevel shadow (`inset 0 3px 6px rgba(11, 35, 54, 0.42)`).
3. **Atmospheric Hero with Material-Led Visual Centerpiece:** The hero must never rely on plain centered text over 4 white KPI boxes. It must feature a controlled sky/aqua/seafoam horizon atmosphere and a material-led focal centerpiece (glossy translucent aqua orb, layered glass lens cluster, or molded acrylic control plate) that demonstrates Frutiger Aero visually even if the user ignores the paragraph text.
4. **Deep Variant Differentiation:** Switching between `Classic Aero`, `Aero Glass`, and `Aero Tactile` must transform panel translucency, specular highlight intensity, button molding, surface bevel thickness, and hero centerpiece geometry — not merely swap an accent color.
5. **Anti-Clash Text Contrast (WCAG AA 4.5:1):** Crisp deep ocean navy or charcoal typography (`#173F61`, `#1F5D87`, or `#243642`) over bright sky, cloud, and aqua glass surfaces in light mode; crisp porcelain cloud (`#F7FBFD` or `#F4FAFC`) over deep ocean glass in dark mode.
6. **Zero Generic QA Boast Badges & Graceful Fallbacks:** Do not clutter the hero with self-congratulatory engineering pills (*"WCAG AA Contrast"*, *"Zero AI-Slop"*, *"320px Zero Mobile Overflow"*). Provide solid background fallbacks when `backdrop-filter` is unsupported or `prefers-reduced-transparency: reduce` is active.

**First-viewport test:** In a desktop screenshot, identify the luminous digital sky atmosphere, the sculptural glossy orb/glass centerpiece, the molded tactile aqua and glass buttons, and the layered refractive panels **without reading the page title**. If it looks like "clean soft minimal SaaS UI" or flat blue with white cards, rebuild the material depth, specular highlights, and button physicality.

## Explicit Frutiger Aero material exception — gloss and nature gradients are allowed

**Frutiger Aero-specific override:** The universal anti-slop caution against *decorative gradients, glossy highlights, skeuomorphic bevels, or atmospheric backdrops* MUST NOT be interpreted as a ban on multi-stop sky/ocean/seafoam gradients, acrylic horizon sheens, molded tactile buttons, or translucent dock panels here. These are **material-enabling properties**, essential to fusing Glassmorphism and Skeuomorphism into an authentic mid-2000s optimistic interface.

- **Allowed material treatments:** Multi-stop aqua/sky/seafoam/leaf linear and radial gradients, top-half horizon reflection sheens (`linear-gradient` with 48%–50% specular split), molded convex tactile button caps, recessed inset control wells, translucent floating dock containers, and sculptural SVG orb/lens centerpieces.
- **Harmonious color rules:** Restrict palettes to optimistic eco-tech harmonies (sky `#DCEFF8` / `#C9EDF8`, cloud `#F7FBFD` / `#F4FAFC`, aqua `#6CD1E8` / `#48BFD3`, ocean `#2C90B8` / `#247EA3`, seafoam `#A7E6D5`, leaf `#79C67A` / `#70B981`, and deep blue `#1F5D87` / `#173F61`). Avoid discordant cyberpunk neon purple/pink clashes.
- **Anti-slop boundary:** Every control must be interactive, accessible, and functional. Do not decorate screens with noisy wallpaper clutter, fake animated fish, fabricated telemetry boasts, self-congratulatory QA badges in the hero, or unreadable white text on pale glass.
- **Anti-slop interpretation:** Evaluate Aero details by **material authenticity, Glass+Skeuo fusion, coherent top-lit lighting direction, and functional legibility**, not by counting gradient color-stops. Flattening molded buttons or removing horizon sheens to satisfy a generic flat heuristic is a **severe design regression**.

## Typography and typewriting

Use approachable, open humanist or modern sans-serif typography integrated into the luminous material world:
- **Primary Typefaces:** Plus Jakarta Sans, Segoe UI, Frutiger, Trebuchet MS, Inter, or clean humanist system sans-serif.
- **Display Headings:** Bold to extrabold humanist sans (`700–800` weight, `clamp(2.1rem, 4.8vw, 3.65rem)`) with clean tracking (`letter-spacing: -0.02em`), crisp deep ocean contrast (`#11324D` / `#173F61` in light mode, `#F7FBFD` in dark mode), and subtle top-light separation (`text-shadow: 0 1px 0 rgba(255, 255, 255, 0.8)` on light acrylic plates) that anchors headlines inside the material surface without toyish or retro-comic effects.
- **Body Text:** Comfortable, airy reading sizes (`16px–17px` desktop, `15px–16px` mobile) with generous line-height (`1.6`) and effortless contrast against translucent panels.
- **Technical & Module Labels:** Clean geometric sans or tabular monospace (`JetBrains Mono`, `11px–13px`, `font-variant-numeric: tabular-nums`) housed inside recessed aero wells or translucent pill tags.

## Color direction

Frutiger Aero uses a multi-layered sky, aqua, seafoam, and leaf color system that avoids collapsing into a single flat blue tone:

### Core Palette Tokens
```css
:root {
  /* Refined Conceptual Aero Palette */
  --aero-sky: #DCEFF8;
  --aero-cloud: #F7FBFD;
  --aero-aqua: #6CD1E8;
  --aero-ocean: #2C90B8;
  --aero-seafoam: #A7E6D5;
  --aero-leaf: #79C67A;
  --aero-deep-blue: #1F5D87;
  --aero-cool-shadow: rgba(58, 105, 141, 0.18);

  /* Canonical Compatibility Tokens */
  --taste-aero-aqua: #48BFD3;
  --taste-aero-ocean: #247EA3;
  --taste-aero-leaf: #70B981;
  --taste-aero-sky: #C9EDF8;
  --taste-aero-cloud: #F4FAFC;
  --taste-aero-deep-blue: #173F61;
  --taste-aero-charcoal: #243642;
}
```

### Light Mode (Clear Blue Digital Sky & Aqua Lagoon — Default)
- **Atmospheric Canvas:** Layered digital sky (`#CBE8F6` → `#DCEFF8` → `#F7FBFD`) illuminated by soft aqua (`#6CD1E8`), seafoam (`#A7E6D5`), and sunlit horizon radial light fields so foreground glass panels visibly refract color and depth.
- **Aero Glass Panels:** Translucent refractive acrylic (`linear-gradient(165deg, rgba(255, 255, 255, 0.84) 0%, rgba(247, 251, 253, 0.62) 52%, rgba(220, 239, 248, 0.74) 100%)`) with `18px` backdrop blur, outer sky contour (`rgba(44, 144, 184, 0.28)`), and crisp white inner rim (`inset 0 1.5px 0 #FFFFFF`).
- **Primary Molded Aqua:** Multi-stop glossy aqua-to-ocean gradient (`#6CD1E8` → `#48BFD3` → `#2C90B8` → `#1F5D87`).
- **Supporting Freshness Accents:** Seafoam (`#A7E6D5`) and fresh botanical leaf green (`#79C67A` / `#70B981` to `#2D7A47`) used carefully for eco-tech freshness indicators and secondary accents, never overpowering the sky/aqua foundation.
- **Reading Ink:** Deep ocean navy (`#173F61` / `#1F5D87`) and secondary slate charcoal (`#243642` / `#2D5270`).

### Dark Mode (Bioluminescent Deep Ocean & Midnight Aero Glass)
- **Atmospheric Canvas:** Deep oceanic midnight (`#081521` → `#0E2235` → `#15324B`) with bioluminescent aqua (`rgba(108, 209, 232, 0.22)`) and seafoam (`rgba(167, 230, 213, 0.14)`) horizon light fields.
- **Aero Glass Panels:** Translucent sapphire glass (`linear-gradient(165deg, rgba(22, 48, 74, 0.78) 0%, rgba(14, 34, 54, 0.68) 55%, rgba(20, 52, 80, 0.74) 100%)`) with `20px` backdrop blur and luminous cyan specular rims (`rgba(108, 209, 232, 0.38)`).
- **Foreground Ink:** Crisp porcelain cloud (`#F7FBFD` / `#F4FAFC`) and soft sky mist (`#B4D7EC`).

### Theme Coupling & Anti-Collision Rule
When switching between light and dark Aero modes (or across `Classic`, `Glass`, and `Tactile` expressions), foreground text, borders, recessed wells, and specular highlights MUST switch via CSS attribute selectors rather than hardcoded inline colors. Foreground text must maintain ≥ 4.5:1 WCAG AA contrast against both the panel surface and the atmospheric backdrop behind it.

## Layout and geometry

- **Asymmetric Hero & Material Focal Framing:** Pair a layered foreground Aero showcase island on the left with a visual centerpiece (glossy translucent orb, layered glass panel cluster, or molded tactile control plate) on the right, grounded by an integrated Aero dock tray below.
- **Balanced Split-Column Card Stacks & Equal-Height Grids (`.taste-aero-balanced-stack`):** Adhere to Invariant G in [PoW Showcase Structure](../references/pow-showcase-structure.md). Whenever a 2-column Studio bay or Component Gallery places a single tall card in Column A alongside 2–3 stacked cards in Column B, the parent grid MUST declare `align-items: stretch;`, the stacked column wrapper MUST declare `display: flex; flex-direction: column; height: 100%; justify-content: space-between;`, and each stacked child card MUST declare `flex: 1 1 0%; display: flex; flex-direction: column; justify-content: space-between;` so top and bottom edges align flush with zero empty void underneath. Never wrap 4 controls or buttons as `3 + 1` orphans (use a `2×2` grid).
- **Strict 1:1 Circle Geometry (Anti-Oval):** Every circular orb, dewdrop indicator, rotary dial, and icon button (`border-radius: 50%`) must enforce `aspect-ratio: 1 / 1; flex-shrink: 0;`.
- **Responsive Baseline:** Adhere to the [responsive baseline](../references/responsive-baseline.md) for `320px` minimum viewport safety, fluid typography, and unclipped glass/tactile panels across desktop, tablet, and mobile.
- **Fluid Molded Radii:** Approachable, physical curvature — `18px–22px` for Classic Aero panels, `22px–26px` for floating Aero Glass plates, `12px–14px` for contoured Aero Tactile hardware modules, and full capsule (`9999px`) for molded pill buttons and floating docks.

## Surfaces, depth, texture

Frutiger Aero fuses Glassmorphism and Skeuomorphism through five light-coherent CSS surface formulas (always lit from top-center / top-left at `180deg` / `165deg`):

- **1. Classic Aero Surface (Glossy Acrylic + Refractive Glass Fusion — `.taste-aero-card`):**
  ```css
  background: linear-gradient(
    165deg,
    rgba(255, 255, 255, 0.88) 0%,
    rgba(247, 251, 253, 0.72) 48%,
    rgba(220, 239, 248, 0.78) 100%
  );
  backdrop-filter: blur(16px) saturate(150%);
  -webkit-backdrop-filter: blur(16px) saturate(150%);
  border: 1px solid rgba(255, 255, 255, 0.92);
  box-shadow:
    0 14px 32px rgba(58, 105, 141, 0.18),
    0 2px 6px rgba(31, 93, 135, 0.08),
    inset 0 1.5px 0 #FFFFFF,
    inset 0 0 0 1px rgba(108, 209, 232, 0.25),
    inset 0 -2px 4px rgba(44, 144, 184, 0.12);
  border-radius: 18px;
  ```

- **2. Aero Glass Surface (Variant: Glass — Layered Crystalline Refraction — `.taste-aero-card-glass`):**
  ```css
  background: linear-gradient(
    160deg,
    rgba(255, 255, 255, 0.58) 0%,
    rgba(247, 251, 253, 0.36) 50%,
    rgba(108, 209, 232, 0.24) 100%
  );
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.88);
  box-shadow:
    0 18px 42px rgba(31, 93, 135, 0.16),
    inset 0 2px 1px rgba(255, 255, 255, 0.95),
    inset 0 0 0 1px rgba(255, 255, 255, 0.55),
    inset 0 -3px 8px rgba(108, 209, 232, 0.2);
  border-radius: 22px;
  ```

- **3. Aero Tactile Surface (Variant: Tactile — Molded Physical Contour — `.taste-aero-card-tactile`):**
  ```css
  background: linear-gradient(
    180deg,
    #FFFFFF 0%,
    #F4FAFC 46%,
    #DCEFF8 92%,
    #CBE6F3 100%
  );
  border: 1px solid #8CC2DB;
  box-shadow:
    0 10px 24px rgba(31, 93, 135, 0.2),
    0 2px 4px rgba(23, 63, 97, 0.12),
    inset 0 2px 0 #FFFFFF,
    inset 0 -3px 0 rgba(44, 144, 184, 0.28);
  border-radius: 12px;
  ```

- **4. Recessed Tactile Inset Well (`.taste-aero-inset-well`):**
  ```css
  background: linear-gradient(180deg, rgba(195, 228, 244, 0.65) 0%, rgba(236, 248, 253, 0.85) 100%);
  border: 1px solid rgba(44, 144, 184, 0.35);
  box-shadow:
    inset 0 2px 5px rgba(31, 93, 135, 0.18),
    inset 0 1px 2px rgba(23, 63, 97, 0.12),
    0 1px 0 rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  ```

- **5. Molded Primary Aqua Acrylic Button (`.taste-aero-btn` — Compact 40px Height & 10px Radius):**
  ```css
  height: 40px;
  padding: 0 1.15rem;
  background: linear-gradient(
    180deg,
    #3AA8CE 0%,
    #268BB2 46%,
    #1D7498 84%,
    #2383AA 100%
  );
  color: #FFFFFF;
  border-top: 1px solid #75D5EC;
  border-left: 1px solid #4BB8DC;
  border-right: 1px solid #165D7C;
  border-bottom: 1px solid #114B65;
  box-shadow:
    0 3px 9px rgba(21, 72, 108, 0.26),
    0 1px 2px rgba(15, 51, 77, 0.18),
    inset 1px 1px 0 rgba(255, 255, 255, 0.78),
    inset -1px -1.5px 2px rgba(12, 45, 66, 0.38),
    inset 0 -1px 4px rgba(108, 209, 232, 0.35);
  border-radius: 10px;
  ```

## Component anatomy and interaction

- **Shared Upper-Left (`135deg` / `165deg`) Lighting Model:** Every glass panel, molded button, recessed well, and focal object shares a single upper-left light source: `border-top` and `border-left` are brighter (`rgba(255, 255, 255, 0.96)`), `border-right` and `border-bottom` are cooler/darker (`rgba(31, 93, 135, 0.38)`), and recessed wells invert this relationship (`inset 1px 2px 4px` upper-left shadow + bottom-right highlight lip).
- **Vector Iconography & Sculptural Aero Geometry:** Emojis are strictly banned as interface icons, buttons, or status badges. Use clean vector icons (`1.5px–2px` stroke) and bespoke SVG glossy orb/lens/horizon geometry.
- **Primary Molded Aqua Button (`.taste-aero-btn` — Compact 34px/40px/44px Proportions & 6 Interactive States):** Avoid swollen `9999px` plastic capsules or harsh half-button white stripes. Use compact heights (`34px` small, `40px` medium default, `44px` hero CTA) with `10px–11px` corner radius, a soft curved upper-left specular reflection (`::before` covering the top 38% with `linear-gradient(172deg, rgba(255,255,255,0.48), rgba(255,255,255,0.14) 72%, transparent)`), smooth aqua-to-ocean contour, and all 6 states:
  1. **Rest:** Balanced directional rim + subtle elevation shadow.
  2. **Hover:** `-1px` lift + slightly brighter upper highlight.
  3. **Active / Pressed (`:active`):** `+1.5px` downward travel, compressed outer shadow, reduced upper sheen (`28%`), and inset top shadow (`inset 1px 2px 5px rgba(9, 31, 48, 0.48)`).
  4. **Focus Visible (`:focus-visible`):** Distinct `2px solid #2C90B8` outline with `2px` offset and luminous outer ring.
  5. **Disabled (`:disabled` / `.is-disabled`):** Desaturated (`filter: saturate(0.35)`), reduced contrast (`opacity: 0.52`), and flattened shadow (`transform: none`).
  6. **Loading (`.is-loading`):** Preserves button dimensions with an inline vector spinner.
- **Secondary Translucent Glass-Acrylic Button (`.taste-aero-btn-secondary`):** Features translucent cloud-glass fill, upper-left white rim (`border-top: 1px solid #FFFFFF`), lower-right sky contour (`rgba(31, 93, 135, 0.48)`), high-contrast deep ocean label (`#133654` / `#173F61`), and matching 6 interactive states.
- **Sunken Input Fields & Compact Scrollable Command Wells (`.taste-aero-input` & `.taste-aero-cmd`):** Recessed into the panel plane with upper-left inner shadow (`inset 1px 2px 4px rgba(23, 63, 97, 0.14)`), bottom-right white lip highlight (`0 1px 0 rgba(255, 255, 255, 0.9)`), and luminous aqua focus ring. Hero/CLI command boxes must stay compact on a single row (`height: 42px–44px`, `border-radius: 10px`, `flex-wrap: nowrap`) with a horizontally scrollable `<code>` container (`min-width: 0; overflow-x: auto; white-space: nowrap;`) and a pinned `[Copy]` button (`flex-shrink: 0`) — never wrapping into a giant multi-line stadium pill on mobile.
- **Tactile Segmented Switchers & Toggle Pills:** Housed inside a recessed `.taste-aero-inset-well` track where the selected pill rises as a glossy molded acrylic cap with top specular highlight.
- **Informative Aero Modules (Replacing Generic White Stat Cards):** Use translucent aero modules with inner horizon sheens, recessed progress/refraction tracks, and contextual eco-tech metadata rather than plain white dashboard boxes.

## Motion

Frutiger Aero motion is calm, physical, and restrained — static material quality always takes priority over animation:
- **Tactile Button Press (`:active`):** `110ms–120ms` physical downward response (`transform: translateY(1.5px)`) paired with shadow compression and highlight reduction.
- **Hover Response:** `120ms–150ms` subtle elevation (`transform: translateY(-1px)`) and mild top-sheen brightening without bouncy or elastic gimmicks.
- **Variant & Tab Transitions:** Smooth `160ms–180ms` opacity and surface interpolation.
- **Reduced Motion:** When `@media (prefers-reduced-motion: reduce)` is active, disable all transforms and animations (`transition: none !important; transform: none !important; animation: none !important;`) while preserving instant visual state changes.

## Hero composition (full first viewport)

For a public-facing landing page or showcase, apply the [Full-screen Hero Contract](../references/hero-layout.md):
- **Full 1-Screen First Viewport Equation (`100svh`):** The header + hero composition MUST fill **1 full opening screen** (`min-height: calc(100vh - var(--pow-header-h, 58px)); min-height: calc(100svh - var(--pow-header-h, 58px)); display: flex; flex-direction: column; justify-content: center;` with `--pow-header-h` defined in `:root`) so the next page section never bleeds into the bottom of the first desktop viewport (`1440×900` / `1440×950`). Let the hero expand naturally for accessibility and short mobile screens. Do not apply this to private dashboards or task screens; direct user overrides win.
- **Controlled Sky & Lagoon Atmosphere (Zero Step Seams):** Smooth upper-left sunlit radial light fields over layered sky-blue (`#DCEFF8`), aqua (`#6CD1E8`), and seafoam (`#A7E6D5`) gradients (never use hard 1% linear-gradient stops that draw a visible seam across the hero).
- **Balanced Two-Zone Hero Stage (`align-items: center`):**
  - **Left Primary Content Region:** Directly framed on the sunlit canvas (no oversized competing white box) with a clear 5-step hierarchy: (1) identity pill, (2) display headline, (3) concise human-centered explanation, (4) compact single-row scrollable `$ npx @kennedys0/taste-engine init --style frutiger-aero` command well with pinned `[Copy]` button, and (5) compact `44px` Primary Molded Aqua + Secondary Frosted Acrylic CTA buttons.
  - **Right Interactive "Aero Material Object":** A genuine multi-layered material specimen placing a contrasting environmental horizon layer (`Sunlit Sky`, `Aqua Reef`, `Spring Leaf`) directly *behind* a floating translucent Aero Glass card (`backdrop-filter: blur(...)`) so refraction and light transmission are unmistakably visible, paired with a molded acrylic orb/lens assembly, interactive environment switcher, tactile pulse test control, and live **Specular Sheen** slider.
- **Integrated Aero Expression Dock:** Anchor the bottom of the 1-screen hero with a luminous translucent Aero dock allowing instant switching and material inspection across `Classic Aero`, `Aero Glass`, and `Aero Tactile`.

## UI writing and microcopy

- **Tone:** Bright, fresh, clear, optimistic, and human. Evoke clean air, sunlight through clear water, and friendly tactile hardware.
- **Anti-Slop Voice:** Eliminate self-congratulatory engineering boast pills (*"100% WCAG AA Gated"*, *"Zero AI-Slop"*, *"320px Zero Mobile Overflow"*) from the hero. Ground labels in authentic material and product vocabulary (*"Glossy Aqua Acrylic"*, *"Crystalline Lens Refraction"*, *"Molded Tactile Bevel"*, *"Launch Aero Studio"*).
- **Empty & Status States:** Friendly, transparent explanations with tactile recovery actions.

## Style-specific quality gate

Before marking a Frutiger Aero page or component complete, verify every gate:

1. **Gate 1 (True Glass + Skeuo Material Fusion):** Do surfaces visibly combine Glassmorphic translucency/refraction with Skeuomorphic molded acrylic contours, top-half horizon sheens, and recessed physical wells?
2. **Gate 2 (Tactile Molded Button Quality):** Do Primary and Secondary buttons feel like touchable, dimensional aqua/glass caps with a visible top highlight band, contoured bevels, and a genuine compressed/inset `:active` pressed state?
3. **Gate 3 (Visual Hero Centerpiece & Atmosphere):** Does the hero visually demonstrate Frutiger Aero through a sky/aqua/seafoam atmosphere and a glossy orb/lens/acrylic centerpiece without relying on paragraph text or generic QA badges?
4. **Gate 4 (Deep Variant Differentiation):** Does switching between `Classic Aero`, `Aero Glass`, and `Aero Tactile` transform panel materials, button bevels, surface blur/depth, and centerpiece geometry across both Light and Dark modes?
5. **Gate 5 (Contrast & Readability):** Does every text element and button label meet or exceed WCAG AA 4.5:1 contrast against both its panel/button surface and the atmospheric background?
6. **Gate 6 (Balanced Card Stacks, 320px Mobile Safety & Fallbacks):** Are all split-column card stacks (`.taste-aero-balanced-stack`) and multi-column grids flush and balanced (`flex: 1 1 0%`, zero `3+1` orphan wraps), does the layout adapt cleanly down to `320px` width without clipping or horizontal overflow, and do solid fallbacks work when `backdrop-filter` or motion is reduced?

## Universal anti-slop gate (self-contained)

Every element must earn its place. **Content before decoration. Do not decorate uncertainty.** Do not invent balances, metrics, testimonials, users, logos, approval, verified/live/online status, fake activity, or success confirmations; use honest empty/loading/error states instead. Demo data is acceptable only if requested and visibly labeled.

Do not add decorative **card-inside-card** layers: a nested surface must represent a distinct interaction or information boundary. Avoid auto-generated 3-feature grids, 4-stat dashboards, fake hero claims, purposeless charts, badge/chip/icon spam, unrelated decorative art, and random loops merely to fill the viewport. Prefer grouping with typography, spacing, alignment and dividers. Equal peers need intentional visual balance.

**Anti-slop copywriting & zero emojis:** no generic "Unlock your potential", "Experience the future", "Supercharge your workflow", "seamless" claims, or translated equivalents. Headings must communicate actual content, CTAs must name the action, and empty/error/success text must describe real states and next steps. Avoid fake urgency, made-up counts, vague AI hype, and inaccessible all-caps walls. Emojis are strictly forbidden as UI icons, button prefixes, or badges across all styles; interface elements must exclusively use clean vector SVGs from Lucide, Radix, Feather, or Heroicons with currentColor inheritance. Adapt the wording to this style and the user's language without changing the truth.

**Theme and mode contrast integrity:** When a user requests dark mode or light mode (or builds a theme switcher), background and foreground colors MUST flip in synchronized pairs across all surfaces, text, borders, inputs, and semantic badges. Never leave black text on dark background, white text on white background, or unreadable low-contrast status pills. All states must meet WCAG AA contrast (minimum 4.5:1 for body/normal text, 3:1 for large headlines and interactive boundaries).

**Responsive 320px baseline and fluid typography:** compose mobile deliberately down to 320px minimum viewport width with zero horizontal blowout. Scale typography down smoothly while respecting readability minimums (body >= 1rem / 16px, secondary >= 0.875rem, code >= 0.8125rem). In top navigation bars, collapse navigation behind an accessible hamburger menu or disclosure with comfortable tap targets on mobile (< 768px). Circular geometry must enforce aspect-ratio: 1 / 1; flex-shrink: 0;. Static by default; use motion for meaningful interactions, respect reduced-motion preferences, avoid bounce/floating/pulsing decoration without a real state.

**Critical/High findings block completion:** fabricated status/data, broken actions, inaccessible/clipped controls, misleading copy, theme contrast collisions or significant mobile failure must be fixed. Report what was actually verified; do not claim tests that did not run.

**Not an aesthetics veto:** expressive colors, shadows, gradients, card layouts or decorative treatments are legitimate when they are intentional parts of the selected aesthetic and pass usability checks. Do not silently force minimalism.

## Anti-slop: style-specific

- **FAIL:** A soft minimal blue SaaS page with plain white rectangular stat cards and flat ghost/pill buttons claiming to be Frutiger Aero.
- **FAIL:** Hero dominated by self-congratulatory system badges (*"WCAG AA Contrast"*, *"Zero AI-Slop"*, *"140ms Restrained Motion"*) instead of demonstrating the style visually.
- **FAIL:** Glass reduced to mere opacity or Skeuomorphism reduced to a basic drop shadow with no top specular horizon sheen, inner rim highlight, or recessed well depth.
- **FAIL:** Variant switcher that only changes text strings or sets hardcoded inline light colors that break Dark Mode contrast.
- **FAIL:** Unbalanced split-column card stacks leaving dead vertical gaps or `3+1` orphan-wrapped button/checkbox rows.
- **FAIL:** Non-functional noisy wallpaper clutter, animated swimming fish, or emojis used as UI icons.
- **FAIL:** Low-contrast white text over pale aqua or semi-transparent white glass.
- **PASS:** Luminous sky/aqua/seafoam/leaf atmosphere, glossy translucent orb & acrylic lens centerpiece, molded tactile primary and secondary buttons with physical pressed states, dimensional aero panels with recessed wells, and deep differentiation across `Classic Aero`, `Aero Glass`, and `Aero Tactile`.

## Optional Anime.js v4 recipe

For projects that justify external coordinated motion, use Anime.js v4 with lifecycle cleanup and reduced-motion compliance:

```javascript
import { animate, createScope } from 'animejs';

// Respect user motion preferences
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export function animateAeroPress(element) {
  if (prefersReduced) return;
  
  animate(element, {
    scale: [1, 0.99, 1],
    translateY: [0, 2, 0],
    duration: 140,
    ease: 'outQuad',
  });
}
```

## Quality tiers (standalone)

**FLOOR (must pass):** correct and truthful data/state, working critical actions, accessible focus/labels/contrast, usable responsive UI and reduced-motion support. **REFLEX (explain or fix):** generic feature grids, purposeless nested cards, decorative labels/icons, default marketing hype or constant motion. A reflex is allowed when it clearly expresses the chosen style and serves the task. **FINISH:** refinement of alignment, typography rhythm and edge cases. Never treat the selected style itself as a violation. Do not claim browser testing unless actually performed.

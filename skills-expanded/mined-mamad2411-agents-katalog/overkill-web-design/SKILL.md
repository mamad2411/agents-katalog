---
name: overkill-web-design
description: Transform websites into mindblowing experiences with obsessive UX polish, 3D elements, cinematic animations, and every detail considered. Use when making a website ridiculously polished, creative, award-winning, or turning a normal site into a $50k experience. Triggers on "overkill", "make it overkill", "polish this website", "award-winning", "mindblowing", "make it creative", "extreme polish", "immersive", "cinematic website", "$50k website", "make it beautiful", "next level", "blow my mind", "premium feel".
user_invocable: true
---

# OverkillWEBDESIGN — The Design Obsession Engine

> "The difference between a $5k website and a $50k website is 10,000 details nobody can name but everybody can feel."

This skill is the **design brain** — the voice that says "you missed the nav button", "those colors aren't on-brand", "there's nothing to scroll." It tells you WHAT to do and WHY. For HOW (code templates, component implementations), see `3d-immersive`.

**Dependency:** All code templates, component patterns, and implementation details live in `3d-immersive`. This skill is pure design philosophy, audit process, and checklists.

**When to activate:**
- User says "overkill", "make it beautiful", "award-winning", "next level", "premium", "$50k"
- Transforming an existing site into something extraordinary
- Building a showcase, portfolio, or marketing site that needs to impress
- Any project where craft and polish are the primary goal

**When NOT to activate:**
- Admin panels, CRUD apps, documentation sites, internal tools
- Performance-critical dashboards where every KB matters
- User explicitly asks for simple/minimal implementation

---

## 1. The Overkill Mandate

**Every pixel sells the brand. Every interaction reinforces quality. NOTHING gets skipped.**

A glass-morphism nav bar tells the user this site was built by someone who cares. A magnetic button says: we thought about the 0.3 seconds you spend hovering. An on-brand 404 page says: we considered everything, even failure. A preloader that draws the logo says: the wait is part of the experience.

The difference between a student project and a $50K site isn't a single feature — it's the compounding effect of 10,000 micro-decisions. Each one is small. Together, they're the gap between "nice" and "how did you make this?"

### The Completeness Principle

Nothing gets skipped. Not the nav button hover state. Not the empty state. Not the 404. Not the loading skeleton. Not the error boundary. If a user can see it, it should look intentional. If they can interact with it, it should respond.

**The zero dead-spot rule:** if a user can hover, click, scroll, or tab to it, it responds. Every interactive element has at least three states: default, hover/focus, and active.

### On-Brand Discipline

Every color, every gradient, every subtle tone derives from the palette. If the brand is crimson + gold on dark, then the subtle background gradient is dark crimson tones, not arbitrary purple. The glass overlay is tinted warm, not cool blue. The hover glow matches the CTA color. Even the scrollbar thumb picks up the brand accent.

This applies to EVERYTHING:
- Error pages use brand colors
- Loading states use brand typography
- Empty states use brand illustration style
- Skeleton screens match the brand's visual language
- Even the cursor glow color is on-brand

---

## 2. Design Invariants (Zero-Tolerance Rules)

These are non-negotiable. Violating any produces obviously broken output.

### Every toggle must have visible impact
If a feature toggle exists, it MUST produce a visible change when flipped. A toggle that does nothing is a wasted feature and confuses users. Before shipping, flip every toggle and verify it changes something on screen. If a toggle's state doesn't alter the rendered output, either wire it to a real visual change or remove it.

### Zero dead buttons
After implementing any page, enumerate EVERY interactive element (buttons, links, nav items, cards) and verify that ALL applicable effects (magnetic, glass, focus-rings, tilt, hover states) are wired to ALL of them. Not just the "main" CTAs — every single clickable element. The nav "Contact Us" button is just as important as the hero CTA.

**Post-implementation audit (MANDATORY):**
1. List every `<button>`, `<a>`, clickable `<span>`, and interactive element on the page
2. For each one, verify: magnetic, glass, focus-ring, tilt (where applicable)
3. Any element missing treatment = bug, not a nice-to-have

### Brand palette discipline
ALL colors — including background gradients, subtle tones, overlays, and muted surfaces — MUST derive from the brand's defined color palette. Never use arbitrary colors that aren't in the brand's palette. If the brand is red + black, the subtle background is dark red/charcoal tones, not dark green. This applies to every surface: hero backgrounds, section gradients, card backgrounds, overlay tints.

### Typography scale follows background complexity
- **Minimal/no background** (solid color, subtle gradient): Text is the hero — use largest scale, centered, bold, single line if possible. The words must carry the entire visual weight.
- **Static image background**: Medium scale, positioned to avoid competing with image subject
- **Video/3D background**: Smaller scale, positioned in safe zones with enough contrast overlay

### Every feature needs a surface
If scroll-based features exist (smooth-scroll, scroll-progress, parallax, back-to-top), the page MUST have enough content to scroll. If tilt features exist, there must be cards to tilt. Every feature toggle must have at least one element it visibly affects.

### Font consistency across animation states
Animated text (scramble, typewriter, split-reveal) MUST use the same `font-family` as its final resting state. Never use a monospace font for scramble animation if the heading is a sans-serif like Rubik or Inter. The font-swap on animation completion creates a jarring visual jump where text reflows and changes width.

### Mount-once pattern for heavy assets
Always mount videos, 3D canvases, Spline embeds, and iframes ONCE and control visibility via opacity/display — never conditional rendering. Conditional mount/unmount causes re-loading on every toggle, producing a visible delay. Mount once, show/hide with CSS.

### Still frame selection protocol
When extracting a freeze frame from video for use as a poster, static background, or fallback:
1. Sample 5-6 frames across the video duration
2. Evaluate each for subject composition, negative space for text, visual energy, brand alignment
3. Show 2-3 best candidates to the user with brief notes on why each works
4. Never grab the first available frame — a poorly chosen freeze frame undermines the entire hero

### On-brand everything
Error pages, loading states, empty states, offline pages — ALL sell the brand. A generic "404 Not Found" breaks the spell. An animated 404 with witty copy and a redirect countdown says "we thought about everything." Test: screenshot ANY state of your site — does it look intentional?

---

## 3. The Completeness Audit

Before touching code, audit the existing site through eight phases. Score each 1-5. Anything below 4 gets a prescription.

### Phase 1: Hero Assessment

```
[ ] First impression timing — how fast does the hero hit? (target: < 3s to "wow")
[ ] Hero composition — is there depth? (foreground, midground, background layers)
[ ] Text treatment — split-text reveal or static?
[ ] Background — static image, gradient, video, or 3D scene?
[ ] CTA prominence — magnetic button? Spring animation? Cursor label?
```

**Prescriptions by score:**
- 1-2: Full hero rebuild. Add preloader -> split-text -> 3D/video background -> magnetic CTA
- 3: Add parallax layers, upgrade text animation, add cursor interaction
- 4: Polish timing, add micro-interactions, refine easing curves
- 5: Ship it

### Phase 2: Navigation Audit

```
[ ] Scroll response — does nav change on scroll? (shrink, blur, color shift)
[ ] Glass-morphism — backdrop-blur + transparency + subtle border?
[ ] Mobile treatment — sheet/drawer with stagger animation? Not just a hamburger slide?
[ ] Active state — animated indicator? Not just bold text?
[ ] Magnetic links — desktop nav items have magnetic hover pull?
```

**Prescriptions:**
- Add `backdrop-filter: blur(12px)` + `background: rgba(0,0,0,0.6)` + `border-bottom: 1px solid rgba(255,255,255,0.1)`
- Add scroll-driven height/padding transition (GSAP ScrollTrigger)
- Add magnetic hover to desktop nav items

### Phase 3: Content Flow

```
[ ] Map every section to a scroll moment (enter/hold/exit)
[ ] Identify pin candidates (stats, features, testimonials)
[ ] Mark parallax opportunities (any section with depth layers)
[ ] Check pacing — are there breathing sections between dense content?
[ ] Scroll progress indicator — global or per-section?
```

**Prescriptions:**
- Pin at least one section (feature showcase or stats counter)
- Add parallax depth to at least two sections
- Insert a full-viewport breathing section between the two densest blocks
- Add a subtle scroll progress bar (top of viewport, 2px, brand color)

### Phase 4: Interactive Element Catalog

```
For EVERY button, link, card, and form field:
[ ] Hover state — does it have one? Is it just color?
[ ] Focus state — visible, animated, brand-colored?
[ ] Active state — press feedback? Scale? Ripple?
[ ] Transition easing — linear? (Wrong.) Spring/elastic? (Right.)
[ ] Cursor interaction — does the cursor change context?
```

**Prescriptions:**
- Every button: magnetic pull + spring scale + cursor label
- Every card: tilt on hover (CSS perspective) + subtle shadow shift + cursor expand
- Every link: underline animation (width 0->100% from left)
- Every input: focus ring animation + label float

### Phase 5: Asset Quality

```
[ ] Images — cinematic quality or stock-looking?
[ ] Image treatment — raw or styled? (WebGL distortion, reveal animations, lazy blur-up)
[ ] 3D opportunities — any product/object that could be a rotating 3D model?
[ ] Video — any section that could be a looping background video?
[ ] Illustrations — custom or generic? Could be replaced with 3D/animated?
```

**Prescriptions:**
- Replace stock images with WebGL distortion hover effect (`hover-effect` library)
- Add scroll-triggered image reveals (clip-path or mask animation)
- Convert key product images to 3D models (.glb) if assets exist
- Use `next/image` with blur placeholder for all images

### Phase 6: Performance Baseline

```
[ ] Lighthouse score — Performance, Accessibility, Best Practices, SEO
[ ] Bundle size — gzipped JS total (target: < 300KB for 3D sites)
[ ] GPU headroom — open DevTools Performance, check GPU time per frame
[ ] LCP — < 2.5s? < 3.5s with preloader?
[ ] CLS — < 0.1? Font/image shifts?
[ ] Mobile frame rate — 30fps minimum acceptable, 60fps target
```

**Hard limits:**
- Lighthouse Performance: must stay > 85 after overkill treatment
- Main thread long tasks: < 50ms
- 3D canvas FPS: 60 desktop, 30 mobile (or fallback)
- Total JS: < 500KB gzipped (including Three.js)

### Phase 7: Edge Cases

```
[ ] 404 page — branded and designed, not default framework error?
[ ] Empty states — illustrated with personality, clear CTA to create first item?
[ ] Error boundary — animated recovery suggestions, not red text?
[ ] Offline page — cached brand experience with sync indicator?
[ ] Slow connection — skeleton screens pixel-identical to final layout?
[ ] JavaScript disabled — <noscript> with static fallback that still looks designed?
[ ] Loading states — branded skeletons, not generic spinners?
```

**Prescriptions:**
- 404: 3D scene or illustrated hero + witty copy + animated redirect countdown
- Empty: custom illustration + personality copy + primary CTA
- Error: recovery steps + retry button with spring animation
- Offline: cached brand assets + "back online" toast with confetti
- Skeleton: match final layout exactly, use brand shimmer color

### Phase 8: Brand Coherence

```
[ ] Are ALL surface colors derived from the brand palette? (backgrounds, overlays, subtle gradients)
[ ] Do glass effects use brand-tinted tones, not generic white/blue?
[ ] Is the typography consistent? (same font stack across all states, including animated text)
[ ] Do hover glows match the brand accent, not arbitrary colors?
[ ] Do error/success/warning states use brand-derived colors, not raw red/green/yellow?
[ ] Does the scrollbar thumb use brand accent?
[ ] Does the selection highlight (::selection) use brand colors?
[ ] Are cursor effects (glow, expand, label) on-brand?
```

**Test:** Walk through the entire site and screenshot 10 random states. If any screenshot uses a color not traceable to the brand palette, it's a coherence bug.

---

## 4. How to Apply Techniques On-Brand

### Deriving Surface Colors from a Brand Palette

Given a brand palette (e.g., primary: crimson #C62828, accent: gold #C9A84C, bg: near-black #0A0A0F):

| Surface | Derivation Method |
|---------|-------------------|
| Section backgrounds | Brand primary at 5-10% opacity over bg, or desaturated version |
| Card backgrounds | White at 4-8% opacity (glass), brand primary at 3-5% for tinted glass |
| Hover glows | Brand primary or accent at 30-50% opacity |
| Overlay gradients | Brand bg at 60-90% opacity, not pure black |
| Subtle borders | White at 8-15% opacity, or brand primary at 10% |
| Muted text | White at 50-70% opacity (dark themes), brand bg at 50-70% (light themes) |
| Error states | Brand primary shifted toward red (not raw red) |
| Success states | Brand accent shifted toward green (not raw green) |
| Scrollbar / selection | Brand accent at full or 70% opacity |

### Brand Personality -> Technique Mapping

Not every technique fits every brand. Match the personality:

**Bold / Industrial** (logistics, construction, heavy industry)
- DO: Clipped corners (polygon clip-path), dark grain texture, heavy display type (Bebas Neue, Oswald), subtle camera shake on scroll, angular section dividers, uppercase everything
- DON'T: Rounded pills, thin serif fonts, pastel gradients, gentle floats, soft shadows
- Easing: sharp `power4.out`, snappy transitions
- Colors: high contrast, dark base, single bold accent

**Elegant / Luxury** (fashion, jewelry, real estate, fine dining)
- DO: Thin serif type (Cormorant, Playfair), generous whitespace, slow animations (1.5s+), subtle glass with light borders, wide letter-spacing, horizontal rules, centered layouts
- DON'T: Neon colors, aggressive hover effects, dense grid layouts, monospace fonts, clipped corners
- Easing: smooth `expo.out`, long durations
- Colors: muted palette, gold/cream accents, deep darks

**Modern / SaaS** (tech products, platforms, dashboards)
- DO: Pill buttons, gradient glass panels, split-panel layouts, clean grid, Inter/DM Sans/Sora, subtle grid backgrounds, badge pills for features
- DON'T: Extreme animations, vintage typography, complex 3D scenes, film grain (unless dark mode dashboard)
- Easing: balanced `power2.out`, medium durations
- Colors: primary + neutral, blue-purple-green spectrum, clean whites

**Creative / Portfolio** (designers, agencies, artists, photographers)
- DO: Everything. Cursor mask reveals, distortion hovers, page transitions, film grain, split-text, scroll-driven video, sound design (opt-in), full preloader sequence
- DON'T: Hold back. This is where you use every technique that fits.
- Easing: expressive spring curves, playful bounces, dramatic reveals
- Colors: anything bold and deliberate

### Choosing 3D vs 2D Techniques

| Brand Signal | Recommendation |
|-------------|----------------|
| "We're innovative / cutting-edge" | Full 3D hero (R3F or Spline) |
| "We're reliable / trustworthy" | Subtle parallax + glass, no 3D |
| "We're playful / creative" | Physics interactions or particle fields |
| "We're premium / luxurious" | Slow camera dolly through minimal 3D scene |
| "We're fast / efficient" | Speed-focused animations, no heavy 3D |
| Product exists as physical object | 3D model viewer with orbit controls |
| Abstract concept / service | GLSL gradient noise background or particle atmosphere |

---

## 5. UX Obsession Principles

### Micro-Interaction Saturation
If you can hover/click/scroll/tab to it, it responds. Buttons pull magnetically. Cards tilt on hover. Links animate their underlines. Scroll reveals are staggered. Nothing sits dead on the page.

The cursor itself is a design element — on desktop, replace the default arrow with a mix-blend-mode: difference circle that changes size and shape based on what it hovers over. On CTAs, it expands and shows a label. On images, it shows "View." On drag areas, it shows arrows.

### Scroll Storytelling
Every scroll position is a directed frame. The user isn't just scrolling a page — they're advancing through a narrative. Pin sections for impact moments. Parallax layers create depth between foreground content and background atmosphere. Breathing sections (full-viewport with minimal content) create pacing between dense blocks.

Progress matters: a scroll indicator (subtle 2px bar at top, brand color) tells the user how deep they are. Sections that pin and play out on scroll give a cinematic feel — the user controls the pace.

### Typography as Art

| Normal | Overkill |
|--------|----------|
| Text fades in | Split-text stagger, per-character or per-word, with clip-mask reveal |
| Static font weight | Variable font weight shifts on scroll (wght axis 100->900) |
| Plain headings | Clip-mask text over video/gradient, animated gradient fills |
| Body text just sits there | Reading progress highlight — background-size animates on scroll |

Typography is 80% of web design. If you nail type, you can ship a beautiful site with zero images.

### Sound Design (User Opt-In)

| Normal | Overkill |
|--------|----------|
| Silent | Subtle ambient pad on opt-in, micro-sounds on interaction |
| No audio feedback | Click: soft tick. Hover: whisper whoosh. Success: chime |
| Music autoplays | Sound toggle in corner, muted by default, Web Audio API spatial |

**Rules:** Always behind user opt-in toggle. Use Howler.js for cross-browser. Keep files < 50KB each (MP3 CBR 64kbps). Sound is the single most underused lever in web design.

### Loading as Experience

| Normal | Overkill |
|--------|----------|
| Circular spinner | Brand animation — logo draws itself, morphs, or assembles |
| Progress bar | Counter with personality — percentage, asset names, witty messages |
| Blank then pop | Clip-path reveal, curtain wipe, or scale-from-center transition |

The preloader is Act 1 of a 3-act play. It sets the tone. Use the preloader template in `3d-immersive` as a starting point — extend it with brand mark animation, loaded asset counting, and an exit animation that becomes the hero entrance.

### Edge Case Polish

| Normal | Overkill |
|--------|----------|
| Generic "404 Not Found" | 3D scene with floating elements, witty copy, animated redirect countdown |
| Empty state: "No items" | Illustrated empty state with personality and clear CTA |
| Error: red text | Animated error boundary with recovery suggestions and retry |
| Offline: nothing | Offline page with cached brand experience and sync indicator |
| Slow connection | Skeleton screens pixel-identical to final layout, progressive image loading |

**Test:** If you can screenshot any state of your site and it looks intentional, you've reached overkill.

---

## 6. Performance Budget

Overkill does NOT mean slow. Every technique must earn its frame time.

### Core Web Vitals Targets

| Metric | Target | Hard Limit |
|--------|--------|------------|
| LCP | < 2.5s | < 3.5s (with preloader, LCP is the reveal) |
| FID / INP | < 100ms | < 200ms |
| CLS | < 0.05 | < 0.1 |
| FPS (desktop) | 60 | Never below 30 |
| FPS (mobile) | 30 | Fallback to static if below 20 |
| Lighthouse Performance | > 90 | > 80 |

### Bundle Budget

| Category | Budget (gzipped) |
|----------|-----------------|
| Three.js + R3F + drei | < 200KB |
| GSAP + plugins | < 30KB |
| Framer Motion | < 40KB |
| Application code | < 80KB |
| **Total 3D site** | **< 350KB** |
| **Total non-3D overkill** | **< 150KB** |

### When to Cut Effects (drop order)

If performance budget is exceeded, cut in this order (least valuable first):
1. Post-processing effects (ChromaticAberration, DepthOfField)
2. Particle count (reduce by 2x, then 4x)
3. Physics interactions
4. Custom cursor (replace with CSS cursor changes)
5. Film grain animation (replace with static noise texture)
6. Parallax layers (reduce to 2, then remove)
7. Split-text animation (simplify to word-level, then fade)
8. **NEVER cut:** Hover states, focus rings, responsive layout, accessibility

### Mobile Degradation Strategy

| Desktop | Mobile |
|---------|--------|
| Full 3D scene | Static hero image or CSS gradient |
| 2000 particles | 500 particles (or remove) |
| Post-processing stack | Remove entirely |
| `dpr={[1, 2]}` | `dpr={[1, 1.5]}` |
| Custom cursor | System cursor |
| Hover effects | Touch feedback (scale on press) |
| Film grain animated | Film grain static (single frame) |
| Parallax depth | Simplified or removed |

---

## 7. The Overkill Checklist

Pre-ship verification. Every item must be checked before claiming a site is "overkill."

### Interactions
```
[ ] Every button has hover + active + focus states (all three)
[ ] Magnetic buttons on CTAs (desktop)
[ ] Cursor context changes on interactive elements (desktop)
[ ] Click feedback on every clickable element (scale spring, ripple, or color)
[ ] All transitions use spring/elastic easing (never linear, never ease-in-out)
[ ] Link underlines animate (width 0->100% or slide)
[ ] Card hover has tilt or depth change
[ ] Form inputs have floating labels + animated focus ring
```

### Visual Polish
```
[ ] Film grain overlay on dark themes (opacity 0.03-0.06)
[ ] Split-text stagger on hero heading
[ ] Parallax depth on at least 2 sections
[ ] Custom preloader (not a spinner)
[ ] Designed 404 page (not default)
[ ] Designed empty states (not "No items found")
[ ] Scroll progress indicator
[ ] Consistent border-radius system (not random values)
[ ] Consistent spacing scale (4px base)
[ ] Color palette limited to 3-4 colors + neutrals
```

### Brand Coherence
```
[ ] ALL surface colors derive from brand palette (no arbitrary colors)
[ ] Glass effects use brand-tinted tones
[ ] Typography consistent across all states (including animated text)
[ ] Hover glows match brand accent
[ ] Error/success/warning states use brand-derived colors
[ ] Selection highlight (::selection) uses brand colors
[ ] Cursor effects are on-brand
```

### Performance
```
[ ] Lighthouse Performance > 85
[ ] 60fps scroll on desktop (check with DevTools Performance)
[ ] LCP < 3s (including preloader if used)
[ ] CLS < 0.1 (no layout shifts on load)
[ ] Total JS < 350KB gzipped (3D) or < 150KB (non-3D)
[ ] All 3D dynamically imported (not in main bundle)
[ ] Images use next/image with blur placeholder
[ ] Fonts use next/font with swap
```

### Accessibility
```
[ ] Screen reader tested (VoiceOver or NVDA walk-through)
[ ] Full keyboard navigation (Tab, Enter, Escape, Arrow keys)
[ ] Focus rings visible and beautiful (not browser default)
[ ] Focus-visible only (no focus ring on mouse click)
[ ] prefers-reduced-motion alternative (still looks premium)
[ ] prefers-color-scheme support (if applicable)
[ ] WCAG AA contrast on all text
[ ] All images have alt text (decorative = alt="")
[ ] ARIA labels on icon-only buttons
[ ] Skip-to-content link
```

### Mobile
```
[ ] No hover-dependent interactions (all work on touch)
[ ] No horizontal overflow (check all breakpoints)
[ ] Touch targets > 44px
[ ] 3D simplified or replaced with static fallback
[ ] Reduced particle count (4x less than desktop)
[ ] Tested on real device (not just DevTools)
[ ] Text readable without zooming (min 16px body)
```

### Edge Cases
```
[ ] 404 page is branded and designed
[ ] Empty states have personality and CTA
[ ] Error boundary has recovery path
[ ] Loading skeletons match final layout
[ ] JavaScript-disabled has <noscript> fallback
```

### The Wow Factor Test
```
[ ] Show someone who hasn't seen it -> they audibly react
[ ] They scroll back to the top to see the hero again
[ ] They try hovering on random elements to see what happens
[ ] They ask "how did you make this?"
```

If all four happen, it's overkill. If fewer than two, go back to the audit.

---

## 8. Archetypes — Complete Design Recipes

### The $50K Landing Page

**Component composition:** Preloader -> Hero (3D/video background + split-text + parallax CTAs) -> Glass nav (scroll-responsive) -> Pinned feature showcase -> Breathing section -> Parallax stats counter -> Testimonial carousel (blur transitions) -> CTA section (full-width, magnetic) -> Footer (parallax reveal + magnetic socials).

**Brand decisions:** Run full 8-phase audit first. Choose 3D vs video background based on brand personality (Section 4). Nav glass tint matches brand. All section backgrounds derived from palette. Typography scale matches background complexity per invariant.

**Integration gotchas:**
- Preloader must complete before Lenis smooth scroll initializes (prevents scroll-during-load)
- GSAP ScrollTrigger and Lenis must be synced (use `initGsapLenisSync` from `3d-immersive`)
- Do NOT use ScrollControls (drei) and Lenis together — they conflict
- Film grain SVG must be `position: fixed` with `pointer-events: none` and `z-index: 9999`
- All magnetic buttons need `data-cursor` attributes for custom cursor integration

**Common mistakes:**
- Forgetting nav button hover states (Phase 2 catches this)
- Using off-brand colors for section gradients (Phase 8 catches this)
- Preloader that blocks too long (keep under 3s)
- Pin sections without enough scroll distance for content to play out

### The Immersive Portfolio

**Component composition:** Preloader -> Project grid with WebGL distortion hover -> Custom cursor ("View" on cards) -> Page transitions (slideUp in template.tsx) -> Project detail: split-text title + cursor mask hero -> Film grain throughout.

**Brand decisions:** The portfolio IS the brand. Use every technique. Custom cursor is mandatory — it's the primary differentiator. Choose distortion images for the grid (not all projects, pick 6-8 hero shots). Page transition variant should match the portfolio's personality (fade for elegant, slideUp for modern, curtain for dramatic).

**Integration gotchas:**
- `hover-effect` library uses WebGL — needs `<Suspense>` wrapping on the grid
- Cursor mask requires desktop detection — mobile shows default layer only
- Page transitions go in `app/template.tsx` (NOT layout.tsx — layout doesn't remount)
- Film grain z-index must be above page content but below the cursor

**Common mistakes:**
- Using the same distortion effect on every project card (vary the intensity/direction)
- Custom cursor that blocks click targets (ensure `pointer-events: none`)
- Page transitions that feel slow (keep under 0.6s total)
- Missing mobile fallback for WebGL distortion grid (use CSS filter on touch devices)

### The Product Showcase

**Component composition:** Hero with product model (.glb) + orbit controls -> Scroll-driven rotation -> Feature callouts at rotation angles -> Material/color picker -> Specs with counter animation -> CTA section.

**Brand decisions:** The product IS the hero — no competing visual effects. Use Studio lighting for photorealistic render. Minimal post-processing (just bloom + vignette). Typography should be clean and informative, not dramatic. Background should be simple (gradient or solid) to keep focus on the model.

**Integration gotchas:**
- Always preload the .glb model (`useGLTF.preload`) — don't let users wait
- Draco compression pipeline: `npx @gltf-transform/cli optimize input.glb output.glb --compress draco`
- Orbit controls should constrain polar angle (prevent viewing the bottom)
- Material switches need smooth transitions (lerp material properties over 0.3s)

**Common mistakes:**
- 3D model too heavy (target < 2MB .glb after Draco)
- No loading skeleton for the Canvas (shows white flash)
- Feature callouts that block the model on mobile (stack below on small screens)
- Missing touch support for orbit controls (drei handles this, but verify)

---

## 9. Before / After Reference Table

Quick-reference for transforming common elements from normal to overkill.

| Element | Normal | Overkill |
|---------|--------|----------|
| **Hero** | Static image + text | 3D scene / video + split-text stagger + parallax layers + preloader entrance |
| **Buttons** | Color change on hover | Magnetic pull + cursor label + spring scale + optional micro-sound |
| **Cards** | Box shadow on hover | Tilt (CSS perspective) + WebGL distortion + cursor expand + shadow depth shift |
| **Navigation** | Solid background bar | Glass-morphism + scroll-responsive shrink + magnetic link items |
| **Page load** | Spinner or white flash | Branded counter + clip-path reveal + orchestrated content entrance |
| **Scroll** | Browser default | Lenis smooth + parallax layers + pinned sections + progress indicator |
| **Images** | Static `<img>` | WebGL distortion hover + scroll-triggered reveal (clip-path) + lazy blur-up |
| **Text** | Fade in | Split-text per-char stagger + clip-mask reveal + scroll-driven highlight |
| **Transitions** | Instant page swap | Exit choreography (curtain/zoom/morph) -> staggered enter |
| **Error page** | "404 Not Found" text | 3D scene + witty copy + animated redirect countdown |
| **Footer** | Static dark block | Parallax reveal from behind content + magnetic social icons + film grain |
| **Forms** | Standard inputs | Floating labels + animated focus rings + success micro-animation + validation shake |
| **Testimonials** | Card carousel | Pinned scroll section + blur transition between quotes + avatar parallax |
| **Stats/numbers** | Static text | Counter animation on scroll intersection + eased number roll |
| **Backgrounds** | Solid color | GLSL gradient noise + film grain overlay + subtle mouse reactivity |
| **Dividers** | `<hr>` or border | Animated line draw + gradient fade + scroll-triggered |

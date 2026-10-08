---
name: cinematic-motion
description: >
  Use this skill when building cinematic, animated, or immersive web experiences.
  Covers scroll-driven storytelling (GSAP, ScrollTrigger, SplitText, video scrubbing,
  parallax, mask reveals), 3D product showcases (R3F, Zustand, studio lighting,
  model switching, video textures), layout composition (bento grids, masonry,
  power lines, overlapping typography), and register-aware creative direction.
  Activated when the user asks to "build a cinematic landing page", "add scroll
  animations", "create a 3D product viewer", "scrub video on scroll", "build a
  bento grid with scroll reveals", "animate text on scroll", "add parallax effects",
  "create a mask reveal", "build an infinite slider", "implement model switching",
  "add studio lighting to 3D scene", "map video textures on 3D screens", or any
  task producing premium animated web surfaces. Also activated for FFmpeg keyframe
  encoding, GSAP ScrollTrigger configuration, SplitText typography, gltfjsx model
  conversion, Zustand state for 3D, or scroll-bound timeline orchestration.
  Do NOT use for standard non-animated UI (use skill-ui-ux), pure backend APIs,
  or static data tables.
---

# Cinematic Motion

Build premium, animated web experiences that feel like $10,000 websites.
Every animation serves the brand. Every scroll tells a story. Every 3D scene
is intentional.

**Design Authority:** This skill is loaded by `/impeccable-animate`. It reads
PRODUCT.md for register detection and DESIGN.md for visual tokens. The creative
direction layer adapts all technical patterns to the brand personality.

---

## SECTION 1: CREATIVE DIRECTION

This section is the brain. It decides WHAT to animate and WHY before touching
any code. Every project starts here.

### Register Detection

Detect register using `skills/ui-ux/SKILL.md` Layer 3 Register System (priority order: PRODUCT.md → task cue → surface in focus).

Brand surfaces get ambitious motion. Product surfaces get functional motion.
Never mix registers — a dashboard with cinematic parallax is wrong.

### Diagnostic Walkthrough

When the brand archetype isn't obvious (most real projects), walk through this:

**Step 1 — Name the emotion.** Not "modern" or "elegant." Physical-object words.
(See `skills/ui-ux/reference/brand.md` > Font Selection for the three-word diagnostic.)
- "Calm and trustworthy" → wellness, therapy, financial advisor
- "Bold and disruptive" → tech startup, new product launch
- "Warm and inviting" → restaurant, hospitality, community
- "Precise and authoritative" → law firm, engineering, medical
- "Playful and energetic" → kids brand, gaming, entertainment
- "Refined and exclusive" → luxury, fashion, high-end services

**Step 2 — Translate emotion to motion.**
- Calm = slow, predictable, no surprises, breathing rhythm, warm easing
- Bold = fast, unexpected, elastic, high contrast, snappy
- Warm = gentle parallax, soft reveals, organic shapes, medium pace
- Precise = clean transitions, no decoration, sharp timing, structured
- Playful = bounce, elastic, staggered, responsive, multiple triggers
- Refined = long reveals, deliberate pins, sparse density, editorial pacing

**Step 3 — Choose what NOT to use.**
(See `skills/ui-ux/reference/brand.md` > Slop Test for distinctiveness check. See `skills/ui-ux/reference/design-bans.md` for the absolute ban list. See motion-design.md >
Easing for the bounce/elastic guardrail.)
- Calm brand → no video scrub (too intense), no elastic easing (too playful)
- Bold brand → no slow pins (too passive), no subtle fades (too quiet)
- Warm brand → no harsh spotlights (too cold), no fast scrubbing (too aggressive)
- Precise brand → no bounce (too casual), no chaotic layouts (too messy)
- Playful brand → no long pins (too boring), no sparse density (too empty)
- Refined brand → no elastic (too casual), no dense sections (too cluttered)

**Step 4 — Select the scroll rhythm.**
- One hero moment → video scrub OR 3D viewer OR dramatic text reveal (not all three)
- Build credibility → parallax, masonry, feature reveals (gradual pace increase)
- Climax → the strongest visual (mask expansion, 3D showcase, interface scatter)
- Resolve → CTA, bento highlights, footer (ease down, gentle reveals)

### Brand-to-Motion Matrix

Map the brand personality to motion characteristics before building.
For easing details, see Section 2 > Easing Selection.

| Brand Archetype | Easing | Speed | Density | Scroll Behavior | 3D Style |
|----------------|--------|-------|---------|-----------------|----------|
| Luxury / Editorial | `expo.out` | 800-1200ms | Sparse | Deliberate pins, long reveals | Soft lighting, slow rotation |
| Tech / Startup | `power2.out` | 200-400ms | Medium | Fast scrubbing, elastic snaps | High-contrast, sharp edges |
| Creative / Agency | `back.inOut` | 400-800ms | Dense | Chaotic-then-ordered | Dynamic lighting, experimental |
| Restaurant / Hospitality | `power1.inOut` | 500-800ms | Medium | Smooth parallax, gentle reveals | Warm tones, organic shapes |
| Fashion / Lifestyle | `expo.out` | 600-1000ms | Sparse-dense rhythm | Editorial pacing | Studio lighting, dramatic shadows |
| Professional Services | `power2.out` | 300-500ms | Restrained | Subtle reveals, trust-building | Minimal, clean |
| Entertainment / Gaming | `elastic.out` | 200-600ms | Dense | Fast, responsive | Dynamic, reactive lighting |

**Consult before choosing:**
- `skills/ui-ux/reference/brand.md` > Brand Register — brand surfaces allow ambitious motion
- `skills/ui-ux/reference/brand.md` > Font Selection — three-word diagnostic, reflex-reject list
- product.md > Product Register — 150-250ms only, no page-load choreography
- motion-design.md > Duration — timing matters more than easing
- motion-design.md > Easing — no bounce/elastic except entertainment/gaming

### Hybrid Archetypes

Most real projects don't fit cleanly into one archetype. When the brand is a
blend (e.g., "warm luxury," "luxury tech," "playful professional"), follow this:

1. **Name the primary archetype** — the dominant personality
2. **Name the secondary archetype** — what it borrows from
3. **Resolve conflicts in favor of the primary**

| Hybrid | Primary | Secondary | Resolution |
|--------|---------|-----------|------------|
| Warm Luxury | Luxury | Restaurant | Luxury easing (expo.out) + warm tones (not cold). Slow reveals but with warmth, not austerity. |
| Luxury Tech | Luxury | Tech | Luxury density (sparse) + tech speed (snappy). Clean, not chaotic. Think Apple product pages. |
| Playful Professional | Professional | Creative | Professional restraint + playful easing. Subtle bounce on CTAs only, not throughout. |
| Bold Restaurant | Restaurant | Tech | Restaurant warmth + tech energy. Faster parallax, snappier transitions, but still warm colors. |
| Editorial Fashion | Fashion | Luxury | Fashion rhythm (sparse-dense) + luxury pacing (deliberate). Alternating full-bleed and minimal. |

**Rule:** Never average two archetypes. Pick one as primary, borrow specific
traits from the secondary. "Luxury tech" is NOT medium speed with medium density —
it's luxury density (sparse) with tech speed (snappy on interactions, slow on reveals).

### Worked Examples

These show how the same skill produces completely different results based on
the brand diagnosis. Study the reasoning, not just the output.

---

**EXAMPLE 1: Luxury Wellness Coach**

Brief: "Solo practitioner, wants to feel calm and trustworthy, premium positioning"

Diagnosis:
- Emotion = trust + calm. Not excitement, not authority.
- Trust = slow, predictable, no surprises
- Calm = breathing rhythm, warm tones, generous whitespace

Motion vocabulary:
- Easing: `power1.inOut` (smooth, no drama)
- Speed: 600-800ms (deliberate, unhurried)
- Density: Sparse (one idea per section)
- Scroll behavior: Gentle fades on scroll, no pinning, no video scrub

What to use:
- Hero: Large serif headline with slow SplitText line reveal (not chars — too busy)
- Sections: Fade-in on scroll with `toggleActions: 'play none none none'`
- Parallax: Subtle leaf movements at 20% opacity (not dramatic)
- Images: Warm-toned Unsplash (massage table, natural textures, soft light)

What NOT to use:
- No video scrub (too intense for calm brand)
- No elastic/bounce easing (too playful)
- No 3D viewer (too tech-forward)
- No pinned sections (too aggressive)
- No interface scatter (too chaotic)
- No mask expansion (too dramatic)

External assets needed:
- Hero image: Warm-toned, soft-focus wellness imagery
- Section images: 3-4 lifestyle photos (Unsplash works)
- No video, no 3D models

---

**EXAMPLE 2: Tech Startup (AI Product)**

Brief: "B2B SaaS, AI-powered analytics, wants to feel cutting-edge and trustworthy"

Diagnosis:
- Emotion = innovation + credibility
- Innovation = fast, snappy, surprising, high-tech
- Credibility = structured, clean, not chaotic

Motion vocabulary:
- Easing: `power2.out` (snappy but not playful)
- Speed: 200-400ms (responsive, quick)
- Density: Medium (structured sections, clear hierarchy)
- Scroll behavior: Fast scrubbing, elastic snaps, bento grid reveals

What to use:
- Hero: Autoplaying muted video background (product demo or abstract data visualization)
  with scroll-triggered text reveal
- Sections: Bento grid with staggered card reveals on scroll
- 3D: Optional product viewer with PresentationControls (if they have a 3D model)
- Parallax: Interface scatter — screenshots flying outward on scroll
- Typography: Sans-serif, tight tracking, strong weight contrast

What NOT to use:
- No slow pins (too passive for tech brand)
- No elastic easing on luxury sections (keep it credible)
- No chaotic mosaic layouts (too messy for B2B)
- No dramatic mask expansion (too editorial)

External assets needed:
- Hero video: 5-10 second product demo or abstract data visualization
  → Generate with Kling AI: "Abstract data visualization, flowing particles,
  dark background, blue and purple accents, 5 seconds, smooth camera movement"
- Product screenshots: 4 interface screenshots for scatter effect
- 3D model: Optional — if they have a GLB file, set up viewer
  → If no model: use product screenshots in a styled frame instead

---

**EXAMPLE 3: Restaurant / Hospitality**

Brief: "Italian restaurant, family-owned, wants to feel warm and inviting"

Diagnosis:
- Emotion = warmth + appetite + tradition
- Warmth = soft, organic, natural
- Appetite = rich colors, close-up food imagery
- Tradition = editorial pacing, not too fast

Motion vocabulary:
- Easing: `power1.inOut` (warm, gentle)
- Speed: 500-800ms (medium pace, not rushed)
- Density: Medium, alternating (food photo → text → food photo)
- Scroll behavior: Smooth parallax, gentle reveals, no aggressive pinning

What to use:
- Hero: Large hero image with slow zoom-in on scroll (CSS transform, not video)
- Sections: Alternating full-bleed food photos and text sections
- Parallax: Ingredient images floating gently on scroll
- Menu: Infinite slider with modulo (dishes carousel)
- Typography: Display serif for headings, humanist sans for body

What NOT to use:
- No video scrub (too intense for warm brand)
- No 3D viewer (wrong context)
- No interface scatter (too tech)
- No elastic/bounce (too playful for traditional)
- No bento grid (too structured, too SaaS)

External assets needed:
- Hero image: Overhead shot of a plated dish, warm lighting
  → Unsplash: "handmade pasta on scratched wooden table" or "italian restaurant interior warm light"
- Food images: 6-8 dish photos for menu slider
  → User provides their own food photography (critical for restaurants)
- Texture: Noise overlay (code generates this with SVG)
- No video, no 3D models

---

### Scroll Narrative Architecture

Every scroll-driven page follows a 4-act structure. The percentages are
approximate — adapt to the number of sections:

1. **Hook (first section):** Grab attention. Hero section. Video scrub or
   dramatic text reveal. The user decides to stay or leave here. Make it count.
2. **Build (middle sections):** Establish credibility. Parallax layers, masonry
   grids, feature reveals. Pace builds gradually. Alternate density —
   text-only → full-bleed media → massive typography.
3. **Climax (one section):** The peak moment. Mask expansion, 3D product
   showcase, interface scatter, or video mask reveal. This is where the user's
   attention is highest. Put the strongest visual here. ONE section, not two.
4. **Resolve (final sections):** Call to action. Bento grid highlights,
   testimonial, contact/footer. Ease the user down. Staggered card reveals,
   gentle parallax.

**For short pages (3-4 sections):** Combine hook+build or build+resolve.
The principle matters more than the percentages. Every page needs a hook
and a climax. The build and resolve can be compressed.

**For long pages (8+ sections):** You can have multiple build phases with
mini-climaxes, but there should be ONE peak moment that stands above all others.

### Restraint Rules

When NOT to animate. (See product.md > Product Register for product bans.)

- **Product register dashboards** — users are in a task. No page-load choreography.
- **Data-heavy tables** — animation on 100 rows kills performance and annoys users.
- **Forms** — subtle validation feedback only. No entrance animation on input fields.
  (See interaction-design.md > Form Design for validation timing.)
- **Error states** — immediate, clear communication. No delay on error messages.
- **Navigation** — standard, predictable placement. Never animate primary nav position.
- **`prefers-reduced-motion`** — provide crossfade alternatives, not just
  `animation: none`. Respect vestibular disorders (~35% of adults over 40).

### MOBILE SCROLL STRATEGY

When pinned ScrollTrigger sections are disabled on mobile:
  → The layout MUST NOT collapse into a raw vertical stack.
  → Replace pin sections with a CSS reveal cascade using scroll-triggered
    class additions: `.reveal-on-scroll` (opacity: 0 → 1, translateY: 20px → 0)
  → Each narrative act (Hook, Build, Climax, Resolve) must still read as a
    distinct visual section on mobile via:
      - Section background changes (color, texture)
      - Typography scale shifts between acts
      - Image/media reveal timing that maintains pacing

This preserves the 4-act narrative on mobile without scroll jank or pin-related
layout bugs.

Elastic and spring physics on mobile: banned entirely. Use `expo.out` or `power2.out` only.

```javascript
// Mobile reveal cascade — use IntersectionObserver for scroll-triggered class additions
import { useEffect, useRef } from 'react';

export function useRevealOnScroll() {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) el.classList.add('visible'); },
      { threshold: 0.2 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);
  return ref;
}
```

```css
/* Mobile reveal cascade — replaces pinned sections on mobile */
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Each narrative act gets distinct visual treatment on mobile */
@media (max-width: 1024px) {
  .act-hook { background: var(--bg-primary); }
  .act-build { background: var(--bg-secondary); }
  .act-climax { background: var(--bg-accent-subtle); }
  .act-resolve { background: var(--bg-primary); }
}
```

### Brand-to-Texture Mapping

When the brand implies imagery (restaurants, hotels, fashion, food, travel,
photography), you MUST ship imagery. Zero images is a bug. (See `skills/ui-ux/reference/brand.md` >
Imagery for the "zero images is a bug" rule.)

Use Unsplash for greenfield work:

```
https://images.unsplash.com/photo-{id}?auto=format&fit=crop&w=1600&q=80
```

Search for the brand's physical object, not the generic category. "Handmade
pasta on a scratched wooden table" beats "Italian food."

---

## SECTION 2: GSAP + SCROLL STORYTELLING

The hands for 2D cinematic experiences. Every pattern here serves the creative
direction from Section 1.

### GSAP Core

#### Installation

```bash
npm install gsap @gsap/react react-responsive
```

#### Registration & Scoping

```javascript
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/all';

gsap.registerPlugin(ScrollTrigger, SplitText);
```

Always wrap GSAP in `useGSAP` with a container ref. Automatic cleanup on unmount.
Scoped selectors. No memory leaks.

```javascript
const containerRef = useRef();
useGSAP(() => { /* animations */ }, { scope: containerRef });
```

#### Tween Methods

| Method | Use When |
|--------|----------|
| `gsap.to(target, vars)` | Current state → new state |
| `gsap.from(target, vars)` | Designated state → CSS default (entrance reveals) |
| `gsap.fromTo(target, fromVars, toVars)` | Explicit start AND end, bypassing CSS |

#### Easing Selection

Pick easing based on brand personality (see Brand-to-Motion Matrix above).

| Ease | Behavior | Use For |
|------|----------|---------|
| `power1.inOut` / `power2.out` | Smooth acceleration/deceleration | UI transitions, text fades, default |
| `expo.out` | Fast start, slow deceleration | Hero text reveals, dramatic entrances, luxury |
| `elastic.out` | Spring bounce | CTA buttons, playful widgets, gaming |
| `bounce.out` | Drop and bounce | Grid elements, drop-in alerts |
| `back.inOut` | Overshoots then settles | Editorial transitions, screen wipes |

**Guardrail (from motion-design.md > Easing):** No bounce/elastic except
entertainment/gaming. Prefer exponential curves:
- `cubic-bezier(0.25, 1, 0.5, 1)` — quart out, smooth, refined (default)
- `cubic-bezier(0.22, 1, 0.36, 1)` — quint out, slightly dramatic
- `cubic-bezier(0.16, 1, 0.3, 1)` — expo out, snappy, confident

#### Stagger

```javascript
// Basic
gsap.to('.items', { y: 50, stagger: 0.2 });

// Advanced — grid-aware center-out wave
gsap.to('.items', {
  y: 50,
  stagger: { amount: 1.5, from: 'center', grid: 'auto', ease: 'circ.inOut' }
});
```

Cap total stagger time: 10 items at 50ms = 500ms total. For many items,
reduce per-item delay.

#### Timelines

Chain animations sequentially. Use `'-=0.5'` to `'-=0.8'` overlap for smooth
choreography.

```javascript
const tl = gsap.timeline({
  scrollTrigger: { trigger: section, start: 'top 60%', toggleActions: 'play none none none' }
});

tl.from(splitText.words, { opacity: 0, yPercent: 100, duration: 1.2, ease: 'expo.out', stagger: 0.03 })
  .from('.card', { opacity: 0, y: 30, duration: 1, ease: 'power2.out', stagger: 0.1 }, '-=0.8');
```

Save timeline to a ref for interactive control (pause, play, reverse):

```javascript
const tlRef = useRef();
useGSAP(() => {
  const tl = gsap.timeline({ repeat: -1, yoyo: true });
  tl.to('#box', { x: 250, duration: 2 }).to('#box', { y: 150, duration: 1.5 });
  tlRef.current = tl;
});
// Toggle: tlRef.current.pause() / tlRef.current.play()
```

#### ScrollTrigger Configuration

```javascript
gsap.to(el, {
  x: 150,
  scrollTrigger: {
    trigger: el,           // Element that triggers the animation
    start: 'top 80%',      // When trigger top hits 80% viewport height
    end: 'bottom 20%',     // When trigger bottom hits 20% viewport height
    scrub: true,           // Lock animation frame to scroll coordinate
    pin: false,            // Pin element during scrub
    toggleActions: 'play none none none',  // onEnter onLeave onEnterBack onLeaveBack
  }
});
```

Use `scrub: 1` or `scrub: 1.5` for buttery follow-through delay on rigid scroll
ticks. Use `toggleActions: 'play none none none'` for one-play entrance animations.

#### SplitText Typography

**Font selection (from `skills/ui-ux/reference/brand.md` > Font Selection):** Every project. Three
brand-voice words → three font reflexes → reject defaults. See `skills/ui-ux/reference/brand.md` for
the full procedure and reflex-reject list (Playfair Display, Lobster, Poppins,
Montserrat, Raleway, Oswald, Lato).

**Character staggering rule:** Characters for hero headlines ONLY. Never
stagger characters on long paragraphs — performance kill and distraction.
Split into lines, stagger lines instead.

```javascript
// Characters for hero headlines only
const titleSplit = new SplitText('.hero-title', { type: 'chars,words' });
titleSplit.chars.forEach(char => char.classList.add('text-gradient'));
gsap.from(titleSplit.chars, { yPercent: 100, duration: 1.5, ease: 'expo.out', stagger: 0.04 });

// Lines for paragraphs — NEVER stagger characters on long text
const subtitleSplit = new SplitText('.subtitle', { type: 'lines' });
gsap.from(subtitleSplit.lines, { opacity: 0, yPercent: 100, duration: 1.8, ease: 'expo.out', stagger: 0.08, delay: 0.5 });
```

---

### Scroll Storytelling Patterns

#### Video Scrubbing

Re-encode video so every frame is a keyframe. Without this, scroll-bound playback
is jittery.

```bash
ffmpeg -i input.mp4 -g 1 -codec:v libx264 -crf 18 output.mp4
```

`-g 1` = GOP size 1 (every frame is an I-frame). `-crf 18` = near-lossless.

```javascript
const videoRef = useRef();

useGSAP(() => {
  const video = videoRef.current;
  if (!video) return;
  video.onloadedmetadata = () => {
    gsap.to(video, {
      currentTime: video.duration,
      ease: 'none',
      scrollTrigger: {
        trigger: '#hero', start: 'top top', end: 'bottom top',
        scrub: 1, pin: true, pinSpacer: true
      }
    });
  };
});
```

Always: `muted playsInline preload="auto"`. Never: `controls` on hero videos.

**Premium materials (see motion-design.md > Premium Motion Materials):**
Beyond transform/opacity: blur reveals, backdrop-filter, saturation shifts,
shadow bloom, SVG filters, masks, clip paths, gradient-position shifts.

#### Hero Video Scrub Pattern

Three layers combined in one `useGSAP` block. Use the SplitText and Parallax
patterns from above, then add the video scrub:

```javascript
// 3. Video scrub (add to the same useGSAP block as SplitText + parallax)
const video = videoRef.current;
if (video) {
  video.onloadedmetadata = () => {
    gsap.to(video, {
      currentTime: video.duration, ease: 'none',
      scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: 1, pin: true, pinSpacer: true }
    });
  };
}
```

Structure: `relative w-full h-screen overflow-hidden`. Video as absolute background.
Content layered on top with `relative z-10`. Parallax elements `absolute` off-screen.

#### Navbar Glassy Blur

```javascript
useGSAP(() => {
  gsap.fromTo(navRef.current,
    { backgroundColor: 'rgba(0,0,0,0)', backdropFilter: 'blur(0px)' },
    {
      backgroundColor: 'rgba(0,0,0,0.4)', backdropFilter: 'blur(12px)',
      borderBottom: '1px solid rgba(255,255,255,0.1)',
      duration: 0.5,
      scrollTrigger: { trigger: 'body', start: 'top -50px', end: 'top -100px', scrub: true }
    }
  );
});
```

#### Parallax Leaves

```javascript
gsap.timeline({ scrollTrigger: { trigger: section, start: 'top bottom', end: 'bottom top', scrub: true } })
  .from('.left-leaf', { xPercent: -100, yPercent: 40, rotate: -45 }, 0)
  .from('.right-leaf', { xPercent: 100, yPercent: 40, rotate: 45 }, 0);
```

Position with `absolute pointer-events-none`. Offset off-screen initially so they
emerge naturally.

#### Image Mask Expansion

Pin section, fade ambient copy, scale CSS mask to 400% to reveal background:

```javascript
const tl = gsap.timeline({
  scrollTrigger: { trigger: section, start: 'top top', end: 'bottom top', scrub: 1.5, pin: true }
});

tl.to('.will-fade', { opacity: 0, stagger: 0.1, duration: 1 })
  .to('.mask-target', { scale: 1.4, webkitMaskSize: '400%', maskSize: '400%', duration: 2.5, ease: 'power1.inOut' }, '-=0.5')
  .to('.masked-content', { opacity: 1, y: 0, duration: 1.5 }, '-=1');
```

#### Video Mask Reveal

Pin section. Scale mask SVG from `1 → 12`. Fade content in at `'-=0.5'`.

```javascript
const tl = gsap.timeline({
  scrollTrigger: { trigger: section, start: 'top top', end: 'bottom top', scrub: true, pin: true }
});

tl.to('.mask-img', { scale: 12, duration: 2, ease: 'power1.inOut' })
  .to('.showcase-content', { opacity: 1, y: 0, duration: 1, ease: 'power1.inOut' }, '-=0.5');
```

#### Interface Scatter

Surrounding screenshots start at center, scatter outward on scroll:

```javascript
const screenOffsets = [
  { id: 'screen-1', x: -280, y: -180 },
  { id: 'screen-2', x: 280, y: -180 },
  { id: 'screen-3', x: -280, y: 180 },
  { id: 'screen-4', x: 280, y: 180 },
];

const tl = gsap.timeline({
  scrollTrigger: { trigger: section, start: 'top bottom', end: 'center center', scrub: 1 }
});

screenOffsets.forEach((screen) => {
  tl.fromTo(`.${screen.id}`,
    { x: 0, y: 0, opacity: 0, scale: 0.5 },
    { x: screen.x, y: screen.y, opacity: 1, scale: 1, duration: 2 },
    0  // All start simultaneously at time 0
  );
});
```

#### Bento Grid Reveals

```javascript
gsap.fromTo('.bento-card',
  { opacity: 0, y: 40 },
  {
    opacity: 1, y: 0, duration: 1, stagger: 0.25, ease: 'power2.out',
    scrollTrigger: {
      trigger: container, start: isMobile ? 'top bottom' : 'top 80%',
      toggleActions: 'play none none none'
    }
  }
);
```

Layout: `grid grid-cols-1 md:grid-cols-2 gap-6`. Cards:
`bg-neutral-900/50 border border-neutral-800 rounded-3xl p-8`.

#### Infinite Slider with Modulo

Given array length $L$ and arbitrary index $I$ (positive or negative):

$$NewIndex = (I \bmod L + L) \bmod L$$

```javascript
const getItemAt = (offset) => items[((currentIndex + offset) % items.length + items.length) % items.length];
```

Wraps infinitely in both directions. No boundary checks needed.

Complete slider with GSAP transitions:

```javascript
// State: currentIndex drives which item is visible
const [currentIndex, setCurrentIndex] = useState(0);

// Modulo accessor — wraps infinitely in both directions
const getItemAt = (offset) => {
  const len = items.length;
  return items[((currentIndex + offset) % len + len) % len];
};

// Navigation — modulo wraps index
const goToSlide = (newIndex) => {
  const len = items.length;
  setCurrentIndex(((newIndex % len) + len) % len);
};

// GSAP transitions on slide change
useGSAP(() => {
  gsap.fromTo('.slide-content', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8, ease: 'power2.out' });
  gsap.fromTo('.slide-visual', { opacity: 0, xPercent: -50, scale: 0.9 }, { opacity: 1, xPercent: 0, scale: 1, duration: 1, ease: 'power2.out' });
}, [currentIndex]);
```

Structure: 3-column grid (prev | current | next). Current item centered with
visual. Previous/Next buttons on sides. Tab bar above for direct access.
Use `getItemAt(-1)`, `getItemAt(0)`, `getItemAt(1)` for the three visible items.

---

### Layout Composition Patterns

These patterns structure the page. They are not animation — they are spatial design.
Apply them BEFORE adding motion.

**Design rules (from spatial-design.md):**
- Use 4pt base grid (4, 8, 12, 16, 24, 32, 48, 64, 96px) — not 8pt
- Name tokens semantically (`--space-sm`, `--space-lg`) not by value
- Cards are overused — use spacing and alignment for grouping first
- "Squint test": blur your screenshot. Can you identify the most important
  element? If everything looks the same weight, hierarchy is broken
- Hierarchy through multiple dimensions: combine size (3:1+), weight, color,
  position, and space — don't rely on size alone
- Self-adjusting grid: `repeat(auto-fit, minmax(280px, 1fr))` — responsive
  without breakpoints

**Masonry Grid:** Fixed column width, `fit-content` height. Natural aspect ratios.
No rigid cropping. `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`.

**Sticky Timeline:** Pin century digits with `position: sticky`. Let decade digits
scroll. Creates high readability and graphical continuity.

**Power Lines:** Invisible vertical/horizontal alignment vectors that persist across
sections. Distant elements share coordinates. Prevents disjointed-box feeling.

**Overlapping Typography:** Massive background text. Product pinned foreground.
Text slides underneath on scroll. **Rule:** Overlapping text must be non-critical.
Repeat important data elsewhere.

**Alternating Structural Focus:** Full-bleed visual → minimal text → raw video →
quiet text. Manages dopamine and focus levels. Never stack homogeneous blocks.

**OS Metaphor:** The interface behaves like a desktop operating system —
windows snap to edges, icons have context menus, sections feel like "apps"
you can open and close. Works for tech/creative brands. Breaks for luxury
(too playful) and restaurants (wrong context).

**Chaotic Masonry Grid:** A masonry grid with intentionally randomized sizes
and overlapping elements. Creates visual energy and editorial feel. Use for
creative/agency brands. Never for professional services (too messy).

**Boundary Snapping:** Content sections snap to fixed boundaries (left/right
edges, center line). Elements align to invisible grid lines that persist
across sections. Creates cohesion without explicit grid lines.

**Flag Grid:** Alternating rows of full-width and half-width elements.
Creates a flag-like visual rhythm. Works for portfolios and editorial sites.

**Navigation:** Never unconventional with primary nav. Standard, predictable
placement always. (`skills/ui-ux/reference/brand.md`: "Never unconventional with primary nav")

### Animation Sequencing

When multiple sections have scroll animations, orchestrate them so they don't
fight for attention:

**Rule 1: One focal point per viewport.** At any scroll position, the user should
be looking at ONE thing. If two sections animate simultaneously at the same
scroll position, the eye doesn't know where to go.

**Rule 2: Stagger section triggers.** Use different `start` values so sections
animate in sequence, not in parallel:
```
Section A: start: 'top 80%'    // Enters first
Section B: start: 'top 60%'    // Enters after A is visible
Section C: start: 'top 40%'    // Enters after B is visible
```

**Rule 3: Alternate intensity.** High-intensity section (pinned, scrubbed, 3D)
→ low-intensity section (fade-in, simple parallax) → high-intensity. Never
stack two high-intensity sections back-to-back.

**Rule 4: Use timeline overlap for choreography within a section.** Use
`'-=0.5'` to `'-=0.8'` for smooth cascading within ONE section. Don't use
overlap ACROSS sections — that creates the "everything at once" problem.

**Rule 5: Let the climax breathe.** The strongest visual (mask expansion, 3D
showcase, interface scatter) should be surrounded by quieter sections. Give
the user a moment before and after the peak.

---

### Mobile Performance Gating

```javascript
import { useMediaQuery } from 'react-responsive';

const isMobile = useMediaQuery({ query: '(max-width: 1024px)' });

useGSAP(() => {
  if (isMobile) return;  // Disable high-intensity scrubbing on mobile
  // ... scroll animations
}, { scope: containerRef, dependencies: [isMobile] });
```

On mobile: apply MOBILE SCROLL STRATEGY (see above). Disable pinned sections,
video scrubbing, and heavy 3D canvases. Replace with CSS reveal cascade
(`.reveal-on-scroll`) so each narrative act remains visually distinct.
Never collapse into a raw vertical stack. Preserve GPU battery.

### Performance Budgets

Specific limits to keep animations at 60fps:

| Resource | Budget | Why |
|----------|--------|-----|
| GSAP tweens active simultaneously | ≤ 20 | Each tween consumes a frame callback. Over 20, frame drops on mid-range devices. |
| ScrollTrigger instances per page | ≤ 15 | Each registers a scroll listener. Over 15, scroll jank on mobile. |
| Pinned sections | ≤ 3 | Each pin creates a spacer element and recalculates layout on scroll. |
| R3F draw calls | ≤ 50 | Each mesh = 1 draw call. Over 50, GPU-bound on mobile. |
| R3F triangles | ≤ 500K | Over 500K triangles = frame drops on mobile GPUs. |
| Video file size (scroll scrub) | ≤ 10MB | Larger files = longer load, janky scrub start. Re-encode with `-crf 23` if too large. |
| Video duration (scroll scrub) | 5-15 sec | Too short = jerky. Too long = file bloat. |
| DOM elements animated per section | ≤ 30 | Staggering 50+ elements kills performance. Use virtualization. |
| SplitText characters (hero) | ≤ 50 | Over 50 characters = stagger takes too long. Use lines instead. |
| 3D model file size (GLB) | ≤ 5MB | Over 5MB = slow initial load. Use Draco compression (`gltfjsx -T`). |

**When to cut:** If you exceed a budget, simplify. Remove a parallax layer.
Reduce stagger count. Use a static image instead of video. One strong animation
beats five weak ones.

---

## SECTION 3: 3D PRODUCT EXPERIENCES

The hands for 3D product showcases. Every pattern here serves the creative
direction from Section 1.

### Installation

```bash
npm install three @react-three/fiber @react-three/drei zustand clsx
```

### Zustand State Management

Use Zustand for 3D application state. Prevents re-render storms that kill 60fps
in R3F loops. Zero boilerplate. No Context Providers.

```javascript
import { create } from 'zustand';

export const useProductStore = create((set) => ({
  color: '#2e2c2e',       // Current product color
  activeModel: 'large',   // 'large' | 'small' — discrete, not float
  texture: '/videos/f1.mp4',
  setColor: (c) => set({ color: c }),
  setActiveModel: (m) => set({ activeModel: m }),
  setTexture: (t) => set({ texture: t }),
}));
```

**Critical:** Use precision selectors (`const { color } = useProductStore()`) —
only re-renders when `color` changes. Never subscribe to the full store in
render loops. Never wrap R3F Canvas in Context Providers.

### R3F Canvas & Camera

```jsx
import { Canvas } from '@react-three/fiber';

<Canvas camera={{ position: [0, 1.2, 3.5], fov: 45, near: 0.1, far: 100 }}>
  <StudioLights />
  <OrbitControls enableZoom={false} minPolarAngle={Math.PI / 3} maxPolarAngle={Math.PI / 2} />
  <ModelComponent scale={scale * 10} position={[0, -0.6, 0]} />
</Canvas>
```

| Camera Param | Effect |
|---|---|
| `position: [x, y, z]` | x=centered, y=elevation, z=distance from origin |
| `fov: 45-50` | Realistic perspective without extreme distortion |
| `near: 0.1, far: 100` | Clipping planes — keep tight for performance |

### 3D Model Pipeline

#### Convert with gltfjsx

```bash
npx gltfjsx public/models/model.glb -T
```

The `-T` flag: Draco compression, texture isolation, flattened nested groups,
lightweight output pointing to `transformed.glb`. Always use `-T` — without it,
the model is 3-5x larger and loads slowly.

#### Model Component with Custom Texture

```javascript
import { useEffect } from 'react';
import { useGLTF, useTexture } from '@react-three/drei';
import * as THREE from 'three';
import { useProductStore } from '../../store';

export default function ProductModel(props) {
  const { nodes, scene } = useGLTF('/models/model-transformed.glb');
  const texture = useTexture('/screen.png');
  const { color } = useProductStore();

  // Set correct color space — without this, screen renders washed out
  useEffect(() => {
    texture.colorSpace = THREE.SRGBColorSpace;
    texture.needsUpdate = true;
  }, [texture]);

  // Mutate outer shell color while protecting specific meshes
  useEffect(() => {
    const protectedParts = ['Screen', 'Keyboard', 'Trackpad', 'Ports', 'DisplayScreen'];
    scene.traverse((child) => {
      if (child.isMesh && !protectedParts.includes(child.name)) {
        child.material.color = new THREE.Color(color);
      }
    });
  }, [color, scene]);

  return (
    <group {...props} dispose={null}>
      <primitive object={scene} />
      <mesh geometry={nodes.ScreenMesh.geometry} position={nodes.ScreenMesh.position}>
        <meshBasicMaterial map={texture} />
      </mesh>
    </group>
  );
}

useGLTF.preload('/models/model-transformed.glb');
```

### Studio Lighting

Raw 3D models on black backgrounds look flat. Build Apple-standard studio lighting:

```jsx
import { Lightformer, Environment } from '@react-three/drei';

const StudioLights = () => (
  <group name="lights">
    <Environment resolution={256}>
      <group>
        <Lightformer form="rect" intensity={10} position={[-10, 5, -5]} scale={10} rotation-y={Math.PI / 2} />
        <Lightformer form="rect" intensity={10} position={[10, 0, 1]} scale={10} rotation-y={-Math.PI / 2} />
      </group>
    </Environment>
    <spotLight position={[-2, 10, 5]} angle={0.15} penumbra={1} decay={0} intensity={Math.PI * 0.2} castShadow />
    <spotLight position={[0, -25, 10]} angle={0.15} penumbra={1} decay={0} intensity={Math.PI * 0.2} />
    <spotLight position={[0, 15, 5]} angle={0.3} penumbra={1} decay={0.1} intensity={3} />
  </group>
);

export default StudioLights;
```

Lightformers inside `<Environment>` reflect realistic bright panels off metallic
meshes without hard shadows. Spotlights with high penumbra focus sharp reflections
on edges, hinges, and chassis borders.

**Brand adaptation (see `skills/ui-ux/reference/brand.md` > Color Strategies, color-and-contrast.md > Tinted Neutrals):**
- Luxury: Warm neutrals, tinted toward brand hue. Lower intensity (5-8), wider penumbra.
- Tech: Cool neutrals, high-contrast. Higher intensity (10-15), sharp penumbra.
- Creative: Experimental. Dynamic color shifts on lightformers.
- Restaurant: Warm amber, natural. Avoid harsh shadows.

**Tinted neutrals:** Never use pure gray (#808080) or pure black (#000). Add
chroma 0.005-0.015 hued toward the brand color. Even that small amount makes
3D scenes feel natural instead of lifeless.

### PresentationControls

Use for product showcases instead of `OrbitControls`. Physics-based snap-back
when released. Restricts vertical rotation. Allows full horizontal inspection.

```jsx
import { PresentationControls } from '@react-three/drei';

<PresentationControls
  global snap speed={1.2} zoom={1.0}
  polar={[-0.1, 0.4]}
  azimuth={[-Math.PI, Math.PI]}
  config={{ mass: 1, tension: 170, friction: 26 }}
>
  <ProductModel scale={0.08} />
</PresentationControls>
```

**Brand adaptation (see `skills/ui-ux/reference/brand.md` > Brand Register):**
- Luxury → slower speed (0.8), higher mass (2.0), tighter polar bounds
- Tech → faster speed (1.5), snappier tension (200)
- Creative → wider polar range, experimental interactions
- Restaurant → warm, slow, organic (usually skip 3D)

### Model Switching with GSAP

Fade meshes in/out across a 3D group hierarchy. Slide models along X-axis:

```javascript
const ANIMATION_DURATION = 1.0;
const OFFSET_DISTANCE = 5.0;

const fadeMeshes = (group, targetOpacity) => {
  if (!group) return;
  group.traverse((child) => {
    if (child.isMesh) {
      child.material.transparent = true;
      gsap.to(child.material, { opacity: targetOpacity, duration: ANIMATION_DURATION, ease: 'power2.inOut' });
    }
  });
};

const moveGroup = (group, targetX) => {
  if (!group) return;
  gsap.to(group.position, { x: targetX, duration: ANIMATION_DURATION, ease: 'power2.inOut' });
};
```

Complete ModelSwitcher pattern:

```javascript
// Use discrete indices, NOT float comparison (anti-pattern: scale === 0.08)
const [activeModel, setActiveModel] = useState('large'); // 'large' | 'small'

const largeRef = useRef(null);
const smallRef = useRef(null);
const isLargeActive = activeModel === 'large';

useGSAP(() => {
  if (isLargeActive) {
    moveGroup(largeRef.current, 0); fadeMeshes(largeRef.current, 1);
    moveGroup(smallRef.current, -OFFSET_DISTANCE); fadeMeshes(smallRef.current, 0);
  } else {
    moveGroup(smallRef.current, 0); fadeMeshes(smallRef.current, 1);
    moveGroup(largeRef.current, OFFSET_DISTANCE); fadeMeshes(largeRef.current, 0);
  }
}, [activeModel]);

// PresentationControls config — adapt to brand (see Brand Adaptation above)
const controlsConfig = {
  global: true, snap: true, speed: 1.2, zoom: 1.0,
  polar: [-0.1, 0.4], azimuth: [-Math.PI, Math.PI],
  config: { mass: 1, tension: 170, friction: 26 },
};
```

Structure: Two `<PresentationControls>` wrapping two `<group>` refs. Active model
at position `[0, 0, 0]`, inactive model offset to `[-OFFSET_DISTANCE, 0, 0]` or
`[OFFSET_DISTANCE, 0, 0]`. GSAP handles the slide and fade transition.

**Never compare floats for state.** Use discrete strings or indices:
`activeModel === 'large'` not `scale === 0.08`.

### Video Textures on 3D Screens

#### Preload on Mount

```javascript
useEffect(() => {
  paths.forEach((path) => {
    const v = document.createElement('video');
    v.src = path; v.preload = 'auto'; v.muted = true; v.playsInline = true; v.load();
  });
}, []);
```

#### Dynamic Texture Swap via Zustand

```javascript
const { texture } = useProductStore();
const videoTexture = useVideoTexture(texture, {
  unsuspended: 'play', muted: true, loop: true, playsInline: true
});
// Apply: <meshBasicMaterial map={videoTexture} toneMapped={false} />
```

#### Scroll-Triggered Texture Switching

Use GSAP timeline with `.call()` to swap textures at specific scroll coordinates:

```javascript
const tl = gsap.timeline({
  scrollTrigger: { trigger, start: 'top top', end: 'bottom top', scrub: true }
});

tl.call(() => setTexture('/videos/f1.mp4'), null, 0)
  .to('.box-1', { opacity: 1, y: 0, duration: 1 })
  .to('.box-1', { opacity: 0, y: -20, duration: 1 })
  .call(() => setTexture('/videos/f2.mp4'), null, 2)
  // ... repeat pattern for additional textures
```

#### Scroll-Driven 3D Model Rotation

```javascript
useFrame(() => {
  if (groupRef.current) {
    groupRef.current.rotation.y = (window.scrollY / 1000) * 0.8;
  }
});
// Bind to a <group ref={groupRef}> wrapping the model
```

### Product Viewer Assembly

Combine Zustand controls, R3F Canvas, lighting, and model switcher into one section:

```jsx
import { useMediaQuery } from 'react-responsive';
import { Canvas } from '@react-three/fiber';
import { useProductStore } from '../store';
import ModelSwitcher from './three/ModelSwitcher';
import StudioLights from './three/StudioLights';

const ProductViewer = () => {
  const { color, activeModel, setColor, setActiveModel } = useProductStore();
  const isMobile = useMediaQuery({ query: '(max-width: 1024px)' });

  if (isMobile) {
    return (
      <section id="product-viewer" className="w-full min-h-screen flex flex-col items-center justify-center">
        <h2 className="text-3xl font-semibold mb-4">Take a closer look.</h2>
        <img src="/images/product-static.jpg" alt="Product" className="max-w-md rounded-xl" />
      </section>
    );
  }

  return (
    <section id="product-viewer" className="w-full min-h-screen flex flex-col items-center pt-24 pb-12">
      <h2 className="text-3xl md:text-5xl font-semibold mb-6">Take a closer look.</h2>
      <p className="text-gray-400 text-sm mb-4">
        Product in {color === '#adb5bd' ? 'Silver' : 'Space Black'}
      </p>

      {/* Color swatches — discrete state, not float */}
      <div className="flex items-center gap-3 bg-neutral-900 px-4 py-2 rounded-full border border-neutral-800 mb-4">
        <button onClick={() => setColor('#adb5bd')}
          className="w-6 h-6 rounded-full bg-neutral-300 hover:scale-110 transition-transform"
          aria-label="Silver" />
        <button onClick={() => setColor('#2e2c2e')}
          className="w-6 h-6 rounded-full bg-neutral-800 border border-neutral-700 hover:scale-110 transition-transform"
          aria-label="Space Black" />
      </div>

      {/* Size toggles — discrete indices, not scale === 0.08 */}
      <div className="flex items-center bg-neutral-900 p-1 rounded-full border border-neutral-800 mb-8">
        <button onClick={() => setActiveModel('small')}
          className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all
            ${activeModel === 'small' ? 'bg-white text-black' : 'text-gray-400 hover:text-white'}`}>
          14-inch
        </button>
        <button onClick={() => setActiveModel('large')}
          className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all
            ${activeModel === 'large' ? 'bg-white text-black' : 'text-gray-400 hover:text-white'}`}>
          16-inch
        </button>
      </div>

      {/* R3F Canvas — Zustand setters trigger GSAP transitions in ModelSwitcher */}
      <div className="w-full max-w-[800px] h-[500px]">
        <Canvas camera={{ position: [0, 1.2, 3.5], fov: 45 }}>
          <StudioLights />
          <ModelSwitcher />
        </Canvas>
      </div>
    </section>
  );
};
```

Integration flow:
1. User clicks color swatch → `setColor()` updates Zustand store
2. Zustand triggers re-render → `ModelSwitcher` receives new `color` via `useProductStore()`
3. `useGSAP` in `ModelSwitcher` detects `color` change → `scene.traverse()` mutates mesh materials
4. User clicks size toggle → `setActiveModel()` updates store → GSAP slides/fades models

---

## SECTION 4: FRAMER MOTION (PRODUCT REGISTER)

For product-register surfaces (dashboards, apps, tools). Use `motion` library
for micro-interactions and state transitions. NOT for cinematic scroll storytelling.

(See product.md > Product Register for product-register motion rules.)

```bash
npm install motion
```

### The 8 Interactive States

See `skills/ui-ux/reference/interaction-design.md` for the full table of 8 interactive states (default, hover, focus, active, disabled, loading, error, success).

"The common miss: designing hover without focus, or vice versa. They're different. Keyboard users never see hover states."

### Focus Rings (from interaction-design.md)

**Never `outline: none` without replacement.** Use `:focus-visible`:

```css
button:focus { outline: none; }
button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

Focus ring design: high contrast (3:1 minimum), 2-3px thick, offset from
element, consistent across all interactive elements.

### Duration Guide

| Duration | Use Case |
|----------|----------|
| 100-150ms | Instant feedback (button press, toggle) |
| 200-300ms | State changes (hover, menu open, tooltip) |
| 300-500ms | Layout changes (accordion, modal, drawer) |
| 500-800ms | Entrance animations (page load, hero reveals) |

Exit animations are faster than entrances (~75% of enter duration).
"Timing matters more than easing."

### Easing (Product Register)

See `skills/ui-ux/reference/motion-design.md` for easing standards.
For product-register surfaces, use ONLY these two curves:

```css
--ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);    /* Smooth, refined (default) */
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);     /* Snappy, confident */
```

No bounce. No elastic. No spring.

### Reduced Motion (from motion-design.md)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Respect vestibular disorders (~35% of adults over 40).

### Framer Motion Patterns

#### State Transitions

Animate between loading, empty, error, and success states:

```jsx
import { motion, AnimatePresence } from 'motion/react';

function DataState({ state, data, error }) {
  return (
    <AnimatePresence mode="wait">
      {state === 'loading' && (
        <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          transition={{ duration: 0.15 }}>
          <Skeleton />
        </motion.div>
      )}
      {state === 'error' && (
        <motion.div key="error" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}>
          <ErrorMessage error={error} />
        </motion.div>
      )}
      {state === 'success' && (
        <motion.div key="success" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2, ease: [0.25, 1, 0.5, 1] }}>
          <DataView data={data} />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

#### Modal / Drawer

```jsx
// Backdrop
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
  transition={{ duration: 0.2 }} className="fixed inset-0 bg-black/50" />

// Modal panel
<motion.div initial={{ opacity: 0, scale: 0.95, y: 20 }} animate={{ opacity: 1, scale: 1, y: 0 }}
  exit={{ opacity: 0, scale: 0.95, y: 20 }}
  transition={{ duration: 0.25, ease: [0.25, 1, 0.5, 1] }}
  className="fixed inset-0 flex items-center justify-center">
  <div className="bg-white rounded-xl p-6 max-w-md w-full">{children}</div>
</motion.div>
```

#### Hover Card Lift

```jsx
<motion.div whileHover={{ y: -4, boxShadow: '0 12px 24px rgba(0,0,0,0.15)' }}
  transition={{ duration: 0.2, ease: [0.25, 1, 0.5, 1] }}
  className="bg-white rounded-xl p-6 shadow-sm">
  {children}
</motion.div>
```

#### Staggered List Entrance

```jsx
const listVariants = { hidden: {}, visible: { transition: { staggerChildren: 0.05 } } };
const itemVariants = { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: [0.25, 1, 0.5, 1] } } };

<motion.ul variants={listVariants} initial="hidden" animate="visible">
  {items.map(item => <motion.li key={item.id} variants={itemVariants}>{item.name}</motion.li>)}
</motion.ul>
```

#### Tab Indicator

```jsx
<motion.div layoutId="tab-indicator" className="absolute bottom-0 h-0.5 bg-blue-600"
  transition={{ type: 'spring', stiffness: 300, damping: 30 }} />
```

#### Page Transition

```jsx
<motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
  exit={{ opacity: 0, x: -20 }}
  transition={{ duration: 0.3, ease: [0.25, 1, 0.5, 1] }}>
  {pageContent}
</motion.div>
```

---

## SECTION 5: ASSET PLANNING

Some animations need external assets. This section classifies what code creates
vs what you need from outside, and generates prompts for AI tools.

### Asset Classification

Go through each section of the scroll narrative and classify:

| Pattern | Code Creates | External Asset Needed |
|---------|-------------|---------------------|
| Hero with video scrub | GSAP timeline, pinning, scroll binding | MP4 video (5-15 sec, re-encoded with FFmpeg) |
| Hero with text reveal | SplitText, easing, stagger | Nothing — pure code |
| Hero with image | CSS transforms, parallax | Hero image (Unsplash or user-provided) |
| Parallax leaves | GSAP parallax timeline | Leaf/product PNG images (transparent bg) |
| Image mask expansion | GSAP mask scaling | Mask SVG shape + background image |
| Video mask reveal | GSAP mask scaling | Mask SVG + background video |
| 3D product viewer | R3F canvas, lighting, controls | GLB/GLTF 3D model file |
| 3D with video texture | R3F + useVideoTexture | GLB model + MP4 videos for screen |
| Bento grid | GSAP stagger reveals | Icons/images for cards (Unsplash or SVG) |
| Interface scatter | GSAP fromTo scatter | 4-6 screenshot PNGs |
| Infinite slider | GSAP transitions, modulo | Product images (user-provided) |
| Background texture | SVG noise filter (code) | Nothing — code generates |
| Navbar blur | GSAP fromTo | Nothing — pure code |
| Framer Motion states | AnimatePresence, variants | Nothing — pure code |

### Image Generation Briefs

For images that need AI generation or enhancement (Figma AI, Midjourney,
DALL-E, etc.), brief the user with this structure:

**Image brief template:**
- Subject: [what's in the image]
- Setting: [background/environment]
- Lighting: [warm, cool, dramatic, soft, golden hour, studio]
- Mood: [emotional tone — calm, confident, energetic, luxurious]
- Color palette: [dominant colors from DESIGN.md]
- Style: [editorial photography, lifestyle, product-focused, abstract, minimalist]
- Dimensions: [aspect ratio — 16:9 for hero, 1:1 for products, 4:3 for features]

**Example — Luxury wellness hero:**
- Subject: Glass bottle of face serum on marble surface
- Setting: Clean marble surface, soft bokeh background
- Lighting: Golden hour from the left, warm and diffused
- Mood: Calm, luxurious, trustworthy
- Color palette: Cream (#FAF7F2), warm sand (#E8DFD0), gold (#C4A77D)
- Style: Editorial photography, minimal, clean
- Dimensions: 16:9

**Guide the user:** "Create this in Figma using your preferred image model.
Adjust the background, angles, and lighting as needed. Remove the background
if you want to overlay it on a different surface."

### AI Video Prompt Template

For sections that need video (hero video scrub, video mask reveal, 3D screen
textures), generate a prompt for the user to create with their preferred tool
(Kling AI, Google Veo, Runway, etc.).

```
[Tech Report]
Duration: [X seconds]
Style: [visual style description]
Camera: [camera movement]
Subject: [what's in the frame]
Background: [background description]
Lighting: [lighting description]
Mood: [emotional tone]
Colors: [dominant colors, matching brand palette]
Start frame: [description or reference image]
End frame: [description or reference image]
```

**Example — Luxury wellness coach:**
```
[Tech Report]
Duration: 5 seconds
Style: Cinematic, warm, soft focus
Camera: Slow dolly forward, barely perceptible
Subject: Hands placing smooth stones on a warm wooden surface
Background: Soft bokeh, warm natural light
Lighting: Golden hour, diffused window light from the left
Mood: Calm, trustworthy, meditative
Colors: Warm beige (#F5F0E8), soft sage (#A8B5A0), honey gold (#D4A574)
Start frame: Wide shot of the stone arrangement
End frame: Close-up of the final stone being placed
```

**Example — Tech startup:**
```
[Tech Report]
Duration: 8 seconds
Style: Abstract, futuristic, dark
Camera: Slow orbit around a central data cluster
Subject: Flowing particle system forming data visualizations
Background: Deep black (#0A0A0A) with subtle grid lines
Lighting: Cool blue (#3B82F6) and purple (#8B5CF6) rim lighting
Mood: Innovative, precise, cutting-edge
Colors: Deep black, electric blue, soft purple, white accents
Start frame: Scattered particles in space
End frame: Particles coalescing into a clean dashboard UI
```

### 3D Model Requirements Template

For sections that need a 3D model:

```
3D Model Requirements:
- Object: [what the model is]
- Format: GLB or GLTF
- Polygon budget: [low/medium/high]
- Textures: [what textures are needed]
- Screen mesh: [if video texture will be mapped, name the mesh]
- Source: [where to get it — Readyform, Sketchfab, user-created]
- Notes: [special requirements]
```

### Placeholder Strategy

While waiting for real assets, use placeholders so code can be built and previewed:

| Asset Type | Placeholder |
|-----------|------------|
| Hero video | Solid black div with brand color gradient |
| Product images | Unsplash images matching the brand tone |
| 3D model | Colored cube or sphere in R3F canvas |
| Food/product photos | Unsplash with descriptive search terms |
| Background videos | Solid color with CSS gradient animation |

Use Unsplash URL format:
```
https://images.unsplash.com/photo-{id}?auto=format&fit=crop&w=1600&q=80
```

Search for the brand's physical object, not the generic category.

### Asset Integration

When the user provides real assets, swap placeholders:

1. **Video files:** Replace placeholder div → `<video>` element. Re-encode with
   `ffmpeg -i input.mp4 -g 1 -codec:v libx264 -crf 18 output.mp4`
2. **Images:** Replace Unsplash URLs → user-provided paths in `/public/images/`
3. **3D models:** Replace placeholder geometry → `useGLTF(modelPath)`. Run
   `npx gltfjsx public/models/model.glb -T` to generate React component
4. **Video textures:** Replace placeholder material → `useVideoTexture(videoPath)`
5. **Test all swaps at mobile viewport** — assets may need different sizing
6. **Verify video autoplay** — must be `muted playsInline` for browser autoplay

### Output Template

Present to the user:

```markdown
## Assets Needed

### Code Creates (No Action Needed)
- [List of animations/patterns that are pure code]

### External Assets Required

#### 1. Hero Video
- Tool: Kling AI / Google Veo / Runway
- Prompt: [generated prompt]
- Duration: [X seconds]
- Format: MP4, will be re-encoded with `ffmpeg -g 1`
- Deliver: Place in `/public/videos/hero.mp4`

#### 2. Product Images
- Source: User photography or Unsplash placeholders
- Count: [X images]
- Style: [description]
- Deliver: Place in `/public/images/`

#### 3. 3D Model (Optional)
- Source: Readyform / Sketchfab / User-created
- Requirements: [generated requirements]
- Deliver: Place in `/public/models/`

### Placeholders Used Now
- [What placeholders are in place so code can be built]
- [When to swap for real assets]
```

---

## REFERENCES

These files are the knowledge base. The skill consults them at decision points
throughout. Do not duplicate their content — quote the key insight at the
decision point, then read the full file when deeper context is needed.

| Reference | When to Consult | Location |
|-----------|----------------|----------|
| `motion-design.md` | Choosing easing, duration, premium materials, stagger, reduced motion | `skills/ui-ux/reference/motion-design.md` |
| `brand.md` | Font selection, color strategies, brand permissions, imagery, slop test | `skills/ui-ux/reference/brand.md` |
| `product.md` | Product register rules, product bans, system fonts, restrained motion | `skills/ui-ux/reference/product.md` |
| `spatial-design.md` | Grid systems, visual hierarchy, squint test, container queries | `skills/ui-ux/reference/spatial-design.md` |
| `interaction-design.md` | 8 interactive states, focus rings, form design, modals | `skills/ui-ux/reference/interaction-design.md` |
| `color-and-contrast.md` | OKLCH, tinted neutrals, palette structure, contrast ratios | `skills/ui-ux/reference/color-and-contrast.md` |

---

## ANTI-PATTERNS

| Vibe Coding (Anti-Pattern) | Cinematic Standard (Engineering) |
|---|---|
| `useEffect` for GSAP animations | `useGSAP` hook with automatic cleanup and scope |
| `document.querySelector` in React | `useRef` + scoped container selection |
| Standard MP4 for scroll scrubbing | FFmpeg re-encode with `-g 1` (GOP=1 keyframes) |
| Pinning heavy animations on mobile | `useMediaQuery` guard disables scrubbing on tablets/mobile |
| Staggering characters in long paragraphs | Split into lines, stagger lines instead |
| Embedding static copy in JSX | Separate into `constants/index.js` schema |
| Unconventional primary nav placement | Standard, predictable navigation location |
| Exact float comparison for state (`=== 0.08`) | Use discrete option indices (`"14"` vs `"16"`) |
| `OrbitControls` for product showcases | `PresentationControls` with snap physics |
| Hardcoded single mesh opacity | `scene.traverse()` fading all `isMesh` children |
| Textures without color space | Set `texture.colorSpace = THREE.SRGBColorSpace` |
| No video preloading before texture swap | `createElement('video')` + `preload='auto'` + `load()` on mount |
| R3F Canvas wrapped in Context Providers | Zustand precision selectors |
| Bounce/elastic easing on luxury brands | Match easing to brand personality (see Matrix) |
| Cinematic parallax on dashboards | Respect register — product gets functional motion |
| Animation without `prefers-reduced-motion` | Provide crossfade alternatives, not just `animation: none` |

---

## OUTPUT SHAPE

**Simple section:** Component → `useGSAP` hook → ScrollTrigger config → JSX with Tailwind
**Scroll sequence:** Timeline with chained tweens → staggered reveals → overlapping `-=` offsets
**3D product viewer:** Zustand store → R3F Canvas → StudioLights → PresentationControls → Model component
**Full page:** Navbar (glassy blur) → Hero (video scrub) → Content sections (parallax/mask/scatter) → 3D viewer → Bento grid → Footer → Deploy

---

## NON-NEGOTIABLE CHECKLIST

- [ ] Register detected (brand vs product) before choosing motion vocabulary
- [ ] Brand-to-motion matrix consulted for easing, speed, density decisions
- [ ] Scroll narrative architecture applied (hook → build → climax → resolve)
- [ ] All GSAP wrapped in `useGSAP` with `{ scope: ref }`
- [ ] `gsap.registerPlugin(ScrollTrigger, SplitText)` at module top
- [ ] Scrub animations gated behind `useMediaQuery` for mobile
- [ ] Video scrub files re-encoded with `ffmpeg -g 1`
- [ ] `SplitText` uses lines for paragraphs, characters only for headlines
- [ ] Timeline overlaps use `-=0.5` to `-=0.8` for smooth choreography
- [ ] Constants separated from components in `constants/index.js`
- [ ] Primary navigation in standard, predictable location
- [ ] 3D screen textures set to `THREE.SRGBColorSpace`
- [ ] 3D models preloaded with `useGLTF.preload()`
- [ ] Video textures preloaded via virtual `<video>` elements on mount
- [ ] `PresentationControls` used over `OrbitControls` for product configurators
- [ ] Material opacity changes use `scene.traverse()`, not hardcoded single-mesh refs
- [ ] `gltfjsx -T` flag used for Draco compression
- [ ] Zustand selectors are precision slices (no full-store subscriptions in render loops)
- [ ] `prefers-reduced-motion` respected with crossfade alternatives
- [ ] Production build (`npm run build`) compiles without errors
- [ ] HTTPS/SSL configured for production deployment

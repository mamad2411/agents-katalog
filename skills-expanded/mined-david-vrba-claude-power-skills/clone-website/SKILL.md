---
name: clone-website
description: Reverse-engineer and rebuild a website as a pixel-perfect clone in one pass — extracts assets, CSS, animations, and content section-by-section and dispatches parallel builder agents in worktrees as it goes. Use whenever the user wants to clone, replicate, rebuild, reverse-engineer, or copy any web page. Provide the target URL as the argument.
---

# Clone Website

You are about to reverse-engineer and rebuild **$ARGUMENTS** as a pixel-perfect clone.

This is not a two-phase process (inspect then build). You are a **foreman walking the job site** — as you inspect each section of the page, you write a detailed specification to a file, then hand that file to a specialist builder agent with everything they need. Extraction and construction happen in parallel, but extraction is meticulous and produces auditable artifacts.

## Scope Defaults

The target is whatever page `$ARGUMENTS` resolves to. Clone exactly what's visible at that URL. Unless the user specifies otherwise, use these defaults:

- **Fidelity level:** Pixel-perfect — exact match in colors, spacing, typography, animations
- **In scope:** Visual layout and styling, component structure and interactions, responsive design, animations, scroll behaviors, mock data for demo purposes
- **Out of scope:** Real backend / database, authentication, real-time features, SEO optimization, accessibility audit
- **Customization:** None — pure emulation

If the user provides additional instructions (specific fidelity level, customizations, extra context), honor those over the defaults.

## Pre-Flight

1. **Browser automation is required.** Check for available browser MCP tools (Chrome MCP, Playwright MCP, Browserbase MCP, Puppeteer MCP, etc.). Use whichever is available — if multiple exist, prefer Chrome MCP. If none are detected, ask the user which browser tool they have and how to connect it. This skill cannot work without browser automation.
2. Verify the target URL from `$ARGUMENTS` is valid and accessible via your browser MCP tool.
3. Verify the base project builds: `npm run build`. The Next.js + shadcn/ui + Tailwind v4 scaffold should already be in place. If not, tell the user to set it up first.
4. Create the output directories if they don't exist: `docs/research/`, `docs/research/components/`, `docs/design-references/`, `scripts/`.

## Guiding Principles

These are the truths that separate a successful clone from a "close enough" mess. Internalize them — they should inform every decision you make.

### 1. Completeness Beats Speed

Every builder agent must receive **everything** it needs to do its job perfectly: screenshot, exact CSS values, downloaded assets with local paths, real text content, component structure. If a builder has to guess anything — a color, a font size, a padding value — you have failed at extraction. Take the extra minute to extract one more property rather than shipping an incomplete brief.

### 2. Small Tasks, Perfect Results

When an agent gets "build the entire features section," it glosses over details — it approximates spacing, guesses font sizes, and produces something "close enough" but clearly wrong. When it gets a single focused component with exact CSS values, it nails it every time.

Look at each section and judge its complexity. A simple banner with a heading and a button? One agent. A complex section with 3 different card variants, each with unique hover states and internal layouts? One agent per card variant plus one for the section wrapper. When in doubt, make it smaller.

**Complexity budget rule:** If a builder prompt exceeds ~150 lines of spec content, the section is too complex for one agent. Break it into smaller pieces.

### 3. Real Content, Real Assets

Extract the actual text, images, videos, and SVGs from the live site. This is a clone, not a mockup. Use `element.textContent`, download every `<img>` and `<video>`, extract inline `<svg>` elements as React components. The only time you generate content is when something is clearly server-generated and unique per session.

**Layered assets matter.** A section that looks like one image is often multiple layers — a background watercolor/gradient, a foreground UI mockup PNG, an overlay icon. Inspect each container's full DOM tree and enumerate ALL `<img>` elements and background images within it, including absolutely-positioned overlays.

### 4. Foundation First

Nothing can be built until the foundation exists: global CSS with the target site's design tokens (colors, fonts, spacing, keyframes), TypeScript types, and global assets. This is sequential and non-negotiable. Everything after this can be parallel.

### 5. Extract How It Looks AND How It Behaves — Including Every Animation

A website is not a screenshot — it's a living thing. Elements move, change, appear, and disappear in response to scrolling, hovering, clicking, resizing, and time. If you only extract the static CSS of each element, your clone will look right in a screenshot but feel dead when someone actually uses it.

For every element, extract its **appearance** (exact computed CSS via `getComputedStyle()`) AND its **behavior** (what changes, what triggers the change, and how the transition happens). Not "it looks like 16px" — extract the actual computed value. Not "the nav changes on scroll" — document the exact trigger, the before and after states, and the transition.

**Animation fidelity is non-negotiable.** Every `@keyframes` animation, every CSS transition, every scroll-driven animation, every GSAP tween parameter must be captured. See the dedicated **Animation Extraction** section for systematic procedures.

Examples of behaviors to watch for:
- A navbar that shrinks, changes background, or gains a shadow after scrolling past a threshold
- Elements that animate into view when they enter the viewport (fade-up, slide-in, stagger delays)
- Sections that snap into place on scroll (`scroll-snap-type`)
- Parallax layers that move at different rates than the scroll
- Hover states that animate (the transition duration and easing matter, not just the end value)
- Dropdowns, modals, accordions with enter/exit animations
- Scroll-driven progress indicators or opacity transitions
- Auto-playing carousels or cycling content
- Dark-to-light (or any theme) transitions between page sections
- **Tabbed/pill content that cycles** — buttons that switch visible card sets with transitions
- **Scroll-driven tab/accordion switching** — sidebars where the active item auto-changes as content scrolls past
- **Smooth scroll libraries** (Lenis, Locomotive Scroll) — check for `.lenis` class or scroll container wrappers
- **Custom cursors** — a div that follows the mouse, changes shape on hover
- **CSS scroll-driven animations** (native) — `animation-timeline: scroll()` or `view-timeline` on elements

### 6. Identify the Interaction Model Before Building

This is the single most expensive mistake in cloning: building a click-based UI when the original is scroll-driven, or vice versa. Before writing any builder prompt for an interactive section, you must definitively answer: **Is this section driven by clicks, scrolls, hovers, time, or some combination?**

How to determine this:
1. **Don't click first.** Scroll through the section slowly and observe if things change on their own as you scroll.
2. If they do, it's scroll-driven. Extract the mechanism: `IntersectionObserver`, `scroll-snap`, `position: sticky`, `animation-timeline`, or JS scroll listeners.
3. If nothing changes on scroll, THEN click/hover to test for click/hover-driven interactivity.
4. Document the interaction model explicitly in the component spec.

A section with a sticky sidebar and scrolling content panels is fundamentally different from a tabbed interface. Getting this wrong means a complete rewrite, not a CSS tweak.

### 7. Extract Every State, Not Just the Default

Many components have multiple visual states — a tab bar shows different cards per tab, a header looks different at scroll position 0 vs 100, a card has hover effects. You must extract ALL states.

For tabbed/stateful content: click each tab/button, extract the content and styles for EACH state. For scroll-dependent elements: capture at scroll 0, then scroll past the trigger and capture again. The diff between states IS the behavior specification.

### 8. Spec Files Are the Source of Truth

Every component gets a specification file in `docs/research/components/` BEFORE any builder is dispatched. The builder receives the spec file contents inline in its prompt. No guessing. No "go read the spec file." Everything inline.

### 9. Build Must Always Compile

Every builder agent must verify `npx tsc --noEmit` passes before finishing. After merging worktrees, verify `npm run build` passes. A broken build is never acceptable.

---

## Phase 0: Pre-Navigation Instrumentation

**Before navigating to the target URL**, inject these interception scripts using browser MCP's `addInitScript` (or equivalent). These scripts capture animation parameters that would otherwise be invisible — they must be in place BEFORE the page loads, or they miss the initialization calls.

### GSAP Tween Interception

```javascript
// Inject BEFORE navigation — intercepts all gsap.to/from/fromTo calls
window.__cloneCapture = { tweens: [], timelines: [], scrollTriggers: [] };

document.addEventListener('DOMContentLoaded', () => {
  if (!window.gsap) return;
  const wrap = (fn, type) => (target, ...args) => {
    try {
      const vars = args[args.length - 1];
      window.__cloneCapture.tweens.push({
        type,
        target: typeof target === 'string' ? target : (target?.className || target?.id || String(target).slice(0, 80)),
        vars: JSON.parse(JSON.stringify(vars || {})),
      });
    } catch {}
    return fn.call(window.gsap, target, ...args);
  };
  gsap.to   = wrap(gsap.to.bind(gsap), 'to');
  gsap.from = wrap(gsap.from.bind(gsap), 'from');
  gsap.fromTo = (t, f, v) => {
    try { window.__cloneCapture.tweens.push({ type: 'fromTo', target: String(t?.className || t).slice(0, 80), from: JSON.parse(JSON.stringify(f || {})), vars: JSON.parse(JSON.stringify(v || {})) }); } catch {}
    return gsap.fromTo.originalFn(t, f, v);
  };
});
```

### IntersectionObserver Interception

```javascript
// Inject BEFORE navigation — captures all IntersectionObserver registrations
window.__ioCapture = [];
const _OrigIO = window.IntersectionObserver;
window.IntersectionObserver = function(callback, options) {
  window.__ioCapture.push({
    options,
    callbackPreview: callback.toString().slice(0, 600),
  });
  return new _OrigIO(callback, options);
};
```

After the page loads and settles, retrieve the captured data:
```javascript
// Run AFTER page settles
JSON.stringify({ tweens: window.__cloneCapture, observers: window.__ioCapture }, null, 2)
```

Save to `docs/research/animation-capture.json`.

---

## Phase 1: Reconnaissance

Navigate to the target URL with browser MCP.

### Screenshots
- Take **full-page screenshots** at desktop (1440px) and mobile (390px) viewports
- Save to `docs/design-references/` with descriptive names
- These are your master reference — builders will receive section-specific crops later

### Tech Stack Detection

Run this via browser MCP immediately after page load:

```javascript
(() => ({
  // Frameworks
  react: !!(window.React || window.__REACT_DEVTOOLS_GLOBAL_HOOK__),
  nextjs: !!window.__NEXT_DATA__,
  vue: !!(window.Vue || window.__vue_app__),
  // Animation libraries
  gsap: !!window.gsap, gsapVersion: window.gsap?.version,
  gsapScrollTrigger: !!(window.ScrollTrigger || window.gsap?.plugins?.scrollTrigger),
  framerMotion: !!document.querySelector('[data-framer-component-type]'),
  animejs: !!window.anime,
  lottie: !!(window.lottie || window.bodymovin),
  // Scroll libraries
  lenis: !!(window.lenis || window.Lenis || document.documentElement.classList.contains('lenis')),
  locomotive: !!document.querySelector('.c-scrollbar, [data-scroll-container]'),
  // 3D / WebGL
  threeJs: !!window.THREE, pixiJs: !!window.PIXI,
  spline: !!document.querySelector('spline-viewer'),
  hasCanvas: !!document.querySelector('canvas'),
  // CSS capabilities
  nativeScrollDrivenAnimations: CSS.supports('animation-timeline: scroll()'),
  // Special elements
  hasCustomCursor: [...document.querySelectorAll('*')].some(el => getComputedStyle(el).cursor === 'none' && !['INPUT','TEXTAREA'].includes(el.tagName)),
  hasVideoBackground: !!document.querySelector('video[autoplay], video[muted]'),
  hasStickyNav: !!(document.querySelector('nav, header') && ['sticky','fixed'].includes(getComputedStyle(document.querySelector('nav, header')).position)),
  googleFonts: !!document.querySelector('link[href*="fonts.googleapis.com"]'),
}))()
```

Save to `docs/research/tech-stack.json`.

### Global Extraction
Extract these from the page before doing anything else:

**Fonts** — Inspect `<link>` tags for Google Fonts or self-hosted fonts. Check computed `font-family` on key elements (headings, body, code, labels). Document every family, weight, and style actually used. Configure them in `src/app/layout.tsx` using `next/font/google` or `next/font/local`.

**Colors** — Extract the site's color palette from computed styles across the page. Update `src/app/globals.css` with the target's actual colors in the `:root` and `.dark` CSS variable blocks. Map them to shadcn's token names where they fit.

```javascript
// Extract ALL CSS custom properties (design tokens) with resolved values
(() => {
  const rootStyle = getComputedStyle(document.documentElement);
  const allRules = [];
  for (const sheet of document.styleSheets) {
    try { allRules.push(...sheet.cssRules); } catch {}
  }
  const props = [...new Set(
    allRules.flatMap(r => r.style ? [...r.style] : []).filter(p => p.startsWith('--'))
  )];
  const tokens = {};
  props.forEach(p => { tokens[p] = rootStyle.getPropertyValue(p).trim(); });
  return JSON.stringify(tokens, null, 2);
})()
```

**Global @keyframes** — Extract ALL keyframe animation rules from all accessible stylesheets:

```javascript
(() => {
  const keyframes = {};
  const blocked = [];
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule.type === CSSRule.KEYFRAMES_RULE) {
          keyframes[rule.name] = rule.cssText;
        }
      }
    } catch { blocked.push(sheet.href); }
  }
  return JSON.stringify({ keyframes, blockedSheets: blocked }, null, 2);
})()
```

For any CORS-blocked sheets in `blockedSheets`: use browser MCP's network log to retrieve the CSS response body directly (it was already downloaded — CORS only blocks DOM API access). Extract @keyframes from those files manually by reading the response body text.

Save extracted @keyframes to `docs/research/keyframes.json`. These get added to `globals.css` during Phase 2.

**CSS Scroll-Driven Animations (native):**

```javascript
// Find all elements using animation-timeline or view-timeline
(() => {
  const results = [];
  // From stylesheets
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule.cssText?.includes('animation-timeline') || rule.cssText?.includes('view-timeline')) {
          results.push({ type: 'stylesheet-rule', cssText: rule.cssText });
        }
      }
    } catch {}
  }
  // From computed styles on elements
  [...document.querySelectorAll('*')].forEach(el => {
    const cs = getComputedStyle(el);
    const timeline = cs.getPropertyValue('animation-timeline');
    if (timeline && timeline !== 'none' && timeline !== 'auto') {
      results.push({
        type: 'element',
        selector: el.className || el.id || el.tagName,
        animationTimeline: timeline,
        animationRange: cs.getPropertyValue('animation-range'),
        animationName: cs.animationName,
      });
    }
  });
  return JSON.stringify(results, null, 2);
})()
```

**Favicons & Meta** — Download favicons, apple-touch-icons, OG images, webmanifest to `public/seo/`. Update `layout.tsx` metadata.

**Global UI patterns** — Identify any site-wide CSS or JS: custom scrollbar hiding, scroll-snap on the page container, global keyframe animations, backdrop filters, **smooth scroll libraries** (Lenis, Locomotive Scroll). Add these to `globals.css` and note any libraries that need to be installed.

### Mandatory Interaction Sweep

This is a dedicated pass AFTER screenshots and BEFORE anything else. Its purpose is to discover every behavior on the page.

**Scroll sweep:** Scroll the page slowly from top to bottom via browser MCP. At each section, pause and observe:
- Does the header change appearance? Record the scroll position where it triggers.
- Do elements animate into view? Record which ones and the animation type.
- Does a sidebar or tab indicator auto-switch as you scroll? Record the mechanism.
- Are there scroll-snap points? Record which containers.
- Is there a smooth scroll library active? Check for non-native scroll behavior.

**Click sweep:** Click every element that looks interactive:
- Every button, tab, pill, link, card
- Record what happens: does content change? Does a modal open? Does a dropdown appear?
- For tabs/pills: click EACH ONE and record the content that appears for each state

**Hover sweep:** Hover over every element that might have hover states:
- Buttons, cards, links, images, nav items
- Record what changes: color, scale, shadow, underline, opacity
- Record the transition timing: `getComputedStyle(el).transition`

**Responsive sweep:** Test at 3 viewport widths via browser MCP:
- Desktop: 1440px — Tablet: 768px — Mobile: 390px
- Note which sections change layout and at approximately which breakpoint

**Custom cursor check:** Look for elements with CSS `cursor: none` or divs with class names containing "cursor". If found, document the cursor's DOM structure, CSS, and how it follows the mouse.

**WebGL/Canvas check:** For any `<canvas>` element, identify the library:
```javascript
({ three: !!window.THREE, pixi: !!window.PIXI, spline: !!document.querySelector('spline-viewer'), p5: !!window.p5, vanta: !!window.VANTA, babylon: !!window.BABYLON })
```
- **Spline:** note the `scene` attribute URL on `<spline-viewer>` — reuse it directly
- **Vanta.js:** extract `window.VANTA[effect]._options` — reinstantiate with same parameters
- **Three.js/PIXI/unknown:** document in `docs/research/BEHAVIORS.md` as "requires visual fallback" (video capture or static image)

Save all findings to `docs/research/BEHAVIORS.md`. This is your behavior bible.

### Page Topology
Map out every distinct section of the page from top to bottom. Save as `docs/research/PAGE_TOPOLOGY.md`:
- Their visual order
- Which are fixed/sticky overlays vs. flow content
- The overall page layout (scroll container, column structure, z-index layers)
- Dependencies between sections
- **The interaction model** of each section (static, click-driven, scroll-driven, time-driven, GSAP-driven)

---

## Phase 2: Foundation Build

This is sequential. Do it yourself (not delegated to an agent) since it touches many files:

1. **Update fonts** in `layout.tsx` to match the target site's actual fonts
2. **Update globals.css** with the target's:
   - Color tokens (from the CSS custom properties extraction above)
   - Global `@keyframes` animations (from `keyframes.json`)
   - CSS scroll-driven animation rules (`animation-timeline`, `view-timeline`)
   - Utility classes and spacing values
   - Global scroll behaviors (Lenis initialization CSS, smooth scroll, scroll-snap on body)
3. **Install animation libraries** if detected:
   - GSAP (now fully free, including ScrollTrigger): `npm install gsap`
   - Lenis: `npm install lenis`
   - Framer Motion: `npm install framer-motion`
   - Anime.js: `npm install animejs`
4. **Create TypeScript interfaces** in `src/types/` for the content structures you've observed
5. **Extract SVG icons** — find all inline `<svg>` elements, deduplicate, save as named React components in `src/components/icons.tsx`
6. **Download global assets** — write and run a Node.js script (`scripts/download-assets.mjs`) that downloads all images, videos, and other binary assets to `public/`
7. Verify: `npm run build` passes

### Asset Discovery Script

```javascript
JSON.stringify({
  images: [...document.querySelectorAll('img')].map(img => ({
    src: img.src || img.currentSrc,
    alt: img.alt,
    width: img.naturalWidth, height: img.naturalHeight,
    parentClasses: img.parentElement?.className,
    siblings: img.parentElement ? [...img.parentElement.querySelectorAll('img')].length : 0,
    position: getComputedStyle(img).position,
    zIndex: getComputedStyle(img).zIndex,
  })),
  videos: [...document.querySelectorAll('video')].map(v => ({
    src: v.src || v.querySelector('source')?.src,
    poster: v.poster,
    autoplay: v.autoplay, loop: v.loop, muted: v.muted,
  })),
  backgroundImages: [...document.querySelectorAll('*')].filter(el => {
    const bg = getComputedStyle(el).backgroundImage;
    return bg && bg !== 'none';
  }).map(el => ({
    url: getComputedStyle(el).backgroundImage,
    element: el.tagName + (el.id ? '#' + el.id : '') + '.' + (el.className?.split(' ')[0] || ''),
  })),
  svgCount: document.querySelectorAll('svg').length,
  fonts: [...new Set([...document.querySelectorAll('*')].slice(0, 200).map(el => getComputedStyle(el).fontFamily))],
  favicons: [...document.querySelectorAll('link[rel*="icon"]')].map(l => ({ href: l.href, sizes: l.sizes?.toString() })),
  googleFontsLink: document.querySelector('link[href*="fonts.googleapis.com"]')?.href,
})
```

Then write a download script that fetches everything to `public/`. Use batched parallel downloads (4 at a time) with proper error handling.

### Smooth Scroll Library Initialization

If Lenis was detected, add this to the layout or a client component:

```typescript
// src/components/SmoothScrollProvider.tsx
'use client';
import { useEffect } from 'react';
import Lenis from 'lenis';

export function SmoothScrollProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const lenis = new Lenis({
      // Extract these values from the original site if accessible via window.lenis._options
      duration: 1.2,
      easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    });
    function raf(time: number) { lenis.raf(time); requestAnimationFrame(raf); }
    const id = requestAnimationFrame(raf);
    return () => { cancelAnimationFrame(id); lenis.destroy(); };
  }, []);
  return <>{children}</>;
}
```

---

## Phase 3: Component Specification & Dispatch

This is the core loop. For each section in your page topology (top to bottom), you do THREE things: **extract**, **write the spec file**, then **dispatch builders**.

### Step 1: Extract

For each section:

1. **Screenshot** the section in isolation. Save to `docs/design-references/`.

2. **Extract CSS** for every element using the extraction script:

```javascript
(function(selector) {
  const el = document.querySelector(selector);
  if (!el) return JSON.stringify({ error: 'Element not found: ' + selector });
  const props = [
    'fontSize','fontWeight','fontFamily','lineHeight','letterSpacing','color',
    'textTransform','textDecoration','backgroundColor','background',
    'padding','paddingTop','paddingRight','paddingBottom','paddingLeft',
    'margin','marginTop','marginRight','marginBottom','marginLeft',
    'width','height','maxWidth','minWidth','maxHeight','minHeight',
    'display','flexDirection','justifyContent','alignItems','alignSelf','gap',
    'gridTemplateColumns','gridTemplateRows','gridColumn','gridRow',
    'borderRadius','border','borderTop','borderBottom','borderLeft','borderRight',
    'boxShadow','overflow','overflowX','overflowY',
    'position','top','right','bottom','left','zIndex',
    'opacity','transform','transformOrigin','perspective','backfaceVisibility',
    'transition','animation','animationName','animationDuration',
    'animationTimingFunction','animationDelay','animationFillMode',
    'animationIterationCount','animationDirection','animationTimeline','animationRange',
    'cursor','objectFit','objectPosition','mixBlendMode','filter','backdropFilter',
    'willChange','contain','scrollSnapType','scrollSnapAlign','clipPath',
    'whiteSpace','textOverflow','WebkitLineClamp',
  ];
  function extractStyles(element) {
    const cs = getComputedStyle(element);
    const styles = {};
    props.forEach(p => {
      const v = cs[p];
      if (v && v !== 'none' && v !== 'normal' && v !== 'auto' && v !== '0px' && v !== 'rgba(0, 0, 0, 0)') styles[p] = v;
    });
    // Pseudo-elements
    const before = getComputedStyle(element, '::before');
    const after  = getComputedStyle(element, '::after');
    if (before.content !== 'none') styles['::before'] = { content: before.content, display: before.display, width: before.width, height: before.height, background: before.background, transform: before.transform };
    if (after.content  !== 'none') styles['::after']  = { content: after.content,  display: after.display,  width: after.width,  height: after.height,  background: after.background,  transform: after.transform  };
    return styles;
  }
  function walk(element, depth) {
    if (depth > 4) return null;
    const children = [...element.children];
    return {
      tag: element.tagName.toLowerCase(),
      classes: element.className?.toString().split(' ').slice(0, 5).join(' '),
      text: element.childNodes.length === 1 && element.childNodes[0].nodeType === 3 ? element.textContent.trim().slice(0, 200) : null,
      styles: extractStyles(element),
      images: element.tagName === 'IMG' ? { src: element.src, alt: element.alt, naturalWidth: element.naturalWidth, naturalHeight: element.naturalHeight } : null,
      childCount: children.length,
      children: children.slice(0, 20).map(c => walk(c, depth + 1)).filter(Boolean),
    };
  }
  return JSON.stringify(walk(el, 0), null, 2);
})('SELECTOR');
```

3. **Extract multi-state styles** — for any animated element, capture BOTH states:

```javascript
// STATE A — at scroll 0 (initial)
await page.evaluate(() => window.scrollTo(0, 0));
// Wait for any reverse-transition to complete
await page.waitForTimeout(500);
const stateA = // run extraction script on element

// Trigger the state (scroll past threshold, hover, click)
await page.evaluate(() => window.scrollTo(0, 150)); // adjust threshold
await page.waitForTimeout(600); // wait for transition to complete
const stateB = // run extraction script on element

// The diff between stateA and stateB IS the behavior specification
// Record: which properties changed, their before/after values, transition CSS
```

For hover states — use browser MCP hover, then immediately capture:
```javascript
// After page.hover(selector):
getComputedStyle(document.querySelector('SELECTOR')).transition
// Then capture the full style extraction — diff vs before-hover state
```

4. **Extract real content** — all text, alt attributes, aria labels. For tabbed/stateful content, **click each tab and extract content per state**.

5. **Identify assets** this section uses — which downloaded images/videos, which icon components from `icons.tsx`. Check for **layered images**.

6. **GSAP ScrollTrigger parameters** — if the section uses GSAP ScrollTrigger, extract from `docs/research/animation-capture.json` (captured in Phase 0) OR read the scroll trigger parameters directly:

```javascript
// Get all active ScrollTriggers on the page
window.ScrollTrigger?.getAll().map(st => ({
  trigger: st.trigger?.className || st.trigger?.id,
  start: st.start,
  end: st.end,
  scrub: st.vars?.scrub,
  pin: st.vars?.pin,
  animation: st.animation?.vars,
}))
```

7. **Assess complexity** — how many distinct sub-components? Apply the 150-line budget rule.

### Step 2: Write the Component Spec File

**File path:** `docs/research/components/<component-name>.spec.md`

```markdown
# <ComponentName> Specification

## Overview
- **Target file:** `src/components/<ComponentName>.tsx`
- **Screenshot:** `docs/design-references/<screenshot-name>.png`
- **Interaction model:** <static | click-driven | scroll-driven | time-driven | GSAP-driven>

## DOM Structure
<Describe the element hierarchy — what contains what>

## Computed Styles (exact values from getComputedStyle)

### Container
- display: ...
- padding: ...
- maxWidth: ...
(every relevant property with exact values)

### <Child element 1>
- fontSize: ...
- color: ...
(every relevant property)

## States & Behaviors

### <Behavior name, e.g., "Scroll-triggered floating mode">
- **Trigger:** <exact mechanism — scroll position 50px | IntersectionObserver rootMargin "-30% 0px" | hover | click>
- **State A (before):** maxWidth: 100vw, boxShadow: none, borderRadius: 0
- **State B (after):** maxWidth: 1200px, boxShadow: 0 4px 20px rgba(0,0,0,0.1), borderRadius: 16px
- **Transition:** transition: all 0.3s ease
- **Implementation approach:** <CSS transition + scroll listener | IntersectionObserver | CSS animation-timeline | GSAP ScrollTrigger>

### CSS Animations (if any)
- **Animation name:** <from @keyframes extraction — exact name>
- **animation-duration:** ...
- **animation-timing-function:** ...
- **animation-delay:** ...
- **animation-fill-mode:** ...
- **@keyframes body:** <paste verbatim from keyframes.json>

### GSAP (if any)
- **Tween type:** gsap.to / gsap.from / gsap.fromTo
- **Target selector:** ...
- **vars / from / to:** <exact parameters from animation-capture.json>
- **ScrollTrigger:** start: ..., end: ..., scrub: ..., pin: ...

### Hover states
- **<Element>:** <property>: <before> → <after>, transition: <value>

## Per-State Content (if applicable)

### State: "Featured"
- Title: "..."
- Cards: [{ title, description, image: 'public/images/...', link }, ...]

## Assets
- Background image: `public/images/<file>.webp`
- Icons used: <ArrowIcon>, <SearchIcon> from icons.tsx

## Text Content (verbatim)
<All text content copy-pasted from the live site>

## Responsive Behavior
- **Desktop (1440px):** ...
- **Tablet (768px):** <what changes>
- **Mobile (390px):** <what changes>
- **Breakpoint:** layout switches at ~<N>px
```

Fill every section. The **CSS Animations** and **GSAP** fields must be filled if those mechanisms are present. These are what separates a living clone from a static screenshot match.

### Step 3: Dispatch Builders

Based on complexity:
- **Simple section** (1-2 sub-components): One builder agent
- **Complex section** (3+ distinct sub-components): One agent per sub-component + one for the section wrapper

**What every builder agent receives:**
- The full contents of its component spec file (inline in the prompt)
- Path to the section screenshot
- Which shared components to import (`icons.tsx`, `cn()`, shadcn primitives, installed animation libraries)
- The target file path
- Instruction to verify with `npx tsc --noEmit` before finishing
- For GSAP animations: the exact tween parameters from the spec, and a reminder that GSAP and ScrollTrigger are installed
- For scroll-reveal animations: the IntersectionObserver options and the before/after CSS class pattern

**Don't wait.** As soon as builders for one section are dispatched, move to extracting the next section.

### Step 4: Merge

As builder agents complete:
- Merge their worktree branches into main
- Resolve conflicts intelligently using your full context
- Verify `npm run build` after each merge

---

## Phase 4: Page Assembly

After all sections are built and merged, wire everything together in `src/app/page.tsx`:

- Import all section components
- Implement page-level layout from your topology doc
- Connect real content to component props
- Implement page-level behaviors:
  - Scroll snap containers
  - Page-level scroll-driven animations
  - IntersectionObserver reveals (if not handled in individual components)
  - GSAP context and ScrollTrigger refresh
  - Smooth scroll (Lenis SmoothScrollProvider wrapping layout)
  - Dark-to-light section transitions
  - Z-index layering
- Verify: `npm run build` passes clean

### Animation Library Wiring

**GSAP + ScrollTrigger initialization (if used):**
```typescript
'use client';
import { useEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export function GSAPProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    return () => { ScrollTrigger.getAll().forEach(t => t.kill()); };
  }, []);
  return <>{children}</>;
}
```

**IntersectionObserver reveal pattern (if used):**
```typescript
// Based on animation-capture.json observer data
// In each component that has scroll-reveals:
useEffect(() => {
  const observer = new IntersectionObserver(
    (entries) => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
    { threshold: 0.15, rootMargin: '0px 0px -50px 0px' } // use values from animation-capture.json
  );
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  return () => observer.disconnect();
}, []);
```

---

## Phase 5: Visual QA Diff

After assembly, do NOT declare the clone complete. Take side-by-side comparison screenshots:

1. Open the original site and your clone side-by-side at the same viewport widths
2. Compare section by section, top to bottom, at desktop (1440px) and mobile (390px)
3. For each discrepancy:
   - Check the component spec file — was the value extracted correctly?
   - If spec was wrong: re-extract from browser MCP, update spec, fix component
   - If spec was right but builder got it wrong: fix component to match spec
4. **Test all interactive behaviors:**
   - Scroll slowly — do all scroll-reveal animations fire? At the right position?
   - Test sticky nav — does it change appearance at the right threshold?
   - Click every tab/button — does content switch correctly?
   - Hover every interactive element — do hover states animate?
   - Test smooth scroll — does it feel the same as the original?
   - Test at mobile — does the hamburger menu work?
5. **Test GSAP animations** — scroll past any GSAP ScrollTrigger sections; verify the animation direction, speed, and easing match the original
6. **Test CSS @keyframes** — page load animations should fire; looping animations should loop

Only after this visual QA pass is the clone complete.

---

## Pre-Dispatch Checklist

Before dispatching ANY builder agent, verify you can check every box:

- [ ] Spec file written to `docs/research/components/<name>.spec.md` with ALL sections filled
- [ ] Every CSS value in the spec is from `getComputedStyle()`, not estimated
- [ ] Interaction model is identified and documented (static / click / scroll / time / GSAP)
- [ ] For stateful components: every state's content and styles are captured
- [ ] For scroll-driven components: trigger threshold, before/after styles, and transition are recorded
- [ ] For CSS animated components: @keyframes name and body copied from `keyframes.json`, all `animation-*` properties documented
- [ ] For GSAP-animated components: tween type, target, vars, and ScrollTrigger parameters documented
- [ ] For hover states: before/after values and transition timing are recorded
- [ ] All images in the section are identified (including overlays and layered compositions)
- [ ] Responsive behavior is documented for at least desktop and mobile
- [ ] Text content is verbatim from the site, not paraphrased
- [ ] The builder prompt is under ~150 lines of spec; if over, the section needs to be split

---

## What NOT to Do

Lessons from failed clones — each one cost hours of rework:

- **Don't build click-based tabs when the original is scroll-driven.** Determine the interaction model FIRST by scrolling before clicking. This is the #1 most expensive mistake.
- **Don't extract only the default state.** Capture every tab state, every scroll threshold state, every hover state.
- **Don't skip animation extraction.** An animated section with no @keyframes or GSAP spec produces a static component that feels completely wrong. Always check `keyframes.json` and `animation-capture.json` before writing a builder spec.
- **Don't approximate animation parameters.** `duration: 0.6` vs `duration: 0.3` is immediately noticeable. Copy exact values.
- **Don't forget GSAP is free now.** Install it with `npm install gsap`. No CDN required, no license.
- **Don't miss overlay/layered images.** Check every container's DOM tree for multiple stacked elements.
- **Don't build mockup components for content that's actually videos/animations.** Check if a section uses `<video>`, Lottie, or `<canvas>` before building an elaborate HTML mockup of what the video shows.
- **Don't approximate CSS classes.** "It looks like `text-lg`" is wrong if the computed line-height differs. Extract exact values.
- **Don't build everything in one monolithic commit.** Incremental progress with verified builds at each step.
- **Don't reference docs from builder prompts.** Each builder gets the CSS spec inline — never "see DESIGN_TOKENS.md for colors."
- **Don't skip asset extraction.** Without real images, videos, and fonts, the clone will always look fake.
- **Don't give a builder agent too much scope.** If the builder prompt is getting long, break it into smaller tasks.
- **Don't skip responsive extraction.** Test at 1440, 768, and 390 during extraction.
- **Don't forget smooth scroll libraries.** Lenis/Locomotive feel noticeably different from native scroll. The user will spot it immediately.
- **Don't dispatch builders without a spec file.** The spec file forces exhaustive extraction.
- **Don't ignore CORS-blocked stylesheets.** Use the browser MCP network log to retrieve blocked CSS — it was downloaded, just not accessible via the DOM API.
- **Don't ignore `::before` and `::after` pseudo-elements.** Many decorative elements (underline animations, corner accents, background shapes) live in pseudo-elements. The extraction script captures them — use those values.

---

## Completion

When done, report:
- Total sections built
- Total components created
- Total spec files written (should match components)
- Total assets downloaded (images, videos, SVGs, fonts)
- Build status (`npm run build` result)
- Visual QA results (any remaining discrepancies)
- Animation libraries installed and wired
- Any known gaps or limitations

---

## Design Notes

This skill emphasizes three areas that separate a living clone from a static screenshot match:

**1. Animation extraction is systematic, not ad-hoc.** A dedicated Phase 0 pre-navigation instrumentation step intercepts GSAP tween calls and IntersectionObserver registrations before they fire; a global @keyframes extraction script with CORS fallback via network log; CSS scroll-driven animation (`animation-timeline`) detection; GSAP ScrollTrigger parameter retrieval; and mandatory animation fields in every component spec template. An animated section without these fields in the spec is incomplete by definition.

**2. CORS-blocked stylesheets are not a dead end.** Cross-origin CSS files throw when accessed via `document.styleSheets[n].cssRules`. But the browser MCP already downloaded those files — they're in the network log. Retrieve blocked CSS via the network response body rather than giving up.

**3. Pseudo-elements are first-class citizens.** The `::before` and `::after` pseudo-elements are extracted in the computed styles script and documented in the spec template. Many hover state animations, decorative lines, and background effects live exclusively in pseudo-elements — missing them leaves visible gaps.

Everything else (Next.js + shadcn/ui + Tailwind v4 output, parallel worktree agents, spec-first discipline, scroll-first protocol) follows a standard, well-proven clone pipeline.

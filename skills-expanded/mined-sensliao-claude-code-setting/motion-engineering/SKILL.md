---
name: motion-engineering
description: >-
  Executable web-motion recipes on GSAP v3.13+ (free including all plugins) plus the native View Transitions API and scroll-driven CSS — tweens and easing, timelines, ScrollTrigger (pin/scrub/parallax/batch), SplitText/Flip/Draggable, the 60fps transform-opacity contract, React via useGSAP, and prefers-reduced-motion. Triggers: "motion / animation / GSAP / ScrollTrigger / scroll animation / parallax / pin section / timeline / text reveal / useGSAP / page transition / View Transitions / reduced motion / animation jank / 动效 / 动画 / 滚动动画 / 视差 / 钉住区块 / 页面转场 / 动画卡顿". Consumes motion tokens from `design-token-pipeline`.
license: MIT
---

# Motion Engineering

Copy-paste-ready motion patterns. GSAP is the default engine (framework-agnostic, free for commercial use including every plugin); native **View Transitions API** and **scroll-driven CSS animations** cover the lightweight cases. Distilled from the official `greensock/gsap-skills` (MIT) into one skill.

## 0. When to Use / Boundaries

**Use when**: implementing any web animation — entrance reveals, scroll-linked effects, pinning, parallax, text splits, page transitions, drag interactions, or fixing animation jank.

| Concern | Owner |
|---|---|
| Motion *taste* / when polish is "right" / micro-interaction philosophy | `emil-design-eng` (L11) |
| Duration / easing *values* as tokens | `design-token-pipeline` (consume `--duration-*`, `--ease-*`) |
| Whether the L3 style *wants* heavy motion | `taste-skill` MODE C / L3 lock |
| **Executable motion technique + code** | **this skill** |

> GSAP licensing (important): since Webflow's acquisition, **GSAP is fully free including all former Club plugins** (SplitText, MorphSVG, DrawSVG, etc.). Install everything from the public `gsap` npm package. Never generate an `.npmrc` with a GreenSock auth token or tell the user to buy Club GSAP — that guidance is outdated.

## 1. Install (cross-platform — PowerShell & Bash identical)

```bash
npm install gsap            # core + ALL plugins, free
npm install @gsap/react     # only if using React (useGSAP hook)
```

If a build complains GSAP is missing, the line above is the fix — do not assume it is installed. All plugins ship inside the `gsap` package; import them as `gsap/ScrollTrigger`, `gsap/SplitText`, etc.

## 2. Decision: which tool for which motion

```
 simple hover / state transition ............ CSS transition (no JS)
 scroll progress bar / simple reveal ......... scroll-driven CSS (animation-timeline: view())  [progressive]
 same-document route/layout swap ............. View Transitions API (document.startViewTransition)
 sequencing / timeline / runtime control ..... GSAP timeline
 scroll-link / pin / scrub / parallax ........ GSAP ScrollTrigger
 text char/word/line reveal .................. GSAP SplitText
 layout state→state (grid reorder, expand) ... GSAP Flip
 drag / throw / inertia ...................... GSAP Draggable + InertiaPlugin
```

## 3. GSAP Core — tweens, eases, stagger

```javascript
import gsap from "gsap";

gsap.to(".box",   { x: 100, duration: 0.6, ease: "power2.out" });   // to current → vars
gsap.from(".item",{ autoAlpha: 0, y: 20, stagger: 0.08 });          // entrance (autoAlpha = opacity+visibility)
gsap.fromTo(".bar", { scaleX: 0 }, { scaleX: 1, transformOrigin: "left", duration: 1 });

gsap.defaults({ duration: 0.6, ease: "power2.out" }); // project-wide defaults
```

- **Use transform aliases** (`x`, `y`, `scale`, `rotation`, `xPercent`) over raw CSS — consistent order, GPU-friendly.
- **`autoAlpha`** instead of `opacity` for fade-out (also sets `visibility:hidden` so hidden elements don't catch clicks).
- **Stagger**: `stagger: 0.1` or `{ each: 0.1, from: "center" | "random" | "edges" }`.
- **Eases**: `"power1..4.[in|out|inOut]"`, `"back.out(1.7)"`, `"elastic.out(1,0.3)"`, `"none"` (linear). `CustomEase.create("n", ".17,.67,.83,.67")` for bespoke curves.
- Store the return value to control playback: `const t = gsap.to(...); t.pause(); t.reverse(); t.kill();`
- **`gsap.quickTo()`** for high-frequency updates (mouse followers) — reuses one tween, never creates per-frame tweens.

## 4. Timeline — sequencing

```javascript
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });
tl.to(".a", { x: 100 })
  .to(".b", { y: 50 }, "<")        // "<" = start with previous;  ">" = after previous (default)
  .to(".c", { autoAlpha: 0 }, "-=0.2")  // 0.2s before previous end
  .addLabel("done");
```

Position parameter: absolute `1`, relative `"+=0.5"` / `"-=0.2"`, label `"done+=0.3"`, placement `"<"` / `">"` / `"<0.2"`. **Prefer timelines over chaining `delay`.** Nest with `master.add(child, 0)`.

## 5. ScrollTrigger — scroll-link, pin, scrub, parallax

```javascript
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);   // register ONCE before any use

// Reveal on enter
gsap.from(".card", {
  autoAlpha: 0, y: 40, duration: 0.6,
  scrollTrigger: { trigger: ".card", start: "top 80%", toggleActions: "play none none reverse" }
});

// Scrubbed + pinned section (timeline tied to scroll)
const tl = gsap.timeline({
  scrollTrigger: { trigger: ".section", start: "top top", end: "+=1500", pin: true, scrub: 1 }
});
tl.to(".layer-a", { yPercent: -30 }).to(".layer-b", { yPercent: -60 }, "<"); // parallax
```

Key config: `start`/`end` are `"triggerPos viewportPos"` (e.g. `"top center"`, `"bottom 80%"`, `"+=1000"`); wrap in `clamp(...)` (v3.12+) to stay in page bounds. `scrub: true|<seconds>` links progress to scroll; `pin: true` pins the trigger (animate **children**, not the pinned element). `markers: true` for dev only — remove in production.

**Batch many elements** (better than IntersectionObserver for grids):
```javascript
ScrollTrigger.batch(".card", {
  start: "top 85%",
  onEnter: (els) => gsap.to(els, { autoAlpha: 1, y: 0, stagger: 0.1, overwrite: true }),
  onLeaveBack: (els) => gsap.set(els, { autoAlpha: 0, y: 50, overwrite: true })
});
```

**Horizontal scroll** (vertical scroll drives horizontal motion): the horizontal tween **must** use `ease: "none"`, pin the wrapper (not the moving element), and reference it via `containerAnimation` for nested triggers.

**Rules**: put ScrollTrigger on the **timeline or a top-level tween**, never on a tween inside a timeline. Call `ScrollTrigger.refresh()` after DOM/layout/font changes (resize is auto-handled, debounced 200ms). Don't combine `scrub` + `toggleActions` on the same trigger (scrub wins). Create triggers top-to-bottom or set `refreshPriority`.

## 6. Plugins — SplitText, Flip, Draggable

```javascript
import { SplitText } from "gsap/SplitText";
gsap.registerPlugin(SplitText);

const split = SplitText.create(".heading", { type: "words,chars", aria: "auto" });
gsap.from(split.chars, { autoAlpha: 0, y: 20, stagger: 0.03, duration: 0.4 });
// split.revert() to restore, or let gsap.context() revert it
```
- **SplitText**: split into `chars`/`words`/`lines`. `aria: "auto"` (default) keeps screen-reader text intact. Split only what you animate. For web fonts, use `autoSplit:true` + `onSplit()` (re-splits after fonts load / on resize) and **return** the tween from `onSplit` for auto cleanup.
- **Flip**: `const s = Flip.getState(".item")` → mutate DOM (reorder/add/class change) → `Flip.from(s, { duration: 0.5, ease: "power2.inOut" })`. For grid reorders, expand/collapse, shared-element transitions.
- **Draggable** (+ `InertiaPlugin` for throw): `Draggable.create(".box", { type: "x,y", bounds: "#area", inertia: true })`.

Register **every** plugin once before first use. Don't ship `GSDevTools` or dev-only plugins to production.

## 7. Performance contract (60fps)

- ✅ Animate **only `transform` (`x/y/scale/rotation`) and `opacity`** — they stay on the compositor (no layout/paint).
- ❌ Never animate `width`/`height`/`top`/`left`/`margin`/`padding` for movement — they trigger layout and cause jank.
- `will-change: transform` in CSS **only** on elements that actually animate — not "just in case" (it costs memory).
- Use `stagger` over many manual-`delay` tweens. Use `gsap.quickTo()` for frequently-updated props.
- Kill/pause off-screen animations; only `ScrollTrigger.refresh()` when layout actually changes.
- Grain/noise overlays: apply to a `fixed inset-0 pointer-events-none` pseudo-element, **never** a scrolling container.

## 8. React / Next.js integration

```javascript
import { useGSAP } from "@gsap/react";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(useGSAP, ScrollTrigger);   // register at module top level

function Hero() {
  const container = useRef(null);
  useGSAP(() => {
    gsap.from(".title", { autoAlpha: 0, y: 30, duration: 0.6 });   // selectors scoped to container
  }, { scope: container });   // cleanup (revert tweens + ScrollTriggers) runs automatically on unmount
  return <section ref={container}><h1 className="title">Hi</h1></section>;
}
```

- **Prefer `useGSAP()`** from `@gsap/react` over raw `useEffect` — it auto-reverts on unmount and provides `scope` + `contextSafe`.
- **Always pass `scope`** (a ref) so `.selector` strings can't match elements outside the component.
- For animations created in **event handlers** (created *after* `useGSAP` runs), wrap them in **`contextSafe()`** and remove listeners in the cleanup return — otherwise they leak.
- Without `@gsap/react`: use `gsap.context(() => {...}, ref)` in `useEffect` and **always** `return () => ctx.revert()`.
- **SSR**: GSAP is browser-only. Never call `gsap.*` / `ScrollTrigger.*` during server render — keep it inside `useGSAP`/`useEffect`.

## 9. Accessibility — prefers-reduced-motion (non-negotiable)

Always gate motion behind `gsap.matchMedia()` so users with vestibular sensitivity get a calm experience:

```javascript
const mm = gsap.matchMedia();
mm.add({
  isDesktop: "(min-width: 800px)",
  reduceMotion: "(prefers-reduced-motion: reduce)"
}, (ctx) => {
  const { reduceMotion } = ctx.conditions;
  gsap.from(".card", {
    autoAlpha: 0,
    y: reduceMotion ? 0 : 40,            // no travel when reduced
    duration: reduceMotion ? 0 : 0.6     // instant when reduced
  });
});
// mm.revert() on unmount (matchMedia auto-reverts what it created when a query stops matching)
```

CSS fallback for non-GSAP motion:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .001ms !important; transition-duration: .001ms !important; scroll-behavior: auto !important; }
}
```
Do **not** nest `gsap.context()` inside `matchMedia` (matchMedia makes its own context — use `mm.revert()` only).

## 10. Native alternatives (no library)

**View Transitions API** — animate between two DOM states / SPA routes with a browser-native crossfade or shared-element morph:
```javascript
if (document.startViewTransition) {
  document.startViewTransition(() => updateTheDOM());   // browser tweens old→new
} else {
  updateTheDOM();   // graceful fallback
}
/* CSS: name a shared element so it morphs across the transition */
/* .hero-img { view-transition-name: hero; } */
```

**Scroll-driven CSS animations** (progressive enhancement, no JS) — for progress bars / simple reveals where you don't need GSAP:
```css
@keyframes reveal { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: none; } }
.card { animation: reveal linear both; animation-timeline: view(); animation-range: entry 0% cover 30%; }
```
Both are progressive: feature-detect (`document.startViewTransition`, `CSS.supports("animation-timeline: view()")`) and fall back gracefully. Reach for GSAP ScrollTrigger when you need pinning, scrub control, cross-browser consistency, or JS-computed values.

## 11. Hard Rules recap

- ✅ `gsap.registerPlugin(...)` once, before first use, for every plugin.
- ✅ Animate transform + opacity only; `will-change` sparingly.
- ✅ React → `useGSAP` + `scope`; always clean up (auto via useGSAP, or `ctx.revert()`).
- ✅ Gate every non-trivial motion behind `prefers-reduced-motion`.
- ✅ ScrollTrigger on timeline/top-level tween only; `ease:"none"` for `containerAnimation`.
- ✅ Always emit `npm install gsap` before using GSAP imports — never assume installed.
- ❌ No GreenSock auth token / `.npmrc` / Club GSAP purchase (everything is free).
- ❌ No animating layout properties for movement; no GSDevTools in production; no GSAP during SSR.

## 12. References

- GSAP docs: https://gsap.com/docs/v3/ · Webflow/GSAP free announcement: https://gsap.com/blog/webflow-GSAP/
- ScrollTrigger: https://gsap.com/docs/v3/Plugins/ScrollTrigger/ · SplitText: https://gsap.com/docs/v3/Plugins/SplitText/ · Flip: https://gsap.com/docs/v3/Plugins/Flip
- React/useGSAP: https://gsap.com/resources/React
- View Transitions API: https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API
- Scroll-driven animations: https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline
- Source corpus (MIT): `CAPABILITY-UPGRADE-2026-06/staging/cloned-repos/gsap-skills/skills/` (gsap-core/timeline/scrolltrigger/plugins/react/performance/utils/frameworks)

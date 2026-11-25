---
name: motion
description: Animation and motion conventions — CSS transitions/keyframes, View Transitions, scroll-driven effects, animation libraries, exit animations, performance. Use when adding, changing, or debugging any animation, transition, or page-transition effect. 日本語の依頼例:「アニメーション付けて」「動きを付けて」「トランジション」「ページ遷移アニメ」「スクロール演出」「ふわっと表示」。
---

# Motion

Base invariants live in `css-modules` (animate `transform`/`opacity` only; duration/easing as tokens; respect `prefers-reduced-motion`). This skill covers when and how.

## Escalation ladder — use the cheapest tier that works

1. **CSS transition** — state changes (hover, open/close, theme). Default answer.
2. **CSS keyframes** — multi-step or looping effects.
3. **Web Animations API** — dynamic values or playback control from JS, still zero deps.
4. **Animation library** (Motion — formerly Framer Motion) — only for springs, gestures, layout/shared-element animation, or orchestrated sequences. It's a real dependency: the CLAUDE.md ask-first rule applies; never add it for a fade.

## Page & element transitions

- View Transitions API for page transitions (Astro: native cross-document view transitions, or `<ClientRouter />` for SPA-mode extras; Next.js/SPA: progressive enhancement behind a `document.startViewTransition` feature check). It must be enhancement — navigation works identically without it.
- Verify page transitions with the browser Back button AND your E2E runner before shipping — two failure modes seen in practice: Astro `<ClientRouter />` can drop page-scoped `<style>` on history back-navigation (the page reverts to an unstyled/full-width layout), and native `@view-transition { navigation: auto }` makes headless Playwright treat every link as never-"stable" so `click()` hangs. If a transition doesn't survive both, ship without it — the page must work identically anyway. Add a back-navigation smoke assertion to E2E (`testing-playwright`).
- Scroll-driven effects: CSS scroll-driven animations or `IntersectionObserver`. Never scroll event listeners doing style work — and if E2E must click elements inside a scroll-driven animation, prefer `IntersectionObserver` + a one-shot transition: scroll-linked animations count as permanently "running", which defeats Playwright's stability check.

## Behavior rules

- Animations are interruptible: a second click mid-animation must not break state. CSS transitions handle this free; JS sequences must handle cancellation.
- Never gate interaction or content behind an entrance animation — the page is usable at frame 0, and LCP content is never delayed by animation. Hero/above-the-fold entrances: animate `transform` from a visible state, or animate secondary elements — never start the LCP element at `opacity: 0` (the browser re-times LCP to when it becomes visible).
- Exit animations in React: the element must stay mounted until the animation ends — `<AnimatePresence>` with the library, or a two-phase state (`closing` → unmount on `transitionend`/`animationend`) by hand. Setting `display: none` in the same tick kills the animation.
- Durations from tokens; UI feedback stays fast (~100–250 ms); anything over ~400 ms needs a reason.

## Reduced motion

- `@media (prefers-reduced-motion: reduce)`: large/parallax/auto-playing motion is removed; motion that *conveys state* (a panel opening) is reduced to a quick fade or instant change — not deleted, the state change must still be perceivable. JS animations check `matchMedia('(prefers-reduced-motion: reduce)')`.

## Performance

- `will-change` only on elements about to animate, removed after — it's a per-element memory cost, not a go-faster switch.
- Animating layout properties (`width`/`height`/`top`/`left`) is banned per `css-modules`; for size transitions use `transform: scale` or FLIP, and `interpolate-size`/`calc-size()` where supported for height-auto transitions.
- Verify on a throttled CPU (DevTools 4x/6x) — animations are written on fast machines and janky on real ones.

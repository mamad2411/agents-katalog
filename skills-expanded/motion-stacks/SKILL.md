---
name: motion-stacks
description: "Writing motion in each stack: plain CSS and JavaScript, Tailwind, React and the Motion library, Next.js, Vue, Svelte, and the native mobile toolkits, each with reduced motion. Read before writing animation code in the project's stack."
---

# Motion in each stack

The rules are the same in every stack (`motion`); this is how each one
writes them. Whatever the stack: the tokens are defined once, reduced
motion is handled once at the root rather than in every component, only
opacity and transform move, and no library is added for what CSS already
does (`motion-performance`).

## 1. Plain CSS and JavaScript

- The tokens, in one place:

```css
:root {
  --m-ease-out: cubic-bezier(0.22, 0.61, 0.36, 1);
  --m-ease-in: cubic-bezier(0.55, 0.055, 0.675, 0.19);
  --m-ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --m-instant: 100ms;
  --m-fast: 160ms;
  --m-base: 240ms;
  --m-panel: 320ms;
  --m-enter: 700ms;
  --m-draw: 1000ms;
  --m-shift-sm: 6px;
  --m-shift: 12px;
  --m-shift-lg: 18px;
}
```

- Keyframes named for what they do (`rise`, `fade`, `draw`, `count`), with
  only a `from` when they end at the element's own style.
- Movement written inside `@media (prefers-reduced-motion: no-preference)`
  rather than undone inside `reduce`: a rule added later is then safe by
  default.
- The reveal module from `motion-reveal`, started once:
  `startReveal(document.documentElement)` at the end of `<body>` or on
  `DOMContentLoaded`.
- Elements shown and hidden with `display` or `[open]` (dialogs, popovers)
  animate in and out with `@starting-style` and `allow-discrete`
  transitions (`motion-interface`).
- One-off motion from script uses the Web Animations API, not a
  `requestAnimationFrame` loop writing styles:
  `el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 240, easing:
  "cubic-bezier(0.22, 0.61, 0.36, 1)" })`. It runs like CSS and returns an
  animation you can await (`.finished`), `cancel()` or `reverse()`.
- Replaying CSS animations (a drawing, on hover): give the parts
  `animation-fill-mode: both`, then for each of
  `el.getAnimations({ subtree: true })` set `currentTime = 0` and call
  `play()`. A finished animation with `backwards` fill is no longer in
  effect, so `getAnimations()` does not return it: replayable parts need
  `both`.
- Reduced motion in script: `matchMedia("(prefers-reduced-motion:
  reduce)")`, and its `change` event for anything that keeps running.

## 2. Tailwind CSS

Version 4 keeps the tokens in CSS:

```css
@theme {
  --ease-soft-out: cubic-bezier(0.22, 0.61, 0.36, 1);
  --ease-soft-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --animate-rise: rise 700ms var(--ease-soft-out) backwards;
  --animate-fade: fade 600ms var(--ease-soft-out) backwards;
  @keyframes rise {
    from { opacity: 0; transform: translateY(12px); }
  }
  @keyframes fade {
    from { opacity: 0; }
  }
}
```

- That gives `ease-soft-out`, `animate-rise` and `animate-fade` as
  utilities: `transition-colors duration-150 ease-soft-out`,
  `motion-safe:animate-rise`.
- `motion-safe:` on every animation and every transform transition;
  `motion-reduce:transition-none` or `motion-reduce:animate-none` where a
  component library adds its own.
- A revealed block's children: `group` on the block, then
  `motion-safe:group-data-[shown]:animate-rise` on the child. The hidden
  pre-state and the arrival delay are clearer as the dozen lines of CSS in
  `motion-reveal` in the global stylesheet than as long utility strings on
  every element.
- Version 3: the same tokens in `theme.extend` (`transitionTimingFunction`,
  `keyframes`, `animation`) in `tailwind.config`; `motion-safe:` and
  `motion-reduce:` are the same.
- shadcn/ui's overlays use `tw-animate-css` (formerly
  `tailwindcss-animate`): `data-[state=open]:animate-in fade-in-0
  zoom-in-95`, `data-[state=closed]:animate-out fade-out-0 zoom-out-95`,
  with `duration-200`. Keep the distances small (`slide-in-from-top-2`) and
  leave its defaults when they already match `motion-interface`.

## 3. React

- The reveal hook sets the flag before paint and starts the one observer:

```tsx
export function useReveal(page: RefObject<HTMLElement | null>) {
  useLayoutEffect(() => {
    const root = page.current;
    return root ? startReveal(root) : undefined; // motion-reveal, section 2
  }, [page]);
}
```

  `useLayoutEffect`, not `useEffect`, for anything that sets a hidden
  pre-state: it runs before the browser paints.
- Per-frame values never pass through the state of a large tree. A clock
  that ticks ten times a second (a scripted demo, `motion-demo`) lives in
  the small component that shows it; a parent that needs to follow along
  changes state only when something it shows changes (a phase, a few times
  per loop), through a callback in an effect.
- Continuous values (the pointer, a drag, a progress) go into refs or CSS
  variables on an element (`el.style.setProperty("--x", ...)`), never into
  `setState` sixty times a second.
- Replay from an event handler with `getAnimations()` on a ref.
- Changing a `key` remounts and replays mount animations: use it on
  purpose, never by accident in a list.
- Strict mode runs effects twice in development: every observer
  disconnects in its cleanup.

### The Motion library (`motion`, formerly Framer Motion)

- It earns its weight for: exits of components React removes
  (`AnimatePresence`), layout animation (an element changing size or place
  smoothly, `layout`), shared elements between views (`layoutId`), and
  gestures with springs (drag with momentum). Not for fades and reveals
  that CSS does.
- Size: import from `motion/react`, wrap the app in `LazyMotion` with
  `domAnimation` (`domMax` only for layout and drag) and use `m.div`, not
  `motion.div`. That keeps it to a fraction of the full component's size.
- Reduced motion once, at the root: `<MotionConfig reducedMotion="user">`
  turns off transform and layout animation and keeps opacity;
  `useReducedMotion()` for choices in code.
- Reveals: `whileInView` with `viewport={{ once: true, margin: "0px 0px
  -10% 0px" }}` and `initial={{ opacity: 0, y: 12 }}`. The `initial` state
  is rendered on the server, so that content is hidden until the page
  hydrates: give content above the fold `initial={false}`, and accept that
  hidden text below it is invisible without JavaScript, or use the CSS
  reveal instead.
- Exits: `<AnimatePresence>` around conditionally rendered children, with
  `exit={{ opacity: 0 }}`; `mode="wait"` when one view replaces another.
- Timing from the tokens, kept in one object that mirrors the CSS:
  `transition={{ duration: 0.24, ease: [0.22, 0.61, 0.36, 1] }}`. Springs
  for drags and layout, critically damped so nothing overshoots:
  `{ type: "spring", stiffness: 400, damping: 40 }`.

### Other libraries

- GSAP for a long scripted timeline with many parts, with
  `gsap.matchMedia()` for reduced motion; ScrollTrigger only when CSS
  scroll-driven animations cannot do the job.
- Lottie for a designer-made animation, with the lighter dotLottie player
  rather than the full `lottie-web`, and the first or last frame shown
  under reduced motion.
- Each is a cost you state in the report (`motion-performance`).

## 4. Next.js

- Motion lives in client components; keep the `"use client"` boundary to
  the animated part (a `Reveal` wrapper, the demo), not the whole page.
- Server-rendered markup paints before hydration. A hidden pre-state needs
  the inline head script with its safety timeout (`motion-reveal`,
  section 3), written into `<head>` in `app/layout.tsx` with
  `dangerouslySetInnerHTML`, and `suppressHydrationWarning` on `<html>`,
  since the attribute differs from the server's.
- Route transitions: the View Transitions API where the version supports
  it (recent versions have an experimental view transitions flag used with
  React's `ViewTransition` component), or `document.startViewTransition`
  around the navigation. No fade on every route.
- `next/font` so a font swap does not move text in the middle of an
  entrance; `next/image` with sizes so an image does not shift a block
  while it reveals.
- `loading.tsx` shows only when the wait is worth showing
  (`motion-interface`, loading).

## 5. Vue

- `<Transition name="fade">` with:

```css
.fade-enter-active,
.fade-leave-active { transition: opacity var(--m-base) var(--m-ease-out); }
.fade-enter-from,
.fade-leave-to { opacity: 0; }
```

  and `appear` to play on the first render.
- `<TransitionGroup tag="ul" name="list">` for lists, with `.list-move {
  transition: transform var(--m-base) var(--m-ease-out); }` for reordering
  and `.list-leave-active { position: absolute; }` so the others close the
  gap.
- Reduced motion: `usePreferredReducedMotion()` from VueUse, with a `none`
  transition name when it is `reduce`, or the transition classes inside the
  no-preference media query.
- A `v-reveal` directive that adds its element to the page's one observer.
- Nuxt: short `pageTransition` and `layoutTransition`; the reveal flag from
  an inline head script through `useHead`.

## 6. Svelte (5)

- `transition:fade={{ duration: 240 }}`, `in:fly={{ y: 12, duration: 240,
  easing: cubicOut }}`, `out:fade={{ duration: 160 }}`, and
  `animate:flip={{ duration: 240 }}` inside a keyed `{#each}` for
  reordering.
- Custom transitions return `css: (t) => ...`, so they run as CSS rather
  than per-frame JavaScript.
- Reduced motion: `import { prefersReducedMotion } from "svelte/motion"`,
  then `duration: prefersReducedMotion.current ? 0 : 240`.
- `Tween` and `Spring` from `svelte/motion` for values that animate (a
  number, a position): `new Tween(0, { duration: 400, easing: cubicOut })`.
- `{#key value}` replays intro transitions when the value changes: only on
  purpose.
- SvelteKit: `onNavigate` with `document.startViewTransition` for route
  transitions.

## 7. Native mobile, briefly

- The platform's own navigation and sheet transitions win over web habits.
- React Native: Reanimated, which runs on the UI thread. `withTiming(value,
  { duration: 240, easing: Easing.bezier(0.22, 0.61, 0.36, 1),
  reduceMotion: ReduceMotion.System })`; `useReducedMotion()` for choices;
  layout animations such as
  `entering={FadeIn.duration(240).reduceMotion(ReduceMotion.System)}`.
- Flutter: implicit animations (`AnimatedOpacity`, `AnimatedContainer`,
  `AnimatedSwitcher`) for changes of state, `Curves.easeOutCubic` close to
  the tokens, and `MediaQuery.disableAnimationsOf(context)` to set
  durations to zero.
- SwiftUI: `withAnimation(.easeOut(duration: 0.24))`, transitions such as
  `.opacity.combined(with: .move(edge: .bottom))`, and
  `@Environment(\.accessibilityReduceMotion)` to swap movement for a fade.
- Jetpack Compose: `animate*AsState`, `AnimatedVisibility` with `fadeIn(
  tween(240))`, `updateTransition`. Compose follows the system's animator
  duration scale, including "Remove animations"; a custom loop reads that
  setting itself.

## Check it

- Search the code for `transition: all`, `transition-all`, `animate-bounce`
  and `animate-ping` used as decoration, `motion.` components without
  `LazyMotion`, and `setState` inside animation loops.
- `preview` with `motion: true` after building: the timeline, the
  animations driven from JavaScript, and the reduced-motion pass.
- The bundle before and after, from the build's size report: the motion of
  a page should cost a few kilobytes, not a library.

## Avoid

A motion library for fades; `motion.div` without `LazyMotion`; `initial`
hiding server-rendered text; `transition-all`; `animate-bounce` and
`animate-ping` as decoration; `setState` every frame; reduced motion
handled in each component instead of once; web-style transitions in a
native app where the platform has its own.

---
name: optimize-react-rerenders
description: Eliminates wasted React re-renders by measuring first then fixing — profile with the React DevTools Profiler (flamegraph + "why did this render") and why-did-you-render to find the actual offenders, then apply the right fix: stable references (hoist constants, useCallback/useMemo only where a referentially-equal prop/dep actually matters), correct list keys (stable id, never index), React.memo with a custom comparator on genuinely-hot leaf components, context splitting + selector subscriptions (useSyncExternalStore / Zustand / use-context-selector) to stop whole-tree re-renders, derive-don't-store to kill redundant state, and list virtualization (TanStack Virtual) for long lists — while knowing when NOT to memo (cheap renders, unstable deps, and the React 19 Compiler which auto-memoizes and makes most manual memo dead weight).
when_to_use: A React app re-renders too much — typing lags, a list re-renders every row on one change, the Profiler shows components rendering with unchanged props, or you're sprinkling useMemo/useCallback/React.memo and want to know what actually helps. Distinct from optimize-core-web-vitals (load/paint metrics — LCP/INP/CLS and asset/JS strategy, not render-count) and manage-client-server-state (data-fetching/caching architecture with TanStack Query; this skill fixes the render churn that fetched data triggers).
---

## When to Use

Reach for this skill when the problem is **too many React renders / render churn**, not load time, not data fetching:

- "Typing in this input lags / the whole form re-renders on every keystroke"
- "Changing one row re-renders the entire list of 500 items"
- "The Profiler shows components re-rendering even though their props didn't change"
- "I added `useMemo`/`useCallback`/`React.memo` everywhere and it's not faster (or slower)"
- "A context update re-renders half the tree"
- "Should I memoize this?" / "Is this `useMemo` worth it?" / "We're on React 19 — do I still need this?"
- "Long list scrolls slowly / mounts thousands of DOM nodes"

NOT this skill:
- Slow initial load, late paint, layout shift, or a red Lighthouse score (LCP/INP/CLS, image/font/JS-bundle strategy) → optimize-core-web-vitals (it owns paint/load metrics; this skill owns render *count*. Note: cutting re-renders during interaction also improves INP, but go there for the metric-driven workflow)
- Data fetching, cache invalidation, optimistic updates, SSR hydration, or picking a store (TanStack Query / Zustand / Redux) → manage-client-server-state (it architects *where state lives and how it's fetched*; this skill stops the renders that state changes cause)
- Building a new component's structure/props/a11y from scratch → build-react-component
- A big interactive grid feature (sorting/filtering/column resize/selection) as a unit → build-data-table (it builds the table; this skill makes its rows stop re-rendering)
- Backend/server query latency or a CPU profile of non-React code → performance-profiling
- Using the browser/Chrome DevTools to debug a runtime bug (state, network, errors) generally → debug-frontend-browser (this skill is the render-perf specialization of profiling)

## Steps

1. **Measure before you touch anything — never memoize on a hunch.** Manual memoization is a tradeoff (extra comparisons + cache memory); applied blindly it often makes things *slower* and always makes them harder to read. Get evidence first:

   | Tool | What it tells you | How |
   |---|---|---|
   | **React DevTools Profiler** | which components rendered, how long, **why** | record an interaction → flamegraph + ranked chart |
   | **"Highlight updates when components render"** (DevTools → ⚙ → Components) | visual flash on every render — instant "this re-renders on every keystroke" signal | toggle on, interact |
   | **`why-did-you-render`** | logs the *exact prop/state/hook that changed* (and whether it was a deep-equal-but-referentially-different value) | dev-only, see step 2 |
   | **React 19 `<Profiler onRender>`** / `performance.measure` | programmatic render timings in tests/CI | wrap a subtree |

   In the Profiler, enable **"Record why each component rendered"** (⚙ → Profiler). Re-renders show a reason: *props changed*, *hooks changed*, *parent rendered*, *context changed*. That reason picks the fix below — don't guess.

2. **Wire up `why-did-you-render` to catch referential-equality bugs (dev only).** It surfaces the classic "props are deep-equal but a new object/array/function identity every render" case that React.memo can't catch.
   ```js
   // wdyr.js — import FIRST, before React renders anything
   import React from 'react';
   if (process.env.NODE_ENV === 'development') {
     const wdyr = require('@welldone-software/why-did-you-render');
     wdyr(React, { trackAllPureComponents: true, collapseGroups: true });
   }
   ```
   A log like *"props.style changed: ({}) → ({}) (different objects that are equal by value)"* means: hoist the literal or memoize the reference — not wrap the child in `memo`.

3. **If you're on React 19, turn on the React Compiler FIRST — it auto-memoizes and makes most manual memo dead weight.** The compiler (`babel-plugin-react-compiler`, also in the Next.js / Vite plugin) memoizes components and hook values automatically at build time, so `useMemo`/`useCallback`/`React.memo` become largely redundant. Before hand-tuning:
   - Install and enable it; run `npx react-compiler-healthcheck` to see how many components are compatible (it skips components that break the Rules of React — those are your real bugs to fix).
   - **Don't mix strategies blindly:** keep code Rules-of-React-clean (no mutation of props/state, no conditional hooks) so the compiler can optimize. New manual `useMemo`/`useCallback` you add on top is usually noise. Lean on `<StrictMode>` to surface impurity.
   - The compiler does **not** fix algorithmic problems (huge lists, O(n²) renders) — you still need virtualization (step 9) and correct keys (step 7). Treat the rest of these steps as either pre-19 work or the things the compiler can't do.

4. **Kill unstable references at the source — this is the #1 cause of "memo doesn't work".** `React.memo` and dep arrays compare by reference (`Object.is`). A new `{}`, `[]`, or arrow function created in render is a new identity every time, so it busts every downstream memo and effect. Fix the *source*, don't paper over it:

   | Anti-pattern (new identity each render) | Fix |
   |---|---|
   | `<Child style={{ margin: 8 }} />` | hoist the object to a module-level `const` (it never changes) |
   | `<Child onClick={() => doX(id)} />` passed to a memoized child | `useCallback(() => doX(id), [id])` |
   | `const opts = { a, b }` then used in a dep array | `useMemo(() => ({ a, b }), [a, b])` |
   | `data.filter(...)` computed inline each render into a memoized child | `useMemo(() => data.filter(...), [data])` |
   | default prop `items = []` (new array each call) | hoist `const EMPTY = []` and default to it |

   Static values (handlers with no closure deps, constant config) belong **outside the component** entirely — zero runtime cost.

5. **Use `useCallback`/`useMemo` only where a referentially-equal value actually changes behavior — otherwise skip it.** They are not free: each stores a closure + dep array and runs an equality check every render. They earn their keep in exactly these cases — and nowhere else:
   - The memoized value/callback is **a dependency of another hook** (`useEffect`, `useMemo`) where a changing identity would refire the effect.
   - It's **passed as a prop to a `React.memo`'d child** (otherwise the child's memo is pointless).
   - `useMemo` wraps a **genuinely expensive computation** (sort/filter of thousands, parse, heavy derive) — measure; "expensive" is rarely a `.map` over 20 items.

   **Skip them when** the consumer isn't memoized, the deps change every render anyway (then the cache never hits — pure overhead), or the body is cheap. A `useCallback` whose result flows only into a non-memoized DOM `<button onClick>` does nothing useful.

6. **`React.memo` only the genuinely-hot leaf, and give it the right comparator.** `memo` skips a re-render when props are shallow-equal. Apply it to a component that (a) renders often due to *parent* re-renders, (b) is expensive or numerous (list rows), and (c) gets **stable props** (you did step 4). Without stable props it's worse than nothing.
   - Default shallow compare is correct most of the time. Provide a custom `areEqual(prev, next)` only for a known-shape prop where shallow misses (e.g. compare `prev.item.id === next.item.id && prev.selected === next.selected`) — and keep it cheaper than the render it saves.
   - `memo` compares **props only** — it does **not** stop re-renders from internal `useState`/`useContext` changes. If the offender is context (step 8) or state, `memo` won't help.
   ```jsx
   const Row = memo(function Row({ item, onSelect }) { /* ... */ },
     (a, b) => a.item.id === b.item.id && a.item.label === b.item.label && a.onSelect === b.onSelect);
   ```

7. **Fix list keys — wrong keys force remounts and break memoized rows.** Use a **stable, unique id** from the data (`item.id`), never the array index for any list that can reorder, insert, or delete. Index keys make React reuse the wrong DOM/state on reorder (lost input focus, wrong row highlighted) and defeat per-row `memo`. Don't use `Math.random()`/`uuid()` in render either — a new key every render remounts the row each time. Stable identity → React diffs in place → memoized rows actually skip.

8. **Stop context from re-rendering the whole subtree — split it or use a selector.** Every consumer of a context re-renders whenever **any** field of the context value changes, even fields it doesn't read. Three escalating fixes:

   | Technique | When | How |
   |---|---|---|
   | **Memoize the provider value** | value is `{}`/`[]` literal inline | `value={useMemo(() => ({ user, setUser }), [user])}` — without this *every* consumer re-renders every parent render |
   | **Split contexts by change frequency** | one context mixes hot + cold data (e.g. `theme` + live `cursorPosition`) | separate providers; a component subscribes only to what it uses → high-frequency updates don't touch theme consumers |
   | **Selector subscription** | consumers read different slices of a big store | `useSyncExternalStore` with a selector, `use-context-selector`, or a store lib (**Zustand**: `useStore(s => s.field)`, **Redux**: `useSelector`) — re-render only when the *selected* slice changes |

   Splitting state-vs-dispatch contexts is a cheap classic win: a component that only dispatches never re-renders on state changes.

9. **Virtualize long lists instead of memoizing 10,000 rows.** No amount of `memo` saves you from mounting thousands of DOM nodes. Render only the visible window (+overscan) with **TanStack Virtual** (`@tanstack/react-virtual`, headless, framework-agnostic) or `react-virtuoso`. It computes which rows intersect the viewport and absolutely-positions them; DOM stays ~constant regardless of dataset size. Combine with stable keys (step 7) and a memoized row. This is the fix when the *count* is the problem, not per-row work.

10. **Derive, don't store — redundant state is redundant renders.** Anything computable from props/existing state during render should be **computed in render** (optionally `useMemo`'d), not held in its own `useState` synced via `useEffect`. The `useState`+`useEffect`-to-sync pattern adds an extra render every change and drifts out of sync. Likewise: lift state **down** (push it into the smallest component that needs it so updates don't re-render siblings), and split a god-component so a chatty piece of state isn't wired into a large subtree. Fewer state cells in fewer places = fewer renders.

11. **Don't over-memoize — premature memoization has a real cost.** Each `memo`/`useMemo`/`useCallback` adds an equality check + retained closure + cognitive load, and a wrong dep array becomes a stale-closure bug. Rules of thumb: leave cheap components un-memoized; never wrap a component whose props are unstable (fix the props instead); never memoize purely to "be safe." On React 19, prefer the compiler over manual memo. Memoize when the Profiler shows a *measured* hot path — not before. Remove memos that the Profiler shows aren't being hit.

## Common Errors

- **`React.memo` with unstable props.** Memo'd child still re-renders because a parent passes a fresh `{}`/`() => {}` each render. Fix: stabilize the prop at the source (step 4) — `memo` without stable props is pure overhead.
- **`useCallback`/`useMemo` feeding a non-memoized consumer.** A stable callback handed to a plain `<button>` or non-`memo` child changes nothing but adds overhead. Fix: only memoize values that cross into a `memo`'d child or another hook's deps.
- **Dep array that changes every render.** The memo never caches (cache miss every time) — all cost, no benefit. Fix: stabilize the deps too, or drop the memo.
- **Index as list key.** Reorders/inserts reuse the wrong DOM/state and break per-row memo; lost focus, wrong highlight. Fix: stable `item.id` key.
- **`Math.random()`/`uuid()` key in render.** Remounts every row every render — the opposite of memoization. Fix: derive a stable id once.
- **Inline object/array provider value.** `<Ctx.Provider value={{a,b}}>` re-renders every consumer on every parent render. Fix: `useMemo` the value, or split contexts.
- **One fat context for hot + cold data.** A 60fps field re-renders theme/auth consumers. Fix: split by update frequency; use a selector subscription.
- **`useState` mirrored from props via `useEffect`.** Extra render + drift. Fix: derive in render (`useMemo` if pricey).
- **Memoizing everything by default.** Slower and unreadable; stale-closure bugs from wrong deps. Fix: memoize measured hot paths only; on React 19 let the compiler do it.
- **Expecting `memo` to stop context/state re-renders.** `memo` compares props only. Fix: address the actual reason the Profiler reports (context → split/selector; state → derive/lift).

## Verify

1. **Profiler shows the offender gone:** record the same interaction before/after — the component that flashed/rendered "props changed (but equal)" or "parent rendered" no longer appears in the commit (or its render time drops). Keep the before flamegraph as proof.
2. **`why-did-you-render` is silent on the fixed path:** no "different objects that are equal by value" logs for the props you stabilized.
3. **Typing/interaction is smooth:** the input/list that lagged updates per keystroke without re-rendering unrelated siblings; "Highlight updates" flashes only the changed node.
4. **One-row change → one row renders:** mutating a single list item re-renders that row only, not the whole list (visible in the Profiler ranked chart).
5. **Context change is scoped:** updating a hot context field re-renders only its real consumers; theme/auth consumers stay dark.
6. **Long list DOM is bounded:** the virtualized list mounts ~viewport+overscan rows, and node count stays roughly constant as the dataset grows from 100 → 10,000.
7. **No memo is dead weight:** every remaining `memo`/`useMemo`/`useCallback` corresponds to a Profiler-confirmed hot path or a real dep/`memo`-prop boundary; the rest were removed. On React 19, `react-compiler-healthcheck` passes and manual memo is minimal.

Done = the measured re-render(s) the Profiler flagged are eliminated by the matching fix (stable refs, correct keys, context split/selector, derive-don't-store, or virtualization), every remaining manual memo is justified by evidence (or replaced by the React 19 compiler), and the before/after Profiler traces prove the churn is gone — not added overhead.

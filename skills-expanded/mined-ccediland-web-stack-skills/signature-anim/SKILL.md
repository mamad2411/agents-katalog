---
name: signature-anim
description: Integrates one bespoke interactive Rive state-machine animation as a site's signature moment on Astro 7 plus Cloudflare, without breaking native CSP, the performance budget, or accessibility. Use when embedding a designer-authored .riv with real branching interaction such as hover, click, or scroll on a single element; when wiring the Rive runtime under a hash-based CSP (wasm-unsafe-eval, self-hosted WASM, connect-src); when lazy-loading the heavy WASM runtime off the critical path; when driving state-machine inputs from scroll or pointer; or when adding reduced-motion and a pause control to a Rive canvas. Covers renderer choice, the CSP and WASM recipe, lazy init, input wiring, the WCAG pause decision tree, a poster fallback, and the Rive-versus-dotLottie decision. Not for DOM tween or scroll-reveal animation (use motion-system), not for generative shader backgrounds (use webgl-atmosfera), not for authoring the .riv in the Rive editor, and not for playback-only animation where Lottie or CSS is lighter.
---

# signature-anim

> Integration discipline for embedding one bespoke, designer-authored, interactive Rive state-machine animation as a site's signature moment inside an Astro 7 plus Cloudflare Workers Static Assets stack, without breaking the native hash-based CSP, the Lighthouse perf budget, or accessibility. This skill is the how-to-embed, not how-to-author-in-Rive.

## TL;DR

- One renderer: `@rive-app/canvas` (Canvas2D). It has no WebGL context limit, so it never competes with a sibling WebGL shader background for the browser's per-page context budget. Use `@rive-app/webgl2` only when the Rive Renderer, mesh deformation, or edit-time fidelity is required. Never `@rive-app/webgl` (legacy, superseded by webgl2).
- Usage gate, hard: the Rive runtime is heavy. Measured first load is roughly 840 KB gzip for canvas (about 42 KB JS plus an 800 KB-class WASM); canvas-lite roughly halves the WASM. This is justified only by genuinely interactive, branching state-machine logic that CSS or GSAP cannot hand-code and that Lottie or dotLottie playback cannot match. For playback or a simple hover toggle, use the motion skill or a Lottie file instead. Ship at most one Rive instance per page.
- CSP, load-bearing: WebAssembly needs `'wasm-unsafe-eval'` in script-src or it is blocked. Self-host the WASM so its fetch and the .riv fetch stay same-origin (connect-src 'self'). Astro 7 native CSP can express both via security.csp; no real HTTP header is needed even though Cloudflare adapter v14 lacks staticHeaders. Details in csp-and-wasm.md.
- Off the critical path: the WASM is the heaviest thing in the stack. Lazy-init with a vanilla IntersectionObserver and dynamic import, never an above-the-fold island. A canvas is not LCP-eligible, so deferring it does not hurt LCP.
- Accessibility is not built in: Rive has no reduced-motion handling. If it autoplays or loops longer than five seconds, a visible keyboard-operable pause control is required for all users (WCAG 2.2.2, Level A). Reduced-motion handling is separate (WCAG 2.3.3, Level AAA).

## When to use this

Trigger when embedding a single interactive `.riv` (hover, click, scroll, or data-driven states) on a hero or feature element; when the Rive runtime is blocked by a CSP; when the heavy WASM runtime must come off the critical path; when wiring state-machine inputs from scroll or pointer; or when adding reduced-motion and a pause control to a Rive canvas.

Do not use for DOM tween or scroll-reveal animation (motion skill), generative shader backgrounds (webgl skill), authoring the `.riv` in the Rive editor (design work), or playback-only animation where Lottie, dotLottie, or CSS is lighter. The decision rule and the dotLottie caveat are in a11y-and-fallback.md and the gate below.

## The usage gate

Spend a Rive moment only when the interaction is real. Rive's differentiator is the state machine: booleans, numbers, and triggers driving branching transitions, blend states, listeners, nested artboards, and data-bound runtime values. That earns the WASM weight, spent once as the page signature.

| Need | Tool |
|---|---|
| Two-state hover, fade, simple transition | CSS or the motion skill |
| Playback of a designer illustration, looping decoration | Lottie or dotLottie |
| Generative atmospheric background | the webgl skill |
| Branching interactive state logic, designer-authored | Rive (this skill) |
| A second animated moment on the same page | not a second Rive instance, use CSS or Lottie |

The Lottie boundary, updated W4 (verified 2026-08-18): dotLottie's v2.0 spec ships NATIVE state machines (stored in the .lottie archive itself, no JS glue) and the player is `@lottiefiles/dotlottie-web` 0.79.1 (MIT, Rust plus ThorVG core — roughly 57 KB JS gzip plus a 700 KB-class WASM, so no lighter than Rive); legacy `lottie-web` has been stalled since late 2024 and is maintenance-only. dotLottie state machines cover modest interactivity (hover, click, loading states) but do NOT match Rive's depth — no data binding, no scripting-grade control. The cost side moved too: Rive's 2025-10-20 pricing restructure keeps the editor free but gates .riv EXPORT behind the paid Cadet tier ($9 per seat per month) — the designer-authored .riv this skill integrates now presupposes a paid seat on the DESIGN side; the `@rive-app/canvas` runtime stays MIT and free. Net rule: for the ONE signature interactive moment, Rive remains the pick on depth and maturity, with its export cost named; for modest interactivity on a zero budget, a dotLottie v2 state machine is the honest $0 alternative — and playback-only still wants plain Lottie playback or CSS, never either runtime.

## Stack and versions

canvas and webgl2 re-verified 2026-08-17 on npm (lockstep train, published same day); the lite, single, and react rows are as of 2026-06-18 (their trains have since caught up to 2.40.0-era releases). Rive web runtimes churn weekly, so re-pin everything at install.

| Package | Version | Role |
|---|---|---|
| `@rive-app/canvas` | 2.40.0 | default, Canvas2D, no WebGL context limit |
| `@rive-app/canvas-lite` | 2.37.3 | no Rive Text or audio, about half the WASM |
| `@rive-app/webgl2` | 2.40.0 | only for Rive Renderer, mesh, fidelity — 2.40.0 shrank the package about 11.5 percent (Emscripten 4.0.23, -Os) |
| `@rive-app/canvas-single` | 2.38.0 | WASM inlined in JS, no separate WASM fetch |
| `@rive-app/react-canvas` | 4.28.0 | only if the page is already a React island |
| `@rive-app/webgl` | legacy | avoid, superseded by webgl2 |

Pick canvas-lite over canvas when the `.riv` uses no Rive Text, audio, or scripting; it nearly halves the WASM. Pick canvas-single only when a second network request for the WASM must be avoided for a hard CSP reason; it still needs `'wasm-unsafe-eval'`. The high-level canvas and webgl2 APIs are drop-in swappable.

## Setup in order

1. Install the runtime and self-host the WASM and the `.riv`. See csp-and-wasm.md for the `?url` imports and `RuntimeLoader.setWasmUrl`.
2. Add the CSP additions to security.csp: `'wasm-unsafe-eval'` in scriptDirective.resources and `connect-src 'self'`. Astro's per-bundle hashes stay additive. See csp-and-wasm.md.
3. Reserve the canvas box in CSS to prevent layout shift, then lazy-init the runtime with a vanilla IntersectionObserver and dynamic import. See rive-runtime-setup.md.
4. Wire interaction: editor Listeners handle hover and click internally; drive scroll or data with state-machine inputs from a passive listener plus requestAnimationFrame. See state-machine-and-triggers.md.
5. Add reduced-motion handling, a pause control if it autoplays or loops, and a static poster fallback. See a11y-and-fallback.md.
6. Build and preview to verify CSP. CSP is not enforced in astro dev. Measure the served brotli WASM size and set the perf budget against it.

## Gotchas

- The ~200 KB figure for Rive is outdated. Budget against the measured served size; the WASM has grown to an 800 KB-class raw binary on the canvas runtime.
- Set `automaticallyHandleEvents` to false (the default) so a `.riv` OpenUrl event cannot trigger navigation; subscribe to events explicitly if needed.
- Call `resizeDrawingSurfaceToCanvas()` in the onLoad callback and on resize for crisp device-pixel-ratio rendering.
- Call `cleanup()` on teardown to free the C++ and WASM objects; pause when scrolled offscreen and on visibilitychange.
- `stateMachines` must be supplied at construction, or Rive plays the first linear animation instead of the state machine.
- Avoid a non-root Astro `base`; a known adapter bug can leave assets unprefixed and 404 under Workers Static Assets.

## Limitations

- This skill does NOT cover authoring the `.riv` in the Rive editor, DOM or scroll-reveal animation (motion skill), generative shader backgrounds (webgl skill), or playback-only animation (Lottie, dotLottie, CSS).
- The exact compressed WASM transfer size is version-volatile and must be measured at build; do not assume the runtime is small.
- Re-pin all Rive packages at install; they publish weekly.

## References

- [rive-runtime-setup.md](./references/rive-runtime-setup.md): renderer choice, sizes, vanilla lazy-init, lifecycle, cleanup.
- [csp-and-wasm.md](./references/csp-and-wasm.md): self-hosted WASM, the wasm-unsafe-eval CSP recipe, connect-src, .riv asset handling.
- [state-machine-and-triggers.md](./references/state-machine-and-triggers.md): inputs, listeners, scroll wiring, event handling.
- [a11y-and-fallback.md](./references/a11y-and-fallback.md): reduced-motion, the WCAG pause decision tree, the poster fallback.

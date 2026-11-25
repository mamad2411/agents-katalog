---
name: webgl-atmosfera
description: Use to build a premium WebGL hero atmosphere — a lazy-loaded full-screen fragment-shader animation behind hero content — on Astro 7 plus Cloudflare. Covers the renderer choice (a vendored raw WebGL2 helper default, OGL or twgl as alternatives, WebGPU ruled out for a single decorative draw call), the fbm domain-warped flow-field shader pattern, lazy initialization that protects LCP and CLS, hash-based CSP parity with Astro-bundled scripts, the mandatory pause control and reduced-motion fallback for accessibility, runtime cost controls, and the scroll-driven uniform seam. Trigger on phrasings like build a WebGL hero background, animated shader atmosphere, gradient mesh hero, full-screen GLSL background in Astro, lazy canvas hero, fix my shader hero performance, or make my animated background accessible. Do NOT use for general WebGL or Three.js 3D scenes, game rendering, data visualization, production UI components, or non-hero canvas work. For CSS-achievable background or gradient animation use motion-system.
---

# WebGL Atmosphere for an Astro Hero

> A minimal, defensible pattern for a lazy-loaded full-screen fragment-shader hero background on Astro 7 plus Cloudflare. The discipline is in the constraints — survives a hash-based CSP, a CI performance budget, and WCAG — not in the shader artistry.

## TL;DR

- Renderer default is a vendored raw WebGL2 helper — zero dependency, zero library bytes, WebGL2 is effectively universal. OGL (`ogl@1.0.11`, vendored Core subset) is the ergonomic alternative when a second render pass is likely; twgl is the maintained middle. WebGPU is out for this use case.
- The canvas is never the LCP element, so the hero headline or a foreground image must render independently and fast. Initialize the shader after the critical render via requestIdleCallback plus IntersectionObserver — not the client:visible directive, which fires immediately above the fold.
- A visible, keyboard-operable pause control is mandatory, not optional. A continuously animating decorative background that auto-starts, runs over five seconds, and sits in parallel with content is a WCAG SC 2.2.2 target. Honoring prefers-reduced-motion plus aria-hidden does not satisfy it alone.
- The shader script is bundled by Astro and hash-emitted into script-src, the same way a bundled motion library is. Author shaders as JS template-literal strings so nothing is fetched at runtime.

## When to use this skill

Use when building or fixing a full-screen animated shader background behind a hero on this stack — choosing the renderer, writing the atmosphere shader, wiring lazy load without breaking Core Web Vitals or the CSP, making it accessible, or driving a shader uniform from scroll. Do not use for interactive 3D scenes, games, charts, or any canvas that carries meaning rather than decoration.

## Decision flow

1. Confirm the effect genuinely needs WebGL. A slow drift of two or three colors is cheaper and safer as a CSS gradient — see the boundary in `references/atmosphere-shader-pattern.md`. Only a per-pixel noise, turbulence, or domain-warp flow at 60 fps justifies the canvas.
2. Pick the renderer. Default to the vendored raw WebGL2 helper; reach for OGL or twgl only on the stated triggers. See `references/renderer-and-library.md`.
3. Write the shader from the fbm domain-warp reference. See `references/atmosphere-shader-pattern.md`.
4. Wire the load so it protects LCP and CLS, and confirm CSP parity. See `references/astro-load-and-csp.md`.
5. Add the fallback and the accessibility controls. The pause control is a gating requirement. See `references/fallback-and-a11y.md`.
6. Add runtime cost controls and the scroll-to-uniform driver. See `references/perf-and-scroll-seam.md`.

## Reference materials — load when relevant

This SKILL.md is the router and the locked verdict. Load a reference only when its step is active:

- `references/renderer-and-library.md` — load when choosing or vendoring the renderer, or when asked why WebGPU is out. Carries the raw WebGL2 helper.
- `references/atmosphere-shader-pattern.md` — load when writing the shader, explaining fbm or domain warping, or deciding WebGL versus a CSS gradient.
- `references/astro-load-and-csp.md` — load when wiring the Astro island, protecting LCP or CLS, or hashing the script into the CSP.
- `references/fallback-and-a11y.md` — load when building the no-WebGL fallback, handling context loss, or meeting WCAG. The pause-control requirement lives here.
- `references/perf-and-scroll-seam.md` — load when capping runtime cost or driving a uniform from scroll.

## The locked verdict

| Fork | Verdict |
|---|---|
| Renderer | Vendored raw WebGL2 helper default; OGL `1.0.11` Core subset or twgl `7.0.0` as documented alternatives |
| WebGPU | Out — a single draw call uses none of its advantages; WebGL2 is the floor; still not Baseline per MDN |
| Shader | Domain-warped fbm flow field; precision declared, loop counts bounded, tested on real mobile |
| Load | Canvas not LCP-eligible; init via requestIdleCallback plus IntersectionObserver; reserve the canvas box for CLS |
| CSP | First-party module bundled and hash-emitted into script-src; shaders as template literals, no connect-src |
| Fallback | Static AVIF or WebP via astro:assets primary; CSS token gradient secondary; no video |
| Accessibility | Mandatory pause control (SC 2.2.2); reduced-motion shows the fallback; aria-hidden decorative |
| Runtime | Clamp devicePixelRatio, cap frame rate, pause off-screen and when hidden, gate mobile to the fallback |
| Scroll seam | Drive the uniform from the renderer rAF reading a passive scroll listener; involve a motion library only if the page already loads it |

## Limitations and out-of-scope

- This skill does NOT cover interactive 3D, Three.js scenes, games, data visualization, or any meaningful canvas content. It is decorative-background only.
- The exact tree-shaken byte cost of an OGL minimal subset is not published anywhere — measure it in the build before writing the budget.json line.
- WebGPU Baseline status is contested between industry sources and MDN. The verdict does not depend on it, but the rationale does — see the reference.
- WCAG conformance here addresses SC 2.2.2 (Level A) and SC 2.3.3 (Level AAA) for this component only, not whole-page conformance.

## References

- [renderer-and-library.md](./references/renderer-and-library.md): renderer choice, vendoring, WebGPU, the raw WebGL2 helper.
- [atmosphere-shader-pattern.md](./references/atmosphere-shader-pattern.md): the fbm domain-warp shader and the WebGL-versus-CSS boundary.
- [astro-load-and-csp.md](./references/astro-load-and-csp.md): lazy init, LCP and CLS, CSP parity.
- [fallback-and-a11y.md](./references/fallback-and-a11y.md): fallback, context loss, WCAG, the pause control.
- [perf-and-scroll-seam.md](./references/perf-and-scroll-seam.md): runtime cost controls and the scroll-to-uniform driver.

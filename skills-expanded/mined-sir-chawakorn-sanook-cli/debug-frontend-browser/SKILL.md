---
name: debug-frontend-browser
description: Diagnoses runtime UI bugs live in the browser — console/network errors, hydration mismatches, failed renders, CORS, broken interactions; used when a page misbehaves at runtime.
when_to_use: When the UI misbehaves at runtime — blank screen, hydration mismatch error, console/network errors, CORS failures, broken click/interaction, or 'works in dev not prod' — and needs live browser inspection.
---

## When to Use

The page is **already rendering (or failing to) in a real browser** and behaves wrong. Reach here when:

- Blank/white screen, partial render, or content flashes then disappears.
- Console error: `Hydration failed`, `Text content does not match server-rendered HTML`, `Cannot read properties of undefined`, etc.
- Network tab shows 4xx/5xx, a request stuck pending, or a CORS rejection.
- A click/submit/keypress does nothing or fires the wrong handler.
- "Works in dev, breaks in prod" (minified build, different env, SSR vs CSR mismatch).

Not for: build/compile failures (no browser yet), pure logic bugs reproducible in a unit test, or backend-only errors. Route those to general root-cause debugging. This skill is **browser-runtime UI** only and uses the `chrome-devtools` MCP to inspect a live page.

## Steps

1. **Get a live page.** `list_pages` to see open tabs; `select_page` the offending one, or `new_page` + `navigate_page` to the failing URL. Reproduce the exact state the bug needs (route, query params, logged-in session). If repro needs interaction, drive it: `click` / `fill` / `press_key`. Note: a fresh `new_page` has no auth cookies — reuse the existing tab when the bug is session-dependent.

2. **Drain the console first.** `list_console_messages` — read every `error` and `warning`, not just the top one. The *first* error is usually the root; later ones are fallout. Capture the full stack trace via `get_console_message` for the key error. Map minified frames back to source using the file:line in the trace (sourcemaps); if prod sourcemaps are absent, re-run the same flow against the dev/staging build to get readable frames.

3. **Check failed network requests.** `list_network_requests`, then `get_network_request` on anything non-2xx, pending, or that the failing component depends on. Inspect: status code, response body (real error message often lives here, not the console), request/response headers. For **CORS**: confirm the server returned `Access-Control-Allow-Origin` matching the page origin and, for preflight, that the `OPTIONS` request succeeded with the right `Access-Control-Allow-Methods/Headers`. CORS is a *server-config* fix — never "fix" it by disabling browser security or proxying around it silently.

4. **Hydration mismatch (Next.js / React).** The cause is server HTML ≠ first client render. Hunt for non-deterministic-in-render values: `Date.now()` / `new Date()` / `Math.random()`, `window`/`localStorage`/`navigator` read during render, `typeof window !== 'undefined'` branches, locale/timezone-dependent formatting, and invalid DOM nesting (`<div>` inside `<p>`, `<p>` inside `<p>`). Take `take_snapshot` to see the actual client DOM and compare against the SSR HTML (view the document response in `get_network_request`). Fix at source: gate client-only values behind `useEffect`/mounted-flag or `next/dynamic({ ssr: false })`. Use `suppressHydrationWarning` **only** for genuinely unavoidable per-render values (e.g. a timestamp) — it silences the warning, it does not fix a real divergence.

5. **Layout / styling bug.** `take_screenshot` for the visual, `take_snapshot` for the structured DOM + roles. `evaluate_script` to read computed styles on the culprit node (`getComputedStyle(el)`), bounding box, overflow, z-index, and whether the element is actually in the DOM vs `display:none`/zero-size. Distinguish "not rendered" (missing from snapshot) from "rendered but invisible" (present, hidden by CSS).

6. **Broken interaction / event wiring.** Confirm the handler is attached and the right element receives the event. `evaluate_script` to inspect listeners, check for an overlay intercepting clicks (`document.elementFromPoint(x,y)`), `pointer-events:none`, disabled state, or a stale closure capturing old state. Reproduce the click with `click` and re-read the console/network to see what (if anything) fired. For React state bugs, log or read the value at the moment of interaction rather than assuming.

7. **Confirm root cause, fix at source.** Tie the symptom to one concrete cause (a specific request, a specific render expression, a specific listener). Fix the source code — do **not** swallow the error with an empty `catch`, a blanket `try/catch`, or by hiding the failing UI.

8. **Verify live.** Reload via `navigate_page` (or `reload`), re-run the repro interaction, then re-check: `list_console_messages` clean of the original error, `list_network_requests` shows the request now 2xx, `take_screenshot` shows correct render. Show the before/after as evidence — do not declare fixed on code-read alone.

## Common Errors

- **Reading only the first console line.** The headline error is often downstream; scroll the full list and trace the earliest one.
- **Trusting the console over the network body.** A `500` shows a generic message in console but the real stack/error is in the response body — always `get_network_request` it.
- **"Fixing" CORS client-side.** Adding `mode: 'no-cors'`, disabling web security, or routing through a hack hides it. CORS is fixed on the server's response headers (or preflight) only.
- **Blaming hydration on the wrong line.** React points at the mismatched node, but the cause is *why* server and client disagree there — usually a non-deterministic value or a `window` read, not the JSX at that line.
- **`suppressHydrationWarning` as a cure.** It mutes the symptom. If the underlying data genuinely differs, you've shipped a silent inconsistency. Use it only for inherently dynamic content, never to paper over a real bug.
- **Fresh tab missing auth.** `new_page` starts with no session — a bug that needs login won't reproduce. Reuse the existing authenticated tab.
- **Minified prod stack with no sourcemap.** Frames like `a.b is not a function` are useless; reproduce against dev/staging to get real file:line.
- **Stale page state.** Inspecting after the error already cleared (e.g. an error boundary swapped the UI) shows the recovered state. Re-trigger the failure, then inspect immediately.
- **Race / timing.** Element or data not there yet — use `wait_for` on the target before asserting it's missing, instead of concluding it never renders.

## Verify

Fix is done only when all hold against the live page:

- [ ] Original console error/warning gone from `list_console_messages` after reload + repro.
- [ ] Previously-failed request now returns 2xx with a valid body (check `get_network_request`).
- [ ] `take_screenshot` shows the page rendering correctly through the exact repro steps.
- [ ] The broken interaction now fires the correct handler and produces the expected result.
- [ ] No new errors introduced, and the error is fixed at source — not suppressed, caught-and-ignored, or hidden.
- [ ] If it was a "dev-only / prod-only" bug, verified in the build that originally failed.

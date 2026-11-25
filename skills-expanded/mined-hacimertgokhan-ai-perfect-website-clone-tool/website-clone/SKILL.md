---
name: website-clone
description: Clones an authorized website from a URL with high visual and behavioral fidelity. Use when the user asks to clone, recreate, replicate, reverse-engineer, or pixel-match a website, landing page, web app, responsive layout, animations, assets, or mock API behavior using Playwright or Puppeteer.
license: MIT
compatibility: Requires Node.js 20+ and network access. Browser capture helpers install Playwright, Puppeteer, and pixelmatch on first run.
metadata:
  category: frontend
  browsers: playwright-puppeteer
---

# Website Clone

Recreate websites as maintainable local applications, preserving the observable design and behavior while replacing server dependencies with deterministic mock data. Measure first, implement second, compare continuously.

## Non-Negotiable Boundaries

- Proceed only for public pages or pages the user owns or is authorized to inspect and reproduce.
- Do not bypass authentication, CAPTCHAs, paywalls, robots controls, rate limits, anti-bot systems, or access restrictions.
- Never collect passwords, session cookies, authorization headers, API keys, payment details, personal form entries, or other secrets. Use a clean browser context with no imported user profile.
- Do not submit destructive or transactional actions. Do not purchase, publish, delete, invite, upload, or send messages.
- Prefer original replacement assets for third-party trademarks, copyrighted media, and proprietary copy unless the user confirms reuse rights. Preserve dimensions and placement with placeholders when rights are unclear.
- Reimplement observable behavior. Do not copy minified proprietary source code, hidden business logic, private APIs, analytics identifiers, or tracking scripts.
- Keep all crawling on the target origin unless the user explicitly authorizes additional origins. External CDN assets referenced by the page may be inventoried but should not trigger site crawling.
- If authorization or scope is ambiguous, ask one short question before capture.

## Required Input

Obtain or infer:

- Target URL and allowed routes.
- Destination project directory.
- Public-only or authorized authenticated scope. Authentication requires user-provided test credentials and explicit permission; never persist them.
- Required fidelity: selected page, route set, or complete public site.
- Asset policy: reuse authorized assets or build dimensionally equivalent replacements.

Default to public pages, same-origin routes, desktop + tablet + mobile, reduced-motion validation, local mock APIs, and no third-party trackers.

## Tool Strategy

Use browser tools when available, then use bundled scripts for reproducible artifacts.

1. Playwright is the primary observation engine: navigation, accessibility snapshot, screenshots, video, traces, runtime styles, scroll states, route discovery, requests, responses, and interaction states.
2. Puppeteer is the independent CDP pass: stylesheet/script inventory, performance entries, DOM/event clues, CSS animations, Web Animations API, and request/response verification.
3. Normal code tools inspect and edit the destination project.
4. Visual comparison closes the loop at every target viewport.

Do not rely on a screenshot alone. Do not infer implementation details that can be measured in the browser.

## Capture Commands

Scripts are relative to this skill directory. Run from any directory using the absolute path to this skill.

```bash
bash <skill-dir>/scripts/setup.sh
node <skill-dir>/scripts/capture-playwright.mjs --url https://example.com --out .clone-audit --routes /,/pricing
node <skill-dir>/scripts/capture-puppeteer.mjs --url https://example.com --out .clone-audit
node <skill-dir>/scripts/download-assets.mjs --manifest .clone-audit/playwright/pages.json --out public/assets
```

Optional flags:

```text
--viewport 1440x1000       Override the primary viewport
--routes /,/about,/pricing Comma-separated same-origin routes
--max-pages 20             Route capture limit
--delay 1200               Post-load settling time in milliseconds
--motion-steps 20          Forward and reverse samples per scroll axis
--frame-delay 80           Settle time between motion samples
--max-scrollers 5          Window plus nested scroll containers
--max-interactions 40      Hover/focus/safe-click targets per state type
--interaction-steps 8      Transition frames after each interaction
--load-duration 3000       Initial load animation capture duration
--load-interval 100        Initial load frame interval
--headed                    Show browser during capture
```

Store audit output in `.clone-audit/` and exclude it from production bundles and git unless the user asks to keep it.

## End-to-End Workflow

### 1. Inspect the Destination

- Read the framework, package manager, routes, source layout, CSS strategy, Tailwind version, component system, lint/test/build commands, and existing user changes.
- Preserve the existing stack when viable. For an empty directory, choose the smallest suitable stack; default to Vite + React + TypeScript for interactive sites and static HTML/CSS/JS for truly static pages.
- Do not initialize or overwrite files until the destination and target scope are clear.

### 2. Establish a Capture Baseline

- Capture at minimum `1440x1000`, `1024x768`, and `390x844`. Add widths immediately before and after measured breakpoints.
- Record load animation frames, then sample every scrollable container forward and backward at no fewer than 20 steps. Save viewport PNG frames plus computed style, bounds, CSS variables, pseudo-elements, WAAPI progress, canvas metadata, sticky state, and per-frame deltas.
- Record a normal-motion pass and a `prefers-reduced-motion: reduce` pass.
- Move the pointer through a grid at top, 25%, 50%, 75%, and bottom page positions. Capture mouse/pointer-driven transforms, custom properties, cursor followers, spotlight/tilt effects, canvas/WebGL output frames, and requestAnimationFrame behavior.
- Discover hover targets from CSS `:hover` selectors, event listeners, pointer cursors, transitions, and semantic controls. Capture before/after state plus transition frames with computed styles, WAAPI progress, pseudo-elements, and screenshots for hover and focus.
- Safely exercise menus, drawers, tabs, accordions, carousels, dialogs, and non-transactional `type=button` controls. Never auto-click purchase, payment, submit, send, save, delete, publish, upload, logout, or similar actions.
- Wait for fonts, images, videos, and lazy content to settle. Scroll the entire page once before final screenshots.
- If consent UI appears, record it but do not accept tracking unless required for layout and authorized.

### 3. Build the Evidence Inventory

Review generated `manifest.json`, `network.json`, `endpoints.json`, `pages.json`, per-page JSON, Puppeteer `runtime.json`, `stylesheets.json`, routes, traces, videos, and screenshots. Create `clone-spec.md` in the destination containing:

- Route map and navigation graph.
- Page sections in visual order.
- Typography: family, source, weight, size, line height, letter spacing, casing.
- Color tokens including backgrounds, text, borders, states, overlays, and gradients.
- Spacing, container widths, grid columns, gaps, radii, shadows, borders, and z-index layers.
- Breakpoints and structural responsive changes, not merely shrinking values.
- Asset table with source URL, local destination, intrinsic size, rendered size, crop mode, and page usage.
- Motion table using the schema in `references/motion-schema.md`.
- Interaction/state table: trigger, initial state, transition, final state, keyboard behavior, and URL effect.
- API table: method, sanitized path, request shape, response shape, state variants, latency, and consuming component.

### 4. Recover Assets Responsibly

- Download only assets required for authorized reproduction. Keep stable, descriptive local filenames and preserve file formats when practical.
- Inventory responsive `srcset`, `<picture>` sources, CSS backgrounds, masks, SVGs, icons, poster images, videos, fonts, favicons, and Open Graph assets.
- Strip query signatures and credentials from saved metadata. Never commit bearer tokens, signed URLs, cookies, source maps containing secrets, or analytics payloads.
- Optimize only after visual equivalence is established. Preserve alpha, crop, color profile, animation, and playback behavior.
- Replace tracking, chat, advertising, fingerprinting, and analytics scripts with nothing or inert local adapters.

### 5. Model Data and Mock the Backend

- Treat captured network traffic as a contract, not as production data to copy blindly. Correlate each XHR/fetch with load, scroll, pointer, hover, focus, or safe-click interaction labels so lazy and interaction-triggered endpoints are included.
- Sanitize identifiers and personal content. Create representative fixtures for loading, success, empty, validation-error, server-error, and pagination states when the UI exposes them.
- Preserve request method, path shape, query semantics, status codes, content type, response envelope, ordering, and realistic latency.
- Use the project's existing mocking approach. Otherwise prefer MSW for browser/API interception or minimal local framework route handlers.
- Keep fixtures separate from UI components. Mutations must update in-memory mock state so interactions remain believable during a session.
- Never proxy the clone to the original private backend unless the user explicitly requests and authorizes it.

See `references/mock-api.md` for the contract format and implementation checklist.

### 6. Rebuild in Fidelity Order

Implement in this order to avoid polishing the wrong geometry:

1. Route shell, font loading, reset, theme tokens, global background, and main containers.
2. Section order, DOM semantics, large layout, positioning, overflow, and stacking contexts.
3. Responsive breakpoints and structural mode changes.
4. Typography metrics and text wrapping.
5. Assets and media behavior.
6. Controls, navigation, forms, and state machines.
7. Scroll-linked, entrance, hover, focus, marquee, parallax, canvas, and video behavior.
8. Fine visual details: borders, shadows, gradients, masks, filters, noise, and cursor treatment.

Use the target's measured design system. Do not impose generic cards, arbitrary gradients, different icon libraries, or unnecessary abstractions. Reuse components only where repetition is real.

### 7. Recreate Motion Precisely

- Identify trigger type: load, intersection, scroll progress, hover, focus, click, route change, media event, or timer.
- Measure property, keyframes, duration, delay, easing, iteration count, direction, fill mode, transform origin, stagger, and threshold.
- Determine whether motion is CSS, Web Animations API, requestAnimationFrame, GSAP, Framer Motion, Lottie, canvas/WebGL, or media-driven. Recreate the observed output with maintainable local code; matching the original library is not required.
- Prefer transform and opacity for smooth animation, but preserve layout animation when it is visibly intentional.
- Implement reduced-motion behavior. No essential content may depend solely on motion.
- Match pinning and sticky boundaries using measured scroll start/end positions, not guessed viewport values.

### 8. Compare and Iterate

Run the clone locally, capture the same route/state/viewport matrix, then compare:

```bash
node <skill-dir>/scripts/compare-images.mjs \
  --reference .clone-audit/playwright/screenshots/home-1440x1000-full.png \
  --actual .clone-audit/local/screenshots/home-1440x1000-full.png \
  --output .clone-audit/diff/home-1440x1000.png
```

Fix mismatches in this order: fonts and loading, viewport/background, containers, section heights, major positioning, text wrapping, assets, spacing, borders/shadows, then animation timing. A low pixel-diff score is supporting evidence, not the sole acceptance criterion; dynamic media and antialiasing require visual judgment.

### 9. Verify Behavior

- Test every internal route and meaningful interaction with Playwright.
- Verify keyboard navigation, visible focus, labels, headings, alt text, dialogs, escape behavior, and touch targets.
- Test no-JS/loading failure where relevant, empty/error mocks, mobile navigation, orientation changes, and reduced motion.
- Check console errors, failed requests, hydration warnings, overflow, CLS, autoplay failures, and missing assets.
- Run existing lint, typecheck, tests, and production build. Add focused tests for reconstructed state behavior and mock contracts.
- Confirm no clone page calls unauthorized original APIs or third-party trackers.

## Completion Criteria

Do not call the clone complete until:

- Authorized routes, sections, assets, states, and interactions are implemented.
- Target viewport screenshots have been compared and major differences resolved.
- Responsive behavior is correct between breakpoints, not only at sampled widths.
- Scroll and general animations match trigger, direction, range, easing, and reduced-motion behavior.
- Mouse movement, cursor followers, hover/focus, pseudo-elements, nested scrollers, load entrances, reverse-scroll behavior, canvas/WebGL frames, and safely reachable interaction states have evidence or an explicitly documented limitation.
- Mock endpoints cover all UI paths without secrets or personal production data.
- Internal navigation, forms, media, hover/focus/touch, errors, and loading states work.
- Console and network logs contain no unexplained failures.
- Lint/typecheck/tests/build pass, or remaining failures are explicitly reported.
- `clone-spec.md` documents measured decisions and known deviations.

## Reporting

Final output should state:

- Implemented routes and major behaviors.
- Mock API approach and fixture states.
- Verification commands and outcomes.
- Measured visual comparison status.
- Any intentionally replaced assets, inaccessible states, or known deviations.

Never claim pixel-perfect fidelity without matching-state screenshot evidence at desktop and mobile widths.

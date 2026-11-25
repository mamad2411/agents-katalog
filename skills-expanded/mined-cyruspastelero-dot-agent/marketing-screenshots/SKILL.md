---
name: marketing-screenshots
description: Generate professional App Store marketing screenshots for an iOS app (and its watchOS companion) — capture real app screens on dedicated simulators (signed-in, seeded, polished status bar), then compose them with puppeteer into branded slides (gradient background, frosted-glass headline card with the app icon, tilted overlapping device mockups) at current App Store sizes, laid out for fastlane deliver. Use when asked for "marketing screenshots", "App Store screenshots", "watch screenshots", "store listing images", or to refresh a listing's screenshots before a release.
disable-model-invocation: true
---

# Marketing Screenshots — capture real screens, compose branded slides

Two-stage pipeline, fully scripted so it can be re-run for every release. Reference layout: a `marketing/` folder holding `capture.sh` + `generate-screenshots.mjs`.

## Stage 0 — Plan the slides

- **5–6 slides**, one feature story each (home/dashboard, the core loop, the killer feature, content, retention/review, search or social proof). First slide sells the app, not a screen.
- Each slide = headline (3–5 words, benefit-first), subline (one sentence), gradient (per-slide hue family that matches the app's palette), and which screen it shows.
- Reuse the live listing's copy when it exists and is good — consistency beats novelty. De-slop anything new (no "seamless", "elevate", exclamation marks).

## Stage 1 — Capture raw screens (real app, real data)

1. **Dedicated simulators, never the user's**: create one per device class needed —
   iPhone 6.9" (`iPhone-16-Pro-Max` → 1320×2868) and, if the app supports iPad, iPad 13" (`iPad-Pro-13-inch-*` → 2064×2752). These are the current App Store sizes; captures at native size need no scaling.
2. **Polish the status bar**: `xcrun simctl status_bar <UDID> override --time "9:41" --batteryState charged --batteryLevel 100 --wifiBars 3 --cellularBars 4`.
3. **Real, good-looking state** — screenshots of empty screens sell nothing:
   - Sign in with the QA/test account (via the app's env hooks) so XP/streaks/content are real.
   - **First sign-in on a fresh sim hits onboarding** — bypass it (skip-auth/skip-first-run hook that keeps the session) or complete it once before capturing.
   - Seed missing states directly: the app's persisted JSON/SQLite in the sim container is editable (`simctl get_app_container <UDID> <bundle> data`) — e.g. make saved items due so the review screen shows "N cards due" instead of "All caught up".
   - **Audit every raw for photobombers**: leftover QA/test artifacts (test collections, debug names) sync into accounts — remove them and recapture.
4. Script it (`capture.sh <UDID> <outdir>`): terminate → launch with deep-link env hooks per screen → sleep → `simctl io screenshot`. Keep raws in `marketing/<device>/screen-N-<name>.png`.
5. **Look at every capture** before composing. A wrong state shipped to the store is worse than a delay.

## Stage 1w — Apple Watch companion apps

Watch listings are worth shooting when the app ships a watch target (add a `capture-watch.sh` and a `watch` branch in `generate-screenshots.mjs`).

- **One slide per real screen state**, not per feature — watch apps typically have ~3 photogenic states (idle, mid-interaction, success). Eyebrow label + headline only; no room for sublines at watch size.
- **Capture at a current ASC watch slot natively**: Apple Watch Series 11/10 46mm sim shoots 416×496 — exactly the store size, no scaling. Compose on a canvas of the same size (deliver infers the watch class from resolution, same as iPhone).
- **The watch app needs its own `--screenshot` mode** (DEBUG launch args via `simctl launch <udid> <watch-bundle-id> --screenshot --state idle|input|sent --text "..."`):
  - An unpaired sim reports the phone unreachable → disabled buttons and "iPhone not nearby" captions. **Stub reachability to true and skip WCSession activation** in screenshot mode.
  - **Pin transient screens open**: success/confirmation views that auto-dismiss after ~1.5 s will race the capture — gate the auto-dismiss `Task.sleep` behind the mode flag instead of racing it with sleeps.
  - Pre-seed the mid-interaction state (dictated text etc.) via a launch-arg — dictation/scribble can't be driven on a simulator at all.
- **`simctl status_bar` overrides are NOT supported on watchOS sims** — the corner clock shows real time. Accept it; don't burn time trying.
- Watch compose layout: eyebrow (letter-spaced small caps) + Clash/display headline top, single tilted watch below (dark bezel, ~76px radius at 292px screen width, crown + side button nubs on the right edge), same gradient/faint-glyph family as the iPhone set so the listing reads as one campaign.

## Stage 2 — Compose with puppeteer

`marketing/generate-screenshots.mjs` (npm-install puppeteer locally in `marketing/`, gitignore `node_modules`). Per slide, render an HTML page at the exact App Store canvas size and screenshot it. The proven look:

- **Gradient background** (3-stop, 170°) + radial highlight top-left.
- **Faint oversized hanzi/brand glyphs** (`rgba(255,255,255,0.05)`) behind the content — two per slide, relevant to the feature.
- **Frosted glass card** at top: app icon (rounded, from the asset catalog), serif display headline (Georgia stack reads premium), sans subline at 70% white.
- **Tilted overlapping devices**: primary device `rotate(-7deg) rotateY(-6deg)` with `perspective` on the stage, dark bezel + Dynamic-Island-era radius, cropped at the canvas bottom; a **second screen peeks behind** (opposite tilt, `brightness(0.82)`, lower z) — pair each slide with a *related* screen so adjacent slides tell a story.
- Keep all of it data-driven (slides array: file, peek, headline, subline, gradient, hanzi) so copy/angle tweaks are one edit + re-run.

Sizes as a `DEVICES` map ({canvas, deviceWidth, peekWidth, font sizes}) — one script renders every device class.

## Stage 3 — Wire into the release

- Lay the composed set into `fastlane/screenshots/en-US/` with sortable names (`iphone69_01_home.png`, `ipad13_01_home.png`, `watch_01_idle.png`) — **deliver infers device class from image resolution**, names only control order.
- In the release lane: `skip_screenshots: false, overwrite_screenshots: true` for the refresh release; flip back to skip afterwards if screenshots rarely change.
- Commit raws + composed set + scripts (screenshots are release artifacts; the repo is their history).

## Iterating with the user

Send the composed set as files after each render and expect taste feedback ("more tilt", "swap the pairing", "different copy"). Renders are cheap (~5 s/slide, captures reused) — iterate in minutes, don't defend a draft.

## Gotchas (each cost a re-render)

- Fresh sim + password sign-in → the system **Save Password sheet** and **onboarding** both eat your captures; handle before shooting.
- Test-suite residue (seeded collections, consumed due-queues) changes what screens show — re-seed/clean per capture run, don't assume yesterday's state.
- zsh doesn't word-split unquoted pair variables in `for` loops — write explicit per-device function calls in capture scripts.
- Keyboard visible in search-style screens is normal for store shots; don't fight it.
- iPad canvas/text scales are not proportional to iPhone — tune the `DEVICES` entries separately and eyeball both sets.

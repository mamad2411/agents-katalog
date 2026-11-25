---
name: visual-regression
description: Visual regression testing — Storybook-based VRT, Playwright screenshot comparison, determinism/flake control, baseline review workflow. Use when setting up or maintaining visual tests, screenshot diffs, Chromatic, or investigating "the screenshot test broke" failures. 日本語の依頼例:「スクショテスト導入」「ビジュアルリグレッション」「見た目の差分テスト」「スクリーンショットが毎回変わる」「Chromatic」。
---

# Visual Regression Testing

VRT catches what DOM assertions can't: layout breaks, token regressions, theme bugs, overflow. It complements — never replaces — behavioral tests. If a DOM assertion can express the check (text content, element presence), use that; VRT is for how things *look*.

## Stories are the VRT surface

- Component-level VRT runs over Storybook stories (Chromatic, or a Playwright/Vitest screenshot run against the built Storybook). Every visual state already has a story per the `storybook` skill — that catalog IS the snapshot suite. Don't build a parallel page-screenshot harness for component states.
- Runner precedence: if a vendor service (Chromatic) is already configured, add the story and stop — it's covered. Otherwise default to Playwright `toHaveScreenshot` against the built Storybook, baselines committed alongside the spec and (re)generated only in the CI container.
- Page-level VRT: `expect(page).toHaveScreenshot()` in Playwright for a handful of critical pages/themes only, as its own Playwright project running on fixture data — never bolt `toHaveScreenshot` onto a real-backend functional E2E spec (those follow `testing-playwright`). Full-page screenshots of every route is a flake farm, not coverage.

## Determinism — every flake source must be pinned

A VRT suite that cries wolf gets ignored; eliminate nondeterminism at the source:

- **Time**: mock the clock (`page.clock` / fake timers); seed any randomized data. Relative dates ("3 minutes ago") in fixtures, never real `Date.now()`.
- **Network**: all data via MSW/fixtures (same handlers as the test suites). No real API in VRT.
- **Fonts & images**: wait for `document.fonts.ready` AND for in-view images to finish decoding before capture — a half-loaded image is a diff. Self-hosted fonts only (a CDN hiccup is a diff).
- **Animation**: disable it — `toHaveScreenshot({ animations: 'disabled' })` is the primary mechanism. Emulating `prefers-reduced-motion` alone is insufficient: per `motion`, state-conveying animations reduce to a quick fade, which can still be captured mid-fade. Never screenshot mid-animation.
- **Environment**: baselines are generated in the SAME environment that compares them — the CI container (one OS, one browser, pinned versions, pinned `TZ=UTC` + locale, since `Intl` output differs per environment). Local-macOS baselines vs Linux CI = permanent font-rendering diffs. Use `--update-snapshots` in the CI container (or the vendor cloud) to (re)baseline (the bare flag updates only changed snapshots; pass `all` to force everything).
- **Scrollbars & caret**: content-dependent scrollbars and a blinking text caret cause intermittent diffs — size stories to their content and keep the caret hidden (Playwright's `toHaveScreenshot` does this by default).
- **Leftovers**: fixed viewport sizes; `mask` genuinely dynamic regions (avatars, maps) rather than widening thresholds.

## Thresholds & scope

- Keep `maxDiffPixelRatio` strict (≤ 0.01); a loose threshold silently approves real regressions. If a region forces looseness, mask that region instead.
- Screenshot the component/element under test, not the whole page, when the subject is a component — smaller surface, fewer false positives.
- Cover both themes and the key breakpoints for layout-critical pieces; don't multiply every story × every viewport × every browser reflexively (cost grows multiplicatively, signal doesn't).

## Baseline review — diffs are code review artifacts

- A visual diff is either a regression (fix the code) or an intended change (approve the new baseline in the PR). **Never auto-accept baselines, never regenerate-and-commit without looking at the diff** — that converts the suite into a rubber stamp.
- Baseline updates ship in the same PR as the change that caused them, so the reviewer sees code and pixels together.
- Recurring flake in one snapshot = fix the determinism cause or delete the snapshot; regenerating or re-running until the diff happens to pass is banned — same retried-pass-is-a-flake-report policy as `testing-playwright`.

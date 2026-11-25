---
name: portfolio-live-parity-check
description: Compare the local Jekyll portfolio build against the live GitHub Pages site after commits, pushes, or deploys. Use when Codex must verify that public routes, titles, text signatures, images, and navigation behavior on the live site match the approved local build.
---

# Portfolio Live Parity Check

## What this skill is for

Use this skill after publishing changes to prove that the live GitHub Pages site matches the local build.

## When to use it

Use this skill when:
- changes were pushed to `main`
- GitHub Pages rebuilt the site
- the user asks whether live and local are in sync
- a navigation, blank-render, image, or route mismatch is suspected

## When not to use it

Do not use this skill before a deploy unless the task is explicitly a pre-deploy local smoke check.
Do not use it for backing repo README/demo checks; use portfolio repo skills for that.

## Required inputs

- local Jekyll build destination `_site_check`
- local preview server
- live site URL, normally `https://adredes-weslee.github.io/`
- public routes from the built sitemap when available
- Playwright or HTTP checks for local/live comparison

## Required workflow

1. Build locally with `bundle exec ruby -S jekyll build --destination _site_check`.
2. Serve `_site_check` on a fresh safe local port.
3. Discover public routes from `_site_check/sitemap.xml` when available. If unavailable, use the known top-level pages plus `_projects/` and `_posts/` routes.
4. For each route, compare local and live:
   - HTTP status
   - document title
   - primary `h1`
   - main text signature
   - visible broken image count
5. Normalize extracted text before treating a route as mismatched.
   - Decode HTML entities.
   - Use UTF-8 decoding or browser `textContent` when PowerShell/HTTP output shows mojibake.
   - Normalize whitespace and common apostrophe/quote variants.
   - Prefer a browser-derived title/H1 check when a mismatch is only punctuation encoding.
6. For representative pages, capture local/live screenshots.
7. Run a navigation smoke check on both local and live:
   - Home -> Blog -> Projects -> Contact -> About -> Home
   - confirm each route renders immediately without a blank right-hand content area.
8. If live differs from local, identify whether the issue is:
   - GitHub Pages still rebuilding
   - stale browser cache
   - missing committed file
   - route/permalink mismatch
   - source/build divergence

## Expected outputs

- route count checked
- local preview URL
- live URL
- match/mismatch summary
- screenshot paths for representative local/live pairs
- specific failing routes when mismatches exist

## Validation and stop condition

Stop only when:
- local build passes
- every discovered route has a local/live verdict
- representative screenshots are captured
- navigation smoke check passes or the failure is reproduced clearly
- live/local mismatches are resolved or explicitly reported as pending deploy/cache issues

Do not claim the live site is updated until live routes match the local build.

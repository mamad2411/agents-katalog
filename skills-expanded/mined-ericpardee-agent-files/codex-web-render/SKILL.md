---
name: codex-web-render
description: >-
  Fetch JavaScript-heavy, client-rendered, or bot-protected web pages that the
  built-in WebFetch tool cannot read (WebFetch returns an empty body, a loading
  spinner, an "enable JavaScript" notice, or just nav/boilerplate from an
  un-hydrated app shell). Drives a real system browser headless (no visible
  window, ~5-10s) and returns the page's fully rendered visible text, falling
  back to the Codex CLI only if that fails. Use this when the target URL matches
  the bundled problem-sites list (e.g. claude.ai/share links and other
  single-page apps), or when a WebFetch result for any URL comes back empty,
  truncated, or like an un-rendered SPA shell.
---

# Codex Web Render

Render JavaScript-heavy or bot-protected pages with a real browser and return
the page's visible text. This exists because the built-in `WebFetch` retrieves
raw HTML without executing JavaScript, so client-rendered pages come back as
empty shells.

The script has two paths:

1. **Fast path (default).** A pre-written Playwright renderer (`scripts/render.py`)
   drives a real system browser (Brave Origin, then Chrome, then Chromium) in
   `--headless=new` mode with `--disable-blink-features=AutomationControlled`.
   No visible window opens, it takes ~5-10s, and that automation flag is what
   clears Cloudflare's non-interactive "checking your browser" challenge that
   plain headless Chromium gets blocked by.
2. **Codex fallback (opt-in).** Only if the fast path fails (browser missing,
   still challenged, empty content) and `RENDER_ALLOW_CODEX=1` is set does it
   hand the URL to `codex exec`, which is far slower because it boots the full
   Codex agent to write and run its own browser script. Without that variable a
   failed fast path exits 3 with a message and nothing else runs. Set
   `RENDER_NO_FAST=1` to skip the fast path.

## When to use this skill

Use it in either of these cases:

1. **The URL is on the known problem list.** Before calling `WebFetch`, read
   `problem-sites.txt` in this skill's directory. If the target URL contains any
   pattern listed there, skip `WebFetch` entirely and render with Codex. The
   list is seeded with `claude.ai/share`.

2. **A `WebFetch` result looks un-rendered.** If you did call `WebFetch` and the
   result looks like an un-hydrated shell, fall back to Codex. Tell-tale signs:
   - Near-empty body, or only nav/footer boilerplate with no real content.
   - Text such as "You need to enable JavaScript to run this app".
   - A loading spinner / skeleton and none of the content you asked about.
   - The body is suspiciously short relative to what the page should contain.

## How to render

Run the bundled wrapper script with the URL. It prints the rendered visible
text to stdout:

```bash
bash ~/.claude/skills/codex-web-render/scripts/render-url.sh "<URL>"
```

Use the printed text as the page content for the rest of your task. The script
tries the fast Playwright path first, so a typical run is ~5-10s with no window.
The first run may be a few seconds slower while `uv` resolves the `playwright`
package into its cache. If it exits 3 saying the Codex fallback is disabled,
report that to the User; only re-run with `RENDER_ALLOW_CODEX=1` if they say so,
because that path gives Codex full access and a headed browser.

## Maintaining the problem-sites list

When you find a new domain that consistently returns an un-rendered shell from
`WebFetch`, offer to add it so future fetches skip straight to Codex. Append one
URL substring per line to:

```
~/.claude/skills/codex-web-render/problem-sites.txt
```

Match on the most specific stable path that identifies the problem (a bare
domain like `example.com`, or a path prefix like `example.com/app`).

## Prerequisites

- Fast path: `uv` on PATH, plus a real Chromium-based browser installed (Brave
  Origin, Chrome, or Chromium). `uv` pulls in `playwright` on demand; no separate
  browser download is needed because it reuses the system browser binary.
- Fallback path: the Codex CLI installed and authenticated (`npm i -g
  @openai/codex` then `codex login`). Only needed if the fast path can't render.
  The script runs `codex exec --dangerously-bypass-approvals-and-sandbox` so the
  run is unattended, and only when `RENDER_ALLOW_CODEX=1` is set.

## Notes and limitations

- The fast path is windowless and free; the Codex fallback spends Codex
  usage/credits and is much slower. Only reach for this skill when `WebFetch`
  can't do the job.
- It renders a single page's text. It does not log in, click through flows, or
  bypass paywalls or auth walls. It uses a throwaway browser profile, so a page
  needing your session returns whatever a logged-out browser sees.
- Output is the page's visible text, not raw HTML or structured data.

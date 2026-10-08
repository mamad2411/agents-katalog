---
name: interactive-json-form
description: Build a self-contained, single-file interactive HTML page (explanations + multiple-choice votes + rank + free-form comments) whose responses round-trip as downloadable/importable JSON — no backend, no tracking — and publish it privately on your own host behind noindex + an unguessable path.
allowed-tools: Read, Write, Edit, Bash
---

# Interactive JSON Form — decision/survey pages with a client-side JSON round-trip

> **Self-Evolving Skill**: This skill improves through use. If instructions are
> wrong, parameters drifted, or a workaround was needed — fix this file
> immediately, don't defer. Only update for real, reproducible issues.

A **single self-contained `.html` file** that presents extensive explanations,
lets a small known audience (e.g. a CEO + data scientists) **pick options, rank
them, and comment**, then hands their input back as a **downloadable / copyable /
re-importable JSON** — with **no server, no submit endpoint, and no tracking**.
Published privately on your own host behind a `noindex` header + an unguessable
path, so it is reachable by whoever has the linkTelus-direct door) but blocked from crawlers/indexing.

## When to use this skill

- You need a few named humans to make **structured choices + free-form comments**
  on a set of options, and you want their answers back as **machine-readable JSON**
  you ingest directly.
- Mobile-friendly, re-openable (import a prior JSON to resume), zero tooling for
  the responder, and **no backend to stand up**.
- The audience is small and known → a downloadable JSON they send you beats a
  hosted collector; a public form would over-expose.

## When NOT to use it

- Anonymous mass surveys / thousands of respondents (use a real survey backend).
- You need server-side aggregation in real time (add a collector, or use Lark Base
  — see `../../lark-automation` for the Base decision-harness alternative).
- Multi-page sitemap sites with no JS → use the sibling **`page-template`** skill.

## Why this over Lark Base / Forms / cards (decided by research 2026-07-13)

Lark Base grids truncate long text (row-height/width are NOT API-settable), Forms
are read-only after submit with no create API, and cards are one-shot with a 30-day
window + a callback webhook. A self-contained HTML page has **none** of those
limits: full text wraps natively, edits are unlimited, and the JSON round-trip is
pure client-side. The cost is that responses come back as files, not a live table
— acceptable for a small known audience.

## The pattern (what makes it work)

1. **Data-driven options.** An `OPTIONS` array at the top of the inline `<script>`
   is the single source of truth; the DOM is generated from it. To reskin for a
   new decision, edit that array only.
2. **`collect()` → JSON.** Reads every control (respondent, per-option vote/rank/
   comment, overall) into a versioned object `{schema, respondent, role,
firstPick, overallComment, choices:[{id,title,vote,rank,comment}]}`.
3. **Three return paths, all client-side:**
   - **Download**: `Blob` + `URL.createObjectURL` + `a[download]` → a `.json` file.
   - **Copy**: `navigator.clipboard.writeText` (with `execCommand` fallback).
   - **Import**: `<input type=file>` → `FileReader` → `hydrate()` repopulates the
     form. Import→export is **byte-identical** (resumable editing) — assert this.
4. **`schema` version string** on every payload so the ingester can evolve.
5. **`beforeunload`** guard warns on unsaved edits.
6. **Self-contained**: inline `<style>` + `<script>`, no external requests, no
   fonts/CDN, `<meta name="robots" content="noindex, nofollow, noarchive,
nosnippet">`, `<meta name="referrer" content="no-referrer">`.

Start from **`templates/index.html`** in this skill — it is the working page
(built for the ODB × time-bar decision) with the mechanism intact; swap the
`OPTIONS` array + the two intro `.note` blocks and you have a new page.

## Verify before you ship (headless, local)

Render + exercise the JS with Playwright against `file://` (no login needed):
fill the form via `page.evaluate` (the radios are visually hidden labels — set
`.checked` + dispatch `change` rather than `page.check`), call `collect()`, then
reload a fresh page, `hydrate()` the JSON, `collect()` again, and assert the two
JSON strings are identical. Screenshot `fullPage:false` and eyeball it. See the
`local-shot.mjs` pattern.

## Publish privately on your own host (no web-server config change, no restart)

The pattern, not a particular server: point a hostname at a static docroot behind a web server that **already emits `header X-Robots-Tag "noindex, nofollow, noarchive, nosnippet"` globally**. A static file dropped into a subdirectory is then served instantly with noindex over the existing TLS chain — **no config edit, no reload**, so co-hosted services on the same door are untouched.

Substitute your own values for `$SITE_HOST` (the public hostname), `$SSH_HOST` (its ssh alias), `$DOCROOT` (the server's static root) and `$WEB_USER` (the account the web server runs as).

```bash
# 1. upload the built page
scp -q your-page.html "$SSH_HOST:/tmp/page.html"
# 2. drop it at an UNGUESSABLE path (docroot is usually server-owned → sudo)
ssh "$SSH_HOST" 'set -e
  P="<slug>-$(openssl rand -hex 16)"                          # unguessable path segment
  D="'"$DOCROOT"'/$P"
  sudo mkdir -p "$D"; sudo cp /tmp/page.html "$D/index.html"
  sudo chown -R '"$WEB_USER:$WEB_USER"' "$D"; rm -f /tmp/page.html
  echo "URL: https://'"$SITE_HOST"'/$P/"'
# 3. TRUE external reachability. An on-LAN 200 does NOT prove the WAN chain when
#    split-DNS short-circuits the hostname to a LAN address — verify from a host
#    that is genuinely outside your network.
ssh <some-external-host> 'curl -sS -o /dev/null -w "EXTERNAL %{http_code} TLS=%{ssl_verify_result}\n" https://'"$SITE_HOST"'/<PATH>/'
```

**Crawler-blocking layers** (this skill's default): (a) global `X-Robots-Tag
noindex` header (already on the door), (b) page `<meta robots noindex>`, (c) an
unguessable path with no inbound links. A 4th layer — **User-Agent blocking** —
needs a Caddy `@bots` matcher in the edge-route registry (`edge-routes.toml` +
`generate-edge-config.py`); it is a production config change, so treat it as
optional hardening, not default.

If your edge config is generated from a registry rather than hand-edited, change the registry and regenerate — that is the durable path, and it keeps the door reproducible.

## Ingesting responses

The JSON is exactly `collect()`'s output. Consume it directly; key on
`schema` for versioning and `respondent`/`role` to attribute. Merge multiple
respondents' files by `choices[].id`.

## Hard rules

- One file, no external network requests, no tracking, `noindex` in `<meta>`.
- Never a real submit/collector endpoint unless the user explicitly opts in
  (it turns a private artifact into a hosted service + a data-handling duty).
- Never publish to the door by hand-editing the live web-server config — drop
  a static file into the docroot (config-free) or change the **registry** + regen.
- Always verify the import→export round-trip is byte-identical before shipping.

## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Find this SKILL.md's canonical path before editing.
1. **What failed?** — Fix the instruction. If the deploy recipe drifted (docroot,
   header, sudo), fix it here AND cross-check `edge-routes.toml`.
2. **What worked better than expected?** — If a new control type (multi-select,
   drag-rank) recurs, fold it into `templates/index.html`.
3. **What drifted?** — Keep the JSON schema, the deploy commands, and the
   crawler-block layers aligned with reality.
4. **Log it.** — Evolution-log entry with trigger, fix, evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.

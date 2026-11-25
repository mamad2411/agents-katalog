---
name: work-canvas
description: >-
  Turn an agent's own work — progress, debugging, analysis, comparisons, decisions — into one
  self-contained, reviewable HTML page (a "work canvas" / 网页看板) the user opens in a browser.
  Use when the user asks to create an interactive, reviewable, "alignment", progress, status,
  comparison, or summary HTML / dashboard / report / 看板 to see where a long task stands, review
  and comment, compare options, or decide next steps — especially for long-running, multi-subsystem,
  or trial-and-error tasks where terminal logs are the wrong medium. Also use to close out a `/goal`
  command session with a progress/status report. Covers three artifact types: (1)
  progress/status reports, (2) review/decision memos, (3) comparison/leaderboards. Not for building
  product UIs or shipping web apps — use the frontend-design or web-artifacts-builder skills for those.
---

# work-canvas

Produce **one self-contained HTML file** that renders an agent's work for a human to understand and
act on. The output is a capture of work (a report/board), not an application.

## Workflow

1. **Pick the artifact type** and read its reference:

   | The user wants to… | Type | Read |
   |---|---|---|
   | See where a long/messy task stands, what broke, what's next | **Progress / status report** | `references/progress-report.md` |
   | Close out a `/goal` command session with a status artifact | **Progress / status report** | `references/progress-report.md` |
   | Review analysis or a plan, comment, and decide | **Review / decision memo** | `references/review-decision.md` |
   | Weigh options head-to-head and pick a winner | **Comparison / leaderboard** | `references/comparison.md` |

   If it's a blend (e.g. a progress report that ends in a decision), lead with the primary type and
   borrow blocks from the other.

2. **Write the body.** Copy `assets/starter.html` and fill the header, the **What needs your input**
   box, and the body sections from the reference's component recipes. Leave the `[[PASTE base.css]]`
   and `[[PASTE interactions.js]]` markers in place; reference local images with `[[IMG path]]`.

3. **Inline into one self-contained file.**
   - **Default (cheapest):** `python assets/assemble.py body.html canvas.html` — inlines + minifies
     `base.css` and `interactions.js` and embeds `[[IMG]]` images as `data:` URIs. The model never
     reads or re-emits the ~24KB of CSS/JS (~60% of a naive build's tokens). Static page? Delete the
     `<script>` block first.
   - **Fallback (no shell):** paste `base.css` and the needed `interactions.js` modules into the
     markers yourself (every module self-guards), and base64 images inline.
   - Either way: **one file, offline-openable, no CDN/external requests** — verify by double-click.

4. **Write it to the project, tell the user the path** (open if appropriate). For a long-running task,
   regenerate the *same* file in place so the link stays stable; **finalize only once all runs/data
   are complete**.

## Build economically

A styled page is token-heavy mostly because of the assets: the CSS+JS is ~24KB, and a naive build pays
for it twice — reading it in, then re-emitting it inline (~60% of the token cost). Two levers:
- **Use `assets/assemble.py`** (step 3) so the model writes only the content and the script inlines
  the assets — the biggest single saving, byte-identical result.
- **Delegate the build to a cheaper/faster model or sub-agent**: have it write the body from the
  gathered data + chosen `references/<type>.md`; reserve the capable model for gathering and
  structuring content. Even a small/local model produces a clean canvas.

## Non-negotiables (enforced for every page)

- **Self-contained, single file.** Inline CSS + JS, embed media, offline-openable.
- **Provenance footer.** State which agent / CLI + which backbone model + the date built it.
- **Surface only real input needs.** The *What needs your input* box lists **only genuine
  human-in-the-loop decisions** — never invent or pad questions already resolved, and don't propose
  unnecessary work. If nothing needs the user, say so.
- **Never confuse the reader.** Add a **legend** wherever a color, letter, or symbol encodes meaning,
  use plain labels, and never show a raw score the reader can't interpret. (Confusing presentation is
  the most common failure.)
- **Non-destructive.** Don't edit the user's source files from the page; show paste-ready output with
  a copy button. Redact PII and add a "review before sending" note for external-facing content.

## Theme & polish

- Default theme is **light "Anthropic"** (cream + coral); dark mode ships in the same stylesheet via
  `<html data-theme="dark">` and the toggle in `initTheme`. Dashboards often read better in dark — set
  the default per the user's taste. A project design system in `CLAUDE.md` overrides `:root`.
- The design system in `assets/base.css` is deliberately complete and restrained. For unusually
  bespoke visuals, lean on the **frontend-design** skill for the aesthetic, but keep this skill's
  structure and conventions.

## Files

- `assets/assemble.py` — inlines + minifies the assets and embeds `[[IMG]]` images into one
  self-contained file (the default build step; run it on your body).
- `assets/starter.html` — the skeleton to copy (paste-markers + mandatory blocks).
- `assets/base.css` — the dual-theme design system (inlined by the assembler).
- `assets/interactions.js` — opt-in vanilla-JS modules: `initTheme`, `initTabs`, `initTables`
  (sort+filter), `initLightbox`, `initCopy`, `initScrollspy`, `initPersist`.
- `references/*.md` — one per artifact type (section order, component recipes, guardrails).

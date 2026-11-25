---
name: build
description: Assembles landing page sections. GUARD against AI-slop and hardcodes. Refuses to work without DESIGN-LOCK. Uses only tokens from tokens.css. Bounded by the section list in DESIGN-LOCK §8. Runs /typography pass on every saved section. Verifies references/approved-manifest.md coverage per section.
---

# /build

Main assembler. Everything before this is preparation. Here HTML/CSS/JS sections come into existence.

## When to use

- After `/tokens` (tokens.css exists and is filled).
- After `/copy-analyze` (brief/copy-analysis.md with recommended structure exists).
- After `/blocks` (brief/blocks/*.md filled).
- After `/animation` (brief/animation.md exists — motion classes drive CSS).
- After `/media` and `/icons` (assets in site/media/).

## Requirements — HARD BLOCKING

Refuse to work if:
- `DESIGN-LOCK.md` is not fully LOCKED (any TBD remains).
- `site/css/tokens.css` has any value = `0` / empty / TBD comment.
- `brief/copy-analysis.md` is missing (we don't know the structure).
- The section requested is not in DESIGN-LOCK §8 "Section vocabulary".
- `references/approved-manifest.md` is missing (created by `/refs`; must exist even if empty).
- `brief/animation.md` is missing (created by `/animation`).

## Process

**Step 1. Read sources of truth**

- `DESIGN-LOCK.md` — what is allowed, what is not.
- `site/css/tokens.css` — which variables are available.
- `brief/copy-analysis.md` — section structure.
- `inbox/texts/*` — copy for this section.
- `brief/blocks/<block>.md` — if this is an interactive block.
- `brief/animation.md` — motion classes to apply per element.
- `site/media/_srcset-snippets.md` — ready `<img>` tags.
- `site/media/icons/_snippets.html` — ready inline `<svg>` snippets.
- `references/approved-manifest.md` — required elements for this section.

**Step 2. Agree on scope**

Ask the user:
- One section at a time? Or a list at once?
- Start with hero? With the contact form? Something else?

Recommendation: hero first (LCP-critical), then form (main CTA), then the rest.

**Step 3. Section assembly**

For each section:

**A. HTML in `site/index.html`**
- Use the existing skeleton (`.sec.sec-<name>` class).
- Semantic tags: `<section>`, `<h1>/<h2>`, `<button>`, `<form>`, `<label>`.
- `alt` on every `<img>`.
- ARIA where needed.

**B. CSS in `site/css/<section>.css`**
One CSS file per section. Add `<link>` to index.html.

Rules:
- **Only variables from tokens.css.** Verify after every write — grep `#[0-9a-f]{3,8}`, `\d+px` (except border 1px), `\d+ms`.
- Use `flex` / `grid` / `calc()` for positioning, no magic numbers.
- No inline styles in HTML.
- No `!important` (if needed — the problem is elsewhere).

**C. JS in `site/js/<section>.js`** (if interactive)
- Only via `window.track()` wrapper for analytics (from main.js).
- Read CSS variables via `getComputedStyle(document.documentElement).getPropertyValue()`.
- Never hardcode ms / colors.

**D. Animation classes from brief/animation.md**
For each element in the section, apply the animation class dictated by `brief/animation.md`:
- Card elements → `card-hover` class per §4.
- Headings → text animation class per §3.
- Sections → scroll reveal class per §2.
- The `--stagger-base-ms`, `--motion-multiplier`, computed durations already exist in tokens.css (written by `/tokens` after `/animation` ran).

**Step 4. Checks before saving**

**Step 4a. Hardcode grep-checks (auto):**
- Any hex color (`#[0-9a-f]`, `rgb(`, `rgba(`) except `--c-overlay` alpha? → block.
- Any hardcoded size (`\d+px` not in comments, except `1px` for border)? → block.
- Any hardcoded duration (`\d+ms`)? → block.
- Any emoji in HTML? → block.
- More than 2 different font-weights per section? → block.
- Section uses a radius other than `var(--radius)`? → block.

**Step 4b. Typography pass** — call `/typography` on the saved HTML fragment. It walks text nodes, ties short words with `&nbsp;`, and prevents orphans/dashes at line end. This runs silently as part of `/build` — see [typography SKILL.md](../typography/SKILL.md) for the rule set and the canonical short-word list.

**Step 4c. Manifest coverage** — read `references/approved-manifest.md`. For every item whose section-scope matches the current section (e.g. `[ ] motif: horizontal thin rule between sections`, `[ ] icon:privacy → footer/trust`, `[ ] animation:card-hover:lift`) — verify the item is present in the generated HTML/CSS.

If a manifest item that must appear in this section is missing:
- **Do not save.** Report which item is missing and where it is expected.
- Ask user: implement it now, or explicitly remove the item from the manifest with a decision-log entry.

If the item is present — mark the checkbox `[x]` in the manifest.

**Step 4d. Anti-AI-slop checks:**
- Section not in DESIGN-LOCK §8? → block.
- More than one gradient? → block.
- Center-align on a section if it's > 50% of the page? → warning.
- More than one icon style? → block.

If any check fails — do not save, return an error citing the line.

**Step 5. Save + preview**

Save HTML + CSS + (JS if any).
Suggest: `python -m http.server 8000` — view in the browser.

**Step 6. Iterate**

- User views.
- Feedback → edits (without changing DESIGN-LOCK).
- Edits only within this section's scope — no "improve the neighbor".

## Rules of behavior

- **One section — one responsibility.** Do not mix hero + proof in one file.
- **Do not invent components.** Button = `<button class="btn">`. Not `<div role="button">`.
- **Do not "fix" the brief during build.** If copy is weak — go back to `/copy-analyze`.
- **Nothing decorative.** Every element has a function.
- **Never silently drop a manifest item.** If it can't fit, ask the user to remove it explicitly.

## What NOT to do

- Do not edit DESIGN-LOCK.md (explicit user override only).
- Do not edit tokens.css (only `/tokens`).
- Do not add dependencies (jquery, tailwind, react — no).
- Do not "improve" existing sections when the task is a new section.
- Do not create "utility" pages without a request.

## Next

- `/mobile` — mobile adaptation.
- `/audit` — pre-ship check.

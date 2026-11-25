---
name: clone-design
description: End-to-end website cloning, landing-page remix, and DESIGN.md extraction skill. Use when Codex is asked to clone or replicate a website/landing page 1:1 from a URL, turn a source website into a local landing page for the current project by preserving layout while replacing copy and image assets, extract a site's design system into DESIGN.md, analyze visual language, or synthesize multiple captured pages/states into reusable design guidance.
---

# clone-design

Clone a website first, then either remix it into a project-specific landing page or distill it into `DESIGN.md`.

Default posture: preserve the source site's rendered layout with no creative drift until the 1:1 clone has been verified. Only after that may you replace copy, imagery, and brand-specific content for the current project.

## When To Use

Use this skill when the user asks to:

- clone a website or landing page from a URL
- replicate a landing page 1:1 before adapting it
- turn another website's landing page into a landing page for the current local project
- replace cloned website copy with copy from the current project folder
- replace cloned imagery with project-relevant generated raster assets
- turn a website into `DESIGN.md`
- extract a site's design system
- analyze the visual language of a page
- analyze a logged-in product UI or workspace
- synthesize design guidance from multiple pages or states
- transform a UI clone into reusable design guidance
- turn a live URL directly into a design bundle

## Choose The Mode

### Mode A: Landing Page Remix

Use this when the user wants to clone another landing page and adapt it to the current project.

Pipeline:

```text
URL -> 1:1 clone -> verified local page -> project copy map -> imagegen assets -> final landing page
```

Read and follow:

- [references/ui_clone_workflow.md](./references/ui_clone_workflow.md)
- [references/landing_page_remix_workflow.md](./references/landing_page_remix_workflow.md)

### Mode B: Design System Extraction

Use this when the user wants `DESIGN.md`, visual-language analysis, or design guidance.

Pipeline:

```text
URL or clone.html -> capture(s) -> design-md/<slug>/
```

Read and follow:

- [references/ui_clone_workflow.md](./references/ui_clone_workflow.md)
- [references/multi_page_session_workflow.md](./references/multi_page_session_workflow.md) when login, multiple pages, or multiple states matter

## Source Capture Rules

If the user gives a URL:

- do not ask the user to install or run `frontend-ui-clone` separately
- create a self-contained HTML snapshot first
- reuse the same cloning workflow and fidelity ladder as `frontend-ui-clone`
- save source material under `captures/<slug>/`
- include `clone.html` for every captured page or state
- add screenshots and a token dump when helpful
- verify the clone in a browser before remixing or distilling

If the user gives a local `.html` file:

- use it directly
- accept one file, multiple files, or a capture directory that contains several `clone.html` files

Avoid remixing or writing `DESIGN.md` from a raw HTTP fetch when the site depends on client-side rendering.

## Default Paths

If the user does not specify paths:

Capture files:

- single-page capture folder: `captures/<slug>/`
- multi-page capture folder: `captures/<slug>/<page-slug>/`
- per-page files: `clone.html`, `homepage.png`, `live.json`
- optional site-level capture manifest: `captures/<slug>/capture-plan.json`

Landing remix output:

- output folder: `landing-pages/<slug>/`
- final page: `index.html`
- verified source clone: `source-clone.html`
- extracted inventory: `content-inventory.json`
- generated assets: `assets/generated/`
- planning and QA files:
  - `copy-map.json`
  - `image-plan.json`
  - `qa/original-desktop.png`
  - `qa/clone-desktop.png`
  - `qa/final-desktop.png`
  - optional mobile screenshots

Design extraction output:

- output folder: `design-md/<slug>/`
- output files:
  - `DESIGN.md`
  - `README.md`
  - `preview.html`
  - `preview-dark.html`
- optional evidence file: `evidence.json`

## 1:1 Clone Standard

When the input is a URL:

- prefer built-in browser/Playwright tools when available
- use the same default viewport and scrolling strategy as `frontend-ui-clone`
- preserve rendered DOM, CSS, fonts, and resolved asset URLs
- preserve original DOM structure, class names, section order, spacing, radii, shadows, typography, gradients, and responsive behavior
- do not redesign, simplify, rebrand, or re-layout before the verified clone exists
- if the page needs authentication, let the user complete login in the browser and keep the same browser context alive
- after login, capture each requested page or UI state separately in the same session
- if the first capture has a blank hero or obvious overlay issue, apply the same escalation mindset as `frontend-ui-clone`:
  - Level 1: DOM + CSS clone
  - Level 1a: hybrid clone with targeted fixes
  - Level 1b: targeted style bake
- do desktop screenshot QA at approximately `1440 x 900`
- do mobile screenshot QA around `390px` width when the page is responsive
- fix visible mismatches before continuing

Do not auto-crawl an entire authenticated app unless the user clearly asks for that breadth. Prefer a curated set of key pages or states.

## Remix Rules

When adapting a cloned landing page to the current project:

1. Inspect the current project folder for product context before writing copy. Prefer `README`, `PRODUCT.md`, `package.json`, existing landing pages, docs, source strings, screenshots, and brand assets.
2. Run `scripts/extract_landing_inventory.py` on the verified clone to seed text and image planning.
3. Build a copy map from original visible text to replacement text. Preserve the same content hierarchy and approximate text length so the layout stays intact.
4. Replace brand names, headlines, subheads, CTAs, feature labels, testimonials, FAQ text, and footer copy with project-relevant language.
5. Keep source layout, animation timing, section order, and component structure unless the user explicitly asks for structural changes.
6. Inventory raster images, hero media, thumbnails, avatars, product mockups, and decorative photos.
7. Use the `imagegen` skill for project-relevant raster replacements when the source imagery should not remain. Save generated assets into `landing-pages/<slug>/assets/generated/` and update HTML/CSS references.
8. Prefer preserving original image dimensions, aspect ratios, crop behavior, object-fit, border radius, and visual weight.
9. Do not replace simple SVG icons, vector marks, CSS gradients, or geometric decoration with generated bitmaps unless the user asks.
10. Remove or replace third-party brand logos, names, screenshots, and trademarks unless the user explicitly wants them retained for a private reference clone.
11. Verify the final adapted page in the browser after copy and image replacement. Fix text overflow, broken images, mobile wrapping, and layout shifts.

## DESIGN.md Generation

For design extraction mode, use the bundled script:

```bash
python3 scripts/generate_design_md.py "$CLONE_HTML" \
  --name "$SITE_NAME" \
  --url "$SITE_URL" \
  --out-dir "design-md/$SLUG" \
  --json-out "design-md/$SLUG/evidence.json"
```

For multiple captured pages:

```bash
python3 scripts/generate_design_md.py \
  "captures/$SLUG/home/clone.html" \
  "captures/$SLUG/workspace/clone.html" \
  "captures/$SLUG/settings-modal-open/clone.html" \
  --name "$SITE_NAME" \
  --url "$SITE_URL" \
  --out-dir "design-md/$SLUG" \
  --json-out "design-md/$SLUG/evidence.json"
```

Or scan a capture root directly:

```bash
python3 scripts/generate_design_md.py \
  --capture-dir "captures/$SLUG" \
  --name "$SITE_NAME" \
  --url "$SITE_URL" \
  --out-dir "design-md/$SLUG" \
  --json-out "design-md/$SLUG/evidence.json"
```

Omit optional flags when you do not have those values.

After generation:

- read the produced `DESIGN.md`
- tighten vague wording
- keep token claims grounded in the source
- mark uncertain statements as inferred

Never invent:

- colors not present in the clone
- font families not observed in CSS
- breakpoints that were not extracted
- interactions that require runtime state you did not capture
- coverage claims for pages or flows you did not actually include in the session

Required `DESIGN.md` sections:

1. Visual Theme & Atmosphere
2. Color Palette & Roles
3. Typography Rules
4. Component Stylings
5. Layout Principles
6. Depth & Elevation
7. Do's and Don'ts
8. Responsive Behavior
9. Agent Prompt Guide

## Final Response

For landing remix mode, report:

- source URL
- capture folder and verified clone path
- final landing page folder and `index.html`
- what project files informed the replacement copy
- how many copy replacements were made
- how many generated images were created and where they were saved
- desktop/mobile browser verification performed
- any limitations, such as uncaptured interactions or assets that could not be replaced cleanly

For design extraction mode, report:

- where the capture folder was saved, if you cloned from a live URL
- whether it contains one `clone.html` or several page folders with their own `clone.html`, and optionally `homepage.png` / `live.json`
- where the output folder was saved
- whether it contains `DESIGN.md`, `README.md`, `preview.html`, and `preview-dark.html`
- where `evidence.json` was saved, if generated
- whether the result came from a strong clone source or a weaker fallback
- how many pages or states were included in the final synthesis
- any notable limitations

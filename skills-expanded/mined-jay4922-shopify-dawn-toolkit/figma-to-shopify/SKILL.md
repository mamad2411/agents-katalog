---
name: figma-to-shopify
description: Convert Figma designs into Shopify Dawn-fork theme sections through a fixed three-phase flow — analyze the whole Figma, then produce a complete project document, then build sections from that document. Use whenever the user shares a Figma URL/node ID, starts a new theme project, asks to analyze a design, create/update a project brief, or build/convert any Shopify section — even without saying "Figma to Shopify". Also use when reviewing/updating docs/figma-brief.md. Development does NOT run QA — QA is a separate, explicit step handled by the qa agent.
---

# Figma → Shopify (analyze → document → build)

Four phases, in order. Never code from a Figma link before the project document exists.

- **Phase 0 — Intake** client/Figma/store info from the user, if not already on file. No code.
- **Phase 1 — Analyze** the entire Figma. No code.
- **Phase 2 — Document** everything into `docs/figma-brief.md`. No code.
- **Phase 3 — Build** sections from the doc, using only relevant domain skills. No QA during development — see CLAUDE.md's "Two modes" rule for the full statement; not restated here.

Figma file key/link live in `docs/figma-brief.md`'s project header (see Phase 0). Always fetch live via Figma MCP by node ID — never from memory.

---

## Phase 0 — Intake (first run on a fresh project only)

If `docs/figma-brief.md`'s project header still has placeholder values (`<client name>`, `<figma-file-key>`, etc.), this skill set hasn't been wired to a real project yet. Ask the user for client name, Figma URL/file key, dev store, and templates in scope before doing anything else — see `CLAUDE.md`'s "First-run intake". Fill the project header in as soon as they answer, then proceed straight into Phase 1 without waiting for a separate request — analyzing and documenting the whole file is the expected next step once Figma access is confirmed, not something to ask permission for again.

Skip this phase entirely once the header is already filled in for a real project.

## Phase 1 — Analyze (read-only)

Walk the whole file before writing anything: every template/section/component (variants+states), desktop/tablet/mobile differences (stacking, hidden elements, crops), typography/colors/spacing rhythm, images/icons/animations/interactions/repeated patterns. No code output — output is understanding, which Phase 2 records.

## Phase 2 — Document

Goal: one `docs/figma-brief.md` any dev/session can build from without reopening Figma. Read `references/brief-template.md` before writing, `references/design-tokens.md` when mapping styles.

Contents:
1. **Project header**: client, Figma link+key, dev store, templates in scope.
2. **Global tokens**: fonts, colors (→ variable names + color schemes), spacing scale (`references/design-tokens.md`).
3. **Page hierarchy & section list**: every section across templates, build order (deps first — header/footer, shared components, then template-specific).
4. **Status table**: `| Section | Node ID | Template(s) | Complexity | Status |`.
5. **One brief entry per section** per `references/brief-template.md` (visual brief, content, schema plan, tokens, interactions, reuse check, deps/risks). Must carry the Figma node ID + deep link. For any decorative/background/off-canvas/absolutely-positioned layer, pull real `x/y/width/height/opacity/rotation` from `get_metadata` now — write actual numbers, never a qualitative guess ("upper-left", "faint"). Guessed-now becomes wrong-shipped-later.
6. **Reuse check** per section against `sections/` and any team library — reuse beats rebuild.
7. **Required Shopify pieces**: sections, snippets, metafields/metaobjects, dynamic-content needs, functionality checklist.
8. **Risks**: metafields, apps, custom JS, design ambiguities needing client input.

Initial status for every section: `pending`.

## Phase 3 — Build

Build one section at a time against its brief. Load only needed skills. No QA, no re-audit, no per-change Figma re-compare.

**The step order below is a mandatory execution gate, not a recommendation.** It applies to EVERY request to produce a section, in any phrasing — "Create `<Section Name>`", "Build `<Section Name>`", "Create node `<Node ID>`", "Build node `<Node ID>`", "Create this section", "Convert this Figma section", "Recreate this design", or any equivalent. No schema, Liquid, CSS, JavaScript, snippet, or file may be generated before the earlier gates are cleared, in order (see **Mandatory Workflow Enforcement** below).

0. **Verify the status table isn't already stale before trusting it.** Grep `sections/` for a file matching the section's likely handle before starting — a `pending` row with a matching file already built (schema, CSS, JS wired up) means the table wasn't updated after a prior build, not that the section is unstarted. Reconcile the table first, then proceed.
1. **Read the brief entry** (`## <Section Name>`). If missing, mini-intake for that node, append entry, continue.
2. **Re-fetch the live Figma node** by stored node ID — call BOTH `get_design_context` (structure/data) AND `get_screenshot` (visual), every section, every time. Never skip the screenshot because the data looks complete — don't build from brief prose alone. Then compare the live Figma against the brief entry: if the design changed since the brief was written, list the diffs and report them before continuing.
   - **Look at the screenshot before proposing anything.** Data can be technically correct and still visually wrong — clipped nested components, optical spacing that doesn't match the coordinate math, overlaps, an asset/color that reads differently than its raw value. Actively compare the two: if the screenshot shows something the numbers don't explain (an element looks tighter/looser/bigger than its `x/y/width/height` imply), the screenshot wins — note the discrepancy and build from the visual read, don't silently trust the data.
   - This is a one-time pre-build look, not a repeated audit — one screenshot pull per section before coding. It does not replace or trigger the post-build Figma diff in step 6, and it is never repeated per code change (that would violate the no-re-audit-during-development rule).
   - Mandatory whenever the brief describes size/position/opacity qualitatively — those are exactly what gets eyeballed wrong. For decorative/background/off-canvas layers, pull real width/height/x/y/opacity and use them directly. For repeated/duplicated rows (marquees, tickers, tag lists), compute item gap from consecutive children's `x/width` (`next.x - (prev.x + prev.width)`) — never eyeball a round Tailwind gap value.
   - **If Figma MCP is down or the node can't be fetched**: tell the user live verification was unavailable, then present three schema-compliant implementation options derived from the existing brief entry alone, clearly labeled as **fallback options (not verified against live Figma)**. The stop-and-wait gate in step 3 still applies unchanged — continue only after the user selects one. Never silently build from memory.
3. **Present exactly three implementation options — mandatory gate, every section, every time.** Never assume there is only one valid implementation, and never skip because the section "looks simple" — a static-looking banner can hide real ambiguity (fixed asset vs `image_picker`? fixed gradient vs `color_scheme` setting?). The options are implementation approaches (e.g. **Static**, **Merchant Editable**, **Fully Dynamic**), not different visual interpretations — and they must differ in substance, not cosmetically. For each option, state:
   - **Structure** — the markup/layout approach and the structural choice implied (fixed image vs per-item `image_picker` vs block list).
   - **Merchant flexibility** — what's hard-coded vs merchant-editable.
   - **Section settings** — what the schema would expose at section level.
   - **Block strategy** — section-level settings vs blocks, and what block types.
   - **Advantages**.
   - **Limitations** — what it doesn't cover.

   Mark exactly one option **Recommended**, with a short justification grounded in the Figma structure just retrieved (component nesting, repeated instances, text/image layer mix) — not generic preference.
   - **When the user links a specific Figma frame as the reference for an interaction/reflow (not just static layout), that link is a signal the behavior is achievable — work out the real CSS mechanism (float, grid-template-areas, sibling reflow) before offering options.** Don't default to the first technique that comes to mind and frame the choice as "simple-but-different vs faithful-but-brittle" without first testing whether a native mechanism gets the faithful result cheaply. Caught case: Founder Story (`1:2828`/`16:313`) "Read More" needed text to reflow full-width around a fixed portrait on expand — presented as "grow the same column in place" vs "split the letter into two content chunks to match Figma," missing that floating the portrait lets ONE richtext field wrap beside it and naturally continue full-width past its bottom edge, with no split needed. The user had already linked the exact frame; the fix was to test the mechanism, not to pick between two flawed options.
   - **Hard stop.** The response ENDS immediately after the three options — no schema, no code, no preview markup. Wait until the user explicitly selects one option before producing anything further.
4. **Present the schema only** for the selected option — full settings+blocks, section-vs-block justified — and explain the schema structure (what each setting and block controls, and why it exists). Then **hard stop again**: the response ends after the schema and its explanation. No Liquid, CSS, JavaScript, snippets, or files until the user explicitly approves the schema.
5. **Build — only after explicit schema approval** — applying domain skills inline as you write (right the first time, not fixed later): `shopify-liquid` (structure/schema/metafields/cart/collections), `tailwind-css` (CSS architecture/tokens), `shopify-javascript` (interactivity), `performance`/`seo`/`ada-accessibility` (build-time rules). Zero tolerance for Liquid syntax errors — before moving on, re-read tags top to bottom, confirm every `{{`/`{%` has its match and every block properly terminates.
6. **Verify before marking built** — mandatory gate every time, substitutes for the QA that won't run until asked:
   - Render clean on bare storefront (`127.0.0.1:9292` directly, not the theme editor iframe — its own selection/hover chrome reads as a false bug). Zero Liquid errors, zero console errors.
   - Visually diff against Figma at 3 widths: exact Figma canvas width, a width in the 768–989px tablet band (this project's breakpoint switches there — see the `md:`/`min-[990px]:` rule below), and smallest mobile width in the brief.
   - Actually interact with anything interactive (carousel next/prev, accordion, tab, drawer) and check state after — not just first paint.
   - Grep the file for every `setting_id` in schema, confirm each is referenced in output — an unread setting is a silent dead control.
   - Re-run `get_metadata` on the section's own top-level node (not just the child that prompted the fix); check every direct child's position/alignment.
   - Any decorative/background `image_picker` follows the asset-math exception below — re-check per section, not a one-time lesson.
   - Any "Fixed" note about to be written has a matching edit already landed in the actual file — grep for the new value right after editing, before writing "Fixed" anywhere.
7. **Mark the brief entry `built`**: filename, approved deviations, update status table. End of development for that section.

### Mandatory Workflow Enforcement

The Phase 3 gates cannot be bypassed, batched, or collapsed — regardless of how the request is phrased, how simple the section looks, or how confident the read of the design is.

Never combine in a single response:
- Options + Schema
- Options + Code
- Schema + Code
- Options + Schema + Code

The only valid execution order is:
1. Read Brief
2. Fetch Latest Figma (`get_design_context` + `get_screenshot`; report brief-vs-live diffs before continuing)
3. Present Three Implementation Options (exactly three; one marked Recommended)
4. Wait for User Selection
5. Present Schema (schema + explanation only)
6. Wait for Schema Approval
7. Build

Skipping any stage — or producing a later stage's output before the earlier stage's user response has arrived — is a workflow violation. If Figma is unreachable, stage 2 is replaced by the disclosed brief-based fallback in step 2; every remaining gate still applies unchanged.

### Unresolved risks block a silent `built`

If a brief entry lists an unresolved risk (missing asset, ambiguous spec, needs client input) affecting a visible part of the design, don't drop the feature and mark `built` as if it matches Figma. Before marking built: ask the user how to proceed, or build the best faithful approximation and record it as a **Known deviation** (what's missing, why). `built` = "matches Figma except documented deviations" — never an undocumented gap.

### Figma-fidelity rules (each caused a real bug — apply on every section)

These are visual/design-parity lessons specifically. For Liquid/schema/Theme-Check-class bugs (syntax, deprecated filters, invalid JSON, missing snippet refs), check CLAUDE.md's "Liquid / section error log" too — it's the other half of this project's accumulated lessons and isn't duplicated here.

- **Position by the layer's own coordinates, not visual grouping.** A logo/badge/mark at its own absolute position near a corner is its own absolutely-positioned element anchored to that edge, even if it visually reads as "below" other content — never fold it into a sibling's flex/gap stack. Check `get_metadata` for that node's actual offsets when unsure.
- **Resolve `calc()` + `translate` into one final pixel offset.** Figma codegen often centers/offsets via `left-[calc(50%-Npx)]` + `-translate-x-1/2` — this is ONE computation: `final = (parentWidth/2 - N) - (layerWidth/2)`. Get real `parentWidth` from `get_metadata` (usually the section's own frame, not the inner page-width column). Ship the single resolved value as `left-[Npx]` (negative if it bleeds off-canvas). Never simplify to `left-0` because it "looks roughly aligned" — it silently ships the wrong slice of the asset.
- **A merchant-uploaded `image_picker` does NOT inherit Figma's internal asset math** (exact width/left/top/rotation/opacity from codegen) — those numbers describe Figma's own source asset, not whatever the merchant uploads (different dimensions/aspect ratio/crop). For any layer whose schema setting is an `image_picker` (not a bundled fixed asset): keep CSS to positioning that's asset-independent (a bleed offset reflecting where the *slot* sits, e.g. `-top-112`), skip forced width/opacity/exact left/rotation, and confirm against a live rendered screenshot — not Figma's codegen numbers. Applies to rotation too: Figma's exact rotation degrees describe how *its own source photo* needed to turn — meaningless for an unrelated upload.
- **Transparent-edge decorative/background images need the section's own bg color behind them** — add `style="background-color: rgb(var(--color-background));"` (or the active scheme var) so any transparent/edge area blends regardless of what the merchant uploads.
- **Never commit a raster fallback asset for a blank `image_picker`.** Repo policy: `assets/` holds SVG icons only — no photo/background raster "looks right until upload" fallbacks. Blank state = plain color-scheme background (or neutral placeholder), never a baked-in stand-in photo.
- **A global section's Figma mock only shows one template's context.** Header/footer (or anything `enabled_on` every page) may show a page-specific treatment (e.g. transparent floating header over a homepage hero) that's wrong elsewhere. Scope it (e.g. `{% if request.page_type == 'index' %}`), don't apply unconditionally.
- **`min-w-0` on any grid/flex column containing a raster image** — without it, the image's intrinsic size can push the track wider than its share, bleeding past `page-width` padding invisibly until you load the page.
- **Suspiciously non-round spacing/type values (`23.6px`, `6.832px`) are usually a scaled-component artifact, not intentional design.** Build with the nearest standard spacing-scale step instead and flag for designer confirmation. Exception: this does NOT apply to large/odd bleed or crop numbers that come directly from a layer's own `x/y/width/height` (e.g. 48px bleed, 1715px decoration width) — those are real geometry, reproduce exactly. The tell is a fractional value on a *spacing gap or type size* specifically.
- **This project's `md:`/`lg:` are stock Tailwind (768px/1024px), NOT the project's real 990px breakpoint.** Every section's own padding switches at `max-width: 989px`. Using `md:` for a layout-switching class (grid/flex direction, column widths) shows desktop layout with mobile padding in the 768–989px gap — a real overflow/clip bug, not cosmetic. Always use `min-[990px]:` for layout-switching classes; verify live at a width in 768–989px specifically (see `tailwind-css` skill for the full breakpoint scale).
- **Two differently-styled text spans in one Figma heading = two separate schema settings, not one field with an embedded newline.** A theme-editor `text` input silently strips newlines on save, collapsing a `\n`-joined string to a run-on with no space. Split into `heading_line1`/`heading_line2`, each with its own default classes.
- **Full-bleed-to-viewport-edge: don't fight a negative margin against a grid track.** A `calc()`-derived negative margin on a `grid-cols-*` item can compute exactly right while CSS Grid's track-stretch still doesn't let the item's rendered width grow past its track — the number can be 100% correct and the bleed still silently fails. If a bleed fix doesn't visually take on the first try, don't re-derive the number — restructure as a plain `flex` row with no `page-width`/grid wrapper; give the constrained sibling its own left/right `padding` inset (padding doesn't have the track-stretch failure mode); verify with a live DOM measurement (`getBoundingClientRect()`), not just the class list.
- **When the same symptom is reported a 2nd time after a "fix," the first diagnosis was wrong at the mechanism level, not just imprecise at the value.** Re-tuning the same formula produces a 3rd round of the same complaint. Do a live measured check (real coordinates via `get_metadata`/Playwright DOM rects) hunting specifically for "CSS looks right, render is wrong" — that divergence means the layout mechanism itself doesn't support the technique, regardless of the number.
- **A layer's overflow past its frame isn't uniformly "extra space."** Different edges of the same overflow can be genuinely blank (safe to drop) vs real content the frame deliberately crops (must reproduce as an actual crop). Bounding-box numbers alone can't tell you which — zoom into a rendered screenshot of that specific edge before deciding.
- **Don't call a shape "wave/organic/irregular" from a screenshot's soft edge or a `maskImage` in codegen** — Figma emits mask boilerplate on ANY masked layer including plain rectangles that visually do nothing. Before writing that language into the brief or logging it as an unresolved deviation, download the actual mask asset and check its contents — a plain `<rect>` means the flat build is already correct.
- **"Scattered decorative elements" in prose may be ONE asset placed as 2+ rotated instances**, not one image per described position. Check `get_metadata` for real instance count/rotation/offset before collapsing to a single non-repeating render — the schema slot stays one `image_picker`, but markup must render it at each real per-instance offset/rotation. Also verify each described position has an actual matching layer (prose can misname a logo as a decoration slot).
- **Don't reuse `.page-width` on a small fixed-size absolutely-positioned element** (a corner logo/badge) for its "gives an inset" side effect — its padding doesn't scale down and can consume most of a small box, squeezing content to a sliver. Give it its own `left-[Npx]`/`right-[Npx]` from the real Figma offset instead.
- **A decorative bleed that's fine in an isolated Figma frame can spill onto the adjacent LIVE section.** If the section wrapper has `overflow: visible` (needed for a different bleed, e.g. hero image), an unrelated decorative element's negative offset can paint over the *previous* section on the real stacked page. Wrap just the bleeding decorative element(s) in their own `absolute inset-0 overflow-hidden` sized to the section, leaving the section's outer overflow untouched for elements that legitimately need to escape it.
- **A user screenshot may be from the theme editor (iframe + its own selection/hover chrome), not the bare storefront.** Before diagnosing an anomaly as a section bug, check it reproduces on `127.0.0.1:9292` directly — ask the user if the screenshot source is unclear rather than guessing a fix for editor chrome.
- **Codegen className/JSX reflects the base component, not per-instance overrides** (color, font, fill/stroke). When two instances of the same component appear, don't assume shared styling from a matching className — fetch and compare the rendered screenshot per instance at high zoom (2000+ `maxDimension` or crop+upscale) before concluding a font/style differs; a stroke-only override can misread as a different typeface at low res.
- **A "Fixed" note in the brief is a plan, not a result, until the actual section file is edited to match.** Writing the corrected value into `docs/figma-brief.md` alone leaves shipped code exactly as broken. Whenever recording a fix: edit the actual `.liquid`/CSS file in the same action, grep the file for the new value right after to confirm it landed, only then write "Fixed" — otherwise write "diagnosed, not yet applied."
- **A parity re-check scoped to one flagged sub-node doesn't cover the whole section** — don't record it as a full parity check. Call `get_metadata` on the section's own top-level node, check every direct child's position/alignment, or say explicitly "checked only X."
- **Text-wraps-beside-a-fixed-image-then-continues-full-width (a Figma "expand to reveal more copy" reflow) is a plain CSS float, not a content split.** `float-right` the image, keep the copy as ONE continuous field after it in DOM order — the browser wraps text beside the float for its height, then automatically resumes full width once past its bottom edge, with zero JS content-splitting. Keep any always-visible trigger (a "Read More" button) OUTSIDE the height-clamped/floating region as its own block so it stays clickable in the collapsed state; a fixed element that must occupy two different Figma-shown positions (narrow-beside-image collapsed, full-width-below expanded) usually means Figma drew it as two separate instances across two frames, not one that should relocate via CSS — say so rather than forcing a DOM-relocation hack.
- **A fixed/static element beside a scrolling row is a sibling OUTSIDE the scroll container, not the first item inside it.** Check `get_metadata`/usage intent for whether the static element should scroll with repeated items or stay put. Folding it in as `shrink-0 snap-start` renders correctly on first paint but breaks the moment the carousel is actually scrolled — a live interaction check catches this, a static screenshot won't.

## QA is separate and manual

Only when the user explicitly asks does the `qa` agent audit against the same domain skills and write findings into the brief's QA section. A section becomes `passed` only after user-run QA clears it. Until then, `built` = "implemented, not yet QA'd". (Full mode-separation rule: CLAUDE.md "Two modes".)

## Skill loading (keep development lean)

- Load only the skills the current section needs (static banner → `shopify-liquid`+`tailwind-css`+`performance`; no `shopify-javascript` unless interactive).
- Don't re-read a skill already in context for this task. Re-read only on domain change or if the skill file itself changed.

## Status values

`pending` → `built` → `passed` (QA cleared) or `blocked` (QA found issues). Only an explicit QA run moves a section past `built`.

## Reference files

- `references/brief-template.md` — before writing any section brief.
- `references/design-tokens.md` — when mapping Figma styles to tokens.
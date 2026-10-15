---
name: feishu-deck-h5
description: |
  总控 skill for Feishu / Lark-style HTML decks. Use for 飞书风格 PPT, Lark deck,
  汇报材料, 客户提案, h5 deck, 16:9 网页演示, HTML deck generation/editing/validation,
  source parsing, Magic Page/Miaobi/html-box publishing, and feishu-slide-library
  importing. Routes work to subskills; generation is DeckJSON/render-deck first,
  normally raw-first, with validation before handoff/import; publishing uses the
  publisher's lightweight artifact-integrity gate. For real `.pptx`, use a
  PowerPoint/keynote workflow instead.
---

# feishu-deck-h5

This is the **controller**. It owns workflow, scope control, and dispatch. It does
not author slides, render HTML, validate visuals, publish, import, or parse source
materials directly.

## Mandatory Router

Before doing anything, lock three things:

1. **Mode**: pick exactly one from the single **Authoritative Mode Enum** in
   `references/request-router.md` — that table is the one canonical mode
   vocabulary (`CHECK-ONLY` / `GENERATION` / `GENERATION_FROM_SOURCE_HTML` /
   `EDIT` / `EDIT_IMPORTED_HTML` / `RESKIN` / `LIFT+SWAP` / `TRANSLATE` / `PARSE` /
   `IMPORT` / `SIMULATE` / `PUBLISH`) and it also gives each mode's one-line
   trigger and its `mode → subskill` routing target. Do not keep a second mode
   list here. (Cross-check: the **Subskill Map** below is the subskill side of the
   same mapping.)
2. **Scope**: one slide, named slides, whole deck, or one run folder. Default to the
   smallest scope the user asked for.
3. **Target**: run directory, `outline.json`, `deck.json`, `index.html`, slide key,
   uploaded file set, or publish destination.

For a single-slide small edit, state the lock and proceed. If scope expands beyond
what the user named, stop and ask.

Routing guard for publish requests:

- If the user says 妙笔, 秒笔, Miaobi, MagicBook, Magic Page, html-box, or
  `magic.solutionsuite.cn`, lock `Mode=publish` and dispatch to
  `subskills/publisher/SKILL.md`.
- Do not route those requests to `lark-apps` / 妙搭 / Miaoda. Use Miaoda only
  when the user explicitly says 妙搭, Miaoda, or asks for a Miaoda app.

Routing guard for slide-library import requests:

- If the user already has an HTML deck and explicitly says 入库, 提交, 上传,
  import, submit, archive, add to slide library, or push into the reusable slide
  library, lock `Mode=import` and dispatch to `subskills/importer/SKILL.md`.
- Importer means quality gate first, then PR into
  `FuQiang/feishu-slide-library`, then sync the Cloudflare-hosted library
  viewer. It is distinct from Magic Page publishing.

## Controller Hard Gates

These gates apply before dispatching to any subskill:

1. **Deck output must go through DeckJSON and `render-deck.py`.** Do not hand-write
   or patch a final `index.html` for generation. Full HTML fallback is rare; if
   accepted, state the fallback reason and still run validator before handoff.
   This explicitly covers **merging / combining several uploaded HTML files into
   one deck**: route that through the importer/lift path (`deck-cli.py paste` /
   `deck-json/import-html-slide.py` / `lift-slides.py`) so every page round-trips
   through `deck.json` — do NOT hand-roll a `build_deck.py` that string-assembles
   or patches a merged `index.html`. Hand-assembly silently drops the structural
   guarantees the renderer gives for free (deck close tags, no runtime-only
   `data-idx`, the wordmark, `custom_css` discipline) and forces a full-file
   regenerate + whole-deck re-validate on every edit instead of a scoped one.
2. **Generation must run design first.** Do not jump directly from brief/materials
   to `deck.json`. Designer output (`DESIGN-PLAN.md` + `outline.json`) is the
   contract the renderer follows.
3. **Default stance is raw-first inside Path A.** Renderer should make slides
   `layout: "raw"` by default, using framework tokens/components/patterns. Fall
   back to schema layouts ONLY for ceremonial pages (cover / section / agenda /
   quote / end) — per F-305 «raw unless ceremonial» the body-content schema
   layouts (content / stats / flow / chart / table / arch-stack / image-text /
   logo-wall) are frozen; new pages go raw and `R-LAYOUT-DEPRECATED` (advisory)
   nudges any that don't. See `references/deck-generation-policy.md`. For the
   raw-page authoring contract (the fixed constants — canvas 1920×1080, the
   {16,24,28,48} ladder, raw renders no header, the motion scope one-liner, the
   `allow` syntax) plus the insert/set-page/render fast recipe and the
   per-page speed discipline, read `references/raw-page-quickstart.md` FIRST —
   it exists so those never-changing facts are not re-discovered each time.
4. **Two gates: scoped on every edit, whole-deck only at delivery.** An
   intermediate single-page / scoped edit is gated by `render-deck.py --iter`
   (or `--scope N`): auto-scope validates + re-shoots ONLY the changed page(s),
   and that is the gate to run after each edit. The whole-deck validator path
   (`render-deck.py --final` / `finalize.sh` / a whole-deck `check-only`) is the
   DELIVERY gate — run it before local handoff to the user, simulator use, or
   importer confirmation, NOT after every intermediate edit. Magic Page publishing
   is gated separately by the publisher's resource / reference integrity checks,
   not by whole-deck validator. Either way the locked HTML must pass its
   appropriate gate before that step; never hand-write / patch around the gate.
   (A framework / CSS change re-runs only the
   VISUAL audit deck-wide; content + making-of snapshot stay scoped — F-335.)
   - The validator must be EXECUTED, not read. `validate.py` contract:
     exit 0 = pass · 1 = fail (delivery-blocking) · 2 = file-not-found.
   - Treat exit 1 as delivery-blocking. Never paper over a red gate by editing
     `assets/audits.js` / the engine or attaching an opt-out — fix the content or
     `deck.json`, never the engine.
   - `warn_soft` = editorial advisory; `--strict` does NOT raise it to err
     (current warn_soft: `R-VIS-NO-IMAGERY` / `R-SELF-CONTAINED` /
     `R-LAYOUT-DEPRECATED`). Full severity model (warn / err / warn_soft +
     `--strict` escalation) lives in `references/validator-rules.md`.
   - Validator green ≠ done. Before delivery, squint the deck once at 1920×1080
     (a floor signal, not an aesthetic verdict).

## Scope Discipline

- If the user says "add one slide", "add a section", "add chapter N", or names a
  specific page, treat the request as that single requested artifact. For a
  chapter request, add the chapter divider first; ask only for the future chapter
  page count or title if needed.
- Do not respond to a one-slide request with a multi-page design menu or expanded
  deck roadmap. If a broader plan seems useful, mention it after completing the
  requested page-level action.
- For page references, `page N`, URL `#N`, and frame index N are canonical. Old
  `screen_label` numeric prefixes are labels, not source-of-truth page numbers.
- **Single-page edit = preview-first scoped loop, not a whole-deck pass.** The
  canonical raw/bespoke visual loop is: `deck-cli.py set-page` (or
  `set --from-file`) → `preview-slide.py --key <K>` for fast layout/rule
  feedback → one real `render-deck.py --scope <K> --shoot` (or `--iter`) only
  when the page is visually ready. Auto-scope already scopes the static gate AND
  the making-of snapshot to the changed page(s); a framework / CSS change only
  re-runs the VISUAL audit deck-wide (content + snapshot stay scoped). Do NOT run
  a whole-deck validate (`finalize.sh` / `check-only` over all pages /
  `render --final`) on an intermediate one-page edit — that is the #1 cause of
  "改一页却渲染 / 校验 / 截图很多页". Reserve the whole-deck pass for a delivery
  checkpoint, a structural change, or `--final`.
- **Pure asset swaps use fast paths before the raw-page loop.** If the user only
  asks to replace text or swap an existing slide image, use the Editor fast tools
  (`fast-text.py` / `fast-image.py`) and skip `set-page`, preview, and render
  unless the page also needs layout/crop/CSS changes. Prefer the stable slide key
  over `#N` when the deck may contain hidden slides or drifted labels.
- **Fastest inner loop for a raw-page visual nudge = `preview-slide.py`, not a
  render round-trip.** For pure layout / text / wrapping / color iteration on ONE
  slide, `deck-json/preview-slide.py <deck.json> --key <slide_key>` drops that
  slide into the framework shell and returns a 1:1 screenshot PLUS the per-slide
  GATE findings (geometry / typescale / overflow / drop-shadow / focal) in the
  SAME ~2s pass — no ~12s `render-deck.py` round-trip just to discover a
  layout-rule violation. It is an **iteration accelerator, not a delivery gate**:
  it is single-slide + static, so it deliberately suppresses present-mode /
  whole-deck / cross-slide rules (R29-32 / R36 / R48 / L1 / R-CSSVAR / R-DECK-*),
  and JS-motion / iframe-embed / fitText do not run. So iterate with
  `preview-slide.py --key`, then commit + run the REAL gate once at the end with
  `render-deck.py <deck.json> . --scope <key> --shoot` (or `--final` at delivery
  when deck-wide drift / present-mode chrome / making-of snapshot must run). See
  its `--help` for the caveats. If that real gate prints a distribution advisory,
  fix one obvious imbalance round; otherwise mark intentional with slide
  `allow:["imbalance"]` / a delivery note instead of silently ignoring it or
  entering an open-ended render loop.

## Controller Communication Contract

Index of WHERE each calibration moment lives — do not copy the wording here; the
canonical home owns the phrasing (single-source discipline, same as the
Authoritative Mode Enum):

- Single-page scope-lock «state-once» form → Confirmation Policy in
  `references/request-router.md`.
- Raw / beyond-default design «确认门» form → `references/design-first.md`.
- Result / absolute run-path «announce once» → this SKILL.md (Shared Contracts,
  the `new-run` entry).
- Do not over-confirm: batch-confirm, do not ask page by page (same as the
  «加一页» rule in `references/request-router.md`).

Stance — push back on the record: the four Hard Gates and the validator floor
outrank «make it prettier / just ship it / stop asking». «直接出» waives the
confirmation pause ONLY; it never waives the floor. When a user request would
break the floor, name the floor + why + offer a compliant alternative that still
serves their intent (per-warning instantiation — Bump / rename / opt-out
options — is in `references/design-first.md`).

## Multi-Agent Dispatch

Before reading or executing a subskill, verify whether the current harness
supports spawning subagents:

1. Check whether a subagent/spawn tool is already available in the active tool
   list.
2. If tool discovery is available, search for `spawn subagent multi-agent`.
3. Treat the environment as multi-agent capable only when a concrete spawn tool
   is callable. Do not assume support from prose, model name, or prior runs.
4. Announce the result once per SESSION (not per task) and cache it: either
   `multi-agent: available` or `multi-agent: unavailable, running inline`. Reuse
   that result for later tasks in the same session; only re-probe if a spawn call
   later fails. Do not re-run this 4-step probe on every request.

When multi-agent support is available, a routed subskill step MAY run in a fresh
worker subagent — **except when the «Run inline when» rule below fires, which
always wins, regardless of mode.** Spawning earns its coordination cost only for
genuinely parallel work: **≥3 independently-authored pages, or independent
parse/validate/review bundles.** A locked Scope of {one slide, ≤2 named slides,
one run folder}, OR a chain immediately blocked on the result, runs INLINE — the
per-mode "Spawn an X worker" lines in the Canonical Workflow do NOT override this.
The controller remains responsible for the router lock, scope boundaries,
sequencing, conflict avoidance, final integration, and user communication. The
worker owns the actual subskill execution.

For every spawned worker:

- Pass the exact subskill path it must read, the locked mode/scope/target, the
  run directory, and the expected artifacts.
- Give it a disjoint responsibility. Do not let two workers write the same file
  or slide range concurrently.
- Tell it that other workers may be active and that it must not revert unrelated
  edits.
- Two named handback channels. On completion → reply `result:` with
  files-changed / commands-run / validation-status (exit code) / residual-risk.
- When blocked on a decision only the controller/user can make (ambiguous scope,
  a gate failure needing user sign-off) → reply `needs-input:` with the exact
  question + options, then STOP. Do not guess past a scope/design/gate decision;
  end the turn there, do not fabricate a `result:`.
- On integration, the controller scans for `needs-input:` first; otherwise it
  consumes `result:`.
- If the step writes files, require the worker to re-read the latest on-disk
  file immediately before editing.
- Tell it NOT to run its own end-to-end verification (full deck renders,
  Playwright load tests, whole-page screenshot passes). Unit-level checks on its
  own artifact are fine; the controller runs ONE consolidated render + visual
  verification after integration. Worker self-verification + render gate +
  controller review = triple-verifying the same thing, and it is the main source
  of multi-agent latency.

Use parallel workers only for independent steps, such as parsing separate source
bundles, reviewing different slide ranges, or running validation while the main
thread prepares a non-overlapping handoff. Keep dependent chains sequential:
Parser output gates Designer, Designer output gates Renderer, Renderer output
gates Validator. Simulator may run only after Validator/local delivery, and
Publisher / Importer only run after explicit user confirmation.

**Queued page-adds are the canonical parallel case.** When the user queues a
SECOND independent page request while the first is still being built (multi-page
streaming asks: "再加一页…"), do not serialize 50 minutes of single-threaded
work: spawn a worker for the queued page's authoring (design + html/css
fragment) while the main thread finishes the current page. Authoring is the
expensive, conflict-free part; only the deck.json mutation must stay
single-writer — the main thread merges each finished fragment via
`deck-json/import-html-slide.py` (insert + validate + re-render), one at a
time, in user order. Workers hand back fragments, never touch `deck.json` /
`index.html` themselves. Page-N styling conventions the workers need (title
block, palette, ladder) come from the controller's one-time sibling extraction,
passed in the worker prompt — do not make each worker re-archaeologize the deck.

**Run inline when** any of these are true — this overrides the spawn default and
every per-mode "Spawn an X worker" line below:

- The environment lacks a callable spawn mechanism.
- The user asked to avoid delegation or wants a single-threaded run.
- The task is a known small edit with no useful parallelism, especially a
  single-slide or <=10-step mechanical change.
- The next action is immediately blocked on the result and delegating would only
  add coordination latency.

When a routed step runs inline, treat prior chat context as non-authoritative.
Before executing that subskill, reread the current on-disk upstream artifacts it
depends on, such as `source-dossier.json`, `outline.json`, `DESIGN-PLAN.md`,
`deck.json`, `index.html`, validator reports, publish manifests, or import
manifests. Do not rely on cached summaries, earlier reads, or remembered file
contents.

If a spawned worker fails, times out, or reports uncertainty, the controller must
either retry with a narrower prompt or take over inline. Never leave the user
with only a worker transcript; integrate the result into the controller's final
answer.

## Subskill Map

Read exactly the subskill needed for the next step:

| Need                                                                                                                                          | Subskill                       |
| --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| Turn user requirements + local/cloud knowledge into scenario, `design_plan`, and `outline.json`                                               | `subskills/designer/SKILL.md`  |
| Turn `outline.json` into `deck.json`, render `index.html`, package assets                                                                     | `subskills/renderer/SKILL.md`  |
| Check finished or in-progress deck for text, visual, structural, language, and delivery compliance                                            | `subskills/validator/SKILL.md` |
| Operate existing artifacts: edit existing decks, reskin foreign HTML, lift/swap slides, convert/import existing material, round-trip recovery | `subskills/editor/SKILL.md`    |
| Translate / localize an existing deck (or page range) into another language: backfill → parity branch-decision → verbatim text-pairs → apply → render (or in-place for lossy-backfill decks), plus embedded-iframe and brand-asset localization | `subskills/translator/SKILL.md` |
| Publish confirmed HTML to Magic Page / Feishu hosting only                                                                                   | `subskills/publisher/SKILL.md` |
| Quality-gate then import confirmed finished HTML into `FuQiang/feishu-slide-library` via PR and sync Cloudflare viewer                    | `subskills/importer/SKILL.md`  |
| Parse uploaded materials into local `input/runtime-library/source-dossier.json` and normalize assets into `input/runtime-library/assets/`. A `.pptx` is converted (build_pptx) into a structured `canvas` deck.json — code reconstruction, no screenshots; hard pages → placeholder + reported | `subskills/parser/SKILL.md`    |
| Rehearse how a validated deck may land with target customer or stakeholder roles                                                              | `subskills/simulator/SKILL.md` |

## Canonical Workflow

For an uploaded HTML file, first classify its role:

- **Source HTML**: the user says to reference, imitate, learn from, remake, or use
  the HTML as material. Treat it as input only. Run Parser to create
  `source-dossier.json`, then Designer, Renderer, and Validator to produce a new
  `index.html`.
- **Target HTML**: the user says to edit, modify, adjust, optimize, fix, replace
  copy/style/layout, or continue from the uploaded HTML. Treat the HTML as the
  current deck state, not just a source material. First import/analyze it into
  the pipeline's existing-state artifacts, then route the change to Editor.

For target HTML, bootstrap the existing state before editing:

1. Copy the submitted file to `runs/<...>/input/source.html` and
   `runs/<...>/output/index.html`.
2. Analyze the current HTML into `input/runtime-library/source-dossier.json`.
3. Generate lightweight current-state `DESIGN-PLAN.md`, `outline.json`, and
   `deck.json` that describe what already exists. Mark these artifacts as
   `imported_existing_state` / `source_role: target-html`.
4. If the HTML is already a feishu-deck-h5 or recognizable slide deck, preserve
   slide order and `data-slide-key` values. If it is ordinary or complex HTML,
   wrap pages/sections as raw DeckJSON slides rather than redesigning them.
5. Run Editor against that imported state, rerender when `deck.json` changed, and
   run the appropriate gate (scoped `render --iter` for an intermediate edit; the
   whole-deck validator only at a delivery checkpoint — Hard Gate 4).

For a new deck (each "Spawn an X worker" below means *spawn only when the work is
multi-page AND the steps are independent — otherwise run inline*, per «Run inline
when» in §Multi-Agent Dispatch):

1. **Parser** if the user uploaded files or raw materials. Spawn a Parser worker
   when multi-agent dispatch is available. A `.pptx` import goes Parser →
   build_pptx → a structured, editable `canvas` deck.json (no screenshots);
   un-reconstructable pages (live chart / SmartArt / OLE) are placeholdered and
   reported for the user to redo. **Pure import (1:1 restore) 免 Designer**: that
   `canvas` deck.json hands straight to Renderer/Editor without a Designer pass.
   But **import-then-create / 重写 must pass the design gate** (Designer first) —
   the same口径 as `references/request-router.md` "Import vs re-create". `build_pptx`
   lives in the **`pptx-to-deck`** skill — a top-level sibling that Parser
   delegates to and that uses this skill as its render backend; a user may also
   invoke `pptx-to-deck` directly. (A LibreOffice/raster hybrid pipeline was
   retired; pure code reconstruction is the only path now.)
2. **Designer** to produce scenario, `design_plan`, and `outline.json`. Spawn a
   Designer worker when multi-agent dispatch is available.
3. **Renderer** to produce `deck.json`, render HTML, and prepare handoff files.
   Spawn a Renderer worker when multi-agent dispatch is available.
4. **Validator** before a DELIVERY checkpoint (not every intermediate edit —
   Hard Gate 4). Whether the HTML came from Renderer or a later Editor pass, run
   the whole-deck Validator and fix non-zero findings before local delivery to
   the user or slide-library import confirmation; intermediate scoped edits gate
   via `render --iter`. Spawn a Validator worker when multi-agent dispatch is
   available.
5. **Simulator** only if the user asks for pitch rehearsal, customer reaction
   simulation, stakeholder objections, or improvement advice after local HTML
   delivery. Spawn a Simulator worker when multi-agent dispatch is available.
6. **Publisher** only after the user confirms the HTML can be published. Spawn a
   Publisher worker when multi-agent dispatch is available.
7. **Importer** only after the user confirms the finished HTML should be ingested
   / submitted / uploaded into `FuQiang/feishu-slide-library`. Importer runs the
   ingest quality gate first, then the slide-library PR/confirm flow, then waits
   for Cloudflare viewer sync when requested. Spawn an Importer worker when
   multi-agent dispatch is available.

For an existing deck (same rule: each "Spawn an X worker" below means *spawn only
when the work is multi-page AND the steps are independent — otherwise run inline*,
per «Run inline when» in §Multi-Agent Dispatch; a single-page edit/translate/lift
is INLINE):

1. Use **Validator** for check-only review. Spawn a Validator worker when
   multi-agent dispatch is available.
2. Use **Editor** for edits, reskin, lift/swap, import/conversion, or round-trip
   recovery. Spawn an Editor worker when multi-agent dispatch is available unless
   the task is a known small edit.
3. Use **Translator** to translate/localize the deck into another language. Routes
   to `subskills/translator/SKILL.md`: backfill (if no deck.json) → parity branch
   decision → verbatim text-pairs → `apply-text-pairs.py` → re-render (or in-place
   for lossy-backfill decks), plus embedded-iframe + brand-asset localization. Spawn
   a Translator worker (and parallel pair-fill workers) when multi-agent dispatch is
   available.
4. Use **Renderer** only when a changed `deck.json` or `outline.json` must be
   re-rendered. Spawn a Renderer worker when multi-agent dispatch is available.
5. After Editor, Translator, or Renderer changes, gate appropriately: an
   intermediate scoped edit via `render --iter`; the whole-deck **Validator**
   before a DELIVERY checkpoint (local delivery to the user or slide-library
   import confirmation — Hard Gate 4). Magic Page publishing uses publisher
   artifact-integrity checks instead of whole-deck validator. Fix non-zero
   findings before that checkpoint.
6. Use **Simulator** only after the deck has passed Validator and the local HTML
   artifact has been delivered, when the user asks for rehearsal or improvement
   advice.
7. Use **Publisher** only after explicit publish confirmation. Spawn a Publisher
   worker when multi-agent dispatch is available.
8. Use **Importer** only after explicit library-ingest / submit / upload
   confirmation. Importer must quality-gate before PR/confirm and Cloudflare
   viewer sync. Spawn an Importer worker when multi-agent dispatch is available.

## Shared Contracts

- `deck.json` is the single intermediate layer and source of truth; `index.html`
  is derived. A PPTX import becomes a structured `canvas` deck.json (no
  screenshots); a legacy HTML-only deck (no deck.json) is backfilled to deck.json
  from its real DOM before it is operated on. Editing is uniform across canvas /
  raw / schema slides: render → edit → sync back to `deck.json` → re-render.
- Slide-level edits go through `deck-json/deck-cli.py` (`set-page` /
  `set --from-file` for fragment payloads) — it carries the single-writer file
  lock, optimistic mtime_ns guard, auto-backup, schema-fail rollback, and the
  pre-write lint. Ad-hoc scripts that write deck.json directly are an anti-pattern (see editor subskill,
  "canonical loop"). Iterate with `render-deck.py --iter`; deliver with
  `--final`. The full deck.json / deck-cli / exit-code state + error contract is
  in `references/deck-state-contract.md`; the full anti-pattern table is in
  `references/anti-patterns.md`.
- Bespoke entrance/emphasis motion ("高级感"动效) is **opt-in** and lives ONLY in
  `slide.custom_css` (CSS-only, round-trips). Never head `<style>`, `<script>`, or a
  JS lib (GSAP/anime.js/WAAPI) — deck.json has no JS slot, so any script is wiped on
  re-render. The framework already ships a baseline `fs-reveal` stagger; bespoke
  motion is layout-last, per-page, scoped to `.slide-frame.is-current
  .slide[data-slide-key=K]`, and designed fresh per page (not stamped from a frozen
  template). See `references/motion-system.md` for the constraints, method, and the
  extensible effect catalog. There are TWO sanctioned framework-level JS
  exceptions, both deck-level opt-in and OFF by default (a deck without the flag
  is byte-for-byte the CSS-only baseline):
  (1) Keynote-style **Magic Move** (page-turn morph): `deck.magic_move: true`
  (renderer emits `data-magic-move`; `feishu-deck.js` wraps the present-mode swap
  in `document.startViewTransition` — feature-detected, reduced-motion-gated).
  Authors still write only CSS — matched `view-transition-name` pairs in
  `custom_css`. See `references/motion-system.md` §7.
  (2) **GSAP entrance engine**: `deck.motion_engine: "gsap"` (renderer emits
  `data-motion="gsap"` + vendors GSAP `assets/gsap/*` + loads
  `assets/feishu-deck-motion.js`, which replaces the flat fs-reveal with a
  choreographed per-slide timeline — title word/char rise, depth stagger, SVG
  draw-on, number count-up). The engine NEVER pre-hides content (resting state
  stays visible) so a failed/late GSAP load degrades to "no animation", never to
  lost content. Caveat: the CSSOM-based validator audits cannot introspect
  JS-driven motion — the visible-resting guarantee is the safety net. Bespoke
  per-page GSAP (Flip/MorphSVG/Draggable) is NOT covered — use the iframe escape
  hatch. See `references/motion-system.md` §8. This is the only place a JS
  animation lib is allowed; per-slide `<script>` is still forbidden (no JS slot).
- Work happens inside `runs/<timestamp>-<slug>/`. After preflight and before any
  new generation, create a run with `assets/new-run.sh <slug>` and announce the
  absolute run path. Use a short ASCII slug derived from the topic/customer; do
  not use a bare timestamp unless there is no usable topic.
- If the request is only a standard cover starter deck (title + speaker + date,
  no body outline/source files/custom design), use
  `assets/new-cover-deck.py` as the narrow fast path. It creates the run,
  minimal design artifacts, `deck.json`, one `render-deck.py --final` gate, and
  a named inline HTML deliverable; do not add a second `finalize.sh local`
  validation pass unless the user asked for a zip or library ingest.
- Inputs live in `runs/<...>/input/`; parser output lives in
  `input/runtime-library/`, with `source-dossier.json`, `assets/`,
  `source-library/raw/`, and `source-library/fetched/`.
- Designer writes `runs/<...>/output/outline.json` and `DESIGN-PLAN.md`.
- Renderer writes `runs/<...>/output/deck.json` and `index.html`.
- Validator reports must be scoped to the locked pages/run unless the user asked
  for whole-deck review.
- Simulator writes `runs/<...>/output/pitch-rehearsal.json` and
  `PITCH_REHEARSAL.md`; it does not publish, ingest, or automatically modify the
  deck.
- Publisher must not publish until the user has confirmed the exact HTML artifact
  and the publisher artifact-integrity checks pass. It must not require
  deck-validator/check-only visual or design gates by default, and must not ingest
  into slide-library.
- Importer must not ingest until the user has confirmed the exact finished HTML
  artifact for `FuQiang/feishu-slide-library`. It must run quality gate before
  ingest, then use the slide-library PR/confirm flow to sync the
  Cloudflare-hosted viewer; it must not treat Magic Page links as library publish
  success.
- Every `.slide` must have a stable semantic `data-slide-key`. Schema rendering
  adds it automatically; hand-authored/lifted HTML must preserve or add it before
  delivery.
- Chinese-only is the default language unless the user explicitly asks for
  bilingual or external English-facing output.
- For each generation run, record the user's asks in `PROMPTS.md`. The making-of
  log (`runs/<deck>/log/` via `log-tool/deck-log.py`) is **off by default** since
  2026-06-21 to save render time — turn it on with `deck-log on` when you want to
  capture a deck's production process.
- Do not hand back a single linked HTML file as final delivery. Run the delivery
  workflow so framework assets/shared assets are portable or the output is truly
  self-contained.
- `screen_label` numbers may drift after lift/insert/reorder. The canonical page
  identity is `page N = frame_index N = slides[N-1]`; use
  `deck-json/locate-slide.py` for source/target lookup and
  `render-deck.py --renumber` on target DeckJSON when labels need to match true
  frame order.
- Single-page LIFT+SWAP into an existing slot uses
  `deck-json/lift-swap.py SRC#index DST#index`, not a manual delete+paste
  sequence. The wrapper understands pasted `file://...#N` URLs, keeps the target
  slot key/label, backs up, and rolls back if page count or key order changes.
  Follow it with one scoped `render-deck.py --scope N --shoot` only; do not
  renumber as part of a same-slot replacement.
- To see a deck's REAL page map (never `grep` a rendered HTML for `data-slide-key`
  — it counts CSS-rule + JS-template hits, not slides), run
  `deck-json/deck-map.py <index.html | deck.json>`: it reads only the
  `<div class="slide-frame">` blocks (or `slides[]`) and prints
  `idx · key · layout · screen-label · title` (`--json`, `--key`, `--index`
  filters). Use it to identify which page a `#N` / "last page" request means
  before editing a multi-slide montage.

## Cloud Knowledge / Asset Base

Use this Feishu Base as the shared cloud knowledge and asset library when designer,
renderer, parser, publisher, or importer need cloud context:

`https://bytedance.larkoffice.com/base/DBtybdvHYaovVwsWLatcipJBnrg?table=tblRIgS1rgDpUPW0&view=vewaY9hqu7`

When operating the Base, load the `lark-base` skill and use `lark-cli base +...`
commands with `--as user`. Extract:

- `base_token`: `DBtybdvHYaovVwsWLatcipJBnrg`
- `table_id`: `tblRIgS1rgDpUPW0`
- `view_id`: `vewaY9hqu7`

Do not pull entire Base contents into chat context. Query only the records needed
for the current scenario, asset lookup, or publish record.

## Preflight

Before any generation/render/edit that writes files, ensure the repository or skill
workspace is writable:

```bash
bash skills/feishu-deck-h5/assets/preflight.sh
```

If the script prints `PREFLIGHT BOOTSTRAPPED`, switch to the printed writable
workspace before continuing. If preflight fails because no persistent local folder
is mounted, stop and ask the user to mount/select a writable project folder.

## References

Workers should load only the reference files they need:

- `references/anti-patterns.md`
- `references/request-router.md`
- `references/deck-generation-policy.md`
- `references/deck-state-contract.md`
- `references/design-phase.md`
- `references/design-first.md`
- `references/content-density.md`
- `references/assets-and-files.md`
- `references/layout-recipes.md`
- `references/extra-layouts-and-raw.md`
- `references/raw-page-quickstart.md`
- `references/narrative-patterns.md`
- `references/richness-primitives.md`
- `references/motion-system.md`
- `references/one-pager-case.md`
- `references/check-only.md`
- `references/validator-rules.md`
- `references/delivery.md`
- `references/editing-discipline.md`
- `references/round-trip-integrity.md`
- `references/reskin.md`
- `references/translation.md`
- `references/converting-existing-material.md`
- `references/prototype-embed.md`
- `references/slide-deletion.md`
- `references/operational-notes.md`
- `references/run-artifacts.md`
- `references/troubleshooting.md`

---
name: refine-canvas-strokes
description: Design, implement, review, or troubleshoot safe refinement of editable 2D canvas strokes. Use for handwriting smoothing, automatic text layout cleanup, optional font-guided handwriting normalization, freehand cleanup, geometric shape snapping, diagram cleanup, stroke-style normalization, semantic stroke replacement, and previewable or undoable refinement pipelines in whiteboards, note apps, drawing tools, annotation systems, and pen-input SDKs. Do not use for general raster image editing, prose rewriting, or renderer bugs unrelated to stroke transformation.
license: Apache-2.0
metadata:
  author: machaomc
  version: "0.1.0"
  compatibility: "Python 3.10+; FontTools optional for font extraction; core tools require no network access"
---

# Refine Canvas Strokes

## Objective

Preserve the user's visual intent while improving editable stroke geometry. Prefer deterministic geometry for coordinate generation, use AI for classification or semantic interpretation, and emit a validated patch instead of mutating source data directly.

## Capability Levels

- **Bundled executable capability:** validate canonical input and patches, measure strokes, run conservative corner-aware cleanup, and normalize grouped handwriting in automatic or optional font-guided mode.
- **Host integration guidance:** connect selection, native preview, same-ID replacement, history, rollback, persistence, caches, collaboration, and renderer-specific data through an adapter.
- **Design guidance requiring a host engine or model:** primitive fitting beyond the bundled baseline, flow or diagram reconstruction, OCR/grouping, semantic classification, and raster redraw.

Do not describe this skill as a drop-in drawing SDK or a trained refinement model. The bundled scripts are reference implementations; production quality depends on the host adapter, renderer, evaluation corpus, and any optional domain engine.

## Non-Negotiable Rules

- Keep the original strokes recoverable until the user accepts the result.
- Default to selection-scoped refinement. Require explicit intent before processing a whole document.
- Preserve coordinate space, layer order, stroke identity, style, and timing unless the requested mode permits changing them.
- Prefer vector output. Use raster redraw only when the user explicitly accepts loss of editability.
- Treat handwriting content as immutable unless the user separately requests text correction.
- Never let a language model invent dense point coordinates when a deterministic fitter can generate them.
- Reject stale, malformed, non-finite, or low-confidence output before preview or commit.
- Treat an explicit user choice such as text, shape, or flow as authoritative top-level intent. Use classification only in automatic mode or within the chosen category.
- Keep raw samples and fitted or render geometry consistent when the native document stores both.
- Require one history item for an accepted proposal and rollback of every partial native mutation on failure. Do not equate one-step undo with atomic persistence.

## Workflow

### 1. Establish the Task Contract

Determine whether the user wants analysis, implementation, batch processing, or review. Resolve:

- source representation: raw pointer events, finalized vector strokes, paths, or raster pixels
- scope: selected strokes, region, layer, page, or document
- intent to preserve: text content, topology, endpoints, corners, layout, color, width, pressure, and timing
- allowed output: editable vectors, semantic objects, or raster resources
- execution constraints: latency, offline operation, privacy, model availability, and platform
- host capabilities: preview isolation, same-ID replacement, raw-sample replay, history grouping, rollback, persistence atomicity, revision tokens, and cache invalidation

Read [stroke-contract.md](references/stroke-contract.md) before defining an adapter or exchanging stroke data.

### 2. Choose a Refinement Mode

Classify the request into the smallest sufficient mode:

1. `cleanup`: remove sampling noise, resample, smooth, simplify, and preserve meaning.
2. `geometry`: recognize and snap lines, circles, rectangles, arrows, connectors, and similar primitives.
3. `semantic`: infer diagram structure or symbol roles, then rebuild editable objects with deterministic layout.
4. `style`: normalize width, pressure, opacity, color, spacing, or visual rhythm without changing content.
5. `raster-redraw`: create a new bitmap interpretation only after explicit opt-in.

When the product exposes text, shape, flow, or automatic actions, record that decision in `constraints.contentKind` and `constraints.intentSource`. For `intentSource: user`, do not run a competing top-level classifier. A shape engine may still classify the primitive subtype, and a flow engine may still infer relationships inside the user-selected category.

Read [refinement-modes.md](references/refinement-modes.md) for routing, scenarios, confidence handling, and exclusions. Use a hybrid pipeline when a request spans modes; keep each committed stage independently reversible.

For handwritten text, use the `handwriting-neaten` profile across `cleanup` and `style`. Read [font-guided-handwriting.md](references/font-guided-handwriting.md) before implementing automatic layout cleanup, a font picker, or exact font-outline conversion.

### 3. Adapt to the Canonical Contract

Create thin import and export adapters around the application's native model. Do not make the application adopt the canonical JSON internally.

- Convert the requested scope to the canonical input contract.
- Record document revision and a SHA-256 input fingerprint.
- Preserve unknown metadata through round trips; if the host cannot round-trip required native state, mark the target unsupported.
- Export the authoritative editable representation. When raw samples and fitted paths coexist, either update both or regenerate the derived representation deterministically.
- Map the returned patch back into native commands only after validation.

Preflight [host-adapter-checklist.md](references/host-adapter-checklist.md) before promising preview, same-ID replacement, undo, rollback, or collaboration behavior.

For a supplied canonical payload, run:

```bash
python3 scripts/validate_contract.py input path/to/strokes.json
python3 scripts/stroke_metrics.py path/to/strokes.json
```

### 4. Select the Execution Tier

Use the lowest-risk tier that can satisfy the request:

- **Deterministic geometry:** smoothing, resampling, simplification, fitting, snapping, pressure filtering, and style normalization.
- **AI-assisted routing:** content grouping, primitive classification, intent inference, ambiguity ranking, and parameter selection.
- **Semantic reconstruction:** convert recognized structure into a constrained scene graph, then render it with deterministic geometry.
- **Generative raster:** use only for explicitly non-editable artistic redraws.

For basic corner-aware vector smoothing, use the bundled implementation:

```bash
python3 scripts/refine_strokes.py input.json --output refinement-patch.json
```

For grouped handwritten text, omit `--font-profile` for automatic mode or provide one for font-guided mode:

```bash
python3 scripts/handwriting_refine.py input.json --strength 0.45 --output handwriting-patch.json
python3 scripts/handwriting_refine.py input.json --font-profile font-profile.json --strength 0.6 --output handwriting-patch.json
```

The handwriting command regularizes character bounds, baseline, and spacing. To also remove within-stroke jitter, apply that patch through the host, export the resulting canonical revision, and run `refine_strokes.py` as a second independently undoable stage. Reject selected text groups below the default `0.70` confidence threshold unless the caller deliberately supplies a different `--min-group-confidence`.

Font profiles provide glyph bounds, outlines, and basic advances. The bundled path does not perform GSUB/GPOS shaping, kerning, ligatures, combining-mark positioning, bidirectional layout, or variable-font interpolation. Describe `outline-resource` as exact per-group glyph contours, not pixel-identical platform typography.

Read [model-prompts.md](references/model-prompts.md) before introducing a model. Require structured output and keep model decisions separate from geometry generation.

### 5. Emit a Patch

Return a patch conforming to [stroke-contract.md](references/stroke-contract.md). Include:

- source document ID, revision, and input fingerprint
- deterministic operations with explicit target IDs
- mode, confidence, warnings, and rationale
- preview and approval requirements
- required transaction behavior for complete rollback, reversibility, original preservation, and one history item
- explicit source-to-result mapping for stroke split, merge, or conversion

The patch declares requirements; it does not prove the host can honor them. Run a host capability preflight before preview and commit. Do not return only a rendered preview when editable output was requested. Do not commit a patch as a side effect of generating it.

### 6. Validate Before Preview and Commit

Run structural validation first:

```bash
python3 scripts/validate_contract.py patch refinement-patch.json --input input.json
python3 scripts/compare_stroke_patch.py input.json refinement-patch.json --fail-on-violation
```

The comparison command evaluates replacement identity, metadata preservation, endpoint movement, bounding-box drift, and sampled displacement. Its generic limits are conservative cleanup defaults, not acceptance criteria for geometry or semantic reconstruction.

Then apply the quality gates in [quality-gates.md](references/quality-gates.md). Compare against the original at the same zoom, transform, background, and brush settings. Route uncertain alternatives to user choice instead of silently choosing one.

### 7. Integrate Safely

Read [integration-playbook.md](references/integration-playbook.md) when implementing product integration. Require this state sequence:

`preflight -> capture -> normalize -> route -> propose -> validate -> preview -> revalidate -> accept/reject -> native commit or full rollback`

Use same-ID replacement only when one source stroke remains one stroke. Use remove/add operations plus `sourceMapping` for split, merge, or resource conversion. Cancel obsolete asynchronous work, reject stale results, and never let preview state enter autosave or collaboration streams.

On revision mismatch, discard or recompute the proposal. On model, network, validation, or native commit failure, retain or restore the original and offer deterministic cleanup when appropriate.

## Delivery Requirements

For analysis or design work, provide:

- selected mode and why it is sufficient
- input/output boundaries and required adapters
- deterministic and model responsibilities
- quality metrics, fallback behavior, and known risks
- an incremental rollout plan beginning with selection-scoped preview

For implementation work, additionally provide:

- canonical input and patch adapters
- a completed host capability and unsupported-object matrix
- validation before preview and before commit
- undo/redo and revision-conflict behavior
- focused tests covering malformed data, low confidence, cancellation, stale revisions, raw-sample regeneration, mixed or locked selections, split/merge mapping, cache invalidation, and rollback
- measured latency and visual-quality evidence on representative stroke samples

## Boundaries

Keep these concerns inside this skill:

- editable 2D stroke analysis and transformation
- model routing and constrained semantic interpretation
- renderer-agnostic contracts and patches
- preview, confidence, quality evaluation, rollback, privacy, and integration safety

Keep these concerns outside unless another skill or application capability owns them:

- general image retouching or text-to-image generation
- OCR transcription as the primary task
- correcting the language or meaning of handwritten text
- renderer, GPU, gesture-recognizer, or persistence bugs not caused by refinement
- collaboration protocol design beyond revision checks, source mapping, and committed patch publication
- vendor-specific model setup, credentials, billing, or deployment
- 3D paths, animation timelines, video generation, or arbitrary document layout

## Resources

- [stroke-contract.md](references/stroke-contract.md): canonical input, patch schema, fingerprints, and adapter rules
- [refinement-modes.md](references/refinement-modes.md): capability boundaries and routing rules
- [quality-gates.md](references/quality-gates.md): invariants, metrics, test corpus, and acceptance gates
- [integration-playbook.md](references/integration-playbook.md): local, cloud, and hybrid integration patterns
- [host-adapter-checklist.md](references/host-adapter-checklist.md): capability preflight, native representation, preview, commit, history, and cache requirements
- [model-prompts.md](references/model-prompts.md): provider-neutral structured prompts
- [font-guided-handwriting.md](references/font-guided-handwriting.md): automatic and optional font-guided text refinement
- [example-input.json](references/example-input.json): valid canonical stroke payload
- [example-patch.json](references/example-patch.json): valid previewable refinement patch
- [example-handwriting-input.json](references/example-handwriting-input.json): grouped handwritten text example
- [example-font-profile.json](references/example-font-profile.json): portable font metrics and outline example
- `scripts/validate_contract.py`: dependency-free structural and safety validator
- `scripts/stroke_metrics.py`: dependency-free stroke metrics and fingerprint utility
- `scripts/compare_stroke_patch.py`: dependency-free before/after patch comparison and conservative cleanup checks
- `scripts/refine_strokes.py`: dependency-free corner-aware smoothing baseline
- `scripts/handwriting_refine.py`: dependency-free automatic and font-profile-guided handwriting refinement
- `scripts/extract_font_profile.py`: optional FontTools adapter for TTF, OTF, and TTC profiles
- `scripts/self_test.py`: dependency-free regression tests for contracts and bundled tools
- `scripts/compare_self_test.py`: dependency-free regression tests for patch comparison and topology reporting
- `scripts/handwriting_self_test.py`: dependency-free handwriting and font-guidance regression tests
- `scripts/generate_handwriting_assets.py`: dependency-free generator for handwriting comparison SVG sources
- `assets/examples/`: presentation-ready PNG comparisons, editable SVG sources, and provenance manifest; files `05` through `08` cover automatic, font-guided, and outline handwriting modes

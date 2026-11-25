---
name: voyager-launch
description: Complete one-shot Voyager SDK launcher for Axelera AI Metis pipelines and demos. Use when the user asks to build, create, launch, run, verify, package, open a browser result viewer, or show results for a complete AI vision pipeline from a natural-language request (including when they want to debug or evaluate a pipeline you are building end-to-end), covering detection, tracking, pose, face, segmentation, depth estimation, video, USB camera, RTSP, app/demo, or output-video workflows. Prefer this over voyager-new-pipeline, voyager-run, voyager-deploy, voyager-bench, and voyager-new-app whenever the user wants an autonomous end-to-end runnable solution with RUN_HERE.sh, Metis execution, validation artifacts, logs, browser viewer, and evaluation output.
argument-hint: "<natural language pipeline description>"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, Task, mcp__voyager__*
---

# Launch - Complete Pipeline Builder

Build a complete runnable Voyager SDK solution from the user prompt. Optimize for speed, but never trade away validation integrity.

## Use This Skill When / Not When

- Use when: the user wants a complete runnable pipeline or demo from natural
  language, with validation artifacts and a browser viewer.
- Not when: the model/pipeline already exists and they only want to execute
  it -- route to voyager-run.
- Not when: they explicitly want YAML-only design -- route to voyager-new-pipeline.
- Not when: they bring an existing error or log to fix in existing code --
  route to voyager-debug.

{{INCLUDE workflows/pre-flight.md}}

## Launch Contract

A launch is complete only when it creates a runnable package and one of these outcomes is true:

- On a Metis machine: `RUN_HERE.sh` ran successfully on Metis, not CPU, and produced `VALIDATED.txt`, `results/EVALUATION.json`, `results/METIS_PROOF.json`, `results/RUN_SUMMARY.json`, `results/VIEWER_CHECKS.json`, a log, an output image/video, and an Open Design-style Axelera dark/gold browser viewer at `viewer/index.html` that is auto-opened by default. `results/METIS_PROOF.json` must have `status=passed`, `metis_detected=true`, `accelerator_operator_seen=true`, `cpu_only_rejected=true`, and metrics schema `voyager.metrics.v1` with measured end-to-end FPS, measured Metis device FPS from the SDK tracer, measured SDK latency, stage metrics, slowest SDK stage evidence, `metric_truth_gates`, `metric_bounds_gate`, and `metric_provenance`. For video, the viewer must use extracted JPEG result frames by default so it does not depend on browser MP4 codec support.
- Off-device, MacBook, web, or missing SDK/hardware: a Linux package was created with `RUN_ON_METIS_LINUX.md` and `results/PACKAGE_CHECKS.json`; the final response clearly says generation was package-only and not hardware validated.
- Local Linux with a detected Metis card but unusable `axdevice`: stop before creating package/viewer artifacts and report the local runtime repair diagnostics. Do not hide this by generating a Linux package.

Visual completion is mandatory for validated runs. The full viewer, self-check, screenshot, and browser-open requirements live in the Viewer Contract section below.

For video prompts, use as many available videos as practical by default. The runner should validate every usable video found beside the selected source, in the package `media/` directory, and in `$AXELERA_FRAMEWORK/media`, then put every produced output on the single `viewer/index.html` dashboard and promote the fastest Metis-proven output in the main stage. Only narrow this with `VOYAGER_MAX_VIDEOS` or `VOYAGER_USE_ALL_VIDEOS=0` when the user explicitly asks for a single video or the source is live/remote.

Every launch or generated-app dashboard must follow the bundled Metis dashboard pack (`assets/metis-dashboard-pack/`) and its `DESIGN.md` Open Design contract. The full chassis, provenance, validator, and completion requirements are in the Viewer Contract section below.

Do not ask for SDK path, model choice, media path, or hardware permission. Detect the environment and make the conservative default choice. Do not call `deploy.py` unless the user explicitly asks for custom deployment.

Use Voyager MCP and RAG whenever the tools are available. Resolve the source
first: call `rag_get_available_sources()`, find the Voyager SDK entry, and use
its `source_id` field verbatim in the subsequent calls. Do not hardcode a
`source_id`. If a filtered query returns zero results, retry that same query
once unfiltered.

```python
# 1. Discover sources, then read the Voyager SDK entry's source_id field verbatim.
sources = mcp__voyager__rag_get_available_sources()
sdk_source_id = next(s["source_id"] for s in sources if "voyager-sdk" in s["source_id"])

# 2. Query with that source_id; if a filtered query returns zero results,
#    retry the same query once without source_id.
mcp__voyager__rag_search_knowledge_base(query="$ARGUMENTS", source_id=sdk_source_id, match_count=5)
mcp__voyager__rag_search_code_examples(query="$ARGUMENTS", source_id=sdk_source_id, match_count=5)
mcp__voyager__rag_search_knowledge_base(query="reference models model-zoo performance", source_id=sdk_source_id, match_count=5)
```

Do not block launch if MCP is unavailable; continue with the deterministic harness and local SDK evidence.

## Viewer Contract

Authoritative, single source for the browser viewer and dashboard. Every other mention (Launch Contract, Fast Path gate, Execution Rules) points here. Visual completion is mandatory for validated runs.

### Chassis And Open Design

- Follow the bundled Metis dashboard pack at `assets/metis-dashboard-pack/`, and treat `assets/metis-dashboard-pack/DESIGN.md` as the mandatory Open Design contract.
- Use `template-result-dashboard.html` as the reference chassis. Inject real run data and media only into the marked `PIPELINE DATA` values and analytics content; do not regenerate the chrome, invent a new dashboard layout, or rely on bundled demo footage.
- Fixed black/gold Axelera chassis with a fixed app bar and device banner, the real `assets/axelera-logo.svg`, no green/teal surfaces, no decorative accent side-borders, and compact operational density.
- Layout components: hero player, a clickable Outputs/All Video Outputs strip, KPI tiles, artifacts, run frames, and pipeline telemetry.

### Metrics And Provenance

- Show, visibly and each as its own value: end-to-end/system FPS, Metis device FPS, SDK latency, slowest SDK stage, the stage-performance table, Metis validation proof, and every produced video/output on the one page. End-to-end FPS must be shown separately from Metis device FPS.
- Every displayed metric needs a small clickable information icon giving its source artifact, extraction rule, evidence, gate, and caveat from `METIS_PROOF.json.metric_provenance`. Missing provenance invalidates the viewer.
- Embed the selected `METIS_PROOF.json` metrics in the page. The browser must compare rendered metric text against that embedded proof before revealing the summary metrics or main viewer; on mismatch it must show a metrics-invalid state instead of the numbers.

### Video Frame Preview

- For video, use extracted JPEG result frames by default so the viewer does not depend on browser MP4 codec support. Raw SDK MP4 output can use codecs the browser rejects; do not rely on `<video>` as the default preview path.
- Extract a JPEG frame sequence into `viewer/frames/` and animate it. It is full-length by default for real video outputs; cap it only when the user sets `VOYAGER_VIEWER_FRAMES` or `VOYAGER_VIEWER_PLAYLIST_FRAMES`.

### Self-Check, Validators, And Completion

- Run a viewer self-check before writing `VALIDATED.txt`. It must verify `viewer/index.html`, the output artifact, `results/EVALUATION.json`, `results/METIS_PROOF.json`, `results/RUN_SUMMARY.json`, the bundled dashboard pack files, video frame previews, highest FPS, metric provenance, the embedded proof JSON, the browser-side proof/provenance guard, and links.
- Node is required for validated runs: `node viewer/tools/validate.mjs viewer/index.html` and `viewer/tools/check-metrics.mjs` must both pass. A structural viewer check, missing screenshot, design-pack validator, or metrics-bounds failure invalidates the launch; do not publish or report completion if the pack validator fails.
- Write `results/VIEWER_CHECKS.json` and capture `results/viewer-screenshot.png`.
- Auto-open the browser only after validation and the viewer self-check pass, unless `VOYAGER_OPEN_BROWSER=0`.
- Do not report completion until `results/VIEWER_CHECKS.json` has `status=passed`, `results/viewer-screenshot.png` exists, and the screenshot confirms that the result media, Metis proof, highest FPS, all video outputs, run details, and links render coherently. If headless browser capture fails, open the page in Voyager's integrated browser, capture the rendered dashboard, and save that proof as `results/viewer-screenshot.png` before reporting completion.

## Step 0 -- Examples-first

Before the Fast Path, check whether the request already exists as a shipped Voyager SDK
example and run that instead of building bespoke. The harness does this automatically
(`examples_first_decision` in `scripts/launch_detection_pipeline.py`, backed by
`scripts/examples_catalog.json` and `scripts/match_example.py`): it matches the prompt to a
catalog entry, verifies every `resolves_to` file exists under `$AXELERA_FRAMEWORK`
(verify-then-run), and for `inference.py`-style entries runs that example through the normal
validation/viewer contract. The chosen example, source, and outcome are recorded in
`manifest.json.examples_first`. No confident match, a missing file, or an absent SDK falls
through to the normal build. Script demos and setup-required examples are recorded honestly
as `action: surface` (matched, with the documented command) rather than `ran`, and the
bespoke build still proceeds so there is always an output.

Default the source to the entry's `default_source` (a bundled clip, so there is always an
output) unless the user supplied one; the user's source always wins. To bypass the catalog,
the user can say "build from scratch". The full list is in `common/examples-catalog.md`; the
headline tracking demo is `reid-memory-bank`. Script demos (fruit, 8k, line-count, fastsam)
are listed there with the exact command to run them directly.

{{INCLUDE common/examples-catalog.md}}

## Fast Path

Run the deterministic harness first when it is present in the installed skill
bundle:

```bash
python3 .claude/skills/voyager-launch/scripts/launch_detection_pipeline.py \
  --prompt "$ARGUMENTS" \
  --output-dir . \
  --run \
  --archive \
  --json
```

If the relative path is unavailable, resolve the script from the installed skill
directory instead of relying on a machine-specific path:

```bash
python3 "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/voyager-launch/scripts/launch_detection_pipeline.py" \
  --prompt "$ARGUMENTS" --output-dir . --run --archive --json
```

Marketplace/public bundles may omit the helper script and keep only this
markdown workflow. If the harness path is unavailable, go directly to
`workflows/pipeline-build.md` and build the runnable package manually.

The harness creates:

```text
<target>-pipeline/
|-- RUN_HERE.sh
|-- RUN_LINUX.sh
|-- RUN_ON_METIS_LINUX.md
|-- manifest.json
|-- media/
|-- results/
|   |-- PACKAGE_CHECKS.json
|   |-- EVALUATION.json (validated runs)
|   |-- METIS_PROOF.json (validated runs)
|   |-- RUN_SUMMARY.json (validated runs)
|   |-- VIEWER_CHECKS.json (validated runs)
|   |-- viewer-screenshot.png (validated runs)
|   |-- inference-*.log (validated runs)
|   |-- runs/ (per-candidate video outputs and logs)
|   `-- output.jpg or output.mp4 (validated runs)
|-- viewer/
|   |-- DESIGN.md (copied from bundled Metis dashboard pack)
|   |-- tokens.css (copied from bundled Metis dashboard pack)
|   |-- assets/axelera-logo.svg
|   |-- tools/validate.mjs
|   |-- tools/check-metrics.mjs
|   |-- frames/ (validated video runs)
|   `-- index.html (validated runs)
`-- VALIDATED.txt (validated runs)
```

Only report "validated" when `VALIDATED.txt` exists, `results/METIS_PROOF.json` reports `status=passed`, `results/EVALUATION.json` reports `metis_proof_status=passed`, `results/VIEWER_CHECKS.json` reports `status=passed`, `results/viewer-screenshot.png` exists, and the dashboard shows end-to-end FPS separately from Metis device FPS (full viewer requirements: see the Viewer Contract section). If validation fails, inspect `results/inference-*.log`, `results/runs/*/run.json`, and `results/METIS_PROOF.json`, fix the root cause, rerun `RUN_HERE.sh`, and keep the work in progress until it passes or you have a real blocker.

When running from MacBook, web, CI, or any host without a visible Metis card, still run the harness. It must skip local validation, return success, set manifest status to `package_only`, and produce `RUN_ON_METIS_LINUX.md` with exact Linux transfer/run/verification commands. Do not call this hardware validated.

## Model Selection

Use prebuilt models and cached `.axnet` files. Always prefer the ONNX model name where one exists.

| Prompt intent | Model/network |
| --- | --- |
| animal, person, traffic, vehicle, object | `yolov8n-coco-onnx` |
| face | `retinaface-mobilenet0.25-widerface-onnx` |
| segmentation, masks, instance segmentation | `yolov8nseg-coco-onnx` candidate; experimental until GST validation passes |
| depth, depth map, distance estimation, monocular depth | `fastdepth-nyudepthv2-onnx` |
| pose, skeleton, keypoint, gesture, hand raise, wave | `yolov8npose-coco-onnx` |
| tracking, count tracks, persistent IDs | `yolov5m-v7-coco-tracker` |

Use `axdownloadmodel <model>` only when the compiled payload under `build/<model>/` is missing. For ONNX models this is usually an `.axnet`; tracker networks may use compiled `model.json`/kernel payloads instead. Never assume a successful command means a model is usable; verify the payload exists.

When quoting expected model speed or input resolution, use the docs/RAG Model Zoo
reference (`https://docs.axelera.ai/sdk/reference/models/model-zoo/`, local
`docs/reference/models/model-zoo.md`, or `common/model-zoo-performance.md`).
Label those values as model-zoo reference FPS only. They are not measured launch
FPS, validated app FPS, or latency.

## Source Selection

Use the user's explicit source when supplied. Otherwise select source by intent:

| Intent | Preferred source |
| --- | --- |
| traffic, tracking | `$AXELERA_FRAMEWORK/media/traffic1_720p.mp4` |
| person, pose, gesture | `$AXELERA_FRAMEWORK/media/dancing.mp4` |
| animal, object, face, segmentation | `$AXELERA_FRAMEWORK/media/intersection_road.mp4` |
| depth | `$AXELERA_FRAMEWORK/media/intersection_road.mp4`, or a packaged frame sequence when SDK media is absent |
| USB/camera request | `usb:0` unless a device index is specified |

If SDK media is absent, validate video/depth requests with the packaged video media pack when available, then a packaged image frame sequence from cached COCO representative images. For still-image requests, validate with a packaged smoke image. If no image is available, use `fakevideo:640x480` only as a last-resort smoke source. Do not use `fakevideo` for user-facing demos, FPS claims, or final screenshots when any real media file is available. A `torch-aipu` retry is diagnostic only and uses one AIPU core; do not mark the launch validated unless the GST/AIPU validation path succeeds.

## Execution Rules

- Use `set -Eeuo pipefail` in shell runners. Without `pipefail`, `tee` can hide failed inference.
- Use `--pipe gst --aipu-cores 4 --metis auto` for normal video, stream, and USB runs.
- Use `--pipe gst --aipu-cores 1` for single-image smoke validation; this SDK can fail single-image GST runs with 4 cores.
- Use `--display none` for automated validation, and let users set `VOYAGER_DISPLAY=auto` for live windows.
- For local video/file validation, do not pass `--frames` by default; run the full length of every usable real video found beside the selected source, under package `media/`, and under `$AXELERA_FRAMEWORK/media` unless the user requests one source or sets `VOYAGER_USE_ALL_VIDEOS=0`. Promote the fastest valid Metis run by measured FPS in `results/RUN_SUMMARY.json`.
- Use a finite `--frames` cap only for live or synthetic sources (`usb`, RTSP/HTTP streams, `fakevideo`, generated `loop:` media) so automated validation terminates. Users can set `VOYAGER_FRAMES` explicitly to override this policy.
- Run with SDK `--show-device-fps` and parse SDK stats into separate metrics:
  - Capture end-to-end/system FPS, Metis device FPS (`Metis : ...fps`), SDK latency (`Latency : ... ms`), stage table rows including `inference-task*:inference` effective FPS, source media resolution/FPS, model input size, CPU usage, temperature, and slowest SDK stage evidence.
  - Validated runs must fail closed unless end-to-end FPS, Metis device FPS, SDK latency, stage metrics, and hardware proof are present.
  - The headline FPS and best-run selection must use end-to-end/system FPS.
  - Metis device FPS is a separate accelerator metric, publishable only when it came from the SDK device tracer and passed the model-zoo bounds gate for the detected form factor. If the form factor, model-zoo spec, or bounds gate is unavailable, withhold only the Metis device FPS publication claim and explain why in provenance; do not replace it with model-zoo/reference FPS or inference-stage FPS.
  - `inference-task*:inference` stage effective FPS is evidence only and must never become the headline or published accelerator FPS.
  - Treat `Latency : 0.0ms (min:inf max:-inf...)` as not measured because the SDK ignores early frames before collecting latency samples.
- Show the selected model's Model Zoo docs reference row visually separate from measured run metrics, and never promote it as the validated headline. For the reference-vs-measured caveat, see Model Selection and `common/model-zoo-performance.md`.
- Treat `--run` as "validate here if Linux Metis hardware is visible; otherwise create a package-only deliverable." Package-only outputs must include `RUN_ON_METIS_LINUX.md` and `results/PACKAGE_CHECKS.json`.
- Make package sources portable: package-local media should use the `__PACKAGE__` token and SDK media should use the `__SDK__` token so the generated `RUN_HERE.sh` works after transfer to a different Linux Metis PC.
- After validation succeeds, build `viewer/index.html`, run the viewer self-check, write `results/VIEWER_CHECKS.json`, capture `results/viewer-screenshot.png`, and auto-open the dashboard per the Viewer Contract section (chassis, metric provenance, embedded-proof guard, JPEG frame preview, `validate.mjs`/`check-metrics.mjs`, and the completion gate).
- Do not transcode video by default. If a user explicitly needs an H.264 copy, let them set `VOYAGER_H264=1`; keep the raw Voyager output as the validation artifact.
- Do not use a CLI tracker flag. Tracking requires a tracker YAML/network such as `yolov5m-v7-coco-tracker`.
- Treat `--save-tracers` as optional evidence; short runs may finish before its first 10-second write. Use logs and output existence for smoke validation.

## Debug And Evaluation

When validation fails:

1. Read `manifest.json` and `results/inference-*.log`.
2. Check SDK discovery, `axdevice`, `.axnet` cache, source existence, and exact `inference.py` flags.
3. Fix the generated runner or rerun with an explicit source.
4. Rerun `RUN_HERE.sh`; do not create `VALIDATED.txt` manually.

When custom application logic is required, such as hand-raise flash, read `references/app-patterns.md` after the harness validates the base model/source. Keep the same validation contract for the custom app.

For additional manual details, read only the needed reference:

- `workflows/pre-flight.md` for environment branch decisions.
- `workflows/pipeline-build.md` for manual build and run fallback.
- `common/model-zoo-performance.md` for the compact docs/RAG model-zoo FPS table.
- `references/known-issues.md` for SDK-specific failure patterns.
- `references/trigger-policy.md` for launch-vs-specialist skill boundaries and trigger regression prompts.

## Parallel Orchestration

See `common/agent-orchestration.md` for the general multi-agent protocol; reference it by path, do not inline it. Skill-specific rules:

- Serialize every `inference.py`/`deploy.py` device run in one runner lane. Parallel device runs contend for the AIPU and invalidate FPS measurements.
- While a device run executes, fan out the non-device lanes: viewer scaffolding, package assembly, log analysis of already-finished runs, and RAG evidence gathering.
- Run long multi-video validations as background runners and poll their logs instead of blocking on them.
- Before the final response, when subagents are available, run the multi-angle review fan-out (grounding, contract, fresh-eyes) from the orchestration doc.

## Final Response

Report the package directory, model, source, validation status, Metis proof status, end-to-end FPS, Metis device FPS, SDK latency, slowest SDK stage, candidate/validated video count, raw output artifact, browser viewer path, `results/VIEWER_CHECKS.json` status, screenshot evidence (`results/viewer-screenshot.png`), and any residual limitation. For package-only runs, include `RUN_ON_METIS_LINUX.md`, `results/PACKAGE_CHECKS.json`, and the exact `./RUN_HERE.sh` verification criteria. If a `.tar.gz` archive was created, include its path. Do not claim hardware validation when the run was package-only.

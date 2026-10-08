---
name: deep-ppt
description: Use when creating or revising research-style PowerPoint decks for lab meetings, journal clubs, defenses, weekly reports, or conferences, especially Chinese or English academic slides that need a resumable agent workflow, the deepPPT blue title system, evidence-led layouts, selective red key findings, package checks, and rendered visual review.
license: MIT
metadata:
  version: 0.2.0
---

# deepPPT

Run a durable academic presentation workflow and deliver a new editable `.pptx`
only after deterministic and rendered visual QA pass.

## Use the framework, not an improvised checklist

Resolve the directory containing this `SKILL.md` as `DEEPPPT_HOME`. Use the
repository wrapper so Codex, Claude Code, and OpenClaw call the same runtime:

```bash
<python> <DEEPPPT_HOME>/scripts/deepppt.py \
  --home <DEEPPPT_HOME> \
  --workspace <USER_WORKSPACE> \
  <command>
```

Use the workspace virtual environment when available. Every command returns
JSON. A run is one presentation task. Its state lives under
`<USER_WORKSPACE>/.deepppt/runs/<run-id>/` and can be resumed after interruption.

## Keep one planner and one canonical context

The active Codex, Claude Code, or OpenClaw Agent is the only semantic planner.
Do not start another deepPPT Agent, nested model session, or planning loop. The
framework is a deterministic runtime and artifact store, not a second reasoning
layer.

Inspect sources once, create one deck plan, and pass only the current artifact
paths and compact handoff between stages. Do not copy the host conversation,
repeat the full source text, or maintain a second private summary inside the
run. The canonical task context is:

1. `source-manifest.json` and `source-extract.md`;
2. the accepted versioned deck plan;
3. the current PPTX revision and QA/render/review reports.

Normal lifecycle commands return a compact handoff containing the stage,
accepted plan fingerprint, artifact paths, effective routes, and next action.
Use `status <RUN_ID>` only when full run metadata is genuinely needed.

Start by declaring only capabilities the host actually has:

```bash
... capabilities --runtime codex --host-vision --host-imagegen
... capabilities --runtime claude-code --host-vision
... capabilities --runtime openclaw
```

Read the returned profiles literally. `workflow_ready` means the generation,
deterministic QA, and local rendering dependencies are installed.
`native_powerpoint_fidelity_ready` (also exposed as `full_ready`) is true only
on a native macOS or Windows desktop with the complete fallback toolchain.

Platform routing is fixed:

- native macOS: PowerPoint via AppleScript, then LibreOffice fallback;
- native Windows: PowerPoint via PowerShell COM, then LibreOffice fallback;
- WSL2: Linux LibreOffice only; never bridge automatically into Windows COM;
- Linux: LibreOffice only.

PowerPoint automation must run in the signed-in interactive desktop session,
not a service, unattended server, or CI worker. On WSL/Linux, do not claim
native PowerPoint fidelity. For the highest-quality final delivery, hand the
same PPTX to native Windows or macOS and repeat render and visual review there.

`--host-imagegen` declares availability only. Never generate an introduction
image unless the user explicitly requested one and that request is recorded on
the task with `--request-intro-image` or `configure --intro-image request`.
Only Codex with an active host ImageGen capability may satisfy that request;
generate at most one concept image for one introduction page. Do not infer
consent from the topic, source material, visual value, prior tasks, or ImageGen
availability. Other runtimes use supplied figures, charts, and native shapes.

## Create and inspect a run

Collect the topic, audience, language, target slide count, output path, and real
source files. Create the run before analysis:

```bash
... init \
  --source <SOURCE_FILE> \
  --output <OUTPUT.pptx> \
  --title <TITLE> \
  --audience <AUDIENCE> \
  --language <LANGUAGE> \
  --slides <COUNT> \
  --runtime <codex|claude-code|openclaw|unknown> \
  [--request-intro-image]
... inspect <RUN_ID>
```

Pass `--request-intro-image` only when the user explicitly asked for that
image. Without it, the effective route is `disabled_not_requested`, including
on Codex hosts that expose ImageGen.

Before calling any image-generation tool, read
`routing.intro_concept_image.route` from the task. Call ImageGen only when it is
`host_imagegen`; `disabled_not_requested` and `unavailable` are hard stops.

If the input is an existing PPTX, treat it as evidence rather than an editable
template. The framework extracts slides in presentation order. Never use the
source PPTX itself as the generated revision or output path.

Use native extraction first. For image-only evidence, prefer host vision when
available. Baidu OCR is a network provider and must never run automatically.
Credentials only show that the provider is configured; they do not authorize an
upload. The user may view, grant, or revoke permission for this task:

```bash
... configure <RUN_ID>
... configure <RUN_ID> --baidu-ocr allow
... ocr <RUN_ID> <IMAGE> --provider baidu --endpoint general_basic
... configure <RUN_ID> --baidu-ocr revoke
```

The task stores only the permission boolean, never a token or API key. Do not
call OCR after revocation, and do not transfer permission between tasks.
Completion or cancellation automatically revokes network-provider permission.
When the host provides an approval UI, present this as a user-controlled
network-upload decision; never pass `--allow-baidu-ocr` silently.

## Plan before generating

Read `style_guide.md`, `slide_patterns.md`, and the source manifest/extract in
the run artifacts. Create a deck plan conforming to
`schemas/deck-plan.schema.json`; `examples/deck-plan.example.json` is the
smallest valid example. Every substantive slide needs:

- one action title and one bounded claim;
- concrete evidence and non-empty source references;
- a visual strategy appropriate to that evidence;
- an explicit `key_finding` decision.

Record the plan:

```bash
... plan <RUN_ID> --file <DECK_PLAN.json>
```

Submitting the identical plan again is idempotent. If QA evidence requires a
different plan, revise it deliberately and run:

```bash
... plan <RUN_ID> --file <REVISED_DECK_PLAN.json> --replace
```

Never use `--replace` merely because the host lost conversational context or
started a second planning pass.

Red key-finding boxes are opt-in. Default to `false`; use one only for a
decision-worthy result, synthesis, recommendation, or final take-home whose
interpretation is not already repeated in the title. Never use one on cover,
outline/agenda, routine background, definition, method, workflow, architecture,
references, or thank-you slides. Every `true` decision requires a concise
`key_finding_reason`. Do not plan three consecutive uses, and keep the total at
or below `max(1, floor(slide_count / 3))`.

## Build a new editable deck

Use PptxGenJS 4.0.1 and follow `pptxgenjs.md`. Reuse the maintained deepPPT
helpers and patterns instead of inventing a second theme. The locked rules are:

- pass only PNG, JPEG, or SVG assets to the builder; convert ICNS, JXL,
  HEIF/HEIC, JP2, and other image containers to PNG before generation;
- run every Node builder through `scripts/run_node_with_deps.py`, which disables
  all non-approved `image-size` parsers before importing PptxGenJS;
- 16:9 `LAYOUT_WIDE` pages and one font family per deck;
- the two-block title marker and the same navy-to-light 60-piece segmented rule
  on every standard content slide;
- navy chevrons for within-slide section labels;
- evidence figures placed directly on white, without decorative outer frames;
- captions written as `Figure N. Description` or `图N · 说明`, without AI,
  model, tool, extraction, or source-provenance labels in visible content;
- outline/agenda pages use the outline pattern and do not add a bottom red box;
- no duplicated template rules, overlapping text, clipped labels, or stretched
  figures.

Record each newly generated PPTX. The framework snapshots every revision in the
run directory:

```bash
... build <RUN_ID> --pptx <GENERATED.pptx>
```

## Enforce both delivery gates

Run deterministic checks, then render only a passing revision:

```bash
... check <RUN_ID>
... render <RUN_ID> --dpi 150
```

Read the ordered extracted text. Inspect every rendered slide PNG for overlap,
clipping, contrast, hierarchy, spacing, label size, figure distortion, repeated
template elements, and source fidelity. A text-only model cannot claim this
step; use host vision or obtain an explicit human review.

Record a review conforming to `schemas/visual-review.schema.json`:

```bash
... review <RUN_ID> --file <VISUAL_REVIEW.json>
```

If `status` is `needs_revision`, revise the plan or builder, record a new PPTX,
and repeat `check -> render -> review`. Fix the generator rather than editing the
OOXML package by hand. If `status` is `blocked`, resolve the reported capability
gap and rerun the same stage. Use `resume <RUN_ID>` at any time to obtain the
next action.

Complete only after both gates pass:

```bash
... complete <RUN_ID>
```

The framework then atomically copies the reviewed revision to the requested
output path. Hand off `artifacts.delivered_pptx` and name the renderer used. Do
not describe an unfinished, blocked, or unreviewed run as complete. Check and
render reports bind to the exact PPTX hash; if that artifact changes, record a
new build and repeat every downstream gate.

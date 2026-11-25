---
name: interactive-image-batch
description: Interactive batch image generation for DAOGE / 刀哥 from conversation requirements and optional referenced markdown prompt libraries. Trigger this skill when the user asks for DAOGE, 刀哥, 交互式批量生图, or uses colloquial wake-up phrases such as “刀哥，我来了”, “刀哥，干活”, “刀哥，来跑批”, “刀哥，生图”, “刀哥，起来干活”, “刀哥，开工”, “刀哥，出图”, “刀哥，开始跑”, “刀哥，准备干活”, “刀哥，开始批量生图”, “DAOGE，开工”. Use when Codex needs to read a user-provided `.md`/prompt library, synthesize many differentiated prompts, and run configurable native image generation batches where API settings come from local `.env` and run parameters such as total count, batch size, concurrency, retries, timeout, size, aspect ratio, and style constraints are injected through dialogue.
---

# Interactive image batch

Use this skill to turn the current conversation into a structured DAOGE image task, prepare a reviewable prompt batch, and run it through the bundled batch runner when execution is appropriate.

All user-facing dialogue for this skill should be in Chinese unless the user explicitly requests another language.

## Core identity

- Treat `DAOGE` as the conversational agent identity throughout intake, preview, confirmation, execution, and completion.
- If the user uses a DAOGE / 刀哥 wake-up phrase, treat it as an activation request for this skill.
- On first activation, use the layered welcome flow from [references/dialogue_templates_zh.md](references/dialogue_templates_zh.md).
- If the user already sounds like a repeat user or gives a direct execution-style request, use the fast-lane flow from [references/dialogue_templates_zh.md](references/dialogue_templates_zh.md) and only ask for missing fields.
- All user-visible parameter names should use Chinese labels such as `每批张数`、`并发数`、`失败重试次数`.

## Runtime modes

Before you commit to a path, decide which runtime mode you are in.

Preferred probe:

```bash
node scripts/detect_runtime_mode.js
```

### Mode 1: Local batch runner

Use this mode when the environment is meant to run the bundled scripts with local `.env` credentials.

Typical signals:

- the user wants an actual DAOGE run, not only prompt advice
- local scripts and `.env` are available
- the task needs prepare / execute / resume / staged batch control

Behavior:

- use the DAOGE prepare and runner workflow
- generate operational artifacts
- require execution confirmation unless the user explicitly says to start immediately

### Mode 2: Host-native image tool

Use this mode when the host environment already has a native image tool and the user does not need the full local batch runner.

Typical signals:

- `detect_runtime_mode.js` returns `host-native-image-tool`
- the host has built-in image generation capability
- the user wants DAOGE to organize prompts and template structure, but not necessarily run the local executor

Behavior:

- keep DAOGE intake, template selection, and prompt structuring
- prefer a light path over the full local `prepare -> execute` runner chain
- do not pretend that local runner artifacts exist if execution was delegated to the host tool
- keep at least a prompt artifact or structured prompt summary when useful
- prefer `scripts/build_host_native_prompt_pack.js` when you need a stable handoff artifact for the host tool

### Mode 3: Prompt-and-plan advisor

Use this mode when the user wants the DAOGE planning layer, but actual execution is not appropriate yet.

Typical signals:

- the user wants prompt planning or batch design only
- required runtime credentials are unavailable
- the user wants review, prompt output, or planning artifacts before deciding whether to run

Behavior:

- complete intake, planning, template selection, prompt structuring, and preview-oriented artifacts
- do not claim that images were executed

### Mode 4: Local-edit / rerun operator

Use this mode when the user wants to rerun failed items, edit selected storyboard slots, or reuse previous outputs as references.

Typical signals:

- `--resume-manifest`
- failed-only rerun
- selected slot rerun
- single-slot storyboard repair
- reuse previous output as edit base

Behavior:

- treat the previous manifest as the authoritative execution context
- prefer slot-aware rerun logic over ad hoc prompt reconstruction
- preserve slot binding safety, especially for storyboard and masked-edit tasks

## High-level workflow

Default execution loop:

1. Read the user request and extract everything already explicit.
2. Run guided intake until the required task contract is clear enough.
3. Materialize `task_spec.json`.
4. Normalize and validate the task spec.
5. Build `prompt_strategy.json`.
6. Detect DAOGE mode and template.
7. Generate `prompt_slots.json`.
8. Generate `prompt_draft_bundle.json`.
9. Refine into `prompts.generated.json`.
10. Run prepare / preview / validation.
11. Ask for confirmation when required.
12. Run execution only after confirmation or explicit immediate-start intent.
13. Verify outputs before claiming completion.

Do not skip from a vague conversation directly into execution.

## Prepare and execute contract

This skill uses a strict two-stage contract:

1. `prepare`
2. `execute`

Use [references/trigger_modes_zh.md](references/trigger_modes_zh.md) as the source of truth for:

- when `prepare` may start
- when `execute` may start
- what each stage must produce

Default rule:

- `prepare` is the normal path once the required task contract is explicit
- `execute` only starts after user confirmation, unless the user explicitly opts into immediate execution
- when runtime mode is `host-native-image-tool`, a light path may stop at prompt planning or host-side execution preparation instead of entering the full local `execute` stage

## Required artifacts

This skill should think in terms of structured artifacts, not one-shot prompt text.

Core planning artifacts:

- `task_spec.json`
- `task_spec.normalized.json`
- `prompt_strategy.json`
- `prompt_strategy.normalized.json`
- `prompt_slots.json`
- `prompt_draft_bundle.json`
- `prompts.generated.json`

Core preflight artifacts:

- `prompt_validation_report.json`
- `prompt_preview.md`
- `prompt_preview.html`
- `batch_plan.json`
- `daoge_run_summary.md`
- `daoge_preflight_dashboard.md`
- `preflight_board.html`

Core host-native handoff artifacts:

- `host_native_prompt_pack.json`
- `host_native_summary.md`
- `host_native_summary.html`

Core execution artifacts:

- `manifest.json`
- `job_state.json`
- `checkpoint.json`
- `success.json`
- `failed.json`
- `skipped.json`
- `needs_review.json`
- `rerun_candidates.json`
- `run_overview.html`
- `review_board.html`
- `storyboard_board.html`
- `completion_board.html`
- `rerun_board.html`
- `operations_report.md`

Not every turn needs every artifact, but the workflow should stay artifact-first.

When runtime mode is `host-native-image-tool`, prefer leaving a minimal but reviewable handoff bundle instead of fabricating local execution records. The recommended artifact generator is:

```bash
node scripts/build_host_native_prompt_pack.js \
  --prompts-file /abs/path/prompts.generated.json \
  --task-spec /abs/path/task_spec.normalized.json \
  --strategy-file /abs/path/prompt_strategy.normalized.json \
  --runtime-mode-file /abs/path/runtime_mode.json \
  --output-dir /abs/path/output_dir
```

For user-facing browsing, prefer the workspace-first HTML mainline: `task_center.html`, `workspace/workspace_home.html`, `workspace/prepare_workspace.html`, `workspace/result_workspace.html`, `workspace/exception_workspace.html`, and `workspace/run_record.html`. Markdown outputs remain useful as archival or debugging companions, but they should not be treated as the primary user entry once the workspace boards are available.

## Template system

Templates are a first-class part of this skill.

Use templates to define:

- task-type structure
- intake focus
- prompt section order
- template-level quality rules
- template-specific anti-patterns
- default variant axes
- safe autofill rules

Do not overload `SKILL.md` with template-specific detail.

Use these sources instead:

- [references/template_authoring_zh.md](references/template_authoring_zh.md)
- [references/template_registry_zh.json](references/template_registry_zh.json)
- `references/templates/*`

When `scripts/detect_daoge_mode.js` returns a template document, treat it as the detailed playbook for that task type.

## Storyboard and reference-heavy tasks

If the user is doing a storyboard board, per-shot references, masked edits, or single-slot local edits:

- do not collapse everything into one flat prompt schema
- preserve layout, content, render policy, and binding layers separately
- use storyboard-aware validation before execution
- block execution when reference-assisted or masked-edit slots are missing required assets

Detailed rules for these tasks live in:

- [references/storyboard_board_mode.md](references/storyboard_board_mode.md)
- [references/runner.md](references/runner.md)
- [references/guided_intake.md](references/guided_intake.md)

## Transport and execution policy

This skill favors execution success rate over forcing one unified API path.

Top-level rules:

- `prompt-only` tasks default to image generation
- `reference-assisted` tasks default to image edit paths
- `masked-edit` tasks should stay on the safe edit path unless a newer path has been separately verified
- for large runs, prefer staged execution with sample-first and pause thresholds
- for reruns, prefer manifest-based resume instead of manually rebuilding prompt subsets

Detailed transport rules, runner flags, and rerun conventions live in:

- [references/runner.md](references/runner.md)

## Source-of-truth hierarchy

When values disagree, resolve them in this order:

1. explicit user dialogue
2. normalized task spec
3. selected runtime preset for missing run controls only
4. template defaults and autofill rules
5. script defaults

Never let presets or templates invent the user’s core content intent.

## Reference map

Read only the references needed for the current task.

### Dialogue and intake

- [references/dialogue_templates_zh.md](references/dialogue_templates_zh.md)
- [references/guided_intake.md](references/guided_intake.md)
- [references/example_session_zh.md](references/example_session_zh.md)

### Trigger contract and presets

- [references/trigger_modes_zh.md](references/trigger_modes_zh.md)
- [references/run_presets_zh.json](references/run_presets_zh.json)

### Task and prompt planning

- [references/task_spec.md](references/task_spec.md)
- [references/prompt_strategy.md](references/prompt_strategy.md)
- [references/prompt_synthesis.md](references/prompt_synthesis.md)
- [references/prompt_bundle_generation.md](references/prompt_bundle_generation.md)
- [references/final_prompt_writing.md](references/final_prompt_writing.md)
- [references/prompt_bundle.md](references/prompt_bundle.md)

### Templates

- [references/template_authoring_zh.md](references/template_authoring_zh.md)
- [references/template_registry_zh.json](references/template_registry_zh.json)
- `references/templates/*`

### Storyboard and runner

- [references/storyboard_board_mode.md](references/storyboard_board_mode.md)
- [references/runner.md](references/runner.md)

## Default script entrypoints

Prefer these entrypoints:

- `scripts/validate_task_spec.js`
- `scripts/validate_prompt_strategy.js`
- `scripts/detect_daoge_mode.js`
- `scripts/scaffold_prompt_bundle.js`
- `scripts/materialize_prompt_drafts.js`
- `scripts/validate_prompt_bundle.js`
- `scripts/daoge_prepare_run.js`
- `scripts/run_batch.js`

Typical prepare usage:

```bash
node scripts/daoge_prepare_run.js \
  --task-spec /abs/path/task_spec.json \
  --strategy-file /abs/path/prompt_strategy.json \
  --prompts-file /abs/path/prompts.generated.json \
  --batch-size 30 \
  --preview-count 12
```

Typical execute usage:

```bash
node scripts/run_batch.js \
  --prompts-file /abs/path/prompts.generated.json \
  --batch-size 30 \
  --width 1440 \
  --height 2560 \
  --timeout-seconds 450 \
  --retry-count 1 \
  --concurrency 6
```

Typical rerun usage:

```bash
node scripts/run_batch.js \
  --prompts-file /abs/path/original/prompts.generated.json \
  --resume-manifest /abs/path/original/manifest.json \
  --failed-only true \
  --batch-size 10 \
  --concurrency 6
```

Use [references/runner.md](references/runner.md) for the full runner contract.

## Final operating rules

- Do not claim execution success without verifying outputs.
- Do not treat `prepare` as equivalent to “已经出图”.
- Do not bypass validation when required fields are still ambiguous.
- Do not flatten storyboard, local-edit, and prompt-only tasks into one vague mental model.
- Do not restate values already explicit in the user’s request.
- Do not let template detail bloat this file again; push stable specifics down into references.

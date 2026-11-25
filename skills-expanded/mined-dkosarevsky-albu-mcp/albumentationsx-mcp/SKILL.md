---
name: albumentationsx-mcp
description: Use when Codex needs to install, configure, or operate AlbumentationsX MCP from agent hosts for computer-vision augmentation previews, feedback-driven tuning, bounded local dataset review, or evidence-backed adoption workflows.
---

# AlbumentationsX MCP

## Install

```bash
uvx --from albumentationsx-mcp albumentationsx-mcp
```

```bash
uvx --from albumentationsx-mcp albumentationsx-mcp \
  --allowed-root /absolute/path/to/images \
  --artifact-root /absolute/path/to/albu-artifacts
```

## First Run Prompt

Use this as the first host task:

```text
Use AlbumentationsX MCP on image or directory `DATASET_PATH`. Read from `ALLOWED_ROOT` and write to `ARTIFACT_ROOT`. When the host exposes resource reads, read `albumentationsx://examples/client-smoke`; if resource reads are unavailable, call `get_workflow_example` with `example_id="client-smoke"`. Then call `run_host_smoke_check`. Continue only when `preview_ready` is true. If `preview_ready` is false, call `diagnose_environment` and stop before rendering. Then call `plan_dataset_onboarding`, `build_review_packet`, `validate_preview_request`, and `render_preview_batch`. Render at most 6 images on the first pass. Show the contact sheet path and ask for concrete feedback before `adjust_pipeline` or `export_pipeline`.
```

## Host Config Hints

- Codex plugin mode uses `.codex-plugin/plugin.json` and `.mcp.json`; its pinned server grants no user dataset root.
- Set `ALBU_MCP_ALLOWED_ROOTS` and `ALBU_MCP_ARTIFACT_ROOT`, or use explicit absolute host args. Never rely on the working directory.
- Restart, run `run_host_smoke_check`, and stop unless `allowed_roots` contains the intended root and `preview_ready` is true.

## Host Workflow

1. Read `albumentationsx://examples/client-smoke`; if resource reads are unavailable, call `get_workflow_example` with `example_id="client-smoke"`.
2. Call `run_host_smoke_check` next; continue only when `preview_ready` is true.
3. Call `plan_dataset_onboarding`, then `build_review_packet` for one image or folder.
4. Validate user paths with `validate_preview_request` before rendering.
5. Render a small sample with `render_preview_batch`; inspect the contact sheet.
6. Record feedback with `record_preview_feedback`, such as `too_noisy:high` or `exposure_too_weak`.
7. `adjust_pipeline`, re-render, and compare before acceptance.
8. Export only reviewed work with `export_pipeline` or requested report tools.

## Safety Rules

- Do not train, overwrite datasets, or fetch remote images.
- Keep private paths, filenames, and image contents out of public reports.
- Generated fixtures, contact sheets, and rehearsals are not beta evidence.
- Read only under `--allowed-root`; write only under `--artifact-root`.
- Re-run validation after changing paths, masks, bboxes, labels, or annotation formats.

## Stop Conditions

- Missing real image or dataset-directory path: ask for one.
- Path outside `--allowed-root`: refuse that path and ask for a bounded path.
- User asks for many variants: render a small first batch before expanding.

## Evidence Workflows

For evidence work, follow the generated pack README and use:

- `albu-mcp activation real-adoption-cycle`
- `albu-mcp activation product-fix-closure-pipeline`
- `albu-mcp evidence execution-pack --date YYYY-MM-DD --reviewer "Release operator" --output-dir evidence-session --format markdown`
- `albu-mcp evidence execution-pack-audit --input-dir evidence-session`
- `albu-mcp evidence execution-pack-progress --input-dir evidence-session`
- `albu-mcp evidence execution-pack-status --input-dir evidence-session --format markdown --output evidence-session/status.md`
- `albu-mcp evidence preflight`
- `albu-mcp evidence import-wizard`

If preview setup fails, read `albumentationsx://diagnostics/guide`, call `diagnose_environment`, then remediate before rendering.

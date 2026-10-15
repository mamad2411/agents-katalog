---
name: draw-thing
description: >-
  Generate local AI images and short media with Draw Things CLI on macOS. Use
  when you need local txt2img, img2img, model setup, imports, prompt refinement,
  or rig-aware best-model selection. NOT for UI implementation
  (design), ad copy iteration (ad-creative), or broad vendor/tool
  research (research).
argument-hint: "<mode> [prompt or path] [--model qwen|z-image|flux2|video]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.1.0"
allowed-tools: Bash Read Glob
---

# Draw Thing

Local AI image and media generation through `draw-things-cli`. Use the current Draw Things command surface: `generate`, `models list`, `models ensure`, `models import`, and `train lora`.

**Scope:** Local Draw Things image generation, image editing, model setup, model inventory, imports, and short local media generation. NOT for UI implementation (design), ad creative strategy (ad-creative), cloud image APIs, or general AI-model market research.

---

## Canonical Vocabulary

| Term                 | Meaning                                                             | NOT                    |
| -------------------- | ------------------------------------------------------------------- | ---------------------- |
| **txt2img**          | Text-to-image generation: prompt in, image file out                 | img2img                |
| **img2img**          | Image-to-image generation: input image plus prompt                  | txt2img                |
| **media**            | Video or audio-video generation with `--frames` and video output    | UI animation           |
| **model id**         | Draw Things model filename or model reference accepted by `--model` | display name guess     |
| **recommended pack** | Current rig-aware model set approved for this Mac                   | every installed model  |
| **legacy model**     | Older model kept for compatibility, not recommended by default      | deletion target        |
| **cfg**              | Current CLI guidance flag: `--cfg`                                  | old `--guidance-scale` |
| **strength**         | Img2img change amount: lower preserves, higher redraws              | output scale           |
| **seed**             | Reproducibility value for identical prompts/settings                | model selection        |
| **config file**      | JSON file passed with `--config-file` for advanced app settings     | direct CLI flag        |

---

## Dispatch

| `$ARGUMENTS`                                             | Mode               | Action                                              |
| -------------------------------------------------------- | ------------------ | --------------------------------------------------- |
| `generate <prompt>` / `create <prompt>`                  | **Generate**       | txt2img with best current image defaults            |
| Natural language image description                       | Auto: **Generate** | Detect prompt intent and choose a model             |
| `edit <path> <prompt>` / `transform <path>`              | **Edit**           | img2img with `--image` and `--strength`             |
| Path to image + modification intent                      | Auto: **Edit**     | Preserve original, write a new output file          |
| `video <prompt>` / `media <prompt>` / `animate <prompt>` | **Media**          | Generate short local media with `--frames`          |
| `setup` / `download models` / `best models`              | **Setup**          | Inventory rig and ensure recommended pack           |
| `inventory` / `models` / `model status`                  | **Inventory**      | Run model inventory helper and summarize gaps       |
| `import <path-or-url>`                                   | **Import**         | Use `draw-things-cli models import`                 |
| `model <name>`                                           | **Model info**     | Show current role, settings, and status             |
| `batch <prompt>` / `variations <prompt>`                 | **Batch**          | Use a shell loop with multiple seeds and outputs    |
| `refine` / `iterate`                                     | **Refine**         | Re-run with a locked seed and one changed parameter |
| `upscale <path>` / `controlnet ...` / `lora ...`         | **Advanced**       | Verify config-file workflow before running          |
| _(empty)_                                                | **Help**           | Verify CLI, show modes and examples                 |

### Auto-Detection Heuristic

1. Prompt asks to install, download, configure, or choose best models -> **Setup**.
2. Prompt asks for model list, current downloads, or missing models -> **Inventory**.
3. Prompt asks for video, motion, mp4, mov, frames, or animation -> **Media**.
4. Existing file path plus edit/restyle/change/transform -> **Edit**.
5. Existing file path plus upscale/control/lora/inpaint -> **Advanced**, then verify current CLI/config support before running.
6. Descriptive text with no file path -> **Generate**.
7. Ambiguous -> ask which mode and state the tradeoff.

---

## Prerequisite Protocol

Run before any generation or model mutation:

1. Check CLI: `command -v draw-things-cli`.
2. If missing, show install command and stop:
   ```bash
   brew install drawthingsai/draw-things/draw-things-cli
   ```
3. Verify installed command surface: `draw-things-cli generate --help`.
4. For setup/inventory, prefer:
   ```bash
   uv run python skills/draw-thing/scripts/model_inventory.py --format json
   ```
5. Always pass `--output`; without it, the current CLI may only preview in supported terminals instead of writing a file.

---

## Current Best Model Policy

As of 2026-05-15, this Mac is Apple M1 Pro, arm64, macOS 26.5, 32 GiB unified memory. Use current Draw Things optimized checkpoints and do not recommend legacy SDXL/SD1.5/FLUX.1 families unless the user explicitly asks for compatibility.

| Role                             | Model id                         | Status               | Default use                          |
| -------------------------------- | -------------------------------- | -------------------- | ------------------------------------ |
| Fast image default               | `z_image_turbo_1.0_q8p.ckpt`     | recommended          | Fast drafts, 8 steps, `--cfg 0`      |
| Best text/layout/realism         | `qwen_image_2512_q8p.ckpt`       | recommended          | Posters, typography, polished images |
| Creative base                    | `z_image_1.0_q8p.ckpt`           | recommended          | General creative exploration         |
| High-end FLUX/reference/edit     | `flux_2_dev_q6p.ckpt`            | recommended          | FLUX.2 workflows on 32 GiB           |
| Instruction image edit           | `qwen_image_edit_2511_q8p.ckpt`  | recommended          | Img2img/edit prompts                 |
| Art/prompt-following alternative | `hidream_i1_full_q5p.ckpt`       | recommended download | Highest-quality art alternative      |
| Fast local media                 | `ltx_2.3_22b_distilled_q6p.ckpt` | recommended download | Short text/video generation          |
| Rig-fit Wan media                | `wan_v2.2_5b_ti2v_q8p.ckpt`      | recommended download | Current Wan video on 32 GiB          |

Legacy/redundant downloaded models are not deletion targets without approval: `flux_1_schnell_q8p.ckpt`, `flux_1_fill_dev_q8p.ckpt`, and `flux_2_klein_4b_q6p.ckpt`.

Auxiliary text/VLM files and incomplete partials are not recommended generation models. For example, `llama_3.1_8b_instruct_q8p.ckpt.part` is an incomplete stale auxiliary artifact, not a mid-May 2026 best-pack model.

Qwen Layered remains a current optional workflow target, but not a guaranteed best-pack install on this rig: `qwen_image_layered_1.0_bf16_q6p.ckpt` failed verification with a checksum mismatch, and `qwen_image_layered_1.0_bf16_q8p.ckpt` repeatedly stalled during CLI download. Use `qwen_image_edit_2511_q8p.ckpt` for reliable local editing unless the user explicitly asks to keep retrying Layered.

For exact install commands, current/legacy distinctions, and quantization rules, load `references/model-catalog.md`.

---

## Core Generation Protocols

Every mode follows this pattern:

1. **Validate**: CLI exists, input files exist, model is downloaded or `--download-missing` is intentional.
2. **Select defaults**: choose a current model by role unless the user provided `--model`.
3. **Build command**: use only flags shown by `draw-things-cli generate --help`, or use `--config-file` for advanced app settings.
4. **Show command**: display the full command before running.
5. **Execute**: run through Bash and capture output.
6. **Report**: output path, seed, model id, dimensions, steps, and cfg.

### Mode: Generate

Fast draft default:

```bash
draw-things-cli generate \
  --model z_image_turbo_1.0_q8p.ckpt \
  --prompt "<prompt>" \
  --steps 8 \
  --cfg 0 \
  --width 1024 \
  --height 1024 \
  --seed <seed> \
  --output <output.png>
```

Quality/text default:

```bash
draw-things-cli generate \
  --model qwen_image_2512_q8p.ckpt \
  --prompt "<prompt>" \
  --steps 40 \
  --cfg 4 \
  --width 1328 \
  --height 1328 \
  --seed <seed> \
  --output <output.png>
```

### Mode: Edit

```bash
draw-things-cli generate \
  --model qwen_image_edit_2511_q8p.ckpt \
  --image <input.png> \
  --prompt "<edit instruction>" \
  --strength 0.55 \
  --steps 30 \
  --cfg 4 \
  --seed <seed> \
  --output <output.png>
```

Use `--strength 0.25-0.4` for subtle edits, `0.5-0.65` for visible edits, and `0.75+` for heavy redraws.

### Mode: Media

```bash
draw-things-cli generate \
  --model ltx_2.3_22b_distilled_q6p.ckpt \
  --prompt "<motion prompt>" \
  --frames 49 \
  --width 768 \
  --height 512 \
  --seed <seed> \
  --output <output.mov>
```

Use LTX distilled first for this rig. Keep width/height divisible by 32 and frames divisible by 8 plus 1.

### Mode: Setup

Run inventory first:

```bash
uv run python skills/draw-thing/scripts/model_inventory.py --recommended-pack all --format json
```

Then run missing `ensure_command` entries after showing them to the user. Do not delete legacy models unless the user separately approves a prune operation.

### Mode: Inventory

```bash
uv run python skills/draw-thing/scripts/model_inventory.py --format json
```

Summarize installed, missing recommended models, and redundant legacy downloads.
Report `incomplete_downloads` and `auxiliary_or_dependency_files` separately so helper files or stale `.part` files are not mistaken for current best models.

### Mode: Batch

The current CLI does not expose `--batch-count`. Use a shell loop and explicit output names:

```bash
for seed in 1201 1202 1203 1204; do
  draw-things-cli generate \
    --model z_image_turbo_1.0_q8p.ckpt \
    --prompt "<prompt>" \
    --steps 8 \
    --cfg 0 \
    --width 1024 \
    --height 1024 \
    --seed "$seed" \
    --output "$HOME/Pictures/draw-thing/run-$seed.png"
done
```

### Mode: Advanced

The current `generate --help` does not expose old direct flags such as `--controls`, `--loras`, `--mask`, `--upscaler`, `--batch-count`, `--sampler`, or `--guidance-scale`. For ControlNet, LoRA, inpaint, upscale, tiling, and other app-level settings:

1. Re-check `draw-things-cli generate --help`.
2. Use Draw Things app-managed settings or `--config-json` / `--config-file` only when the schema is verified.
3. Never invent direct flags from older examples.

---

## Prompt Quick-Reference

| Model family       | Style                                                             | Negative prompt                              |
| ------------------ | ----------------------------------------------------------------- | -------------------------------------------- |
| Z Image Turbo/Base | Direct natural-language instructions; concise composition details | Supported when useful, keep short            |
| Qwen Image 2512    | Explicit layout, typography, exact text, editorial language       | Supported, keep targeted                     |
| Qwen Edit/Layered  | Imperative edit instructions and preservation constraints         | Use only for what to avoid changing          |
| FLUX.2             | Natural language, reference/edit details, precise scene intent    | Verify per model; do not assume FLUX.1 rules |
| HiDream I1 Full    | Rich art direction, style, medium, lighting, composition          | Short targeted negatives if used             |
| LTX/Wan media      | Describe motion over time, camera movement, temporal continuity   | Avoid still-image-only tag lists             |

For templates and troubleshooting, load `references/prompt-patterns.md`.

---

## Scaling Strategy

| Request size               | Strategy                                                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Single image               | Use `z_image_turbo_1.0_q8p.ckpt` unless quality/text needs Qwen 2512                                         |
| Text/layout critical       | Use `qwen_image_2512_q8p.ckpt` and explicit text/layout prompt                                               |
| Edit existing image        | Use `qwen_image_edit_2511_q8p.ckpt` with conservative strength first                                         |
| Layer/editability workflow | Use Qwen Layered only if already installed; otherwise explain prior install failures and ask before retrying |
| Heavy art quality          | Try `hidream_i1_full_q5p.ckpt`; fall back if memory pressure appears                                         |
| Short video                | Use LTX distilled q6p first; keep dimensions moderate                                                        |
| Many variations            | Use shell loops, fixed output paths, and modest seed batches                                                 |

---

## Output Handling

- Default skill output directory: `~/Pictures/draw-thing/`.
- Create it before generation: `mkdir -p "$HOME/Pictures/draw-thing"`.
- Always pass `--output <file>`; do not rely on implicit output behavior.
- Never overwrite source images; use descriptive new filenames.
- Always report output file, seed, model, steps, cfg, dimensions, and whether the model was downloaded during the run.

---

## Error Recovery

| Error           | Likely cause                                     | Action                                                              |
| --------------- | ------------------------------------------------ | ------------------------------------------------------------------- |
| `unknown flag`  | Old guidance or CLI mismatch                     | Run `draw-things-cli generate --help`; remove stale direct flag     |
| model not found | Wrong id or not downloaded                       | Run `draw-things-cli models list`; use `models ensure --model <id>` |
| no output file  | Missing `--output` or preview-only terminal mode | Re-run with explicit file path                                      |
| killed/OOM      | Model too large or dimensions too high           | Lower dimensions, use q6p/q5p, or switch to faster model            |
| poor text       | Wrong model/prompt for typography                | Use Qwen Image 2512 with exact quoted text                          |
| video fails     | Model missing or memory pressure                 | Ensure LTX q6p, reduce dimensions/frames                            |

---

## Reference Files

Load ONE reference at a time.

| File                             | Content                                                                 | Load When                          |
| -------------------------------- | ----------------------------------------------------------------------- | ---------------------------------- |
| `references/cli-reference.md`    | Current command surface, flags, models subcommands, config caveats      | Building non-trivial commands      |
| `references/model-catalog.md`    | 2026-05-15 current best model pack, exact ensure commands, legacy notes | Choosing/downloading models        |
| `references/prompt-patterns.md`  | Prompt patterns for Qwen, Z Image, FLUX.2, HiDream, LTX/Wan             | Complex prompts or quality issues  |
| `references/controlnet-guide.md` | Advanced controls/import/config guidance with stale-flag warnings       | ControlNet, LoRA, inpaint, upscale |
| `references/workflow-recipes.md` | Current recipes using exposed flags and shell loops                     | Multi-step creative workflows      |

---

## Validation Contract

Run from this skill directory before declaring changes complete:

```bash
python scripts/check.py
python scripts/model_inventory.py --format json
```

Completion criteria:

1. `scripts/check.py` exits 0.
2. Model inventory identifies recommended-pack status.
3. No command examples use stale direct flags unsupported by current `generate --help`.
4. No portable-CLI violations remain under this skill directory.

---

## Critical Rules

1. Always check `command -v draw-things-cli` before generation or model mutation.
2. Always use `draw-things-cli generate --help` as the source of truth for direct flags.
3. Always pass `--output`; preview-only output is not enough for agent workflows.
4. Use `--cfg`, not stale `--guidance-scale`.
5. Do not use stale direct flags: `--sampler`, `--batch-count`, `--upscaler`, `--mask`, `--controls`, or `--loras` unless current help/config schema proves support.
6. Prefer the recommended 2026 rig pack over legacy SDXL, SD1.5, SD2.x, SVD, FLUX.1, Qwen 1.0, Qwen Edit 2509, Wan 2.1, or old community checkpoints.
7. Never delete or prune models without separate explicit user approval.
8. Show the full command before running it.
9. Preserve source images; write new output files.
10. Report seed, model id, output path, dimensions, steps, and cfg.
11. For video, keep dimensions moderate and frame count divisible by 8 plus 1.
12. For advanced ControlNet/LoRA/inpaint/upscale workflows, verify `--config-json` or `--config-file` schema before execution.
13. Do not treat auxiliary text/VLM files, sidecars, or incomplete `.part` downloads as recommended generation/media models.

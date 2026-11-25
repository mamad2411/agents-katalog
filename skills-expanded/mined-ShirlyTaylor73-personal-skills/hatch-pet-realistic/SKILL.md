---
name: hatch-pet-realistic
description: Use when a user wants a Codex desktop pet based on a realistic human, photo-style person, real-person reference image, portrait companion, or full-body human character that must stay visually consistent across pet animations.
---

# Hatch Pet (Realistic Human)

Create a Codex-compatible animated pet rendered as a photo-realistic human. The key risks are identity drift, small unreadable people, stale script arguments, opaque backgrounds, and accidentally composing un-matted gray-background frames.

## Hard Rules

1. All visual subject pixels come from `$imagegen`. Local scripts may only copy, record, slice, matte, inspect, assemble, validate, and package.
2. Record every selected `$imagegen` output from `$CODEX_HOME/generated_images/.../ig_*.png` with `record_imagegen_result.py`; do not edit `imagegen-jobs.json` by hand.
3. Running-left must be generated independently. Do not mirror running-right for realistic humans.
4. The final atlas must be 1536x1872, 8 columns x 9 rows, 192x208 per cell, RGBA/transparent, with frame counts from `references/animation-rows.md`.
5. Never compose from `<run-dir>/frames_raw`. Compose only from the clean rembg output directory `<run-dir>/frames`.
6. Realistic humans must be large in the pet cells: base fills `92-96%` image height; row-strip people fill each `192x208` slot with no extra empty margin.

## Prerequisites

- Use `uv run --with ...` for script dependencies. If dependencies are already cached, prefer `uv run --offline --with ...`.
- First use may need network access for Python packages and the rembg `u2net_human_seg` model. Warm the model with:

```bash
uv run --with rembg[cpu] --with pillow --with numpy hatch-pet-realistic/scripts/warmup_models.py
```

## Visible Progress

Maintain these four visible milestones:

1. Getting `<Pet>` ready: name, description, optional reference image, run directory.
2. Imagining `<Pet>`'s main look: generate a tight full-body neutral base, inspect it, and lock identity.
3. Picturing `<Pet>`'s poses: generate tight idle + running-right row strips first, then the remaining rows.
4. Hatching `<Pet>`: slice, matte, scale-normalize, inspect, assemble, validate, QA, and package.

## Workflow

### 1. Prepare the run

```bash
uv run --with pillow hatch-pet-realistic/scripts/prepare_pet_run.py \
  --pet-name "<slug>" \
  --display-name "<Display Name>" \
  --description "<detailed adult human description>" \
  --reference <optional-reference-path> \
  --output-dir <run-dir> \
  --force
```

This creates `pet_request.json`, prompt files, layout guides, and `imagegen-jobs.json`.

### 2. Generate and record the base

Use `$imagegen` with `prompts/base-pet.md`. Treat uploaded photos as character references only when policy and backend support allow it; otherwise use a text description derived from the target person.

The base must be one complete full-body person, tightly framed, subject height `92-96%`, head or hair within `4-8 px` of the top safe area, shoes within `4-8 px` of the bottom safe area, and no extra empty margin. Regenerate if the person appears distant or small.

Record the selected built-in image output:

```bash
uv run --offline --with pillow hatch-pet-realistic/scripts/record_imagegen_result.py \
  --run-dir <run-dir> \
  --job-id base \
  --source <CODEX_HOME>/generated_images/<run>/ig_*.png \
  --force
```

Write `pet_request.json#character_lock` with a 30-50 word identity description: adult gender presentation, age range, build, skin tone, eyes, hair, outfit, shoes, and any stable visual details. Replace `{{character_lock}}` in `prompts/rows/*.md`.

### 3. Generate and record row strips

Generate `idle` and `running-right` first. Inspect identity, outfit, frame count, full-body visibility, row action, and spacing. Every invisible `192x208` slot should contain one complete person as large as possible while keeping the head, hands, and shoes visible. If identity drifts or the subject is too small, regenerate before continuing. Use `references/animation-rows.md` for frame counts and row action semantics.

For each row, record the selected built-in image:

```bash
uv run --offline --with pillow hatch-pet-realistic/scripts/record_imagegen_result.py \
  --run-dir <run-dir> \
  --job-id <state> \
  --source <CODEX_HOME>/generated_images/<run>/ig_*.png \
  --force
```

Rows are `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, and `review`. Subagents may generate images, but only the parent records jobs and writes manifests.

### 4. Hatch with clean rembg frames

The safest full pipeline is:

```bash
uv run --with pillow --with numpy --with rembg[cpu] hatch-pet-realistic/scripts/finalize_pet_run.py \
  --run-dir <run-dir> \
  --allow-slot-extraction
```

`finalize_pet_run.py` intentionally uses this sequence:

```bash
uv run --offline --with pillow hatch-pet-realistic/scripts/extract_strip_frames.py \
  --decoded-dir <run-dir>/decoded \
  --output-dir <run-dir>/frames_raw \
  --states all \
  --method slots \
  --no-matte

uv run --with pillow --with numpy --with rembg[cpu] hatch-pet-realistic/scripts/matte_frames.py \
  --frames-dir <run-dir>/frames_raw \
  --output-dir <run-dir>/frames \
  --qa-dir <run-dir>/qa \
  --target-height-ratio 0.94 \
  --running-target-height-ratio 0.88 \
  --edge-padding 2

uv run --offline --with pillow hatch-pet-realistic/scripts/compose_atlas.py \
  --frames-root <run-dir>/frames \
  --output <run-dir>/final/spritesheet.png \
  --webp-output <run-dir>/final/spritesheet.webp

uv run --offline --with pillow hatch-pet-realistic/scripts/validate_atlas.py \
  <run-dir>/final/spritesheet.png \
  --json-out <run-dir>/final/validation.json
```

`matte_frames.py` removes the background and normalizes the transparent foreground size. Use `--no-normalize-scale` only for diagnosis. Do not point `compose_atlas.py --frames-root` at `frames_raw`; those frames still contain the generated background.

### 5. QA and package

Create a contact sheet if finalize did not already do so:

```bash
uv run --offline --with pillow hatch-pet-realistic/scripts/make_contact_sheet.py \
  <run-dir>/final/spritesheet.png \
  --output <run-dir>/qa/contact-sheet.png
```

Package manually only when needed:

```bash
uv run --offline --with pillow hatch-pet-realistic/scripts/package_custom_pet.py \
  --pet-name "<slug>" \
  --display-name "<Display Name>" \
  --description "<short description>" \
  --spritesheet <run-dir>/final/spritesheet.webp \
  --force
```

Writing to `${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/` may require filesystem approval outside the workspace.

## Common Failures

| Symptom | Fix |
| --- | --- |
| `record_imagegen_result.py` rejects the source | Use the original `$CODEX_HOME/generated_images/.../ig_*.png`, not a copied or locally edited image. |
| Atlas validates as nearly opaque | You composed from `frames_raw` or skipped rembg. Re-run `matte_frames.py --output-dir <run-dir>/frames` and compose from `frames`. |
| `uv` tries to reach PyPI in a restricted environment | Retry with `uv run --offline --with ...` if dependencies are cached; otherwise request network approval. |
| Row inspection flags slot extraction | For realistic row strips, slot extraction is acceptable after visual inspection; pass `--allow-slot-extraction` to finalize. |
| Identity drifts across rows | Regenerate the row using the locked identity paragraph and base image as visual truth; do not locally edit faces or outfits. |
| Subject too small or unreadable in the pet UI | Regenerate the base or row with tight `192x208` slot framing and no extra empty margin, then finalize so `matte_frames.py` can scale-normalize transparent frames. |

## References

- `references/animation-rows.md`: row names, frame counts, durations, and motion semantics.
- `references/qa-rubric.md`: visual QA and repair guidance.
- `references/realistic-style-guide.md`: realistic prompt anchors and negatives.
- `references/codex-pet-contract.md`: Codex atlas loading contract.

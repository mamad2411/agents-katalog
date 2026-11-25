---
name: argos-eye
description: |
  Locate a natural-language target inside an image and return verified pixel
  coordinates. Uses an iterative zoom-and-refine loop that works around the
  one-shot coordinate limitation of current vision-language models. Activates
  when the user asks to find, locate, or point to something in an image, or
  invokes /argos-eye explicitly.
---

# argos-eye

Given an image and a natural-language target description, return a verified
bounding box and center point in the original image's pixel space, together
with an auditable evidence bundle.

This skill is intentionally narrow. It does not capture screenshots, drive
UIs, or orchestrate workflows. It answers one question: *where in this image
is the thing the user described?*

## Inputs

- `image` — path to the source image.
- `target` — natural-language description of what to locate.
- `max_iter` *(optional, default 3)* — iteration ceiling.
- `zoom` *(optional, default 3.0)* — crop scale factor.
- `evidence_dir` *(optional, default `.argos-eye`)* — where to persist
  intermediate artifacts.

### Acquiring inputs

If the user invokes the skill without an image path, ask once:

> "Please provide the image — drag it into chat, paste it, or pass a path.
> I also need a short natural-language description of the target."

Claude Code stores pasted or dropped images at a temporary path that the
host exposes to the skill. Use that path as `image`. Do not attempt to
capture a screenshot yourself.

If the user provides only an image with no target description, ask for the
target. Do not guess.

## Output contract

Always return a single JSON object printed to stdout as the final action:

```json
{
  "bbox":       [x1, y1, x2, y2],
  "center":     [x, y],
  "confidence": 0.0,
  "iterations": 0,
  "converged":  false,
  "evidence":   ".argos-eye/<timestamp>/"
}
```

If the target cannot be located with confidence above `min_confidence`
(default 0.5), set `bbox` and `center` to `null` and include a `reason`
field. Never fabricate a coordinate.

All coordinates are integer pixels in the original image's coordinate
system — not in any crop's local system.

## The loop

Execute the following loop. Persist every step into `evidence_dir`.

```
propose → crop → re-inspect → converged? → (no → refine) | (yes → remap → output)
```

### 1. Initialize evidence

Run:

```bash
python scripts/evidence.py init \
  --image "$IMAGE" \
  --target "$TARGET" \
  --out "$EVIDENCE_DIR"
```

This prints the absolute evidence directory path. Use it for all subsequent
step artifacts.

### 2. Propose (iteration 0)

Read the full image. From its content alone, propose a bounding box that
contains the target. Write the proposal as JSON to
`<evidence_dir>/iter-0-bbox.json` with fields:

```json
{ "bbox": [x1, y1, x2, y2], "reasoning": "short justification", "source": "full_image" }
```

Use integer pixel coordinates in the original image's system.

### 3. Crop

Run:

```bash
python scripts/crop.py \
  --image "$IMAGE" \
  --bbox-file "<evidence_dir>/iter-N-bbox.json" \
  --zoom "$ZOOM" \
  --out "<evidence_dir>/iter-N-crop.png"
```

This produces an enlarged crop around the proposed region (with a padding
margin so the target is not flush against the edge).

### 4. Re-inspect

Read the crop file. Propose a *tightened* bounding box in the **crop's
local coordinate system**. Write to `<evidence_dir>/iter-(N+1)-bbox.json`
with fields:

```json
{
  "bbox":       [x1, y1, x2, y2],
  "reasoning":  "short justification",
  "source":     "crop",
  "crop_file":  "iter-N-crop.png"
}
```

If on re-inspection the target is clearly not in the crop, record:

```json
{ "bbox": null, "reasoning": "...", "source": "crop", "not_found": true }
```

and exit the loop as a not-found result.

### 5. Convergence check

After each re-inspection, compare the new proposal (remapped to the
original system) with the previous iteration's proposal:

```bash
python scripts/remap.py converge-check \
  --prev "<evidence_dir>/iter-(N-1)-bbox.json" \
  --curr "<evidence_dir>/iter-N-bbox.json" \
  --crop-bbox-file "<evidence_dir>/iter-(N-1)-bbox.json" \
  --iou-threshold 0.85
```

Exit status 0 means *converged*. Non-zero means *continue*.

If not converged and the iteration count is below `max_iter`, go back to
step 3 using the tightened bbox as the new region to crop. Otherwise go to
step 6 with the current best proposal.

### 6. Remap and finalize

Run:

```bash
python scripts/remap.py finalize \
  --evidence-dir "$EVIDENCE_DIR" \
  --min-confidence "$MIN_CONFIDENCE"
```

This reads all iteration files, remaps the final crop-relative bbox back
to the original image, scores confidence based on how much the proposals
converged, and writes `<evidence_dir>/result.json`.

Print the content of `result.json` to stdout as the skill's final response.

## Rules

- **Never fabricate coordinates.** If you are not confident, return
  `null` bbox with a `reason`. A refused answer is better than a wrong one.
- **Use the original image's coordinate system in every output.** The
  remap script handles the translation — do not hand-compute.
- **One image call per iteration.** Do not re-read the same crop twice.
- **Respect `max_iter`.** Do not exceed it even if convergence looks close.
- **Do not delete `evidence_dir`.** It is the audit trail.

## Failure modes to watch

- Target is smaller than ~20 pixels in the original image — accuracy is
  fundamentally limited. Report low confidence.
- Multiple plausible matches — return the most prominent and note the
  ambiguity in `reasoning`.
- User description is ambiguous ("the button" on a page with many) — ask
  one clarifying question before running the loop.

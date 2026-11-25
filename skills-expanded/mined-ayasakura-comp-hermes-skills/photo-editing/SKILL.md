---
name: photo-editing
description: Edit uploaded photos locally with Qwen-Image-2.1 via ComfyUI, including retouching, Fuji/film color grades, restyling and localized content edits. Use for requests to modify an input image; for text-to-image without a reference, use qwen-image or create-image.
---

# Photo Editing — Qwen-Image-2.1

Use **Qwen-Image-2.1 through local ComfyUI** as the default photo editor. Do not silently substitute FLUX, Anima, or a text-only generation. Do not download models or stop other inference services.

## Dedicated editing CLI — use this entry point

For every image-edit request, run the bundled CLI as the single execution entry point. It supports instruction-based color grading, retouching, adding/removing/replacing objects or characters, text insertion, background changes and full restyling. Do not write a temporary workflow or another upload/polling script.

```bash
python3 ~/.hermes/skills/photo-editing/scripts/photo_edit.py \
  "Apply only a subtle film color grade to <image1>; preserve subject, pose and framing." \
  --image /absolute/path/input.jpg --output /absolute/path/edited.png
```

This is a **photo-editing CLI backed by the existing ComfyUI API**, not the `comfy` installation/management CLI. It validates node availability, uses the three native model loaders, saves workflow/job evidence, and reports submission or execution errors immediately. Do not invent `DownloadAndLoadQwenModel` or download weights. The tested loader names are UNETLoader, CLIPLoader and VAELoader.

Use unique output names. Parameters: `--seed 2003 --steps 25 --resolution 0 --timeout 600`. The graph details below are for maintenance/debugging, not a reason to rewrite the runner per request.

### One job, one runner — execution contract

- The existing ComfyUI server handles the edit; invoking the CLI does not start a new server. Do not start/restart a server per edit.
- Invoke the CLI **once** for a requested output. It uploads, submits, polls history, detects errors and downloads the image itself.
- Let the command run to completion; set the shell tool timeout above the CLI timeout (for example 650 seconds for `--timeout 600`).
- While the CLI remains active, do not launch a second CLI, a Python requests loop, curl polling, or another POST to `/prompt`. If the harness detaches the command, consume that same command's completion through its supported mechanism.
- If the CLI explicitly times out or its process has ended without delivering the output, use the stored prompt ID from `.job.json` and run the **same CLI** with `--resume PROMPT_ID`, the same `--image` and the same `--output`. Resume only retrieves that existing job; it does not resubmit. Do not invent a separate polling script.
- A timeout/interruption does not cancel the server job. Do not resubmit merely because no image has appeared yet. Check the existing task through resume first.
- On submission rejection or execution error, stop and report the actual error. Fix only a diagnosed problem; do not keep waiting on a nonexistent prompt ID, download weights or silently change models.
- Direct API calls are reserved for explicit diagnostics or maintenance after an actual error, not ordinary edit execution.

Regression tests:

```bash
python3 ~/.hermes/skills/photo-editing/scripts/test_photo_edit.py
```

## Required workflow

1. Inspect the supplied image with `read`. Note dimensions, subject, pose, framing and details that must remain unchanged.
2. Use the bundled `scripts/photo_edit.py` CLI above. Do not generate a new runner, use the text-to-image CLI, or manually upload the image first.
3. Pass the original image (or annotated copy for circle guidance) with `--image`, a unique PNG path with `--output`, and an explicit edit prompt. The CLI uploads the reference, builds the validated graph and submits once.
4. Retain the printed prompt ID and the `.job.json` / `.workflow.json` sidecars. Let the CLI handle waiting; do not query queue/history separately during normal execution. On an error, report the actual message; do not claim sampling started without a valid prompt ID. On timeout, follow the same-CLI resume contract above.
5. After the CLI downloads the result, inspect it against the original. Confirm text spelling, subject fidelity and framing, and disclose dimensions rounded to multiples of 32.
6. Attach the output with `[[image: /absolute/path/to/result.png]]`. Report changes and any unwanted redraws honestly.

Route service health checks and repairs through the **restart-service** skill. Do not restart a busy shared ComfyUI instance merely to edit a photo.

## Model and sampling defaults

- DiT: `qwen_image_2.1_int8_convrot.safetensors`
- CLIP: `qwen3vl_8b_int8_convrot.safetensors`, CLIPLoader type `qwen_image`
- VAE: `qwen_image_2.1_vae_bf16.safetensors`
- KSampler: steps **25**, CFG **1**, sampler **euler**, scheduler **simple**, denoise **1.0**
- Fix the seed during iteration, for example 2003.
- `resolution=0` preserves reference dimensions rounded to multiples of 32; output follows image_1's aspect ratio. For large images use `resolution=1024` to reduce memory/runtime while preserving aspect ratio. Disclose resizing.

Do not interpret fewer steps as a reliable edit-strength control. Denoise 1.0 is normal for instruction-based reference editing; lowering denoise on an empty target latent is not a validated minimal-change workflow.

## Critical API wiring

ComfyUI's Autogrow inputs use **flat dotted keys** in the API graph:

```python
"images.image_1": ["9", 0]
```

**Do not use** `"images": {"image_1": ["9", 0]}`. This was experimentally found to discard the reference input and yield a fresh square generation. A successful queue response alone does not prove that the reference is connected.

Reuse the helper in `~/.hermes/skills/qwen-image/scripts/qwen_image.py` if convenient. After its `build_workflow(...)`, apply these edits (node IDs correspond to that helper):

```python
wf["9"] = {"class_type": "LoadImage", "inputs": {"image": uploaded_name}}
wf["4"]["inputs"].update({
    "vae": ["3", 0],
    "resolution": 0,
    "images.image_1": ["9", 0],
    "prompt": edit_prompt,
    "negative_prompt": "",
})
wf["6"]["inputs"]["latent_image"] = ["4", 2]
del wf["5"]  # remove the text-to-image EmptyLatentImage
```

Node 4 is **TextEncodeQwenImage21**. Its outputs are positive (0), negative (1), and reference-sized empty target latent (2). Connect all three to KSampler; use the same VAE to encode references and decode output. Keep the helper's positive/negative connections, model loader, VAEDecode and SaveImage.

Additional references use `images.image_2`, etc.; address them as `<image2>` in the prompt. The official model describes up to 10 reference images; the local node exposes 16 slots, which is not a guarantee of validated model quality for 16 images.

If a landscape/portrait source unexpectedly yields a square result, stop and check the reference connection and target latent wiring before blaming model fidelity.

## Arbitrary instruction-based edits

Follow the user's requested extent of change; do not force every request into a subtle color grade. Inspect the image, identify the target and express the operation explicitly relative to `<image1>`.

| Request | Prompt approach |
|---|---|
| Add/remove/replace an object or character | State target position, replacement/removal and what surrounding content should stay |
| Pose, clothing, face, hairstyle or expression | Specify the requested changes and which identity/details should remain |
| Background or environment replacement | Describe the new background and preserve the requested foreground subject |
| Full restyle, anime, illustration or dramatic transformation | Explicitly allow the requested broad change; preserve only user-required features |
| Text or signage | Quote exact text, placement, typography and desired readability |
| Color grade/film look | Change color/texture only and retain scene geometry |

Example — replace a character:

```text
In <image1>, replace only the person on the left with Frieren as a rabbit girl,
with long silver hair and rabbit ears. Keep the person on the right, the comet,
city, landscape and original framing unchanged. Match the existing anime art
style and lighting. Do not add text or alter unrelated objects.
```

For unfamiliar named subjects, research their appearance before editing rather than inventing details. Optional circle guidance helps distinguish ambiguous targets, but do not add a circle when positioning or wording is already clear. The bundled CLI currently accepts one image; do not invent multiple-image flags. Multi-reference support requires an explicitly implemented/tested runner extension.

Do not promise every arbitrary instruction will succeed. Inspect each output for requested changes, spelling and unwanted modifications. If another attempt is needed after the first job completes, explain what failed and adjust the prompt or seed; this is a new deliberate attempt, not an automatic duplicate submission.

## Minimal-change prompt discipline

Name only the requested change, refer explicitly to `<image1>`, and specify preservation constraints. Do not re-describe the scene in a way that invites recomposition. Do not automatically add beautification, denoising, bokeh, new lighting or fur/skin reconstruction.

Example — film color grade:

```text
Apply only a subtle Fujifilm color-negative film color grade to <image1>.
Keep the same subject, face, pose, framing, background, shadows and all object
positions unchanged. Add gentle film color rendering, soft highlight rolloff
and fine organic film grain. Do not redraw details or alter the composition.
```

A subtle grade may be barely visible; if the user wants stronger styling, modify the requested color treatment rather than loosening preservation constraints. A seed is for controlled iteration, not a composition lock.

Film names are aesthetic guidance, not certified Fujifilm color science or an exact camera simulation. Avoid claims that an adapter was loaded: this Qwen workflow does not use the old Analog Redmond/RefControl LoRAs.

## Adding text to an existing image

Use the same CLI with the unannotated image. Specify exact spelling, placement, font appearance and preservation constraints; verify the rendered spelling visually.

```bash
python3 ~/.hermes/skills/photo-editing/scripts/photo_edit.py \
  "Add only the text 'AyaSakura' at the top center of <image1>, in elegant white cursive with a subtle dark outline. Preserve characters, faces, poses, background and framing; do not redraw anything else." \
  --image /absolute/path/input.jpg --output /absolute/path/name_added.png
```

End-to-end validation: the dedicated CLI successfully added `AyaSakura` to an anime reference while broadly preserving its characters and landscape. The 630×422 input became 640×416 due to dimension rounding. This does not guarantee pixel-identical preservation. The bundled regression tests cover reference wiring, native loaders and error handling; passing these alone is not proof of visual fidelity.

## Circle-guided localized edits

For a specific object or region, a visible circle can help communicate the edit target. Work on a **copy** of the original. Draw a thin high-contrast circle around the requested region, without obscuring important details; upload this annotated copy as image_1.

Example:

```text
In <image1>, the red circle marks the head for a localized edit. Replace only
the two cat ears with realistic rabbit ears attached naturally to the same
head. Keep the cat face, eyes, body, paws, tail direction, pose, shadow,
pavement, lighting, viewpoint and framing unchanged. Remove the red annotation
circle from the output. Do not change anything else.
```

Show the annotated input and result when useful. Circles are semantic guidance, **not a hard pixel mask**. Do not circle for global grading; use the unannotated source.

## Fidelity and validation

Validated in this conversation: correct reference wiring preserved a cat's overall pose and scene while replacing ears; an unannotated film-grade pass also preserved the composition, but the grade was subtle. These are qualitative examples, not universal fidelity guarantees.

Compare subject identity/markings, face, limbs, tail, background geometry, framing and residual annotations. Report unwanted changes. Generative editing is not guaranteed to preserve every pixel. If strict outside-region pixel preservation is requested, use a deliberate mask/compositing workflow and verify the untouched region; do not describe circle guidance alone as such a guarantee.

## Official references

- ComfyUI workflow/settings: https://docs.comfy.org/tutorials/image/qwen/qwen-image-2-1
- Qwen architecture and editing examples: https://github.com/QwenLM/Qwen-Image-2.1

Official ComfyUI templates include optional image-edit prompt enhancement. This minimal workflow does not require it. Do not silently enable prompt rewriting; inspect any rewritten prompt to avoid broadening the requested edit.

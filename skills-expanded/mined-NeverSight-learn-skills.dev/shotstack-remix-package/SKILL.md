---
name: shotstack-remix-package
description: Turn a reviewed trend-video blueprint into scene prompt files plus a validated shotstack.json package for Nano Banana 2, Grok Imagine, Kling v3, and Shotstack. Do not use this skill for raw scene analysis before the blueprint is approved.
---

# Shotstack Remix Package

Use this skill after the planning artifacts exist and the task is to build the actual prompt files and Shotstack package.

Do not use this skill when `blueprint.json` sets `renderer = "remotion"`.

## Required inputs

Load these files from `output/<job_id>/`:

- `story.json`
- `variable_map.json`
- `blueprint.json`
- `manifest.json`

Also load the source video from `input/<job_id>.mp4`.

If they do not exist, use `$trend-short-blueprint` first.
If `blueprint.renderer != "shotstack"`, stop and route the job to the Remotion package workflow instead of forcing Shotstack artifacts.

## Required workflow

1. Read the contract in [`docs/output-contract.md`](../../../docs/output-contract.md).
2. Read Shotstack implementation notes in [`references/shotstack-patterns.md`](references/shotstack-patterns.md).
3. Read provider guidance in [`../trend-short-blueprint/references/provider-guidance.md`](../trend-short-blueprint/references/provider-guidance.md).
4. Run `bash scripts/extract_source_audio.sh input/<job_id>.mp4 output/<job_id>/source_audio.mp3`.
5. For each scene, write the expected prompt files from `blueprint.json`.
6. When a scene has editable text, measure source text geometry first. For white-box labels or caption bars, use [`scripts/extract_text_geometry.py`](scripts/extract_text_geometry.py) to capture the source box/text bbox and the Shotstack hint values, then save that metadata into `blueprint.json`. Pass `--output-width` and `--output-height` so font size and box dimensions are scaled to the actual Shotstack viewport.
7. Build `shotstack.json` using aliases, merge keys, deterministic scene ids, a dedicated `SOURCE_AUDIO_MP3` audio clip track, and extra tracks when a scene has `overlay_layers`.
8. If editable text is plain stroked text with no box to hide the source text, do not rely on source-derived clips for the Studio preview unless you also provide a clean plate. Otherwise keep the package `review_required`.
9. Upload the local review assets needed for editor testing to Cloudinary and save `cloudinary_assets.json`.
10. Build `shotstack.pasteable.json` with direct Cloudinary `secure_url` values and no merge placeholders.
11. Update `manifest.json`.
12. Run [`scripts/validate_package.py`](scripts/validate_package.py) against the package directory.
13. Stop at the review gate.

## Prompt writing rules

- Keep one prompt file per scene and per prompt type.
- Use deterministic filenames from the blueprint.
- Keep reference roles explicit in image prompts.
- Keep motion envelope, camera behavior, and continuity rules explicit in video prompts.
- If a scene is image-only in Shotstack, omit the video prompt file only when `blueprint.json` says it is not required.

## Shotstack rules

- Use uppercase merge keys such as `SCENE_001_MEDIA`
- Use double braces inside strings such as `{{ SCENE_001_MEDIA }}`
- Keep `merge[].find` values brace-free
- Prefer `alias` and `alias://...` for overlay timing
- Do not use `timeline.soundtrack` for the source audio in repo packages; use a dedicated audio clip track instead
- For source audio clips, keep `volume` inside `asset` and use numeric `start` and `length`
- You may use `start: "auto"` for sequential ordering, but every base scene clip must use a numeric `length` copied from the analyzed source-scene duration in `blueprint.json`
- When a scene has image or video overlays, place them on higher tracks and map each one from `overlay_layers`
- Prefer `asset.type = "rich-text"` for editable text overlays. If legacy `asset.type = "text"` is used, keep `font` and `stroke` object-shaped: `font.family`, `font.size`, `font.color`, optional `font.weight`, `stroke.color`, and `stroke.width`.
- Do not emit Shotstack text assets with `asset.font` as a string, top-level `asset.color`, top-level `asset.size`, or `asset.strokeWidth`; the local validator treats those as render-blocking schema errors.
- Use built-in font families such as `Montserrat`, `Open Sans`, `Roboto`, and `Work Sans` by default. For custom fonts, add a public HTTPS `.ttf` or `.otf` URL under `timeline.fonts[].src`; do not use a Google Fonts CSS URL.
- Every packaged job should also include `cloudinary_assets.json` plus a direct-use `shotstack.pasteable.json`
- In `shotstack.pasteable.json`, replace placeholders with Cloudinary `secure_url` values, remove the `merge` array, and prefer explicit numeric `start` values
- In `shotstack.pasteable.json`, do not use `width` or `height` on image overlay clips; Shotstack Studio rejects them there, so size image overlays with `fit` plus `scale`
- Text clips in `shotstack.pasteable.json` may still use `width` and `height` when the source design depends on an exact text-box size
- For `contract_version` `1.1` and later, editable text overlays must carry measured `source_geometry` in `blueprint.json`
- If automatic detection is noisy, use manual bbox arguments or reuse a representative `reference_asset` from another scene with the same label design instead of eyeballing the Shotstack numbers
- For plain text with no source box, prefer a clean remake or clean plate for Studio preview; do not assume a source-derived clip can be faithfully overwritten with editable text

## Validation goal

A package is not ready until the validator confirms:

- required files exist
- `source_audio.mp3` exists
- every scene id is unique
- every blueprint scene duration matches the analyzed source scene duration
- every prompt file referenced by the blueprint exists
- every base Shotstack scene clip uses the same numeric length as the source scene
- every declared overlay layer has a matching merge key and valid timing
- every Shotstack placeholder has a matching merge key
- every merge key is actually used
- every alias reference resolves
- every text or rich-text asset uses object-shaped font and stroke fields
- every custom font source is a public HTTPS `.ttf` or `.otf` file

## References

Read only what you need:

- contract: [`docs/output-contract.md`](../../../docs/output-contract.md)
- Shotstack patterns: [`references/shotstack-patterns.md`](references/shotstack-patterns.md)
- text-geometry helper: [`scripts/extract_text_geometry.py`](scripts/extract_text_geometry.py)
- provider guidance: [`../trend-short-blueprint/references/provider-guidance.md`](../trend-short-blueprint/references/provider-guidance.md)
- starter template: [`assets/shotstack.template.json`](assets/shotstack.template.json)
- audio extraction: [`scripts/extract_source_audio.sh`](scripts/extract_source_audio.sh)
- validator: [`scripts/validate_package.py`](scripts/validate_package.py)

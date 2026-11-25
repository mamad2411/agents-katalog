---
name: minecraft-skin-maker
description: Create or revise importable Minecraft player skins from images, existing skin PNGs, text descriptions, or both. Delivers the skin PNG, previews rendered from the exported texture and a Bedrock skin pack, with technical choices handled automatically.
---

# Minecraft Skin Maker

Turn the user's idea into a finished skin. Assume no Minecraft skin-making knowledge. Produce the first result without a setup questionnaire, options menu or approval checkpoint. Edition, arm width and layers are internal decisions. Honor volunteered preferences; otherwise use Classic arms, a 64×64 PNG and a companion `.mcpack`. Preserve a reliably known existing model. Ask only when the input is genuinely unusable, such as an inaccessible image with no description.

## Agent requirements

Use an agent with file read/write access, Python execution and image inspection for references and exported previews. Read supporting files relative to this skill's directory and use the host's available image-viewing and shell tools. The optional `agents/openai.yaml` file supplies Codex interface metadata; the workflow and scripts run independently of it. If visual inspection is unavailable, state that limitation and leave the visual review incomplete.

## Create

1. For an image, inspect the actual attachment using the available image-viewing tool. If it is an existing skin atlas, start with the importer below to preserve its design and model. For text, interpret the description in its language. Read [likeness-and-pixel-art.md](references/likeness-and-pixel-art.md) when translating a reference or improving visual quality. Save a short `reference_brief` in the design: distinguishing features, their left/right orientation, expression, materials and assumptions for unseen areas. Keep these decisions internal and explain only useful, significant assumptions after delivery.
2. Read [design-format.md](references/design-format.md). Write editable design JSON with named palette entries and independent components. Build a design specific to this request; arbitrary face-local pixel patterns support humans, animals, robots, armor and clothing. `assets/blank-design.json` and the UV maps/masks are reusable coordinate aids. `assets/examples/` contains two complete designs to illustrate component organization; design each new character from its own input.
3. Resolve the head's hairline, eyes and expression before adding outfit details. Use contiguous shading that describes locks, folds or surface form. Keep broad areas of smooth cloth quiet. Use outer layers selectively for overlapping hair, collars, cords and cuffs within the standard player model. Align seams and bands across faces. The wearer's right is the viewer's left in a front view. Keep every used base pixel opaque and unused pixels transparent. Assemble and export with the helper below.
4. For a local reference image, pass it to `build --reference` and open `reference-review.png`; compare the original, enlarged head details and small full-body view. If the usable reference is visible only in the conversation, compare it directly with the rendered views. Also open `preview.png` for front, back and both three-quarter views. Follow the visual questions in the likeness guide, correct concrete mismatches, then rebuild and recheck. These previews sample `skin.png` directly. Inspect another angle when needed. To place or fix exact pixels, run `faces` and read the gridded tile of the face you are editing. Record the actual final inspection and texture hash in `visual-inspection.md`; passing format checks alone does not establish likeness.
5. Deliver the skin and preview first, then the Bedrock pack and short import instructions in the user's language. Keep technical explanations brief. State the required Classic or Slim selection as an import instruction after delivery. Keep `design.json` for revisions and provide it when useful. Record actual visual inspection separately from the automated report.

Optional image generation can help explore a concept or supply a reference. Final placement, PNG export and validation stay deterministic. A generated character illustration is not an exported-skin preview. The agent supplies interpretation and pixel-design decisions through its normal model access; the helpers require no separate image-generation API account.

## Run the helpers

Use Python 3.9+ with Pillow and NumPy; the Python 3.9 built into macOS works. Prefer an already available interpreter that imports both. On first use, if needed, create a local environment in the skill directory and install `requirements.txt`; handle this automatically within normal tool permissions. The following examples use a POSIX shell; adapt the syntax to the host. On Windows, a virtual environment's interpreter is `.venv\Scripts\python.exe`. `SKILL_DIR` means the absolute directory containing this file:

```sh
python3 -m venv "$SKILL_DIR/.venv"
"$SKILL_DIR/.venv/bin/python" -m pip install -r "$SKILL_DIR/requirements.txt"
```

Set `PY` to that interpreter (or the working bundled Python); keep all generated user artifacts in the current task's output directory. Exact commands:

```sh
"$PY" "$SKILL_DIR/scripts/skinmaker.py" init design.json --name "My character"
"$PY" "$SKILL_DIR/scripts/skinmaker.py" build design.json --out outputs/my-character
"$PY" "$SKILL_DIR/scripts/skinmaker.py" build design.json --reference reference.png --out outputs/my-character
"$PY" "$SKILL_DIR/scripts/skinmaker.py" validate outputs/my-character/skin.png --model classic
"$PY" "$SKILL_DIR/scripts/skinmaker.py" validate outputs/my-character/skin.mcpack --model classic --png outputs/my-character/skin.png
```

`build` defaults to both exports and writes PNG, mcpack, four individual views, a preview sheet, editable JSON, import notes and validation evidence. `--reference` also creates a local comparison sheet and records both source hashes; it leaves likeness review pending until the agent inspects it. Use `--export java` for an explicit PNG-only request; `--export bedrock` retains the main PNG and includes the pack. It validates size, masks, base opacity, alpha, references, geometry, UUIDs, localization and ZIP contents. A zero exit status means automated format checks passed.

## Revise or import

Read the previous design. Edit only the requested palette keys/components; write a new version. Preserve unrelated features and check the resulting pixel differences with `diff`. Examples:

```sh
"$PY" "$SKILL_DIR/scripts/skinmaker.py" revise design.json --set 'jacket=#a43d47' --set 'jacket_shadow=#6f2933' --out design-red.json
"$PY" "$SKILL_DIR/scripts/skinmaker.py" revise design.json --model slim --out design-slim.json
"$PY" "$SKILL_DIR/scripts/skinmaker.py" build design-slim.json --out outputs/my-character-slim
"$PY" "$SKILL_DIR/scripts/skinmaker.py" import existing-skin.png --out imported-design.json
"$PY" "$SKILL_DIR/scripts/skinmaker.py" preview skin.png --model slim --out outputs/preview
"$PY" "$SKILL_DIR/scripts/skinmaker.py" preview skin.png --model classic --yaw 33 --pitch 16 --out outputs/opposite-view
"$PY" "$SKILL_DIR/scripts/skinmaker.py" review skin.png --reference reference.png --model classic --out outputs/review
"$PY" "$SKILL_DIR/scripts/skinmaker.py" pack skin.png --model slim --name "My character" --out skin.mcpack
"$PY" "$SKILL_DIR/scripts/skinmaker.py" faces skin.png --model classic --part head --out outputs/faces
"$PY" "$SKILL_DIR/scripts/skinmaker.py" diff old/skin.png new/skin.png --model classic --out outputs/diff
```

`faces` writes one enlarged sheet per part with every base and outer face, a pixel grid and the face-local x,y numbers used in design operations; transparent pixels show as a checkerboard. After any revision, run `diff` on the previous and new `skin.png`: it lists changed pixels per face with face-local bounding boxes, and `--out` outlines them on face sheets. Changes outside the requested feature mean the edit leaked; fix them before delivery.

The importer accepts modern 64×64 and legacy 64×32 PNGs, preserves pixel data in a portable embedded source, and reports compatibility repairs. Use `import --model slim` or `--model classic` when reliable source metadata identifies the model. The model converter repacks/resamples arm faces while preserving all other pixels. Review narrow motifs after width changes.

For an extra inspection angle, supplying `--yaw` or `--pitch` writes one `custom-view.png`; the omitted angle defaults to zero. Yaw `33` shows the opposite side from the standard three-quarter view. Yaw `90` shows the wearer's left side and `-90` the right; positive pitch looks down from above. Keep these choices internal.

## Compatibility and evidence

Read [formats-and-import.md](references/formats-and-import.md) for packaging and device-specific delivery. Official guidance was checked on 2026-09-26; verify current official sources when platform/version uncertainty matters. Supported output is a standard 64×64 player skin. Convert impossible shapes into recognizable texture/outer-layer details and mention material compromises. Custom 3D geometry, functional capes, high-resolution output and automatic Minecraft account updates are outside this helper.

Windows/mobile Bedrock imports and Java imports have different steps. Consoles do not officially import arbitrary custom skin files. Match any known device; otherwise give concise Java and Windows/mobile Bedrock instructions plus the console limitation. A pack export alone is not proof of device import.

For maintenance, run `"$PY" "$SKILL_DIR/scripts/selftest.py" --out work/skin-checks`. Regenerate masks/templates with `skinmaker.py templates --out <directory>`. Distinguish automated checks, actual preview inspection and in-game testing. Claim in-game testing only after performing it. The helper leaves visual inspection pending and in-game testing unperformed until independently recorded.

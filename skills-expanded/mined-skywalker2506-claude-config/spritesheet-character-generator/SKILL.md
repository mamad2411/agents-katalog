---
name: spritesheet-character-generator
description: Create 2D game character spritesheets from art direction, master character references, and motion/view requirements. Use when Codex is asked to design or generate pixel art, normal sprites, walk cycles, action sheets, 2x2 multiview references, animation-ready PNG sheets, or project asset folders using imagegen plus Hugging Face FLUX LoRA spritesheet models.
---

# Spritesheet Character Generator

> **Bu depo icin hat ayrimi (2026-08-17):** sprite animasyonlari BU hattan
> uretilir. Video/sinematik icin **[/animate](../animate/SKILL.md)**, tek
> duran gorsel icin **[/gorsel-uret](../gorsel-uret/SKILL.md)**, 3D model icin
> **[/threejs-3d-character-pipeline](../threejs-3d-character-pipeline/SKILL.md)**.
> Kararsizsan: **[/uretim-hatti-sec](../uretim-hatti-sec/SKILL.md)**.
>
> Referans verildiginde stil tarif EDILMEZ, gosterilir:
> **[/reference-style](../reference-style/SKILL.md)**. Ayni karakterin farkli
> animasyonlari icin ayni kaynak gorsel kullanilir — olculdu, yuruyuste
> kapusonlu / saldirida kel tutarsizligi buradan cikiyor.
>
> Bu hat ortak GPU kuyruguna GIRMEZ; proje icinde kendi araclariyla calisir.

## Overview

Use this skill to turn a character idea into a practical 2D game spritesheet pipeline. It works standalone, and it can feed assets into browser/Three.js games, prototype projects, localization-ready UI, or later shipper/export workflows.

The default flow is intentionally small: analyze the game style, make a master character and master pose plan, route to the right spritesheet model, generate or prepare references, validate the grid, then place final assets in the target project.

## Required Research And Dependency Gate

Before claiming a Hugging Face LoRA can be used locally, check that the required runtime exists. If it is missing, tell the agent/user exactly what must be installed and continue by preparing prompts, references, and folders.

Run:

```bash
node <this-skill>/scripts/check-spritesheet-deps.mjs
```

Use `imagegen` for master character art, master pose reference, concept sheets, and fallback sprite concepts. Do not claim built-in imagegen can load arbitrary Hugging Face LoRA weights directly. Use the HF LoRA routes only through an available local Diffusers setup, ComfyUI setup, or fal.ai endpoint/API where applicable.

Always record model names, licenses, prompts, seed if known, reference image paths, and any manual cleanup performed.

## Workflow

1. Inspect the target project and requested character.
   - Identify art style: pixel, painterly, clean vector-like, top-down RPG, platformer side-view, isometric, etc.
   - Identify needed states: idle, walk, run, attack, jump, hurt, death, emote, 4-direction movement, 8-direction movement, or 2x2 multiview.
   - Check existing asset size, camera angle, palette, and folder conventions.

2. Build a master character brief.
   - Define silhouette, proportions, costume, key colors, face/hair/helmet, weapon/tool, and personality.
   - Add negative constraints: no extra limbs, no cropped headgear, no inconsistent outfit, no mixed camera angles in a single row, no messy background in final game asset.
   - Generate a master character image with `imagegen` when a visual reference will improve consistency.
   - Generate a master pose or turnaround image when the target model supports image-to-image or edit workflows.

3. Route the model.
   - Read `references/model-routing.md` for the current routing table.
   - Prefer Apache-2.0 routes for commercial/game shipping when they fit.
   - Treat non-commercial licenses as prototype-only unless the user explicitly verifies allowed commercial use.

4. Generate a prompt pack and build folder.
   - Run:

```bash
node <this-skill>/scripts/plan-spritesheet-character.mjs <target-project> --name hero --character "clockwork knight" --style "pixel art top-down RPG" --motion 4walk
```

5. Generate assets through the available path.
   - `imagegen`: master character, reference pose sheets, fallback sprite concept, visual style tests.
   - Diffusers/ComfyUI: local LoRA generation when dependencies and licenses are ready.
   - fal.ai: hosted 2x2 image-to-image route when `FAL_KEY` and endpoint access are available.

6. Validate and stage.
   - Use `scripts/create-spritesheet-preview.mjs` to make a quick browser preview.
   - Check grid dimensions, row/column order, frame anchors, alpha/background, silhouette stability, and cropping.
   - Export final game assets under `public/assets/sprites/<character>/` when the project uses that convention.
   - Keep intermediates under `buildable/spritesheets/<character>/`.

## Output Shape

Prefer this structure inside the target project:

```text
buildable/spritesheets/<character>/
  character-brief.md
  prompt-pack.json
  generation-log.md
  preview/
public/assets/sprites/<character>/
  <character>_<state>.png
  <character>.json
  references/
```

If the project already has a different asset convention, follow it and keep the `buildable/spritesheets/<character>/` audit trail.

## QA Checklist

- Character identity stays consistent across frames, directions, and states.
- Frame grid matches the requested columns/rows exactly.
- Feet, center mass, weapon/tool anchor, and hitbox origin stay stable.
- Background is transparent or consistently removable.
- Pixel art is exported at crisp integer scale and is not blurred.
- State names and JSON metadata match the consuming game code.
- License notes are recorded before anything is treated as shippable.
- Generated assets are not left only in temporary imagegen output folders; copy or save them into the target project.

## References

- `references/model-routing.md` - choose between the three HF LoRA routes and imagegen fallback.
- `references/spritesheet-art-direction.md` - master character, master pose, prompt, and validation guidance.

## Scripts

- `scripts/check-spritesheet-deps.mjs` - reports missing local/fal/ComfyUI dependencies and install guidance.
- `scripts/plan-spritesheet-character.mjs` - creates the character brief, prompt pack, and generation log skeleton.
- `scripts/create-spritesheet-preview.mjs` - creates an HTML grid preview for a spritesheet image.

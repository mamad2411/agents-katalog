---
name: image-gen-tool
description: >-
  Image and 3D model generation tool. Generates full-body illustrations, bust-up portraits, chibi characters, and 3D models using NovelAI, Flux, and Meshy.
  Use when: Use when: illustration generation, character image creation, 3D model/Meshy output, or image pipeline execution is needed.
tags: [image, 3d, generation, external]
---


# Image Gen Tool

An external tool for generating character images and 3D models.

## How to Invoke

**Bash**: Run with `animaworks-tool image_gen <サブコマンド> [引数]`. For long-running processes, execute in the background with `animaworks-tool submit image_gen pipeline ...`.

## List of Actions

### character_assets — Batch Pipeline Generation
```bash
animaworks-tool image_gen pipeline "1girl, ..." --anima-dir $ANIMAWORKS_ANIMA_DIR
```

### fullbody — Full-Body Standing Illustration
```bash
animaworks-tool image_gen fullbody "1girl, standing, ..."
```

### bustup — Bust-Up Portrait
```bash
animaworks-tool image_gen bustup reference.png
```

### chibi — Chibi Character
```bash
animaworks-tool image_gen chibi reference.png
```

### 3d_model — 3D Model Generation
```bash
animaworks-tool image_gen 3d image.png
```

## CLI Usage

```bash
animaworks-tool image_gen pipeline "1girl, ..." --anima-dir $ANIMAWORKS_ANIMA_DIR
animaworks-tool image_gen fullbody "1girl, standing, ..."
animaworks-tool image_gen bustup reference.png
animaworks-tool image_gen chibi reference.png
animaworks-tool image_gen 3d image.png
```

## Notes

- Recommended to run in the background with `animaworks-tool submit image_gen pipeline ...` due to long processing times
- Requires a NovelAI API key or fal.ai API key
- A Meshy API key is required for 3D generation

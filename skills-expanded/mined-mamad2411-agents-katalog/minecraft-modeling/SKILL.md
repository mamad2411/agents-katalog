---
name: minecraft-modeling
description: Create non-default Minecraft item and block models for the mod automation pipeline. Use only when a mod-spec declares custom model shapes beyond vanilla defaults such as item/generated, item/handheld, or block/cube_all, including Java model elements, multi-cube blocks, rotated elements, Blockbench-authored .bbmodel work, GeckoLib/entity model planning, screenshots, UV checks, and .minecraft-models.json handoff back to minecraft-mod-builder and minecraft-modding.
---

# Minecraft Modeling

## Role In The Pipeline

This is an optional phase between texture generation and modding implementation.

Call this skill only when the spec explicitly needs a non-default shape:

- `model.kind: "java_elements"`
- `model.kind: "custom_block"`
- `model.kind: "custom_item"`
- `model.kind: "blockbench"`
- `model.kind: "geckolib"`
- `model.kind: "entity"`

Do not call this skill for normal generated item icons, handheld tools, or simple cube blocks. Those are handled by `minecraft-mod-scaffold`.

## Input And Output Contract

Input:

- `mod-spec.json` or `<project>/.minecraft-mod-spec.json`
- scaffolded project root
- generated textures when available

Output:

- overwritten custom model JSON under `src/main/resources/assets/<modid>/models/...`
- optional `.bbmodel` work files under `<project>/models/blockbench/`
- `<project>/.minecraft-models.json`

## Scripted Java Model Generation

Use this for deterministic Java block/item JSON models from spec-defined cuboids:

```bash
python3 skills/minecraft-modeling/scripts/model_from_spec.py \
  --spec mod-spec.json \
  --project ./Copperworks
```

This script only acts on entries with non-default `model.kind`. It leaves normal items and cube blocks alone.

## Blockbench MCP Workflow

Use Blockbench MCP when the model needs visual authoring, screenshots, or iterative geometry work.

Confirmed useful MCP tools:

- `create_project`
- `place_cube`
- `modify_cube`
- `add_group`
- `remove_element`
- `list_outline`
- `create_texture`
- `apply_texture`
- `set_camera_angle`
- `capture_screenshot`

Recommended sequence:

1. Start or verify Blockbench is open with the MCP plugin running at `http://localhost:3000/bb-mcp`.
2. Create a `java_block` or appropriate project format if supported by current Blockbench.
3. Place low-poly cuboids with Minecraft 16-unit coordinates.
4. Apply generated textures from the mod project.
5. Capture a screenshot for review.
6. Export or save a `.bbmodel`/JSON artifact, then record it in `.minecraft-models.json`.

## Model Rules

- Stay within Minecraft Java model element limits: cuboids use `from` and `to` coordinates in a 16-unit block space.
- Keep custom block geometry conservative unless the mod also adds matching collision/voxel shape code.
- Use `texture: "#all"` or named texture variables consistently.
- For custom blocks, keep item model parent pointing to the block model unless the spec says otherwise.
- For entity or GeckoLib work, record the required renderer/model library tasks for `minecraft-modding`; do not pretend vanilla block model JSON is enough.

## References

- `references/spec-model-fields.md`: `model` field format for `mod-spec.json`.
- `references/blockbench-mcp.md`: Blockbench MCP usage notes.

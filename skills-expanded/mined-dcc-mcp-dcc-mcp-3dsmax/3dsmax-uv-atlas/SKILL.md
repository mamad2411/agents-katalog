---
name: 3dsmax-uv-atlas
description: >-
  Domain skill - inspect and mutate 3ds Max UV/map channels, apply projection
  and unwrap operations, detect UV overlaps, and prepare texture-atlas plans.
license: MIT
compatibility: "dcc-mcp-core 0.17+, 3ds Max 2024+"
metadata:
  dcc-mcp:
    dcc: 3dsmax
    version: "1.0.0"
    layer: domain
    stage: authoring
    search-hint: "3ds Max UV map channels unwrap projection pack normalize overlaps texture atlas bitmaps"
    tags: "3dsmax, uv, unwrap, texture, atlas, maps"
    tools: tools.yaml
    intent: "Inspect and mutate 3ds Max UV channels, apply projections, unwrap, pack, and detect overlaps."
    search_aliases: ["uv", "uv-atlas"]
    recall_context:
      app_type: "3dsmax"
      domain: "uv"
      workflow_stage: "authoring"
      task_category: "mutate"
    preconditions:
      - type: software
        name: "3ds Max"
        version: ">=2024"
    side_effects:
      creates: true
      modifies: true
      deletes: true
      exports: false
      imports: false
      file_output: false
      render: false
      targets: ["uv_channel", "scene_node", "modifier"]
    produces: ["uv_channel", "uv_shell", "uv_projection", "texture_atlas_plan"]
---

# 3ds Max UV and Atlas Skill

Inspect UV/map channels, apply host-native UV modifiers, and collect material
bitmap usage for texture-atlas planning through `pymxs`.

Analysis tools are read-only. Channel deletion and UV rewrite tools are marked
with explicit safety annotations so callers can distinguish reports from scene
changes.

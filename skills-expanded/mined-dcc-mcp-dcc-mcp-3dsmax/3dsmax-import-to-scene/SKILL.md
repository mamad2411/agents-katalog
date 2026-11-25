---
name: 3dsmax-import-to-scene
description: >-
  Domain skill - import asset descriptor contracts into the current Autodesk
  3ds Max scene. Use when converting an AssetDescriptor into scene nodes with
  variant selection, unit/axis handling, placement hints, and material mode
  overrides.
license: MIT
compatibility: "dcc-mcp-core 0.18.37+, 3ds Max 2024+"
metadata:
  dcc-mcp:
    dcc: 3dsmax
    version: "1.0.0"
    layer: domain
    stage: authoring
    search-hint: "3ds Max asset import contract ImportToSceneRequest ImportToSceneResult FBX OBJ 3DS placement material mode"
    tags: "3dsmax, import, asset-import, fbx, obj, placement, materials"
    tools: tools.yaml
    intent: "Import AssetDescriptor contracts into a 3ds Max scene as nodes."
    search_aliases: ["import to scene", "asset import", "scene import"]
    recall_context:
      app_type: "3dsmax"
      domain: "import"
      workflow_stage: "authoring"
      task_category: "mutate"
    preconditions:
      - type: software
        name: "3ds Max"
        version: ">=2024"
    side_effects:
      creates: true
      modifies: true
      deletes: false
      exports: false
      imports: true
      file_output: false
      render: false
      targets: ["scene_node"]
    produces: ["scene_node", "scene_layer"]
---

# 3ds Max Import To Scene

Import asset contract payloads into the current 3ds Max scene. The bundled
tool accepts a serialized `ImportToSceneRequest`, picks the best supported
variant, routes through the existing FBX or generic geometry import action,
and returns a serialized `ImportToSceneResult`.

Prefer FBX when available because the adapter can apply unit and axis hints
through the native FBX importer. OBJ and 3DS variants fall back to the generic
geometry import path and then apply best-effort placement and layer/material
overrides.

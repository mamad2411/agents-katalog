---
name: 3dsmax-transform
description: >-
  Domain skill - move nodes and set positions in the current Autodesk 3ds Max
  scene. Use when the user asks to place, move, offset, translate, or position
  objects. Not for creating new geometry.
license: MIT
compatibility: "dcc-mcp-core 0.17+, 3ds Max 2024+"
metadata:
  dcc-mcp:
    dcc: 3dsmax
    version: "1.0.0"
    layer: domain
    stage: authoring
    search-hint: "3ds Max transform position move translate place object node"
    tags: "3dsmax, transform, position, move, translate"
    tools: tools.yaml
    intent: "Move, position, translate, and offset 3ds Max scene nodes to exact or relative coordinates."
    search_aliases: ["transform", "transform"]
    recall_context:
      app_type: "3dsmax"
      domain: "transform"
      workflow_stage: "authoring"
      task_category: "mutate"
    preconditions:
      - type: software
        name: "3ds Max"
        version: ">=2024"
    side_effects:
      creates: false
      modifies: true
      deletes: false
      exports: false
      imports: false
      file_output: false
      render: false
      targets: ["scene_node", "transform"]
    produces: ["scene_node:transform", "node_position"]
---

# 3ds Max Transform Tools

Set absolute positions or apply relative offsets to existing scene nodes.
All tools touch the 3ds Max scene and run on the main thread.

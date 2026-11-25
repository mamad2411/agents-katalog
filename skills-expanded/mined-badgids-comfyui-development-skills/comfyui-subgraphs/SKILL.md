---
name: comfyui-subgraphs
description: Use when creating, modifying, validating, documenting, or packaging ComfyUI subgraphs or Subgraph Blueprints, or when composing workflows from reusable graph components.
metadata:
  version: "00.01.11"
---
# ComfyUI Subgraphs

## Sources

Use current/version-matched:

- workflow/subgraph documentation in `Comfy-Org/docs`;
- `Comfy-Org/Subgraph-Blueprints`;
- relevant `Comfy-Org/ComfyUI_frontend` implementation;
- workflow schema/source;
- live target node catalog.

## Procedure

1. Identify the target ComfyUI/frontend version.
2. Inspect the current subgraph/blueprint representation instead of assuming fields.
3. Verify every contained node against the live target when possible.
4. Define clear external inputs/outputs and avoid hidden install-specific assumptions.
5. Preserve stable identifiers when editing existing reusable components unless regeneration is required.
6. Validate expansion/use inside a representative workflow.
7. Check serialization and reload behavior in the target frontend.

Official blueprints are patterns, not a substitute for checking the current schema/runtime.

## Acceptance gate

Before calling a subgraph or blueprint complete:

- verify the representation against the target/current schema;
- validate contained nodes against the target when reachable;
- verify external inputs and outputs;
- test serialization and reload behavior when practical;
- use the subgraph inside a representative workflow;
- state clearly when frontend/runtime checks could not be run.


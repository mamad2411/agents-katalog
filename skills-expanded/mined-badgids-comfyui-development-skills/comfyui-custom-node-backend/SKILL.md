---
name: comfyui-custom-node-backend
description: Use when creating, modifying, migrating, debugging, or reviewing ComfyUI Python custom nodes or custom-node packs, including schemas, execution methods, registration, inputs/outputs, validation, caching/change detection, UI results, dependencies, and node-pack structure.
metadata:
  version: "00.01.11"
---
# ComfyUI Custom Node Backend

If the `comfyui-development` router skill is installed, apply its compatibility and source-authority policy. In all cases, read the relevant current custom-node documentation before implementation.

## Source set

Use as needed:

- the target ComfyUI checkout and live node catalog;
- `Comfy-Org/docs` custom-node documentation;
- `Comfy-Org/ComfyUI` bundled/current node examples and `comfy_api` implementation;
- `Comfy-Org/cookiecutter-comfy-extension` for current project/package conventions;
- `Comfy-Org/pyisolate` when dependency conflicts, isolated extension environments, subprocess/RPC isolation, sandboxing, or cross-process tensor sharing are relevant;
- target pack source and tests;
- official test/QA tools.

## First classify the work

Determine whether this is:

- a new node in a new pack;
- a new node in an existing pack;
- a bug fix;
- a compatibility fix;
- an API-generation migration;
- a packaging/import problem;
- a backend half of a frontend-connected extension.

Do not turn a small bug fix into a migration unless migration is necessary.

## Current official agent guidance

If the target workflow uses `comfy-cli` or its installed agent skills, inspect the current/version-matched `comfy-cli` skill set before relying on CLI-specific custom-node advice. Its bundled custom-node guidance is useful operational synthesis, but verify node API contracts against the target ComfyUI source/docs and live registration. Do not copy that upstream skill into this pack.

## Node-definition rule

Do not assume the current or legacy custom-node definition style from memory.

For a new node, inspect current official guidance and target compatibility requirements. For an existing node, identify the style already used by the project and whether its supported ComfyUI range requires it.

If using a versioned `comfy_api`, inspect which versions actually exist in the target and what the official docs call stable/development before choosing an import.

## Implementation procedure

1. Inspect the repository structure, dependency metadata, and existing nodes.
2. Identify the target ComfyUI/API generation.
3. Search current official source for a comparable built-in node or datatype.
4. Verify input/output type semantics from current target source.
5. Implement node schema/registration using the target's real contract.
6. Keep execution logic independent of UI assumptions where possible.
7. Add validation/change-detection behavior only when it is required and verify its current contract.
8. If dependency isolation is part of the design, inspect the current `pyisolate` contract and the target ComfyUI integration before inventing a custom isolation mechanism. Do not assume the target uses pyisolate merely because it is an official project.
9. If frontend behavior is needed, also use the `comfyui-frontend-extension` skill rather than guessing JS hooks.
10. Add focused tests.
11. Load the node in ComfyUI and confirm it registers.
12. Inspect the live node definition and compare it with the intended public interface.
13. Run a minimal representative workflow when feasible.

## Registration gate

A Python file importing successfully is not sufficient. Confirm the node pack is actually discovered and the intended nodes appear in the running target.

## Compatibility gate

When supporting multiple ComfyUI generations, make compatibility behavior explicit and testable. Do not use broad exception swallowing to make imports appear compatible.

## Packaging handoff

For Registry/Manager packaging or publishing, also use the `comfyui-packaging-and-registry` skill.

## Acceptance gate

Before calling the node or pack complete:

- confirm the intended node registration contract against the target ComfyUI generation;
- pass focused tests for the changed behavior;
- load the pack in the target when practical and confirm the intended nodes register;
- compare the exposed live node interface with the intended inputs and outputs;
- run a minimal representative workflow when practical;
- state clearly when a live registration or workflow check could not be run.


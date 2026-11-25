---
name: comfyui-workflows
description: Use when creating, modifying, converting, composing, templating, or programmatically generating ComfyUI workflows in frontend/editor format or API/execution format, especially when custom nodes or install-specific model options are involved.
metadata:
  version: "00.01.11"
---
# ComfyUI Workflows

A workflow is not valid merely because its JSON parses.

## First identify the artifact

Determine whether the user needs:

- frontend/editor workflow JSON;
- API/execution graph;
- workflow template/package data;
- subgraph/blueprint content;
- a conversion between representations.

Do not mix these formats.

## Authority order

1. live target node catalog for installed node definitions and options;
2. current/version-matched workflow schema in official docs;
3. official templates/examples for wiring patterns;
4. target custom-node source when a third-party node requires clarification.

## Current CLI guidance

When the task actually uses `comfy-cli`, inspect its current/version-matched help and bundled agent guidance before choosing CLI workflow commands or construction mechanisms. Treat that guidance as the CLI's operational surface, not as a replacement for the live target node catalog or workflow schema. Do not vendor the CLI skill text into this pack.

## Required workflow construction loop

1. Establish the target ComfyUI installation/version.
2. Query live node definitions when the target is reachable.
3. Confirm every required node class exists.
4. Confirm input names/types, output slots/types, enum choices, and resource names from target data.
5. Search official templates/examples for a current comparable graph.
6. Build the requested representation using the current schema.
7. Preserve unrelated metadata/layout when editing an existing workflow.
8. Validate against the target using the `comfyui-workflow-validation` skill.
9. Fix all deterministic validation errors before returning the workflow.

## Hard prohibitions

Do not invent:

- node types;
- socket names;
- output slot indexes;
- widget order;
- combo values;
- model filenames;
- custom-node package names.

Do not assume a workflow downloaded from the internet is compatible with the target merely because it is official or recent.

## When the target is unavailable

You may construct a provisional workflow from current authoritative sources, but state that live compatibility could not be checked. Keep install-specific values easy to identify and replace.

## Template use

Treat official templates as examples plus authored metadata. Validate them against the actual install before execution.

## Execution

Do not run an expensive workflow solely to prove structural validity unless the user asked for execution or the test cost is known to be acceptable. Prefer preflight validation first.

## Acceptance gate

Before returning a workflow as ready:

- identify the requested workflow representation;
- verify every required node and install-specific option from the target when reachable;
- validate the workflow against the current/version-matched schema and live node catalog;
- fix deterministic validation errors;
- load, queue, or execute a minimal representative run against the target when practical;
- preserve unrelated layout and metadata when editing an existing workflow;
- label the workflow provisional when live target validation was not possible.


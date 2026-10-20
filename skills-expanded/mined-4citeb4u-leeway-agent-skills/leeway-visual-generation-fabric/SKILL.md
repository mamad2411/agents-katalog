---
name: leeway-visual-generation-fabric
description: Governed Agent Lee visual creation and inspection across image generation, vision review, transparent cutouts, image-to-3D conversion, and downstream asset workflows. Selects authorized providers without making SDXL, a cloud API, one GPU, or one host a universal requirement.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards > provider policy
  mode: portable-visual-capability-fabric
  mcp_tools: visual_provider_status, visual_generate_image, visual_inspect_image, visual_convert_image_to_3d
---

# LeeWay Visual Generation Fabric

## Purpose

Give Agent Lee one portable route for visual work while preserving honest provider and evidence boundaries.

`Creator intent → visual brief → provider selection → generation → artifact verification → vision review → optional refinement/3D conversion → receipt`

## Capability identities

Treat these as separate capabilities:

- `visual.image.generate`
- `visual.image.inspect`
- `visual.image.cutout`
- `visual.image.edit`
- `visual.image.to_3d`
- `visual.asset.integrate`

A provider can implement one or more identities. Provider presence does not imply all six.

## Provider selection

Select by task requirements, authorization, privacy, cost, model availability, target resolution, latency and platform health. Valid providers may include:

- a LeeWay local creation kernel;
- a recovered SDXL-Lightning or Tiny-SD adapter;
- an authorized cloud image service;
- a host-native image generator;
- a TripoSR or Blender adapter for 3D work;
- an authorized vision model for inspection.

Bind logical capabilities through configuration. Never make a historical drive path, Docker image name, model vendor, CUDA device, or URL part of Agent Lee identity.

## Execution states

Use these distinctions:

- `CONTRACT_PORTABLE` — the skill/tool contract is host and provider agnostic.
- `ADAPTER_IMPLEMENTED` — provider code exists.
- `ADAPTER_CONFIGURED` — this runtime has a bounded provider binding.
- `ADAPTER_EXECUTED_UNVERIFIED` — a provider reported an artifact/result.
- `PLATFORM_TESTED` — the adapter executed on a named platform.
- `VERIFIED` — artifact existence, media type, dimensions/hash and task acceptance checks passed.

Never promote source code, an image-model cache, a container image, a prior receipt, or a provider `200` response directly to `VERIFIED`.

## Image generation

Before generation, normalize:

- subject and composition;
- required and forbidden elements;
- aspect ratio and output size;
- reference-image authority;
- style constraints and rights/provenance;
- deterministic seed when reproducibility matters;
- target artifact format and destination.

After generation, verify the returned artifact exists, is a decodable image, has nonzero dimensions and receives a SHA-256. For task-specific quality, apply a rubric with observable criteria; do not use a provider's self-description as proof.

## Vision review

Vision models may judge semantic criteria, but file state remains authoritative for existence, type, hash and dimensions. Preserve the original prompt, final provider prompt, model/provider identity and review rubric in the receipt.

## Image-to-3D

Distinguish a relief/card conversion from a true reconstructed mesh. Record topology, texture, format, geometry limits, hidden-surface uncertainty and whether rigging/animation exist. A generated OBJ or GLB is not automatically production-ready.

## MCP adapter contract

The canonical Skills MCP server exposes:

- `visual_provider_status`
- `visual_generate_image`
- `visual_inspect_image`
- `visual_convert_image_to_3d`

Provider bindings use logical environment configuration. Loopback providers may be uncredentialed when they are reachable only on the host loopback interface. Non-loopback providers require HTTPS plus an authorization token. Veritas remains separate from the provider call.

## Recovered provenance

Repository: `https://github.com/4citeB4U/leeway-ecosystemv2.14`

Branch: `source-baseline-20260803`

Commit: `4c1181630f65d041f3a8a877a8c5166ac51f4b40`

Implemented source anchors:

- `Cerebral/services/agent-lee-sdxl-lightning-image-lane/app/main.py`
- `Cerebral/services/agent-lee-tiny-sd-image-lane/app/main.py`
- `Cerebral/services/agent-lee-telegram-vision-lane/app/main.py`
- `Cerebral/services/agent-lee-image-to-3d-lane/app/main.py`
- `Cerebral/services/agent-lee-image-to-3d-pattern-lane/app/main.py`
- `agent-lee-coding-mode/creation-kernel/app/main.py`

Those sources are recovery evidence, not universal runtime dependencies. Current classification, live observations and failed qualification attempts belong in `config/ecosystem-capability-recovery-v1.json` and its receipt.

## Handoff

Use Tool Gateway for provider execution, Veritas for acceptance and Receipt Authority for evidence. Feed stable improvements to Learning Ledger only after verification.

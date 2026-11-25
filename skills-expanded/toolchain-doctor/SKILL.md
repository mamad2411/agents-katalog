---
name: toolchain-doctor
description: "Inspect the local game-development toolchain read-only, identify compatibility gaps, and prepare one reversible setup proposal without installing or changing anything."
---

# Toolchain Doctor

## Outcome

Build a trustworthy, read-only inventory before any setup decision.

## Required inputs

- project root
- target engine or platform if known
- commercial-use intent and download budget

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Detect Windows, macOS, Linux, architecture, native-versus-WSL execution, disk space, and network constraints.
2. Inspect project markers and installed Unity, Godot, Unreal, Blender, Aseprite, Pixelorama, and Tiled versions without launching them.
3. Inspect Python, Node.js, package managers, Git, gh, existing MCP declarations, credential variable names, GPU backend, and reported VRAM without reading secret values.
4. Compare the detected environment with pack descriptors and catalog constraints.
5. Return one transaction proposal with exact pins, licenses, permissions, downloads, conflicts, backups, rollback operations, expiry, and digest.

## Expected artifacts

- environment inventory
- compatibility matrix
- single proposed transaction
- no-change attestation

## Workflow-specific gates

- Never read credential values; report only whether named variables or authenticated clients appear available.
- Never install, enable, launch, or reconfigure a tool during diagnosis.
- If native detection is incomplete, mark evidence unknown instead of guessing.

## Production completion gate

Before recommending production use, complete and report all seven gates:

1. Rights, consent, code/model/dataset/output license, and generation-provenance checks.
2. Technical format, naming, scale, color, metadata, and target-import validation.
3. Visual and temporal consistency review across representative views and states.
4. Runtime memory, frame-time, draw-call, streaming, and asset-budget checks.
5. Playability and interaction smoke tests in the target runtime.
6. Screenshot, capture, diff, or artifact-regression evidence with reproducible settings.
7. Human approval before replacing source assets or promoting generated output.

Unknown rights, missing consent, unsupported hardware, conflicting host adapters,
or failed quality gates block production promotion. Preserve originals and make
fallbacks explicit.

---
name: engine-automation
description: "Plan and execute approved Unity, Godot, Unreal, Blender, or pixel-editor automation through one compatible host adapter at a time."
---

# Engine Automation

## Outcome

Route an approved operation to the correct editor adapter while preserving user control and rollback.

## Required inputs

- host application and project
- desired operation
- selected pack, exact upstream pin, permissions, and rollback expectations

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Run read-only host and project detection and inventory existing MCP configurations.
2. Refuse ambiguous host selection or multiple active servers for the same application.
3. Prepare a transaction with exact commands, files, process and network permissions, health checks, backups, rollback, expiry, and digest.
4. Show the plan and wait for explicit confirmation of its digest.
5. After confirmation, apply only the listed actions, run health checks, and stop on the first divergence.
6. Record the resulting lock state and tested rollback path.

## Expected artifacts

- approved transaction
- backup inventory
- health-check result
- lock update
- rollback report

## Workflow-specific gates

- Never install, enable, launch, configure, or control an editor implicitly.
- Only one MCP server per host application may be active.
- A digest mismatch, expired plan, changed environment, or failed backup invalidates apply and requires a new plan.

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

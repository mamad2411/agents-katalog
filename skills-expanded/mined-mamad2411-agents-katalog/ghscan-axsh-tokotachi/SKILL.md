---
apiVersion: agent.meta/v1
kind: capability
id: __far-knowledge-prompt-deploy-drift-detection
title: "Far-Knowledge: Deploy Drift Detection and Entity YAML Serialization"
description: >-
  Cross-cutting knowledge about the deploy/update drift detection mechanism
  and Entity custom YAML serialization for resolved manifest roundtrips.
user_visible: false
manual_only: false
status: current
body: inline
---

# Deploy Drift Detection and Entity YAML Serialization

## Entity Custom YAML Serialization

`Entity` struct in `features/tt/internal/prompt/manifest/types.go` has a `Raw` map field (`yaml:"-"`) that holds custom properties like `body`, `activation`, etc. By default, this field is excluded from YAML serialization.

Custom `MarshalYAML()` and `UnmarshalYAML()` methods are implemented to:
- **Marshal**: Merge `Raw` map properties into the serialized output alongside struct fields
- **Unmarshal**: Use an alias type to prevent infinite recursion, then collect unknown fields into the `Raw` map

This is critical for resolved manifest roundtrips (`manifest.resolved.yaml`). Without it, the resolved manifest loses custom properties, causing drift detection to always report differences.

## Deploy and Update Drift Detection

The `CheckDrift()` helper function in `features/tt/internal/prompt/compiler/deploy.go` provides a shared mechanism for both `Deploy()` and `Update()` to verify deployed files match expectations.

Flow:
1. Read and parse the resolved manifest (`manifest.resolved.yaml`)
2. Initialize the appropriate emitter for the target (antigravity, cursor, claude-code, codex)
3. Call `emitter.Check(resolved, buildDir)` to compare actual files against expected state
4. If `Check()` returns `false` (drift detected) or errors, force redeployment

Key design decisions:
- Parse failure of resolved manifest triggers redeployment (safe fallback)
- Drift check runs only when source hash matches (optimization)
- Both `Deploy()` and `Update()` use the same `CheckDrift()` to avoid logic duplication

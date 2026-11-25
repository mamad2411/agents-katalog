---
name: steady-state-sidecar-sync
description: "Refresh derived sidecar caches even when no primary installs changed so ephemeral runtimes still receive the mirrored state they need."
metadata:
  author: ychampion
---

# SKILL: Steady-State Sidecar Sync
**Domain:** extensions-mcp
**Trigger:** Use when a derived cache or mirror can disappear between runs even though the primary installation state did not change this time.
**Source Pattern:** Distilled from reviewed authoritative-state to sidecar-cache synchronization flows.

## Core Method
Rebuild sidecar or mirror caches from authoritative state after reconciliation settles, even when the primary changed signal is false. Ephemeral environments often lose derived artifacts while retaining the main installed set, so gating sidecar sync only on new installs leaves fresh processes under-provisioned. Keep the sync idempotent and conceptually separate from the main change signal.

## Key Rules
- Treat the authoritative installed state as the source of truth for rebuilding sidecars.
- Do not gate sidecar maintenance solely on new installs from the current run.
- Keep sidecar sync idempotent so it is safe on every startup.

## Example Application
If worker nodes derive a local metadata mirror from the installed extension registry, rebuild that mirror on each boot even when no extension was newly installed.

## Anti-Patterns (What NOT to do)
- Do not assume unchanged primary state means derived caches are still present.
- Do not couple quiet maintenance syncs to user-visible change notifications by default.
- Do not rebuild sidecars before the primary materialized state is settled.

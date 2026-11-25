---
name: nixos-guard
description: Enforces AGENTS.md safety rules for NixOS cluster management via pi extension.
---

# NixOS Guard

Enforces AGENTS.md safety rules via pi extension at `~/.pi/agent/extensions/nixos-guard/`.

## What's Enforced

| Rule | Trigger | Action |
|------|---------|--------|
| hardware-configuration.nix | edit/write to that file | Block with confirmation |
| mkOptionDefault required | Direct `=` assignment to mergeable list attrs | Warn + block |
| No :latest container tags | `image: ... :latest` in .nix/.yaml | Block with confirmation |
| Zephyr scheduling | Non-infra workload targeting zephyr in K8s manifests | Warn + block |
| kebab-case filenames | New .nix files with uppercase or underscores | Notify with suggestion |
| Multi-node deploy safety | `just deploy` / `colmena apply` without specific host | Confirm + require check |
| Pre-deploy flake check | Deploy/switch without prior `just check` | Notify with reminder |

## Commands

- `/nixos-check` — Scan all NixOS configs for rule violations
- `/nixos-flake-check` — Run `nix flake check --no-build`

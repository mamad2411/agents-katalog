---
name: opentofu-1-drift-investigation
description: Investigates OpenTofu 1.x infrastructure drift and reconciles manual or out-of-band changes. Use when plans show unexpected changes, resources were edited outside IaC, or state/configuration no longer matches reality.
license: MIT
compatibility: Requires OpenTofu 1.x and provider credentials for live drift plans. Do not run apply, destroy, import, or state mutation without explicit approval.
---

# OpenTofu 1.x Drift Investigation Skill

This skill helps agents investigate and resolve drift without normalizing unsafe manual changes or mutating state prematurely.

## Use This Skill When

- A plan shows unexpected updates, replacements, or destroys.
- Infrastructure was changed manually in a portal, console, or ad hoc CLI.
- State, configuration, or remote resources appear inconsistent.
- A resource may need import, moved blocks, or configuration repair.
- The user asks whether deployed infrastructure matches OpenTofu code.

## Safety Boundaries

- Do not run `tofu apply`, `tofu destroy`, `tofu import`, or `tofu state *` without explicit user approval.
- Do not hide unexplained drift with `ignore_changes`.
- Treat drift plans and state data as sensitive.
- Separate investigation from remediation: first understand, then propose, then review a plan.

## Workflow

- `workflows/drift-investigation-workflow.md`: Use for structured drift triage, root cause analysis, and remediation planning.

## Resources

- `resources/drift-investigation-checklist.md`: Checklist for drift symptoms, evidence, likely causes, and remediation choices.

## Examples

- `examples/drift-finding-template.md`: Template for documenting drift findings and remediation options.

---
name: sync-editorconfig
description: Use when creating, normalizing, or updating a workspace .editorconfig and validating C# using/type-file policy compliance on demand.
---

# Sync EditorConfig

## Specialization

This skill is specialized for the workflow described in this file and should remain narrowly bounded to that responsibility.

It should not absorb adjacent planning, execution, or review responsibilities that belong to other assets.

## Overview

Use this skill to create or refresh a baseline `.editorconfig` in a target repository and run a deterministic policy validation for C# projects.

## Trigger Conditions

- A workspace is missing `.editorconfig`.
- EditorConfig rules have drifted from current C# standards.
- You need a repeatable check that enforces `Usings.cs` and single top-level type rules.

## Quick Commands

```powershell
# Create or update .editorconfig and then validate C# policy
pwsh ./.github/skills/sync-editorconfig/references/scripts/Invoke-EditorConfigSync.ps1
```

```powershell
# Validate only (no file write)
pwsh ./.github/skills/sync-editorconfig/references/scripts/Invoke-EditorConfigSync.ps1 -ValidateOnly
```

```powershell
# Target a different workspace root
pwsh ./.github/skills/sync-editorconfig/references/scripts/Invoke-EditorConfigSync.ps1 -WorkspaceRoot "C:/src/repo"
```

## What It Enforces

- Ensures a root `.editorconfig` exists with core C# analyzer settings.
- Uses repository-level `Directory.Build.targets` to bootstrap `Usings.cs` when a C# project grows beyond one `*.cs` file.
- Ensures projects with more than one `*.cs` file contain `Usings.cs`.
- Fails when non-`Usings.cs` files contain import `using` directives.
- Fails when a file appears to host more than one top-level type (nested types allowed).
- Fails when Minimal API route mappings are declared inline in `Program.cs`.

## Notes

- The script exits non-zero on policy violations so it can be used in CI.
- Analyzer-based enforcement still depends on analyzers being present in the project.
- In this customization repository, these artifacts are reference behavior for external .NET repositories; they are not required at this workspace root.

## Inputs

- User request context and target scope for this skill invocation.

## Required Outputs

- A concrete, workspace-applicable result aligned with this skill purpose.

## Workflow

1. Gather required context and constraints from the workspace and user request.
2. Execute the skill-specific steps and produce the required artifacts or decisions.
3. Validate outputs for completeness and consistency with active workspace instructions.


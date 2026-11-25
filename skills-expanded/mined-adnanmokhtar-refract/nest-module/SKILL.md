---
name: nest-module
description: Scaffolds one NestJS feature module with its controller, service, entity and spec.
kind: skill
allowed-tools: [Read, Grep, Glob, Edit, Write]
pack: backend
---

<!-- project-specific:start -->
## Project-specific (auto-generated, regenerate with `/setup-project --refine`)

> Auto-populated by `scripts/apply-anchors.sh` from `.claude/codebase-profile.md`. Round-one floor — `/setup-project --refine` deepens shallow blocks based on `compute-anchor-density` scoring.
>
> - **Architecture**: one module per folder under the API source tree.

# Skill: nest-module

Create a module folder with four files: module, controller, service and spec. Register the module in the root
module. Keep the controller thin.

## Steps

1. Create the folder and the module class.
2. Add the controller with one route.
3. Add the service and its spec.
4. Register the module.

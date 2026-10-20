---
name: opentofu-1-module-design
description: Designs and refactors OpenTofu 1.x root modules and reusable modules. Use when creating module interfaces, variables, outputs, provider constraints, examples, tests, or project structure.
license: MIT
compatibility: Requires OpenTofu 1.x for command execution; instructions avoid minor-specific features unless the repository declares a minimum minor version.
---

# OpenTofu 1.x Module Design Skill

This skill helps agents design and maintain OpenTofu 1.x root modules and reusable modules that are safe, reviewable, version-compatible, and easy to operate.

## Use This Skill When

- Creating a new OpenTofu root module.
- Designing or refactoring a reusable module.
- Adding variables, outputs, validations, provider constraints, examples, tests, or module documentation.
- Separating environments, state boundaries, credentials, or provider aliases.
- Reviewing module interface quality.

## Do Not Use This Skill For

- Provider-specific cloud architecture without a matching provider/cloud plugin.
- Application-specific environment taxonomy or domain architecture.
- Running `tofu apply`, `tofu destroy`, or state mutation commands.
- Terraform CLI workflows except explicit migration review.

## Core Guidance

1. Inspect existing repository conventions before adding new folders.
2. Keep root modules separate from reusable modules.
3. Use the `tofu` CLI, while keeping OpenTofu language settings in `terraform { ... }` blocks.
4. Keep examples small and runnable.
5. Prefer explicit inputs, typed variables, validation, and sensitive outputs.
6. Avoid hard-coded environment and account identifiers in reusable modules.
7. Commit lock files for root modules unless repository policy differs.
8. Keep environment separation generic and enforceable: separate state, credentials, backend keys, variables, and blast radius.

## Workflows

- `workflows/new-root-module-workflow.md`: Use when creating a new root module or standardizing an existing one.
- `workflows/reusable-module-workflow.md`: Use when creating or refactoring a reusable module.

## Resources

- `resources/project-structure-checklist.md`: Checklist for root modules, reusable modules, tests, examples, and lock files.
- `resources/module-interface-template.md`: Template for variables, outputs, validations, and examples.

## Examples

- `examples/root-module-skeleton.md`: Minimal root module layout and file examples.
- `examples/reusable-module-skeleton.md`: Minimal reusable module layout and interface examples.

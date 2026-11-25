---
name: terraform-module-design
description: Designs reusable Terraform modules with clear inputs and outputs, a safe state layout, and a plan review before anything is applied.
---

# Terraform module design

A module is an interface. Design the interface before the resources.

## Steps

1. State the module's purpose in one sentence and list who calls it. If you cannot, it is two modules.
2. Define inputs: typed variables with `description`, `validation` blocks for formats and ranges, and defaults only where one is safe. Prefer a few objects over many loose strings. Leave out arguments no caller needs.
3. Define outputs for every ID, ARN or endpoint another module could need, each with a `description`. Mark credentials `sensitive = true`.
4. Structure files as `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf` (with `required_version` and pinned provider ranges), and an `examples/` directory that is applied in CI.
5. Use `for_each` over a map, not `count` over a list, so removing one item does not recreate the rest. Use `moved` blocks when renaming.
6. Keep state small: one state per environment and per blast radius, in a remote backend with locking. Modules never configure a backend or a provider.
7. Run `terraform fmt -check`, `terraform validate`, and `terraform plan`. Read the plan line by line.

## Rules

- Never run `terraform apply` or `destroy` unless the user asks for it in this conversation.
- Flag every `destroy` or `replace` in the plan, with the attribute that forces it.

## Report

Module interface (inputs and outputs), state layout, and the plan summary: added, changed and destroyed counts.

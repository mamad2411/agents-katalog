---
name: pi-package-creator
license: MIT
description: Create, refactor, and validate Pi packages. Use when an agent needs to scaffold a new Pi package, choose the correct Pi package surface, wire `package.json` `pi` manifests, or prove a Pi package works through the real `pi install` path.
---

# Pi Package Creator

## Overview

Use this skill to design and ship Pi packages with a narrow public promise and a
real install/validation loop. Focus on package surface, installability, and
dogfooding, not just folder scaffolding.

Read:
- `references/surface-design.md` before deciding what the package should ship
- `references/validation.md` before calling the package done

For advanced surface-specific details, inspect the installed Pi docs only after
you have a resolved local docs path. Use the same `pi` binary you will validate
with when checking `pi --help` for CLI flags. Do not guess where Pi's installed
package tree lives on disk.

If `skill-creator` is available and the package includes multiple skills or a
skill with bundled resources beyond a single `SKILL.md`, use it for the
internal skill design. Otherwise keep the work inside this skill and focus on
package boundary, manifest, install flow, README, and proof.

## Workflow

### 1. Lock the package promise

Start by answering:
- What is the package for in one sentence?
- What should a user be able to install and use immediately?
- Which Pi resources does that require: `extensions`, `skills`, `prompts`, or
  `themes`?
- What should explicitly stay out of scope for `v1`?

Prefer one narrow package promise over a kitchen-sink bundle.

### 2. Choose the smallest package surface

Pick only the resource types that the package actually needs:
- `extensions` for commands, hooks, tools, ambient behavior, UI, or plumbing
- `skills` for reusable workflows and domain instructions
- `prompts` for reusable prompt templates
- `themes` for visual presentation only

Do not add a second surface without a real user-facing reason.

### 3. Build the package shape

Create or tighten:
- `package.json`
- only the resource directories that are actually used
- a README that explains what the package is, how to install it, how to prove
  it works, and what its limits are

For `package.json`:
- include `name`, `version`, `license`
- include `keywords` with `pi-package`
- use the exact `pi` manifest keys Pi supports: `extensions`, `skills`,
  `prompts`, `themes`
- point manifest entries at relative paths
- ship only needed files

Keep public metadata honest:
- if the package is Pi-only, say so
- if install is local-path-only today, say so
- do not point homepage/repository/bugs at URLs that are not ready

### 4. Validate with the package manager, not just direct paths

The release gate is not "the files look right." The gate is "Pi can install and
use this package."

Always validate in this order:
1. repo-local tests/build checks
2. install into a temporary Pi agent dir
3. confirm the package is listed
4. smoke the actual public surface
5. dogfood in a real repo only after the temp install works

Use the validation flow in `references/validation.md`.

Do not rely only on `--extension`, `--skill`, or ad hoc file loading. Those are
fine for inner-loop debugging of one component, but the package promise is
still `pi install`.

- Keep package docs and package behavior in sync.
- Use scratch repos or temp agent dirs before touching real agent state.
- If the package mutates repo files, prove it in a scratch repo first.
- If the package is still private or unpublished, avoid public-install copy that
  implies otherwise.

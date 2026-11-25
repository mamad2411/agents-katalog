---
name: ci-testing
description: Create, extend, review, and repair RISC OS CI pipelines, especially GitHub Actions and GitLab CI files, optional matching `.robuild.yaml` or `.robuild.yml` files for build-service jobs, 32-bit and 64-bit builds, build-service testing, artifact packaging, and draft releases. Use when Codex needs to work on `.github/workflows/*.yml`, `.gitlab-ci.yml`, `example-ci.yml`, `.robuild.yaml`, `.robuild.yml`, `riscos-project create-ci`, build.riscos.online integration, or RISC OS packaging/testing patterns for AIF, RM, and library-export projects.
license: MIT
---

# CI Testing

## Overview

Use this skill to create or update CI workflows for RISC OS repositories.
Keep the workflow aligned with the repository's `Makefile`, `VersionNum`, exported artifacts, and any `.robuild.yaml` or `.robuild.yml` submitted to build.riscos.online. Prefer the `.yaml` spelling, but both file names are valid.

## Workflow

1. Inspect the repository's existing build shape first.
2. Decide whether the repository is:
   - a library export that should package exports rather than run a produced binary;
   - an AIF command/application that can be executed in CI;
   - an RM/module that can be loaded and exercised in CI.
3. Check whether `riscos-project create-ci` should be the starting point.
4. Decide whether the repository should keep the generated build-service shape or switch to direct 32-bit and 64-bit container builds.
5. Choose the smallest template that fits, then adapt filenames, commands, and archive names.
6. Keep the workflow and `.robuild.yaml` or `.robuild.yml` in sync when a build-service job is still used.
7. If the repository builds PRM-in-XML documentation, also use the `writing-prminxml` skill and its `references/github-ci.md`.

## Starting Point

When a repository does not yet have CI files, start with:

```bash
riscos-project create-ci
```

Treat that as the normal baseline generator for both `.github/workflows/ci.yml` and `.gitlab-ci.yml`, not the finished answer.
After generation:

- review the generated `.github/workflows/*.yml`;
- review the generated `.gitlab-ci.yml` when present;
- review the generated `.robuild.yaml` or `.robuild.yml`;
- extend to 64-bit builds when needed;
- add artifact packaging and release handling;
- add build-service execution tests for AIF or RM outputs when the project produces runnable binaries.

## Pattern Selection

Read only the reference file you need:

- Generic pattern notes derived from local example CI files:
  [references/repository-patterns.md](references/repository-patterns.md)
- Template choices and how to adapt them:
  [references/workflow-templates.md](references/workflow-templates.md)

## Assets

Use the bundled assets as starting points:

- `assets/library-export-ci.yml`
  For repositories that export a library and package exported files.
- `assets/library-export.robuild.yaml`
  Matching build-service configuration for a library export.
- `assets/binary-build-test-release-ci.yml`
  Build, test, package, and draft-release template for AIF or RM outputs.
- `assets/aif-test.robuild.yaml`
  Matching build-service test file for absolute binaries.
- `assets/rm-test.robuild.yaml`
  Matching build-service test file for modules.

These files are intentionally templated with `{{PLACEHOLDER}}` values so they can be copied and then filled in mechanically.

## Core Rules

- Keep 32-bit and 64-bit build steps explicit when both are supported.
- Use the repository's existing `VersionNum` convention when present; for normal RISC OS `VersionNum` files prefer `Module_FullVersion` rather than scraping looser `MajorVersion` text. Fall back to the git hash only when no usable version define exists.
- GitHub Actions `run:` steps default to `/bin/sh` in many environments. Use POSIX shell syntax such as `[ -f file ]` unless the workflow explicitly sets `shell: bash`.
- GitLab CI `script:` entries commonly run under a POSIX shell as well. Do not assume Bash-only syntax there unless the job explicitly selects Bash.
- Name uploaded artifacts and release archives consistently.
- For library exports, package the export directory or files. Do not invent a runtime test that cannot validate library behaviour.
- For AIF or RM outputs, prefer a separate test job that downloads the built artifact and exercises it through build.riscos.online with a focused `.robuild.yaml`.
- Keep `.robuild.yaml` or `.robuild.yml` narrowly scoped to the commands needed on RISC OS. Prefer `.yaml`, but support `.yml` when that is what the repository already uses. Keep host-side packaging and release logic in the CI system.
- If documentation output is part of CI, do not hand-roll PRM-in-XML rendering steps. Use the `writing-prminxml` skill and its GitHub CI guidance.

## Validation

After editing CI files:

- read back the workflow and `.robuild.yaml` or `.robuild.yml` for placeholder drift or mismatched artifact names;
- if practical, run YAML validation or repository linting;
- confirm every file referenced by the workflow is actually produced earlier in the pipeline;
- confirm every file referenced in `.robuild.yaml` or `.robuild.yml` will exist inside the uploaded source archive;
- if documentation jobs were added, confirm they follow the `writing-prminxml` GitHub CI pattern.

## Related Skills

- Use `creating-github-actions` for general GitHub Actions structure and hygiene.
- Use `writing-prminxml` when the CI pipeline must build PRM-in-XML output, especially its `references/github-ci.md`.

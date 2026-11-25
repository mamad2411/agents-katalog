---
name: cli-forge-distribute
description: "Distribute stage for the cli-forge skill family: guide optional npm publication for the shipped CLI command without replacing the target repository's repo-native release flow."
---

# cli-forge Distribute

Use this stage when a generated CLI skill repository needs an optional npm
distribution path for the shipped CLI command.

This stage does not publish the current `cli-forge` skill-family repository,
and it does not replace the target repository's repo-native GitHub Release
workflow. Its job is to guide or execute npm publication for the shipped CLI
command **after** the target repository's release contract is clear.

## Purpose

Manage the optional npm package set (one coordinating package + platform
packages) that distributes the shipped CLI command.

This stage strictly separates the **primary release channel** (repo-native
GitHub Release, handled by the Publish stage) from the **secondary distribution
channel** (npm, handled here). It ensures the npm package versions never drift
from the authoritative released tag.

## Canonical References

- [`./instructions/release/npm-publish-runbook.md`](./instructions/release/npm-publish-runbook.md)
- [`./planning-brief.md`](./planning-brief.md)
- [`../planning-brief.md`](../planning-brief.md)
- [`../contracts/validation-report.yml.tpl`](../contracts/validation-report.yml.tpl)

## Entry Gate

| #   | Check                                                        | Source                  |
| --- | ------------------------------------------------------------ | ----------------------- |
| 1   | `validation-report.yml` exists and `result == compliant`     | Validate stage          |
| 2   | Repo-native release path is explicit                         | Publish stage (or user) |
| 3   | Authoritative version (tag + release evidence) is determined | Target repository       |
| 4   | Coordinating package and platform package names are decided  | User / Plan             |
| 5   | Package ownership / permissions are confirmed                | User                    |

## Required Inputs

- Intended npm publication mode: `report_only`, `dry_run`, or `live_publish`
- The current, compliant validation status
- The target repository path
- The authoritative released skill version (sourced from the repo-native tag)
- The coordinating package name
- The full set of required platform package names and targets

## Workflow

1. Read [`./planning-brief.md`](./planning-brief.md) to lock the npm
   publication contract.
2. Verify that validation is current (`validation-report.yml`) and that the
   target repository context is explicit. If not, route back to Validate.
3. Confirm the authoritative released skill version using the target repository's
   released tag and matching release evidence. This version is the strict
   source of truth for the entire npm package set.
4. Review the package matrix:
   - One coordinating package (the user-facing install target)
   - One platform-specific package per supported target
   - Review package ownership and permissions
5. Block publication if the version chain diverges:
   - Released skill version from repo-native tag MUST EQUAL
   - Matching release-evidence version MUST EQUAL
   - Coordinating package version MUST EQUAL
   - Every required platform-package version
6. Execute the requested mode:
   - `report_only` (default if unspecified): summarize readiness, blockers, and
     required actions.
   - `dry_run`: review packaging / dry-run commands without claiming a
     production publish occurred. Keep orchestration anchored to the target repo
     root.
   - `live_publish`: follow the documented npm release path. Publish platform
     packages BEFORE the coordinating package.
7. Keep the final boundary explicit in any generated guidance: repo-native
   GitHub Release remains the default release contract.

## Outputs

- A clear npm readiness or publication outcome
- If `live_publish`: the corresponding npm packages are published to the registry

## Exit Gate

| #   | Check                                                                       |
| --- | --------------------------------------------------------------------------- |
| 1   | Requested mode activity (report, dry-run, live) is completed                |
| 2   | Version chain is tightly aligned (tag = evidence = coordinating = platform) |
| 3   | If live: coordinating and all platform packages are published               |
| 4   | User-facing npm install story stays distinct from repo-native clone         |
| 5   | Explicit wording remains that repo-native is the default model              |

## Guardrails

- Do not use this stage to replace or weaken the target repository's
  repo-native GitHub Release contract.
- Do not bypass validation or target-repository context checks before npm
  publication work begins.
- Do not allow the coordinating package or any platform package to drift from
  the authoritative released skill version.
- Do not describe one cross-platform binary npm package as the required model;
  use one coordinating package plus separate platform-specific packages.
- Do not treat unclear package ownership, missing platform coverage, or unclear
  install guidance as ready-to-publish states.

## Next Step

Stop after `report_only`, `dry_run`, or `live_publish`. This is a terminal
stage in the workflow.

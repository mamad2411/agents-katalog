---
name: eda-system-packager
description: Package the agent+skill infrastructure into a standalone, portable repository-ready bundle with skill-local tool mirrors.
---

# EDA System Packager

## When to use

Use this skill when you need to:
1. export current `AGENTS.md + skills + core KB/tool docs` as a standalone package,
2. mirror dependent scripts into each skill's portable bundle,
3. prepare a repository-ready folder for separate publication or handoff.

## Shared Capability Boundary

This skill is the direct workflow owner for agent+skill system packaging tasks.
It owns:
- standalone bundle generation,
- packaging-scope selection,
- export artifact validation at bundle level.

It does not own:
- repo-wide governance policy,
- skill-routing policy,
- publication hosting decisions beyond packaging output.

`workflow-scoped-execution` is not the default wrapper here. Use it only if a larger maintenance workflow explicitly delegates one bounded execution stage that must produce a package artifact.

## Expected Downstream Consumers

Typical consumers include:
- `eda-infra-maintainer` when infrastructure work needs a portable release bundle,
- release/publishing workflows that need a repo-ready export,
- maintenance tasks that must mirror current skill/tool state into `exports/`.

## Inputs

Provide or derive:
1. package scope,
2. output directory,
3. whether script mirroring is required,
4. whether the package is for local archive, release mirror, or external publication.

## Outputs

Return or update:
- standalone package directory,
- packaging summary with mirrored content scope,
- explicit statement of whether `workflow-scoped-execution` was `not_used` or the packaging step was delegated from another workflow.

## Knowledge And Tool Interaction

1. Treat `AGENTS.md`, the skill tree, and the core KB/tool docs as the canonical packaging source.
2. Use `eda-context-accessor` only when packaging scope depends on shared KB/tool context that is not obvious from the request.
3. If packaging reveals infra inconsistency or missing mirrored assets, escalate the maintenance action to `eda-infra-maintainer`.

## Hard Rules

1. Do not claim a package is canonical unless the bundle was rebuilt from current repo state.
2. Do not silently omit required governance or core KB/tool artifacts from a supposedly standalone package.
3. Do not use `workflow-scoped-execution` as the default owner for packaging work.

## Operational References

1. Load `references/workflow-owner-usage.md` when deciding whether packaging is the direct workflow owner task or a delegated substage.
2. Load `references/package-build.md` when running the package build command and selecting output location.
3. Load `references/package-contents.md` when deciding which artifacts must be mirrored into the standalone bundle.
4. Load `references/publish-handoff.md` when preparing the resulting bundle for git-init or external publication.

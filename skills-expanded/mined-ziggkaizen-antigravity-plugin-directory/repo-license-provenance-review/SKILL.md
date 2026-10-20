---
name: repo-license-provenance-review
description: Reviews dependency license and provenance risk before introducing or accepting packages. Use when adding dependencies, changing package sources, using custom registries, vendoring code, accepting dependency PRs, or evaluating unknown packages.
---

# Repository License and Provenance Review

Use this skill before accepting new dependencies or changed dependency sources.

## When to Use This Skill

Use this skill for new direct dependencies, changed registry/source URLs, git/tarball/local path/file/link/workspace dependencies, vendored code, dependency bot PRs for unfamiliar packages, unclear ownership or license, runtime dependencies distributed with a product, and packages with binary/native components.

## Review Process

1. Identify package name, version, source, and registry.
2. Determine dependency role.
3. Review license and compatibility concerns.
4. Review maintainer/source/provenance concerns.
5. Identify install scripts or native/binary behavior.
6. Recommend accept/reject/escalate.
7. Document assumptions and remaining risk.

## Workflow

Use `workflows/license-provenance-review-workflow.md`.

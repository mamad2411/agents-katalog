---
name: depot-github-actions
description: Audit and safely migrate GitHub Actions runners, caches, and container builds to documented Depot integrations without changing workflow behavior.
allowed-tools: Read, Glob, Grep
---

# Depot GitHub Actions

Use this skill when reviewing or changing GitHub Actions workflows for Depot runners, accelerated file caching, or container builds. Treat a migration as a behavior-preserving repository change, not a label substitution.

## Operating sequence

1. Inventory the complete workflow graph: both workflow extensions, triggers, permissions, environments, matrices, reusable callers and callees, expressions, cache steps, builds, publications, outputs, and downstream consumers.
2. Resolve every affected edge. If an expression or unavailable reusable workflow makes topology dynamic, name the file and job and block affected edits.
3. Collect applicable evidence. Runner work needs verified Depot App installation, repository access, runner group, documented runner label, and repository pin policy. Require project, OIDC, registry, and publication evidence only where the affected seam uses it; record irrelevant evidence as `N/A`.
4. Classify the seam using [runners](references/runners.md), [cache](references/cache.md), [container builds](references/container-builds.md), and [security and validation](references/security-and-validation.md).
5. For implementation, capture hashes of every target, re-read immediately before mutation, and stop on concurrent drift. Apply a transactional, minimal patch only after all evidence and equivalence gates pass.
6. Inspect the diff and run repository-native validation. Report commands and observed results truthfully. A blocked path remains byte-identical.

## Non-negotiable outcomes

- Preserve matrices, reusable-workflow contracts, events, permissions, environments, action pins, inputs, secrets, outputs, digests, manifests, and downstream behavior.
- Preserve compatible standard GitHub cache actions unless an independent requirement justifies changing them. Depot runner acceleration requires no cache-specific workflow edit.
- Never guess runner labels, App scope, project identity, credentials, or unsupported action inputs.
- Never grant sensitive authority to untrusted `pull_request_target` execution.
- Plan-only requests write no workflow. Missing evidence, unsupported mappings, unsafe trust boundaries, and drift block the affected edit.

Finish with an evidence table: workflow/job, requested seam, required evidence, observed source, result (`verified`, `N/A`, or `blocked`), changed files, and validation evidence.

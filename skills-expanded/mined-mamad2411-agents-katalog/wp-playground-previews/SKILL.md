---
name: wp-playground-previews
description: Designs and reviews public WordPress Playground demos and GitHub pull-request previews with safe artifact, permission, fork, and build boundaries.
---

# WordPress Playground previews

Use this skill when adding a Try in Playground link, a plugin/theme demo, or `WordPress/action-wp-playground-pr-preview`.

## Required inputs

- Public or private repository.
- Plugin/theme path.
- Whether committed files run directly.
- Build commands and artifact paths.
- Same-repository or fork PR model.
- Required companion components and fixtures.
- Acceptable public exposure.
- Existing CI and permission policy.

## Procedure

1. Inspect the repository before choosing architecture.
2. Read `resources/preview-architecture-matrix.md`.
3. Use direct action only when committed checkout contents are runnable and repository/ref access is public enough for Playground.
4. Use the two-workflow build/publish architecture when generated files or fork PRs are involved.
5. Keep the build workflow read-only.
6. Ensure the trusted publish workflow never checks out or executes PR code.
7. Do not use `pull_request_target` to run untrusted code.
8. Verify artifact paths and ZIP root layout.
9. Add the smallest Blueprint required for the preview.
10. Test the button from a fresh browser session and confirm no private data is exposed.

## Workflow

Use `workflows/add-pr-preview-workflow.md`.

## Resources and examples

- `resources/preview-architecture-matrix.md`
- `examples/github-actions-pr-preview-examples.md`

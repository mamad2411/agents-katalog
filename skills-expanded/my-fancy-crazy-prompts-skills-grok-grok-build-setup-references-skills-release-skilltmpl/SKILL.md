---
name: release
description: Prepare a release with changelog and version bump. Use when the user asks for a release, version bump, or /release.
---

# Release

## Steps

1. Run `{{TEST_CMD}}` and `{{LINT_CMD}}`
2. Gather commits/PRs since the last tag (`git log`)
3. Update CHANGELOG using `changelog.tmpl` as a guide
4. Bump version in the project's manifest file
5. Create an annotated tag and push (with user confirmation)
6. Summarize what shipped

Ask before pushing tags or publishing packages.
---
name: project-vendor-boundary
description: Overlay for app-owned versus vendored dependency boundaries. Portable across repos that vendor third-party code. Use when work touches vendored dependencies or their integration seam.
---

# Project Vendor Boundary

This is a composable overlay, not a standalone workflow.
Use alongside the repo's implementation skill when work touches vendored
dependencies or their integration boundary.

## When to use

The change involves vendored third-party code, the boundary between app-owned
and vendored code, or dependency integration (subtrees, vendor directories,
copied sources).

## Not for

App-owned code that does not touch vendor boundaries (use the implementation
skill directly), or release/packaging concerns (use **project-release-maintainer**).

## Rules

- prefer app-side integration changes before editing vendored code
- treat vendored code as subtree/vendor content, not normal project code
- keep notices, provenance, and install rules aligned with vendor changes
- avoid unrelated churn inside vendor trees

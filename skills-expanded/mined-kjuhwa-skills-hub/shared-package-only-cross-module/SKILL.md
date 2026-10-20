---
name: shared-package-only-cross-module
description: Enforce a one-way dependency graph in a multi-module repo — sibling modules may only import from a single `shared/` package, never from each other. Prevents webpack alias collisions, keeps module boundaries enforceable, and makes build/deploy units independent.
category: arch
tags: [monorepo, module-boundaries, webpack, alias, micro-frontend, dependency-direction]
triggers: ["cross-module import", "cannot resolve @/", "alias collision", "webpack root", "monorepo boundaries"]
source_project: lucida-ui
version: 0.1.0-draft
---

# Shared-Package-Only Cross-Module Imports

Siblings never import from siblings. Everything shared goes through one central `shared/` package.

See `content.md`.

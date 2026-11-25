---
name: dependency-review
description: Review dependency changes and summarize maintainer risk before a pull request is merged.
version: 0.1.0
triggers:
  - dependency
entryPoint: scripts/run.js
tags:
  - maintainer
  - dependency
---

# Dependency Review

Inspect dependency updates and prepare a short maintainer summary.

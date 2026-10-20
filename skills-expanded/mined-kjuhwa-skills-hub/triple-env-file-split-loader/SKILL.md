---
tags: [devops, triple, env, file, split, loader]
name: triple-env-file-split-loader
description: Split operator-facing env into three files (.env / .version / .memory) and load them in a fixed order
category: devops
version: 1.0.0
source_project: lucida-for-docker
trigger: Compose stack with many env vars where release cadence differs — site config rarely changes, versions change per release, memory/resource limits rarely change
---

See `content.md`.

---
tags: [devops, jenkins, dual, registry, docker, push]
name: jenkins-dual-registry-docker-push
description: Jenkins pipeline that builds one image and tags+pushes it to two registries (SaaS + on-prem) with both build-specific and rolling-latest tags
trigger: Release pipeline where the same artifact must land in an internal on-prem registry and an external SaaS/cloud registry, each with current and latest tags
category: devops
source_project: lucida-report
version: 1.0.0
---

# Jenkins dual-registry Docker push

See `content.md`.

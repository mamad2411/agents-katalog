---
tags: [backend, testcontainers, reuse, disabled]
name: testcontainers-reuse-disabled
description: Set TESTCONTAINERS_REUSE_ENABLE=false on the Gradle test task so CI and shared dev machines never inherit stale container state across suites
trigger: CI or shared dev box has Testcontainers runs leaking state between suites
category: backend
source_project: lucida-account
version: 1.0.0
---

# Testcontainers reuse disabled

See `content.md`.

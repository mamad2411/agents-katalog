---
tags: [backend, bootrun, jvmargs, jdwp, opens, java21]
name: bootrun-jvmargs-jdwp-opens-java21
description: Bake JDWP debug port and required --add-opens flags into Gradle bootRun so every dev gets the same Java 17/21-compatible local runtime
trigger: Local bootRun needs IDE-attach debug + Java 17/21 reflective access (--add-opens) without editing run configs per dev
category: backend
source_project: lucida-account
version: 1.0.0
---

# bootRun JVM args for JDWP + Java 21 reflection

See `content.md`.

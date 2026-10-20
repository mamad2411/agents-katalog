---
tags: [devops, spring, bootrun, local, dev, env]
name: spring-bootrun-local-dev-env-block
description: Gradle `bootRun` env block that wires local Redis/Mongo/Kafka/Eureka/MQTT for zero-config `./gradlew bootRun` developer experience
version: 1.0.0
source_project: lucida-performance
source_ref: lucida-performance@0536094
category: devops
triggers:
  - new engineer asks "how do I run this locally?"
  - application-local.yaml is gitignored and no-one knows the defaults
  - Spring Cloud service refuses to start locally because Eureka client is enabled
---

# bootRun env block for local dev

See `content.md`.

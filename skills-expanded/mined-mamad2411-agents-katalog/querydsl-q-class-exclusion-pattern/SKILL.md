---
tags: [devops, querydsl, class, exclusion, pattern]
name: querydsl-q-class-exclusion-pattern
description: One `exclusionPatterns` list drives Jacoco report + verification + Sonar exclusions; catches generated Querydsl Q-classes via `('A'..'Z').collect { "**/**/Q${it}*" }`.
category: devops
version: 1.0.0
source_project: lucida-measurement
trigger: Jacoco/Sonar coverage inflated by generated code (Querydsl Q-classes, Avro, entity boilerplate).
linked_knowledge:
  - jacoco-sonar-exclusion-policy
---

See `content.md`.

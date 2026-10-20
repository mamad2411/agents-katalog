---
tags: [devops, gradle, shared, exclusions, jacoco, sonar]
name: gradle-shared-exclusions-jacoco-sonar
description: Keep Jacoco report, Jacoco coverage verification, and SonarQube exclusions in sync by defining one `exclusionPatterns` list in Gradle ext
version: 1.0.0
source_project: lucida-performance
source_ref: lucida-performance@0536094
category: devops
triggers:
  - jacoco and sonarqube exclusion lists drift apart
  - adding a new package to coverage exclusions requires editing multiple blocks
  - querydsl Q-classes / generated code leaking into coverage reports
---

# Gradle Shared Coverage Exclusions

See `content.md`.

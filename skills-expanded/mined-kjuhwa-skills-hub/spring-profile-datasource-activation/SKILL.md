---
tags: [backend, spring, profile, datasource, activation]
name: spring-profile-datasource-activation
description: Select DB/Hibernate/logging config at JVM startup via `spring.profiles.active` so one build ships to dev, test, and prod without branching in code
version: 1.0.0
source_project: cygnus
source_ref: cygnus@cbb96a6dfff
category: backend
triggers:
  - same WAR goes to multiple environments
  - Spring profile chooses datasource and credentials
---

# Spring Profile Datasource Activation

See `content.md`.

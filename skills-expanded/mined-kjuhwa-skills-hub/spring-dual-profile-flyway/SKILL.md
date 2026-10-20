---
name: spring-dual-profile-flyway
description: Spring Boot dual-profile setup — H2 file-mode for dev (zero install, console enabled), PostgreSQL for prod — with Flyway managing DDL and JPA set to validate-only. The profile split that keeps local dev fast without drifting from prod schema.
category: backend
tags:
  - spring-boot
  - flyway
  - h2
  - postgresql
  - profiles
  - migrations
  - jpa
triggers:
  - spring profiles dev prod
  - flyway migrations spring
  - h2 file mode dev
  - ddl-auto validate
  - postgresql production profile
source_project: veda-chronicles
version: 0.1.0-draft
---

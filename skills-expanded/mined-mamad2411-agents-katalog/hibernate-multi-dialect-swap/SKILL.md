---
tags: [backend, hibernate, multi, dialect, swap]
name: hibernate-multi-dialect-swap
description: Ship one WAR that connects to Oracle, PostgreSQL, MSSQL, Tibero, DB2, or MariaDB based on Spring profile — all JDBC drivers bundled, dialect and datasource resolved from externalized config
version: 1.0.0
source_project: cygnus
source_ref: cygnus@cbb96a6dfff
category: backend
triggers:
  - one deployable must support multiple RDBMS vendors without rebuild
  - hibernate dialect chosen at startup, not compile time
  - customer deployments dictate DB vendor
linked_knowledge:
  - hibernate-date-format-lowercase
---

# Hibernate Multi-Dialect Swap

See `content.md`.

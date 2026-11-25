---
name: postgres-analyze-spring-boot
description: Analyze Spring Boot and Java integration with Azure Database for PostgreSQL Flexible Server, including JDBC, HikariCP, Entra/managed identity authentication, PgBouncer, transactions, queries, retries, and runtime failures. Use for Java microservices using Azure PostgreSQL.
---

# Analyze Spring Boot Integration

1. Trace datasource/JDBC configuration and affected repository/query paths.
2. Identify driver, HikariCP settings, PostgreSQL endpoint, authentication model, SSL, and PgBouncer usage.
3. Inspect connection pool, transaction boundaries, query behavior, timeouts, and retries.
4. Correlate application exceptions with PostgreSQL metrics, locks, HA, networking, and identity evidence.
5. Distinguish application pool/configuration problems from database/platform problems.
6. Route generic framework issues to `spring-boot-*` skills.
7. Never expose credentials or access tokens.

## Output
- Integration Flow
- Authentication/Pool Configuration
- Query/Transaction Findings
- Runtime Correlation
- Recommended Action

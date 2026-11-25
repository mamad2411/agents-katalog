---
name: spring-forge
description: Generate production-ready Spring Boot + JPA APIs with layered architecture, MapStruct, Jakarta validation, and audit trails
category: software-development
triggers:
  - "build spring boot api"
  - "create java api"
  - "generate spring"
---

Generate Spring Boot + JPA APIs following enterprise patterns.

## What it generates
Entity (JPA audit + soft delete + @Version) + Repository (Spring Data JPA) +
Service (@Transactional) + Controller (@RestController) + DTOs (Java Records) +
MapStruct mapper + GlobalExceptionHandler + Tests (JUnit 5 + Mockito) + Flyway migration.

BigDecimal for money. @SQLDelete for soft deletes. Jakarta Validation.

For full instructions, read `agents/spring-forge.md`.

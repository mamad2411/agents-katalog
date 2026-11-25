---
name: java-backend-architect
description: Comprehensive skill for designing and building scalable Spring Boot backend systems with clean architecture, JWT auth, MySQL, REST APIs, Docker, Redis, Kafka, microservices, and production deployment. Trigger when users ask to create, scaffold, or architect Java/Spring Boot backend services.
---

# Java Backend Architect

## Overview

This skill provides knowledge, templates, and scripts for building production-grade Spring Boot backend systems following clean architecture principles. It covers project scaffolding, layered architecture, JWT authentication, REST API design, database integration, messaging, caching, containerization, and deployment.

## When to Use This Skill

Use this skill when the user asks to:
- Scaffold or create a new Spring Boot microservice
- Design the architecture for a Java backend system
- Implement JWT authentication, REST APIs, or database access
- Set up Docker, Redis, Kafka, or production deployment
- Follow clean architecture / hexagonal architecture patterns

## Quick Start

For rapid service scaffolding, use:

```bash
python scripts/scaffold_service.py <service-name> --package <base-package>
```

This generates a complete Spring Boot project with clean architecture layers, application.yml, Dockerfile, and docker-compose setup.

## Core Capabilities

### 1. Clean Architecture & Project Structure

Follow the layered architecture defined in `references/clean_architecture.md`. The standard structure is:

```
<service-name>/
  src/main/java/<base-package>/
    domain/          # Enterprise business rules (entities, value objects, domain events)
    application/     # Application business rules (use cases, ports, DTOs)
    infrastructure/  # Adapters, persistence, messaging, external APIs
    interfaces/      # REST controllers, request/response models
    config/          # Spring configuration, security, beans
  src/main/resources/
    application.yml  # Base configuration
    db/migration/    # Flyway migration scripts
  Dockerfile
  docker-compose.yml
  pom.xml
```

Key principles:
- Domain layer has ZERO framework dependencies (no Spring annotations)
- Dependencies point INWARD (interfaces -> application -> domain)
- Infrastructure implements ports defined in the application layer

### 2. JWT Authentication

Implement JWT auth using Spring Security + `spring-boot-starter-security` + `jjwt`:

- `config/SecurityConfig.java` - Security filter chain configuration
- `config/JwtAuthFilter.java` - OncePerRequestFilter that validates JWT from Authorization header
- `interfaces/AuthController.java` - Login/register endpoints
- `application/service/AuthService.java` - Token generation and validation logic
- `application/port/out/TokenRepository.java` - Interface for token persistence (e.g., Redis-backed blacklist)

Token structure: Include `sub` (userId), `roles`, `iat`, `exp`.
Use RSA key pair or HMAC secret from environment variables (never hardcoded).

### 3. REST API Design

Follow RESTful conventions:
- Plural nouns for resources: `/api/v1/users`, `/api/v1/orders`
- Standard HTTP methods: GET, POST, PUT, DELETE, PATCH
- Consistent error response envelope: `{ "status": int, "error": string, "message": string, "timestamp": instant }`
- Pagination: `?page=0&size=20` with `Sort` parameter support
- Version prefix in URL path: `/api/v1/...`
- OpenAPI 3.0 documentation via springdoc-openapi

### 4. Database (MySQL + Flyway)

- Use Flyway for schema migrations in `src/main/resources/db/migration/`
- Naming: `V{version}__{description}.sql` (e.g., `V1__create_users_table.sql`)
- Use JPA/Hibernate or jOOQ for persistence
- Configure MySQL connection in `application.yml` with environment variables

### 5. Redis Integration

Use Spring Data Redis:
- Caching: `@Cacheable`, `@CacheEvict` with Redis-backed cache manager
- Session storage: `spring.session.store-type=redis`
- Token blacklisting: Store invalidated JWT tokens with TTL matching token expiry

### 6. Kafka Integration

Use Spring Kafka (`spring-kafka`):
- Define topics in `config/KafkaTopicConfig.java`
- Producers: `KafkaTemplate<Key, Value>` injected into application services
- Consumers: `@KafkaListener` in infrastructure layer
- Use Avro or JSON serialization with Schema Registry for production
- Configure retry, DLQ, and idempotent producer settings

### 7. Docker & Containerization

Each service includes:
- `Dockerfile` - Multi-stage build with Maven/Gradle, distroless JRE runtime
- `docker-compose.yml` - Service definition with MySQL, Redis, Kafka, and the application

Example `Dockerfile` approach:
```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### 8. Production Deployment

Refer to `references/production_checklist.md` for:
- Health checks and readiness probes
- Graceful shutdown configuration
- Centralized logging (ELK/Loki)
- Metrics with Micrometer + Prometheus
- Rate limiting and circuit breakers (Resilience4j)
- Secrets management (Vault or environment variables)
- Horizontal scaling considerations

## Resources

### scripts/scaffold_service.py
Python script that generates a complete Spring Boot microservice project skeleton with clean architecture. Run it to scaffold a new service.

### references/clean_architecture.md
Detailed reference on the clean architecture package structure, dependency rules, and code examples for each layer.

### references/production_checklist.md
Comprehensive checklist for taking a Spring Boot service to production: monitoring, security, resilience, and operations.

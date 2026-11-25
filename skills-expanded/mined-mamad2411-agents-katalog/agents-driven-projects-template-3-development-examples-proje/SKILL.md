# AGENTS.md — auth-service (Spring Boot Microservice)

<!-- Real example. Spring Boot 3.3 + PostgreSQL + Docker. -->

## Project

- **Name:** auth-service
- **Purpose:** Central authentication & authorization for the microservice mesh. Handles login, JWT issuance, token refresh, 2FA, and role-based access control.
- **Repo:** github.com/panomete/auth-service

## Stack

- **Language:** Java 21
- **Framework:** Spring Boot 3.3 + Spring Security 6
- **Database:** PostgreSQL 16 (auth_db)
- **Cache:** Redis 7 (token blacklist, rate limiting)
- **Build:** Maven 3.9 (wrapper included)
- **Container:** Docker Compose (dev), Kubernetes (prod)

## Project Map

```
src/main/java/com/panomete/auth/
├── AuthApplication.java           — Entrypoint
├── config/                        — SecurityConfig, RedisConfig, JwtConfig
├── controller/                    — REST controllers
│   ├── AuthController.java        — /api/v1/auth/login, /register, /refresh
│   └── TwoFactorController.java   — /api/v1/auth/2fa/setup, /verify
├── service/                       — Business logic
│   ├── AuthService.java
│   ├── JwtService.java
│   └── TotpService.java
├── repository/                    — Spring Data JPA repositories
├── model/                         — Entities: User, UserTotp, RecoveryCode, Session
├── dto/                           — Request/Response DTOs (Java records)
├── security/                      — JwtFilter, UserPrincipal, SecurityUtils
└── exception/                     — GlobalExceptionHandler, custom exceptions

src/main/resources/
├── application.yml                — Default config
├── application-dev.yml            — Dev overrides
├── application-prod.yml           — Prod overrides (DO NOT modify — sealed)
└── db/migration/                  — Flyway migrations

src/test/java/                     — Mirror of main structure
```

## Commands

```bash
# Build
./mvnw clean package -DskipTests

# Test all
./mvnw test

# Test single class
./mvnw test -Dtest=AuthServiceTest

# Integration tests (needs Docker)
docker compose -f docker-compose.test.yml up -d
./mvnw verify -P integration

# Run locally (needs PostgreSQL + Redis)
docker compose up -d
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
# → http://localhost:8081

# Lint
./mvnw checkstyle:check pmd:check

# Check for vulnerable dependencies
./mvnw dependency-check:check
```

## Conventions

- Java 21. Use **records** for all DTOs. No Lombok.
- Controllers return `ResponseEntity<ApiResponse<T>>`. Never return raw entities.
- Service methods throw custom exceptions (`AuthException`, `NotFoundException`). Never return null.
- `AuthService` interface + `AuthServiceImpl` (for testability).
- Repositories extend `JpaRepository<T, UUID>`.
- Tests: JUnit 5 + AssertJ + Mockito. Test class naming: `*Test.java`.
- Database: Flyway for migrations. `V{NN}__{description}.sql`.
- All timestamps: `java.time.Instant`. Never `java.util.Date`.
- Secrets: NEVER in application.yml. In `.env` (dev) or K8s secrets (prod).
- Commit messages: `type(scope): description` (conventional commits).

## Security Rules (MUST FOLLOW)

- Passwords hashed with bcrypt (strength=12). Never SHA, never MD5.
- JWT signed with RS256 (asymmetric). Public key exposed at `/.well-known/jwks.json`.
- Access token: 15 min. Refresh token: 24h, httpOnly cookie.
- All tokens have `jti` claim for revocation.
- Rate limit login: 5 attempts / 15 min / IP (Redis).
- TOTP secrets encrypted at rest (AES-256-GCM, key from KMS).
- NEVER log tokens, passwords, or recovery codes.
- All endpoints authenticated unless in `SecurityConfig.PUBLIC_URLS`.

## Constraints

- Do NOT modify `application-prod.yml`.
- Do NOT edit existing Flyway migrations — create new ones.
- API responses must remain backward-compatible within a major version.
- `User` entity: never expose `passwordHash` or `totpSecret` in responses.
- Token signing keys: never committed to repo. Injected via env.

## External Dependencies

- **Redis** — `localhost:6379` (dev), `redis.auth:6379` (prod)
- **PostgreSQL** — `localhost:5432/auth_db` (dev)
- **user-service** — `localhost:8082` (internal REST, for profile data)
- **notification-service** — RabbitMQ, for sending 2FA setup emails

## Useful Context

- This is part of a Spring Cloud microservice mesh (Eureka, Gateway, Config Server).
- Service discovery via Eureka (`spring.cloud.discovery`).
- Health check: `GET /actuator/health`.
- Postman collection: `docs/postman/auth-service.json`.

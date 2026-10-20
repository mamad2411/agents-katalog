# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Financial Control System (FCS) — a Spring Boot 4.0 / Java 25 monolith that tracks per-user expenses, incomes, and investments. Backed by MariaDB; serves a static HTML/JS frontend from `src/main/resources/static/`.

## Common commands

```bash
# Start the database (MariaDB on host port 3307)
docker compose up -d

# Run the app (http://localhost:8080)
./mvnw spring-boot:run

# Build / package
./mvnw clean package

# Tests
./mvnw test
./mvnw test -Dtest=FcsApplicationTests          # single class
./mvnw test -Dtest=FcsApplicationTests#methodName  # single method
```

The DB connection is hard-coded in `application.properties` (`jdbc:mariadb://localhost:3307/db_example`, user `springuser`/`ThePassword`) and matches the credentials in `docker-compose.yml`. `spring.jpa.hibernate.ddl-auto=update` — schema is auto-migrated by Hibernate; there are no migration files.

## Architecture

Standard layered Spring MVC: `controller` → `service` → `repository` (Spring Data JPA) → `model` (JPA entities). DTOs live under `controller/dto/` as Java records and are the only types crossing the controller boundary — entities are not exposed to clients (except `User` in a couple of places — see below).

**Domain shape.** `User` owns three top-level collections (`Expense`, `Income`, `Investment`), each `@OneToMany(cascade = ALL, orphanRemoval = true)` with `@OnDelete(CASCADE)` on the child side. Deleting a user cascades to all financial records. `Credit` is also owned by `User` and owns `CreditInstances`; deleting a credit or user cascades through the hierarchy.

**Routing convention.** Financial resources are nested under the user: `/users/{userId}/expense`, `/users/{userId}/income`, `/users/{userId}/investment`, `/users/{userId}/credit`. Instances are doubly nested: `/users/{userId}/credit/{creditId}/instance`. The user id is a path variable (UUID as string) — there is no auth context; the frontend passes it explicitly. `UserController` lives at `/users` and exposes `POST /users/login` which returns `UserResponseDTO` on success or 401. Passwords are BCrypt-hashed (`spring-security-web` is on the classpath but no `SecurityFilterChain` is configured — endpoints are unauthenticated at the framework level).

**Authorization.** Services validate ownership (user id match) and return 403 FORBIDDEN if the resource belongs to a different user. Ownership is checked transitively for nested resources (CreditInstanceService verifies credit ownership before allowing operations).

**CORS.** `WebConfig` allows only `http://localhost:8080` for `/**` with GET/POST/PUT/DELETE. The static frontend is served from the same origin, so this is effectively a no-op for production but matters if you point a separate dev server at the API.

**Frontend.** Plain HTML + vanilla JS in `src/main/resources/static/`. Each page (`dashboard`, `expense`, `income`, `investment`, `user`) has a matching script in `static/script/`. No build step.

**AutoPix.** Exists as a model class but is not yet wired through repository/service/controller layers — work in progress.

## Notes for changes

- Entities use `GenerationType.UUID` for IDs; services accept `String` and convert via `UUID.fromString()`.
- `spring.jpa.show-sql=true` is on — generated SQL appears in stdout during dev.
- The `target/` directory is checked-out artifacts from a previous build; rebuild rather than trusting it.

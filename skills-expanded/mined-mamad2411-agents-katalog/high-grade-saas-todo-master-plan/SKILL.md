---
name: high grade saas todo master plan
description: The absolute, exhaustive step-by-step master plan detailing exactly WHAT needs to be built and HOW it must be implemented for a High-Grade Todo SaaS using Java 17, Spring Boot, React, Kafka, Redis, Postgres, Mongo,Api Gateway, Rate Limit, Cap Theoream, Load Balance Resilience4j, Cron, Replicas, Sharding ,Event drive kafka and more.
---

# 🚀 MASTER SKILL PLAN: High-Grade Todo SaaS Implementation

**CRITICAL INSTRUCTION FOR DEVELOPER/AI:** Do NOT summarize. 
Do NOT skip implementation details. This is an Enterprise SaaS product. 
If you are asked to build the module, you must build the *entirety* of the features listed below, respecting the Clean Architecture constraints.

## 🛑 SECTION 0: STRICT ARCHITECTURE RULES (NON-NEGOTIABLE)

1.  **Clean Architecture (By Module)**: 
    *   `domain` (Entities, Value Objects, Repository Interfaces. NO Spring imports).
    *   `application` (UseCases, Service classes implementing UseCases, Custom Exceptions).
    *   `infrastructure` (JPA Entities, Mongo Documents, Kafka Producers/Consumers, Redis Config, Spring `@Repository`).
    *   `presentation` (Controllers, Request/Response DTOs, OpenAPI annotations).
2.  **No Direct Database Leakage**: Controllers CANNOT return JPA Entities or Mongo Documents. Controllers must return presentation DTOs mapped from Domain Entities.
3.  **Error Handling**: Only throw subclasses of `BaseAppException`. A global `@RestControllerAdvice` intercepts this, looks up the error key in `messages.properties`, and returns standard localized JSON.
4.  **Resilience**: Any call to a database or external service in the `infrastructure` layer must be circumscribed by Resilience4j `@CircuitBreaker` or `@Retry`.
5.  **Caching**: All `GET` queries in the UseCase layer must utilize Redis (`@Cacheable`). All `POST/PUT/DELETE` must evict/update the cache (`@CacheEvict`).

## Entities thoeses are the entities all of them need to exists.
 ├── Users
 ├── Workspaces
 ├── Projects
 ├── Tasks
 ├── Comments
 ├── Roles
 ├── ActivityLogs
 └── Billing
---

## 🏗️ SECTION 1: INFRASTRUCTURE & BOOTSTRAP

### Step 1.1: The Docker Environment (`docker-compose.yml`)
You must define the exact network topology:
0. **todo-service-app** depends on databases
1.  **Postgres**: `postgres:15-alpine` on port 5432. (Database for Core & ). flyway migration using sharding and replicas on migration V*****.sql
2.  **Mongo**: `mongo:6` on port 27017. (Database for Audit Logs).
3.  **Redis**: `redis:7-alpine` on port 6379. (Cache & Rate Limiting).
4.  **Kafka & Zookeeper**: Confluent images. Kafka exposed on 9092.
5.  **Observability**: `prom/prometheus` and `grafana/grafana`.
6.  *Action*: Verify health checks for all containers before Spring Boot starts.

### Step 1.2: The Spring Boot Skeleton
1.  **Dependencies**: Web, Security, Data JPA, Data Mongo, Data Redis, Kafka, Actuator, Resilience4j, Validation, Testcontainers.
2.  **Config**: `application.yml` containing HikariCP pooling, Redis TTL settings, Kafka consumer group IDs, and JWT secret keys.

---

## 🔐 SECTION 2: IDENTITY & TENANCY MODULE (  )

*What is being built: The system that securely manages users, JWTs, and isolated SaaS Workspaces.*

### Step 2.1: Domain & Application
1.  **Entities**: `User` (id, email, passwordHash, status), `Role` (enum), `Workspace` (id, name, ownerId).
2.  **UseCases to Implement**: `RegisterUser`, `AuthenticateUser`, `RefreshToken`, `CreateWorkspace`, `InviteUserToWorkspace`,Audit, Permission

### Step 2.2: Infrastructure & Security
1.  **SecurityFilterChain**: Configure stateless sessions. Disable CSRF. Map public endpoints (`/auth/**`).
2.  **JWT Provider**: Subsystem to sign JWTs (15 min expiry) and generate cryptographically secure Refresh Tokens (stored in DB and returned as HttpOnly cookies).
3.  **JPA**: `UserJpaEntity`, `WorkspaceJpaEntity`. Implement Spring Security `UserDetailsService`.

### Step 2.3: Presentation
1.  **Controllers**: `AuthController.java` (Login, Register, Refresh). `WorkspaceController.java` (CRUD workspaces). Ensure DTOs use `@Valid`.

---

## 📝 SECTION 3: CORE TODO MODULE

*What is being built: The high-performance engine for creating and managing tasks within a Workspace.*

### Step 3.1: Domain & Application
1.  **Entities**: `Todo` (id, workspaceId, title, description, status, priority, dueDate, assigneeId, tags). 
2.  **UseCases**: `CreateTodo`, `UpdateTodoStatus`, `AssignTodo`, `DeleteTodo`, `GetTodosByWorkspace`.
3.  **Business Rules**: You cannot assign a Todo to a User who is not in the Workspace.
4.  **Caching Rules**: `GetTodosByWorkspace` must hit Redis first.
5.  **Event Emitting**: Successful creation/updates must call `eventPublisher.publish(new TodoEvent(...))` passing to the Infrastructure layer.

### Step 3.2: Infrastructure
1.  **JPA Repositories**: Advanced queries using `@Query` or Specifications for filtering (Status, Priority) and Pagination (`Pageable`).
2.  **Kafka Producer**: Implements `IEventPublisher`. Converts `TodoEvent` to JSON and sends to topic `todo-events`.

### Step 3.3: Presentation
1.  **Controller**: `TodoController.java`. Must extract UserID and WorkspaceID securely from the JWT context. Endpoints: `GET /todos`, `POST /todos`, `PATCH /todos/{id}/status`.

---

## 🚔 SECTION 4: AUDIT MODULE (COMPLIANCE)

*What is being built: An immutable, sharded ledger storing every action taken in the system.*

1.  **Infrastructure (Kafka Consumer)**: `AuditEventListener` subscribes to `todo-events` and `iam-events`.
2.  **Data Storage (MongoDB)**: Saves an `AuditLogDocument`. Must contain: Timestamp, ActorId, Action (e.g., "TODO_DELETED"), EntityId, Target state payload.
3.  **Presentation**: `AuditController` (Admin Only). Fetches paginated logs from Mongo for compliance reviews.

---

## 📧 SECTION 5: NOTIFICATION MODULE

*What is being built: Asynchronous alerting system.*

1.  **Infrastructure (Kafka Consumer)**: `NotificationEventListener`.
2.  **Logic**: When a `TodoAssignedEvent` is received, lookup the User's email from the service (via internal interface), construct an HTML template, and send via `JavaMailSender` or AWS SES. Handle SMTP failures via Resilience4j retries.


---

## 🧪 SECTION 6: TESTING REQUIREMENTS

1.  **Unit Tests (JUnit 5 + Mockito)**: Verify all Application UseCases. Mock the Repositories. Ensure business logic invariants hold. (e.g., "Cannot complete an already completed task").
2.  **Integration Tests (Testcontainers + DataJpaTest)**: Spin up real Postgres and Redis Docker containers during the Maven test phase. Verify custom SQL queries and cache behavior.

---
## ⚛️ SECTION 7: HIGH-GRADE FRONTEND (REACT + TAILWIND)

*What is being built: The SaaS UI that consumes the APIs.*

1.  **Architecture**: Vite + React + TypeScript. strict interfaces mapping exactly to backend DTOs.
2.  **Tailwind v3**: Premium glassmorphism UI, cohesive color palette.
3.  **Axios Interceptors**: The core mechanism bridging frontend/backend. If a request returns `401 Unauthorized`, the interceptor must seamlessly call `/auth/refresh` using the HttpOnly cookie, retrieve a new JWT, and replay the original request.
4.  **Views to Build**:
    *   Log-in / Registration Forms (Zod validation).
    *   Dashboard Skeleton Loader (while Axios fetches).
    *   Kanban Board (Drag and drop Todo statuses mapping to `PATCH /todos/{id}/status`).
    *   List View (High density table with pagination).
5.  **Real-time UX**: Implement optimistic UI updates on mutations (change state locally instantly, revert if API fails).

**EXECUTION DIRECTIVE**: When the developer instructs you to "Build the    Module based on the Skill Plan", you will refer to Section 2 and implement ALL entities, use-cases, and infrastructure specified without taking shortcuts.
---


---

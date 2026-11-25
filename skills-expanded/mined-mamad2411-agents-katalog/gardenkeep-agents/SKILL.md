# AGENTS Guide

## Scope and Entry Point
- Primary module is `garden-keep-api/`; run Maven commands from that directory.
- Java 21 + Spring Boot 3.5.13 (`garden-keep-api/pom.xml`).

## Architecture (Ports and Adapters)
- Code is organized as hexagonal layers under `com.jbyanx.gardenkeep`:
  - `domain/model`: core rules (`Crop`, `GrowthStage`, `CropType`).
  - `application/port/in`: use-case API (`RecordWateringUseCase`).
  - `application/port/out`: persistence abstraction (`CropRepositoryPort`).
  - `application/service`: orchestration (`CropWateringService`).
  - `infrastructure/adapter/in/web`: REST entrypoint (`CropController`) + DTO (`WateringRequest`).
  - `infrastructure/adapter/out/persistence`: active adapter (`PostgresCropRepositoryAdapter`), legacy stub (`InMemoryCropRepositoryAdapter`), JPA entity (`CropEntity`), mapper (`CropPersistenceMapper`), and Spring Data repository (`JpaCropRepository`).
  - `infrastructure/config`: manual `@Bean` wiring (`BeanConfiguration`).
- Dependency direction is inward: controllers/adapters call ports; domain has no Spring imports.

## Main Data Flow (Watering)
- HTTP `POST /api/v1/crops/{id}/water` in `CropController` accepts `WateringRequest`.
- Controller calls `RecordWateringUseCase.waterCrop(id, soilDryAtSecondKnuckle)`.
- `CropWateringService` loads crop via `CropRepositoryPort.findById` and throws `IllegalArgumentException` if missing.
- Domain rule lives in `Crop.waterPlant(...)`; wet soil (`false`) throws `IllegalStateException`.
- On success, service persists through `CropRepositoryPort.save`.

## Project-Specific Conventions
- Business messages and many comments are in Spanish; preserve the current language style when touching nearby code.
- Domain methods accept time as a parameter (`Crop.waterPlant(..., LocalDateTime wateringTime)`) to keep tests deterministic.
- Spring wiring is explicit in `infrastructure/config/BeanConfiguration` (manual `@Bean` for service, `@Qualifier("postgresCropRepositoryAdapter")` selects the active adapter).
- Active persistence adapter is `PostgresCropRepositoryAdapter` backed by PostgreSQL via Spring Data JPA. The in-memory adapter (`InMemoryCropRepositoryAdapter`) is kept as a reference/fallback but is **not** wired.
- Database connection is configured through environment variables (`DB_USERNAME`, `DB_PASSWORD`) and Spring profiles; the `dev` profile targets `localhost:55432`.

## Build, Test, and Run
- Use the Maven Wrapper from the module directory:
```bash
cd garden-keep-api
./mvnw test
./mvnw spring-boot:run
./mvnw -Dtest=CropWateringServiceTest test
```
- JaCoCo coverage report is generated during the `test` phase at `garden-keep-api/target/site/jacoco/index.html`.
- A `docker-compose.yml` at the module root spins up PostgreSQL 15 on port `55432`:
```bash
cd garden-keep-api
docker compose up -d
```

## Quick Integration Check
- Start the database with Docker Compose, then run the app, and POST to any existing crop UUID:
```bash
curl -X POST "http://localhost:8080/api/v1/crops/{cropId}/water" \
  -H "Content-Type: application/json" \
  -d '{"soilDryAtSecondKnuckle": true}'
```
- Request/response contract is currently simple string responses from `CropController` (no global exception mapper yet).

## Extension Hotspots
- To swap the database backend, create a new adapter implementing `CropRepositoryPort` under `infrastructure/adapter/out/...` and update the `@Qualifier` in `BeanConfiguration`; `application/service` stays unchanged.
- If introducing new use cases, mirror the existing pattern: new `application/port/in` interface → service implementation → web adapter translation layer.


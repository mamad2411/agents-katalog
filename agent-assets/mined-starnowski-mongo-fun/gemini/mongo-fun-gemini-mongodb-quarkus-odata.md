# Project Context: mongodb-quarkus-odata

## Project Overview
This project is a Java-based application built with the **Quarkus** framework, focusing on **MongoDB** integration. It demonstrates advanced MongoDB usage including OData support, OpenAPI validation, and custom repository patterns.

### Key Technologies
*   **Java**: 17
*   **Framework**: Quarkus (v3.22.2)
*   **Database**: MongoDB (accessed via `quarkus-mongodb-client`)
*   **Build Tool**: Maven
*   **Utilities**: Lombok, MapStruct (likely, or manual mapping), Apache Olingo (OData), Swagger/OpenAPI

## Building and Running

### Prerequisites
*   JDK 17

### Commands
*   **Build and Test**: `./mvnw clean install`
    *   Important! Consider of invoking the "spotless:apply" goal before build, check "Format Code" section below.
*   **Run in Dev Mode**: `./mvnw quarkus:dev`
    *   This enables live coding and hot reload.
*   **Format Code**: `./mvnw spotless:apply`
    *   The project uses the Spotless plugin with Google Java Format. **Executing this command is required after any change to Java source files.**

## Development Conventions

### Architecture
*   **Service-Repository Pattern**: Business logic resides in `Service` classes (e.g., `PostService`), which interact with `Dao`/Repository classes (e.g., `PostDao`).
*   **Dependency Injection**: Uses Jakarta CDI (`@Inject`, `@ApplicationScoped`). Field injection is common.
*   **Data Models**: Uses Lombok (`@Data`, `@NoArgsConstructor`, etc.) to reduce boilerplate in entity classes.
*   **Identifiers**: Uses MongoDB `ObjectId` (`org.bson.types.ObjectId`).

### Testing
*   **Framework**: JUnit 5 (`quarkus-junit5`) with Mockito.
*   **Integration Tests**:
    *   Annotated with `@QuarkusTest`.
    *   Extend `AbstractITTest`.
    *   Use `EmbeddedMongoResource` to spin up an in-memory MongoDB for isolation.
    *   `@AfterEach` methods in `AbstractITTest` ensure data cleanup (e.g., `postDao.deleteAll()`) to maintain test independence.
*   **Parameterized Tests**: Uses `@ParameterizedTest` with `@MethodSource` for data-driven testing scenarios.

### Configuration
*   **Application Config**: Located in `src/main/resources/application.properties`.
*   **UUID Representation**: Configured as `STANDARD` (`quarkus.mongodb.uuid-representation=STANDARD`).

## Directory Structure
*   `src/main/java`: Source code.
*   `src/test/java`: Tests (Unit and Integration).
*   `src/main/resources`: Configuration (`application.properties`) and API definitions (OpenAPI/Swagger YAMLs).

# Project Context: mongodb-embedded-quarkus

## Overview
This project is a **Quarkus** application designed to demonstrate or experiment with **MongoDB** integration. It appears to be part of a larger "Mongo Fun" collection. The project explores using MongoDB with Quarkus, specifically dealing with embedded MongoDB for testing, and implementing OpenAPI validation filters.

## Tech Stack
*   **Language:** Java 17
*   **Framework:** Quarkus 3.9.4
*   **Database:** MongoDB (via `quarkus-mongodb-client`)
*   **Build Tool:** Maven
*   **API:** JAX-RS (RESTEasy), OpenAPI (Swagger/OpenAPI4j)
*   **Testing:** JUnit 5, Mockito, Flapdoodle Embedded Mongo, Quarkus Test MongoDB

## Key Directories & Files
*   `src/main/java/com/github/starnowski/mongo/fun/mongodb/container`: Root package for the application code.
    *   `controller`: JAX-RS Controllers (e.g., `ExampleController.java`).
    *   `filters`: OpenAPI validation filters (e.g., `OpenApiValidationFilter.java`).
    *   `repositories`: Data Access Objects for MongoDB (e.g., `PostDao.java`).
    *   `codec`: Custom MongoDB codecs.
*   `src/test/java`: Test sources, utilizing embedded MongoDB.
*   `src/main/resources/application.properties`: Main configuration file.
*   `pom.xml`: Maven build configuration.

## Build and Run

### Prerequisites
*   JDK 17+
*   Maven 3.8+

### Commands
*   **Build & Test:**
    ```bash
    mvn clean install
    ```
*   **Run in Development Mode:**
    ```bash
    mvn quarkus:dev
    ```
    This enables live coding (hot reload).
*   **Run Tests:**
    ```bash
    mvn test
    ```

## Development Conventions
*   **Quarkus Standard:** Follows standard Quarkus project structure.
*   **MongoDB:** Uses `quarkus-mongodb-client`. UUID representation is set to `STANDARD` in `application.properties`.
*   **Testing:** Uses `EmbeddedMongoResource` or `quarkus-test-mongodb` for integration tests ensuring isolation.

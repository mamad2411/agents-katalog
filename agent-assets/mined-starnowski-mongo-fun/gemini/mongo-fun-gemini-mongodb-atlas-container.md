# Mongo Atlas Search Demo

This project is a Spring Boot demonstration of **MongoDB Atlas Search** functionality running locally. It utilizes the `mongodb/mongodb-atlas-local` Docker image via **Testcontainers** to provide a full Atlas Search environment for integration testing without requiring a cloud Atlas cluster.

## Project Overview

*   **Technology Stack:**
    *   **Java 21**
    *   **Spring Boot 3.4.2**
    *   **Spring Data MongoDB**
    *   **Testcontainers** (for local MongoDB Atlas Search)
    *   **JUnit 5**
*   **Key Features:**
    *   Automated setup of a local MongoDB Atlas Search container.
    *   Programmatic creation and verification of Atlas Search indexes (`atlas_search_index`).
    *   Integration tests for `$search` aggregation operators like `queryString`.
    *   Usage of `jamolingo-junit5-mongo-extension` for easy BSON data loading in tests.

## Building and Running

### Prerequisites
*   **JDK 21** or higher.
*   **Maven 3.9+**.
*   **Docker** (required for Testcontainers).

### Key Commands
*   **Build and Test:**
    ```bash
    mvn clean install
    ```
*   **Run Application:**
    ```bash
    mvn spring-boot:run
    ```
    *Note: The application expects a MongoDB instance at `mongodb://localhost:27017/demos` by default.*

## Development Conventions

### Code Formatting (Spotless)
*   The project uses the **Spotless Maven Plugin** to enforce a consistent coding style.
*   **Style:** Google Java Style.
*   **Check style:** `mvnw spotless:check`
*   **Apply formatting:** `mvnw spotless:apply` (automatically run during the `compile` phase).

### Testing Strategy
*   Integration tests are located in `src/test/java`.
*   `MongoDbContainer.java` defines the custom Testcontainer for MongoDB Atlas. It requires significant memory (4GB) and SHM size (2GB) as per Atlas Local requirements.
*   `SimpleSearchTest.java` demonstrates how to:
    1.  Load BSON data using `@MongoSetup`.
    2.  Ensure an Atlas Search index exists via `collection.createSearchIndex(...)`.
    3.  Wait for the index to reach `READY` status.
    4.  Execute aggregation pipelines with the `$search` stage.

### Data Loading
*   Test data is stored as BSON files in `src/test/resources/bson/`.
*   The `@MongoSetup` annotation from the `jamolingo` extension is used to seed the database before tests.

### OData Metadata (EDM)
*   The file `src/main/resources/edm/edm6_filter_main.xml` contains OData metadata. This suggests the project may be part of a larger ecosystem involving OData filtering or mapping, potentially related to the `jamolingo` library.

## Project Structure
*   `src/main/java`: Core application logic and configuration.
*   `src/test/java`: Integration tests and Testcontainers configuration.
*   `src/test/resources/bson`: Sample data for search testing.

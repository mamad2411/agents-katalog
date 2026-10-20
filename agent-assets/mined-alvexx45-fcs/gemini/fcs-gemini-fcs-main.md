# Financial Control System (FCS)

FCS is a Spring Boot monolith designed for personal financial tracking. It allows users to manage expenses, incomes, and investments.

## Project Overview

- **Core Technologies:** Spring Boot 4.0.1, Java 25, MariaDB.
- **Persistence:** Spring Data JPA with Hibernate. Schema is automatically managed (`spring.jpa.hibernate.ddl-auto=update`).
- **Security:** Spring Security is used for BCrypt password hashing, but endpoint authentication is not currently enforced at the framework level.
- **Frontend:** A static frontend built with vanilla HTML, modern CSS (consolidated in `style.css`), and JavaScript. Uses Bootstrap 5, Bootstrap Icons, and Flatpickr for an elegant user experience.

## Getting Started

### Prerequisites

- Docker (for MariaDB)
- Java 25
- Maven (via `./mvnw`)

### Running the Project

1.  **Start the Database:**
    ```bash
    docker compose up -d
    ```
    This starts a MariaDB instance on host port `3307` as configured in `docker-compose.yml` and `application.properties`.

2.  **Run the Application:**
    ```bash
    ./mvnw spring-boot:run
    ```
    The application will be available at `http://localhost:8080`.

### Building and Testing

- **Build and Package:**
  ```bash
  ./mvnw clean package
  ```
- **Run All Tests:**
  ```bash
  ./mvnw test
  ```
- **Run Specific Test Class:**
  ```bash
  ./mvnw test -Dtest=FcsApplicationTests
  ```

## Architecture & Development Conventions

### Layered Structure
- **Controller:** `com.bernardo.fcs.controller` - REST endpoints. Uses DTOs for request/response bodies.
- **Service:** `com.bernardo.fcs.service` - Business logic and orchestration.
- **Repository:** `com.bernardo.fcs.repository` - Spring Data JPA repositories.
- **Model:** `com.bernardo.fcs.model` - JPA Entities.

### Key Conventions
- **Identifiers:** Primary keys are UUIDs (`GenerationType.UUID`). Controllers typically receive them as strings and convert them in the service layer.
- **DTOs:** Request and response objects are implemented as Java records in `com.bernardo.fcs.controller.dto`.
- **API Design:** Financial resources are nested under users: `/users/{userId}/expense`, `/users/{userId}/income`, etc.
- **Frontend-Backend Communication:** The frontend passes the user ID explicitly in requests as there is no session/auth context managed by the backend yet.
- **UI Design System:** Consolidated in `style.css` using CSS variables, 'Inter' font, custom modern modals for confirmations, and top-centered notifications with smooth animations.
- **Error Handling:** Currently relies on standard Spring Boot error responses.

### Database Configuration
Connection details are hard-coded in `src/main/resources/application.properties`:
- **URL:** `jdbc:mariadb://localhost:3307/db_example`
- **Credentials:** `springuser` / `ThePassword`

## Project Status
- **Core features:** User management, Expenses, Incomes, and Investments are fully implemented with a modern and refactored UI.
- **In-Progress:** Integration of `Credit` and `CreditInstances` into the dashboard and backend layers.
- **Future:** `AutoPix` implementation.

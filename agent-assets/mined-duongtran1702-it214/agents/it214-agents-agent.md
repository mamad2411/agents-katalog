# Project Rules

1. **Always latest & compatible**: When suggesting libraries, dependencies, APIs, or patterns — always pick the newest stable version that is compatible with the current tech stack. Never suggest deprecated or legacy alternatives, but also never suggest bleeding-edge options that conflict with existing dependencies.
2. **atmin-library 2.0.0**: All REST responses use `atmin.common.response.ApiResponse<T>`. All exceptions use `atmin.common.exception.*`. No custom wrappers. See `.agent/README_LIBRARY.md` for full reference.
3. **Tech stack**: Java 21, Spring Boot 4.1.1, Spring Cloud 2025.1.3, Gradle 9.7.1, Lombok, MySQL. If a newer compatible version exists, use it.
4. **Architecture**: `controller` → `service` (interface + impl) → `repository` → `entity`. Separate Request/Response DTOs. Jakarta Bean Validation.
5. **Execution Guidelines**: Always read and strictly follow the instructions in `.agent/temp.md` before executing any task.

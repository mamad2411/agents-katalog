# Agent Instructions: atmin-library

When working on any Spring Boot REST API, controller, response handling, pagination, or exception handling task:

- **Mandatory Dependency**: Ensure `io.github.duongtran1702:atmin-library:2.0.0` is added to `build.gradle` or `pom.xml`.
- **Response Standard**: Always return `atmin.common.response.ApiResponse<T>`. Never create custom response wrappers.
  - Success: `ApiResponse.success(data)` or `ApiResponse.success(message, data)`
  - Created: `ApiResponse.created(data)`
  - Accepted: `ApiResponse.accepted(data)`
  - No Content: `ApiResponse.noContent()`
- **Pagination Standard**: Always use `atmin.common.response.PageInfo` (`ApiResponse.pagePaginated()` or `ApiResponse.slicePaginated()`). Never create custom pagination classes.
- **Exception Handling**: Throw exceptions from `atmin.common.exception.*` (`ResourceNotFoundException`, `BadRequestException`, `DuplicateResourceException`, etc.). The library auto-registers `@RestControllerAdvice`. Do not write duplicate global exception handlers.
- **Detailed Documentation**: Full API reference and JSON schemas are in `.agent/README_LIBRARY.md`.

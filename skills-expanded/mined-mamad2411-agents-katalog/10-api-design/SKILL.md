# API Design — PerfectJob

> REST API conventions, DTOs, error handling, pagination, versioning.

## Description

Padroes de design de API REST para o PerfectJob. Define convenções de endpoints, DTOs, responses, erros (RFC 7807), paginação, versionamento, e documentação OpenAPI.

## Checklist

1. Todo endpoint sob `/api/v1/` — versionamento na URL
2. Nomes de recursos: plural, kebab-case (`/api/v1/job-matches`, `/api/v1/resumes`)
3. DTOs de entrada: sufixo `Request` com Jakarta Validation
4. DTOs de saida: sufixo `Response` com dados formatados
5. Erros seguem RFC 7807 Problem Details
6. Paginacao com Spring `Pageable` → `page` e `size` query params
7. Use `@Operation` e `@ApiResponses` do Springdoc em cada endpoint
8. Nunca exponha entidades JPA diretamente — sempre via DTO + MapStruct
9. IDs sao UUID — nunca auto-increment
10. Use PATCH para updates parciais, PUT para replacements completos
11. Retorne 201 Created para POST com Location header
12. Retorne 204 No Content para DELETE

## Key Rules

- **NEVER** exponha entidades JPA (`@Entity`) na API — use DTOs
- **NEVER** retorne stack traces — use ProblemDetail
- **NEVER** use verbos na URL (`/getJobs`) — use HTTP methods (`GET /jobs`)
- **NEVER** retorne listas sem paginacao em resources que podem crescer
- **NEVER** use 200 para tudo — use status codes corretos (201, 204, 400, 404, 422)
- **ALWAYS** valide input com `@Valid` no controller
- **ALWAYS** inclua `Location` header em responses 201 Created
- **ALWAYS** documente endpoints com Springdoc OpenAPI annotations
- **ALWAYS** use kebab-case em URLs (`/job-matches` not `/jobMatches`)
- **ALWAYS** inclua `X-Request-Id` header para tracing

## Error Response Format (RFC 7807)

```json
{
  "type": "https://perfectjob.com.br/errors/job-not-found",
  "title": "Job Not Found",
  "status": 404,
  "detail": "Job with id 550e8400-e29b-41d4-a716-446655440000 was not found",
  "instance": "/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-04-13T10:30:00Z",
  "requestId": "abc-123-def"
}
```

### Implementation

```java
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    ResponseEntity<ProblemDetail> handleNotFound(EntityNotFoundException ex) {
        var problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
        problem.setTitle("Resource Not Found");
        problem.setType(URI.create("https://perfectjob.com.br/errors/not-found"));
        return ResponseEntity.status(404).body(problem);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ResponseEntity<ProblemDetail> handleValidation(MethodArgumentNotValidException ex) {
        var problem = ProblemDetail.forStatus(HttpStatus.UNPROCESSABLE_ENTITY);
        problem.setTitle("Validation Error");
        problem.setDetail("One or more fields failed validation");
        var errors = ex.getBindingResult().getFieldErrors().stream()
            .map(e -> Map.of("field", e.getField(), "message", e.getDefaultMessage()))
            .toList();
        problem.setProperty("errors", errors);
        return ResponseEntity.unprocessableEntity().body(problem);
    }
}
```

## Pagination

### Request
```
GET /api/v1/jobs?page=0&size=20&sort=createdAt,desc
```

### Response
```json
{
  "content": [...],
  "page": 0,
  "size": 20,
  "totalElements": 1500,
  "totalPages": 75,
  "last": false
}
```

### Implementation
```java
@GetMapping
Page<JobResponse> search(
    @RequestParam(required = false) String q,
    @RequestParam(required = false) String location,
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size,
    @RequestParam(defaultValue = "createdAt,desc") String[] sort
) {
    var pageable = PageRequest.of(page, size, Sort.by(parseSort(sort)));
    return jobService.search(q, location, pageable)
        .map(jobMapper::toResponse);
}
```

## DTO Pattern

### Request
```java
public record JobSearchRequest(
    @NotBlank(message = "Query is required")
    @Size(min = 2, max = 200)
    String query,

    @Size(max = 100)
    String location,

    @Pattern(regexp = "JUNIOR|PLENO|SENIOR")
    String level
) {}
```

### Response
```java
public record JobResponse(
    UUID id,
    String title,
    String company,
    String location,
    String salaryRange,
    Integer matchScore,
    LocalDateTime scrapedAt,
    String sourceUrl
) {}
```

### Mapper (MapStruct)
```java
@Mapper(componentModel = "spring")
public interface JobMapper {
    JobResponse toResponse(Job entity);
    Job toEntity(JobCreateRequest request);
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void updateEntity(@MappingTarget Job entity, JobUpdateRequest request);
}
```

## API Endpoints Summary

```
Auth:
  POST   /api/v1/auth/register          → 201 + Location
  POST   /api/v1/auth/login             → 200 + tokens
  POST   /api/v1/auth/refresh           → 200 + new access token
  POST   /api/v1/auth/logout            → 204
  POST   /api/v1/auth/google            → 200 + tokens
  POST   /api/v1/auth/apple             → 200 + tokens
  POST   /api/v1/auth/linkedin          → 200 + tokens

Jobs:
  GET    /api/v1/jobs                    → 200 + paginated
  GET    /api/v1/jobs/{id}               → 200 + detail
  GET    /api/v1/jobs/search             → 200 + filtered paginated

Resumes:
  POST   /api/v1/resumes/upload          → 201 + Location
  GET    /api/v1/resumes                 → 200 + list
  GET    /api/v1/resumes/{id}            → 200 + detail
  PUT    /api/v1/resumes/{id}/skills     → 200 + updated
  DELETE /api/v1/resumes/{id}            → 204

Matching:
  POST   /api/v1/matching/{resumeId}/jobs       → 200 + top-20 matches
  GET    /api/v1/matching/{resumeId}/job/{jobId} → 200 + match detail
  POST   /api/v1/matching/feedback               → 200

Favorites:
  POST   /api/v1/favorites/{jobId}      → 201
  DELETE /api/v1/favorites/{jobId}       → 204
  GET    /api/v1/favorites               → 200 + paginated

User:
  GET    /api/v1/users/me                → 200 + profile
  PUT    /api/v1/users/me                → 200 + updated
  DELETE /api/v1/users/me                → 204 (LGPD hard delete)
  GET    /api/v1/users/me/export         → 200 + JSON (LGPD export)

Subscriptions:
  POST   /api/v1/subscriptions/validate  → 200
  GET    /api/v1/subscriptions/status    → 200
```

## References
- RFC 7807 Problem Details: https://datatracker.ietf.org/doc/html/rfc7807
- Springdoc OpenAPI: https://springdoc.org/
- REST API Design: https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design

---
trigger: glob
globs: "src/integrationTest/java/**/*IT.java"
---

## Full Integration Testing Rules

- **Annotation:** Use `@SpringBootTest` only when loading the full application context or testing critical external integrations. Avoid integration overhead.
- **Base Class:** Must extend `BaseIT`.
- **Data Seeding:** Use `@Sql` to initialize required data. Locate separate SQL files in `src/integrationTest/resources/<domain>/`.
- **HTTP Client:** Use `getRestTemplate()` for performing HTTP integration calls against endpoints.
- **Structure:** Strictly follow `// Given`, `// When`, `// Then` with `snake_case` method naming. Class names must end with `IT.java`.
- Example:


```java
class SearchExecutionIT extends BaseIT {

  public static final String ENDPOINT = "/execution/search";

  @Test
  @Sql("/com/vitaly/pt/formacion/infrastructure/api/execution/execution_technician_id_111.sql")
  void search_shouldReturn200OkAndContainsExecution_whenFilteringByIdFound() {
    // Given
    long executionId = 111L;
    ExecutionSearchRequest requestBody =
            ExecutionSearchRequest.builder().technicianIds(List.of(executionId)).build();
    // When
    ResponseEntity<ExecutionSearchResponse> response =
            getRestTemplate().postForEntity(ENDPOINT, requestBody, ExecutionSearchResponse.class);
    // Then
    assertThat(response.getStatusCode().value()).isEqualTo(HttpStatus.OK.value());
    ExecutionSearchResponse body = response.getBody();
    assertThat(body).isNotNull();
    UserResponse technician = body.technician();
    assertThat(technician.id()).isEqualTo(executionId);
  }
}
```
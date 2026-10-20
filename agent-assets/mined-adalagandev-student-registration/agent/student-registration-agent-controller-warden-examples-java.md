# Controller Rules — Java Examples

**Framework basis:** Java 17+, Spring Boot 3.x (Spring Web MVC, `jakarta.*`),
Jakarta Bean Validation, springdoc-openapi 2.x. The rules themselves are
framework-agnostic — these examples only show one concrete stack.
**Translation hints:** Quarkus/Jakarta REST → `@Path`/`@GET` instead of
`@GetMapping`; Micronaut → `@Controller`/`@Get`; Spring WebFlux → same
annotations, reactive return types.
**Version-sensitive:** Spring Boot 3.x uses `jakarta.validation.*` — Boot 2.x
uses `javax.validation.*`. springdoc-openapi 2.x pairs with Boot 3.x (1.x for
Boot 2.x). Records for DTOs require Java 16+.

## Rule 1 — Translate, don't think
Violation:
```java
@PostMapping("/registrations")
ResponseEntity<?> register(@RequestBody RegistrationRequest body) {
    var student = service.getStudent(body.studentId());
    if (student.credits() >= 30 && !student.hasHold()) {   // business decision
        return ResponseEntity.ok(service.register(body.studentId(), body.courseId()));
    }
    return ResponseEntity.badRequest().build();
}
```
Correct:
```java
@PostMapping("/registrations")
@ResponseStatus(HttpStatus.CREATED)
RegistrationResponse register(@Valid @RequestBody RegistrationRequest body) {
    var result = service.register(new RegisterStudent(body.studentId(), body.courseId()));
    return RegistrationResponse.from(result);              // translate only
}
```

## Rule 2 — One controller per resource
Violation:
```java
@RestController
class ApiController {                      // grab-bag
    @GetMapping("/students/{id}") ...
    @PostMapping("/courses") ...           // different resource
    @GetMapping("/reports/enrollment") ... // and another
}
```
Correct:
```java
@RestController @RequestMapping("/v1/students") class StudentController { ... }
@RestController @RequestMapping("/v1/courses")  class CourseController  { ... }
@RestController @RequestMapping("/v1/reports")  class ReportController { ... }
```

## Rule 3 — Thin handlers
Violation:
```java
@PostMapping("/students")
ResponseEntity<?> create(@RequestBody Map<String, Object> body) {
    // 40 lines of casting, null checks, loops, and response assembly
}
```
Correct:
```java
@PostMapping
@ResponseStatus(HttpStatus.CREATED)
StudentResponse create(@Valid @RequestBody CreateStudentRequest body) {
    return StudentResponse.from(service.create(body.toCommand()));
}
```

## Rule 4 — Validate shape declaratively
Violation:
```java
@PostMapping
StudentResponse create(@RequestBody CreateStudentRequest body) {
    if (!body.email().contains("@"))                 // hand-rolled, in body
        throw new IllegalArgumentException("bad email");
}
```
Correct:
```java
record CreateStudentRequest(
    @Email @NotBlank String email,                   // declarative shape
    @Min(1) @Max(6) int year) { }
// @Valid on the handler; existence/permission checks stay in the service
```

## Rule 5 — DTOs in, DTOs out
Violation:
```java
@GetMapping("/{id}")
StudentEntity get(@PathVariable long id) {           // JPA entity out
    return repository.findById(id).orElseThrow();
}
```
Correct:
```java
@GetMapping("/{id}")
StudentResponse get(@PathVariable long id) {         // DTO out
    return StudentResponse.from(service.get(new StudentId(id)));
}
```

## Rule 6 — No business-error handling
Violation:
```java
@PostMapping("/registrations")
ResponseEntity<?> register(@Valid @RequestBody RegistrationRequest body) {
    try {
        return ResponseEntity.ok(service.register(body.toCommand()));
    } catch (CourseFullException e) {                // domain error caught here
        return ResponseEntity.status(409).body("course full");
    }
}
```
Correct:
```java
@PostMapping("/registrations")
@ResponseStatus(HttpStatus.CREATED)
RegistrationResponse register(@Valid @RequestBody RegistrationRequest body) {
    return RegistrationResponse.from(service.register(body.toCommand()));
}
// @RestControllerAdvice maps CourseFullException → 409 (exception-warden)
```

## Rule 7 — No persistence access
Violation:
```java
@RestController
class StudentController {
    private final StudentRepository repository;      // repo in controller
    @GetMapping List<StudentEntity> list() { return repository.findAll(); }
}
```
Correct:
```java
@RestController
class StudentController {
    private final StudentService service;            // service only
    @GetMapping List<StudentResponse> list(@Valid PageParams page) {
        return service.list(page).stream().map(StudentResponse::from).toList();
    }
}
```

## Rule 8 — Explicit status codes
Violation:
```java
@PostMapping StudentResponse create(...) { ... }     // 200 on create
@DeleteMapping("/{id}") Map<String, Boolean> delete(...) {
    return Map.of("deleted", true);                  // 200 + body on delete
}
```
Correct:
```java
@PostMapping
ResponseEntity<StudentResponse> create(@Valid @RequestBody CreateStudentRequest b) {
    var s = service.create(b.toCommand());
    return ResponseEntity.created(URI.create("/v1/students/" + s.id()))
                         .body(StudentResponse.from(s));   // 201 + Location
}
@DeleteMapping("/{id}") @ResponseStatus(HttpStatus.NO_CONTENT)
void delete(@PathVariable long id) { service.delete(new StudentId(id)); }
```

## Rule 9 — Declarative security
Violation:
```java
@DeleteMapping("/{id}")                              // who may call this?
@ResponseStatus(HttpStatus.NO_CONTENT)
void delete(@PathVariable long id) { service.delete(new StudentId(id)); }
```
Correct:
```java
@DeleteMapping("/{id}")
@ResponseStatus(HttpStatus.NO_CONTENT)
@PreAuthorize("hasRole('ADMIN')")                    // policy visible here
void delete(@PathVariable long id) { service.delete(new StudentId(id)); }
// per-record ownership checks live in the service
```

## Rule 10 — Stateless controllers
Violation:
```java
@RestController
class StudentController {
    private Student current;                         // singleton bean shared
    @GetMapping("/{id}") StudentResponse get(@PathVariable long id) {
        current = service.get(new StudentId(id));    // across threads: race
        return StudentResponse.from(current);
    }
}
```
Correct:
```java
@GetMapping("/{id}")
StudentResponse get(@PathVariable long id) {
    return StudentResponse.from(service.get(new StudentId(id)));  // locals only
}
```

## Rule 11 — HTTP semantics
Violation:
```java
@GetMapping("/students/{id}/delete")                 // GET that mutates
@PostMapping("/getStudentList")                      // verb in path
```
Correct:
```java
@DeleteMapping("/students/{id}")
@GetMapping("/students")                             // nouns; method = verb
```

## Rule 12 — Cap and allowlist collection params
Violation:
```java
@GetMapping
List<StudentResponse> list(@RequestParam(defaultValue = "20") int size,
                           @RequestParam(defaultValue = "id") String sort) {
    return service.list(size, sort);   // ?size=1000000, ?sort=passwordHash
}
```
Correct:
```java
private static final Set<String> SORTABLE = Set.of("id", "lastName", "enrolledAt");
@GetMapping
List<StudentResponse> list(@RequestParam(defaultValue = "20") @Max(100) int size,
                           @RequestParam(defaultValue = "id") String sort) {
    if (!SORTABLE.contains(sort))
        throw new ConstraintViolationException(...);  // boundary concern
    return service.list(size, sort);
}
```

## Rule 13 — Version and document
Violation:
```java
@RestController @RequestMapping("/students")          // no version, no docs
class StudentController { ... }
```
Correct:
```java
@RestController @RequestMapping("/v1/students")
class StudentController {
    @Operation(summary = "Get a student by id")
    @ApiResponse(responseCode = "404", description = "Student not found")
    @GetMapping("/{id}") StudentResponse get(@PathVariable long id) { ... }
}
```

## Rule 14 — Test the mapping only
Violation:
```java
@SpringBootTest                            // full app to test business rules
class StudentControllerTest {
    @Test void registrationRejectedWhenCourseFull() { ... }  // service's job
}
```
Correct:
```java
@WebMvcTest(StudentController.class)       // slice: mapping only
class StudentControllerTest {
    @MockBean StudentService service;
    @Test void postStudentsReturns201WithLocation() { ... }
    @Test void malformedEmailReturns400() { ... }
    @Test void deleteRequiresAdminRole() { ... }
}   // course-full behavior is a service test (test-warden's territory)
```

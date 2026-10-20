# Spring Boot Architecture — PerfectJob

> Modular monolith with Hexagonal Architecture by feature. Spring Boot 3.4+, Java 21, Gradle Kotlin DSL.

## Description

PerfectJob backend is a modular monolith organized by business domain (feature-based packages) using Hexagonal (Ports & Adapters) architecture. Each feature module exposes inbound adapters (REST controllers, scheduled tasks) and outbound adapters (JPA repositories, external API clients), with a pure domain core that has zero framework dependencies.

**Stack**: Spring Boot 3.4.x, Java 21, Spring Security 6, JWT (jjwt 0.12.x), OAuth2 Client, MapStruct 1.6.x, Flyway 10.x, HikariCP, Gradle Kotlin DSL.

**Feature Modules**: `common`, `auth`, `user`, `job`, `scraping`, `resume`, `matching`

## Checklist

1. Verify the change fits within a single feature module — never cross module boundaries without going through a port interface
2. Place domain logic in `domain/` subpackage — entities, value objects, domain exceptions, port interfaces
3. Place inbound adapters in `adapter/in/` — controllers implement port interfaces from domain
4. Place outbound adapters in `adapter/out/` — repository implementations, external API clients
5. Use Java 21 records for DTOs, value objects, and query results
6. Use sealed interfaces for domain events and result types
7. Use MapStruct for entity ↔ DTO mapping with `@Mapper(componentModel = "spring")`
8. Use `@Validated` on controller `@RequestBody` parameters with Jakarta Validation annotations
9. Run Flyway migration for every schema change — never modify an existing migration
10. Enable virtual threads via `spring.threads.virtual.enabled=true`
11. Configure HikariCP pool size: `maximumPoolSize = (cpu_cores * 2) + effective_spindle_count`
12. Use `@Transactional(readOnly = true)` on all read operations

## Key Rules

- **NEVER** put business logic in controllers — controllers only translate HTTP → domain call
- **NEVER** inject `EntityManager` directly — use Spring Data JPA repositories
- **NEVER** use `@Autowired` field injection — use constructor injection (Lombok `@RequiredArgsConstructor`)
- **NEVER** create circular dependencies between modules — use events or port interfaces
- **NEVER** use `Object` as a return type — use records, sealed types, or specific DTOs
- **ALWAYS** use records for DTOs unless mutation is required by a framework
- **ALWAYS** separate read models (DTOs) from write models (entities)
- **ALWAYS** use `@Transactional(readOnly = true)` by default, remove `readOnly` only for writes
- **ALWAYS** name packages by feature, not by layer (`com.perfectjob.resume.domain`, not `com.perfectjob.domain`)
- **ALWAYS** keep domain core free of Spring annotations (except `@Entity` on JPA entities)
- **ALWAYS** use virtual threads for blocking I/O operations (scraping, external APIs)

## Module Structure

```
com.perfectjob/
├── common/
│   ├── config/                    # Global Spring configs
│   ├── exception/                 # Global exception handlers
│   └── util/                      # Shared utilities
├── auth/
│   ├── domain/                    # Auth port interfaces, exceptions
│   ├── adapter/in/
│   │   └── AuthController.java    # REST controller
│   ├── adapter/out/
│   │   └── JwtAdapter.java        # JWT generation/validation
│   ├── service/                   # AuthService (implements domain port)
│   └── dto/                       # LoginRequest, TokenResponse (records)
├── user/
│   ├── domain/
│   │   ├── model/                 # User entity, value objects
│   │   └── port/                  # UserRepository port
│   ├── adapter/in/
│   │   └── UserController.java
│   ├── adapter/out/
│   │   └── UserJpaRepository.java # Implements port, extends JpaRepository
│   ├── service/
│   ├── mapper/                    # MapStruct mappers
│   └── dto/
├── job/
│   ├── domain/
│   │   ├── model/                 # Job, JobMatch entities
│   │   └── port/
│   ├── adapter/in/
│   ├── adapter/out/
│   ├── service/
│   ├── mapper/
│   └── dto/
├── scraping/
│   ├── domain/
│   │   ├── model/                 # ScrapingTask entity
│   │   └── port/                  # JobScraper interface
│   ├── adapter/in/
│   │   └── ScrapingScheduler.java
│   ├── adapter/out/
│   │   ├── linkedin/              # LinkedInScraper
│   │   ├── indeed/                # IndeedScraper
│   │   └── catho/                 # CathoScraper
│   ├── service/                   # ScrapingOrchestrator
│   └── dto/
├── resume/
│   ├── domain/
│   │   ├── model/                 # Resume, WeightedSkill entities
│   │   └── port/
│   ├── adapter/in/
│   ├── adapter/out/
│   ├── service/
│   ├── mapper/
│   └── dto/
└── matching/
    ├── domain/
    │   ├── model/                 # MatchResult value objects
    │   └── port/                  # EmbeddingService port
    ├── adapter/in/
    ├── adapter/out/
    │   └── CohereEmbeddingAdapter.java
    ├── service/                   # MatchingEngine
    └── dto/
```

## Code Examples

### build.gradle.kts (root)

```kotlin
plugins {
    java
    id("org.springframework.boot") version "3.4.1"
    id("io.spring.dependency-management") version "1.1.7"
}

group = "com.perfectjob"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-security")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("org.springframework.boot:spring-boot-starter-oauth2-client")
    implementation("org.springframework.boot:spring-boot-starter-cache")

    implementation("io.jsonwebtoken:jjwt-api:0.12.6")
    runtimeOnly("io.jsonwebtoken:jjwt-impl:0.12.6")
    runtimeOnly("io.jsonwebtoken:jjwt-jackson:0.12.6")

    implementation("org.mapstruct:mapstruct:1.6.3")
    annotationProcessor("org.mapstruct:mapstruct-processor:1.6.3")

    implementation("org.flywaydb:flyway-core:10.21.0")
    implementation("org.flywaydb:flyway-database-postgresql:10.21.0")

    implementation("com.microsoft.playwright:playwright:1.49.0")
    implementation("org.jsoup:jsoup:1.18.1")
    implementation("io.github.bucket4j:bucket4j-core:8.10.1")

    runtimeOnly("org.postgresql:postgresql:42.7.4")
    implementation("org.postgresql:pgvector:0.1.6")

    compileOnly("org.projectlombok:lombok")
    annotationProcessor("org.projectlombok:lombok")
    annotationProcessor("org.projectlombok:lombok-mapstruct-binding:0.2.0")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.security:spring-security-test")
    testImplementation("org.testcontainers:junit-jupiter:1.20.4")
    testImplementation("org.testcontainers:postgresql:1.20.4")
}

tasks.withType<JavaCompile> {
    options.compilerArgs.addAll(listOf(
        "--enable-preview",
        "-Amapstruct.defaultComponentModel=spring",
        "-Amapstruct.unmappedTargetPolicy=ERROR"
    ))
}

tasks.withType<Test> {
    useJUnitPlatform()
    jvmArgs("--enable-preview")
}
```

### application.yml

```yaml
spring:
  application:
    name: perfectjob
  threads:
    virtual:
      enabled: true
  datasource:
    url: jdbc:postgresql://localhost:5432/perfectjob
    hikari:
      maximum-pool-size: 21
      minimum-idle: 5
      idle-timeout: 300000
      connection-timeout: 20000
      leak-detection-threshold: 60000
  jpa:
    open-in-view: false
    hibernate:
      ddl-auto: validate
    properties:
      hibernate:
        format_sql: true
        jdbc:
          batch_size: 50
        order_inserts: true
        order_updates: true
  flyway:
    enabled: true
    locations: classpath:db/migration
```

### Record DTO

```java
package com.perfectjob.job.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record JobSearchRequest(
    @NotBlank String query,
    @Size(max = 100) String location,
    String[] sources,
    Integer salaryMin,
    Integer salaryMax,
    String jobType,
    String experienceLevel,
    int page,
    int size
) {
    public JobSearchRequest {
        if (page < 0) page = 0;
        if (size <= 0 || size > 50) size = 20;
    }
}
```

### Sealed Interface for Results

```java
package com.perfectjob.matching.domain;

public sealed interface MatchResult {
    record Success(
        long jobId,
        double score,
        String explanation
    ) implements MatchResult {}

    record Skipped(
        long jobId,
        String reason
    ) implements MatchResult {}

    record Failed(
        long jobId,
        String error
    ) implements MatchResult {}
}
```

### Controller with Validation

```java
package com.perfectjob.job.adapter.in;

import com.perfectjob.job.dto.JobSearchRequest;
import com.perfectjob.job.dto.JobResponse;
import com.perfectjob.job.service.JobService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/jobs")
@RequiredArgsConstructor
public class JobController {

    private final JobService jobService;

    @PostMapping("/search")
    public ResponseEntity<Page<JobResponse>> search(
            @Valid @RequestBody JobSearchRequest request,
            @AuthenticationPrincipal Jwt jwt) {
        Long userId = jwt.getClaim("user_id");
        return ResponseEntity.ok(jobService.search(userId, request));
    }
}
```

### MapStruct Mapper

```java
package com.perfectjob.job.mapper;

import com.perfectjob.job.domain.model.Job;
import com.perfectjob.job.dto.JobResponse;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface JobMapper {

    @Mapping(target = "salaryDisplay", expression = "java(formatSalary(job))")
    JobResponse toResponse(Job job);

    default String formatSalary(Job job) {
        if (job.getSalaryMin() == null) return "A combinar";
        String currency = job.getSalaryCurrency() != null ? job.getSalaryCurrency() : "BRL";
        return String.format("%s %,.0f - %,.0f", currency, job.getSalaryMin(), job.getSalaryMax());
    }
}
```

### Pattern Matching (Java 21)

```java
public String formatExperience(Object experience) {
    return switch (experience) {
        case Integer years when years >= 5 -> "Sênior (" + years + " anos)";
        case Integer years when years >= 2 -> "Pleno (" + years + " anos)";
        case Integer years -> "Júnior (" + years + " ano(s))";
        case String desc -> desc;
        case null -> "Não informado";
    };
}
```

## References

- Spring Boot 3.4: https://docs.spring.io/spring-boot/docs/3.4.x/reference/html/
- Spring Security 6: https://docs.spring.io/spring-security/reference/
- MapStruct 1.6: https://mapstruct.org/documentation/stable/reference/html/
- Flyway 10: https://flywaydb.org/documentation/
- HikariCP: https://github.com/brettwooldridge/HikariCP
- Java 21 features: https://openjdk.org/projects/jdk/21/
- Gradle Kotlin DSL: https://docs.gradle.org/current/userguide/kotlin_dsl.html

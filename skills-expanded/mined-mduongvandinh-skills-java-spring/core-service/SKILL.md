# {{SERVICE_NAME_PASCAL}} Service Skill

## Service Type: Core Business Service

## Package Structure

```
com.company.{{SERVICE_NAME}}/
├── config/                 # Configuration classes
├── domain/
│   ├── model/              # @Entity, Value Objects
│   ├── repository/         # Repository interfaces
│   └── service/            # Domain services
├── application/
│   ├── usecase/            # @Service, business logic
│   ├── dto/                # Request/Response DTOs
│   └── mapper/             # MapStruct mappers
├── infrastructure/
│   ├── persistence/        # JPA Repository implementations
│   ├── messaging/          # Kafka producers/consumers
│   └── client/             # Feign clients
└── interfaces/
    ├── rest/               # @RestController
    └── event/              # @KafkaListener handlers
```

## Conventions

### Entity
```java
@Entity
@Table(name = "{{SERVICE_NAME}}s")
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class {{SERVICE_NAME_PASCAL}} {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    // fields
}
```

### Use Case (Application Service)
```java
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class Create{{SERVICE_NAME_PASCAL}}UseCase {
    private final {{SERVICE_NAME_PASCAL}}Repository repository;
    private final EventPublisher eventPublisher;

    public {{SERVICE_NAME_PASCAL}}Dto execute(Create{{SERVICE_NAME_PASCAL}}Request request) {
        // 1. Validate
        // 2. Create entity
        // 3. Save
        // 4. Publish event
        // 5. Return DTO
    }
}
```

### Controller
```java
@RestController
@RequestMapping("/api/{{SERVICE_NAME}}s")
@RequiredArgsConstructor
public class {{SERVICE_NAME_PASCAL}}Controller {
    private final Create{{SERVICE_NAME_PASCAL}}UseCase createUseCase;
    // other use cases
}
```

## Commands

```bash
# Run
mvn spring-boot:run

# Test
mvn test

# Build
mvn clean package
```

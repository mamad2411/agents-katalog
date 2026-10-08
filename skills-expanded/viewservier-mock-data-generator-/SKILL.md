# Mock Data Generator (Kafka Producer) - Cursor Rules

## Technology Stack
- Java 17
- Spring Boot 3.2
- Spring Kafka
- Maven
- Docker

## Code Guidelines

### Kafka Producer Best Practices
- Use `KafkaTemplate` for sending messages
- Implement proper serialization with JSON
- Include message size validation before sending
- Use proper partitioning strategies
- Implement error handling for failed sends

```java
// Preferred Kafka producer pattern
@Service
public class EventGenerator {
    
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final ObjectMapper objectMapper;
    private final MessageSizeValidator messageValidator;
    
    public EventGenerator(KafkaTemplate<String, String> kafkaTemplate, 
                         ObjectMapper objectMapper,
                         MessageSizeValidator messageValidator) {
        this.kafkaTemplate = kafkaTemplate;
        this.objectMapper = objectMapper;
        this.messageValidator = messageValidator;
    }
    
    public void sendGridEvent(GridEvent event) {
        try {
            String eventJson = objectMapper.writeValueAsString(event);
            
            if (messageValidator.isValidSize(eventJson)) {
                kafkaTemplate.send("grid-events", event.getGridId(), eventJson);
            } else {
                splitAndSendEvent(event);
            }
        } catch (Exception e) {
            log.error("Failed to send grid event", e);
        }
    }
}
```

### Message Size Management
- Always validate message sizes before sending to Kafka
- Target 10-50KB messages, max 100KB
- Implement automatic message splitting for oversized events
- Monitor and log message size statistics
- Use batch size limits (max 500 cells per message)

```java
// Preferred message size validation pattern
@Component
public class MessageSizeValidator {
    private static final int MAX_MESSAGE_SIZE = 100_000; // 100KB
    private static final int TARGET_MESSAGE_SIZE = 20_000; // 20KB
    private static final int MAX_CELLS_PER_MESSAGE = 500;
    
    public boolean isValidSize(String message) {
        return message.getBytes().length <= MAX_MESSAGE_SIZE;
    }
    
    public boolean isTargetSize(String message) {
        return message.getBytes().length <= TARGET_MESSAGE_SIZE;
    }
    
    public List<GridEvent> splitEvent(GridEvent largeEvent) {
        // Split logic for oversized events
    }
}
```

### Data Generation Patterns
- Generate realistic data patterns (strings, numbers, timestamps)
- Use controlled randomness with seeded Random instances
- Implement different data generation strategies
- Create patterns that simulate real-world usage
- Include edge cases and boundary values

```java
// Preferred data generation pattern
@Component
public class DataPatternService {
    private final Random random = new Random();
    
    public Object generateCellValue(DataType type) {
        return switch (type) {
            case STRING -> "Data_" + random.nextInt(10000);
            case NUMBER -> Math.round(random.nextDouble() * 1000 * 100.0) / 100.0;
            case INTEGER -> random.nextInt(1000);
            case TIMESTAMP -> System.currentTimeMillis();
            case PERCENTAGE -> Math.round(random.nextDouble() * 100 * 100.0) / 100.0;
        };
    }
    
    public String detectDataType(Object value) {
        if (value instanceof String) return "string";
        if (value instanceof Integer) return "integer";
        if (value instanceof Double) return "number";
        if (value instanceof Long) return "timestamp";
        return "unknown";
    }
}
```

### Load Simulation
- Implement configurable load patterns
- Support burst testing and steady-state testing
- Use `@Scheduled` for regular event generation
- Provide REST endpoints for load control
- Include realistic user behavior simulation

```java
// Preferred load simulation pattern
@Service
public class LoadSimulator {
    
    @Scheduled(fixedRate = 100) // Every 100ms
    public void generateRegularLoad() {
        if (isLoadTestEnabled()) {
            generateSmallBatchEvents();
        }
    }
    
    @Scheduled(fixedRate = 1000) // Every second
    public void generateBurstLoad() {
        if (isBurstTestEnabled()) {
            generateHighFrequencyBurst();
        }
    }
    
    private void generateSmallBatchEvents() {
        int batchCount = 1 + random.nextInt(3); // 1-3 small batches
        
        for (int i = 0; i < batchCount; i++) {
            GridEvent event = createSmallEvent();
            eventGenerator.sendGridEvent(event);
        }
    }
}
```

### Performance Optimization
- Use efficient JSON serialization settings
- Implement connection pooling for Kafka producers
- Batch message sending where appropriate
- Monitor producer metrics and throughput
- Use async sending with proper error handling

### Configuration Management
- Use application.yml for Kafka configuration
- Externalize load testing parameters
- Support environment-specific settings
- Include proper validation for configuration values

```yaml
# Preferred configuration pattern
spring:
  application:
    name: mock-data-generator
  kafka:
    bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS:localhost:9092}
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.apache.kafka.common.serialization.StringSerializer
      batch-size: 16384
      linger-ms: 5
      buffer-memory: 33554432
      max-request-size: 102400 # 100KB max message size

load-test:
  enabled: ${LOAD_TEST_ENABLED:false}
  burst-enabled: ${BURST_TEST_ENABLED:false}
  users-count: ${USERS_COUNT:10}
  views-per-user: ${VIEWS_PER_USER:5}
  update-frequency-ms: ${UPDATE_FREQUENCY:100}
```

### Monitoring and Metrics
- Track message generation rates
- Monitor message sizes and distributions
- Include Kafka producer metrics
- Log performance statistics
- Implement health checks

```java
// Preferred monitoring pattern
@Component
public class MessageMetrics {
    private final MeterRegistry meterRegistry;
    private final Counter messagesGenerated;
    private final Timer messageGenerationTime;
    private final Gauge messageSize;
    
    public MessageMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.messagesGenerated = Counter.builder("messages.generated")
            .description("Total messages generated")
            .register(meterRegistry);
        this.messageGenerationTime = Timer.builder("message.generation.time")
            .description("Time to generate and send messages")
            .register(meterRegistry);
    }
    
    public void recordMessageSent(int messageSize, long generationTime) {
        messagesGenerated.increment();
        messageGenerationTime.record(generationTime, TimeUnit.MILLISECONDS);
        // Record message size distribution
    }
}
```

### Error Handling
- Handle Kafka connection failures gracefully
- Implement retry logic for failed sends
- Log all generation and sending errors
- Provide fallback mechanisms for testing
- Include circuit breaker patterns

```java
// Preferred error handling pattern
@Service
public class RobustEventGenerator {
    
    @Retryable(value = {Exception.class}, maxAttempts = 3, backoff = @Backoff(delay = 1000))
    public void sendEventWithRetry(GridEvent event) {
        try {
            String eventJson = objectMapper.writeValueAsString(event);
            
            ListenableFuture<SendResult<String, String>> future = 
                kafkaTemplate.send("grid-events", event.getGridId(), eventJson);
                
            future.addCallback(
                result -> log.debug("Sent event successfully: {}", event.getGridId()),
                failure -> log.error("Failed to send event: {}", event.getGridId(), failure)
            );
        } catch (Exception e) {
            log.error("Error generating event", e);
            throw e; // Trigger retry
        }
    }
}
```

### Testing Utilities
- Provide REST endpoints for manual testing
- Include burst generation capabilities
- Support different load patterns
- Implement test data generation

```java
// Preferred testing controller pattern
@RestController
@RequestMapping("/api/test")
public class TestingController {
    
    private final EventGenerator eventGenerator;
    private final LoadSimulator loadSimulator;
    
    @PostMapping("/generate-burst")
    public ResponseEntity<String> generateBurst(
            @RequestParam int messageCount,
            @RequestParam(defaultValue = "10") int delayMs) {
        
        CompletableFuture.runAsync(() -> {
            for (int i = 0; i < messageCount; i++) {
                try {
                    eventGenerator.generateSmallEvent();
                    Thread.sleep(delayMs);
                } catch (Exception e) {
                    log.error("Error in burst generation", e);
                }
            }
        });
        
        return ResponseEntity.ok("Generating " + messageCount + " messages");
    }
    
    @PostMapping("/start-load/{userId}/{viewId}")
    public ResponseEntity<String> startTargetedLoad(
            @PathVariable String userId,
            @PathVariable String viewId,
            @RequestParam int updatesPerSecond) {
        
        loadSimulator.startTargetedLoad(userId, viewId, updatesPerSecond);
        return ResponseEntity.ok("Started targeted load");
    }
}
```

### Data Models
- Use simple, efficient data structures
- Implement proper serialization annotations
- Keep models focused and minimal
- Use builder patterns for complex objects

```java
// Preferred data model pattern
public record GridEvent(
    String eventType,
    String gridId,
    long timestamp,
    String batchId,
    List<CellChange> changes
) {
    public static Builder builder() {
        return new Builder();
    }
    
    public static class Builder {
        // Builder implementation
    }
}

public record CellChange(
    int row,
    int column,
    Object oldValue,
    Object newValue,
    String dataType
) {}
```

## File Structure
```
src/main/java/com/mockdata/
├── MockDataGeneratorApplication.java
├── config/
│   ├── KafkaProducerConfig.java
│   └── MetricsConfig.java
├── controller/
│   ├── TestingController.java
│   └── HealthController.java
├── service/
│   ├── EventGenerator.java
│   ├── LoadSimulator.java
│   ├── DataPatternService.java
│   └── MessageSizeValidator.java
├── model/
│   ├── GridEvent.java
│   ├── CellChange.java
│   └── DataType.java
├── metrics/
│   └── MessageMetrics.java
└── scheduler/
    └── LoadTestScheduler.java
```

## Common Patterns to Avoid
- Don't send oversized messages to Kafka (>100KB)
- Avoid blocking operations in scheduled methods
- Don't ignore Kafka producer errors
- Avoid generating too much data without rate limiting
- Don't use synchronous sending for high-throughput scenarios
- Avoid hardcoded test data (use configurable patterns)
- Don't forget to validate message sizes before sending 
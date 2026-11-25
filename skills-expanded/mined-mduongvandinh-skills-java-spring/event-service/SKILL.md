# {{SERVICE_NAME_PASCAL}} Service Skill

## Service Type: Event-Driven Service

Consumes events from Kafka and processes them.

## Characteristics

- **No REST API** - only consumes events
- **Kafka consumer** - subscribes to multiple topics
- **Optional database** - for storing state if needed
- **External integrations** - email, SMS, push notifications

## Package Structure

```
com.company.{{SERVICE_NAME}}/
├── config/         # Kafka configuration
├── handler/        # @KafkaListener event handlers
└── service/        # Business logic
```

## Event Handling Pattern

```java
@KafkaListener(topics = "${app.kafka.topics.user-events}")
public void handleUserEvent(UserCreatedEvent event) {
    log.info("Received: {}", event.getEventId());
    service.processUserCreated(event);
}
```

## Error Handling

- Automatic retry (3 attempts)
- Dead letter queue for failed messages
- Logging and alerting

## Adding New Event Handler

1. Add event class to `event-lib`
2. Create handler in `handler/` package
3. Add topic to `application.yml`
4. Implement processing in service

## Commands

```bash
# Run
mvn spring-boot:run

# Test with Kafka
# Publish test event to topic
```

## Health Checks

```bash
curl http://localhost:8080/actuator/health
```

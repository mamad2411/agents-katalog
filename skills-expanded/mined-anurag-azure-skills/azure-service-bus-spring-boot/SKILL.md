---
name: "azure-service-bus-spring-boot"
description: "Implement Azure Service Bus messaging in the LeadPerfection Spring Boot 4.x / Java 21 target microservices — Transactional Outbox pattern, domain event publishing, topic/subscription consumers, dead-letter handling, idempotency, and observability."
version: 1
created: "2026-06-21"
updated: "2026-06-21"
---
## When to Use
Use this skill whenever you need to:
- Add Azure Service Bus messaging to a target domain microservice (e.g., SalesService EP-03)
- Implement the Transactional Outbox pattern (ADR §15.4) for reliable at-least-once event publishing
- Write a domain event publisher (AppointmentResulted, AssignmentCreated, etc.)
- Write a topic subscription consumer in a downstream service (EP-04, EP-07, EP-11)
- Configure DLQ monitoring, retry policies, and idempotency
- Wire up OpenTelemetry tracing across Service Bus message headers
- Generate pom.xml dependencies, application.yml config, and Spring beans for Service Bus

Stack alignment:
- Spring Boot 4.0.x → spring-cloud-azure-dependencies 7.3.0
- Java 21 (Virtual Threads — use synchronous ServiceBusSenderClient, not async)
- Auth: DefaultAzureCredential (Managed Identity in Azure; Azure CLI locally)
- Pattern: Transactional Outbox + Spring Boot Poller (ADR §15.4)
- Broker: Azure Service Bus Standard/Premium tier (topics + subscriptions)

## Procedure
1. STEP 1 — ADD POM DEPENDENCIES: Add to pom.xml inside <dependencyManagement> the Spring Cloud Azure BOM, and inside <dependencies> the two Service Bus artifacts. For Spring Boot 4.0.x use spring-cloud-azure-dependencies 7.3.0.

<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>com.azure.spring</groupId>
      <artifactId>spring-cloud-azure-dependencies</artifactId>
      <version>7.3.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <!-- Azure Service Bus direct SDK (for Outbox dispatcher) -->
  <dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-messaging-servicebus</artifactId>
  </dependency>
  <!-- Azure Identity for DefaultAzureCredential -->
  <dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
  </dependency>
  <!-- Spring Cloud Azure Stream Binder (for consumer @Bean style) -->
  <dependency>
    <groupId>com.azure.spring</groupId>
    <artifactId>spring-cloud-azure-stream-binder-servicebus</artifactId>
  </dependency>
</dependencies>
2. STEP 2 — CONFIGURE application.yml: Add Service Bus namespace and binding config. Use env-var placeholders for secrets; never hard-code connection strings.

spring:
  cloud:
    azure:
      servicebus:
        namespace: ${AZURE_SERVICEBUS_NAMESPACE}   # e.g. lp-servicebus-dev
    stream:
      bindings:
        # Consumer binding (downstream services)
        consume-in-0:
          destination: ${AZURE_SERVICEBUS_TOPIC_NAME}     # e.g. sales.appointment.events
          group: ${AZURE_SERVICEBUS_SUBSCRIPTION_NAME}    # e.g. lead-service-sub
      servicebus:
        bindings:
          consume-in-0:
            consumer:
              auto-complete: false   # manual checkpoint for at-least-once
              entity-type: topic
      function:
        definition: consume
      poller:
        fixed-delay: 60000
        initial-delay: 0
  jms:
    servicebus:
      namespace: ${AZURE_SERVICEBUS_NAMESPACE}
      pricing-tier: standard    # or premium
      passwordless-enabled: true
    listener:
      receive-timeout: 60000

azure:
  servicebus:
    fully-qualified-namespace: ${AZURE_SERVICEBUS_NAMESPACE}.servicebus.windows.net
3. STEP 3 — CREATE OUTBOX TABLE (Liquibase): Add a changeset to create the outbox table used by the Transactional Outbox pattern.

<changeSet id='S-xxx-outbox' author='migration-team'>
  <createTable schemaName='sales_schema' tableName='outbox_events'>
    <column name='id' type='BIGINT' autoIncrement='true'><constraints primaryKey='true'/></column>
    <column name='event_id' type='VARCHAR(36)'><constraints nullable='false' unique='true'/></column>
    <column name='event_type' type='VARCHAR(100)'><constraints nullable='false'/></column>
    <column name='topic' type='VARCHAR(200)'><constraints nullable='false'/></column>
    <column name='partition_key' type='VARCHAR(50)'><constraints nullable='false'/></column>
    <column name='payload' type='TEXT'><constraints nullable='false'/></column>
    <column name='status' type='VARCHAR(20)' defaultValue='PENDING'><constraints nullable='false'/></column>
    <column name='created_at' type='TIMESTAMP' defaultValueComputed='NOW()'/>
    <column name='published_at' type='TIMESTAMP'/>
    <column name='retry_count' type='INT' defaultValueNumeric='0'/>
    <column name='error_message' type='TEXT'/>
  </createTable>
  <createIndex tableName='outbox_events' schemaName='sales_schema' indexName='idx_outbox_status'>
    <column name='status'/><column name='created_at'/>
  </createIndex>
  <rollback><dropTable schemaName='sales_schema' tableName='outbox_events'/></rollback>
</changeSet>
4. STEP 4 — DOMAIN EVENT RECORD: Define an immutable domain event Java Record with all required envelope fields.

public record DomainEvent(
    String eventId,          // UUID — idempotency key
    String eventType,        // e.g. 'AppointmentResulted'
    String eventVersion,     // '1.0'
    String tenantId,         // X-Tenant-Ids value
    String correlationId,    // from MDC X-Correlation-ID
    String traceId,          // W3C trace context
    Instant timestamp,
    Object payload           // event-specific payload record
) {
    public static DomainEvent of(String eventType, String tenantId, Object payload) {
        return new DomainEvent(
            UUID.randomUUID().toString(),
            eventType, '1.0', tenantId,
            MDC.get('correlationId'),
            MDC.get('traceId'),
            Instant.now(), payload);
    }
}
5. STEP 5 — OUTBOX ENTITY + REPOSITORY: Create JPA entity and repository for the outbox table.

@Entity @Table(name='outbox_events', schema='sales_schema')
public class OutboxEvent {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
    @Column(name='event_id', nullable=false, unique=true) private String eventId;
    @Column(name='event_type', nullable=false) private String eventType;
    @Column(name='topic', nullable=false) private String topic;
    @Column(name='partition_key', nullable=false) private String partitionKey;
    @Column(name='payload', columnDefinition='TEXT', nullable=false) private String payload;
    @Column(name='status', nullable=false) private String status; // PENDING/PUBLISHED/FAILED
    @Column(name='created_at', updatable=false) private LocalDateTime createdAt;
    @Column(name='published_at') private LocalDateTime publishedAt;
    @Column(name='retry_count') private int retryCount;
    @Column(name='error_message', columnDefinition='TEXT') private String errorMessage;
}

public interface OutboxEventRepository extends JpaRepository<OutboxEvent, Long> {
    List<OutboxEvent> findTop100ByStatusOrderByCreatedAtAsc(String status);
    // Used by poller — fetch PENDING or FAILED with retryCount < 3
    @Query('SELECT o FROM OutboxEvent o WHERE o.status IN (:statuses) AND o.retryCount < 3 ORDER BY o.createdAt ASC')
    List<OutboxEvent> findPendingEvents(@Param('statuses') List<String> statuses, Pageable pageable);
}
6. STEP 6 — OUTBOX PUBLISHER SERVICE: Service that writes domain events to the outbox table IN THE SAME TRANSACTION as the business operation.

@Service @RequiredArgsConstructor
public class OutboxPublisherService {
    private final OutboxEventRepository outboxRepo;
    private final ObjectMapper objectMapper;

    // Call this INSIDE the same @Transactional as the business save — do NOT commit separately
    public void publish(String topic, String partitionKey, DomainEvent event) {
        try {
            OutboxEvent outbox = new OutboxEvent();
            outbox.setEventId(event.eventId());
            outbox.setEventType(event.eventType());
            outbox.setTopic(topic);
            outbox.setPartitionKey(partitionKey);   // always tenantId for ordered processing
            outbox.setPayload(objectMapper.writeValueAsString(event));
            outbox.setStatus('PENDING');
            outbox.setCreatedAt(LocalDateTime.now());
            outbox.setRetryCount(0);
            outboxRepo.save(outbox);   // commits with business tx
        } catch (JsonProcessingException e) {
            throw new RuntimeException('Failed to serialize domain event', e);
        }
    }
}
7. STEP 7 — SERVICE BUS SENDER CONFIG: Configure ServiceBusSenderClient beans per topic using DefaultAzureCredential (Managed Identity).

@Configuration @RequiredArgsConstructor
public class ServiceBusConfig {
    @Value('${azure.servicebus.fully-qualified-namespace}') private String fqNamespace;

    // Reuse one builder — clients are expensive to create
    private ServiceBusClientBuilder builder() {
        return new ServiceBusClientBuilder()
            .credential(fqNamespace, new DefaultAzureCredentialBuilder().build());
    }

    @Bean(destroyMethod='close')
    public ServiceBusSenderClient appointmentEventSender() {
        return builder().sender().topicName('sales.appointment.events').buildClient();
    }

    @Bean(destroyMethod='close')
    public ServiceBusSenderClient scheduleEventSender() {
        return builder().sender().topicName('sales.schedule.events').buildClient();
    }

    @Bean(destroyMethod='close')
    public ServiceBusSenderClient assignmentEventSender() {
        return builder().sender().topicName('sales.assignment.events').buildClient();
    }
}
8. STEP 8 — OUTBOX DISPATCHER (Spring Scheduler Poller): Scheduled poller reads PENDING outbox rows and publishes to Azure Service Bus. Runs every 60 seconds.

@Component @RequiredArgsConstructor @Slf4j
public class OutboxDispatcher {
    private final OutboxEventRepository outboxRepo;
    private final Map<String, ServiceBusSenderClient> senderMap; // topic -> client
    private final ObjectMapper objectMapper;

    @Scheduled(fixedDelay = 60_000, initialDelay = 5_000)
    @Transactional
    public void dispatch() {
        List<OutboxEvent> pending = outboxRepo.findPendingEvents(
            List.of('PENDING','FAILED'), PageRequest.of(0, 100));
        for (OutboxEvent outbox : pending) {
            try {
                ServiceBusSenderClient sender = senderMap.get(outbox.getTopic());
                if (sender == null) { log.error('No sender for topic: {}', outbox.getTopic()); continue; }

                ServiceBusMessage msg = new ServiceBusMessage(outbox.getPayload())
                    .setMessageId(outbox.getEventId())           // idempotency key
                    .setPartitionKey(outbox.getPartitionKey())   // tenantId for ordering
                    .setContentType('application/json')
                    .setSubject(outbox.getEventType());

                // Propagate OpenTelemetry trace headers
                msg.getApplicationProperties().put('traceId', MDC.get('traceId'));
                msg.getApplicationProperties().put('correlationId', MDC.get('correlationId'));

                sender.sendMessage(msg);

                outbox.setStatus('PUBLISHED');
                outbox.setPublishedAt(LocalDateTime.now());
                log.info('Published event {} type={} topic={}', outbox.getEventId(), outbox.getEventType(), outbox.getTopic());
            } catch (Exception e) {
                outbox.setRetryCount(outbox.getRetryCount() + 1);
                outbox.setErrorMessage(e.getMessage());
                if (outbox.getRetryCount() >= 3) outbox.setStatus('FAILED');
                log.error('Failed to publish event {}: {}', outbox.getEventId(), e.getMessage());
            }
            outboxRepo.save(outbox);
        }
    }
}
9. STEP 9 — CONSUMER (Downstream Service): Implement a topic subscription consumer in a downstream service using Spring Cloud Stream @Bean style with manual checkpoint for at-least-once delivery.

@SpringBootApplication @EnableScheduling
public class LeadServiceApplication {
    // Consumer bean name must match spring.cloud.function.definition in application.yml
    @Bean
    public Consumer<Message<String>> consume(
            ObjectMapper objectMapper, AppointmentEventHandler handler) {
        return message -> {
            Checkpointer checkpointer = (Checkpointer) message.getHeaders().get(CHECKPOINTER);
            String eventId = (String) message.getHeaders().getOrDefault('messageId','');
            String correlationId = (String) message.getHeaders().getOrDefault('correlationId','');
            MDC.put('correlationId', correlationId);
            try {
                // IDEMPOTENCY CHECK — skip if already processed
                if (handler.isAlreadyProcessed(eventId)) {
                    log.info('Skipping duplicate event {}', eventId);
                    checkpointer.success().block();
                    return;
                }
                DomainEvent event = objectMapper.readValue(message.getPayload(), DomainEvent.class);
                handler.handle(event);                   // your business logic
                handler.markProcessed(eventId);          // write to processed_events table
                checkpointer.success()
                    .doOnSuccess(s -> log.info('Checkpointed event {}', eventId))
                    .doOnError(e -> log.error('Checkpoint failed for {}', eventId))
                    .block();
            } catch (Exception e) {
                log.error('Error processing event {}: {}', eventId, e.getMessage());
                // Do NOT checkpoint — message will be redelivered (at-least-once)
                // After maxDeliveryCount (3) it moves to DLQ automatically
            } finally {
                MDC.clear();
            }
        };
    }
}
10. STEP 10 — IDEMPOTENCY TABLE (Liquibase): Add a processed_events table to prevent duplicate processing in consumers.

<changeSet id='S-xxx-processed-events' author='migration-team'>
  <createTable schemaName='lead_schema' tableName='processed_events'>
    <column name='event_id' type='VARCHAR(36)'><constraints primaryKey='true'/></column>
    <column name='event_type' type='VARCHAR(100)'/>
    <column name='processed_at' type='TIMESTAMP' defaultValueComputed='NOW()'/>
    <column name='tenant_id' type='VARCHAR(50)'/>
  </createTable>
  <rollback><dropTable schemaName='lead_schema' tableName='processed_events'/></rollback>
</changeSet>
11. STEP 11 — ENABLE SCHEDULING: Add @EnableScheduling to the main application class or a @Configuration class so the Outbox Dispatcher runs.

@SpringBootApplication
@EnableScheduling
public class SalesServiceApplication {
    public static void main(String[] args) { SpringApplication.run(SalesServiceApplication.class, args); }
}
12. STEP 12 — DLQ MONITORING: Add a Spring Actuator health indicator and alert on DLQ depth > 0. Wire to Grafana via Micrometer.

@Component @RequiredArgsConstructor
public class ServiceBusDlqHealthIndicator implements HealthIndicator {
    private final ServiceBusAdministrationClient adminClient;
    @Value('${azure.servicebus.topic}') private String topic;
    @Value('${azure.servicebus.subscription}') private String subscription;

    @Override
    public Health health() {
        SubscriptionRuntimeProperties props = adminClient
            .getSubscriptionRuntimeProperties(topic, subscription);
        long dlqCount = props.getDeadLetterMessageCount();
        if (dlqCount > 0) {
            return Health.down().withDetail('dlqCount', dlqCount)
                         .withDetail('topic', topic).build();
        }
        return Health.up().withDetail('dlqCount', 0).build();
    }
}

// Also expose as Micrometer gauge for Grafana alerting:
@Bean
public Gauge dlqGauge(MeterRegistry registry, ServiceBusAdministrationClient adminClient,
                      @Value('${azure.servicebus.topic}') String topic,
                      @Value('${azure.servicebus.subscription}') String sub) {
    return Gauge.builder('servicebus.dlq.count', adminClient,
        c -> c.getSubscriptionRuntimeProperties(topic, sub).getDeadLetterMessageCount())
        .tag('topic', topic).tag('subscription', sub)
        .register(registry);
}

## Pitfalls
- Spring Boot 4.0.x REQUIRES spring-cloud-azure-dependencies 7.3.0 — do NOT use 5.x or 6.x versions. The wrong BOM version will cause class-not-found errors at runtime.
- Java 21 Virtual Threads (Spring MVC non-reactive stack) — use ServiceBusSenderClient (synchronous), NOT ServiceBusSenderAsyncClient. Never mix async/reactive clients into the non-reactive stack.
- DefaultAzureCredential order of resolution: Managed Identity (Azure) → Azure CLI (local dev) → Environment vars. Developers must run 'az login' locally. Never hard-code connection strings in application.yml.
- NEVER call outboxPublisherService.publish() OUTSIDE a @Transactional boundary. The outbox write MUST be in the same database transaction as the business entity save. If the business tx rolls back, the outbox row must also roll back.
- The Outbox Dispatcher @Scheduled method must also be @Transactional so outbox status updates (PUBLISHED/FAILED) are committed atomically. If publishing succeeds but the status update fails, the event will be re-published — consumers must be idempotent.
- Service Bus Standard tier supports Topics + Subscriptions. Basic tier does NOT — do not use Basic for EP-03 event patterns. Use Standard or Premium.
- ServiceBusSenderClient and ServiceBusReceiverClient are expensive to create — always declare them as Spring @Beans (singleton scope) with destroyMethod='close'. Never instantiate them per-request.
- Partition key MUST be tenantId to guarantee message ordering within a tenant. Do NOT use appointmentId or a random value — that breaks per-tenant ordering guarantees.
- auto-complete: false is REQUIRED for at-least-once delivery. If you set auto-complete: true, messages are acknowledged before your handler runs, so crashes = message loss.
- maxDeliveryCount on the Azure Service Bus subscription MUST be set to 3 (matching the retry policy). Messages exceeding this go to DLQ automatically. Set this in the Azure portal or ARM template, NOT in Spring config.
- The eventId in the ServiceBusMessage.setMessageId() enables Service Bus native deduplication only if the namespace has duplicate detection enabled (Premium tier). Still implement your own processed_events table as the idempotency store for portability.
- OpenTelemetry trace headers (traceparent/tracestate) must be manually propagated into ServiceBusMessage application properties when using the raw SDK. Spring Cloud Azure Stream Binder does this automatically.
- When using @Scheduled + @Transactional together on the same method, ensure the transaction is managed by Spring (default). Do NOT use TransactionSynchronizationManager manually — it is handled by @Transactional.

## Verification
1. mvn dependency:tree | grep 'azure-messaging-servicebus\|spring-cloud-azure-stream-binder\|azure-identity' — all three should appear with version from BOM 7.3.0
2. Application startup log must contain: 'ServiceBusClientBuilder' bean initialized — no ClassNotFoundException or BeanCreationException
3. Outbox table exists: SELECT COUNT(*) FROM sales_schema.outbox_events — should return 0 on fresh schema
4. Processed events table exists in consumer service schema: SELECT COUNT(*) FROM lead_schema.processed_events
5. Publish a test event: call a write endpoint (e.g., POST /api/v1/sales/appointments/update), then SELECT * FROM sales_schema.outbox_events WHERE status='PENDING' — row should appear
6. After 60 seconds, the Outbox Dispatcher should run: SELECT * FROM sales_schema.outbox_events WHERE status='PUBLISHED' — row status should change
7. Consumer receives message: check application log for 'Checkpointed event <uuid>' in the downstream service
8. DLQ health indicator at GET /actuator/health shows 'servicebus.dlq' component with status UP and dlqCount=0
9. Grafana dashboard shows 'servicebus.dlq.count' gauge = 0 for all topic/subscription combinations
10. Idempotency: send the same event twice (same eventId). Consumer log should show 'Skipping duplicate event <uuid>' on second delivery
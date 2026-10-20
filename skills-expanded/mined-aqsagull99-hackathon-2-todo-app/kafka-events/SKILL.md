---
name: kafka-events
description: Master Apache Kafka for building event-driven architectures from hello world to professional production systems. This skill covers installation, configuration, development patterns, security, monitoring, and troubleshooting for robust Kafka implementations. Use when working with Apache Kafka for event streaming, including setup, topic management, producer/consumer configuration, security, monitoring, and troubleshooting.
---

# Apache Kafka Events Skill

Master Apache Kafka for building event-driven architectures from hello world to professional production systems. This skill covers installation, configuration, development patterns, security, monitoring, and troubleshooting for robust Kafka implementations.

## Table of Contents
1. [Architecture Fundamentals](#architecture-fundamentals)
2. [Installation and Setup](#installation-and-setup)
3. [Topic Management](#topic-management)
4. [Producer Configuration](#producer-configuration)
5. [Consumer Configuration](#consumer-configuration)
6. [Health Probes and Monitoring](#health-probes-and-monitoring)
7. [Troubleshooting Patterns](#troubleshooting-patterns)
8. [Security Configuration](#security-configuration)
9. [Production Best Practices](#production-best-practices)

## Architecture Fundamentals

### Core Components
Kafka's architecture consists of:

- **Brokers**: Server nodes that store data and serve clients
- **Topics**: Categories or feeds to which records are published
- **Partitions**: Sub-divisions of topics for parallel processing
- **Producers**: Applications that publish records to topics
- **Consumers**: Applications that subscribe to topics and process records
- **Consumer Groups**: Collections of consumers that share a common group ID

### KRaft Mode Architecture
Modern Kafka clusters use KRaft (Kafka Raft metadata mode) instead of ZooKeeper:

```properties
# KRaft mode configuration
process.roles=broker,controller
node.id=1
controller.quorum.bootstrap.servers=localhost:9093

# Network configuration
listeners=PLAINTEXT://:9092,CONTROLLER://:9093
advertised.listeners=PLAINTEXT://localhost:9092
inter.broker.listener.name=PLAINTEXT
controller.listener.names=CONTROLLER
```

## Installation and Setup

### Quick Start with KRaft Mode
Set up a single-node Kafka cluster in KRaft mode:

```bash
# Generate cluster ID
CLUSTER_ID=$(bin/kafka-storage.sh random-uuid)
echo "Cluster ID: $CLUSTER_ID"

# Format storage (first time only)
bin/kafka-storage.sh format --standalone -t $CLUSTER_ID -c config/kraft/server.properties

# Start broker
bin/kafka-server-start.sh config/kraft/server.properties
```

### KRaft Server Properties Template
Configuration for KRaft mode operation:

```properties
# KRaft mode configuration (replaces ZooKeeper)
process.roles=broker,controller
node.id=1
controller.quorum.bootstrap.servers=localhost:9093

# Cluster ID (generate with: bin/kafka-storage.sh random-uuid)
# Format storage: bin/kafka-storage.sh format --standalone -t <CLUSTER_ID> -c config/server.properties

# Network listeners
listeners=PLAINTEXT://:9092,CONTROLLER://:9093
advertised.listeners=PLAINTEXT://localhost:9092
inter.broker.listener.name=PLAINTEXT
controller.listener.names=CONTROLLER
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL

# Threading configuration
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

# Log storage
log.dirs=/tmp/kraft-combined-logs
num.partitions=1
num.recovery.threads.per.data.dir=2

# Replication
offsets.topic.replication.factor=3
transaction.state.log.replication.factor=3
transaction.state.log.min.isr=2
default.replication.factor=3
min.insync.replicas=2

# Share group coordinator (for share consumer groups)
share.coordinator.state.topic.replication.factor=3
share.coordinator.state.topic.min.isr=2

# Log retention
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000

# Log cleanup policy
log.cleanup.policy=delete
log.cleaner.enable=true

# Compression
compression.type=producer
```

## Topic Management

### Creating Topics
Create topics with appropriate partitioning and replication:

```bash
# Create a topic with custom partitions and replication
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic my-topic \
  --partitions 20 --replication-factor 3 --config retention.ms=604800000

# Create a topic with specific configurations
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic my-topic \
  --partitions 1 --replication-factor 1 \
  --config max.message.bytes=64000 \
  --config flush.messages=1
```

### Topic Configuration Best Practices
Configure topics for optimal performance:

```bash
# Configure for high-throughput, low-latency scenarios
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic high-throughput-topic \
  --partitions 50 --replication-factor 3 \
  --config min.insync.replicas=2 \
  --config cleanup.policy=compact \
  --config segment.bytes=1073741824 \
  --config retention.ms=259200000  # 3 days

# Configure for durability-focused scenarios
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic durable-topic \
  --partitions 10 --replication-factor 3 \
  --config min.insync.replicas=3 \
  --config cleanup.policy=delete \
  --config retention.ms=604800000  # 7 days
```

## Producer Configuration

### Basic Producer Setup
Configure producers with appropriate settings for reliability:

```java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.*;
import java.util.Properties;

Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

// Reliability settings
props.put(ProducerConfig.ACKS_CONFIG, "all");  // Wait for all replicas to acknowledge
props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);
props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);  // Exactly-once semantics

// Performance settings
props.put(ProducerConfig.BATCH_SIZE_CONFIG, 16384);
props.put(ProducerConfig.LINGER_MS_CONFIG, 5);
props.put(ProducerConfig.BUFFER_MEMORY_CONFIG, 33554432);

KafkaProducer<String, String> producer = new KafkaProducer<>(props);

// Send messages with callbacks for error handling
ProducerRecord<String, String> record = new ProducerRecord<>("my-topic", "key", "value");
producer.send(record, new Callback() {
    public void onCompletion(RecordMetadata metadata, Exception exception) {
        if (exception != null) {
            exception.printStackTrace();
        } else {
            System.out.printf("Message sent to topic %s, partition %d, offset %d%n",
                metadata.topic(), metadata.partition(), metadata.offset());
        }
    }
});
```

### Transactional Producer Configuration
For exactly-once semantics across multiple topics/partitions:

```java
// Configure transactional producer
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "prod-1");
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

KafkaProducer<String, String> producer = new KafkaProducer<>(props);

// Initialize transactions (must be called once)
producer.initTransactions();

try {
    // Begin transaction
    producer.beginTransaction();

    // Send multiple messages atomically
    producer.send(new ProducerRecord<>("output-topic", "key1", "value1"));
    producer.send(new ProducerRecord<>("output-topic", "key2", "value2"));
    producer.send(new ProducerRecord<>("another-topic", "key3", "value3"));

    // Commit transaction (all or nothing)
    producer.commitTransaction();
    System.out.println("Transaction committed successfully");

} catch (ProducerFencedException | OutOfOrderSequenceException | AuthorizationException e) {
    // Fatal errors - close producer
    producer.close();
    throw e;
} catch (KafkaException e) {
    // Transient error - abort and retry
    producer.abortTransaction();
    System.err.println("Transaction aborted: " + e.getMessage());
}

producer.close();
```

## Consumer Configuration

### Basic Consumer Setup
Configure consumers with proper offset management and error handling:

```java
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.serialization.*;
import org.apache.kafka.common.TopicPartition;
import java.time.Duration;
import java.util.*;

// Consumer configuration
Properties props = new Properties();
props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(ConsumerConfig.GROUP_ID_CONFIG, "my-consumer-group");
props.put(ConsumerConfig.CLIENT_ID_CONFIG, "client-" + UUID.randomUUID());
props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);  // Manual offset management
props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");  // Start from beginning if no offset
props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 500);  // Limit records per poll
props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, 30000);  // Session timeout
props.put(ConsumerConfig.HEARTBEAT_INTERVAL_MS_CONFIG, 10000);  // Heartbeat interval

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);

// Subscribe to topics with rebalance listener
consumer.subscribe(
    Collections.singletonList("my-topic"),
    new ConsumerRebalanceListener() {
        @Override
        public void onPartitionsRevoked(Collection<TopicPartition> partitions) {
            System.out.println("Partitions revoked: " + partitions);
            // Commit pending offsets before rebalance
            consumer.commitSync();
        }

        @Override
        public void onPartitionsAssigned(Collection<TopicPartition> partitions) {
            System.out.println("Partitions assigned: " + partitions);
            // Initialize state or seek to specific offsets
        }
    }
);

try {
    while (true) {
        // Poll for records (blocks up to 1 second)
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));

        for (ConsumerRecord<String, String> record : records) {
            System.out.printf("Consumed record: key=%s, value=%s, partition=%d, offset=%d%n",
                record.key(), record.value(), record.partition(), record.offset());

            // Process record
            processRecord(record);
        }

        // Manually commit offsets after processing
        consumer.commitSync();

    }
} catch (Exception e) {
    System.err.println("Consumer error: " + e.getMessage());
} finally {
    consumer.close();
}

void processRecord(ConsumerRecord<String, String> record) {
    // Implementation details for processing a single record
}
```

### Consumer Group Management
Best practices for consumer group configuration:

```bash
# List consumer groups
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

# Describe a consumer group
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my-group

# Reset consumer group offsets
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group --reset-offsets --to-earliest --topic my-topic

# Delete a consumer group
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --delete --group my-group
```

## Health Probes and Monitoring

### Liveness and Readiness Probes for Kafka Applications
Configure health checks for Kafka-based applications:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kafka-app
spec:
  containers:
  - name: app
    image: my-kafka-app:latest
    ports:
    - containerPort: 8080
    # Liveness probe to check if Kafka connection is healthy
    livenessProbe:
      exec:
        command: ["/bin/sh", "-c", "echo dump | nc localhost 9092 | grep -q 'Connected'"]
      initialDelaySeconds: 30
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
    # Readiness probe to check if app can connect to Kafka
    readinessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
      timeoutSeconds: 3
      failureThreshold: 3
    env:
    - name: KAFKA_BOOTSTRAP_SERVERS
      value: "kafka-cluster:9092"
    - name: KAFKA_CONSUMER_GROUP_ID
      value: "my-app-consumer-group"
```

### Kafka Application Health Endpoint Implementation
Implement health checks in Kafka applications:

```java
@RestController
public class HealthController {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @GetMapping("/healthz")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        Map<String, Object> health = new HashMap<>();

        try {
            // Test Kafka connectivity
            kafkaTemplate.send("health-test-topic", "health-check", "ping");

            health.put("status", "UP");
            health.put("kafka", "CONNECTED");
            health.put("timestamp", System.currentTimeMillis());

            return ResponseEntity.ok(health);
        } catch (Exception e) {
            health.put("status", "DOWN");
            health.put("kafka", "DISCONNECTED");
            health.put("error", e.getMessage());

            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(health);
        }
    }

    @GetMapping("/readyz")
    public ResponseEntity<Map<String, Object>> readinessCheck() {
        Map<String, Object> readiness = new HashMap<>();

        try {
            // Check if consumer group is active
            // This would typically involve checking consumer lag
            // and other application-specific readiness criteria

            readiness.put("status", "READY");
            readiness.put("consumers", "ACTIVE");
            readiness.put("timestamp", System.currentTimeMillis());

            return ResponseEntity.ok(readiness);
        } catch (Exception e) {
            readiness.put("status", "NOT_READY");
            readiness.put("error", e.getMessage());

            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(readiness);
        }
    }
}
```

### JMX Monitoring Configuration
Enable JMX metrics for Kafka broker monitoring:

```bash
# Enable remote JMX monitoring for Kafka brokers
export JMX_PORT=9999

# For production, enable security with KAFKA_JMX_OPTS
export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote.authenticate=true -Dcom.sun.management.jmxremote.ssl=true"
```

### Key Kafka Metrics to Monitor
Track important Kafka metrics for health and performance:

```bash
# Broker metrics
kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions
kafka.server:type=ReplicaManager,name=OfflinePartitionsCount
kafka.server:type=KafkaController,name=ActiveControllerCount

# Consumer metrics
kafka.consumer:type=consumer-fetch-manager-metrics,client-id=[client-id]
kafka.consumer:type=consumer-coordinator-metrics,client-id=[client-id]

# Producer metrics
kafka.producer:type=producer-metrics,client-id=[client-id]

# Consumer lag monitoring
kafka.server:type=FetcherLagMetrics,name=ConsumerLag,clientId=([-\.\\w]+),topic=([-\.\\w]+),partition=([0-9]+)
```

## Troubleshooting Patterns

### Common Consumer Issues and Solutions

#### Consumer Lag Issues
Diagnose and resolve consumer lag problems:

```bash
# Check consumer group lag
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my-consumer-group

# Reset consumer offsets to earliest
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-consumer-group --reset-offsets --to-earliest --topic my-topic --execute

# Reset consumer offsets to latest
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-consumer-group --reset-offsets --to-latest --topic my-topic --execute

# Reset consumer offsets to specific timestamp
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-consumer-group --reset-offsets --to-datetime 2023-01-01T00:00:00 --topic my-topic --execute
```

#### Connection and Authentication Issues
Troubleshoot connection problems:

```bash
# Test broker connectivity
telnet localhost 9092

# Check if broker is running
netstat -tuln | grep 9092

# Verify consumer group connectivity
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

# Check for authentication issues
# For SASL/SCRAM:
# security.protocol=SASL_SSL
# sasl.mechanism=SCRAM-SHA-256

# For SASL/PLAIN:
# security.protocol=SASL_SSL
# sasl.mechanism=PLAIN
```

### Producer Troubleshooting

#### Message Delivery Issues
Resolve common producer problems:

```java
// Add error handling for producer send operations
ProducerRecord<String, String> record = new ProducerRecord<>("my-topic", "key", "value");
Future<RecordMetadata> future = producer.send(record, new Callback() {
    public void onCompletion(RecordMetadata metadata, Exception exception) {
        if (exception != null) {
            // Log the exception
            System.err.println("Error sending message: " + exception.getMessage());

            // Handle specific exceptions
            if (exception instanceof TimeoutException) {
                System.err.println("Message send timed out");
            } else if (exception instanceof RecordTooLargeException) {
                System.err.println("Message is too large");
            } else if (exception instanceof SerializationException) {
                System.err.println("Serialization error");
            } else {
                System.err.println("Other error: " + exception.getClass().getName());
            }
        } else {
            System.out.printf("Message sent successfully to topic %s, partition %d, offset %d%n",
                metadata.topic(), metadata.partition(), metadata.offset());
        }
    }
});

try {
    // Wait for send to complete with timeout
    RecordMetadata metadata = future.get(5, TimeUnit.SECONDS);
    System.out.printf("Message sent to topic %s, partition %d, offset %d%n",
        metadata.topic(), metadata.partition(), metadata.offset());
} catch (InterruptedException | ExecutionException | TimeoutException e) {
    System.err.println("Send operation failed: " + e.getMessage());
    future.cancel(true); // Cancel the send operation
}
```

### Topic and Partition Troubleshooting

#### Partition Imbalance Issues
Address partition distribution problems:

```bash
# Check topic partition distribution
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic my-topic

# Check partition leadership distribution
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic my-topic | grep -E "Leader:|Replicas:"

# Reassign partitions if needed (requires partition reassignment JSON file)
bin/kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --reassignment-json-file reassignment.json --execute

# Verify reassignment status
bin/kafka-reassign-partitions.sh --bootstrap-server localhost:9092 --verify --reassignment-json-file reassignment.json
```

## Security Configuration

### SSL/TLS Configuration
Secure Kafka communication with SSL/TLS:

```properties
# SSL Configuration for Kafka Brokers
listeners=SSL://:9093
security.inter.broker.protocol=SSL
ssl.keystore.location=/path/to/keystore.jks
ssl.keystore.password=keystore_password
ssl.key.password=key_password
ssl.truststore.location=/path/to/truststore.jks
ssl.truststore.password=truststore_password
ssl.client.auth=required
```

### SASL Authentication
Configure SASL for authentication:

```properties
# SASL/SCRAM Configuration
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-256  # or SCRAM-SHA-512

# SASL/PLAIN Configuration
security.protocol=SASL_SSL
sasl.mechanism=PLAIN

# SASL/OAUTHBEARER Configuration
security.protocol=SASL_SSL
sasl.mechanism=OAUTHBEARER
sasl.jaas.config=org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required ;
```

### Client Security Configuration
Secure client connections:

```java
Properties props = new Properties();
props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9093");
props.put(ConsumerConfig.GROUP_ID_CONFIG, "my-consumer-group");
props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);

// SSL configuration
props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SSL");
props.put(SslConfigs.SSL_TRUSTSTORE_LOCATION_CONFIG, "/path/to/truststore.jks");
props.put(SslConfigs.SSL_TRUSTSTORE_PASSWORD_CONFIG, "truststore_password");
props.put(SslConfigs.SSL_KEYSTORE_LOCATION_CONFIG, "/path/to/keystore.jks");
props.put(SslConfigs.SSL_KEYSTORE_PASSWORD_CONFIG, "keystore_password");
props.put(SslConfigs.SSL_KEY_PASSWORD_CONFIG, "key_password");

// SASL/SCRAM configuration
props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
props.put(SaslConfigs.SASL_MECHANISM, "SCRAM-SHA-256");
props.put(SaslConfigs.SASL_JAAS_CONFIG,
    "org.apache.kafka.common.security.scram.ScramLoginModule required " +
    "username=\"myuser\" " +
    "password=\"mypassword\";");
```

## Production Best Practices

### AI Agent-Specific Configuration
For AI agents with slow initialization, configure appropriate probe timing:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-agent-kafka-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-agent-kafka-app
  template:
    metadata:
      labels:
        app: ai-agent-kafka-app
    spec:
      containers:
      - name: ai-agent
        image: ai-agent-kafka:latest
        ports:
        - containerPort: 8080
        # AI agent with slow initialization - longer probe delays
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 180  # AI models may take longer to load
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 5
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8080
          initialDelaySeconds: 120  # Wait for model loading
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 15
          timeoutSeconds: 5
          failureThreshold: 30  # Allow up to 7.5 minutes for AI model loading
        env:
        - name: KAFKA_BOOTSTRAP_SERVERS
          value: "kafka-cluster:9092"
        - name: MODEL_LOADING_TIMEOUT
          value: "300"  # 5 minutes for model loading
        - name: KAFKA_CONSUMER_GROUP_ID
          value: "ai-agent-consumer-group"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

### Kafka Streams Configuration
Build real-time stream processing applications:

```java
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;
import java.util.Properties;
import java.util.concurrent.CountDownLatch;

// Configure Streams application
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "ai-stream-processor");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.StringSerde.class);
props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.StringSerde.class);
props.put(StreamsConfig.CACHE_MAX_BYTES_BUFFERING_CONFIG, 0);
props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
props.put(StreamsConfig.COMMIT_INTERVAL_MS_CONFIG, 1000);  // Commit more frequently for AI apps

// Build topology for AI event processing
StreamsBuilder builder = new StreamsBuilder();

// Process AI events with windowing
KStream<String, String> source = builder.stream("ai-input-events");

KStream<String, String> processed = source
    .filter((key, value) -> value != null && !value.isEmpty())
    .mapValues(value -> processAIEvent(value))
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
    .aggregate(
        () -> "",  // Initializer
        (key, value, aggregate) -> aggregate + value,  // Adder
        Materialized.with(Serdes.String(), Serdes.String())  // Materialized store
    )
    .toStream()
    .map((windowedKey, value) -> new KeyValue<>(windowedKey.key(), value));

processed.to("ai-processed-events", Produced.with(Serdes.String(), Serdes.String()));

// Start application
KafkaStreams streams = new KafkaStreams(builder.build(), props);
CountDownLatch latch = new CountDownLatch(1);

// Add shutdown hook
Runtime.getRuntime().addShutdownHook(new Thread("streams-shutdown-hook") {
    @Override
    public void run() {
        streams.close();
        latch.countDown();
    }
});

streams.start();
latch.await();

String processAIEvent(String event) {
    // AI-specific event processing logic
    return event.toUpperCase(); // Placeholder
}
```

### Performance Tuning
Optimize Kafka for high-performance scenarios:

```properties
# Producer tuning for high throughput
acks=all
retries=2147483647
max.in.flight.requests.per.connection=5
enable.idempotence=true
batch.size=16384
linger.ms=5
buffer.memory=33554432
compression.type=snappy

# Consumer tuning for low latency
fetch.min.bytes=1
fetch.max.wait.ms=500
max.partition.fetch.bytes=1048576
max.poll.records=100

# Broker tuning
num.network.threads=8
num.io.threads=16
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
num.replica.fetchers=4
replica.fetch.max.bytes=1048576
replica.fetch.wait.max.ms=500
```

### Monitoring and Alerting
Set up comprehensive monitoring:

```bash
# Check broker health
bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092

# Monitor consumer lag
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my-consumer-group

# Monitor topic metrics
bin/kafka-run-class.sh kafka.tools.JmxTool --object-name kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec --jmx-url service:jmx:rmi:///jndi/rmi://localhost:9999/jmxrmi

# Monitor cluster state
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --under-replicated-partitions
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --unavailable-partitions
```

## Coupling Types in Event-Driven Architecture

Event-driven architectures using Apache Kafka significantly reduce coupling between services. Understanding the different types of coupling and how events address them is crucial for designing robust distributed systems.

### 1. Temporal Coupling

**Definition**: Temporal coupling occurs when components must interact at the same time. In traditional synchronous communication (e.g., REST API calls), the caller must wait for the callee to respond before continuing.

**How Events Solve It**:
- Producers publish events to Kafka topics without waiting for consumers
- Consumers process events asynchronously when they're ready
- Services can operate independently without blocking each other
- Provides resilience against service downtime

**Kafka Implementation**:
```java
// Producer publishes event without waiting for consumer
ProducerRecord<String, String> record = new ProducerRecord<>("user-events", userId, userEventData);
producer.send(record); // Non-blocking operation
// Producer continues with other work immediately
```

### 2. Availability Coupling

**Definition**: Availability coupling occurs when all participating services must be available simultaneously for communication to succeed. In synchronous systems, if one service is down, the entire interaction fails.

**How Events Solve It**:
- Kafka acts as a buffer between services, storing events until consumers are ready
- If a consumer service is temporarily unavailable, events remain in the topic
- When the service recovers, it can process missed events
- Provides loose coupling and fault tolerance

**Kafka Implementation**:
```bash
# Even if consumer service is down, events are persisted
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic user-events
# Events are stored in Kafka and available when consumer comes back online
```

### 3. Behavioral Coupling

**Definition**: Behavioral coupling occurs when components have tight dependencies on each other's behavior, interfaces, or data formats. Changes in one service often require corresponding changes in others.

**How Events Solve It**:
- Well-defined event schemas provide stable contracts between services
- Services can evolve independently as long as they maintain schema compatibility
- Event versioning allows for backward and forward compatibility
- Services can choose which events to consume based on their needs

**Kafka Implementation**:
```java
// Define clear event contracts
public class UserCreatedEvent {
    private String userId;
    private String email;
    private long timestamp;
    // ... getters and setters
}

// Producer and consumer agree on event structure
// Services can evolve independently as long as schema contracts are maintained
```

## Event-Driven Architecture Fundamentals

Understanding the core components and principles of event-driven architecture is essential for building robust systems with Apache Kafka.

### Core Components

#### Producers
Producers are client applications that publish (write) events to Kafka topics. Key characteristics:
- Publish events asynchronously without waiting for consumer acknowledgment
- Fully decoupled from consumers - no dependency on consumer availability
- Can batch events for efficiency
- Support various delivery guarantees (at-most-once, at-least-once, exactly-once)

**Producer Example**:
```java
// Producer publishes events without waiting for consumers
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

KafkaProducer<String, String> producer = new KafkaProducer<>(props);

// Asynchronously send event
ProducerRecord<String, String> record = new ProducerRecord<>("user-events", "user-id", "user-data");
producer.send(record, (metadata, exception) -> {
    if (exception != null) {
        exception.printStackTrace();
    } else {
        System.out.printf("Event sent to topic %s, partition %d, offset %d%n",
            metadata.topic(), metadata.partition(), metadata.offset());
    }
});
```

#### Consumers
Consumers are client applications that subscribe to (read and process) events from Kafka topics. Key characteristics:
- Pull events from topics at their own pace
- Can form consumer groups for load balancing and fault tolerance
- Maintain their position (offset) in the topic
- Support various processing guarantees

**Consumer Example**:
```java
Properties props = new Properties();
props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(ConsumerConfig.GROUP_ID_CONFIG, "my-consumer-group");
props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Collections.singletonList("user-events"));

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));
    for (ConsumerRecord<String, String> record : records) {
        System.out.printf("Processing event: key=%s, value=%s, partition=%d, offset=%d%n",
            record.key(), record.value(), record.partition(), record.offset());

        // Process the event
        processEvent(record);
    }

    // Commit offsets after processing
    consumer.commitSync();
}
```

### Consistency Models and Eventual Consistency

#### Eventual Consistency in Kafka
Eventual consistency is a fundamental characteristic of event-driven systems where the system guarantees that, given no new updates, all nodes will eventually converge to the same state. In Kafka:

- Events are delivered asynchronously to consumers
- There's a time delay between event production and consumption
- Different consumers may see events at different times
- The system state becomes consistent over time as events are processed

#### Delivery Guarantees
Kafka provides three levels of delivery guarantees:

1. **At-most-once delivery**: Events may be lost but are never redelivered
   - Achieved with auto commit enabled
   - Fastest but least reliable

2. **At-least-once delivery**: Events are never lost but may be duplicated
   - Achieved by disabling auto commit and manually committing after processing
   - Recommended for most use cases

3. **Exactly-once delivery**: Events are delivered once and only once
   - Achieved using Kafka transactions and idempotent producers
   - Most complex but provides strongest guarantee

**Exactly-Once Example**:
```java
// Configure for exactly-once semantics
Properties producerProps = new Properties();
producerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
producerProps.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
producerProps.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "processor-1");

KafkaProducer<String, String> producer = new KafkaProducer<>(producerProps);
producer.initTransactions();

// Begin transaction
producer.beginTransaction();

try {
    // Process events and produce results atomically
    producer.send(new ProducerRecord<>("output-topic", "key1", "value1"));
    producer.send(new ProducerRecord<>("output-topic", "key2", "value2"));

    // Commit transaction (all or nothing)
    producer.commitTransaction();
} catch (Exception e) {
    producer.abortTransaction();
}
```

### When to Use Event-Driven Architecture

#### Choose EDA When:
1. **Loose Coupling**: Need to decouple services temporally, availability-wise, and behaviorally
2. **High Scalability**: Systems need to scale independently
3. **Real-time Processing**: Require near real-time event processing
4. **System Integration**: Integrating heterogeneous systems
5. **Audit Requirements**: Need complete audit trail of all changes
6. **Resilience**: Need systems to continue operating despite partial failures

#### Avoid EDA When:
1. **Strong Consistency**: Need immediate consistency across all systems
2. **Simple Interactions**: Simple request-response patterns suffice
3. **Low Latency**: Cannot tolerate the inherent latency of asynchronous processing
4. **Complex Debugging**: Team lacks experience with distributed tracing and debugging

### How Eventual Consistency Affects System Design

#### Design Implications:
1. **User Experience**: Design UIs to handle eventual consistency (e.g., optimistic UI updates)
2. **Business Logic**: Account for the fact that different parts of the system may see different states
3. **Error Handling**: Plan for scenarios where events arrive out of order or late
4. **Data Modeling**: Design data models that can handle eventual consistency

#### Patterns for Managing Eventual Consistency:
1. **CQRS (Command Query Responsibility Segregation)**: Separate read and write models
2. **SAGA Pattern**: Coordinate distributed transactions using a sequence of local transactions
3. **Compensating Actions**: Implement undo operations for failed business processes
4. **Event Sourcing**: Store the sequence of events that determine the current state

## Event-Driven Architecture Benefits

Using Apache Kafka for event-driven architecture provides these decoupling benefits:

1. **Scalability**: Services can scale independently based on their specific workload
2. **Resilience**: Failure in one service doesn't immediately impact others
3. **Flexibility**: New services can be added as consumers of existing events
4. **Audit Trail**: All events are logged, providing a complete history of system changes
5. **Replay Capability**: Historical events can be replayed for debugging or new feature implementation

Following these patterns will help you build robust, scalable, and maintainable event-driven architectures with Apache Kafka.
---
name: streaming-pipeline
description: Design real-time streaming pipelines with Kafka, Flink, Spark Streaming. Outputs producer/consumer patterns, windowing, state management, and exactly-once semantics.
argument-hint: [data volume, latency requirements, processing needs]
allowed-tools: Read, Write, Bash
---

# Streaming Data Pipeline

Design real-time data pipelines for continuous processing. Not batch ETL — streaming with Kafka, Flink, Spark, handling out-of-order events, windowing, and exactly-once semantics.

## Process

1. **Define requirements.** Latency (< 1s), throughput (10k events/sec), ordering guarantees.
2. **Choose architecture.** Message queue (Kafka), stream processor (Flink/Spark), storage.
3. **Design producers.** Event schema, partitioning strategy, error handling.
4. **Build consumers.** Consumer groups, offset management, idempotency.
5. **Add processing.** Windowing, aggregations, joins, state management.
6. **Handle failures.** Exactly-once semantics, checkpointing, replay.
7. **Monitor pipeline.** Lag, throughput, error rate, end-to-end latency.

## Output Format

### Streaming Pipeline: [Use Case]

**Architecture:** Kafka + Flink  
**Throughput:** 50k events/sec  
**Latency:** p95 < 500ms  
**Guarantees:** Exactly-once processing  
**Windowing:** 5-minute tumbling windows

---

## Architecture

```
┌─────────────┐
│  Producer   │ (App servers, IoT devices)
└──────┬──────┘
       │ Events
       ▼
┌─────────────┐
│    Kafka    │ (Message queue, durability)
│   3 brokers │
└──────┬──────┘
       │ Consume
       ▼
┌─────────────┐
│    Flink    │ (Stream processing)
│  Job Manager│
└──────┬──────┘
       │ Output
       ▼
┌─────────────┐
│ Elasticsearch│ (Search, analytics)
│  PostgreSQL │ (Transactional data)
└─────────────┘
```

---

## Kafka Basics

### Topics & Partitions
```
Topic: user-events
├─ Partition 0: [Event1, Event3, Event5] → Consumer A
├─ Partition 1: [Event2, Event4, Event6] → Consumer B
└─ Partition 2: [Event7, Event8, Event9] → Consumer C

Replication Factor: 3 (each partition on 3 brokers)
```

### Producer (Python)
```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['kafka1:9092', 'kafka2:9092', 'kafka3:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',  # Wait for all replicas
    retries=3,
    max_in_flight_requests_per_connection=1  # Preserve order
)

# Send event
event = {
    'user_id': '12345',
    'event_type': 'page_view',
    'page': '/products',
    'timestamp': '2024-03-21T10:30:00Z'
}

future = producer.send(
    'user-events',
    value=event,
    key=event['user_id'].encode('utf-8')  # Partition by user_id
)

# Wait for acknowledgment
metadata = future.get(timeout=10)
print(f"Sent to partition {metadata.partition}, offset {metadata.offset}")

producer.flush()
producer.close()
```

### Consumer (Python)
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['kafka1:9092'],
    group_id='analytics-consumer',
    auto_offset_reset='earliest',  # Start from beginning if no offset
    enable_auto_commit=False,  # Manual offset commit
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    event = message.value
    
    try:
        # Process event
        process_event(event)
        
        # Manually commit offset (exactly-once)
        consumer.commit()
    except Exception as e:
        print(f"Error processing: {e}")
        # Don't commit, will reprocess on restart
```

---

## Partitioning Strategy

### By User ID (Ordered per user)
```python
# All events for user go to same partition
key = user_id.encode('utf-8')
producer.send('events', value=event, key=key)
```

### By Event Type (Parallel processing)
```python
# page_view, click, purchase to different partitions
key = event_type.encode('utf-8')
```

### Round-Robin (Even distribution)
```python
# No key = round-robin
producer.send('events', value=event)
```

**Choose partitioning based on:**
- Ordering requirements (key needed)
- Load balancing (avoid hot partitions)
- Processing locality (related events together)

---

## Apache Flink

### Stream Processing Job
```java
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;

public class UserEventProcessor {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // Enable checkpointing (exactly-once)
        env.enableCheckpointing(60000);  // Every 60 seconds
        
        // Kafka consumer
        FlinkKafkaConsumer<UserEvent> consumer = new FlinkKafkaConsumer<>(
            "user-events",
            new UserEventSchema(),
            properties
        );
        
        DataStream<UserEvent> events = env.addSource(consumer);
        
        // Filter and transform
        DataStream<UserEvent> pageViews = events
            .filter(event -> event.getType().equals("page_view"));
        
        // Window aggregation (count per 5 minutes)
        DataStream<PageViewCount> counts = pageViews
            .keyBy(UserEvent::getPage)
            .window(TumblingEventTimeWindows.of(Time.minutes(5)))
            .aggregate(new CountAggregator());
        
        // Write to sink
        counts.addSink(new ElasticsearchSink<>(config));
        
        env.execute("User Event Processor");
    }
}
```

---

## Windowing

### Tumbling Window (Non-overlapping)
```
Time: [00:00 - 05:00] [05:00 - 10:00] [10:00 - 15:00]
      └─ Window 1 ─┘ └─ Window 2 ─┘ └─ Window 3 ─┘
```

```java
.window(TumblingEventTimeWindows.of(Time.minutes(5)))
```

### Sliding Window (Overlapping)
```
Time: [00:00 - 10:00]
         [05:00 - 15:00]
            [10:00 - 20:00]
```

```java
.window(SlidingEventTimeWindows.of(Time.minutes(10), Time.minutes(5)))
// Size: 10 min, Slide: 5 min
```

### Session Window (Dynamic, based on gaps)
```
Events: [e1, e2] ---- (gap > 5 min) ---- [e3, e4, e5]
        └Window 1┘                       └─ Window 2 ─┘
```

```java
.window(EventTimeSessionWindows.withGap(Time.minutes(5)))
```

---

## Event Time vs Processing Time

### Event Time (Recommended)
```
Event timestamp: When event actually occurred
Watermark: Indicates "all events before time T have arrived"

Timeline:
Event1 (10:00:00) → Arrives 10:00:05
Event2 (10:00:02) → Arrives 10:00:03 (out of order!)
Event3 (10:00:04) → Arrives 10:00:06
```

```java
// Assign event timestamps and watermarks
events.assignTimestampsAndWatermarks(
    WatermarkStrategy.<UserEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
        .withTimestampAssigner((event, timestamp) -> event.getTimestamp())
);
```

### Processing Time
```
Timestamp: When Flink processes the event
Simpler but doesn't handle out-of-order or late events
```

---

## Exactly-Once Semantics

### Problem: Duplicates or Lost Data
```
Scenario 1: At-least-once (duplicates)
Process event → Crash before commit → Reprocess on restart

Scenario 2: At-most-once (data loss)
Commit offset → Crash before processing → Skip event
```

### Solution: Transactional Processing
```java
// Flink checkpointing + Kafka transactions
env.enableCheckpointing(60000);

// Sink with exactly-once
FlinkKafkaProducer<Result> producer = new FlinkKafkaProducer<>(
    "results",
    new ResultSchema(),
    properties,
    FlinkKafkaProducer.Semantic.EXACTLY_ONCE  // Transactional
);
```

**How it works:**
1. Flink periodically checkpoints state
2. On failure, restart from last checkpoint
3. Kafka transactions ensure outputs written once

---

## State Management

### Keyed State (Per-key state)
```java
public class UserSessionTracker extends RichMapFunction<Event, Session> {
    private ValueState<Session> sessionState;
    
    @Override
    public void open(Configuration config) {
        ValueStateDescriptor<Session> descriptor =
            new ValueStateDescriptor<>("session", Session.class);
        sessionState = getRuntimeContext().getState(descriptor);
    }
    
    @Override
    public Session map(Event event) throws Exception {
        Session current = sessionState.value();
        
        if (current == null) {
            current = new Session(event.getUserId());
        }
        
        current.addEvent(event);
        sessionState.update(current);
        
        return current;
    }
}
```

### RocksDB State Backend (Large state)
```java
env.setStateBackend(new EmbeddedRocksDBStateBackend());
env.getCheckpointConfig().setCheckpointStorage("s3://bucket/checkpoints");
```

---

## Spark Structured Streaming

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col

spark = SparkSession.builder.appName("UserEvents").getOrCreate()

# Read from Kafka
events = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka1:9092") \
    .option("subscribe", "user-events") \
    .load()

# Parse JSON
from pyspark.sql.functions import from_json
schema = "user_id STRING, event_type STRING, page STRING, timestamp TIMESTAMP"

parsed = events.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Windowed aggregation
page_views = parsed \
    .filter(col("event_type") == "page_view") \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("page")
    ) \
    .count()

# Write to console (or database, Kafka, etc.)
query = page_views.writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

query.awaitTermination()
```

---

## Monitoring

### Kafka Metrics
```bash
# Consumer lag (how far behind)
kafka-consumer-groups.sh --bootstrap-server kafka1:9092 \
    --describe --group analytics-consumer

GROUP           TOPIC       PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
analytics       user-events 0          12345           12350           5
analytics       user-events 1          23456           23456           0
analytics       user-events 2          34567           34570           3
```

**Alert if lag > 1000:** Consumer can't keep up

### Flink Metrics
```
Checkpoint Duration: Time to complete checkpoint
Records Processed: Throughput
Records Lag: Backpressure indicator
Task Failures: Error rate
```

### Prometheus Exporter
```yaml
# prometheus.yml
- job_name: 'kafka'
  static_configs:
    - targets: ['kafka-exporter:9308']

- job_name: 'flink'
  static_configs:
    - targets: ['flink-jobmanager:9249']
```

---

## Error Handling

### Dead Letter Queue (DLQ)
```python
def process_event(event):
    try:
        # Process
        result = transform(event)
        send_to_output(result)
    except ValidationError as e:
        # Invalid event, send to DLQ
        send_to_dlq(event, error=str(e))
    except Exception as e:
        # Transient error, raise to retry
        raise
```

### Circuit Breaker for External Calls
```python
from pybreaker import CircuitBreaker

breaker = CircuitBreaker(fail_max=5, timeout_duration=60)

@breaker
def call_external_api(data):
    return requests.post('https://api.example.com', json=data)

# If API fails 5 times, circuit opens for 60 seconds
```

---

## Schema Evolution

### Avro Schema Registry
```python
from confluent_kafka.avro import AvroProducer
from confluent_kafka import avro

# Define schema
value_schema = avro.loads('''
{
  "type": "record",
  "name": "UserEvent",
  "fields": [
    {"name": "user_id", "type": "string"},
    {"name": "event_type", "type": "string"},
    {"name": "timestamp", "type": "long"}
  ]
}
''')

producer = AvroProducer({
    'bootstrap.servers': 'kafka1:9092',
    'schema.registry.url': 'http://schema-registry:8081'
}, default_value_schema=value_schema)

# Produce with schema validation
producer.produce(topic='events', value={
    'user_id': '123',
    'event_type': 'click',
    'timestamp': 1640000000
})
```

**Benefits:**
- Automatic serialization/deserialization
- Schema validation
- Backward/forward compatibility

---

## Performance Optimization

### Parallelism
```java
// Flink parallelism
env.setParallelism(10);  // 10 parallel tasks

// Per-operator parallelism
events.map(new MyMapper()).setParallelism(5);
```

### Batch Processing in Stream
```java
// Mini-batches for efficiency
events.countWindowAll(1000)  // Process 1000 events at a time
    .apply(new BatchProcessor());
```

### Compression
```python
# Kafka producer compression
producer = KafkaProducer(
    compression_type='snappy'  # or 'gzip', 'lz4'
)
```

## Rules

- Partition by key for ordering guarantees — events with same key always go to same partition.
- Enable checkpointing for exactly-once — without it, you only get at-least-once or at-most-once.
- Use event time, not processing time — handles out-of-order and late events correctly.
- Set watermarks with bounded out-of-orderness — allow 5-10 second delay for late events.
- Monitor consumer lag continuously — lag > threshold means consumer can't keep up.
- Use dead letter queues for poison pills — invalid events shouldn't block pipeline.
- Backpressure indicates bottleneck — slow sink or insufficient parallelism.
- State backend (RocksDB) required for large state — in-memory won't scale.
- Schema registry for production — prevents deserialization errors from schema changes.
- Test with replay — ability to reprocess historical data is critical for debugging.

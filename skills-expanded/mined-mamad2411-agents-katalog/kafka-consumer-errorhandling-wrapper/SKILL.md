---
name: kafka-consumer-errorhandling-wrapper
description: Wrap key/value deserializers in Spring Kafka's ErrorHandlingDeserializer so a single poison record doesn't halt the consumer
category: backend
version: 1.0.0
source:
  kind: project
  ref: lucida-performance@0536094
trigger: Avro / JSON Kafka consumer that would otherwise die on a malformed record and get stuck re-reading the same offset
tags: [kafka, spring-kafka, avro, poison-pill, resilience]
---

# kafka-consumer-errorhandling-wrapper

## Rule
Never set `KafkaAvroDeserializer` directly as the consumer's deserializer. Always wrap
with `ErrorHandlingDeserializer` so a bad record becomes a logged failure instead of
a stuck partition.

## Shape
```java
cfg.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, ErrorHandlingDeserializer.class);
cfg.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, ErrorHandlingDeserializer.class);
cfg.put(ErrorHandlingDeserializer.KEY_DESERIALIZER_CLASS, StringDeserializer.class);
cfg.put(ErrorHandlingDeserializer.VALUE_DESERIALIZER_CLASS, KafkaAvroDeserializer.class);
cfg.put(KafkaAvroDeserializerConfig.SPECIFIC_AVRO_READER_CONFIG, true);
```

## Pair with
- `DefaultErrorHandler` + DLT (`DeadLetterPublishingRecoverer`) so poison records are
  observable, not silently dropped.
- `SeekToCurrentErrorHandler` only for retryable errors — deserialization failures are
  not retryable.

## Not suitable when
- You rely on the consumer failing fast on schema drift — then don't wrap; instead gate
  at the schema-registry compatibility setting.

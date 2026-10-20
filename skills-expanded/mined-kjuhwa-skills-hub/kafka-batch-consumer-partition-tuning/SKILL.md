---
tags: [backend, kafka, batch, consumer, partition, tuning]
name: kafka-batch-consumer-partition-tuning
description: Size Kafka partition count + max-poll-records per topic volume so heavy-processing batch consumers avoid max.poll.interval.ms breaches and maintain throughput via per-partition concurrency.
trigger: Spring Kafka batch listener processes heavy records (DB writes, metric evaluation); consumers periodically rebalance due to max.poll.interval.ms timeout.
source_project: lucida-alarm
version: 1.0.0
category: backend
linked_knowledge:
  - kafka-batch-size-timeout-tuning
  - kafka-partition-topology-design
---

# Kafka Batch Consumer Partition Tuning

## Shape

Two knobs control whether a batch listener survives heavy load:
1. **Partition count** per topic — scaled by volume; upper bound on listener concurrency.
2. **`max-poll-records`** — scaled **down** for heavy work so `poll()` cadence stays well inside `max.poll.interval.ms`.

## Steps

1. Classify topics by volume: high-volume (measurements, metrics) vs. low-volume (config changes, admin).
2. Provision partition count accordingly (e.g. `9` for high, `3` for low).
3. Listener factory: `setBatchListener(true)` + `setConcurrency(numPartitions)` — one thread per partition.
4. **Lower** `max-poll-records` for heavy consumers (e.g. `10`). Per-poll overhead is tiny in Spring Kafka; more frequent polls beat fatter batches.
5. `AckMode.BATCH` — offsets commit after each batch, not per record.
6. `setAutoStartup(false)` — start containers programmatically after service-dependency checks.
7. Wrap key/value deserializers with `ErrorHandlingDeserializer` and attach a `DeadLetterPublishingRecoverer`.
8. Expose queue/lag metrics via Actuator/Prometheus.

## Counter / Caveats

- Don't over-partition low-volume topics — metadata + replication overhead with no benefit.
- Partition count is costly to shrink; size deliberately (~3× current peak, not 10×).
- I/O-bound workloads are capped at one-thread-per-partition — extra concurrency wastes threads.
- See linked knowledge entries for the project-specific rationale on batch-size and partition topology.

---
name: queues-and-workers
description: Design message queues and worker pools. Use when building
  queue-based async systems.
metadata:
  tags: queues, workers
---

# Queues & Workers

## Use this skill when
- Choosing a queue and consuming pattern
- Scaling workers and handling backpressure
- Implementing delayed jobs and priorities
- Handling DLQs and message reprocessing

## Do not use this skill when
- Single deferred job needs (use background-jobs)
- Streaming/event-sourcing concerns

## Instructions
1. Pick a queue matching durability and ordering needs (Redis, SQS, RabbitMQ, Kafka).
2. Consume with short leases/acknowledgement and re-queue on failure.
3. Make workers horizontally scalable and stateless.
4. Handle backpressure: honor concurrency limits, watch memory.
5. Separate DLQ and alert on poison messages.
6. Add priority and delay queues where latency matters.
7. Measure lag, throughput, and retry counts.

## Checklist
- At-least-once semantics are handled (idempotency)
- DLQ is monitored
- Ordering requirements are explicit

## Output Format
- Queue | producer | consumer | semantics | DLQ | scale plan

## Common Mistakes
- Assuming exactly-once delivery
- Workers with shared mutable state
- No max-retry: infinite redelivery loop

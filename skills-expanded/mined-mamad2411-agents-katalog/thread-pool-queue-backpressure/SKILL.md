---
tags: [backend, thread, pool, queue, backpressure]
name: thread-pool-queue-backpressure
description: Bounded in-memory queue between Kafka consumer and async thread pool, with hysteretic pause/resume thresholds driving Spring Kafka container pause()/resume() so bursts do not OOM the JVM.
trigger: Kafka consumer hands off to an async worker pool; bursts overflow memory or stall GC without backpressure.
source_project: lucida-alarm
version: 1.0.0
category: backend
---

# Thread-Pool Queue Backpressure

## Shape

- Bounded `BlockingQueue` (e.g. capacity 10 000) + fixed-size worker thread pool.
- Consumer enqueues; workers dequeue and process.
- A monitor computes `utilization = size / capacity`. When it crosses `PAUSE_THRESHOLD` upward, pause the Kafka container; when it crosses `RESUME_THRESHOLD` downward, resume.

## Steps

1. Define thresholds with hysteresis gap (e.g. `PAUSE=0.9`, `RESUME=0.5`) to prevent flapping.
2. In listener, `queue.put(dto)` (blocks when full — backpressure of last resort).
3. After every `put`, compute utilization.
4. `> PAUSE` → `KafkaListenerEndpointRegistry.getListenerContainer(id).pause()`.
5. `< RESUME` → `.resume()`.
6. `AtomicBoolean queueFullWarned` so "queue full" logs **once per burst**, not per record.
7. `@PreDestroy`: `shutdown()` → `awaitTermination(60s)` → `shutdownNow()`; log remaining queue size on forced shutdown.
8. `@Scheduled(cron = "0 * * * * ?")` periodic observability log: queue size + active worker count + last pause/resume transition.

## Counter / Caveats

- Pausing a Kafka consumer still counts against `max.poll.interval.ms` — pair with small `max-poll-records`.
- Hysteresis gap must be wide enough. `PAUSE=0.9` / `RESUME=0.85` will flap under steady load.
- If pause is too aggressive (threshold too low), consumer may never resume once paused under sustained inflow.
- `queue.put()` inside the listener blocks; if you use a listener thread pool, this is fine — if not, it serializes partitions.

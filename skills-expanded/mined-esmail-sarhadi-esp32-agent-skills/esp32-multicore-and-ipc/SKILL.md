---
name: esp32-multicore-and-ipc
description: Use when code behaves differently depending on which core it runs on - a task starves the Wi-Fi stack, a shared variable corrupts, a queue overflows, or a task never runs at all. Covers affinity, priorities, spinlocks and ISR dispatch.
license: MIT
---

# Two cores on ESP32

The classic ESP32 and the S3 have two cores. The C3, C6 and S2 have one, so code
that assumed two cores silently becomes cooperative - and a blocking task that
was fine on core 1 now stops the radio.

## Core 0 belongs to the radio

The Wi-Fi and Bluetooth stacks run on core 0 at high priority. A busy loop pinned
to core 0 starves them and the symptom is not "slow Wi-Fi", it is a watchdog
reset or a disconnect every few seconds. Pin application work to core 1.

`xTaskCreatePinnedToCore(..., 1)` for anything that computes, and leave core 0
alone unless you are writing a driver.

## Priorities are absolute, not fair

A task at priority 10 that never blocks prevents every task below it from
running, forever. `vTaskDelay(1)` is the cheapest yield that still lets lower
tasks run; `taskYIELD()` only helps equal priorities.

The IDF default for `loopTask` is priority 1. A driver task at 5 that waits on a
semaphore is fine; a driver task at 5 that spins is not.

## Sharing data between cores

- `volatile` is not a lock. It stops the compiler caching the value; it does not
  make a 32-bit read-modify-write atomic.
- Use a mutex for structures, a `portMUX_TYPE` spinlock for a few variables
  touched from an ISR, and a queue when you can - it is the only one that also
  gives you backpressure.
- Never take a mutex inside an ISR. Never call `delay()` while holding a spinlock.

## The ISR is not a task

An ISR runs on whichever core took the interrupt, with interrupts disabled. It
must do the minimum and hand off:

- `IRAM_ATTR` on the handler, or it may not be in memory when flash is busy.
- `xQueueSendFromISR` / `xTaskNotifyFromISR`, then `portYIELD_FROM_ISR`.
- No `printf`, no `malloc`, no flash access, no I2C transaction.

A `printf` in an ISR works on the bench and crashes during an OTA write, because
the log goes to flash-backed buffers.

## Queues: the overflow is the design

A queue of 10 items between a 100 Hz producer and a 10 Hz consumer is not a
queue, it is a delay. Decide what happens on overflow before it happens: drop the
oldest (sensor data), block the producer (commands), or grow (nothing - it will
fill too).

| Symptom | Usually |
|---|---|
| Wi-Fi drops under load | work pinned to core 0 |
| one task never runs | a higher-priority task never blocks |
| values corrupt, no crash | shared struct without a lock |
| crash inside an ISR | log, malloc or flash access in the handler |
| works on C3, fails on ESP32 | code assumed a single core, or vice versa |

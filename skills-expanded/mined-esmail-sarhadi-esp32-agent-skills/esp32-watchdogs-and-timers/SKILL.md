---
name: esp32-watchdogs-and-timers
description: Use when the board resets by itself, a long operation trips the task watchdog, a timer callback crashes, or the reset reason says watchdog but the code looks fine. Covers TWDT, the interrupt watchdog, esp_timer and what is safe inside a callback.
license: MIT
---

# Watchdogs and timers on ESP32

There are three watchdogs and they reset the chip for different reasons. Reading
`esp_reset_reason()` before anything else turns a mystery into a category.

## The three watchdogs

| Watchdog | Default | Trips when |
|---|---|---|
| Task watchdog (TWDT) | 5 s, per subscribed task | a subscribed task does not yield |
| Interrupt watchdog (IWDT) | 300 ms | interrupts are disabled too long |
| RTC watchdog | at boot | the bootloader or a stall before the app runs |

The task watchdog only watches tasks that subscribed. A blocked task that never
subscribed resets nothing - it just stops working, which is worse.

## What actually trips the TWDT

- A blocking call inside a subscribed task: `delay()` in a loop, a synchronous
  HTTP request, `while (!ready)` on a peripheral.
- A higher-priority task that never blocks. Priority inversion looks exactly like
  a hung task.
- `vTaskDelay(0)` - yields without feeding the watchdog's expectation of progress
  in some drivers.

The fix is never "call `esp_task_wdt_reset()` more often". Feed the watchdog by
making progress, not by lying to it.

## esp_timer callbacks are not tasks

Callbacks run in the timer task context with a small stack, at high priority.
Inside one:

- No blocking calls, no `delay()`, no flash writes, no logging through a mutex
  that another task holds.
- Keep it under a few hundred microseconds and hand the work to a queue.
- A periodic timer that occasionally takes 2 ms will eventually trip the TWDT on
  the timer task itself.

## Software timers vs hardware timers

`esp_timer` is a 64-bit microsecond counter with callbacks: good for scheduling,
not for precise edges. For a pulse with microsecond accuracy use the RMT
peripheral or a hardware timer with an ISR. A `vTaskDelay(1)` loop drifts by
milliseconds and jitters by more.

## Feeding from the wrong place

A watchdog fed by a low-priority housekeeping task tells you nothing about the
task that is actually stuck. Subscribe the task that does the work, and let the
others be.

| Symptom | Usually |
|---|---|
| reset every N seconds, same interval | TWDT on a task that blocks |
| reset during a flash write or OTA | TWDT not fed during erase, or IWDT during a long critical section |
| reset with no log at all | IWDT, or a brownout misread as a watchdog |
| timer callback crashes after a while | stack overflow in the timer task |
| drift of seconds per hour | `vTaskDelay` loop used as a clock |

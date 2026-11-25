---
name: esp32-freertos
description: Use when adding tasks, timers or interrupts to an ESP32 sketch, when the device resets with a watchdog or stack overflow, or when two tasks fight over a shared variable.
license: MIT
---

# FreeRTOS on ESP32

`setup()` and `loop()` are not "the program". They are one task among several,
and the rest of the system keeps running whether the sketch expects it or not.

## What the sketch actually is

- `loop()` runs inside a task created by the Arduino core (`loopTask`), on core
  1, at priority 1, with a stack in the low kilobytes.
- The Wi-Fi stack, the Bluetooth stack and the idle tasks are separate tasks
  with their own priorities. A tight loop in `loop()` does not starve them on a
  dual-core chip, but it does starve anything pinned to the same core.
- `delay()` yields. A busy `while` loop does not, and that is what triggers the
  task watchdog.

## The three resets you will actually see

1. **`Task watchdog got triggered`** — a task held the CPU without yielding for
   longer than the watchdog period. Long blocking work belongs in its own task
   with `vTaskDelay()`, not in `loop()`.
2. **`***ERROR*** A stack overflow in task ...`** — the task ran out of stack.
   The Arduino `loopTask` stack is small; a task that parses JSON or builds a
   large `String` will overflow it. Either reduce the recursion and `String`
   use, or create a task with an explicit larger stack.
3. **`Guru Meditation Error ... LoadProhibited`** — a null or dangling pointer,
   usually a buffer freed by another task while this one was using it.

## Interrupts

- An ISR must be marked `IRAM_ATTR` if it can run while the flash cache is
  disabled (during a flash write, for example).
- An ISR must not allocate, must not call `delay()`, must not use `Serial` or
  `Wire`, and must not take a mutex that a task holds.
- Communicate out of an ISR with a queue or a notification, never with a shared
  `volatile` flag that the task then polls.
- Call `portYIELD_FROM_ISR()` when the handler wakes a higher priority task,
  otherwise the wake-up waits for the next tick.

## Sharing data between tasks

- A `volatile` variable is not a lock. It stops the compiler caching the value;
  it does not make a 32-bit read-modify-write atomic.
- Use a mutex for a structure, a queue for a stream of values, and an atomic for
  a single counter.
- Priority inversion is real: a low priority task holding a mutex blocks a high
  priority one. FreeRTOS mutexes implement priority inheritance; binary
  semaphores do not. Use the mutex.

## Rules for the agent

- When adding a task, always state its stack size, its priority and its core.
  A task created with defaults is a task that will overflow on someone else's
  data.
- Do not add `delay()` inside a critical section or while holding a mutex.
- If the user reports a reset, ask for the full panic output including the
  backtrace. The first line names the failure; guessing from the symptom
  wastes a day.

---
name: embed-rtos
description: RTOS specialist. Owns task design, scheduling, synchronization primitives, memory layout, stack sizing, and real-time constraints. Auto-invoked when writing or refactoring task / scheduler / IPC code on FreeRTOS, Zephyr, ThreadX, etc.
---

# Embedded RTOS

Deadlines are contracts with the physical world — an RTOS app that misses them
is a broken product, not a slow one. Priority design, stack sizing, and the
choice of sync primitives are the whole game; everything else is configuration.

## When to reach for this

- Designing or refactoring the task set, priorities, and IPC on FreeRTOS,
  Zephyr, ThreadX, or NuttX
- Debugging deadline misses, jitter, priority inversion, or deadlock
- Chasing stack overflows or heap fragmentation in long-running devices
- Reviewing ISR ↔ task interaction (what's safe to call from interrupt context)

## Principles

1. **Prioritize by deadline, not importance.** Rate-monotonic as the default:
   shorter period/deadline → higher priority. "Important" background work at
   high priority is how the motor-control loop misses its slot.
2. **Priority inheritance by default.** Mutexes with inheritance for shared
   resources; plain semaphores for signaling only — a semaphore used as a lock
   has no owner and cannot inherit, which is the classic inversion landmine.
3. **Size stacks empirically.** Measure high-water mark (FreeRTOS
   `uxTaskGetStackHighWaterMark`, Zephyr `CONFIG_THREAD_STACK_INFO`) under
   worst-case load including nested interrupts, then add 20–30% margin. Enable
   stack-overflow checking / guard regions in every dev build.
4. **No dynamic allocation after init.** Allocate at startup or use fixed-size
   pools; on FreeRTOS prefer the static-allocation APIs or heap_4/heap_5 with a
   watermark check. Fragmentation failures arrive after weeks of uptime, in the
   field.
5. **Keep ISRs decoupled via the RTOS.** From interrupt context use only the
   `*FromISR` / ISR-safe variants; prefer direct task notifications over queues
   for the hot path (cheapest wake on FreeRTOS). Defer all real work to tasks.
6. **Tickless idle where supported.** It's the bridge between the scheduler and
   the power budget — but verify with a current measurement that the tick
   actually stops.

## Task table — the design artifact

| Task | Priority | Period / trigger | Deadline | Stack (HWM + margin) | IPC in/out |
|---|---|---|---|---|---|
| motor_ctrl | highest | 1 ms timer | 1 ms | measured | notif from ISR |
| sensor_poll | high | 10 ms | 10 ms | measured | queue → fusion |
| comms | mid | event | soft | measured | queue, mutex(bus) |
| logger | low | event | none | measured | stream buffer in |

Fill this in for every project and keep it current: it makes utilization
visible (`Σ WCET/period` — keep it under ~70% for rate-monotonic headroom),
exposes priority mistakes at a glance, and is the document a timing review
starts from.

## Pitfalls

- Semaphore-as-mutex: no ownership, no inheritance, silent inversion
- Two mutexes taken in different orders on two paths — deadlock that needs
  load to reproduce
- Non-`FromISR` API called in an ISR (often "works" until it corrupts state)
- Stack sized from the happy path; the overflow happens in the error path with
  `printf`-style logging on the stack
- `vTaskDelay()` used for periodic work instead of `vTaskDelayUntil()` — period
  drifts by execution time
- Shared data "protected" by task priority assumptions instead of a primitive —
  breaks the day a priority changes
- Busy-wait polling loops that starve everything below them

---
*Related: `embed-driver` (ISR/DMA interaction with tasks), `embed-power`
(tickless idle, idle hooks), `embed-connectivity` (comms task design),
`embed-ota` (update task scheduling) · domain agent: `embed-architect` ·
output/ADR format: `playbook-conventions`*

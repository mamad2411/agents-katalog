---
name: rtos
description: "Real-Time Operating Systems: preemptive scheduling, priority inversion, semaphores, mutexes, message queues, and rate-monotonic scheduling"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/rtos/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Real-Time Operating Systems (RTOS)

## Scope
RTOS architectures provide deterministic task scheduling, inter-task communication, and resource synchronization for hard and soft real-time applications.

## RTOS Core Mechanics
- **Preemptive Priority-Based Scheduling**: Highest priority ready task executes immediately; context switches occur on timer tick or blocking events.
- **Synchronization Primitives**:
  - Binary/Counting Semaphores: Signaling between ISR and task.
  - Mutexes: Mutual exclusion with Priority Inheritance to prevent Priority Inversion (Mars Pathfinder bug).
  - Message Queues: Thread-safe, fixed-size data passing by value or pointer.
- **Rate-Monotonic Scheduling (RMS)**: Liu & Layland theorem for independent periodic tasks: schedulable if utilization $U = \sum (C_i / T_i) \le n(2^{1/n} - 1) \approx 0.693$.

## Tools & Standards
- **Software**: FreeRTOS, Zephyr RTOS, ThreadX (Azure RTOS), RT-Thread.
- **Canonical References**: Laplante — *Real-Time Systems Design and Analysis*.

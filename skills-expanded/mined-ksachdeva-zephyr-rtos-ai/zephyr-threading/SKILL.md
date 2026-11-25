---
name: zephyr-threading
description: Expert guidance on Zephyr RTOS thread management, scheduling, and workqueues. Use when implementing threads (k_thread_create, K_THREAD_DEFINE), choosing thread priorities (cooperative vs preemptive), configuring scheduling behavior (time slicing, yielding), managing thread lifecycle (start, suspend, resume, abort, join), or using workqueues for deferred processing. Triggers include questions about thread stacks, priority inversion avoidance, system threads (main, idle), and thread-to-thread synchronization patterns.
---

# Zephyr Threading

## Overview

This skill provides expert knowledge on Zephyr kernel threading: creating and managing threads, understanding the scheduling model, selecting appropriate priorities, and using workqueues for deferred processing.

When thread blocking behavior and idle residency matter for battery life or low-power operation, also read [../zephyr-power-management/SKILL.md](../zephyr-power-management/SKILL.md).

## Workflow

### 1. Determine Thread Type Needed

First, identify what kind of execution context is required:

| Need | Solution |
| :--- | :--- |
| Lengthy/complex processing not suitable for ISR | Create a thread |
| Deferred work from ISR or high-priority thread | Use workqueue |
| Background processing with timeout control | Use delayable work item |
| Single-threaded application | Use main thread directly |

### 2. Select Priority Class

Zephyr has two priority classes. Choose based on preemption requirements:

**Cooperative threads** (negative priority, e.g., -1 to -CONFIG_NUM_COOP_PRIORITIES):
- Never preempted by scheduler until they voluntarily yield
- Best for: device drivers, performance-critical code, short atomic operations
- Use `K_PRIO_COOP(x)` macro where x=0 is highest cooperative priority

**Preemptive threads** (non-negative priority, 0 to CONFIG_NUM_PREEMPT_PRIORITIES-1):
- Can be preempted by higher-priority threads at any reschedule point
- Best for: application logic, time-sensitive processing
- Use `K_PRIO_PREEMPT(x)` macro where x=0 is highest preemptive priority

**Meta-IRQ threads** (optional, highest priority cooperative):
- Enable with `CONFIG_NUM_METAIRQ_PRIORITIES`
- Can preempt even cooperative threads — use only for interrupt bottom-half processing

**Rule of thumb**: Lower numeric value = higher priority. Priority -2 > -1 > 0 > 1.

### 3. Implementation

Once requirements are clear, implement using the appropriate reference:

**Step 3a:** For thread creation and lifecycle management:
- Read [references/thread-lifecycle.md](references/thread-lifecycle.md) — Static vs dynamic creation, stacks, start/suspend/resume/abort/join

**Step 3b:** For scheduling behavior and priority decisions:
- Read [references/scheduling.md](references/scheduling.md) — Time slicing, yielding, sleeping, scheduler locking

**Step 3c:** For deferred/background processing:
- Read [references/workqueues.md](references/workqueues.md) — System workqueue, custom workqueues, delayable work

**Step 3d:** For API signatures and configuration:
- Read [references/api.md](references/api.md) — Full function signatures, Kconfig options

## Quick Reference

### Static Thread Definition (compile-time)

```c
#define STACK_SIZE 1024
#define PRIORITY 5

void my_entry(void *p1, void *p2, void *p3) {
    while (1) {
        /* thread work */
        k_msleep(100);
    }
}

K_THREAD_DEFINE(my_thread, STACK_SIZE, my_entry, NULL, NULL, NULL,
                PRIORITY, 0, 0);  /* 0 = start immediately */
```

### Dynamic Thread Creation (runtime)

```c
K_THREAD_STACK_DEFINE(my_stack, 1024);
struct k_thread my_thread_data;

k_tid_t tid = k_thread_create(&my_thread_data, my_stack,
                              K_THREAD_STACK_SIZEOF(my_stack),
                              my_entry, NULL, NULL, NULL,
                              PRIORITY, 0, K_NO_WAIT);
k_thread_name_set(tid, "my_thread");
```

### Workqueue Usage

```c
void work_handler(struct k_work *work) {
    /* deferred processing */
}

K_WORK_DEFINE(my_work, work_handler);

/* From ISR or thread: */
k_work_submit(&my_work);  /* submits to system workqueue */
```

## Common Patterns

### ISR to Thread Communication

ISR signals thread via semaphore, thread does heavy processing:
```c
K_SEM_DEFINE(data_ready, 0, 1);

void my_isr(void *arg) {
    /* quick ISR work */
    k_sem_give(&data_ready);
}

void processing_thread(void *p1, void *p2, void *p3) {
    while (1) {
        k_sem_take(&data_ready, K_FOREVER);
        /* heavy processing */
    }
}
```

### Thread Ping-Pong (mutual handoff)

```c
K_SEM_DEFINE(sem_a, 1, 1);  /* thread A goes first */
K_SEM_DEFINE(sem_b, 0, 1);

void thread_a_entry(void *p1, void *p2, void *p3) {
    while (1) {
        k_sem_take(&sem_a, K_FOREVER);
        /* A's work */
        k_sem_give(&sem_b);
    }
}

void thread_b_entry(void *p1, void *p2, void *p3) {
    while (1) {
        k_sem_take(&sem_b, K_FOREVER);
        /* B's work */
        k_sem_give(&sem_a);
    }
}
```

## Common Mistakes

| Mistake | Problem | Fix |
| :--- | :--- | :--- |
| Arbitrary stack buffer | Alignment/MPU issues | Use `K_THREAD_STACK_DEFINE` |
| Wrong stack size parameter | Stack overflow/corruption | Use `K_THREAD_STACK_SIZEOF()` |
| Blocking in cooperative thread | Starves other threads | Yield periodically or use preemptive |
| Not releasing resources before exit | Memory/mutex leaks | Clean up before returning from entry |
| Aborting thread with held mutex | Deadlock | Signal thread to exit gracefully |
| Workqueue handler blocks forever | Queue stalls | Use K_NO_WAIT or bounded waits |

## Source Locations

| Description | Path |
| :--- | :--- |
| **Thread Docs** | `<zephyr-ws>/deps/zephyr/doc/kernel/services/threads` |
| **Scheduling Docs** | `<zephyr-ws>/deps/zephyr/doc/kernel/services/scheduling` |
| **Kernel Header** | `<zephyr-ws>/deps/zephyr/include/zephyr/kernel.h` |
| **Synchronization Sample** | `<zephyr-ws>/deps/zephyr/samples/synchronization` |
| **Philosophers Sample** | `<zephyr-ws>/deps/zephyr/samples/philosophers` |

*Note: `<zephyr-ws>` represents the root of the Zephyr workspace.*

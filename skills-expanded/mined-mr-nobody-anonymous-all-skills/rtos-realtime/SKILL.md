---
name: rtos-realtime
description: "Use when writing or reviewing real-time firmware for robots — FreeRTOS task architecture, control-loop scheduling, ISR design, priority inversion, jitter measurement, PREEMPT_RT Linux tuning, or RT/non-RT communication. Provides expert knowledge on priority assignment, mutex protocols, lockless queues, and why deadline misses kill robots in production."
category: robotics
domain: robotics
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "rahulbachina/robotics-skills"
  commit: "e69d9828fb"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# Real-Time Firmware for Robots: FreeRTOS, PREEMPT_RT, and Deterministic Control

## Why This Matters

A 1 kHz motor control loop has a 1000 µs budget. If your loop runs late by 200 µs
*occasionally*, your current controller integrates stale error, your derivative term
spikes, and your robot oscillates or faults — intermittently, unreproducibly, and
usually only under load. Real-time is not about speed. **It is about bounded
worst-case latency.** A system that responds in 10 µs on average but 5 ms at the
99.999th percentile is not real-time. A system that always responds within 100 µs is.

Hard rules that follow from this:

1. The worst case is the only case that matters. Mean latency is a vanity metric.
2. Anything with unbounded execution time (malloc, printf, flash writes, GC) is
   banned from the deadline path.
3. Determinism is a property of the *whole system* — one misconfigured DMA, cache,
   or SMI can destroy it regardless of how good your code is.

---

## Part 1 — FreeRTOS Task Architecture for Robots

### The Canonical Robot Task Set

Priority is **higher number = higher priority** in FreeRTOS (opposite of most RTOSes
— this trips up everyone coming from VxWorks/Zephyr). With `configMAX_PRIORITIES = 8`:

| Priority | Task | Period / Trigger | Why |
|---|---|---|---|
| 7 | (reserved) | — | Headroom for timer svc / emergency stop |
| 6 | `motor_control` | 1 kHz, timer-ISR-released | The deadline that matters |
| 5 | `safety_monitor` | 100 Hz + event | Watchdog feed, limit checks, e-stop logic |
| 4 | `sensor_fusion` / `state_est` | 200–500 Hz | IMU/encoder fusion feeding control |
| 3 | `comms_rx` | event (CAN/UART/EtherCAT ISR defer) | Commands must preempt logging |
| 2 | `comms_tx` / telemetry | 50–100 Hz | Outbound state |
| 1 | `logging` | event, batched | Never allowed to delay anything above |
| 0 | idle hook | — | CPU-load measurement, WFI for power |

**Rules behind this ordering:**

- **Control > comms > logging. Always.** A robot that logs perfectly but misses
  control deadlines is a broken robot. A robot that drops log lines is fine.
- **Rate-Monotonic as default:** shorter period → higher priority. This is optimal
  for fixed-priority scheduling of periodic tasks (Liu & Layland, 1973). Deviate
  only with a reason (e.g., safety_monitor above sensor_fusion despite longer
  period, because its *deadline* is shorter — that's Deadline-Monotonic, the
  correct generalization).
- **One task per rate, not per peripheral.** Don't make an "IMU task" and an
  "encoder task" both at 1 kHz that the control task waits on — read both sensors
  *inside* the control task (or in one fusion task) to eliminate scheduling jitter
  between them.
- **Never run application code at `configMAX_PRIORITIES - 1`** if you use software
  timers — the timer service task (`configTIMER_TASK_PRIORITY`) should sit above
  anything that depends on timer callbacks, or below everything if you don't.

### Schedulability Check (Do The Math)

Rate-Monotonic utilization bound for n tasks:

```
U = Σ (Ci / Ti) ≤ n(2^(1/n) − 1)
```

For n→∞ the bound is ln 2 ≈ **69.3%**. Worked example:

| Task | C (WCET) | T (period) | U |
|---|---|---|---|
| motor_control | 250 µs | 1000 µs | 0.250 |
| sensor_fusion | 800 µs | 5000 µs | 0.160 |
| safety | 300 µs | 10000 µs | 0.030 |
| comms | 2000 µs | 20000 µs | 0.100 |
| **Total** | | | **0.540** |

0.54 < 0.693 → schedulable, guaranteed, no further analysis needed. If U lands
between the bound and 1.0, the set *may* still be schedulable — do exact
response-time analysis:

```
R_i = C_i + Σ_{j ∈ higher-prio} ⌈R_i / T_j⌉ · C_j      (iterate to fixed point)
```

Task i is schedulable iff R_i ≤ D_i (deadline). **Measure C (WCET) on hardware
with caches/flash wait-states in their worst configuration — never trust -O3
average timings.** Add ISR time: every ISR is effectively a task above all tasks.

Budget rule of thumb for a 1 kHz control task: keep WCET under 30–40% of the
period. You need headroom for ISRs, the occasional cache miss storm, and the
feature someone will add next year.

### Releasing the Control Loop: Hardware Timer, Not vTaskDelay

`vTaskDelay()` drifts (delay is relative to *now*, including your own execution
time). `vTaskDelayUntil()` is acceptable but quantized to the tick (typically
1 ms) and jitters with tick-ISR latency. The professional pattern is a **hardware
timer ISR releasing the task via direct-to-task notification** — notifications
are ~45% faster than binary semaphores and impossible to "give" twice
accidentally into a counting overflow:

```c
/* Hardware timer ISR @ 1 kHz — e.g. STM32 TIM2 update interrupt */
void TIM2_IRQHandler(void)
{
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    TIM2->SR = ~TIM_SR_UIF;                      /* clear flag FIRST */

    vTaskNotifyGiveFromISR(xMotorTaskHandle, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken); /* context-switch on exit */
}

void motor_control_task(void *arg)
{
    uint32_t missed;
    for (;;) {
        missed = ulTaskNotifyTake(pdFALSE, pdMS_TO_TICKS(2)); /* pdFALSE = count */

        if (missed == 0) {            /* TIMEOUT — timer died. This is a fault. */
            enter_safe_state();       /* disable PWM via hardware, not software */
            continue;
        }
        if (missed > 1) {
            overrun_count += missed - 1;   /* we missed (missed-1) cycles */
            /* policy decision: log + continue, or fault if missed > N */
        }

        read_encoders(&fb);                /* direct register/DMA-buffer reads  */
        read_current_adc(&fb);             /* must be < ~50 µs total            */
        compute_control(&cmd, &fb, &ref);  /* PID/FOC — pure function, no locks */
        write_pwm(&cmd);                   /* registers, never through a queue  */
        publish_state_lockless(&fb, &cmd); /* seqlock/ring — see Part 5         */
    }
}
```

Key details an AI agent must not omit:

- `pdFALSE` (don't clear-on-exit) makes the notification a **counting** semaphore:
  overruns are *detected*, not silently swallowed. `pdTRUE` hides missed deadlines.
- The timeout branch is a **safety feature**: if the timer ISR ever stops firing,
  the motor task must not block forever holding torque commands stale.
- PWM disable on fault must be a hardware path (break input, gate-driver enable
  pin) — software might be the thing that's broken.

### Stack Sizing and the Things That Corrupt It

- Set `configCHECK_FOR_STACK_OVERFLOW = 2` in development (pattern-fill check).
  It catches overflow *after the fact* — it is a debug aid, not protection.
- On Cortex-M with MPU support, use FreeRTOS MPU port or at minimum put a guard
  region below each stack.
- Measure with `uxTaskGetStackHighWaterMark()` after exercising worst-case paths
  (fault handlers, printf-formatting in logger, math library calls — `sinf` and
  friends can use surprising stack). Provision measured + 30%.
- `configASSERT()` must be defined and must halt into a breakpoint/safe-state in
  development builds. Most "weird random crash" reports on FreeRTOS forums are a
  failed assert that was compiled out.

---

## Part 2 — Priority Inversion and Mutex Protocols

### The Failure

Low-priority task L holds a mutex. High-priority task H blocks on it. Medium task
M (which needs no mutex) preempts L indefinitely. H is now blocked for an
**unbounded** time by M — a task it should always preempt. This is what reset the
Mars Pathfinder lander in 1997 (VxWorks, a select() mutex, watchdog reboots on
Mars). On a robot it looks like: control task sporadically misses deadlines
whenever telemetry traffic is heavy, because logging (L) and comms (M) interact
through a shared I2C mutex.

### The Protocols

| Protocol | FreeRTOS support | Blocking bound | Notes |
|---|---|---|---|
| Priority Inheritance (PIP) | ✅ `xSemaphoreCreateMutex()` | one critical section per mutex level (can chain) | L is boosted to H's priority while holding. Default, use it. |
| Priority Ceiling (PCP/IPC) | ❌ (emulate manually) | one critical section, period; deadlock-free | Boost to ceiling on lock. Emulate with `vTaskPrioritySet` if you need the stronger bound. |
| None (binary semaphore) | `xSemaphoreCreateBinary()` | **unbounded** | Never use a binary semaphore for mutual exclusion. Semaphores signal; mutexes protect. |

Rules:

1. **Mutex for mutual exclusion, semaphore/notification for signaling.** A binary
   semaphore used as a lock gives you no inheritance — this is the #1 RTOS code
   review finding.
2. **Keep critical sections short and measured.** Priority inheritance bounds the
   inversion to the length of the critical section — if your critical section
   does an I2C transaction (milliseconds), inheritance doesn't save you.
3. **The control loop holds no mutexes. Ever.** If the 1 kHz task can block on a
   lock shared with logging, you have built a priority inversion machine. Use
   lockless exchange (Part 5).
4. Never call mutex take/give from an ISR (it's also simply not allowed in
   FreeRTOS — there is no `xSemaphoreTakeFromISR` for mutexes, by design).
5. Recursive mutexes (`xSemaphoreCreateRecursiveMutex`) are a code smell that
   your locking layers are tangled. Allowed, but flag it.
6. For tiny shared data on single-core MCUs, a critical section
   (`taskENTER_CRITICAL()`, masks interrupts up to
   `configMAX_SYSCALL_INTERRUPT_PRIORITY`) for < ~1 µs of straight-line code is
   often the right tool — cheaper and inversion-free. Do not nest function calls
   inside it.

---

## Part 3 — ISR Rules (The Non-Negotiables)

ISRs run above every task. Every microsecond in an ISR is a microsecond of jitter
added to *all* deadlines. The discipline:

1. **Top-half/bottom-half split.** ISR: acknowledge hardware, grab the data or
   timestamp, notify a task, exit. Target **< 10 µs**, hard cap ~25 µs. All
   parsing/math happens in the deferred task.
2. **Only `*FromISR` API functions.** Calling `xQueueSend` (no suffix) from an ISR
   corrupts the scheduler state. `configASSERT` catches this if interrupt priority
   config is right (see #6).
3. **No malloc, no printf, no float-formatting, no flash writes** in ISRs.
   `printf` takes a heap lock or a stream mutex and can run for milliseconds.
   If you need ISR-context debug output, write a record into a ring buffer and
   let the logger task drain it.
4. **Always honor `xHigherPriorityTaskWoken` + `portYIELD_FROM_ISR()`.** Omitting
   it means the woken high-priority task waits until the *next tick* (up to 1 ms
   of silent latency). This bug passes every functional test and fails only in
   latency measurement.
5. **FPU context:** on Cortex-M4F/M7, using floats in an ISR triggers lazy FPU
   stacking — extra latency and stack use. Keep ISRs integer-only.
6. **The Cortex-M priority trap (causes ~half of all FreeRTOS hard faults):**
   Cortex-M priorities are *lower number = higher urgency*, and only the top bits
   are implemented (e.g. 4 bits on STM32 → priorities 0–15). Any ISR that calls a
   `FromISR` function must have priority **numerically ≥**
   `configMAX_SYSCALL_INTERRUPT_PRIORITY`. With STM32Cube/HAL:

   ```c
   /* configMAX_SYSCALL_INTERRUPT_PRIORITY = 5 << 4 typical on STM32 */
   HAL_NVIC_SetPriority(CAN1_RX0_IRQn, 6, 0);   /* 6 ≥ 5 → may use FromISR APIs */
   HAL_NVIC_SetPriority(TIM8_BRK_IRQn, 1, 0);   /* 1 < 5 → "super-priority":
                                                   never masked by RTOS, but must
                                                   NOT touch any FreeRTOS API */
   ```

   Super-priority interrupts (above the syscall ceiling) are the right place for
   motor-current trip / gate-fault shutdown: they fire even inside RTOS critical
   sections, but they may only touch hardware registers.
7. **Clear the interrupt flag before doing work**, and re-check status sources for
   peripherals that coalesce events, or you'll lose edges.

```c
/* Pattern: UART RX deferred to task via stream buffer (ISR-safe, lock-free) */
void USART2_IRQHandler(void)
{
    BaseType_t wake = pdFALSE;
    while (USART2->ISR & USART_ISR_RXNE) {
        uint8_t b = (uint8_t)USART2->RDR;          /* read clears RXNE */
        xStreamBufferSendFromISR(rx_sbuf, &b, 1, &wake);
    }
    portYIELD_FROM_ISR(wake);
}
```

(Note: FreeRTOS stream buffers assume a **single reader and single writer** —
ideal for ISR→task, wrong for anything else.)

---

## Part 4 — Measuring Jitter (If You Didn't Measure It, You Don't Have It)

### Definitions

- **Release jitter:** variation in when the periodic task actually starts vs. its
  ideal release time.
- **Latency:** event (interrupt) → first instruction of the handling task.
- Report **min / mean / max / histogram**, and run for hours under worst-case
  load. The max is the number that matters. A 10-minute quiet-bench measurement
  is worthless.

### MCU technique: cycle counter, not GPIO-only

The Cortex-M DWT cycle counter gives single-cycle resolution for free:

```c
/* enable once */
CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
DWT->CYCCNT = 0;
DWT->CTRL  |= DWT_CTRL_CYCCNTENA_Msk;

/* in the 1 kHz task, every cycle: */
uint32_t now = DWT->CYCCNT;
uint32_t dt  = now - last;            /* wraps correctly with unsigned math */
last = now;
int32_t jitter_cycles = (int32_t)(dt - CYCLES_PER_PERIOD);
hist_update(&jitter_hist, jitter_cycles);   /* log-bucket histogram, O(1) */
if (abs_jitter > worst) worst = abs_jitter;
```

Complement with a **GPIO toggle at task entry/exit** viewed on a scope or logic
analyzer — this also reveals preemptions (gaps inside the high pulse) and is the
ground truth that survives arguments. For deep analysis, use SEGGER SystemView or
Percepio Tracealyzer (both hook FreeRTOS trace macros) to see exactly *which*
task/ISR stole the time.

**Load the system while measuring:** saturate the comms link, force logging
floods, trigger flash writes, run the worst-case math path. Jitter that only
appears under load is the only jitter you'll see in the field.

### Acceptance targets (typical)

| Loop | Period | Max release jitter target |
|---|---|---|
| Current/FOC loop | 50–100 µs (often in ISR/hardware) | < 1 µs |
| Velocity/torque loop | 1 ms | < 10 µs (MCU), < 50 µs (PREEMPT_RT) |
| Position/whole-body | 1–4 ms | < 100 µs |
| Planner | 10–100 ms | soft |

---

## Part 5 — Lockless Communication Between RT and Non-RT

The control loop must never block on a consumer. Two patterns cover ~95% of needs:

### Pattern A: SPSC ring buffer (streams: telemetry, log records, sensor samples)

Single producer, single consumer, power-of-two size, no locks, no CAS:

```c
typedef struct {
    sample_t buf[RING_SIZE];                  /* RING_SIZE = power of 2 */
    _Alignas(64) volatile uint32_t head;      /* producer-owned          */
    _Alignas(64) volatile uint32_t tail;      /* consumer-owned          */
} spsc_ring_t;                                /* separate cache lines:
                                                 avoids false sharing on
                                                 multicore (M7 dual, Linux) */

/* Producer (RT). NEVER blocks. Drops on full — by design. */
bool ring_push(spsc_ring_t *r, const sample_t *s)
{
    uint32_t h = r->head;
    if (h - r->tail >= RING_SIZE) { r_dropped++; return false; } /* full */
    r->buf[h & (RING_SIZE - 1)] = *s;
    __atomic_thread_fence(__ATOMIC_RELEASE);  /* data visible before index */
    r->head = h + 1;
    return true;
}

/* Consumer (non-RT) */
bool ring_pop(spsc_ring_t *r, sample_t *out)
{
    uint32_t t = r->tail;
    if (t == r->head) return false;           /* empty */
    __atomic_thread_fence(__ATOMIC_ACQUIRE);
    *out = r->buf[t & (RING_SIZE - 1)];
    r->tail = t + 1;
    return true;
}
```

- **Overflow policy is drop-and-count, never block.** Count the drops and alarm
  on them; blocking the producer is a deadline miss.
- On single-core Cortex-M the fences compile to nothing/DMB but keep them — the
  code then ports correctly to M7 dual-core and Linux.
- This is exactly what FreeRTOS stream/message buffers are internally; use those
  on FreeRTOS unless you need the buffer shared across cores without the kernel.

### Pattern B: Seqlock / double buffer (latest-state: "current robot state", gains)

Consumers want the *newest* value, not every value:

```c
typedef struct {
    volatile uint32_t seq;     /* even = stable, odd = writer mid-update */
    robot_state_t state;
} seqlock_state_t;

/* RT writer — wait-free, constant time */
void state_write(seqlock_state_t *s, const robot_state_t *in)
{
    s->seq++;                                  /* now odd */
    __atomic_thread_fence(__ATOMIC_RELEASE);
    s->state = *in;
    __atomic_thread_fence(__ATOMIC_RELEASE);
    s->seq++;                                  /* even again */
}

/* Non-RT reader — retries if torn; never delays the writer */
void state_read(const seqlock_state_t *s, robot_state_t *out)
{
    uint32_t a, b;
    do {
        a = s->seq;
        __atomic_thread_fence(__ATOMIC_ACQUIRE);
        *out = s->state;
        __atomic_thread_fence(__ATOMIC_ACQUIRE);
        b = s->seq;
    } while (a != b || (a & 1));
}
```

The asymmetry is the point: the RT side is wait-free; only the unimportant side
ever retries. For the reverse direction (non-RT writes gains/setpoints that RT
reads), use the same seqlock with roles swapped *only if* the writer is a single
thread — otherwise add a mutex among the non-RT writers (RT reader still never
blocks).

On Linux RT (Part 6), the same two patterns apply across `mmap`'d shared memory
between an RT thread and ROS2 code. Do **not** use ROS2 intraprocess pub/sub
inside a 1 kHz loop — even with zero-copy, executor wakeups and DDS listener
paths are not deadline-safe. `ros2_control` exists precisely to keep the RT loop
in plain C++ and bridge to topics outside it.

---

## Part 6 — PREEMPT_RT Linux for Soft/Firm Real-Time

Since kernel 6.12, PREEMPT_RT is mainline (`CONFIG_PREEMPT_RT=y`). It converts
spinlocks to PI-mutexes and forces threaded IRQs, getting worst-case scheduling
latency on decent x86/ARM hardware to **~20–100 µs** — fine for 1 kHz robot
loops, not for 100 kHz current loops (keep those on the MCU/FPGA).

### The RT thread recipe (every line is load-bearing)

```c
#include <pthread.h>
#include <sched.h>
#include <sys/mman.h>
#include <time.h>

void *control_thread(void *arg)
{
    struct timespec next;
    clock_gettime(CLOCK_MONOTONIC, &next);
    for (;;) {
        next.tv_nsec += 1000000;                      /* 1 ms, absolute time */
        if (next.tv_nsec >= 1000000000L) { next.tv_nsec -= 1000000000L; next.tv_sec++; }
        clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next, NULL);
        /* TIMER_ABSTIME → no drift. Relative sleeps drift; never use them. */
        do_control_cycle();
    }
}

int main(void)
{
    /* 1. Lock ALL memory — a page fault in the loop is a multi-ms stall */
    mlockall(MCL_CURRENT | MCL_FUTURE);

    /* 2. Pre-fault the stack and heap pools NOW, then never malloc again
          on the RT path. (Touch every page of a static buffer.) */
    prefault_stack(64 * 1024);

    pthread_attr_t attr;
    struct sched_param sp = { .sched_priority = 80 };  /* 1..99; don't use 99 —
                                                          leave kthread headroom */
    pthread_attr_init(&attr);
    pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
    pthread_attr_setschedparam(&attr, &sp);
    pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED); /* MANDATORY:
        without this, the policy/priority you just set is silently IGNORED
        and the thread inherits SCHED_OTHER. Classic silent failure. */

    pthread_t t;
    pthread_create(&t, &attr, control_thread, NULL);

    /* 3. Pin to an isolated core */
    cpu_set_t cs; CPU_ZERO(&cs); CPU_SET(3, &cs);
    pthread_setaffinity_np(t, sizeof(cs), &cs);
    ...
}
```

Locks shared with non-RT threads must be PI mutexes:
`pthread_mutexattr_setprotocol(&ma, PTHREAD_PRIO_INHERIT)` — a plain pthread
mutex on PREEMPT_RT reintroduces priority inversion in userspace.

### System tuning checklist

```
# kernel cmdline — isolate core 3 (and its tick) for the RT thread
isolcpus=3 nohz_full=3 rcu_nocbs=3 irqaffinity=0-2

# disable frequency scaling — DVFS transitions cost latency
cpupower frequency-set -g performance

# pin device IRQs away from the RT core (or onto it, if it's *your* device's IRQ)
echo 1 > /proc/irq/<N>/smp_affinity

# verify with cyclictest under full load (stress-ng) for hours:
cyclictest -m -p95 -t1 -a3 -i1000 -h400 --duration=8h
# Pass criterion: Max latency < your budget. On a tuned industrial PC expect
# max ~50-150 µs. If you see multi-ms spikes: suspect SMIs (BIOS — check
# /sys/devices/system/machinecheck or hwlatdetect), GPU driver, or DVFS.
```

Production failure modes specific to PREEMPT_RT:

- **SMIs (System Management Interrupts):** firmware-level, invisible to the
  kernel, can stall the CPU for milliseconds. Run `hwlatdetect`. Some BIOSes let
  you disable USB legacy/thermal SMI sources; some hardware is simply unusable
  for RT. Qualify the board before committing.
- **A spinning SCHED_FIFO thread can hang the machine** (starves kernel
  threads). Set `/proc/sys/kernel/sched_rt_runtime_us` consciously (default
  950000 = RT throttled to 95% — it saves you in dev, but the throttle itself is
  a deadline miss in production; design loops that sleep).
- **printf/iostream in the RT thread** → glibc internal locks shared with non-RT
  threads → inversion (PI saves you partially, the malloc inside doesn't). Same
  rule as ISRs: ring buffer to a logger thread.
- **C++ on the RT path:** no `new`, no `std::string` growth, no `std::vector`
  resize, no throwing exceptions, no `std::mutex` (no PI protocol — use
  pthread PI mutex), no `std::cout`. Pre-size everything at init.

---

## Part 7 — Why GC Languages Don't Drive 1 kHz Loops

The argument, precisely (not "Python is slow" — speed is irrelevant):

1. **Stop-the-world pauses are unbounded from the application's view.** Go's GC
   advertises sub-millisecond pauses *typically* — but a 1 kHz loop has a 1000 µs
   budget total, and "typically" is exactly the word real-time forbids. Java
   ZGC/Shenandoah claim <1 ms pauses, but allocation stalls, JIT deoptimization,
   and safepoint polls add tail latencies that no one will bound in writing.
2. **CPython adds the GIL and refcount cascades** (a deallocation can trigger an
   arbitrarily long chain of frees), plus generational GC for cycles. Jitter in
   the hundreds of µs to ms range is normal under load.
3. **JIT warm-up and deopt**: the first (or recompiled) execution of the control
   path can be 100× slower. Your robot's worst control cycle happens at the worst
   moment — right after a mode switch.
4. The math: a 2 ms GC pause in a 1 kHz current-controlled joint means 2 missed
   commands; with a stale torque command during a contact transient, that's
   overcurrent trip at best, a broken harmonic drive or a hurt person at worst.

What actually works in production:

| Layer | Rate | Language |
|---|---|---|
| Current/FOC | 10–100 kHz | C on MCU / FPGA |
| Servo & whole-body control | 0.5–4 kHz | C / C++ (no-alloc subset) or Rust, FreeRTOS or PREEMPT_RT |
| State machines, planners | 10–100 Hz | C++ / Rust / (Java/Go acceptable) |
| UI, fleet, tooling, offline ML | — | Python/TypeScript/anything |

Notes for completeness:
- **Rust** is excellent on the RT path (no GC, no hidden allocation if you avoid
  `alloc` or audit it) — RTIC and Embassy on MCUs, plain threads on PREEMPT_RT.
- Python *prototyping* of a 100–200 Hz loop on PREEMPT_RT can work for lab demos
  (and `mujoco`/`pinocchio` bindings make it tempting) — but never ship it on a
  torque-controlled robot, and never claim determinism for it.
- If someone proposes "real-time Java" (JamaicaVM, PTC) or Go on the control
  path, the burden of proof is a multi-hour histogram under worst-case load with
  a documented max — which is exactly the artifact they will not be able to
  produce within budget.

---

## Part 8 — Debugging Methodology for RT Failures

Symptoms are intermittent by nature. Work the list:

1. **Instrument first, hypothesize second.** DWT cycle-counter jitter histogram
   (MCU) or `cyclictest`/ftrace (`trace-cmd record -e sched_switch -e irq`) on
   Linux. Get the *max* and *when*.
2. **Correlate the spike with a cause:** SystemView/Tracealyzer (FreeRTOS) or
   kernelshark (Linux) shows exactly which ISR/task/lock occupied the gap.
3. Usual suspects, in observed frequency order:
   - ISR calling non-`FromISR` API or wrong NVIC priority grouping (Cortex-M)
   - Missing `portYIELD_FROM_ISR` (silent up-to-1-tick latency)
   - Binary semaphore used as a mutex (inversion under load only)
   - `printf`/malloc snuck into the hot path by a dependency
   - Flash write/erase stalling instruction fetch (run RT code from RAM, or use
     dual-bank flash)
   - DMA/bus contention with a high-bandwidth peripheral (camera, SDIO)
   - Linux: page fault (forgot `mlockall`), SMI, DVFS transition, missing
     `PTHREAD_EXPLICIT_SCHED`
4. **Stack overflow masquerades as everything.** Rule it out early
   (high-water marks, `configCHECK_FOR_STACK_OVERFLOW=2`).
5. Reproduce under amplified load, fix **one thing**, re-run the multi-hour
   histogram, compare maxima. No before/after histogram → not fixed.

## Review Checklist (apply to any RT firmware diff)

- [ ] Control loop released by HW timer + task notification, overruns counted
- [ ] No mutex, malloc, printf, flash write, or unbounded loop on the deadline path
- [ ] All ISRs: `FromISR` APIs only, priority ≥ `configMAX_SYSCALL_INTERRUPT_PRIORITY`, yield-from-ISR honored, < 25 µs
- [ ] Mutexes (not binary semaphores) for shared resources; critical sections measured
- [ ] RT↔non-RT data via SPSC ring or seqlock; producer never blocks; drops counted
- [ ] Schedulability math done with measured WCET; U documented
- [ ] Linux: `mlockall` + pre-fault + `SCHED_FIFO` + `PTHREAD_EXPLICIT_SCHED` + PI mutexes + isolated/pinned core
- [ ] Jitter histogram exists, was captured under worst-case load for hours, and max < budget
- [ ] Fault path (timer death, overrun storm) drives a **hardware** safe-state

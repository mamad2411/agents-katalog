---
name: zephyr-isr
description: Expert guidance on Zephyr RTOS Interrupt Service Routines (ISRs). Use when the user asks about interrupts, ISR handlers, IRQ configuration, interrupt priorities, direct ISRs, dynamic ISRs, zero-latency interrupts, IRQ locking, ISR-to-thread offloading, shared interrupts, or interrupt context behavior in Zephyr.
---

# Zephyr ISR (Interrupt Service Routines)

## Overview

This skill provides expert knowledge on interrupt handling in Zephyr RTOS. It covers ISR registration (static and dynamic), direct ISRs for low-latency handling, IRQ management, interrupt context constraints, and patterns for offloading work from ISRs to threads.

## Key Constraints (Memorize)

**ISR Context Rules:**
- ISRs run on a dedicated interrupt stack
- ISRs can be nested (higher priority preempts lower)
- ISRs must **never block** - no `K_FOREVER` or `K_MSEC(n)` timeouts
- Use `k_is_in_isr()` to detect interrupt context
- Many kernel APIs are thread-only; check docs before use in ISR

**ISR-Safe Operations:**
- `k_sem_give()` - always safe
- `k_sem_take(&sem, K_NO_WAIT)` - safe (non-blocking)
- `k_msgq_put()` / `k_fifo_put()` with `K_NO_WAIT` - safe
- `k_work_submit()` - safe (offload to system workqueue)

## Workflow

### 1. Choose ISR Type

| Type | Use When | Registration |
|------|----------|--------------|
| **Regular** | Most cases, arguments known at build time | `IRQ_CONNECT()` |
| **Dynamic** | Arguments known only at runtime | `irq_connect_dynamic()` |
| **Direct** | Ultra-low latency required | `IRQ_DIRECT_CONNECT()` |

**Step 1:** Read [references/isr-types.md](references/isr-types.md) for detailed implementation of each type.

### 2. Implement ISR

Once the ISR type is chosen, implement the handler:

```c
/* Regular ISR */
void my_isr(const void *arg)
{
    /* Fast processing only - never block */
}

/* Direct ISR (for lowest latency) */
ISR_DIRECT_DECLARE(my_direct_isr)
{
    do_minimal_work();
    ISR_DIRECT_PM();  /* Power management hook */
    return 1;         /* 1 = check reschedule, 0 = skip */
}
```

### 3. Register and Enable

```c
/* Build-time registration */
IRQ_CONNECT(IRQ_NUM, PRIORITY, my_isr, my_arg, FLAGS);
irq_enable(IRQ_NUM);

/* Runtime registration */
irq_connect_dynamic(IRQ_NUM, PRIORITY, my_isr, my_arg, FLAGS);
irq_enable(IRQ_NUM);
```

### 4. Offload Time-Consuming Work

If ISR needs to trigger complex processing, offload to a thread.

**Step 4:** Read [references/offloading.md](references/offloading.md) for patterns:
- Semaphore signaling (ISR gives, thread takes)
- Work queue submission
- Message queue / FIFO handoff

### 5. API & Configuration

For complete API signatures and Kconfig options.

**Step 5:** Read [references/api.md](references/api.md) for:
- All IRQ/ISR macros and functions
- Kconfig options
- Header locations

### 6. Advanced Features

For specialized interrupt scenarios.

**Step 6:** Read [references/advanced.md](references/advanced.md) for:
- Zero-latency interrupts
- Shared interrupts
- Multi-level interrupt controllers
- IRQ locking patterns

## Quick Decision Guide

```
Need interrupt handling?
├── Arguments known at build time?
│   ├── Yes → IRQ_CONNECT() [most common]
│   └── No → irq_connect_dynamic()
│
├── Need ultra-low latency?
│   └── Yes → IRQ_DIRECT_CONNECT() + ISR_DIRECT_DECLARE()
│
├── Must bypass irq_lock()?
│   └── Yes → Zero-latency IRQ (ARM Cortex-M only)
│
└── Multiple ISRs on same line?
    └── Yes → Enable CONFIG_SHARED_INTERRUPTS
```

## Common Pitfalls

1. **Blocking in ISR** - Never use timeouts; always `K_NO_WAIT`
2. **IRQ_CONNECT args not const** - All args must be build-time constants
3. **Forgetting irq_enable()** - ISR won't fire without it
4. **Wrong IRQ number** - Check devicetree/board docs for correct IRQ line
5. **Priority inversion** - High-priority ISR can starve threads

## Source Locations

| Description | Path |
|:---|:---|
| **Interrupts Docs** | `<zephyr-ws>/deps/zephyr/doc/kernel/services/interrupts.rst` |
| **IRQ Header** | `<zephyr-ws>/deps/zephyr/include/zephyr/irq.h` |
| **Kernel Header** | `<zephyr-ws>/deps/zephyr/include/zephyr/kernel.h` |
| **Interrupt Tests** | `<zephyr-ws>/deps/zephyr/tests/arch/common/interrupt/` |
| **Architecture IRQ** | `<zephyr-ws>/deps/zephyr/include/zephyr/arch/<arch>/irq.h` |

*Note: `<zephyr-ws>` represents the root of the Zephyr workspace.*

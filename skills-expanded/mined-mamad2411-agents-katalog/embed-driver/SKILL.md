---
name: embed-driver
description: Embedded driver / peripheral specialist. Owns device drivers, bus protocols (I2C, SPI, UART, CAN, USB), DMA, interrupt handling, and hardware-abstraction layers. Auto-invoked when writing, porting, or debugging driver / bus / peripheral code.
---

# Embedded Drivers

Drivers are where software meets physics. Timing, interrupts, and memory
coherence bite in ways compile-time checks never catch — a driver that "works"
on the bench can still corrupt data under load or wedge the bus in the field.

## When to reach for this

- Writing or porting a driver for a sensor, actuator, or comms peripheral
- Debugging bus faults: I2C NACKs/stuck SDA, SPI mode mismatches, UART framing,
  CAN error frames, USB enumeration failures
- Adding DMA to a transfer path, or chasing cache-coherency corruption
- Restructuring interrupt handling (ISR latency, priority, deferred work)

## Principles

1. **Datasheet before keyboard.** Read the timing diagrams, the errata sheet,
   and the reference schematic before writing a line. Half of "driver bugs" are
   documented silicon errata.
2. **ISRs are short.** Capture the event, clear the flag, wake a task (semaphore
   / task notification); all real work happens in task context. Never log,
   allocate, or block inside an ISR.
3. **DMA where it's justified.** CPU copies are fine for small transfers; for
   sustained or large ones (audio, display, bulk SPI flash), DMA frees the CPU —
   but on cache-enabled cores it demands cache clean/invalidate or non-cacheable
   buffers, and cache-line-aligned buffer boundaries.
4. **Error paths are exercised, not assumed.** NACK, timeout, bus-busy, device
   unplugged — every one has a tested recovery, including I2C bus recovery
   (clock out up to 9 SCL pulses to release a stuck slave, then STOP).
5. **Power-aware from the start.** Every driver exposes suspend/resume hooks and
   restores full state after a power-domain cycle; "reinit on resume" hides
   state-loss bugs.

## Driver contract skeleton

```c
typedef struct {
    int (*init)(dev_t *dev, const dev_cfg_t *cfg);   /* idempotent */
    int (*read)(dev_t *dev, void *buf, size_t len, uint32_t timeout_ms);
    int (*write)(dev_t *dev, const void *buf, size_t len, uint32_t timeout_ms);
    int (*suspend)(dev_t *dev);                      /* save state, gate clocks */
    int (*resume)(dev_t *dev);                       /* restore, no caller-visible loss */
    int (*deinit)(dev_t *dev);
} dev_ops_t;
/* Rules: every call takes a timeout; return codes distinguish timeout vs
   bus-error vs bad-arg; no global state — context lives in dev_t so two
   instances on different buses coexist. */
```

## Bring-up checklist

- [ ] Scope/logic-analyzer capture of one good transaction kept as reference
- [ ] Errata sheet reviewed; applicable workarounds linked in comments
- [ ] Timeout on every blocking bus call — no infinite waits
- [ ] NACK / timeout / disconnect each provoked and recovered in test
- [ ] ISR measured: worst-case duration and priority documented
- [ ] DMA buffers: alignment, lifetime, and cache maintenance verified
- [ ] Suspend → resume → transfer passes without reinit
- [ ] Concurrent access policy stated (mutex per bus, not per device)

## Pitfalls

- Read-modify-write on shared registers without disabling the relevant IRQ
- `volatile` used as a substitute for memory barriers / DMA cache maintenance
- Polling loops with no timeout ("it always responds on my board")
- Clearing interrupt flags after the handler body — re-entry races
- Blocking bus calls from an ISR, or taking a mutex in one
- HAL leakage: app code touching registers directly around the driver

---
*Related: `embed-rtos` (task/ISR interaction, priorities), `embed-power`
(system power budget the driver plugs into), `embed-connectivity` (the stack
above a radio-module driver) · domain agent: `embed-architect` · output/ADR
format: `playbook-conventions`*

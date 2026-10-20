---
name: embed-power
description: Power management specialist. Owns sleep modes, duty cycling, peripheral gating, wake sources, and battery-life budgeting. Auto-invoked for battery devices, low-power design, or power regressions.
---

# Embedded Power

A device that dies early is a support ticket; a fleet that dies early is a
recall. Battery life is decided in microamps of sleep current and seconds of
awake time — and a single accidentally-enabled peripheral can halve it.

## When to reach for this

- Budgeting battery life for a new device, or validating a marketing claim
- Choosing sleep modes, wake sources, and duty-cycle structure
- Chasing a power regression ("battery life dropped after the last release")
- Standing up a power-measurement harness or CI current test

## Principles

1. **Measure before modeling.** Real currents on real hardware beat datasheet
   numbers every time — datasheets quote typicals at 25 °C with everything
   else off. Use a dynamic-range meter (Joulescope, Nordic PPK2, or similar)
   that can resolve µA sleep floors and mA active bursts in one capture.
2. **Sleep is the default state; work is the exception.** Structure firmware as
   event-driven wake → do the work → return to deepest viable sleep. Any task
   that polls is a battery bug.
3. **Gate aggressively.** Every unused clock, peripheral, and power domain off;
   every GPIO in a defined state (floating inputs leak). Audit this with a
   measurement, not a code review — the meter finds what the eyes miss.
4. **Pick the shallowest sleep that meets the deadline.** Deeper modes save
   current but cost wake latency and lost state (deep modes can mean RAM loss
   and a reset-path wake). Map each wake source to the deepest mode it can
   still wake from.
5. **Average current is the only number that matters.**
   `I_avg = Σ(I_state × t_state) / T_period`, then
   `life ≈ capacity × 0.8 / I_avg` — the ~0.8 derate covers self-discharge,
   temperature, and end-of-life capacity. Sleep current usually dominates:
   at 1-hour wake intervals, the µA floor matters more than the mA burst.
6. **Guard against regressions in CI.** An automated current measurement on
   every firmware PR, with thresholds per state (sleep floor, active peak,
   duty-cycle average). Power regressions are silent — nothing fails
   functionally when a clock is left on.

## Duty-cycle budget — worked shape

| State | Current | Time per hour | Charge (µAh) |
|---|---|---|---|
| Deep sleep | 5 µA | 3594 s | ~5.0 |
| Wake + measure | 5 mA | 2 s | ~2.8 |
| Radio TX/RX | 50 mA | 4 s | ~55.6 |
| **Average** | | | **≈ 63 µAh/h → I_avg ≈ 63 µA** |

With a 2000 mAh cell: `2000 × 0.8 / 0.063 ≈ 25,000 h ≈ 2.9 years`. The radio
burst dominates — halving TX time buys far more than shaving the sleep floor.
Build this table from *measured* numbers and keep it in the repo; it is the
spec every regression is judged against.

## Pitfalls

- Floating GPIOs or enabled pull-ups leaking hundreds of µA in "deep sleep"
- Debug peripherals (SWD, UART console) left clocked in release builds
- Measuring with a meter that can't resolve both µA sleep and mA bursts —
  averages from a coarse meter hide the sleep floor entirely
- Battery life quoted at 25 °C for a device shipping into freezers or cars
- Sleep entered with a pending interrupt — instant wake, looks like "sleep
  current is high" but is actually 100% duty cycle
- Tickless idle assumed but never verified (a 1 kHz tick is a wake source)

---
*Related: `embed-rtos` (tickless idle, idle hooks), `embed-connectivity`
(radio duty cycle is usually the budget's biggest line), `embed-ota`
(update-window energy), `embed-driver` (peripheral suspend/resume hooks) ·
domain agent: `embed-architect` · output/ADR format: `playbook-conventions`*

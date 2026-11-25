---
name: esp32-field-gotchas
description: Use when an ESP32 misbehaves in a way the code does not explain - reboots, brownouts, dead I2C, garbled UART, a sketch that will not flash, a crash with no line number. One hundred and sixty failures collected from Stack Overflow, each with the cause and the fix.
license: MIT
---

# ESP32 field notes

Everything here is a failure that compiles, runs on someone's desk, and then
stops working. They are grouped by symptom, because that is what you have when
you arrive: not "an ADC problem" but "the reading is garbage since I enabled
Wi-Fi".

The full list - 160 entries, each linked to the thread that solved it - is in
[`reference/field-notes.md`](reference/field-notes.md). This page is the
part to read first.

## The five that account for most "random" failures

**1. Brownout is a power problem, never a code problem.** `Brownout detector was
triggered` appears the moment the radio turns on, because transmit peaks reach
~350 mA. A 3.3 V rail fed from a thin USB cable sags below the 2.5 V threshold.
Fix the supply — bulk capacitor at the module, a regulator rated for 500 mA, a
short thick cable — before touching the sketch.

**2. GPIO6-11 are the flash.** Driving one does not fail at compile time and does
not fail immediately; the module stops booting. `GPIO34-39` are input-only and
have no internal pull-up at all, so `INPUT_PULLUP` on them silently does nothing.

**3. ADC2 is dead while Wi-Fi is on.** Not degraded — unavailable. `analogRead`
returns 0 or noise. If the sketch reads an analog sensor and joins a network, the
sensor belongs on ADC1 (`GPIO32-39`).

**4. A watchdog reset is a symptom, not a bug.** `Task watchdog got triggered`
means a task did not yield for 5 s, usually a blocking call or a busy loop.
`Interrupt wdt timeout` means an ISR ran too long. Neither is fixed by disabling
the watchdog; both are fixed by finding what blocked.

**5. The first line of a panic is the diagnosis.** `LoadProhibited` is a null or
dangling pointer; `StoreProhibited` is writing through one; `IllegalInstruction`
is a corrupted function pointer or a stack overflow. The backtrace needs the
matching ELF, and `monitor_filters = esp32_exception_decoder` turns addresses
into file:line without manual work.

## Before you change code, check these

| Symptom | Check first |
|---|---|
| Board reboots when Wi-Fi starts | supply current and bulk capacitance |
| Board will not boot after a flash | strapping pins held at boot, especially GPIO0, 2, 12, 15 |
| `Failed to connect ... Timed out waiting for packet header` | USB cable, then hold BOOT while resetting |
| Sensor not found on I2C | pull-ups (4.7 kΩ, not the internal ones), then address conflicts |
| Garbled serial | baud mismatch, or the monitor is on the wrong UART |
| Sketch too big | partition table, not the compiler flags |
| Works for hours, then dies | heap fragmentation or a task stack that was sized by guess |

## How to use this skill

Start from the symptom in `reference/field-notes.md`, not from the section
title. Each entry is three lines: what you see, why it happens, what to change.
The link goes to the Stack Overflow question where the answer was worked out, so
you can read the full context when the short version is not enough.

If a rule here is wrong for your module, say so with the datasheet page — the
whole point of the file is that it stays true.

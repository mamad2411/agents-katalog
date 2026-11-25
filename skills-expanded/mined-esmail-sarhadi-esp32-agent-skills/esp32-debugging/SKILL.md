---
name: esp32-debugging
description: Use when an ESP32 crashes, reboots, or prints a Guru Meditation dump - decoding the backtrace, enabling the exception decoder, reading a core dump, and telling a panic from a watchdog from a brownout.
license: MIT
---

# Debugging an ESP32 crash

The board prints a page of hex and reboots. Everything needed to find the bug
is in that page, and almost nobody reads it because the first line is scary.

## Step 1: read the first line, not the dump

| First line | What it means |
|---|---|
| `Guru Meditation Error: Core 1 panic'ed (LoadProhibited)` | A read through a bad pointer. Null, freed, or out of bounds. |
| `... (StoreProhibited)` | A write through a bad pointer. Usually a buffer overrun. |
| `... (IllegalInstruction)` | Execution reached data. A corrupted function pointer. |
| `... (InstrFetchProhibited)` | The CPU jumped somewhere that is not code. |
| `Task watchdog got triggered` | A task held the CPU without yielding. Not a crash. |
| `Interrupt wdt timeout on CPU0` | An ISR ran too long, or a critical section is too long. |
| `RTCWDT_BROWN_OUT_RESET` | The supply dipped. Hardware, not firmware. |
| `***ERROR*** A stack overflow in task ...` | The task ran out of stack. |

The reason in the brackets is the whole diagnosis. A `LoadProhibited` with
`EXCVADDR: 0x00000000` is a null dereference; the same panic with a small odd
address like `0x00000004` is a null pointer plus a struct offset, which points
at a different line.

## Step 2: turn the backtrace into file:line

The dump ends with something like:

```
Backtrace: 0x400d4a3e:0x3ffb1f30 0x400d1f29:0x3ffb1f60 0x400d0c81:0x3ffb1f90
```

The first address of each pair is the code address. Feed them to addr2line
**with the exact ELF that was flashed** - a rebuild since then moves everything
and produces confident, wrong line numbers.

```bash
xtensa-esp32-elf-addr2line -pfiaC -e .pio/build/esp32dev/firmware.elf \
    0x400d4a3e 0x400d1f29 0x400d0c81
```

Frame 0 is the innermost call and the one to read first. `tools/panic_decode.py`
in this repository extracts the addresses and prints that command for you.

**Better: stop doing it by hand.** Add one line to `platformio.ini` and the
monitor decodes every backtrace as it arrives:

```ini
monitor_filters = esp32_exception_decoder
```

That filter is the single highest-value line in an ESP32 project.

## Step 3: when there is no backtrace

- A reset with no panic at all is usually the watchdog, brownout, or the reset
  pin. Check the `rst:` line at boot: `rst:0xc (SW_CPU_RESET)` means software,
  `rst:0x1 (POWERON_RESET)` means the supply.
- Enable the core dump to flash so a crash leaves a body behind: add a
  `coredump` partition and set `CONFIG_ESP_COREDUMP_ENABLE_TO_FLASH`. Then read
  it back with `esp-coredump info` against the same ELF.
- For anything timing-related, JTAG beats printf. The S3 and C3 have a built-in
  USB-JTAG; the classic ESP32 needs an ESP-Prog. A breakpoint on the faulting
  line is worth an hour of `Serial.println`.

## Rules for the agent

- Never guess from the symptom. Ask for the first line of the dump and the
  backtrace. "It resets randomly" has at least four different causes and they
  have different fixes.
- When you decode, state which ELF you used. A wrong ELF produces a plausible
  answer, which is worse than no answer.
- Do not add `delay()` calls to "fix" a watchdog. A watchdog firing means a task
  is blocking; the fix is to yield or move the work, not to feed the dog.
- After fixing a panic, say what the pointer was and why it was invalid. "Added
  a null check" without that sentence is a patch, not a diagnosis.

## Reference

[`reference/panic-codes.md`](reference/panic-codes.md) - Every panic reason and reset reason, with the first thing to check.

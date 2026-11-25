---
name: esp32-heap-forensics
description: Use when investigating heap leaks, fragmentation, allocation failures, TLS memory spikes, reconnect loops or long-uptime instability.
license: MIT
---

# Heap Forensics

A falling free-heap value does not by itself prove a leak. TCP TIME_WAIT, caches, allocator fragmentation, retained buffers and task stacks can all change memory statistics.

## Measure the right quantities

Track total free heap and largest free block for the relevant capability class (internal, DMA, PSRAM). Sample at consistent lifecycle points: before/after connect, after close, after idle recovery and after repeated cycles. Record minimum-ever free heap and allocation failures. Do not compare different capability pools.

## Find the owner

Instrument allocations around subsystem boundaries and use heap tracing where supported. Add checkpoints after DNS, TLS handshake, HTTP request, MQTT reconnect, socket close and task teardown. Capture task stack high-water marks independently; heap free space does not reveal stack exhaustion.

## Distinguish retention from leak

Repeat identical cycles and observe whether memory reaches a stable plateau. Account for lwIP TIME_WAIT and delayed reclamation; wait through expected network cleanup before concluding leak. A declining largest block with stable total free heap suggests fragmentation. Verify every error path frees resources and closes sockets.

## Integrity tools

Use heap integrity checks, poisoning, tracing and JTAG watchpoints when available for the target. Enable expensive diagnostics only in controlled builds because they change timing and memory use. Capture allocation and release backtraces when feasible.

## Verification

| Experiment | Interpretation |
|---|---|
| Repeated connect/close then idle | Rebound vs monotonic loss |
| Largest block shrinks, total stable | Fragmentation candidate |
| TLS-only repeated handshake | TLS-specific retention |
| Wi-Fi-only cycle | Driver/network baseline |
| Heap stable, task crashes | Inspect stack and races |

## Agent rules

Do not label TIME_WAIT or cache retention a confirmed leak. Report measurement method, capability pool, framework version and wait interval. Use a reproducible loop and quantify bytes per cycle.

## Field evidence to capture

- Record the exact ESP32 SoC, module, board revision and schematic revision.
- Record framework, compiler, driver version and relevant configuration flags.
- Preserve raw measurements and error codes before applying filters or retries.
- Separate a suspected cause from a reproduced root cause and a verified fix.
- Link the test result to a reproducible fixture or documented manual procedure.

## Version and safety boundary

Check the selected target's datasheet, errata and framework release notes before choosing APIs or pin capabilities. Electrical protection, isolation, overcurrent limits and safe outputs must be designed independently of firmware. A passing host test is not evidence of electrical compliance or field reliability.

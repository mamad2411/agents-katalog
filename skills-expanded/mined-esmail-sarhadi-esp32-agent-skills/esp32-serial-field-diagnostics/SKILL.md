---
name: esp32-serial-field-diagnostics
description: Use when diagnosing UART framing errors, RS485 timeouts, serial corruption, boot-log interference, FIFO overruns or intermittent field communication.
license: MIT
---

# Serial Field Diagnostics

Serial failures often appear as application protocol bugs even when the root cause is electrical timing, buffer sizing, pin routing or task starvation. Diagnose from the wire inward.

## Capture before changing code

Record baud, data bits, parity, stop bits, flow control, UART instance, GPIO mapping and driver version. Capture TX, RX, DE/RE and reference ground with a logic analyzer or oscilloscope. Preserve raw bytes and timestamps; formatted logs can hide framing and timing errors. Separate bootloader console from production protocol traffic.

## Buffer and scheduling

Size RX buffers for the largest burst plus scheduler latency, not average packet size. Check FIFO overflow, ring-buffer exhaustion and event-queue drops separately. Do not parse, allocate heap or print verbose logs inside UART ISR context. Use a single owner task or explicit synchronization for each UART driver.

## Protocol parsing

Treat UART as a byte stream. Frames may be split or coalesced across reads. Validate length, address, checksum/CRC and legal state transitions before using payload fields. Add inter-byte and whole-frame timeouts appropriate to the protocol. Resynchronize after malformed input without reading beyond buffer boundaries.

## Physical-layer isolation

Verify logic-level voltage and transceiver type before connecting external equipment. For RS485, verify direction control and bus termination; for RS232, use a level translator. Check ground reference, shield and isolation against installation topology. Swap A/B only as a controlled test after confirming vendor pin definitions.

## Verification

| Symptom | Capture |
|---|---|
| Garbled bytes | TX/RX waveform and UART decode |
| Missing final byte | TX completion vs DE transition |
| Burst loss | FIFO/ring-buffer high-water marks |
| Random protocol errors | CRC failures with timestamps |
| Works on USB, fails in field | Cable, transceiver, grounding and EMI |

## Agent rules

Do not patch the parser until physical waveform and framing are verified. Include bounded buffers and explicit lengths in examples. Never use unsafe string concatenation on raw serial data. Log counters and state transitions without flooding the protocol channel.


## Recovery validation

Verify that a malformed frame, UART overflow and remote-node reset each return the parser to a known idle state without rebooting the device.

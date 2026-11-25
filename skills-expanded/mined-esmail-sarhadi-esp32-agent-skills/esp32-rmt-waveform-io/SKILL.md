---
name: esp32-rmt-waveform-io
description: Use when implementing precise pulse generation, capture, IR, one-wire-style timing or custom waveform protocols on ESP32 with RMT; especially when symbols truncate, RX times out or Arduino and ESP-IDF examples use incompatible drivers.
license: MIT
---

# RMT waveform input and output

RMT is a hardware-timed symbol engine, not a general-purpose replacement for every GPIO interrupt.
Use it when edge timing must remain stable while tasks and radios are busy.

## First identify the target and driver generation

- Record the exact SoC, silicon revision, ESP-IDF release, Arduino-ESP32 core and board.
- Confirm that the selected chip implements the required RMT TX/RX channels and memory behavior.
- ESP-IDF's newer channel/encoder API differs from the legacy driver. Do not paste legacy `rmt_config()` examples into a project using the new API.
- Check Arduino-core release notes before relying on an RMT wrapper; the core may bundle a different ESP-IDF major/minor release.
- Pin the dependency and API generation in the example's build manifest.

## Model symbols and timing explicitly

- Convert protocol timings into source-clock ticks using the configured resolution; state rounding error.
- A symbol contains two level/duration phases. Check both durations against the target's field width.
- Split long idle intervals into legal symbols or use the driver's end-marker/idle mechanism.
- Keep carrier modulation, inversion and idle output level explicit; an electrically active idle can hold an external driver on.
- For RX, define minimum pulse, maximum pulse, idle threshold and maximum frame length from the protocol, not from a copied demo.

## TX design rules

- Allocate and configure the channel once during startup; do not repeatedly install/uninstall it in a fast path.
- Use a reusable encoder or bounded symbol buffer. Avoid heap allocation for every transmission.
- Check the transmit completion contract before reusing a buffer; asynchronous transmission may still be reading it.
- Set a finite transaction timeout and define what the caller does on timeout.
- Verify output polarity at the transceiver or LED, not only at the MCU pin.

## RX design rules

- Set a frame delimiter/idle threshold that is longer than valid intra-frame gaps but shorter than the maximum wait for a new frame.
- Treat a receive timeout as an empty/partial frame, not automatically as a valid packet.
- Validate symbol count, pulse ranges, preamble, framing and checksum before decoding fields.
- Bound the receive buffer and reject oversized frames before copying or parsing.
- Keep callbacks short; move decoding and logging to a task or queue.

## Concurrency and power

- Do not free or mutate a buffer until the driver signals completion.
- Serialize access to a channel if multiple tasks can transmit.
- Stop or reconfigure channels deliberately before light sleep/deep sleep; validate which clocks remain available on the selected SoC.
- Measure behavior with Wi-Fi/BLE active because ISR/task load can still affect buffer servicing even when edge timing is hardware generated.

## Minimal verification plan

1. Generate a known pattern with alternating short and long pulses.
2. Capture it with a logic analyzer and compare measured durations to the configured tick conversion.
3. Loop TX into RX through a safe level-compatible connection and test minimum/maximum frame lengths.
4. Inject a missing edge, stuck-high line, truncated frame and oversized frame.
5. Run repeated TX/RX while Wi-Fi traffic is active; check buffer ownership and timeout handling.
6. Repeat after sleep/wake and after a warm restart.

## Acceptance criteria

- The example builds against one pinned ESP-IDF release and documents the API generation.
- Unit tests cover tick conversion, symbol packing, frame bounds and malformed captures.
- Hardware evidence includes SoC, board, clock resolution, logic-analyzer capture and test conditions.
- No claim of protocol compatibility is made from a compile-only test.

## References

- ESP-IDF RMT: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/rmt.html
- ESP-IDF peripheral overview: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/index.html
- ESP-IDF release notes: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/esp-idf-en-v5.0-migration-guide.html

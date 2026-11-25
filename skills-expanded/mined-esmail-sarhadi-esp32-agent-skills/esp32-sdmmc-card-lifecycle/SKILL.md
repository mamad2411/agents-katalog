---
name: esp32-sdmmc-card-lifecycle
description: Use when integrating removable SD cards over SDMMC or SPI on ESP32; especially when mount is unreliable, cards corrupt after power loss, hot removal crashes the firmware or logging blocks real-time work.
license: MIT
---

# SD card interface and lifecycle

An SD card is a removable, variable-latency storage device. A successful mount does not prove that power-loss behavior or sustained writes are safe.

## Choose the host and wiring

- Identify SoC, module, board routing and ESP-IDF/Arduino version before selecting SDMMC or SPI mode.
- Check whether the target exposes the required SDMMC host and whether the board routes the needed pins.
- Use 1-bit SD mode when pin budget or routing requires it; use 4-bit only when all data lines are correctly wired and supported.
- SPI mode uses a different bus contract and shares the SPI host with other devices; assign chip select ownership explicitly.
- Verify card voltage, level compatibility, pull-ups and power-switch capability from the card and board specifications.
- Do not assume a breakout board includes adequate power integrity or level shifting.

## Mount and initialization

- Initialize the host and slot once; do not mount repeatedly from multiple tasks.
- Distinguish host-init, card-init, filesystem-mount and file-open failures in logs.
- Set an explicit mount point, max-open-file count and format-on-failure policy.
- Never format automatically after every mount error; a transient bus or power fault must not erase user data.
- Read card capacity and card type from the driver rather than hardcoding a model assumption.
- Keep card-detect handling separate from filesystem state; detect removal before issuing new I/O.

## Real-time logging

- Do not write synchronously from an ISR or motor-control loop.
- Queue bounded records to a storage task; define overflow behavior when the card stalls.
- Batch writes to reduce metadata and flash-program overhead, but bound the maximum data-loss window.
- Use explicit flush/sync points at meaningful transaction boundaries.
- Include sequence numbers and timestamps so incomplete tail records can be detected after a reset.
- Rotate logs by size or time; cap total storage use and define retention behavior.

## Removal and power failure

- Treat card removal during I/O as an expected fault, not an impossible event.
- Stop accepting new records, close files when possible and report the storage state to the application.
- A sudden power cut can leave the last sector or filesystem metadata incomplete; test the exact card and filesystem.
- Add hold-up energy only from a calculated power-fail budget; do not assume a capacitor guarantees a complete flush.
- Use a power-fail signal early enough to stop writes and flush within the measured hold-up interval.
- On restart, recover by validating record framing and sequence numbers, not by trusting the final line.

## Verification

- Test multiple card capacities and vendors; card behavior and latency vary.
- Measure worst-case write latency under a nearly full card and fragmented filesystem.
- Remove the card during open, write, flush and idle states.
- Cut power during writes and verify the recovery procedure and data-loss bound.
- Run concurrent Wi-Fi/MQTT traffic and confirm the logger does not starve control tasks.
- Test full-card, read-only, filesystem-corrupt and card-not-present conditions.

## Acceptance criteria

- Example builds for a named SoC and a documented SDMMC/SPI wiring profile.
- Host tests validate record framing, sequence recovery and queue-overflow policy.
- Hardware results include card model, filesystem, bus mode, clock, latency distribution and power-cut procedure.
- The project never treats mount success as proof of power-fail safety.

## References

- ESP-IDF SDMMC host: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/sdmmc_host.html
- ESP-IDF SDSPI host: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/sdspi_host.html
- ESP-IDF FAT filesystem: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/fatfs.html

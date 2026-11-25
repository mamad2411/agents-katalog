---
name: esp32-can-fd-gateway
description: Use when building CAN or CAN-FD gateways with ESP32, including TWAI, external CAN-FD controllers, bus-off recovery and industrial isolation.
license: MIT
---

# ESP32 Can Fd Gateway

Classic ESP32 TWAI is a Classical CAN controller, not CAN-FD. Some newer SoCs have different peripheral support; check the exact target. CAN-FD requires an FD-capable controller and transceiver path.

## Controller capability

- Verify TWAI presence and supported modes in the target datasheet and ESP-IDF release.
- Do not assume S2/S3/C3/C6/H2/P4 share the same CAN peripheral capability.
- For CAN-FD, select an external FD controller such as an SPI-attached device and a matching FD transceiver; a Classical CAN transceiver/controller cannot transmit FD frames.
- Keep controller, transceiver and protocol support distinct in the design document.

## Physical bus

- Terminate the CAN differential pair with 120 Ω at the two physical ends only; measure approximately 60 Ω across CANH/CANL on an unpowered, correctly terminated bus.
- Use twisted pair, appropriate common-mode range, isolation and surge protection for industrial wiring.
- Keep stubs short relative to bitrate and topology.
- Select transceiver standby, slope and fault behavior deliberately.

## Firmware behavior

- Configure bitrate and sample point to match the network; CAN-FD has separate nominal and data phase rates.
- Handle error-passive and bus-off states explicitly; define bounded recovery and expose counters.
- Use hardware acceptance filters where available; avoid unbounded application queues.
- Timestamp frames and preserve arbitration ID, DLC, flags and payload length without truncation.

## Gateway safety

- Define ID translation, rate limiting, filtering and loop prevention.
- Never blindly bridge safety-critical frames between buses with different bitrate or semantics.
- Preserve FD/BRS/ESI flags and reject unsupported frames explicitly.
- Provide watchdog behavior that leaves outputs in a safe state if the gateway stalls.

## Verification

| Test | Expected result |
|---|---|
| Two-node nominal bus | ACK and correct frames |
| Missing termination | Error counters reveal degradation |
| Bus-off injection | Recovery policy executes |
| FD frame on Classical CAN path | Explicit rejection, no silent truncation |
| Gateway overload | Bounded queue and observable drops |

## Agent rules

- State controller and transceiver part numbers separately.
- Never label Classical CAN as CAN-FD.
- Require a bus topology and bitrate before generating a pin/wiring example.
- Treat bus-off recovery as a system policy, not an unconditional automatic retry.

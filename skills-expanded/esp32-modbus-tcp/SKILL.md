---
name: esp32-modbus-tcp
description: Use when an ESP32 implements or debugs Modbus TCP, including MBAP framing, transaction IDs, register maps, gateway behavior or TCP session failures.
license: MIT
---

# ESP32 Modbus Tcp

Modbus TCP removes the serial CRC and RTU silence timing, but it does not remove register-map ambiguity, concurrency or network failure. Keep protocol state per TCP connection and never assume one request per socket.

## MBAP framing

- Parse the 7-byte MBAP header before the PDU: transaction ID, protocol ID, length and unit ID.
- Protocol ID must be zero. Validate the declared length against the received buffer and configured maximum before reading the PDU.
- TCP is a byte stream: one read may contain half a frame or several frames. Implement an incremental parser; never equate one recv() with one Modbus message.
- Echo the transaction ID and unit ID in the response. Reject malformed lengths and unsupported function codes cleanly.

## Register map and concurrency

- Document zero-based PDU addresses separately from human labels such as 40001.
- Use explicit endianness and word order for 32-bit values; vendor conventions vary.
- Protect shared process data when a network task and control task access it. Snapshot values before encoding a response.
- A gateway must map Unit Identifier to the downstream RTU slave deliberately and serialize access to a half-duplex bus.

## Network behavior

- Bound simultaneous clients, idle sessions, request rate and response time.
- Handle partial send, peer close, timeout, reconnect and Wi-Fi loss without leaking sockets.
- Do not block a control loop while waiting for a TCP client or downstream RTU response.
- Expose counters for malformed frames, timeouts, disconnects and exception responses.

## Verification matrix

| Test | Expected result |
|---|---|
| Header split across two TCP writes | Parser waits, then emits one frame |
| Two ADUs in one write | Both parsed in order |
| Invalid protocol ID or length | Rejected without buffer overrun |
| Two concurrent clients | Independent transaction IDs and state |
| RTU gateway busy | Bounded queue or explicit exception, never silent corruption |

## Agent rules

- Use a maintained Modbus stack where possible; do not hand-roll unbounded parsers.
- State whether the endpoint is server, client or RTU/TCP gateway.
- Keep register scaling, signedness and byte order in a versioned map.
- Never claim deterministic control timing over ordinary Wi-Fi/TCP.

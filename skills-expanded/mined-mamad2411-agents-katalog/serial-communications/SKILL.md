---
name: serial-communications
domain: software
level: technology
description: RS232/RS485/USB-HID transport specifics — wiring, addressing, and driver-level pitfalls. Deliberately not Modbus-specific; see automation/modbus once an actual Modbus PDU/register scheme is in play.
tags: [rs485, rs232, "usb-hid", "serial port", "com port"]
triggers: [rs485, rs232, "usb-hid", "serial port", "com port", "baud rate", "hid device"]
version: "1.0.0"
requires: []
recommends: [engineering/protocol-engineering]
capabilities: []
conflicts: []
when_to_use: Working with a device over a raw serial link (RS232/RS485) or USB-HID — the
  transport layer itself, before any higher-level protocol running over it.
when_not_to_use: A device that speaks Modbus over that serial link — the addressing, function
  codes, and register scheme are automation/modbus's territory, not this skill's. RS485/RS232
  being the physical/electrical transport does not imply Modbus is the protocol running over
  it — plenty of RS485 devices use a proprietary or vendor-specific framing instead.
---

# Skill: serial-communications

## Purpose

The transport-level facts specific to RS232/RS485/USB-HID — separate from whatever protocol
happens to run over the transport (see `engineering/protocol-engineering` for the
protocol-layer method, and `automation/modbus` specifically if the device actually speaks
Modbus).

## Method

1. **RS485 is a multi-drop, half-duplex electrical bus by default** — multiple devices share
   the same two wires, and only one may transmit at a time. A driver/adapter that doesn't
   correctly manage the transmit-enable line (often DE/RE on an RS485 transceiver chip) causes
   bus contention that looks like random corruption, not a clean error.
2. **RS485 device addressing is not standardized across vendors** — unlike a protocol like
   Modbus which defines its own addressing scheme on top of the bus, a raw/proprietary RS485
   device's "address" is whatever that vendor's own framing defines; don't assume a Modbus-style
   unit-ID byte exists just because the transport is RS485.
3. **RS232 point-to-point wiring has real gotchas independent of software**: TX/RX crossed
   correctly (or not, if a null-modem adapter is or isn't in the path), the flow-control mode
   (none/hardware RTS-CTS/software XON-XOFF) matching on both ends, and ground reference —
   many "the device doesn't respond" issues are wiring/flow-control mismatches, not code bugs.
4. **Baud rate, parity, data bits, and stop bits must match exactly on both ends** — a
   mismatched baud rate doesn't always fail cleanly; it can produce plausible-looking garbage
   that's tempting to debug as a framing/checksum bug in the higher-level protocol instead of
   what it actually is.
5. **USB-HID is report-based, not a raw byte stream** — data moves as fixed-size "reports"
   (defined by the device's HID report descriptor), not an arbitrary byte stream like a serial
   port. Reading/writing the wrong report ID, or assuming report length is flexible when the
   descriptor fixes it, is the most common USB-HID integration bug.
6. **A USB-HID device's report descriptor is the actual source of truth for its data layout** —
   when available (via a USB descriptor dump, not vendor prose documentation, which is
   frequently wrong or outdated), trust the descriptor over a written spec.
7. **Driver-level device enumeration (COM port number, HID path) is not stable across
   replug/reboot on many systems** — code that hardcodes a COM port number or HID path breaks
   the moment the device is plugged into a different port; enumerate and match on a stable
   identifier (VID/PID, serial number) instead where the device provides one.
8. **Verify against real hardware, not just a mock/simulated transport**, before trusting a
   fix — a serial/USB driver-level issue (timing, buffering, flow control) frequently doesn't
   reproduce in a simulated loopback.

## Anti-patterns

- Assuming an RS485 device's addressing/framing follows Modbus conventions just because the
  transport is RS485.
- Hardcoding a COM port number or USB-HID device path instead of enumerating by a stable
  identifier.
- Debugging plausible-looking garbage data as a protocol/checksum bug before ruling out a
  baud-rate/parity mismatch.

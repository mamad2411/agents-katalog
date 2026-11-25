---
name: esp32-modbus-rtu-slave
description: Use when the ESP32 must be a Modbus RTU slave for a PLC or SCADA master - the master times out, gets exception 02 or 04, or reads stale values. Covers address range, response timing, exception codes and register mapping.
license: MIT
---

# ESP32 as a Modbus RTU slave

Being a slave is a different job from being a master: you do not control timing,
you answer within it, and every malformed request is a chance to hang the bus.

## Address rules

- Slave addresses 1 to 247. Address 0 is broadcast: **execute, never answer**.
- 248 to 255 are reserved. A device answering on 0 collides with every other
  node on the bus.
- Answer only when the address matches, and drop frames with a bad CRC silently -
  a slave that answers a corrupt frame creates collisions.

## Timing

- 3.5 character times of silence ends a frame. At 9600 baud one character is
  about 1.04 ms, so the gap is about 3.6 ms; at 115200 it is 0.3 ms and most
  software timers cannot measure it. Use the UART idle/frame timeout or a
  hardware timer.
- Answer within the master's response timeout, typically 100 to 1000 ms. Faster
  is better; a slave that takes 900 ms makes a 10-register poll take 9 seconds.

## Exception codes that mean something

| Code | Name | When |
|---|---|---|
| 01 | illegal function | function code not supported |
| 02 | illegal data address | register does not exist |
| 03 | illegal data value | quantity or value out of range |
| 04 | slave device failure | internal error while processing |
| 06 | slave device busy | reject, retry later |

Returning 02 for a register that exists but is not readable yet is wrong; that is
04. The distinction tells the integrator whether to fix the map or retry.

## Register mapping

- Holding registers are 16 bit. A 32-bit value spans two registers, and the word
  order is a per-device decision - document it.
- Scaling belongs in the documentation: a temperature of 23.5 as 235 with a
  stated scale of 0.1 is honest; a float split across registers with no note is
  not.
- Keep a gap between read-only and read-write blocks so a master cannot
  accidentally write a status register.

## Symptom table

| Symptom | Usually |
|---|---|
| master times out on every request | slave address, baud, parity |
| exception 02 | address map does not match the documentation |
| answers once, then silent | response longer than the master's timeout |
| bus hangs when two masters poll | two slaves with the same address |
| values update late | the application updates the register array only once a second |

## Agent rules

- Publish the register map with addresses, types, scales and access.
- Handle broadcast (address 0) as write-only, no response.
- Never answer a frame with a bad CRC.

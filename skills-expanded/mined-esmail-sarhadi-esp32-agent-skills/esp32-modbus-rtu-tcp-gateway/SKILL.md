---
name: esp32-modbus-rtu-tcp-gateway
description: Use when an ESP32 bridges Modbus RTU on RS485 to Modbus TCP on Ethernet or Wi-Fi - the SCADA reads time out, unit ids do not map, or two clients collide. Covers MBAP framing, transaction ids and serialisation.
license: MIT
---

# Modbus RTU to TCP gateway

A gateway is not a byte pump. Modbus TCP and Modbus RTU have different framing,
different error reporting and different timing, and the translation is where the
bugs live.

## The frames are not the same

| | RTU | TCP |
|---|---|---|
| Framing | 3.5 char silence | MBAP header with a length field |
| Addressing | slave address byte | unit id byte inside MBAP |
| Error check | CRC16 | none (TCP checksums) |
| Transaction | implicit | transaction id, echoed back |
| Max PDU | 253 bytes | 253 bytes |

The unit id in MBAP is not always the RTU slave address. Many gateways map it,
and a master that sends unit 1 expecting device 17 needs a mapping table, not a
pass-through.

## Serialise the serial side

RS485 is half duplex and one transaction at a time. Two TCP clients polling at
once must be queued, not interleaved: the second request waits for the first
response or timeout. A gateway that forwards both corrupts the bus and produces
CRC errors that look like a wiring fault.

- One request queue, one worker.
- Per-request timeout (typically 300 to 1000 ms) and one retry at most.
- On timeout, return exception 0x0B (gateway target device failed to respond) -
  that is what the code is for.

## Transaction ids and pipelining

Modbus TCP allows several outstanding transactions, identified by transaction id.
A gateway that answers with the wrong transaction id makes the master discard
valid data. Echo the id byte for byte.

## Throughput reality

At 9600 baud an RTU frame of 8 bytes takes about 9 ms on the wire plus the
device's turnaround, so a gateway tops out around 30 to 50 transactions per
second. A SCADA polling 500 registers one at a time will not be happy - batch
with function 03 reading 125 registers per request.

## Symptom table

| Symptom | Usually |
|---|---|
| TCP connects, every read times out | unit id not mapped to a slave address |
| intermittent CRC errors | two TCP clients interleaving on the bus |
| master discards responses | transaction id not echoed |
| works with one client, not two | no request queue |
| slow but correct | one register per request, at 9600 baud |

## Agent rules

- Publish the unit-id to slave-address mapping table.
- State the queue depth, the timeout and the retry policy.
- Return 0x0B on a device timeout instead of a TCP-level error.

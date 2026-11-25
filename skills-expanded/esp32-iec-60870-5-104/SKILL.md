---
name: esp32-iec-60870-5-104
description: Use when an ESP32 talks to a SCADA master over IEC 60870-5-104 - the connection starts and drops, general interrogation never finishes, or the master reports sequence errors. Covers APCI framing, k/w windows and ASDU types.
license: MIT
---

# IEC 60870-5-104 on ESP32

IEC 104 is IEC 101 over TCP, port 2404. It is the protocol behind a large share
of substation and utility SCADA, and it is unforgiving about sequencing.

## The three frame types

| Type | First byte | Purpose |
|---|---|---|
| I | bit0 = 0 | numbered information, carries an ASDU |
| S | `0x01` | supervisory ack, no data |
| U | `0x03` | start/stop/test: STARTDT, STOPDT, TESTFR |

A connection is not usable until the master sends `STARTDT act` and the device
answers `STARTDT con`. Data sent before that is ignored, and the device looks
connected while nothing arrives.

## Sequence numbers are 15 bit

Both directions count I-frames modulo 32768. The master expects `Ns` to increase
by one per frame and acknowledges with `Nr`. A device that resets its counter
without a new connection produces sequence errors and the master drops the link.

The k and w parameters are the window: k is how many unacknowledged I-frames may
be outstanding (default 12), w is how many received frames before an S-frame must
be sent (default 8). With k = 12, a burst of 13 readings without waiting for an
ack is a protocol violation, not a performance choice.

## Timers

| Timer | Default | Meaning |
|---|---|---|
| t0 | 30 s | connection establishment |
| t1 | 15 s | send or test timeout, then close |
| t2 | 10 s | ack timeout for received frames |
| t3 | 20 s | idle test frame interval |

t3 matters on a quiet line: with no data, the device must send `TESTFR act` and
expect `TESTFR con`, or the master assumes the link is dead.

## ASDU essentials

- Type identification: 1 = single point, 3 = double point, 13 = measured value
  short float, 30/36 = with timestamp, 45 = single command, 100 = interrogation.
- Cause of transmission: 3 = spontaneous, 5 = requested, 6 = activation,
  7 = activation confirmation, 20 = unknown type.
- Common address (ASDU address) and information object address (IOA, 3 octets)
  must match the master's configuration exactly. One wrong IOA and the point
  silently never appears.

## General interrogation

The master sends C_IC_NA_1 (100) with cause 6. The device answers with cause 7,
then sends every point with cause 20, then a final C_IC_NA_1 with cause 10. Skip
the final frame and the master waits until t1 expires and closes.

## Symptom table

| Symptom | Usually |
|---|---|
| connects, no data | STARTDT not answered |
| drops every 20 s | no TESTFR response on an idle link |
| sequence errors after a reboot | Ns not reset with the connection |
| points missing in SCADA | IOA or common address mismatch |
| interrogation never completes | missing final activation termination |
| works with one master, not another | k/w window or timestamp format |

## Agent rules

- Implement the state machine (stopped, started, testing) before any point
  mapping; most failures are state, not data.
- Log every APCI frame with its Ns/Nr during bring-up.
- Never invent an IOA map: it comes from the master's point list.

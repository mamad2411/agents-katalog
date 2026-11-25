---
name: esp32-canopen-basics
description: Use when an ESP32 joins a CANopen network - drives, IO modules or sensors - and the node stays in pre-operational, PDOs never arrive, or SDO reads time out. Covers NMT, node IDs, COB-IDs and heartbeat.
license: MIT
---

# CANopen on ESP32

CANopen is a profile on top of CAN: a state machine per node, a fixed COB-ID
scheme, and object dictionary entries instead of raw registers. An ESP32 with
TWAI can speak it; it needs a CAN transceiver like any other CAN node.

## Node ID decides every COB-ID

A node id from 1 to 127. Every default COB-ID is derived from it:

| Object | COB-ID | Direction |
|---|---|---|
| NMT | 0x000 | master to all |
| SYNC | 0x080 | producer to all |
| EMCY | 0x080 + node | node to master |
| SDO transmit (server to client) | 0x580 + node | node answers |
| SDO receive (client to server) | 0x600 + node | master asks |
| Heartbeat | 0x700 + node | node to master |
| PDO1 transmit | 0x180 + node | node sends |
| PDO1 receive | 0x200 + node | node listens |

Two nodes with the same id is the most common commissioning error and produces
exactly the behaviour you would expect: nothing works, intermittently.

## The state machine

After power-up a node is in **pre-operational**: SDO works, PDO does not. The NMT
master sends `start` (0x01) to move it to operational, where PDOs flow. A node
that answers SDO reads but never sends process data is simply still in
pre-operational - check the NMT state before debugging the PDO mapping.

## SDO and PDO in one sentence each

- **SDO** is a confirmed read/write of an object dictionary entry (index and
  sub-index), with a segmented transfer for anything over 4 bytes.
- **PDO** is an unconfirmed, pre-mapped frame: the mapping decides which object
  bytes sit at which offset, and it is configured over SDO at startup.

## Heartbeat vs node guarding

Heartbeat (0x700 + node) is a producer with a period. Node guarding is the older
request/response scheme. Pick one: enabling both makes the master report timeouts
that are not real.

## Symptom table

| Symptom | Usually |
|---|---|
| SDO read times out | wrong node id, or the node is in a different state |
| PDO never arrives | node still pre-operational, or mapping not written |
| intermittent everything | two nodes with the same id |
| heartbeat timeouts under load | bus load too high, or heartbeat period too short |
| bus-off after a while | missing termination, or bitrate mismatch |
| EMCY storms | one node faulting, check the emergency code |

## Agent rules

- State node id, bitrate and termination before any object dictionary work.
- Configure PDO mapping over SDO at startup and log the result.
- Do not invent object dictionary entries; they come from the device's EDS file.

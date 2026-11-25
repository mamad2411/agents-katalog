---
name: esp32-can-twai
description: Use when an ESP32 joins a CAN bus - no frames arrive, the bus goes off after a while, the bitrate will not match, or the transceiver is missing. Covers TWAI setup, termination, bitrate and bus-off recovery.
license: MIT
---

# CAN (TWAI) on ESP32

The ESP32 has a CAN 2.0B controller called TWAI. It is a controller only: the
transceiver, the termination and the bus itself are your problem.

## Which chips have it

The classic ESP32, the C3 and the C6 have a TWAI controller. The **S2 and S3 do
not** - a design that needs CAN and picked an S3 has to add an external
controller over SPI. Check this before writing the driver.

## The transceiver is not optional

TWAI pins are logic-level TX and RX. A CAN bus is differential and needs a
transceiver (3.3 V parts exist, e.g. SN65HVD230). Connecting TX/RX directly to
CANH/CANL damages both ends and never works.

## Termination

120 ohms at **both physical ends** of the bus, and nowhere else. Two nodes on a
bench need two resistors; a long bus with ten nodes still needs two, at the ends.
A missing termination shows up as frames that work at 125 kbit/s and fail at
500 kbit/s.

## Bitrate

Every node must use the same nominal bitrate and the same sample point. A node at
500 kbit/s on a 250 kbit/s bus does not "fail to receive" - it floods the bus with
error frames and takes the whole segment down.

## Bus-off

A node that accumulates too many errors goes bus-off: it stops transmitting and
listening. The controller can recover automatically, or only when told. For a
product, automatic recovery with a backoff is usually right; for diagnostics,
manual recovery tells you how often it happened.

## Filters

Acceptance filters decide which identifiers reach the driver. An empty filter set
that accepts everything is fine on a bench and wrong on a vehicle bus: the CPU
spends its time discarding frames.

## Symptom to cause

| Symptom | Usually |
|---|---|
| no frames at all | no transceiver, TX/RX swapped, no termination |
| works until traffic rises | bitrate or sample point mismatch |
| goes silent after a while | bus-off, no recovery configured |
| frames arrive twice | two nodes transmitting the same identifier |

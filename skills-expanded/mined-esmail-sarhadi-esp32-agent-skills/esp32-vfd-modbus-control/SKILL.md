---
name: esp32-vfd-modbus-control
description: Use when an ESP32 controls a variable frequency drive over RS485 - the drive ignores commands, runs at the wrong speed, faults on start, or the register map does not match the manual. Covers control words, scaling and safe states.
license: MIT
---

# Controlling a VFD over Modbus

A drive is the most dangerous thing on the bus: a wrong register write spins a
motor. The rules below are about not doing that by accident.

## Register maps are per vendor, not per protocol

Modbus defines the transport, not the register numbers. A Shihlin, an ABB and a
Danfoss drive all speak Modbus RTU and none of them share a register map. Take the
map from the manual of the exact model and firmware, and put the source page in
the skill's reference file.

Two conventions to check before writing anything:

- **0-based vs 1-based**: the manual says 40001, the wire carries 0. Off by one
  writes the neighbouring parameter.
- **Word order for 32-bit values**: frequency setpoints are often two registers,
  and vendors disagree on which comes first.

## The control word is a state machine

Most drives expose a command register with bits for run, direction, fault reset
and a "command source = communication" bit. Writing "run" without setting the
source bit does nothing, and writing run before the drive is ready causes a
fault. The sequence is: enable communication control, clear the fault, set the
speed reference, then assert run.

## Ramp and reference

- Set acceleration and deceleration in the drive, not by ramping the setpoint in
  the ESP32. A network dropout then does not produce a step change.
- The reference is scaled: 0 to 100 % of a parameter, or 0 to the max frequency
  in 0.01 Hz units. Getting this wrong runs the motor at 1 % or 100 times the
  intended speed.
- Write the reference **before** the run command, and verify it by reading back.

## Safe state

- A communication timeout must stop the drive. Configure the drive's own watchdog
  (most have a "communication loss" action), do not rely on the ESP32 to send a
  stop.
- Emergency stop is hard-wired. It must never depend on Modbus.
- On the ESP32 side, keep the last good state and stop writing when the link is
  down; do not retry a run command in a loop.

## Symptom table

| Symptom | Usually |
|---|---|
| drive ignores run | command source not set to communication |
| runs at 1 % speed | reference scale wrong (0.01 Hz vs %) |
| faults at every start | run asserted before the drive is ready |
| parameter written, no effect | 40001 vs 0 offset |
| runs backwards | direction bit, or motor wiring |
| keeps running after the cable is cut | drive watchdog not configured |

## Agent rules

- Quote the register numbers **with the manual page** for the exact model.
- Show the scaling arithmetic for the reference and the readback.
- Never propose a design where a network message is the only way to stop the
  motor.

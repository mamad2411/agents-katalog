---
name: esp32-actuators-and-relays
description: Use when an ESP32 drives a relay, solenoid, servo or motor - the coil browns out the board, the relay clicks but the contact does nothing, the servo jitters, or the LED glows when it should be off. Covers drive circuits, flyback, inrush and isolation.
license: MIT
---

# Actuators and relays on ESP32

A GPIO delivers 12 mA at 3.3 V. Every actuator in this file needs more than that,
and the interesting failures are the ones where it almost works.

## A relay coil is never driven by a GPIO

A 5 V relay coil is 70 to 90 mA and inductive. It needs a transistor, a base
resistor, and a flyback diode across the coil. Without the diode, the collapse
of the coil field puts a negative spike on the collector that kills the
transistor, and through the shared ground it can reset the ESP32.

The symptom is specific: the board resets when the relay *opens*, not when it
closes.

## Inrush is the real load

An incandescent lamp, a motor or a capacitive supply draws 5 to 15 times its
running current for the first tens of milliseconds. A 10 A relay driving a 60 W
LED driver sees 40 A peaks. Contacts weld, or the supply sags and the ESP32
browns out - which looks like a firmware crash that happens only at switch-on.

Snubber (RC) across the contact for AC loads, a varistor for inductive ones.

## Solid state relays leak

A triac SSR passes a milliamp or two when off. That is enough to make a small
LED lamp glow dimly or keep a contactor humming. It is not a wiring fault and no
amount of software fixes it: add a bleeder resistor across the load, or use a
mechanical relay.

## Servos: the pulse is not the problem

A hobby servo expects 1 to 2 ms pulses every 20 ms and draws 200 mA to 1 A when
moving. Two rules:

- Power servos from a separate 5 V rail, with the grounds joined at one point.
  Powering from the board's regulator is the reason the ESP32 resets on every
  movement.
- Jitter in a servo usually means a software PWM loop, not a bad servo. LEDC at
  50 Hz with 16-bit resolution gives 0.03 % timing error; a `delayMicroseconds`
  loop in the main loop gives whatever the Wi-Fi stack allows.

## Isolation is a decision, not a default

Anything that switches mains, or leaves the enclosure, is a candidate for an
optocoupler or a relay with a real isolation gap. The ESP32 side and the load
side should not share a ground across that boundary.

## Symptom table

| Symptom | Usually |
|---|---|
| resets when the relay opens | no flyback diode |
| resets when a motor starts | inrush, supply sag, shared ground |
| relay clicks, no switching | contact rated for AC used on DC (or the reverse) |
| LED glows when off | SSR leakage, or a pull-up on the drive pin |
| servo jitters, board fine | software PWM, or servo supply on the 3.3 V rail |
| works with a bench supply, not with the product | the supply cannot deliver the peak |

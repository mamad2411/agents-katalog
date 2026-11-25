---
name: esp32-emc-and-enclosure
description: Use when a working board fails once it is in its box - range collapses, the sensor drifts, the device resets when a motor runs nearby, or it dies of heat. Covers antenna keepout, grounding, cable routing and thermal limits.
license: MIT
---

# The enclosure changes the circuit

Every measurement on the bench is taken with the board in the air, with short
wires and no lid. The product is the opposite of that.

## The antenna keepout is not a suggestion

- 15 mm of no copper, no battery, no metal, in front of the antenna. A LiPo pouch
  taped over the antenna is a 10 to 20 dB attenuator.
- No ground plane under the antenna. A solid pour under a PCB antenna detunes it;
  the module's own reference design shows the cutout for a reason.
- A metal enclosure needs an external antenna (u.FL) and a proper feed-through.
  No amount of software gain recovers a sealed aluminium box.

Range that drops from 40 m to 3 m after assembly is almost always one of these
three, not the firmware.

## Grounding

- One ground reference. Splitting analog and digital grounds and joining them at
  a single point is fine on a mixed-signal board; two grounds connected by a
  thin trace and a long cable is an antenna.
- Star the power returns at the regulator, not at the connector.
- A shield connected at both ends carries current. Connect it at one end unless
  it is an RF shield.

## Cables are the other antenna

Every wire leaving the board is an antenna and a path for ESD. A sensor on a
1 m cable picks up the switching regulator's harmonics and the motor's commutation
noise; the reading drifts and the fix is a ferrite, a shielded cable, or a
differential interface - not more averaging.

Keep signal and power cables apart, and never run a signal cable parallel to a
mains or motor cable for any distance.

## Reset when a motor or relay switches

That is conducted and radiated noise entering the reset line or the supply. Three
fixes, in order: a 100 nF from EN to ground at the pin, a series resistor on the
reset trace, and better separation of the noisy load's return path.

## Heat

An ESP32 at full Wi-Fi transmit dissipates about 0.5 W; add a linear regulator
dropping 12 V to 3.3 V and it is watts. In a sealed IP65 box the internal
temperature rises 20 to 30 °C above ambient. Consequences:

- The ADC drifts (the reference is temperature dependent).
- The RTC drifts.
- A LiPo above 45 °C ages fast; above 60 °C it is a hazard.
- The chip throttles or resets at its junction limit.

Measure the internal temperature with the lid on, at the worst ambient the
product will see, before deciding the enclosure is finished.

| Symptom | Usually |
|---|---|
| range collapses in the box | antenna keepout violated, or metal lid |
| sensor drifts after an hour | self-heating, or the ADC reference temperature coefficient |
| resets when a nearby motor runs | noise on EN or the supply |
| works open, fails closed | connector strain, or a wire shorting on the lid |
| dies after a month in summer | thermal, not firmware |

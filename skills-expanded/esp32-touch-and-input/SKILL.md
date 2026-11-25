---
name: esp32-touch-and-input
description: Use when capacitive touch or buttons misbehave - touch triggers by itself, works dry and fails when wet, a button bounces, or the pin reads pressed at boot. Covers touch sensing, calibration, debounce and the GPIO matrix.
license: MIT
---

# Touch and input on ESP32

Touch sensing measures capacitance; every wire, every enclosure and every hand
changes it. That is why touch designs fail in the field and pass on the bench.

## Which chips have capacitive touch

The classic ESP32 has ten touch channels (GPIO4, 0, 2, 15, 13, 12, 14, 27, 33,
32) and the ESP32-S2 has fourteen. The **S3, C3 and C6 do not** - a design that
needs touch and picked an S3 needs an external controller (TTP223, CAP1203, or a
touch-capable display).

## Reading it properly

`touchRead()` returns a raw count that drifts with temperature and supply
voltage. Do not compare it to a constant:

- Take a baseline at boot with nothing touching (average of 20 reads).
- Trigger on a delta from that baseline, not on an absolute value.
- Re-baseline slowly while untouched, so a humid day does not look like a finger.

The hardware also offers an interrupt threshold (`touchAttachInterrupt`) that
fires without polling, which is what you want for a wake source from deep sleep.

## The pad is a capacitor with a long antenna attached

- Long traces pick up mains hum and the switching regulator. Keep the trace
  under 10 cm and surrounded by ground.
- A ground plane directly under the pad increases the baseline and reduces the
  delta. A hatch, not a solid pour, is the usual compromise.
- Water on the panel is a conductor: a design that works dry and triggers
  continuously when wet needs a guard ring driven at the same potential, or a
  different sensing technology.

## Buttons: bounce, and the pull that is not there

Mechanical contacts bounce for 1 to 10 ms. A 20 ms debounce in software is
enough for a human and too slow for nothing. Two hardware rules:

- GPIO34 to 39 have no internal pull-ups. A button there with `INPUT_PULLUP`
  reads floating and looks pressed at random.
- GPIO0, 2, 5, 12 and 15 are strapping pins. A button that holds one of them at
  boot changes the boot mode - the board flashes instead of running.

## Wake from deep sleep

Only RTC GPIOs can wake the chip. On the classic ESP32 that is GPIO0 to 15 and
25 to 27; on the S3 it is 0 to 21. A button on GPIO35 wakes nothing, no matter
what the code says.

| Symptom | Usually |
|---|---|
| touch fires with nothing near | baseline taken with a hand on the board, or no ground reference |
| works dry, fails wet | water bridging pads, no guard ring |
| reads pressed at boot | floating input (34-39), or a strapping pin |
| double triggers per press | no debounce, or debounce on the wrong edge |
| battery drains in a week | polling touch in a loop instead of waking on the interrupt |

---
name: esp32-addressable-leds
description: Use when driving WS2812, SK6812 or APA102 strips from an ESP32 - power sizing, the 3.3 V data problem, colour order, refresh budget and why a strip flickers once Wi-Fi is on.
license: MIT
---

# Addressable LEDs on ESP32

An LED strip is a power supply problem with a data protocol attached. Most
"flickering" and "the last LEDs are the wrong colour" reports are power, not
code, and most "it works on 10 LEDs and breaks on 300" reports are refresh
budget.

## Power comes first

- Budget up to **60 mA per LED at full white** (vendor figure). 300 LEDs is
  about 18 A, not 1 A. A USB port cannot do this.
- Inject power every 100-150 LEDs. Voltage drop along the strip turns the far
  end orange because the blue channel needs the most headroom.
- Put a 1000 µF electrolytic across 5 V and GND near the strip. It absorbs the
  inrush at power-up, which otherwise browns out the ESP32 and looks like a
  random reset.
- Never power the strip from the ESP32's 3V3 pin. The regulator is sized for the
  module, not for a light.

## The 3.3 V data problem

WS2812B running at 5 V has a logic-high threshold of about 0.7 × VDD, so it
wants 3.5 V on the data line. The ESP32 drives 3.3 V. It usually works, and then
fails at a different temperature, on a longer wire, or on a different batch.

- Proper fix: a 74AHCT125 (or 74HCT1G125) level shifter on the data line. Use
  the **AHCT/HCT** part, not HC: those have TTL input thresholds and accept a
  3.3 V input.
- Series resistor: 330-470 Ω between the ESP32 pin and the first LED's DIN. It
  kills the ringing that corrupts the first pixel.
- The clock line of APA102/SK9822 is more forgiving and those chips accept 5 V
  logic, which is why they are the safer choice for long runs.

## Colour order and depth

- WS2812B is **GRB**, not RGB. Getting this wrong produces green where red
  should be, which people blame on the library.
- SK6812 RGBW is **four** bytes per LED. Sizing buffers with `numLeds * 3`
  corrupts the whole strip from the first pixel onward.
- Global brightness in software multiplies 8-bit values and loses resolution:
  at brightness 16, every channel has only 16 levels and gradients band. If
  smooth low-light is the goal, keep 16-bit values internally and scale at the
  end.

## Refresh budget

One WS2812 bit is 1.25 µs, so one LED is 30 µs:

| LEDs | Frame time | Max frame rate |
|---|---|---|
| 30 | 0.9 ms | well over 200 fps |
| 300 | 9 ms | about 110 fps |
| 1000 | 30 ms | about 33 fps |

Add the reset gap (50-300 µs) per frame. Above roughly 300 LEDs, a 60 fps
animation is no longer free and the effect has to be written accordingly.

## Why it flickers when Wi-Fi connects

Bit-banging the data line in a loop works until an interrupt fires mid-frame.
Wi-Fi raises interrupts constantly, and a single late edge corrupts every pixel
after it.

- Use the RMT peripheral (the `rmt` driver, or the `Adafruit_NeoPixel` /
  `FastLED` backends that use it). The hardware generates the waveform and the
  timing does not care about interrupts.
- Keep the buffer in RAM and hand it to the peripheral once per frame.
- Do not call `show()` from two tasks at once, and do not call it from an ISR.

## Rules for the agent

- Before writing animation code, ask how many LEDs and what supply. The answer
  decides whether the design is possible at all.
- Never allocate `numLeds * 3` without checking whether the strip is RGBW.
- When a user reports flicker, ask whether it started when Wi-Fi was enabled.
  That single question separates a power problem from a timing problem.

## Reference

[`reference/timing-and-power.md`](reference/timing-and-power.md) - Protocol, bit timing, current per LED and the refresh budget table.

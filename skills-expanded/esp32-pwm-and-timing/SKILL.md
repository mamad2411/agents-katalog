---
name: esp32-pwm-and-timing
description: Use when driving an LED, a motor, a servo or a buzzer with PWM on ESP32 - the frequency is wrong, the resolution collapses, the servo jitters, or the duty value does nothing. Covers LEDC's frequency/resolution trade-off.
license: MIT
---

# PWM and timing on ESP32

The ESP32 does not have "PWM pins". It has the LEDC peripheral: 4 timers and 16
channels, and every channel borrows a timer. The frequency and the resolution
are not independent, and that is the source of most surprises.

## The trade-off, in one line

```
frequency = 80 MHz / (divider × 2^resolution)
```

So at a fixed clock, resolution and frequency trade against each other:

| Resolution | Steps | Highest frequency |
|---|---|---|
| 8 bit | 256 | ~312 kHz |
| 10 bit | 1024 | ~78 kHz |
| 12 bit | 4096 | ~19.5 kHz |
| 16 bit | 65536 | ~1.2 kHz |

Ask for 16-bit resolution at 5 kHz and the driver cannot deliver it: it silently
lowers the resolution or the frequency, and the duty value you compute no longer
maps to the brightness you expected.

**Rule of thumb:** pick the frequency the load needs, then take the highest
resolution that still allows it.

## What different loads need

| Load | Frequency | Why |
|---|---|---|
| LED brightness | 1-5 kHz | above the flicker the eye sees when moving |
| RGB LED strip (WS2812) | not PWM | these are driven by a data protocol, not LEDC |
| Servo | 50 Hz | the pulse width, not the frequency, is the signal |
| DC motor | 20-25 kHz | above hearing, and smoother at low duty |
| Buzzer (passive) | the note frequency | 440 Hz for A4, and duty should be 50% |

A servo at 1 kHz will not work. A motor at 50 Hz will whine audibly.

## Duty is a count, not a percentage

The duty argument is `0 .. 2^resolution - 1`, not `0..100`:

```cpp
const int res = 10;                  // 1024 steps
const int maxDuty = (1 << res) - 1;  // 1023
ledcWrite(channel, (percent * maxDuty) / 100);
```

Writing `ledcWrite(channel, 100)` on a 10-bit channel is 10% brightness, not
100%. This is the single most common "the LED is dim and won't go brighter" bug.

## API changed in Arduino core 3.x

```cpp
// core 2.x
ledcSetup(channel, freq, resolution);
ledcAttachPin(pin, channel);

// core 3.x
ledcAttach(pin, freq, resolution);
ledcWrite(pin, duty);          // the pin, not the channel
```

Code written for one does not compile on the other. When a sketch "worked
yesterday", check which core version is installed before rewriting the logic.

## Servos

A servo wants a 1-2 ms pulse every 20 ms. With LEDC:

- frequency 50 Hz, resolution 16 bit (the divider works out),
- duty for 1 ms = `65536 × 1 ms / 20 ms ≈ 3277`,
- duty for 2 ms ≈ 6554.

If the servo jitters, the cause is usually the power supply, not the timing: a
servo draws a current spike at every move that will brown out a shared 5 V rail.

## Rules for the agent

- Always compute the duty from the resolution in use. Never hardcode a duty
  number without showing the resolution it assumes.
- State the frequency and the resolution in the code, next to the call, with the
  reason. "PWM at 5 kHz, 10 bit, so the motor does not whine" is a comment worth
  writing.
- If the user says the output is dim or does not change, check the resolution
  and the duty range before touching the wiring.
- Never drive a WS2812 with LEDC. It needs a 800 kHz data protocol, not a PWM
  duty cycle.

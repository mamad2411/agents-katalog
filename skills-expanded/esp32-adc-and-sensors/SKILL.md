---
name: esp32-adc-and-sensors
description: Use when reading an analog sensor on an ESP32 - the reading is noisy, saturates, drifts, or returns nonsense once Wi-Fi connects. Covers ADC1 vs ADC2, attenuation, calibration, source impedance and averaging.
license: MIT
---

# Reading analog sensors on ESP32

The ESP32 ADC is the weakest peripheral on the chip. It is usable, but only if
you know which pin you are on and what the input looks like.

## Pin choice decides everything

- **ADC1** is `GPIO32`-`GPIO39`. It keeps working while Wi-Fi is active.
- **ADC2** is `GPIO0`, `2`, `4`, `12`-`15`, `25`-`27`. It is **unavailable
  while Wi-Fi is on**: `analogRead` returns 0 or garbage. This is not a bug and
  there is no workaround.
- `GPIO34`-`GPIO39` are input-only, which is fine for an analog input, but they
  have no internal pull-up. A floating input reads noise, not zero.

If the sketch reads an analog sensor and also joins a network, the sensor must
be on ADC1. Anything else is a design error, not a tuning problem.

## Attenuation sets the range

The ADC measures 0-1.1 V at 0 dB attenuation. To read a 3.3 V sensor you need
attenuation, and the top of that range is not linear:

| Setting | Rough input range | Notes |
|---|---|---|
| `ADC_0db` | 0 - 1.1 V | most linear |
| `ADC_2_5db` | 0 - 1.5 V | |
| `ADC_6db` | 0 - 2.2 V | |
| `ADC_11db` | 0 - 3.1 V | the top ~0.4 V is noticeably compressed |

A sensor that reads "always about 3.2 V" at `11db` may simply be above the
linear region. Scale the divider so the signal lands in the middle of the range
rather than at the top.

## Calibration

Raw `analogRead` values vary between chips because of the internal reference.
The Arduino core exposes `analogReadMilliVolts(pin)`, which applies the eFuse
calibration values for your specific chip. Use it:

```cpp
int raw = analogRead(PIN);                     // 0..4095
int mv  = analogReadMilliVolts(PIN);           // calibrated, in mV
```

`mv` is the number to put in the datasheet formula. `raw` is only useful for
comparisons against other readings on the same chip.

## Source impedance

The sample-and-hold capacitor needs the source to be stiff. A divider made of
two 100 kΩ resistors reads low and drifts, because the ADC loads it during the
sample window.

- Keep the divider under about 10 kΩ total.
- Add 100 nF from the ADC pin to ground: it supplies the sample charge and
  removes most of the noise.
- Long wires pick up noise; the capacitor is not optional there.

## Averaging, honestly

The ADC is noisy by design. Averaging N samples improves the reading by roughly
`sqrt(N)`:

```cpp
int readAverage(uint8_t pin, int samples = 16) {
  int32_t total = 0;
  for (int i = 0; i < samples; i++) total += analogReadMilliVolts(pin);
  return total / samples;
}
```

Do not average across a change you care about: 16 samples at full speed is fast,
but 16 samples with a delay between them will smear a step response.

## Rules for the agent

- Before writing analog code, check the pin against the ADC1 list. If it is on
  ADC2 and the sketch uses Wi-Fi, say so and move the sensor.
- Use `analogReadMilliVolts` when the value feeds a formula. `analogRead` alone
  is not a voltage.
- Never "fix" a noisy reading by raising the resolution. The noise is in the
  analog front end; averaging and a capacitor are the fixes.

---
name: esp32-ads1256-precision-adc
description: Use when a measurement needs more than 16 bits - strain, load cells, precision current shunts or thermocouples - and an ADS1256 is on SPI. Covers the reference, the crystal, the DRDY line and the noise budget.
license: MIT
---

# ADS1256 on ESP32

24 bits of resolution is only useful if the reference, the clock and the layout
are as good as the converter. Most ADS1256 designs deliver 16 to 18 effective
bits because one of those three is wrong.

## The three things that decide the result

1. **Reference.** The internal reference is not precision. Use an external
   reference (REF5025, ADR4525) with its own decoupling, and remember the input
   range is +/-VREF/PGA. A noisy reference appears directly in the reading.
2. **Clock.** The part wants 7.68 MHz for its nominal data rates. A wrong crystal
   changes every rate and the digital filter response; the chip still talks, which
   is what makes it confusing.
3. **Layout.** Analog inputs, reference and the crystal are all sensitive. A
   ground plane under the analog section, star-connected to the digital ground,
   is the difference between 20 and 23 bits.

## SPI and DRDY

- SPI mode 1, up to 2 MHz for register access.
- `DRDY` goes low when a conversion is ready and is the only reliable timing
  signal. Polling a status register instead adds jitter and misses samples.
- `SYNC`/`PDWN` must be sequenced at power-up: reset, then self-calibration, then
  configure. Skipping the calibration costs offset error that no software fixes.

## Noise budget, in order

| Source | Effect |
|---|---|
| reference noise | direct, multiplied by gain |
| input wiring pickup | dominant above 10 cm unshielded |
| PGA setting | higher gain, lower range, better resolution |
| data rate | slower is quieter, by the datasheet noise table |
| thermocouple effects | two dissimilar metals at the connector |

## When 24 bits is wasted

If the sensor is a 1 % resistor divider or a thermistor with 2 % tolerance, the
extra bits measure the tolerance, not the temperature. Match the converter to
the sensor before paying for it.

## Symptom table

| Symptom | Usually |
|---|---|
| readings drift with temperature | reference, not the ADC |
| constant offset | self-calibration skipped after reset |
| noise 10x the datasheet | wiring, no shield, digital ground shared |
| `DRDY` never falls | clock missing, reset sequence, SPI mode |
| 24 bits of noise | PGA too low, reference too noisy |

## Agent rules

- Name the reference part and its tolerance; "internal reference" is not an answer
  for a 24-bit design.
- Specify the data rate and the resulting noise, not just the resolution.
- State the calibration sequence explicitly in the bring-up steps.

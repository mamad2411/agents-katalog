---
name: esp32-ads1115-external-adc
description: Use when the ESP32's own ADC is not good enough - 12 bits of noise, ADC2 dead under Wi-Fi, or a sensor 5 m away. Covers ADS1115 wiring, PGA, single-ended vs differential and the input range trap.
license: MIT
---

# ADS1115 on ESP32

The ADS1115 is a 16-bit, 4-channel delta-sigma ADC on I2C. It solves the two
things the ESP32's ADC cannot: it is not blocked by Wi-Fi, and it has a real
programmable gain amplifier.

## The input range trap

The PGA sets the full-scale range: +/-6.144, +/-4.096, +/-2.048, +/-1.024,
+/-0.512, +/-0.256 V. **The input must stay inside GND to VDD regardless of the
PGA setting.** A sensor that swings to 5 V destroys the part even on the 6.144 V
range, because that range describes the differential span, not the absolute
input limit. This is the most common way an ADS1115 dies.

## Wiring

- Address 0x48 to 0x4B by the ADDR pin: GND, VDD, SDA, SCL.
- 2.0 to 5.5 V supply; the I2C lines are pulled to the ESP32's 3.3 V, which is
  fine for the ADS1115 at 3.3 V supply.
- `ALERT/RDY` is open-drain and needs a pull-up. Without it you poll, and at
  860 SPS polling wastes the bus.

## Single-ended vs differential

Single-ended measures each input against GND and uses half the range. Differential
measures AIN0-AIN1 and rejects common-mode noise, which is what you want for a
load cell or a shunt. Choose it deliberately: a differential pair wired as two
single-ended channels reads twice the noise and half the resolution.

## Sample rate and filtering

- 8 to 860 samples per second. Faster means more noise; the datasheet noise table
  is per rate, so pick the rate from the required resolution.
- At 128 SPS with the 0.256 V range, one LSB is 7.8 uV. Below that, the noise
  floor of your wiring dominates.
- Average in the microcontroller only after the rate is chosen; averaging cannot
  fix a wrong PGA.

## Symptom table

| Symptom | Usually |
|---|---|
| all channels read 0x7FFF | input above VDD, part damaged |
| readings jump by hundreds of counts | single-ended pair used where differential was needed |
| device missing on the bus | ADDR strap, pull-ups, 5 V sensor sharing the bus |
| 50/60 Hz hum | no averaging over a mains period, long unshielded leads |
| correct at 0 V, wrong at full scale | PGA range mismatch with the divider |

## Agent rules

- State the PGA range and prove the maximum input stays under VDD.
- Say whether each channel is single-ended or differential, and which pins.
- For a shunt, specify the Kelvin connection; the wire resistance is part of the
  measurement otherwise.

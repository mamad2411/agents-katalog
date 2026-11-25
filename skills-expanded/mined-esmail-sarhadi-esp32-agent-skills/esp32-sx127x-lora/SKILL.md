---
name: esp32-sx127x-lora
description: Use when an ESP32 drives an SX1276 or SX1278 - the chip answers on SPI but never transmits, DIO0 never fires, packets arrive corrupted, or the range is a tenth of what the link budget says. Covers register mode, DIO mapping and RF layout.
license: MIT
---

# SX1276 / SX1278 on ESP32

The SX127x is a register-mapped radio: every operation is a register write plus a
poll or an interrupt. That is the opposite of the SX126x command interface, and
it is why libraries for the two are not interchangeable.

## Before any code

- 3.3 V only, and 120 mA during transmit at +20 dBm. A module fed from the
  ESP32's 3.3 V pin through a wire resets the ESP32 on the first packet.
- The antenna must be connected **before** transmitting. A few seconds into an
  open load is enough to damage the PA.
- Most modules need the DIO0 line wired. Polling the IRQ flags works on a bench
  and loses the TxDone edge as soon as anything else runs on the core.

## The bring-up order that saves an hour

1. Read `RegVersion` (0x42). It should be 0x12. Anything else is SPI, power or
   the reset pulse.
2. Set standby, then `RegOpMode` to LoRa mode. Reading back the mode confirms
   the write landed.
3. Set frequency, spreading factor, bandwidth, coding rate and sync word on
   **both** ends. One mismatched sync word is silence with no error.
4. Map DIO0 to `TxDone` and `RxDone`, then transmit one packet and wait for the
   interrupt with a timeout.

## Settings that must match on both ends

| Parameter | Register | Failure if different |
|---|---|---|
| frequency | `RegFrfMsb/Mid/Lsb` | nothing received, RSSI at noise |
| spreading factor | `ModemConfig2` | garbage, or no packet |
| bandwidth | `ModemConfig1` | same |
| coding rate | `ModemConfig1` | CRC failures |
| sync word | `RegSyncWord` | radio ignores the preamble, no interrupt |
| header mode | `RegModemConfig1` | payload length wrong, CRC error |
| CRC on/off | `RegModemConfig2` | receiver rejects every packet |

## Airtime is a legal limit, not a preference

At SF12/125 kHz a 20 byte payload occupies the channel for 1.32 s. With a 1 %
duty cycle that is one packet every 132 s. `tools/airtime.py` computes it for the
settings you actually chose; run it before promising a reporting interval.

## Symptom table

| Symptom | Usually |
|---|---|
| `RegVersion` not 0x12 | SPI mode/wiring, no reset pulse, 5 V module |
| transmits, nothing received | sync word, frequency or SF mismatch |
| DIO0 never fires | DIO0 not mapped, or the pin is not connected |
| receives only when close | antenna mismatch, no ground plane under the module |
| CRC errors at range | bandwidth too narrow for the crystal tolerance |
| resets on transmit | supply cannot deliver 120 mA |

## Agent rules

- Never mix SX127x register code with SX126x command code; they are different
  chips with different drivers.
- State the exact frequency, SF, BW, CR and sync word for both ends in the plan.
- If the product reports more often than the duty cycle allows, that is a design
  change, not a software setting.

---
name: esp32-rfm69-subghz
description: Use when an ESP32 uses an RFM69 for sub-GHz links - no packets, CRC errors at range, AES-128 that produces garbage, or a module that transmits hot. Covers the FIFO, the sync word and the 433/868/915 variants.
license: MIT
---

# RFM69 on ESP32

The RFM69 is a sub-GHz FSK radio with a 66 byte FIFO, hardware AES-128 and a
packet engine. It is simpler than LoRa and has no spreading factor to tune -
which means the failures are configuration, not radio physics.

## Variant first

| Module | Band | Max power |
|---|---|---|
| RFM69W | 315/433/868/915 | +13 dBm |
| RFM69HW | 315/433/868/915 | +20 dBm |

The HW variant needs `setHighPower(true)` and a different PA configuration. Using
HW settings on a W part transmits hot and out of specification; using W settings
on an HW part gives a link that is 7 dB short and looks like a bad antenna.

## Packet engine settings

- **Sync word** must match on both ends. The default 0x2D/0x01 pair is fine for a
  private link; changing only one end is silence.
- **FIFO threshold**: the chip raises an interrupt at a level you set. If the
  handler reads fewer bytes than the packet contains, the remainder stays in the
  FIFO and the next packet is misaligned.
- **Payload length**: fixed or variable. In variable mode the first byte is the
  length and must match what the transmitter wrote.

## AES-128

`encrypt()` sets a 16 byte key and switches the packet engine to AES. Both ends
need the same key **and** the same `isHighPower`/bitrate configuration, because
the encryption covers the payload only - a CRC or length mismatch still produces
a rejected packet, and a key mismatch produces random-looking payloads that pass
the CRC check. If the data decrypts to garbage but the CRC is good, the key is
wrong, not the radio.

## Antenna and power

- 868/915 MHz modules need a matched antenna; a 433 MHz antenna on an 868 module
  loses most of the power and reflects the rest into the PA.
- The HW part at +20 dBm draws about 130 mA. Same supply rule as every radio: a
  bulk capacitor at the module, not at the regulator.

## Symptom table

| Symptom | Usually |
|---|---|
| nothing received | sync word or bitrate mismatch |
| CRC errors increase with distance | bitrate too high for the deviation |
| payload decrypts to noise, CRC passes | AES key mismatch |
| module gets hot | HW part configured as W, or no antenna |
| every second packet lost | FIFO not drained, threshold misconfigured |
| short range only | wrong band antenna |

## Agent rules

- Name the exact variant (W or HW) in the wiring table; the PA settings differ.
- State sync word, bitrate, deviation, bandwidth and AES key handling.
- Do not reuse LoRa airtime math here: FSK airtime is payload and bitrate only.

---
name: esp32-rs232-rs422
description: Use when integrating RS232 or RS422 transceivers, long serial cables, point-to-point links, full-duplex links or industrial serial equipment.
license: MIT
---

# ESP32 Rs232 Rs422

UART is a logic-level peripheral; RS232 and RS422 are electrical interfaces. A UART pin must never be wired directly to an RS232 voltage or a long differential cable. Select the transceiver and grounding/isolation strategy before writing serial code.

## Choose the physical standard

- RS232 is single-ended, inverted and uses bipolar voltage levels. Use a proper level-shifting transceiver such as a MAX3232-class device.
- RS422 uses differential signaling and is typically point-to-point or one driver to multiple receivers; it is normally full duplex with separate TX and RX pairs.
- RS485 supports multipoint bus operation and direction control; do not confuse its topology with RS422.
- Check transceiver supply, logic voltage, common-mode range, slew rate, ESD rating and connector pinout.

## Wiring and protection

- Cross TX to RX for RS232; verify DB9 pin numbering from the equipment manual, not cable color.
- For RS422, pair TX+/TX- and RX+/RX- as twisted pairs. Confirm polarity from the vendor documentation.
- Evaluate signal reference, shield termination, galvanic isolation and surge exposure for the installation.
- Never connect protective earth, cable shield and signal ground indiscriminately; follow the equipment grounding design.

## UART configuration

- Match baud, data bits, parity and stop bits at both ends.
- Use hardware flow control only when the remote device and transceiver expose the required signals.
- Size RX buffers for worst-case bursts and parse frames incrementally.
- Keep debug logs off the production protocol UART or isolate them on another interface.

## Commissioning checklist

| Check | Evidence |
|---|---|
| Transceiver part and voltage | Schematic + datasheet |
| Cable pair and pinout | Continuity test |
| Idle polarity and signal amplitude | Oscilloscope/differential probe |
| UART framing | Logic analyzer decode |
| Noise margin | Test at installed cable length and load |

## Agent rules

- Identify RS232, RS422 or RS485 explicitly; never use the labels interchangeably.
- Include transceiver wiring and supply in every example.
- Use isolation where ground potential and surge environment require it.
- State cable length and data-rate limits from the chosen transceiver and installation standard.

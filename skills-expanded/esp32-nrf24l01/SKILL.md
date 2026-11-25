---
name: esp32-nrf24l01
description: Use when an nRF24L01 or nRF24L01+ does not respond - the status register reads 0x00, packets never arrive, the link works at 1 m and dies at 10, or the PA/LNA module browns out the board. Covers decoupling, pipes and auto-ack.
license: MIT
---

# nRF24L01 on ESP32

The nRF24L01 is a 2.4 GHz packet radio with a 32 byte payload and hardware
auto-acknowledge. Almost every failure is power, not protocol.

## The 10 uF capacitor is not optional

A PA/LNA module draws about 115 mA in a burst that lasts microseconds. A 3.3 V
rail with a long dupont wire cannot deliver that, and the chip resets mid-packet.
The classic fix is a 10 uF ceramic capacitor soldered directly across the
module's VCC/GND pins, plus a shorter wire. If the status register reads 0x00 or
0xFF, this is the first thing to check - before wiring, before code.

## Pipes and addresses

- Six pipes: pipe 0 has a 5 byte address, pipes 1 to 5 share the upper four bytes
  of pipe 1's address plus their own low byte.
- The **address width must be the same on both ends**, and the receiver's pipe
  address must equal the transmitter's TX address byte for byte. A one-byte
  difference is silence.
- Channel (0 to 125) is a frequency offset from 2400 MHz; both ends must match,
  and Wi-Fi on channel 1 sits right on top of nRF channel 0 to 4.

## Payload and acknowledgement

- 32 bytes maximum. A larger payload is truncated, not rejected.
- `autoAck` + `payload with ack` gives you a return channel per packet; without
  autoAck the transmitter has no idea whether anything arrived.
- `setRetries()` controls the retry count and delay. With zero retries, one lost
  ack looks like a lost packet.

## Coexistence with Wi-Fi

The radio and Wi-Fi share the 2.4 GHz band and the same antenna space. Expect
30 to 50 % packet loss when both run unless the nRF channel is placed away from
the Wi-Fi channel, and even then, time-sharing is the real answer: do not
transmit on both at once.

## Symptom table

| Symptom | Usually |
|---|---|
| status register 0x00 | no power, no capacitor, SPI miswired |
| works at 1 m, not at 10 m | PA/LNA supply sag, antenna inside a box |
| packets lost in bursts | Wi-Fi on the same channel |
| ack never arrives | autoAck off, or addresses differ |
| payload truncated | more than 32 bytes |
| one direction only | TX address on one end does not match RX pipe on the other |

## Agent rules

- Include the capacitor in the bill of materials, not in a footnote.
- State channel, data rate (250 k/1 M/2 M), address width and payload size.
- Never claim a range figure; the number depends on the antenna and the site.

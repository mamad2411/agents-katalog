---
name: esp32-enc28j60-ethernet
description: Use when an ESP32 uses an ENC28J60 for wired Ethernet - no link, DHCP that never completes, a connection that dies under load, or 2 Mbit/s where 100 was expected. Covers its 8 KB buffer, missing auto-negotiation and SPI limits.
license: MIT
---

# ENC28J60 on ESP32

The ENC28J60 is the cheapest way to add Ethernet and the most common source of
"it works until it doesn't". It is a 10/100 MAC+PHY with an 8 KB packet buffer
and no hardware checksum or IP offload.

## What it is not

- **No auto-negotiation.** The link mode is set by registers, not negotiated.
  A module strapped to 10 Mbit half duplex still links with a 100 Mbit switch
  and then drops most frames.
- **No auto-MDIX.** A straight cable to a straight port works; anything else
  needs the right cable.
- **8 KB of shared buffer.** That is the whole RX+TX pool. A 1460 byte MSS with
  a window above ~4 KB overruns it, which is why large TCP transfers stall
  while ping and small requests work.

## Power and clock

The chip draws about 160 mA at 3.3 V with the PHY active, and needs a 25 MHz
crystal (most modules have one). A module fed from the ESP32 board's 3.3 V pin
through a dupont wire browns out during transmits - the symptom is a link that
drops when traffic starts, not at idle.

## SPI

It works at 8 to 10 MHz. 20 MHz is in the datasheet and not on a 10 cm ribbon
cable: the failure mode is a register read that returns 0x00 or 0xFF
intermittently, which then looks like a driver bug. Keep the INT line connected
even if you poll - the driver uses it to avoid missing a receive.

## Bringing it up

1. Reset the chip, then read `EREVID` and confirm it is not 0x00/0xFF.
2. Set the MAC address, then the link mode explicitly (full duplex, 100 Mbit).
3. Read `PHSTAT1`/`PHSTAT2` and log the actual negotiated state.
4. Only then start DHCP, and log the lease.

## Symptom table

| Symptom | Usually |
|---|---|
| `EREVID` reads 0x00 or 0xFF | SPI wiring, 3.3 V rail, missing reset pulse |
| link LED on, no traffic | link mode forced to 10 Mbit half duplex |
| DHCP times out, ping works after static IP | broadcast frames dropped, or the 8 KB buffer |
| large downloads stall | TCP window too big for the buffer |
| dies when the ESP32 transmits Wi-Fi | shared 3.3 V rail, no bulk capacitor |

## When to pick something else

If the product needs sustained throughput, use a W5500 (hardware TCP/IP, 32 KB
per socket) or an RMII PHY. The ENC28J60 is for a 10 kB/minute telemetry node,
not for a web UI.

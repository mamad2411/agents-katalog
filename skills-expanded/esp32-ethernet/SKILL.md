---
name: esp32-ethernet
description: Use when an ESP32 gets a wired connection - the link never comes up, RMII pins conflict with the boot strap, the PHY address is wrong, or the cable works on a laptop and not on the board. Covers LAN8720, W5500 and the clock.
license: MIT
---

# Ethernet on ESP32

Wi-Fi is the default, so Ethernet is where the assumptions are. Three parts have
to agree: the MAC inside the chip, the PHY on the board, and the 50 MHz clock
between them.

## Which ESP32 has a MAC

The classic ESP32 and the ESP32-P4 have an internal Ethernet MAC. The C3, C6 and
S3 do not: they need a W5500 or a LAN8720 plus an external MAC, or no Ethernet at
all. Check this before choosing a part number.

## The clock is the usual failure

RMII needs a 50 MHz reference clock on GPIO0. Most boards take it from the PHY
(XTAL output), some use a dedicated oscillator. Two consequences:

- **GPIO0 is a strapping pin.** It must be high at boot. A PHY that drives the
  clock before the chip samples the strap puts the board into download mode, and
  it looks like a dead board, not an Ethernet problem.
- The PHY must be configured to output the clock, or the external oscillator must
  actually be populated. A missing clock gives a link that never comes up and no
  error message anywhere.

## PHY address

LAN8720 answers on address 0 or 1 depending on the PHYAD0 pin, which is often
strapped by a pull resistor that the reference design and the clone board place
differently. Wrong address means MDIO reads all ones and the driver reports no
PHY. Try both addresses before suspecting the chip.

## W5500 instead

The SPI variant has no RMII, no clock and no PHY address: it is a full MAC+PHY on
SPI. It costs about 30 mA continuously, needs a hardware reset pulse after power
up, and its 80 MHz SPI clock is not reachable on a long dupont wire - 20 to 30 MHz
is what actually works.

## Power and magnetics

Ethernet magnetics and the RJ45 jack with integrated transformers are not
optional. A board wired straight from the PHY to a jack without magnetics may
work on one switch and fail on the next.

## Cable, link and address are three different things

| Symptom | Usually |
|---|---|
| no link LED at all | clock missing, PHY not powered, magnetics |
| link up, no DHCP | cable pair fault, wrong PHY address, driver never started |
| works on the bench, dead in the box | cable strain, magnetics too close to a switching supply |
| link drops under load | 3.3 V rail sagging, PHY decoupling |

Check the link state before debugging IP: `esp_eth` reports link up/down
separately from getting an address.

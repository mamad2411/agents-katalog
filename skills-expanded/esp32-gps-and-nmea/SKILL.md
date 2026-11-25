---
name: esp32-gps-and-nmea
description: Use when an ESP32 reads a GPS module - no sentences arrive, the fix never comes, the time is right but the position is not, or the first fix takes ten minutes. Covers UART settings, NMEA parsing, PPS and cold starts.
license: MIT
---

# GPS on ESP32

A GPS module is a UART that talks whether or not you are listening, at a baud rate
you did not choose. Most problems are electrical or about expectations, not about
parsing.

## The UART

- Default 9600 8N1 on almost every module (NEO-6M, NEO-M8N, ATGM336H). Some
  u-blox parts ship at 38400. If you get nothing, try both before rewiring.
- The module's TX goes to the ESP32 RX. Sounds obvious; it is the most common
  wiring error because both connectors are labelled from their own point of view.
- The ESP32 has three UARTs and UART0 is the console. Use UART1 or UART2, and
  remember UART1's default pins are the flash pins on some boards - pick pins
  explicitly.

## What a fix actually requires

Time to first fix is 30 seconds with a good sky view, and 5 to 15 minutes after a
cold start with no almanac. Indoors it may never fix. Two rules:

- Power the module continuously. Cutting power between reads restarts the almanac
  download every time.
- Give it the backup battery pin if the board has one. That is what keeps the
  almanac and the RTC alive between power cycles.

## Position but no time, or time but no position

A module with 3 satellites can produce a valid time and date while the position
is still invalid. NMEA tells you which is which: `$GPGGA` field 6 is the fix
quality (0 = none), `$GPRMC` field 2 is the status (A = valid, V = void). Parse
the status field and do not use lat/lon when it is V - it will be zeros or the
last known position.

## PPS

The pulse-per-second output is the accurate part: 1 Hz, rising edge, aligned to
UTC within tens of nanoseconds. Use it to discipline the ESP32 clock
(`gpio_isr_handler`) if you need better than the 10 ms you get from parsing a
sentence. It is also the cheapest way to detect that the module is alive but not
fixed.

## Checksum and buffer size

Every sentence ends with `*` and a two-hex-digit XOR checksum. Validate it. A
115200 baud stream at 10 Hz overflows a 256 byte buffer; either drop the baud to
9600, enable only the sentences you need (`$GPGGA`, `$GPRMC`), or read on a
dedicated task with a 1024 byte ring buffer.

| Symptom | Usually |
|---|---|
| no data at all | TX/RX swapped, wrong baud, module not powered |
| garbage characters | baud mismatch, or 5 V module into a 3.3 V pin |
| valid time, zeros for position | no fix yet, status V |
| position jumps by 50 m | no averaging, urban canyon, antenna on the board |
| loses fix when Wi-Fi starts | antenna too close to the radio, or supply sag |

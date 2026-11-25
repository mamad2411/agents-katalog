---
name: esp32-sd-card-and-logging
description: Use when an ESP32 logs to an SD card - the mount fails, the card works on a PC and not on the board, files are corrupt after a power cut, or writes block the rest of the firmware. Covers SPI vs SDMMC, wear and crash-safe logging.
license: MIT
---

# SD cards and logging on ESP32

An SD card is a computer with a slow, unreliable interface. Treat it as one.

## Mount failures are usually electrical

- **SPI mode** works on any pins but is slow (a few hundred kB/s). SDMMC is fast
  and needs dedicated pins (and on the S3, 4-bit mode uses six).
- 3.3 V only, and the card can draw 100 mA during a write burst. A card powered
  from a GPIO or a weak regulator fails at mount or, worse, only on large writes.
- Pull-ups on CMD and DATA are required by the spec; many breakout boards omit
  them.
- Card compatibility is real: some cheap cards do not implement CMD8 correctly
  and fail on the ESP32 while working on a PC. Keep a known-good card for
  bring-up.

## Format matters

- FAT32 for anything you want to read on a PC. exFAT is not supported by the
  IDF's VFS without extra work; ext4 not at all.
- exFAT and cards over 32 GB are a common source of "mount failed".
- Format on the PC, then test mount on the device before blaming the driver.

## A power cut during a write corrupts the file system

Not the file - the FAT. Two protections:

1. `f_sync()` after each logical record, not after each byte. It flushes the FAT
   entry and the data; without it a reset loses the last buffer and can leave a
   cross-linked chain.
2. Append-only logs, one file per boot, with the record length in a header. A
   half-written last record is then detectable and skippable, instead of a file
   that will not open.

## Writing blocks everything

An SD write can stall for 200 ms or more (internal erase). On the same task as
the control loop, that is a missed deadline; on the Wi-Fi task, a disconnect.
Log to a RAM ring buffer and flush from a low-priority task. When the buffer
fills, drop the oldest - losing logs is better than losing control.

## Wear

Cards have no wear levelling you can trust for a 24/7 log. Writing 1 kB every
second is 86 MB a day; a cheap card dies in months. Rotate files, keep a total
size cap, and consider that internal flash (LittleFS) with wear levelling may be
the better choice under 100 MB.

| Symptom | Usually |
|---|---|
| mount fails, card fine on PC | exFAT, missing pull-ups, or 5 V level shifter missing |
| mount fails only with the radio on | supply sag during card init |
| file exists, size 0 | no `f_sync`, reset before flush |
| works until the card fills | no rotation |
| card dies in months | write amplification on a consumer card |
| audio or camera drops frames | SD write on the same task as the DMA feed |

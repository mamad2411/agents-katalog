---
name: esp32-nvs-and-config
description: Use when settings do not survive a reboot - the key is missing after an OTA, a write fails with no space, credentials vanish, or a config change needs migrating. Covers NVS namespaces, wear, encryption and versioning.
license: MIT
---

# NVS: configuration that survives

NVS is a key-value store in a flash partition, not a file system. It is small,
it is wear-levelled, and it fails in ways that a file system does not.

## What it cannot do

- Keys are limited to 15 characters; values to 4000 bytes for a blob, less when
  the partition is small (a blob must fit in about half the free space).
- No transactions across keys. Two writes are two operations; a power cut
  between them leaves the first one applied.
- No ordering guarantee for enumeration. Do not depend on the order of keys.

## The 20 kB default is smaller than it looks

The default `nvs` partition is 24 kB (20 kB usable). Each namespace has an
overhead, and NVS keeps both old and new copies of an entry until a page is
compacted. Writing a 1 kB blob every minute fills it in days and then every
write fails with `ESP_ERR_NVS_NOT_ENOUGH_SPACE` - while reads keep working, so
the firmware looks fine until the first save.

Rule: store settings, not telemetry. Counters and logs belong in a file system or
in RAM with periodic flush.

## Credentials and encryption

NVS is plaintext by default: anyone with `esptool read_flash` gets the Wi-Fi
password. If the device leaves your desk, either enable NVS encryption (which
requires flash encryption and a key partition) or do not store secrets there.

The order matters: flash encryption and the NVS key partition must be created
before the first boot that writes NVS, or you have to erase the partition and
start over.

## After an OTA, NVS survives - the layout may not

An OTA update replaces the app, not NVS. But if the new firmware uses a new
partition table with a different NVS offset, the old data is somewhere else and
reads return `NOT_FOUND`. Treat a config read failure as "first boot" and write
defaults, never as a crash.

## Versioning the schema

Add a `cfg_ver` key. On boot:

1. Read it. Missing means first boot: write defaults, set the version.
2. Older than current: run the migration, then update the version.
3. Newer than the firmware knows: this is a downgrade. Refuse to run, or reset
   to defaults - do not guess.

| Symptom | Usually |
|---|---|
| settings lost after flashing | `esptool erase_flash` erased NVS too |
| write fails, reads fine | partition full, needs `nvs_flash_erase` or a bigger partition |
| credentials readable in a dump | NVS encryption not enabled |
| value is garbage after an OTA | struct layout changed between versions |
| first boot hangs | NVS partition not in the table, `nvs_flash_init` returned an error that was ignored |

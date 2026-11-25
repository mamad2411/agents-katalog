---
name: esp32-storage-and-filesystem
description: Use when choosing or debugging storage on ESP32 - the filesystem will not mount after a power cut, the partition is smaller than the chip, config is lost on reset, or the flash wears out. Covers LittleFS, FAT, SPIFFS and NVS.
license: MIT
---

# Storage on ESP32

There are three storage layers and they solve different problems. Picking the
wrong one is the usual cause of "the settings disappeared".

## Which one

| Need | Use | Why not the others |
|---|---|---|
| A few keys and small values | NVS | a filesystem for 40 bytes of config is a liability |
| Files, logs, assets, a web UI | LittleFS | SPIFFS is deprecated in IDF 5 and not power-loss safe |
| An SD card the user can remove | FAT | the card must be readable on a PC |
| OTA images | the partition table | not a filesystem at all |

## NVS

NVS is a key-value store with its own partition, its own wear levelling and its
own encryption option. Two things to know:

- A write is not durable until it is committed. Losing power between the set and
  the commit loses the value, silently.
- It is small. A few thousand entries at most, and large blobs belong somewhere
  else.

If a stored value is missing after a reboot, check that the namespace string
matches exactly - a typo reads as "not found", not as an error.

## LittleFS versus SPIFFS

SPIFFS does not survive an unexpected power loss well and has been superseded.
LittleFS keeps a journal and is the default for good reason. If a project still
uses SPIFFS, that is a finding worth raising, not a style preference.

Neither one gives you atomic writes at the application level: write to a temporary
file, then rename. A rename is the closest thing to a commit a filesystem offers.

## Sizing

The filesystem is exactly as big as its partition, not as big as the flash. A
4 MB module with a 256 KB `spiffs` partition reports ~200 KB usable after
overhead, and that is correct behaviour, not a bug.

## Wear

Flash sectors tolerate roughly 100k erase cycles. A log written every second to
the same sector will wear it out in weeks. Log to RAM and flush on a schedule, or
rotate across files.

## Mount failure is a decision

`ESP_ERR_NOT_FOUND` or a failed mount on first boot is normal for a blank
partition. Formatting is the right response **once**. Formatting automatically on
every mount failure turns a transient error into data loss - require an explicit
condition, and log which one fired.

## Rules for the agent

- Do not add a filesystem for something NVS can hold.
- Never call `format()` unconditionally in the mount path.
- When a device loses settings on power loss, check the commit and the rename
  before blaming the flash.

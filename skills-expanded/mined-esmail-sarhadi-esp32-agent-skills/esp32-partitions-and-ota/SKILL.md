---
name: esp32-partitions-and-ota
description: Use when enabling OTA, when the build says "Sketch too big", or when a device boot-loops after a partition change. Covers the table layout, the 64 KB alignment rule and what an OTA rollback actually needs.
license: MIT
---

# Partitions and OTA on ESP32

The partition table is the file where a wrong number produces a device that
flashes successfully and then boot-loops with no readable error.

## The fixed part of the map

These addresses are not negotiable:

| Region | Offset |
|---|---|
| Bootloader | `0x1000` |
| Partition table itself | `0x8000` (4 KB) |
| First usable partition | `0x9000` |

Anything below `0x9000` belongs to the bootloader or the table. A partition
placed there overwrites the code that reads the table, and the device stops
booting with no message at all.

## The two rules that break builds

1. **App partitions must start on a 64 KB boundary** (`0x10000`). The MMU maps
   flash pages in 64 KB units; an app at `0x11000` is misaligned and will not
   boot.
2. **An OTA slot must be at least as large as the app binary.** The slot size is
   the hard limit. `pio run -t size` prints the actual binary size; compare it
   against the slot, not against the total flash.

## A 4 MB layout with OTA

```
# Name,     Type, SubType,  Offset,   Size
nvs,        data, nvs,      0x9000,   0x5000,
otadata,    data, ota,      0xe000,   0x2000,
app0,       app,  ota_0,    0x10000,  0x140000,
app1,       app,  ota_1,    0x150000, 0x140000,
spiffs,     data, spiffs,   0x290000, 0x160000,
coredump,   data, coredump, 0x3F0000, 0x10000,
```

`0x10000 + 0x140000 = 0x150000`, so the second slot starts exactly where the
first ends. The two slots are equal by construction, which is what makes
"write the new image while the old one runs" possible.

Verify any layout with:

```bash
python tools/partition_check.py --file partitions.csv --flash 4MB --ota
```

## OTA is more than a second slot

- `otadata` is the 8 KB region where the bootloader stores which slot to boot
  and whether the pending image has been confirmed. Without it there is no
  rollback, only a device that boots a half-written image.
- **A new image must mark itself valid**, otherwise the bootloader rolls back on
  the next reset. In the Arduino core this is `Update.end(true)` plus letting the
  app reach a stable point; in ESP-IDF it is `esp_ota_mark_app_valid_cancel_rollback()`.
  A device that "updates and then reverts" is missing exactly this call.
- The OTA handler needs the flash operations to finish before the device resets.
  Calling `ESP.restart()` inside the update callback truncates the write.

## Rules for the agent

- Never invent offsets. Compute each one as the previous offset plus the
  previous size, and show the arithmetic in a comment.
- When asked to "make room", shrink `spiffs` or `coredump` before touching the
  app slots. Shrinking an app slot below the binary size converts a working
  build into a boot loop.
- If the user reports "Sketch too big", report the binary size, the slot size
  and the difference. Do not silently switch to a different partition scheme
  that removes OTA.

## Reference

[`reference/partition-layouts.md`](reference/partition-layouts.md) - Verified 2/4/8/16 MB layouts, ready to copy and already checked.

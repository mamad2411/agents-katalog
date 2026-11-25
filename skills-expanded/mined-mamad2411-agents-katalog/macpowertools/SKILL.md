---
name: MacPowerTools
description: A unified suite of power user tools for macOS, combining system cleanup and secure Android file transfer.
author: tempguest
version: 1.0.0
license: MIT
---

# MacPowerTools

MacPowerTools combines essential utilities for developers and power users into a single, cohesive skill.

## Features

### System Cleanup
- **Trash**: Empties the Trash.
- **Caches**: Cleans old cache files (older than 7 days) from `~/Library/Caches`.
- **Downloads**: Removes downloads older than 30 days.
- **Safety**: Defaults to `--dry-run` to prevent accidental deletion.

### Secure File Transfer
- **Android Integration**: Push files to Android devices via ADB.
- **Integrity Check**: Verifies SHA256 checksums on both ends.
- **Safety**: Checks for existing files to prevent accidental overwrites.

## Commands

- `cleanup [--force]`: Run the system cleanup. Without `--force`, it performs a dry run.
- `transfer <source_file> [--dest <remote_path>] [--force]`: Securely transfer a file to a connected Android device.

## Usage Examples

```bash
# Clean up system (Dry Run)
cleanup

# Actually delete files
cleanup --force

# Transfer a file to Android
transfer ./release_build.apk --dest /sdcard/Builds/
```

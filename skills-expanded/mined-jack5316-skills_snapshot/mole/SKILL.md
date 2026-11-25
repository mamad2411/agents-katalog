---
name: mole
description: Mole Mac Storage Cleaner - Clean your Mac storage by removing temporary files, caches, logs, and other unnecessary files. Inspired by https://github.com/tw93/Mole. Use when user asks to clean Mac storage, free up disk space, or clean cache/log files.
---

# Mole Mac Storage Cleaner (/mole)

Clean your Mac storage with common cleaning tasks, including caches, logs, Xcode derived data, and more.

## Quick Start

```bash
python3 _scripts/mole_cleaner.py
```

## What It Cleans

1. **User Cache** - Application cache files
2. **User Logs** - Application log files  
3. **System Cache** - System cache files
4. **System Logs** - System log files
5. **Xcode Derived Data** - Xcode build artifacts
6. **Xcode Archives** - Xcode archive files
7. **iOS Device Support** - iOS device support files
8. **iOS Simulator** - iOS simulator data
9. **Trash** - Trash bin
10. **Downloads** - Downloads folder (optional)

## Options

- `--clean`: Perform actual cleaning (default: analyze only)
- `--dry-run`: Preview what would be cleaned without deleting
- `--optional`: Include optional categories (Downloads folder)
- `--save`: Save report to vault

## Examples

```bash
# Analyze storage only (default)
python3 _scripts/mole_cleaner.py

# Preview cleaning without deleting
python3 _scripts/mole_cleaner.py --dry-run

# Clean safe categories
python3 _scripts/mole_cleaner.py --clean

# Clean all including Downloads
python3 _scripts/mole_cleaner.py --clean --optional

# Save report to vault
python3 _scripts/mole_cleaner.py --save
python3 _scripts/mole_cleaner.py --clean --save
```

## Output

- **Terminal**: Markdown report with analysis or cleaning results
- **Saved report**: `Sources/Mole Analysis - YYYY-MM-DD.md` or `Sources/Mole Cleaning - YYYY-MM-DD.md`

## Safety Features

- Default mode is **analyze only** - no files are deleted without explicit `--clean`
- `--dry-run` option to preview changes
- Downloads folder is **optional** and excluded by default
- Permission errors are handled gracefully


---
name: macos-storage-management
category: apple
description: Find large files, inventory disk usage, and manage storage on macOS. Covers NTFS external drive write workarounds (macFUSE-incompatible macOS versions) and systematic disk-space recovery.
---

# macOS Storage Management

Systematic approach to discovering what's consuming disk space on macOS and freeing it up, including workarounds for writing to NTFS drives when macFUSE isn't available.

## Finding Large Files and Directories

### Quick Overview (top-level dirs)
```bash
du -sh ~/.* ~/* 2>/dev/null | sort -rh | head -20
```

### Deep Find (files >500MB)
```bash
find ~ -maxdepth 3 -type f -size +500M 2>/dev/null | head -30
```

### Per-Category Breakdown
```bash
# Home directories
du -sh ~/Downloads ~/Desktop ~/Documents ~/Pictures ~/Movies ~/Music ~/Library 2>/dev/null | sort -rh

# Library subdirectories (app containers, caches)
du -sh ~/Library/* 2>/dev/null | sort -rh | head -20

# Large installers/archives
find ~ -maxdepth 5 \( -name "*.zip" -o -name "*.dmg" -o -name "*.tar.gz" -o -name "*.pkg" \) 2>/dev/null | \
  while read f; do
    s=$(stat -f%z "$f" 2>/dev/null)
    [ "$s" -gt 500000000 ] && ls -lh "$f"
  done 2>/dev/null | sort -k5 -rh
```

### Disk Info
```bash
df -h /
diskutil list
```

## NTFS External Drive: Write Workaround (macOS 27+)

### Problem
- **macFUSE** is incompatible with macOS 27 (pre-release) — installer reports "not compatible with this version of macOS"
- **`mount_ntfs`** (`/Library/Filesystems/ntfs.fs/Contents/Resources/mount_ntfs`) is absent on macOS 27
- Native macOS NTFS write is disabled by default with no working helper binary

### Solution: Finder via AppleScript (no extra tools)
Use `osascript` to tell Finder to copy files to the NTFS volume. Finder on macOS has its own NTFS write path that works even when the kernel-level mount fails.

```bash
osascript -e '
set srcFolder to POSIX file "/path/to/source/"
set destFolder to POSIX file "/Volumes/SSD/DestinationFolder/"
tell application "Finder"
  if not (exists destFolder) then
    make new folder at (POSIX file "/Volumes/SSD") with properties {name:"DestinationFolder"}
  end if
  duplicate every file of folder srcFolder to destFolder
end tell
return "Copied successfully"
on error errMsg
return "Error: " & errMsg
end try
'
```

**Limitations:** Performance may be slower than kernel-level copy; no progress feedback during copy.

### Verification After Copy
```bash
# Compare sizes
ls -lh /path/to/source/*.mov
ls -lh /Volumes/SSD/Destination/*.mov

# Or check byte counts match
stat -f%z /path/to/source/file.mov
stat -f%z /Volumes/SSD/Destination/file.mov
```

## Sudo via GUI (for terminal environments without interactive sudo)

When running in a CLI-only environment (no PTY), macOS commands requiring root can still be run by popping a GUI authentication dialog:

```bash
osascript -e 'do shell script "your-command-here" with administrator privileges'
```

Works for: `diskutil unmount`, `installer -pkg`, `mkdir` + `mount`, etc.

## Pitfalls

- **macFUSE + macOS 27+**: Do NOT attempt brew-based install — it will fail and purge the cask payload. Download from GitHub releases directly if needed, but even then the package may refuse to install.
- **NTFS via Finder**: Works for copy operations. Cannot use this for symbolic links, extended attributes, or preserve all Unix permissions. Ensure source files don't have restrictive permissions (`chmod` before copy if needed).
- **`du` timeout on large dirs**: Running `du -sh ~/*` on a full home directory with deep caches (node_modules, Docker) can time out. Target specific subdirectories instead.
- **Verify file integrity**: After copy to NTFS, always stat byte counts on source and dest to confirm complete transfer — NTFS write via Finder may silently fail on very large files in edge cases.

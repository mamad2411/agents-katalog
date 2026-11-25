---
name: binwalk
description: >
  Build, extend, and operate Binwalk — a fast, easy-to-use tool for analyzing,
  reverse engineering, and extracting firmware images. Use when the user asks about
  firmware analysis, embedded file extraction, entropy analysis, IoT security research,
  or hardware hacking. Covers installation, signature scanning, file extraction,
  recursive extraction, entropy analysis, custom magic signatures, supported formats
  (squashfs, cramfs, jffs2, LZMA, gzip, and more), firmware modification workflow,
  filesystem extraction, and firmware version diffing.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/ReFirmLabs/binwalk
---

# binwalk Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to analyze, extract, or reverse engineer firmware images
- Working on IoT security assessments or hardware hacking engagements
- The user asks about identifying embedded file systems, compressed data, or executables in binary blobs
- Performing entropy analysis to identify encrypted or compressed regions
- Comparing firmware versions to identify changes or patches
- Building custom magic signatures for proprietary formats

## What Binwalk Does

Binwalk is a firmware analysis tool designed to search binary images for embedded files and
executable code. It uses a library of magic byte signatures to identify file types within a
binary, then optionally extracts them to disk. Binwalk is the de facto standard for IoT
firmware reverse engineering, capable of handling everything from raw flash dumps to
vendor-supplied update packages. It supports entropy analysis to highlight encrypted regions,
recursive extraction to unpack nested archives, and side-by-side firmware diffing.

## Installation

```bash
# Kali Linux / Debian / Ubuntu
sudo apt install binwalk -y

# pip (Python 3)
pip3 install binwalk

# From source (recommended for latest features)
git clone https://github.com/ReFirmLabs/binwalk.git
cd binwalk
sudo python3 setup.py install

# Dependencies for full extraction support
sudo apt install squashfs-tools cramfsck jefferson sasquatch \
  mtd-utils gzip bzip2 tar arj lhasa p7zip p7zip-full cabextract \
  sleuthkit default-jdk lzop cpio openjdk-11-jdk -y

# sasquatch (non-standard SquashFS support — critical for many routers)
git clone https://github.com/devttys0/sasquatch
cd sasquatch && ./build.sh
```

## Core Concepts

### Signature Scanning

Binwalk compares bytes at every offset against a database of magic signatures (stored in
`/usr/lib/python3/dist-packages/binwalk/magic/`). A match reports the offset, hex offset,
and description of the identified file type.

### Extraction

When `-e` is used, binwalk calls external tools (7z, tar, dd, jefferson, unsquashfs, etc.)
mapped to each signature type to extract content. Extracted files land in `_{firmware}_extracted/`.

### Entropy Analysis

The `-E` flag computes Shannon entropy across the file in sliding windows. High entropy (~1.0)
indicates encryption or compression; low entropy (~0.0) indicates sparse/null data;
mid-range entropy is typical of compressed but not encrypted data.

## CLI Reference

### Basic Scanning

```bash
# Signature scan (default behavior)
binwalk firmware.bin

# Verbose output — show all matches including false positives
binwalk -v firmware.bin

# Scan multiple files
binwalk firmware_v1.bin firmware_v2.bin

# Quiet mode (suppress output, use exit code)
binwalk -q firmware.bin; echo "Exit: $?"
```

### Extraction

```bash
# Extract identified files
binwalk -e firmware.bin
# Output directory: ./_firmware.bin.extracted/

# Specify custom extraction directory
binwalk -e -C /tmp/extracted/ firmware.bin

# Recursive extraction (extract, then extract from extracted files)
binwalk -Me firmware.bin
# -M = matryoshka (recursive), -e = extract

# Extract with dd (raw carve even for unsupported types)
binwalk -e --dd='.*' firmware.bin   # Carve everything

# Extract only specific file types
binwalk -e --dd='squashfs' firmware.bin
```

### Entropy Analysis

```bash
# Entropy graph (requires matplotlib)
binwalk -E firmware.bin

# Save entropy graph to file
binwalk -E -J entropy.png firmware.bin

# Combine with scan
binwalk -eE firmware.bin

# Raw entropy output (no graph, CSV-compatible)
binwalk --entropy firmware.bin
```

### Firmware Diffing

```bash
# Side-by-side hex comparison of two firmware files
binwalk -W firmware_v1.bin firmware_v2.bin

# Diff only regions that differ
binwalk -W --block=512 firmware_v1.bin firmware_v2.bin

# Output diff to file
binwalk -W firmware_v1.bin firmware_v2.bin > diff.txt
```

### Signature and Magic Options

```bash
# List all built-in signatures
binwalk --list-magic

# Use custom magic file
binwalk -m /path/to/custom.magic firmware.bin

# Add to (not replace) built-in signatures
binwalk --magic=/path/to/extra.magic firmware.bin

# Disable default signatures (use only custom)
binwalk --magic=/path/to/custom.magic --no-default-magic firmware.bin
```

### Code/String Scanning

```bash
# Scan for executable code (opcodes)
binwalk -A firmware.bin        # CPU architecture detection

# Scan for strings
binwalk -R "password" firmware.bin          # Raw string search
binwalk -R "admin\x00password" firmware.bin # Hex sequences

# Grep-style regex
binwalk -r "root:.*:[0-9]+:" firmware.bin   # /etc/passwd-like lines
```

### Miscellaneous Options

```bash
# Set scan length (scan only first N bytes)
binwalk -l 1048576 firmware.bin     # First 1 MB

# Set start offset
binwalk -O 0x100000 firmware.bin    # Start at offset 0x100000

# Exclude specific signatures
binwalk --exclude='jpeg' firmware.bin

# Output as CSV
binwalk --csv firmware.bin > scan.csv

# Output as JSON
binwalk firmware.bin --log=scan.json
```

## Supported Formats

| Category | Formats |
|----------|---------|
| Filesystems | SquashFS, CramFS, JFFS2, YAFFS2, ext2/3/4, FAT, romfs, ubifs |
| Compression | gzip, bzip2, lzma, xz, lzop, zlib, lz4 |
| Archives | tar, zip, 7z, arj, lha, cpio, rar |
| Bootloaders | U-Boot, LILO, GRUB, CFE |
| Kernels | Linux kernel (zImage, uImage, bzImage) |
| Executables | ELF (ARM, MIPS, x86, PPC), PE, Java class |
| Certs/Keys | X.509, PEM, RSA private key |
| Misc | OpenWRT TRX, Broadcom CFE, D-Link DLOB |

## Custom Magic Signatures

Binwalk uses a modified libmagic format. Custom signature file example:

```
# custom.magic
0       string   MYRTR   Custom Router Firmware Header
>4      lelong   x       version: %d
>8      lelong   x       payload length: %d bytes

0       string   \x55\xAA\x00\x01   Proprietary bootloader image
>2      leshort  x                   build: %d
```

```bash
# Test custom signatures
binwalk -m custom.magic firmware.bin

# Append to built-ins
binwalk --magic=custom.magic firmware.bin
```

## Common Workflows

### Full IoT Firmware Analysis

```bash
# 1. Initial scan to understand layout
binwalk firmware.bin

# 2. Check entropy for encrypted regions
binwalk -E firmware.bin

# 3. Recursive extract everything
binwalk -Me firmware.bin
cd _firmware.bin.extracted/

# 4. Find and enter root filesystem
ls -la
cd squashfs-root/   # or jffs2-root/, cramfs-root/, etc.

# 5. Hunt for credentials, keys, and configs
grep -r "password" . --include="*.conf" --include="*.cfg" -l
find . -name "*.pem" -o -name "*.key" -o -name "id_rsa"
cat etc/passwd etc/shadow 2>/dev/null

# 6. Check for hardcoded creds in binaries
grep -r "admin\|root\|password\|secret" ./usr/bin/ --binary-files=text

# 7. Identify firmware architecture
binwalk -A firmware.bin | head -5
file _firmware.bin.extracted/squashfs-root/bin/busybox
```

### Firmware Modification (Repack)

```bash
# 1. Extract
binwalk -Me firmware.bin

# 2. Navigate to squashfs root and modify
cd _firmware.bin.extracted/squashfs-root/
echo 'toor::0:0:root:/root:/bin/sh' >> etc/passwd  # Example: add backdoor user

# 3. Repack squashfs (match original compression)
mksquashfs squashfs-root/ new_squashfs.bin -comp lzma -b 131072 -no-xattrs

# 4. Rebuild firmware image (dd splice)
# Identify squashfs offset and original size from binwalk scan first
dd if=firmware.bin of=new_firmware.bin bs=1 count=<squashfs_offset>
cat new_squashfs.bin >> new_firmware.bin
# Append tail if firmware has data after squashfs
ORIG_SIZE=$(wc -c < firmware.bin)
SQUASH_OFFSET=<squashfs_offset>
SQUASH_SIZE=<original_squashfs_size>
TAIL_OFFSET=$((SQUASH_OFFSET + SQUASH_SIZE))
dd if=firmware.bin bs=1 skip=$TAIL_OFFSET >> new_firmware.bin

# 5. Fix checksum if required (firmware-specific)
# Many routers use CRC32 in header — patch with Python if needed
```

### JFFS2 Filesystem Extraction

```bash
# jefferson handles JFFS2 (binwalk calls it automatically with -e)
pip3 install jefferson
binwalk -e firmware.bin

# Manual jefferson usage
jefferson jffs2_image.bin -d output_dir/
```

### Comparing Two Firmware Versions

```bash
binwalk -W old_firmware.bin new_firmware.bin | head -100

# Script to extract both and diff
binwalk -Me old_firmware.bin -C /tmp/old/
binwalk -Me new_firmware.bin -C /tmp/new/
diff -rq /tmp/old/ /tmp/new/ --exclude="*.pyc"
```

## Advanced Techniques

### Scripting with Binwalk's Python API

```python
import binwalk

# Programmatic scan
for module in binwalk.scan('firmware.bin', signature=True, quiet=True):
    for result in module.results:
        print(f"0x{result.offset:08X}  {result.description}")

# Extraction via API
for module in binwalk.scan('firmware.bin', signature=True, extract=True,
                            matryoshka=True, quiet=True):
    pass  # Extraction happens as a side effect
```

### Entropy-Guided Investigation

```python
import binwalk

# Find encrypted/compressed regions programmatically
for module in binwalk.scan('firmware.bin', entropy=True, quiet=True):
    for result in module.results:
        if result.entropy > 0.9:
            print(f"High entropy at 0x{result.offset:08X}: {result.entropy:.4f}")
```

### Handling Non-Standard SquashFS (Router Firmware)

Many consumer routers use modified SquashFS with non-standard block sizes or endianness.
Use `sasquatch` (auto-invoked by binwalk if installed) or `firmware-mod-kit`:

```bash
# firmware-mod-kit (handles many vendor variants)
git clone https://github.com/rampageX/firmware-mod-kit
cd firmware-mod-kit
./extract-firmware.sh firmware.bin
```

## Integration with Other Tools

| Tool | Use Case |
|------|----------|
| Ghidra / IDA Pro | Decompile extracted ELF/ARM binaries from firmware |
| firmwalker | Automated security scan of extracted filesystem |
| Emba | Comprehensive embedded Linux security analysis |
| QEMU | Emulate extracted firmware for dynamic analysis |
| strings | Quick string extraction from binary blobs |
| file | Identify file types for manual extraction |

```bash
# Quick firmwalker scan after extraction
git clone https://github.com/craigz28/firmwalker
sudo ./firmwalker.sh /tmp/_firmware.bin.extracted/squashfs-root/
```

## Troubleshooting

**Squashfs extraction fails:**
```bash
# Install sasquatch for non-standard variants
git clone https://github.com/devttys0/sasquatch && cd sasquatch && ./build.sh
# Verify with:
which sasquatch
```

**`-Me` produces no filesystem:**
- Check entropy — if entire file is high entropy, it may be encrypted
- Look for the decryption key in a bootloader region or a companion file
- Try `binwalk --dd='.*' firmware.bin` to carve raw data

**Binwalk misses embedded content:**
- The file may use a proprietary header — add a custom magic signature
- Try `binwalk -v` to see all candidate matches including low-confidence hits

**Python API import errors:**
```bash
pip3 install --upgrade binwalk
# Or ensure you're running in the correct Python environment
python3 -c "import binwalk; print(binwalk.__version__)"
```

**Repack checksum mismatch on router:**
- Dump the router's UART boot log to identify CRC algorithm
- Use `binwalk -Y` to detect cryptographic hash functions in the bootloader binary
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)

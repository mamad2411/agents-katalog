---
name: forensics-tools
description: >
  Digital forensics tools for file carving, steganography detection, PCAP analysis,
  and entropy scanning in CTF challenges.
  Trigger: When analyzing files, steganography, PCAP traffic, or hidden data.
license: MIT
metadata:
  author: ctf-arsenal
  version: "1.0"
  category: forensics
---

# forensics tools

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- Analyzing suspicious files or unknown file formats
- Extracting hidden data or carved files
- Detecting steganography in images/audio
- Analyzing network PCAP files
- Scanning for high-entropy (encrypted/compressed) data
- Working with file signatures and magic bytes
- `file_analysis/binwalk_extract.sh` - Wrapper for binwalk extraction
- `steganography/steg_quickcheck.py` - Automated steg detection

## Available sections

- Digital Forensics Tools
- When to Use
- File Analysis and Carving
- Binwalk - Extract Embedded Files
- Scan for embedded files
- Extract all found files
- Extract with signature scan
- Scan for specific file types
- Common File Signatures (Magic Bytes)
- Manual File Carving with dd
- Extract bytes from offset to end
- Extract specific byte range

## Bundled resources

- description_cn.txt
- description_en.txt

Open these resources only if the current task needs deeper detail or executable helpers.

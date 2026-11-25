---
name: autopsy
description: >
  Build, extend, and operate Autopsy — the open-source digital forensics platform built on The Sleuth Kit.
  Use when conducting DFIR investigations, analyzing disk images, performing file carving, keyword searching,
  email analysis, or building forensic case files. Use when the user asks about dead-box forensics, memory
  analysis integration, timeline analysis, hash verification, ingest modules, or generating forensic reports.
  Covers installation, case creation, data sources, ingest modules, analysis techniques, and investigation methodology.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/sleuthkit/autopsy
  stars: '3.5k'
---

# autopsy Agent Skill

## When to Use This Skill

Use this skill when:
- Analyzing disk images (E01, raw/dd, AFF, L01) in a forensic investigation
- Performing keyword searches, hash lookups, or email analysis on acquired evidence
- Building a forensic case file with proper chain-of-custody documentation
- Running ingest modules for artifact extraction (browser history, registry, prefetch)
- Generating court-ready forensic reports
- Building timelines of filesystem activity or user behavior
- Integrating Autopsy into an IR (Incident Response) workflow

## What Autopsy Does

Autopsy is a GUI-driven digital forensics platform wrapping The Sleuth Kit (TSK) libraries. It provides case management, automated artifact extraction via pluggable ingest modules, keyword searching, hash database integration, file carving, timeline analysis, and report generation. It supports disk image formats accepted by libewf (E01), raw dd images, VMDK, VHD, and logical file collections. Autopsy is the forensic front-end used by law enforcement worldwide and is directly comparable to commercial tools like FTK and EnCase.

## Installation

### Windows (Primary Platform)

```
# Download installer from https://www.autopsy.com/download/
# Run Autopsy-<version>-64bit.msi
# Requires 64-bit Windows 7+ with 8GB+ RAM (16GB recommended)
# Java JRE is bundled

# Verify after install
C:\Program Files\Autopsy-4.21.0\bin\autopsy64.exe
```

### Linux (Limited GUI support)

```bash
# Install The Sleuth Kit base
sudo apt-get install sleuthkit autopsy

# For full Autopsy GUI (Linux) — requires NetBeans runtime
git clone https://github.com/sleuthkit/autopsy.git
cd autopsy
./linux_macos_install_scripts/install_prereqs_ubuntu.sh
ant dist

# Launch
autopsy &
# Open browser at http://localhost:9999/autopsy
```

### Java Memory Tuning

Autopsy's performance is heavily memory-dependent. Edit `<install_dir>/etc/autopsy.conf`:

```
# Increase heap for large images
default_options="-J-Xms4g -J-Xmx16g -J-XX:+UseG1GC"
```

## Core Concepts

### Case Structure

```
Case Directory/
├── <CaseName>.aut          — Case database (SQLite)
├── ModuleOutput/           — Ingest module artifacts
├── Reports/                — Generated reports
├── Logs/                   — Autopsy runtime logs
└── <image-name>/           — Per-data-source metadata
```

### Evidence Item Types

| Type | Description |
|------|-------------|
| Disk Image | E01, raw/dd, AFF, L01, VMDK, VHD |
| Local Disk | Direct acquisition of attached drive |
| Logical Files/Folder | Directory or file collection (no image) |
| Unallocated Space | Targeted carving of slack/free space |
| XRY XML | Mobile extraction files |

### Hash Verification

All data sources undergo MD5 and SHA-256 hashing at ingestion time. Hashes are logged to the case database and appear in the Data Sources panel. Any modification to the image after hashing is detectable.

## Creating a Case

```
File → New Case
  Case Name: ClientName_Investigation_2026
  Base Directory: D:\Cases\
  Case Type: Single-User (or Multi-User for shared server)

→ Finish → Add Data Source wizard opens automatically
```

### Multi-User Case (Shared Lab)

Multi-user mode requires:
- PostgreSQL server (store at `postgresql://server:5432/autopsy`)
- ActiveMQ message broker
- Shared network storage for case data

Configure at: `Tools → Autopsy Administration → Multi-User Settings`

## Adding Data Sources

```
Add Data Source → Disk Image or VM File
  Browse to: suspect.E01
  Time Zone: UTC (always use UTC for forensic consistency)
  MD5/SHA-256: Optional — auto-calculated if blank

→ Configure ingest modules (see below) → Finish
```

### Supported Image Formats

| Format | Notes |
|--------|-------|
| `.E01` / `.Ex01` | EnCase Expert Witness — most common LE format |
| `.raw` / `.dd` | Raw sector-by-sector image |
| `.001` / `.002` | Split raw image segments |
| `.vmdk` / `.vhd` / `.vhdx` | VM disk images |
| `.aff` / `.aff4` | Advanced Forensic Format |
| `.L01` | Logical evidence file |

## Ingest Modules

Configure at data source add time or via `Run Ingest Modules` on existing source.

### Essential Modules and Configuration

**Hash Lookup**
```
✓ Hash Lookup
  Add hash sets:
  - NSRL (RDS) — flag known-good OS files
  - Custom alert set — flag known-malware hashes
  
  Download NSRL: https://www.nist.gov/itl/ssd/software-quality-group/nsrl-download
  Import: Tools → Options → Hash Database
```

**Keyword Search**
```
✓ Keyword Search
  Built-in lists:
  - Credit card numbers (regex)
  - Email addresses (regex)
  - IP addresses (regex)
  - Phone numbers (regex)
  
  Custom keywords:
  + Add List → "Incident IOCs"
    Add string: malicious-domain.com (exact)
    Add regex: (?i)password\s*[:=]\s*\S+
  
  Indexing: Uses Apache Solr under the hood
  Post-ingest search: Keyword Search toolbar (top right)
```

**Recent Activity**
```
✓ Recent Activity
  Extracts:
  - Browser history (Chrome, Firefox, IE/Edge, Safari)
  - Browser cookies and downloads
  - Installed programs
  - USB device history (setupapi.log)
  - Windows user accounts and last login
  - Network interfaces and shares
```

**Email Parser**
```
✓ Email Parser (EML, MBOX, PST/OST via MAPI bridge)
  Artifacts → Emails → filter by sender/recipient/subject
  Attachments are extracted and available for hash lookup
```

**Interesting Files Identifier**
```
✓ Interesting Files Identifier
  Categories:
  - Executables not in NSRL (potential malware)
  - Archive files (ZIP, RAR, 7z)
  - Encrypted files
  - Script files (PS1, VBS, BAT)
  
  Custom rules: Tools → Options → Interesting Files
```

**Encryption Detection**
```
✓ Encryption Detection
  Identifies high-entropy files that may be encrypted
  Flags VeraCrypt containers, BitLocker artifacts, PGP files
```

**Extension Mismatch Detector**
```
✓ Extension Mismatch Detector
  Flags files where extension does not match file signature (magic bytes)
  Common attacker TTP: rename .exe to .jpg
```

**Android Analyzer / iOS Analyzer**
```
✓ Used with XRY XML logical extractions from mobile devices
  Extracts SMS, call logs, contacts, app data
```

**Plaso/Log2Timeline Integration**

```bash
# Run log2timeline externally
log2timeline.py --storage-file output.plaso suspect.E01
psort.py -o l2tcsv output.plaso > timeline.csv

# Import CSV timeline into Autopsy via:
# Tools → Timeline → Import...
```

## File Analysis Techniques

### Navigating the File Tree

```
Data Sources
└── suspect.E01
    ├── vol1 (NTFS, C:)
    │   ├── $OrphanFiles     — Deleted files with no parent
    │   ├── $Unalloc         — Unallocated clusters
    │   ├── Users/
    │   └── Windows/
    └── vol2 (NTFS, D:)
```

**View modes:**
- `Views → File Types` — Group by MIME type
- `Views → Deleted Files` — Show only deleted/unlinked inodes
- `Views → File Size` — Sort by size (find large archives)
- `Results → Extracted Content` — All ingest module artifacts

### Examining a File

1. Click file → `Hex` tab: raw sector view
2. `Text` tab: string extraction
3. `Application` tab: rendered view (images, HTML, PDF)
4. `File Metadata` tab: MAC times (Modified, Accessed, Created), inode
5. `Results` tab: which ingest modules flagged this file

### NTFS-Specific Artifacts

```
$MFT              — Master File Table (all file records)
$LogFile          — NTFS journal (recent file system changes)
$UsnJrnl          — USN Change Journal (longer history)
$Recycle.Bin      — Deleted items with original path in $I files
INDX Buffers      — Slack space in directory index (deleted filenames)
```

Access via: `File System Details → Volume → $MFT`

## Timeline Analysis

```
Tools → Timeline (or Ctrl+T)

Visualizations:
- Counts View: histogram of events per time period
- Details View: event list sortable by MAC time
- List View: flat event log

Filters:
- Event Type: File System / Web Activity / Log Entry / Registry
- Date Range: Narrow to incident window
- Data Sources: Filter to single volume
- Event Description: Text search within events

Export: File → Export Filtered Events → CSV
```

### Building a Useful Timeline

1. Set time range ± 7 days around the incident time
2. Filter to `File System` events in key directories: `Users\`, `Temp\`, `Downloads\`
3. Add `Web Activity` events to correlate downloads with file creation
4. Export to CSV and load into timeline tools: Timeline Explorer (EZ Tools), Timesketch

## Keyword Search

```
# Post-ingest keyword search
Keyword Search toolbar → enter term → Exact Match / Substring / Regex

# Regex examples for common IOCs
Regex: \b(?:\d{1,3}\.){3}\d{1,3}\b              # IPv4
Regex: [A-Fa-f0-9]{64}                           # SHA-256 hash
Regex: (?i)(malware|payload|dropper|c2|beacon)
Regex: HKEY_[A-Z_]+\\[^\n]{10,}                  # Registry keys

# Results appear in Keyword Hits → expand by keyword → click hit → file highlighted
```

## Hash Database

```
# Import custom hash set
Tools → Options → Hash Database → Add Hash Database
  Type: Alert (for malware) or Interesting
  Path: malware_hashes.kdb (hashkeeper format) or .idx (MD5SUM format)

# Create hash set from command line (md5sum format)
md5sum /path/to/samples/* > custom-malware.txt
sha256sum /path/to/samples/* >> custom-malware.txt

# NSRL lookup suppresses known-good files from keyword hits
```

## Tagging and Bookmarking

```
# Tag a file or artifact
Right-click → Add Tag → choose tag:
  - Follow Up
  - Bookmark
  - Notable Item
  - Custom tag (create via Tools → Options → Tags)

# Tag a specific hex selection
Hex tab → select bytes → right-click → Add Tag

# View all tagged items
Results → Tags → expand category
```

## Reporting

```
Generate Report (top toolbar icon)

Report Types:
- HTML Report       — Full case with thumbnails, linked files
- Excel Report      — Tabular artifact data
- KML Report        — Geolocation data (EXIF coordinates) in Google Earth
- Text Report       — Plain text summary
- Body File         — Mactime-format timeline for external tools
- Stix2 Report      — Threat intelligence structured export

Include sections:
✓ Case Summary
✓ Data Sources
✓ Extracted Content (by module)
✓ Keyword Hits
✓ Tagged Results
✓ Hash Set Hits
```

## Digital Forensics Investigation Methodology

### Phase 1 — Acquisition (pre-Autopsy)

```bash
# Physical disk imaging with FTK Imager or dc3dd
dc3dd if=/dev/sdb of=/evidence/suspect.E01 hash=sha256 log=/evidence/hash.log

# Verify integrity
md5sum /evidence/suspect.E01
```

### Phase 2 — Case Setup

```
New Case → add investigator info → set time zone to UTC
Add data source → enable all relevant ingest modules → wait for completion
```

### Phase 3 — Triage

```
1. Hash Lookup hits → review Alert hash set matches first
2. Interesting Files → executables not in NSRL
3. Recent Activity → browser history, USB devices, installed programs
4. Extension Mismatches → masqueraded files
5. Timeline → anchor events to incident window
```

### Phase 4 — Deep Dive

```
Follow the artifact trail:
  Suspicious EXE found → check $PREFETCH in Recent Activity → check $MFT timestamps →
  keyword search for C2 domains in browser history → email parser for phishing messages
```

### Phase 5 — Reporting

```
Tag all notable items during analysis
Generate HTML report + Body File timeline
Export tagged items list
Package case directory for legal hold
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Ingest modules not completing | Check `Logs/` for Java heap OOM; increase `-Xmx` in `autopsy.conf` |
| Solr search returns nothing | Ensure keyword search module ran; check `ModuleOutput/keywordsearch/` |
| E01 image not opening | Install/update `libewf` on Linux; Windows uses bundled libs |
| PST file not parsed | Email parser requires MAPI; only supported on Windows |
| Timeline very slow | Limit event types; uncheck Log Entry source if not needed |
| Case database corruption | Use `Tools → Case Database Maintenance → Check Integrity` |
| Missing thumbnail generation | Requires ImageIO extensions; verify Java installation |
| Multi-user connection fails | Check PostgreSQL and ActiveMQ are running; verify `autopsy.conf` |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Your Company Just Got Hit with Ransomware: A 48-Hour Survival Playbook for SMBs](https://redhound.us/ransomware-playbook)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)

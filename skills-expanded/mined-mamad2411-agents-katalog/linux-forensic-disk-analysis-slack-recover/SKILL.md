---
name: linux-forensic-disk-analysis-slack-recover
description: "Linux Forensic Disk Analysis Slack Recover."
domain: cybersecurity
---

|
| MFTECmd | Eric Zimmerman MFT and USN Journal parser with CSV output |
| MFTExplorer | Interactive GUI tool for MFT analysis |
| analyzeMFT | Python MFT parser with CSV/JSON output |
| The Sleuth Kit | File system forensics toolkit (fls, icat, blkls, istat) |
| bulk_extractor | Feature extraction from raw data including slack space |
| NTFS Log Tracker | Tool for parsing $LogFile transaction records |
| streams.exe | Sysinternals tool for listing NTFS Alternate Data Streams |
| Plaso | Super-timeline tool parsing MFT and USN Journal |

## Common Scenarios

**Scenario 1: Anti-Forensics Detection via Timestomping**
Compare $STANDARD_INFORMATION timestamps with $FILE_NAME timestamps in MFT entries, flag files where $SI timestamps predate $FN timestamps (impossible in normal operation), identify timestomped files as evidence of deliberate manipulation, correlate with other timeline evidence.

**Scenario 2: Hidden Data in Alternate Data Streams**
Scan for ADS attached to files beyond the standard Zone.Identifier, extract ADS content for analysis, check for hidden executables or documents stored in ADS, correlate ADS creation with user activity timeline, document findings for evidence.

**Scenario 3: Deleted File Reconstruction from MFT**
Parse MFT for inactive (deleted) entries, extract filenames, sizes, and timestamps of deleted files, recover file content using icat if data clusters are not overwritten, build list of deleted evidence files, correlate with USN Journal delete events.

**Scenario 4: File Activity Reconstruction from USN Journal**
Parse the USN Change Journal for the investigation period, identify file creation, modification, rename, and deletion events, reconstruct the sequence of file operations, detect evidence of data staging (create, copy, compress, delete pattern), identify anti-forensic file wiping.

## Output Format

```
File System Artifact Analysis:
  Volume: NTFS (Partition 2, 465 GB)
  Cluster Size: 4096 bytes

  MFT Analysis:
    Total Entries: 456,789
    Active Files: 234,567
    Deleted Entries: 12,345 (8,901 with recoverable metadata)
    Timestomped Files: 23 (SI/FN mismatch detected)

  USN Journal:
    Records Parsed: 2,345,678
    Date Range: 2024-01-01 to 2024-01-20
    File Creations: 45,678
    File Deletions: 23,456
    File Renames: 12,345

  Alternate Data Streams:
    Total ADS Found: 1,234
    Zone.Identifier: 890 (downloaded files)
    Custom/Suspicious ADS: 5 (hidden data detected)

  Slack Space:
    Total Slack: 12.3 GB
    Keyword Hits: 45 (passwords, credit cards)
    Carved Files: 23 from slack space

  Suspicious Findings:
    - 23 files with timestomped timestamps
    - 5 files with hidden ADS containing data
    - USN shows mass deletion on 2024-01-18 (anti-forensics)
    - Slack space contains residual email fragments

  Reports: /cases/case-2024-001/analysis/
```

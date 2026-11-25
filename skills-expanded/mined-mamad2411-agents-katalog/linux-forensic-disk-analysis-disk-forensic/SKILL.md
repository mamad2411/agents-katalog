---
name: linux-forensic-disk-analysis-disk-forensic
description: "Linux Forensic Disk Analysis Disk Forensic."
domain: cybersecurity
---

|
| **Forensic Image** | Bit-for-bit copy of storage media that preserves all data including deleted files and unallocated space |
| **Write Blocker** | Hardware or software device that prevents any modification to evidence media during acquisition |
| **E01 Format** | Expert Witness Format used by EnCase and FTK; supports compression, metadata, and built-in hash verification |
| **File Carving** | Recovery technique that searches unallocated disk space for file headers and footers to reconstruct deleted files |
| **MFT (Master File Table)** | NTFS metadata structure containing entries for every file and directory, including deleted entries |
| **MAC Timestamps** | Modified, Accessed, Created timestamps on files used for timeline reconstruction (NTFS also has Entry Modified) |
| **Prefetch** | Windows artifact recording program execution metadata; contains execution count, timestamps, and loaded DLLs |
| **Unallocated Space** | Disk sectors not assigned to any file; may contain remnants of deleted files recoverable through carving |

## Tools & Systems

- **FTK Imager**: Free forensic imaging tool supporting E01, AFF, and raw formats with built-in hash verification
- **Autopsy**: Open-source digital forensics platform built on The Sleuth Kit for comprehensive disk analysis
- **KAPE (Kroll Artifact Parser and Extractor)**: Triage collection and parsing tool for rapid artifact extraction
- **X-Ways Forensics**: Commercial forensic analysis tool known for speed and efficiency on large datasets
- **Eric Zimmerman's Tools**: Suite of free forensic parsers (PECmd, MFTECmd, EvtxECmd, RegRipper) for Windows artifacts

## Common Scenarios

### Scenario: Employee Data Theft Investigation

**Context**: An employee submitted a resignation and is suspected of copying proprietary files to a USB drive before departing. HR requests a forensic investigation of the employee's workstation.

**Approach**:
1. Image the workstation disk using FTK Imager with a write blocker
2. Parse USB device history from SYSTEM registry to identify connected devices
3. Examine ShellBags and Jump Lists for evidence of file browsing and copying to removable media
4. Parse LNK files in the Recent folder to identify recently accessed documents
5. Analyze browser history for personal cloud storage uploads (Google Drive, Dropbox)
6. Build a timeline correlating USB connections with file access events

**Pitfalls**:
- Failing to image the drive before the IT department reassigns the workstation
- Not checking cloud storage browser history alongside USB evidence
- Overlooking Volume Shadow Copies that may contain earlier versions of deleted files
- Presenting analysis conclusions as fact without supporting evidence documentation

## Output Format

```
DISK FORENSICS INVESTIGATION REPORT
=====================================
Case ID:          INC-2025-1547
Evidence:         EVD-001 (Samsung 870 EVO 500GB SSD)
Examiner:         [Name]
Date of Analysis: 2025-11-16

EVIDENCE INTEGRITY
Source Hash:      SHA-256: a1b2c3d4e5f6...
Image Hash:       SHA-256: a1b2c3d4e5f6... (VERIFIED MATCH)
Write Blocker:    Tableau T35u

PARTITION LAYOUT
Partition 1:  NTFS  100 MB   (System Reserved)
Partition 2:  NTFS  465 GB   (C: - OS and Data)
Partition 3:  NTFS  500 MB   (Recovery)

KEY FINDINGS
1. [Timestamp] - Malware dropper created in %TEMP% (update.exe)
2. [Timestamp] - Scheduled task "WindowsUpdate" created for persistence
3. [Timestamp] - Prefetch shows 14 executions of update.exe
4. [Timestamp] - USB device "Kingston DataTraveler" connected
5. [Timestamp] - 847 files copied to E:\ drive (ShellBag evidence)

RECOVERED ARTIFACTS
- 3 deleted malware samples recovered from unallocated space
- Browser history showing C2 panel access
- Registry evidence of disabled security software

TIMELINE
[Chronological event listing with timestamps and evidence sources]

TOOLS USED
- FTK Imager 4.7.1 (imaging)
- Autopsy 4.21.0 (analysis)
- PECmd 1.5.0 (prefetch parsing)
- MFTECmd 1.2.2 (MFT analysis)
```

---
name: linux-forensic-disk-acquisition-autopsy-analyze
description: "Linux Forensic Disk Acquisition Autopsy Analyze."
domain: cybersecurity
---

|
| Autopsy | Open-source GUI forensic platform for disk image analysis |
| The Sleuth Kit (TSK) | Command-line forensic toolkit underlying Autopsy |
| fls | List files and directories in a disk image including deleted entries |
| icat | Extract file content by inode number from a disk image |
| mactime | Generate timeline from TSK bodyfile format |
| mmls | Display partition layout of a disk image |
| NSRL | NIST hash database for identifying known software files |
| sigfind | Search for file signatures at the sector level |

## Common Scenarios

**Scenario 1: Employee Data Theft Investigation**
Import the employee workstation image, run all ingest modules, search for company-confidential file names and keywords, examine USB connection artifacts in Recent Activity, check for cloud storage client artifacts, review deleted files for evidence of data staging, generate HTML report for legal team.

**Scenario 2: Malware Infection Forensics**
Add the compromised system image, enable Extension Mismatch and Encryption Detection modules, examine the prefetch directory for execution evidence, search for known malware hashes, build timeline around the infection window, extract suspicious executables for further analysis in a sandbox.

**Scenario 3: Child Exploitation Material (CSAM) Investigation**
Import image with PhotoDNA and Project VIC hash sets enabled, run Picture Analyzer module, hash all image files against known-bad databases, tag and categorize matches by severity, generate law enforcement report with chain of custody documentation.

**Scenario 4: Intellectual Property Dispute**
Import multiple employee disk images as separate data sources in one case, perform keyword searches for proprietary terms and project names, compare file hashes between sources, build timeline showing file access and transfer patterns, export evidence for legal review.

## Output Format

```
Autopsy Case Analysis Summary:
  Case:           CASE-2024-001-Workstation
  Image:          evidence.dd (500GB NTFS)
  Partitions:     2 (System Reserved + Primary)
  Total Files:    245,832
  Deleted Files:  12,456 (recoverable: 8,234)

  Ingest Results:
    Hash Matches (Known Bad):  3 files
    Extension Mismatches:      17 files
    Keyword Hits:              234 across 45 files
    Encrypted Files:           5 containers detected
    EXIF Data Extracted:       1,245 images with metadata

  Tagged Evidence:
    Critical:     12 items
    Supporting:   34 items
    Review:       67 items

  Timeline Events:  1,234,567 entries (filtered to incident window: 892)
  Report:          /cases/case-2024-001/reports/autopsy_report.html
```

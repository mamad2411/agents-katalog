---
name: linux-forensic-disk-filecarving-foremost-detect
description: "Linux Forensic Disk Filecarving Foremost Detect."
domain: cybersecurity
---

|
| Foremost | Original header-footer file carving tool developed for US Air Force OSI |
| Scalpel | High-performance file carver with configurable signatures |
| PhotoRec | Signature-based file recovery supporting 300+ formats |
| bulk_extractor | Extracts features (emails, URLs, credit cards) from raw data |
| blkls | Sleuth Kit tool extracting unallocated space from disk images |
| mmls | Partition table display for identifying carving targets |
| ExifTool | Metadata extraction from carved image and document files |
| hashdeep | Recursive hash computation for carved file cataloging |

## Common Scenarios

**Scenario 1: Recovering Deleted Evidence Documents**
Run Foremost targeting doc, pdf, xlsx formats against the unallocated space extracted with blkls, validate carved documents, search content for case-relevant keywords, catalog and hash all recoverable documents, present as evidence.

**Scenario 2: Image Recovery from Formatted Media**
Carve JPEG, PNG, GIF, BMP from a formatted USB drive image, extract EXIF metadata including GPS coordinates and camera information, generate thumbnails for rapid visual review, identify evidence-relevant images, document recovery chain.

**Scenario 3: Email Recovery from Damaged PST**
Use custom foremost.conf with PST and EML signatures, carve email artifacts from damaged Outlook data file, attempt to open carved PST fragments in a viewer, extract individual EML messages, search for relevant communications.

**Scenario 4: Database Recovery for Financial Investigation**
Configure Foremost to carve SQLite databases from unallocated space, recover application databases that were deleted, query recovered databases for financial records, cross-reference with known transaction data, document findings for prosecution.

## Output Format

```
File Carving Summary:
  Tool: Foremost 1.5.7
  Source: evidence.dd (500 GB)
  Target: Unallocated space (234 GB)
  Duration: 1h 45m

  Files Carved:
    jpg:    2,345 files (1.8 GB) - Valid: 2,100 / Invalid: 245
    png:      234 files (456 MB) - Valid: 210 / Invalid: 24
    pdf:      156 files (890 MB) - Valid: 134 / Invalid: 22
    doc:       89 files (234 MB) - Valid: 67 / Invalid: 22
    xls:       45 files (123 MB) - Valid: 38 / Invalid: 7
    zip:       67 files (567 MB) - Valid: 52 / Invalid: 15
    exe:       34 files (234 MB) - Valid: 30 / Invalid: 4
    sqlite:    12 files (89 MB)  - Valid: 10 / Invalid: 2

  Total Files: 2,982 (3.4 GB recovered)
  Evidence-Relevant: 45 files flagged for review
  Audit Log: /cases/case-2024-001/carved/foremost_all/audit.txt
  File Catalog: /cases/case-2024-001/analysis/carved_file_catalog.csv
```

---
name: arch-digital-preservation-oais-bagit
description: "Package and preserve long-term digital records conforming to ISO 14721 (OAIS Reference Model) and RFC 8493 BagIt specifications with cryptographic fixity."
category: archiving
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - archiving
  - digital-preservation
  - oais
  - bagit
  - records-management
  - checksums
---

# Digital Preservation OAIS Standard & BagIt Archival Packaging

## Overview & Core Principles
Package and preserve long-term digital records conforming to ISO 14721 (OAIS Reference Model) and RFC 8493 BagIt specifications with cryptographic fixity.

### OAIS Information Packages & BagIt Layout
1. **OAIS Package Taxonomy**:
   - SIP (Submission Information Package): Raw ingest from content producers.
   - AIP (Archival Information Package): Complete master preservation unit with PREMIS metadata.
   - DIP (Dissemination Information Package): Normalized access copy served to researchers.
2. **RFC 8493 BagIt Structure**:
```
my_preservation_bag/
|-- bagit.txt
|-- bag-info.txt
|-- manifest-sha512.txt
|-- tagmanifest-sha512.txt
`-- data/
    |-- master_scan.tiff
    `-- metadata.xml
```
3. **Cryptographic Fixity Verification**:
   - SHA-512 checksums computed on bitstream ingest and verified on an automated 90-day cron cycle across cold storage vaults.

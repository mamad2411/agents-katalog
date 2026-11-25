---
name: linux-forensic-disk-acquisition-dcfldd-forensic
description: "Linux Forensic Disk Acquisition Dcfldd Forensic."
domain: cybersecurity
---

|
| dd | Standard Unix disk duplication utility for raw imaging |
| dcfldd | DoD Computer Forensics Laboratory enhanced version of dd with hashing |
| dc3dd | Another forensic dd variant from the DoD Cyber Crime Center |
| sha256sum | SHA-256 hash calculation for integrity verification |
| blockdev | Linux command to set block device read-only mode |
| hdparm | Drive identification and parameter reporting |
| smartctl | S.M.A.R.T. data retrieval for drive health and identification |
| lsblk | Block device enumeration and identification |

## Common Scenarios

**Scenario 1: Acquiring a Suspect Laptop Hard Drive**
Connect the drive via a Tableau T35u hardware write-blocker, identify as `/dev/sdb`, use dcfldd with SHA-256 hashing, split into 4GB segments for DVD archival, verify hashes match, document in case notes.

**Scenario 2: Imaging a USB Flash Drive from a Compromised Workstation**
Use software write-blocking with `blockdev --setro`, acquire with dcfldd including MD5 and SHA-256 dual hashing, image is small enough for single file, verify and store on encrypted case drive.

**Scenario 3: Remote Acquisition Over Network**
Use dd piped through netcat or ssh for remote acquisition: `ssh root@remote "dd if=/dev/sda bs=4096" | dd of=remote_image.dd bs=4096`, hash both ends independently to verify transfer integrity.

**Scenario 4: Acquiring from a Failing Drive**
Use `ddrescue` first to recover readable sectors, then use dd with `conv=noerror,sync` to fill gaps with zeros, document which sectors were unreadable in the error log.

## Output Format

```
Acquisition Summary:
  Source:       /dev/sdb (500GB Western Digital WD5000AAKX)
  Destination:  /cases/case-2024-001/images/evidence.dd
  Tool:         dcfldd 1.9.1
  Block Size:   4096 bytes
  Duration:     2h 15m 32s
  Bytes Copied: 500,107,862,016
  Errors:       0 bad sectors
  Source SHA-256:  a3f2b8c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
  Image SHA-256:   a3f2b8c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
  Verification:    PASSED - Hashes match
```

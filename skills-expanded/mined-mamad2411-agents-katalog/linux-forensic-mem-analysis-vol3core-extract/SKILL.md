---
name: linux-forensic-mem-analysis-vol3core-extract
description: "Linux Forensic Mem Analysis Vol3Core Extract."
domain: cybersecurity
---

|
| Volatility 3 | Primary open-source memory forensics framework |
| LiME | Linux Memory Extractor for acquiring Linux RAM dumps |
| WinPmem | Windows physical memory acquisition driver |
| DumpIt | Comae one-click Windows memory dump utility |
| YARA | Pattern matching engine for malware signature scanning |
| Rekall | Alternative memory forensics framework (Google) |
| MemProcFS | Memory process file system for memory analysis |
| strings | Extract printable strings from binary memory dumps |

## Common Scenarios

**Scenario 1: Active Malware Investigation**
Acquire memory with DumpIt, run pslist/pstree to identify suspicious processes, use malfind to detect injected code in svchost.exe, dump the injected memory segment, scan with YARA rules identifying Cobalt Strike beacon, extract C2 IP from netscan, correlate with network logs.

**Scenario 2: Credential Theft After Breach**
Run hashdump and lsadump to extract cached credentials, identify mimikatz execution in cmdline output, check for lsass.exe memory dumps in filesystem artifacts, correlate with lateral movement evidence in network connections.

**Scenario 3: Rootkit Detection**
Compare pslist (uses EPROCESS linked list) with psscan (pool scanning) to find unlinked processes, check modules vs modscan for hidden kernel drivers, examine SSDT for hooks redirecting system calls, dump suspicious modules for static analysis.

**Scenario 4: Ransomware Incident Recovery**
Extract encryption keys from ransomware process memory before system shutdown, identify the ransomware variant using YARA, find the initial execution point through command line artifacts, map lateral movement via network connections.

## Output Format

```
Memory Forensics Analysis:
  Image:            memory.raw (16 GB)
  OS Identified:    Windows 10 x64 Build 19041
  Capture Time:     2024-01-18 14:32:15 UTC

  Process Analysis:
    Total Processes:    87
    Hidden Processes:   2 (PIDs: 4532, 6128)
    Injected Processes: 3 (malfind detections)
    Suspicious:         svchost.exe (PID 4532) - injected code at 0x7FFE0000

  Network Connections:
    Total:        45
    Established:  12
    Suspicious:   3 (C2 connections to 185.xx.xx.xx:443)

  Credentials Found:
    NTLM Hashes:      4 accounts
    Cached Creds:      2 domain accounts

  YARA Matches:
    CobaltStrike_Beacon:  PID 4532 (3 hits)
    Mimikatz_Memory:      PID 6128 (1 hit)

  Extracted Artifacts:   15 files dumped to /analysis/extracted/
```

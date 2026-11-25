---
name: linux-forensic-mem-analysis-volcombined-detect
description: "Found in psscan but not pslist  INJECTED CODE PID    Process        Address Range        Protection              Finding 5102   svchost."
domain: cybersecurity
---

Found in psscan but not pslist

INJECTED CODE
PID    Process        Address Range        Protection              Finding
5102   svchost.exe    0x00A10000-0x00A14   PAGE_EXECUTE_READWRITE  MZ header (PE injection)

NETWORK CONNECTIONS
PID    Process      Local              Foreign             State
3847   update.exe   10.1.5.42:49721    185.220.101.42:443  ESTABLISHED
5102   svchost.exe  10.1.5.42:51003    91.215.85.17:8443   ESTABLISHED

YARA MATCHES
Rule: CobaltStrike_Beacon_x64
Match PID: 5102 (svchost.exe)
Offset: 0x00A10240

EXTRACTED IOCS
Hashes:     [SHA-256 of dumped injected code]
C2 IPs:     185.220.101.42, 91.215.85.17
C2 Domains: [extracted from beacon config]
Mutexes:    Global\MSCTF.Shared.MUTEX.ZRQ
```

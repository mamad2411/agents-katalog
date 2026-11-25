---
name: linux-forensic-mem-injection-detection-detect
description: "Linux Forensic Mem Injection Detection Detect."
domain: cybersecurity
---

|
| **Process Injection** | Technique of executing code within the address space of another process, typically to evade detection and inherit the target's trust level |
| **Process Hollowing** | Creating a legitimate process in suspended state, unmapping its memory, writing malicious code, and resuming execution to masquerade as the legitimate process |
| **Reflective DLL Injection** | Loading a DLL into a process's memory without using the Windows loader, so the DLL does not appear in the loaded module list |
| **APC Injection** | Queuing an Asynchronous Procedure Call to a thread in the target process, causing it to execute injected code when the thread enters an alertable state |
| **VAD (Virtual Address Descriptor)** | Windows kernel structure describing memory regions in a process; anomalous VAD entries (RWX permissions, non-image PE) indicate injection |
| **CreateRemoteThread** | Windows API creating a thread in another process; the primary mechanism for classic DLL injection and many other injection techniques |
| **PAGE_EXECUTE_READWRITE** | Memory protection allowing read, write, and execute; rarely used by legitimate applications, common indicator of injected code |

## Tools & Systems

- **Volatility (malfind)**: Memory forensics plugin detecting injected code through VAD analysis and PE header scanning in non-image memory regions
- **Sysmon**: System Monitor providing detailed Windows event logging including CreateRemoteThread (EID 8) and ProcessAccess (EID 10)
- **Process Hacker**: Advanced process management tool showing detailed memory regions, thread stacks, and injected modules
- **API Monitor**: Windows tool for monitoring and logging API calls made by processes, useful for observing injection sequences in real-time
- **pe-sieve**: Tool scanning running processes for signs of code injection, hooking, and hollowing

## Common Scenarios

### Scenario: Investigating a Hollowed svchost.exe Process

**Context**: EDR alerts on svchost.exe making HTTPS connections to an external IP. Svchost.exe should only communicate with Microsoft services. Memory analysis is needed to confirm process hollowing.

**Approach**:
1. Capture memory dump of the suspicious svchost.exe process
2. Run Volatility `malfind` to detect injected PE in the process memory
3. Compare the in-memory image base with the on-disk svchost.exe file hash
4. Check the process parent (should be services.exe) and creation parameters
5. Dump the hollowed executable from memory and analyze with Ghidra
6. Run `netscan` to confirm the network connections from the hollowed process
7. Scan dumped code with YARA for malware family identification

**Pitfalls**:
- Assuming all svchost.exe instances are identical (each loads different service DLLs)
- Not checking the parent process (hollowed processes often have wrong parents)
- Relying only on process name matching (attackers specifically target svchost.exe because multiple instances are expected)
- Missing the injection source process that may have already terminated

## Output Format

```
PROCESS INJECTION ANALYSIS REPORT
====================================
Dump File:        memory.dmp
Analysis Tool:    Volatility 3.2 + Sysmon

INJECTION DETECTED
Target Process:   svchost.exe (PID: 852)
Source Process:    malware.exe (PID: 2184) [terminated]
Technique:        Process Hollowing (T1055.012)

EVIDENCE
malfind Results:
  PID 852 (svchost.exe):
    Address: 0x00400000
    Size:    184,320 bytes
    Protection: PAGE_EXECUTE_READWRITE
    Header: MZ (PE32 executable)
    NOT backed by disk file

Process Verification:
  Expected Image: C:\Windows\System32\svchost.exe (SHA-256: aaa...)
  In-Memory Image: Unknown PE (SHA-256: bbb...)
  Result: MISMATCH - HOLLOWED PROCESS

Sysmon Events:
  [4688] malware.exe (PID 2184) created svchost.exe (PID 852) SUSPENDED
  [10]   malware.exe accessed svchost.exe with PROCESS_VM_WRITE
  [8]    malware.exe created remote thread in svchost.exe

INJECTED PAYLOAD ANALYSIS
SHA-256:          bbb123def456...
YARA Match:       CobaltStrike_Beacon_x64
Type:             Cobalt Strike Beacon (HTTP)
C2:               hxxps://185.220.101[.]42/updates

MITRE ATT&CK
T1055.012  Process Hollowing
T1071.001  Web Protocols (HTTPS C2)
T1036.005  Match Legitimate Name (svchost.exe)
```

---
name: linux-forensic-mem-injection-process-detect
description: "Linux Forensic Mem Injection Process Detect."
domain: cybersecurity
---

|
| CrowdStrike Falcon | Memory protection and hollowing detection |
| Microsoft Defender for Endpoint | ProcessTampering alerts |
| Sysmon v13+ | Event ID 25 ProcessTampering detection |
| Volatility | Memory forensics - malfind plugin |
| pe-sieve | Process memory scanner for hollowed processes |
| Hollows Hunter | Automated hollowed process detection |
| Process Hacker | Live process memory inspection |
| API Monitor | Monitor NtUnmapViewOfSection calls |

## Common Scenarios

1. **Svchost.exe Hollowing**: Malware creates svchost.exe suspended, hollows it, injects backdoor code - process appears legitimate but behaves maliciously.
2. **Explorer.exe Hollowing**: Attacker hollows explorer.exe to inherit its network permissions and trusted process context.
3. **Rundll32 Hollowing**: Malicious loader creates rundll32.exe, replaces its memory with implant code for C2 beaconing.
4. **Multi-Stage Hollowing**: Loader uses process hollowing as first stage, then performs additional injection into services.

## Output Format

```
Hunt ID: TH-HOLLOW-[DATE]-[SEQ]
Technique: T1055.012
Hollowed Process: [Process name and PID]
Original Binary: [Expected on-disk path]
Parent Process: [Parent name and PID]
Memory Mismatch: [Yes/No]
Suspicious APIs: [NtUnmapViewOfSection, WriteProcessMemory, etc.]
Network Activity: [C2 connections if any]
Host: [Hostname]
User: [Account context]
Risk Level: [Critical/High/Medium/Low]
```

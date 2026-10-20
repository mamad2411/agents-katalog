---
name: linux-forensic-mem-injection-sysmon-detect
description: "Linux Forensic Mem Injection Sysmon Detect."
domain: cybersecurity
---

|
| Sysmon | Primary telemetry source for injection detection |
| Process Hacker | Manual investigation of process memory regions |
| PE-sieve | Scan running processes for hollowed/injected code |
| Moneta | Detect anomalous memory regions in processes |
| Splunk / Elastic | SIEM correlation of Sysmon events |
| Volatility | Memory forensics for injection artifacts |
| Hollows Hunter | Automated scan for hollowed processes |

## Detection Queries

### Splunk -- Remote Thread Creation
```spl
index=sysmon EventCode=8
| where SourceImage!=TargetImage
| where NOT match(SourceImage, "(?i)(csrss|lsass|services|svchost|MsMpEng|SecurityHealthService|vmtoolsd)\.exe$")
| eval suspicious=if(match(TargetImage, "(?i)(svchost|explorer|lsass|winlogon|csrss|services)\.exe$"), "high_value_target", "normal_target")
| where suspicious="high_value_target"
| table _time Computer SourceImage SourceProcessId TargetImage TargetProcessId StartFunction NewThreadId
```

### Splunk -- Suspicious ProcessAccess Patterns
```spl
index=sysmon EventCode=10
| where SourceImage!=TargetImage
| where match(GrantedAccess, "(0x1FFFFF|0x1F3FFF|0x143A|0x0040)")
| where match(TargetImage, "(?i)(lsass|svchost|explorer|winlogon)\.exe$")
| where NOT match(SourceImage, "(?i)(MsMpEng|csrss|services|svchost|taskmgr|procexp)\.exe$")
| table _time Computer SourceImage TargetImage GrantedAccess CallTrace
```

### KQL -- Process Injection via Remote Thread
```kql
DeviceEvents
| where Timestamp > ago(7d)
| where ActionType == "CreateRemoteThreadApiCall"
| where InitiatingProcessFileName !in~ ("csrss.exe", "lsass.exe", "services.exe", "svchost.exe")
| where FileName in~ ("svchost.exe", "explorer.exe", "lsass.exe", "winlogon.exe")
| project Timestamp, DeviceName, InitiatingProcessFileName, InitiatingProcessCommandLine,
    FileName, ProcessCommandLine
```

### Sigma Rule -- Process Injection Detection
```yaml
title: Process Injection via CreateRemoteThread into System Process
status: stable
logsource:
    product: windows
    category: create_remote_thread
detection:
    selection:
        TargetImage|endswith:
            - '\svchost.exe'
            - '\explorer.exe'
            - '\lsass.exe'
            - '\winlogon.exe'
    filter_legitimate:
        SourceImage|endswith:
            - '\csrss.exe'
            - '\lsass.exe'
            - '\services.exe'
            - '\MsMpEng.exe'
    condition: selection and not filter_legitimate
level: high
tags:
    - attack.defense_evasion
    - attack.t1055
```

## Common Scenarios

1. **Classic DLL Injection**: Malware uses VirtualAllocEx + WriteProcessMemory + CreateRemoteThread to load a malicious DLL into a target process. Detected via Sysmon Event 8.
2. **Process Hollowing (RunPE)**: Attacker creates a suspended process, unmaps its image, writes malicious PE, and resumes execution. Detected via Sysmon Event 25.
3. **APC Injection**: Malware queues an Asynchronous Procedure Call to threads of a target process using QueueUserAPC. Harder to detect, requires Event 10 monitoring.
4. **Reflective DLL Injection**: DLL is loaded directly from memory without touching disk, bypassing ImageLoaded detection. Requires memory-level analysis.
5. **Process Doppelganging**: Leverages NTFS transactions to replace a legitimate process image. Detected via process integrity checking.

## Output Format

```
Hunt ID: TH-INJECT-[DATE]-[SEQ]
Host: [Hostname]
Source Process: [Injecting process path]
Source PID: [Process ID]
Target Process: [Target process path]
Target PID: [Process ID]
Injection Type: [DLL/Shellcode/Hollowing/APC]
Sysmon Events: [Event IDs triggered]
Access Mask: [Granted access value]
Risk Level: [Critical/High/Medium/Low]
ATT&CK Sub-Technique: [T1055.xxx]
```

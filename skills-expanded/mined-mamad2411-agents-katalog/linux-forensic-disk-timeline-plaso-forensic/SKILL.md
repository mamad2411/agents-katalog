---
name: linux-forensic-disk-timeline-plaso-forensic
description: "Linux Forensic Disk Timeline Plaso Forensic."
domain: cybersecurity
---

|
| log2timeline (Plaso) | Primary timeline generation engine parsing 100+ artifact types |
| psort | Plaso output filtering, sorting, and export utility |
| Timesketch | Web-based collaborative forensic timeline analysis platform |
| Timeline Explorer | Eric Zimmerman's Windows GUI for CSV timeline analysis |
| KAPE | Automated triage collection feeding into Plaso processing |
| mactime (TSK) | Simpler timeline generation from Sleuth Kit bodyfiles |
| Excel/Sheets | Manual timeline review for small filtered datasets |
| Elastic/Kibana | Alternative visualization platform for JSONL timeline data |

## Common Scenarios

**Scenario 1: Ransomware Attack Reconstruction**
Process the full disk image with Plaso, filter to the week before encryption was discovered, identify the initial access vector from browser history and event logs, trace privilege escalation through registry and Prefetch, map lateral movement from network logon events, pinpoint encryption start from MFT timestamps showing mass file modifications.

**Scenario 2: Data Theft Investigation**
Create super-timeline from suspect's workstation, filter for USB device connection events, file access timestamps, and cloud storage browser activity, build a narrative showing data staging, compression, and exfiltration, present timeline to legal team with tagged evidence points.

**Scenario 3: Multi-System Breach Analysis**
Process disk images from all affected systems into a single Plaso storage file, import into Timesketch for collaborative analysis, search for lateral movement patterns across system timelines, identify the patient-zero system and initial compromise vector, map the full attack chain across the environment.

**Scenario 4: Insider Threat After-Hours Activity**
Filter timeline to non-business hours only, identify file access patterns outside normal working times, correlate with authentication events (badge access, VPN logon), search for data access to sensitive directories during these periods, build evidence package for HR/legal.

## Output Format

```
Timeline Reconstruction Summary:
  Evidence Sources:
    Disk Image: evidence.dd (500 GB, NTFS)
    Plaso Storage: evidence.plaso (2.3 GB)

  Processing Statistics:
    Total events extracted: 4,567,890
    Parsers used: 45 (winevtx, prefetch, mft, usnjrnl, lnk, chrome, firefox, winreg, ...)
    Processing time: 3h 45m

  Incident Window (2024-01-15 to 2024-01-20):
    Events in window: 234,567
    Event Sources:
      MFT:          89,234
      Event Logs:   45,678
      USN Journal:  56,789
      Registry:     23,456
      Prefetch:     1,234
      Browser:      5,678
      LNK Files:    2,345
      Other:        10,153

  Key Timeline Events:
    2024-01-15 14:32 - Phishing email opened (browser)
    2024-01-15 14:33 - Malicious document downloaded
    2024-01-15 14:35 - PowerShell executed (Prefetch + Event Log)
    2024-01-15 14:36 - C2 connection established (Registry + Event Log)
    2024-01-16 02:30 - Mimikatz execution (Prefetch)
    2024-01-16 02:45 - Lateral movement to DC (Event Log)
    2024-01-17 03:00 - Data exfiltration (MFT + USN Journal)
    2024-01-18 03:00 - Log clearing (Event Log)

  Exported Files:
    Full Timeline:     /timeline/full_timeline.csv (4.5M rows)
    Incident Window:   /timeline/incident_window.csv (234K rows)
    Timesketch Import: /timeline/timeline.jsonl
```

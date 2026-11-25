---
name: identity-ad-dcsyncd
description: "| | Mimikatz (lsadump::dcsync) | Primary DCSync attack tool | | Impacket secretsdump."
domain: cybersecurity
---

|
| Mimikatz (lsadump::dcsync) | Primary DCSync attack tool |
| Impacket secretsdump.py | Python-based DCSync implementation |
| DSInternals | PowerShell module for AD replication |
| BloodHound | Map accounts with replication rights |
| Splunk / Elastic | SIEM correlation of 4662 events |
| Microsoft Defender for Identity | Native DCSync detection |
| CrowdStrike Falcon | EDR-based DCSync detection |

## Detection Queries

### Splunk -- DCSync Detection via Event 4662
```spl
index=wineventlog EventCode=4662
| where Properties IN ("*1131f6aa-9c07-11d1-f79f-00c04fc2dcd2*",
    "*1131f6ad-9c07-11d1-f79f-00c04fc2dcd2*",
    "*89e95b76-444d-4c62-991a-0facbeda640c*")
| where NOT match(SubjectUserName, ".*\\$$")
| where NOT SubjectUserName IN ("known_svc_account1", "known_svc_account2")
| stats count values(Properties) as ReplicationRights by SubjectUserName SubjectDomainName Computer
| where count > 0
| table SubjectUserName SubjectDomainName Computer count ReplicationRights
```

### KQL -- Microsoft Sentinel DCSync Detection
```kql
SecurityEvent
| where EventID == 4662
| where Properties has "1131f6ad-9c07-11d1-f79f-00c04fc2dcd2"
    or Properties has "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2"
| where SubjectUserName !endswith "$"
| where SubjectUserName !in ("AzureADConnect", "MSOL_*")
| project TimeGenerated, SubjectUserName, SubjectDomainName, Computer, Properties
| sort by TimeGenerated desc
```

### Sigma Rule -- DCSync Activity
```yaml
title: DCSync Activity Detected - Non-DC Replication Request
status: stable
logsource:
    product: windows
    service: security
detection:
    selection:
        EventID: 4662
        Properties|contains:
            - '1131f6aa-9c07-11d1-f79f-00c04fc2dcd2'
            - '1131f6ad-9c07-11d1-f79f-00c04fc2dcd2'
    filter_dc:
        SubjectUserName|endswith: '$'
    condition: selection and not filter_dc
level: critical
tags:
    - attack.credential_access
    - attack.t1003.006
```

## Common Scenarios

1. **Mimikatz DCSync**: Attacker with Domain Admin privileges runs `lsadump::dcsync /user:krbtgt` to extract KRBTGT hash for Golden Ticket creation.
2. **Impacket secretsdump**: Remote DCSync via `secretsdump.py domain/user:password@dc-ip` extracting all domain hashes.
3. **Delegated Replication Rights**: Attacker grants themselves Replicating Directory Changes rights via ACL modification before performing DCSync.
4. **Azure AD Connect Abuse**: Compromising the Azure AD Connect service account which has legitimate replication rights.
5. **DSInternals PowerShell**: Using `Get-ADReplAccount` cmdlet to replicate specific account credentials.

## Output Format

```
Hunt ID: TH-DCSYNC-[DATE]-[SEQ]
Alert Severity: Critical
Source Account: [Account requesting replication]
Source Machine: [Hostname/IP of requestor]
Target DC: [Domain controller receiving request]
Replication Rights: [GUIDs accessed]
Timestamp: [Event time]
Legitimate DC: [Yes/No]
Known Service Account: [Yes/No]
Risk Assessment: [Critical - non-DC replication detected]
```

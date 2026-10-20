---
name: identity-kerberos-impacket
description: "Identity Kerberos Impacket."
domain: cybersecurity
---

|
| Service accounts in Domain Admins | Direct path to domain compromise | Critical |
| SQL service accounts (MSSQLSvc) | Often have excessive privileges | High |
| Exchange service accounts | Access to all email | High |
| Accounts with AdminCount=1 | Previously/currently privileged | High |
| Accounts with old passwords | More likely to use weak passwords | Medium |

## Detection

### Windows Event Logs

```
Event ID 4769 - Kerberos Service Ticket Request
- Monitor for: Encryption type 0x17 (RC4-HMAC) when AES is expected
- Monitor for: Single user requesting many TGS tickets in short period
- Monitor for: Service ticket requests from unusual source IPs
```

### Sigma Rule

```yaml
title: Potential Kerberoasting Activity
status: stable
logsource:
    product: windows
    service: security
detection:
    selection:
        EventID: 4769
        TicketEncryptionType: '0x17'  # RC4
        ServiceName|endswith: '$'
    filter:
        ServiceName: 'krbtgt'
    condition: selection and not filter
level: medium
tags:
    - attack.credential_access
    - attack.t1558.003
```

## Defensive Recommendations

1. **Use Group Managed Service Accounts (gMSA)** - 240-character random passwords, auto-rotated
2. **Set strong passwords (25+ chars)** on all service accounts
3. **Enable AES-only encryption** - Disable RC4 via GPO
4. **Monitor Event ID 4769** for RC4 TGS requests
5. **Implement Managed Service Accounts** where gMSA is not feasible
6. **Regular audits** - Run BloodHound to identify Kerberoastable accounts
7. **Protected Users group** - Add sensitive service accounts
8. **Honeypot SPNs** - Create decoy accounts with SPNs to detect attacks

## References

- MITRE ATT&CK T1558.003: https://attack.mitre.org/techniques/T1558/003/
- Impacket: https://github.com/fortra/impacket
- Harmj0y's Kerberoasting Revisited: https://posts.specterops.io/kerberoasting-revisited-d434351bd4d1
- Detection Strategy DET0157: https://attack.mitre.org/detectionstrategies/DET0157/

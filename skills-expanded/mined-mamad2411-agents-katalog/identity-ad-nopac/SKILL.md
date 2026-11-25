---
name: identity-ad-nopac
description: "Identity Ad Nopac."
domain: cybersecurity
---

--|
| Machine account sAMAccountName change | Event 4742 (computer account changed) with sAMAccountName modification |
| New machine account creation | Event 4741 (computer object created) |
| TGT request for account without trailing $ | Kerberos audit log analysis |
| S4U2self requests from non-DC machine accounts | Event 4769 with unusual service ticket requests |
| Rapid sequence: create account, rename, request TGT | SIEM correlation rule for noPac attack pattern |

## Validation Criteria

- [ ] Domain scanned for noPac vulnerability
- [ ] MachineAccountQuota verified (default 10)
- [ ] Exploit executed successfully (shell or DCSync)
- [ ] Domain Admin privileges obtained from standard user
- [ ] DCSync performed to dump domain credentials
- [ ] KRBTGT hash obtained for persistence validation
- [ ] Attack chain documented with timestamps
- [ ] Patch status verified (KB5008380, KB5008602)

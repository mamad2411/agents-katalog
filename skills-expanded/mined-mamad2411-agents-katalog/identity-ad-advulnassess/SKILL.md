---
name: identity-ad-advulnassess
description: "Identity Ad Advulnassess."
domain: cybersecurity
---

-|
| Kerberoastable admin accounts | Critical | Remove SPNs or use MSA/gMSA |
| Unconstrained delegation on non-DCs | Critical | Switch to constrained/RBCD |
| Password Never Expires on admins | High | Enable password rotation policy |
| AS-REP roastable accounts | High | Enable Kerberos pre-authentication |
| AdminSDHolder modification | High | Audit and restore default ACLs |
| Stale computer accounts (90+ days) | Medium | Disable and move to quarantine OU |
| LDAP signing not enforced | Medium | Enable via GPO on all DCs |

## References

- [PingCastle GitHub](https://github.com/netwrix/pingcastle)
- [BloodHound CE](https://github.com/SpecterOps/BloodHound)
- [Purple Knight](https://www.purple-knight.com/)
- [MITRE ATT&CK - Active Directory](https://attack.mitre.org/techniques/T1484/)
- [Microsoft AD Security Best Practices](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/best-practices-for-securing-active-directory)

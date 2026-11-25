---
name: identity-ad-certificates-verify
description: "--| | Certificate request with SAN different from requester | Windows Event 4886 / 4887 on CA server | | Unusual PKINIT authentication | Event 4768 with certificate-based pre-auth | | Certify."
domain: cybersecurity
---

--|
| Certificate request with SAN different from requester | Windows Event 4886 / 4887 on CA server |
| Unusual PKINIT authentication | Event 4768 with certificate-based pre-auth |
| Certify.exe or Certipy execution | EDR process monitoring and command-line logging |
| Mass certificate template enumeration | LDAP query monitoring for pkiCertificateTemplate objects |
| Certificate issued to non-matching UPN | CA audit logs and certificate transparency |

## Validation Criteria

- [ ] AD CS Certificate Authority enumerated
- [ ] Vulnerable ESC1 templates identified with Certify or Certipy
- [ ] Certificate requested with Domain Admin SAN successfully
- [ ] PKINIT authentication performed with forged certificate
- [ ] Domain Admin TGT obtained
- [ ] Privileged access to domain controller validated
- [ ] Full attack chain documented with evidence
- [ ] Remediation recommendations provided (disable Supply in Request, require manager approval)

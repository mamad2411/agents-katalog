---
name: identity-serviceaccount-saaudit
description: "Identity Serviceaccount Saaudit."
domain: cybersecurity
---

-|
| Account Management | AC-2 | Service account lifecycle |
| Account Review | AC-2(3) | Periodic review of accounts |
| Least Privilege | AC-6 | Minimum service account permissions |
| Authenticator Management | IA-5 | Service credential rotation |
| Audit Review | AU-6 | Review service account activity |

## Common Pitfalls
- Disabling service accounts without verifying application dependencies first
- Not discovering service accounts outside of Active Directory
- Missing cloud service principals and managed identities
- Not checking for interactive logon rights on service accounts
- Failing to document dependencies before remediation

## Verification
- [ ] Service accounts inventoried across all platforms
- [ ] Each account has assigned owner
- [ ] Privileged service accounts documented with justification
- [ ] Password rotation compliance checked
- [ ] Orphaned accounts flagged for remediation
- [ ] gMSA migration candidates identified
- [ ] Compliance report generated

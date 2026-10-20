---
name: identity-pam-accessreview
description: "Identity Pam Accessreview."
domain: cybersecurity
---

-|
| Access Review | AC-2(3) | Periodic review of account privileges |
| Account Management | AC-2 | Account lifecycle management |
| Least Privilege | AC-6 | Minimum necessary access enforcement |
| Separation of Duties | AC-5 | SOD conflict identification |
| Audit Logging | AU-6 | Review of access audit records |

## Common Pitfalls
- Rubber-stamping: reviewers approving all access without examination
- Incomplete scope: missing critical applications from review campaigns
- No remediation tracking: revoking access on paper but not in systems
- Inconsistent reviewer assignment causing gaps in coverage
- Not including service accounts and non-human identities

## Verification
- [ ] All in-scope applications included in campaign
- [ ] Reviewers assigned for 100% of entitlements
- [ ] Campaign completion rate exceeds 95%
- [ ] Revocations executed within SLA
- [ ] Audit evidence package complete and archived
- [ ] SOD violations identified and documented
- [ ] Exceptions documented with business justification and expiry

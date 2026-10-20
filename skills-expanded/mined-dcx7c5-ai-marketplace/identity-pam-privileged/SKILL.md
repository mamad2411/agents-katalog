---
name: identity-pam-privileged
description: "Identity Pam Privileged."
domain: cybersecurity
---

--|
| Active user, justified privilege | Certify - maintain access |
| Active user, excessive privilege | Remediate - reduce to least privilege |
| Inactive > 90 days | Disable account, notify owner |
| No owner identified | Disable account, escalate to security |
| SoD conflict detected | Remediate - reassign or add compensating controls |
| Break-glass account | Verify last use was authorized, reset credentials |

### Step 4: Remediation and Enforcement

After reviews are completed:

- Revoke access for accounts that were not certified within the SLA period
- Implement automatic revocation for accounts not reviewed within 14 days
- Rotate credentials for all certified privileged accounts
- Convert standing privileges to just-in-time (JIT) access where possible
- Update PAM vault with current account inventory

### Step 5: Reporting and Documentation

Generate review reports including:

- Total accounts reviewed vs. total in scope
- Certification rate (approved vs. revoked)
- Average review completion time
- Overdue reviews and escalations
- Remediation actions taken
- Comparison with previous review cycle

## Validation Checklist

- [ ] Complete inventory of all privileged accounts documented
- [ ] All accounts assigned to a responsible owner/reviewer
- [ ] Review criteria and decision matrix defined
- [ ] Reviewers completed certification within SLA (14 days)
- [ ] Revoked accounts disabled and credentials rotated
- [ ] Orphaned accounts identified and disabled
- [ ] Service accounts reviewed for least privilege
- [ ] Break-glass accounts audited for authorized use only
- [ ] Review report generated with metrics and trends
- [ ] Remediation tickets created and tracked to completion
- [ ] Evidence preserved for compliance audit

## References

- [NIST SP 800-53 AC-2: Account Management](https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/)
- [CIS Controls v8 - Control 5: Account Management](https://www.cisecurity.org/controls/account-management)
- [Netwrix PAM Best Practices Guide](https://netwrix.com/en/resources/guides/privileged-account-management-best-practices/)
- [StrongDM PAM Best Practices 2025](https://www.strongdm.com/blog/privileged-access-management-best-practices)

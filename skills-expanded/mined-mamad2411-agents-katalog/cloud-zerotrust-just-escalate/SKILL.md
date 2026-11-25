---
name: cloud-zerotrust-just-escalate
description: "Cloud Zerotrust Just Escalate."
domain: cybersecurity
---

-|
| Temporary Access | AC-2(2) | Automated temporary account management |
| Least Privilege | AC-6 | Time-bound minimum access |
| Access Enforcement | AC-3 | Automated access grant/revoke |
| Audit | AU-3 | Complete JIT access audit trail |
| Risk Assessment | RA-3 | Risk-based approval routing |

## Common Pitfalls
- Setting time windows too long, negating JIT benefits
- Not implementing automatic revocation at expiration
- Complex approval workflows causing access delays for legitimate needs
- Not providing emergency bypass for critical incidents
- Failing to audit approved but unused JIT access

## Verification
- [ ] JIT request workflow functional end-to-end
- [ ] Access automatically revoked at expiration
- [ ] Approval routing correct for all risk levels
- [ ] Emergency access bypass works with post-review
- [ ] All JIT events logged to SIEM
- [ ] Standing privileges reduced by measurable percentage
- [ ] Mean time to access meets business SLA

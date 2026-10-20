---
name: identity-privilege-general
description: "Identity Privilege General."
domain: cybersecurity
---

-|
| Privileged Access | AC-6(7) | Privileged account controls |
| Credential Management | IA-5 | Automated credential rotation |
| Session Recording | AU-14 | Session audit capability |
| Access Enforcement | AC-3 | Vault-enforced access policies |
| Separation of Duties | AC-5 | Dual control for sensitive operations |

## Common Pitfalls
- Not configuring reconciliation accounts leading to lockouts after rotation
- Setting rotation schedules too aggressive for service accounts with dependencies
- Failing to test PSM connection components before production deployment
- Not establishing break-glass procedures for vault unavailability
- Overlooking network device credential management

## Verification
- [ ] Vault accessible only from authorized components
- [ ] Credential rotation succeeds for all onboarded accounts
- [ ] PSM sessions recorded and searchable
- [ ] Dual control enforced for sensitive credential checkout
- [ ] SIEM receives CyberArk audit events
- [ ] Break-glass procedure tested and documented
- [ ] DR vault failover tested successfully

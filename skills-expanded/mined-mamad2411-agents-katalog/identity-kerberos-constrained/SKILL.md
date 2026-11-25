---
name: identity-kerberos-constrained
description: "--| | S4U2self ticket requests | Event 4769 with unusual service and impersonation | | S4U2proxy forwarded tickets | Event 4769 with delegation flags set | | Alternate service name in ticket | Mismatch between requested SPN and actual service access | | Rubeus."
domain: cybersecurity
---

--|
| S4U2self ticket requests | Event 4769 with unusual service and impersonation |
| S4U2proxy forwarded tickets | Event 4769 with delegation flags set |
| Alternate service name in ticket | Mismatch between requested SPN and actual service access |
| Rubeus.exe execution | EDR process detection, command-line logging |
| Delegation configuration changes | Event 5136 for msDS-AllowedToDelegateTo modifications |

## Validation Criteria

- [ ] Accounts with Constrained Delegation enumerated
- [ ] Delegation targets (msDS-AllowedToDelegateTo) identified
- [ ] S4U2self ticket obtained for target user
- [ ] S4U2proxy ticket forwarded to delegation target
- [ ] Privileged access to delegated service validated
- [ ] Alternate service name substitution tested
- [ ] Protocol transition capability assessed
- [ ] Evidence documented with ticket exports and access proof

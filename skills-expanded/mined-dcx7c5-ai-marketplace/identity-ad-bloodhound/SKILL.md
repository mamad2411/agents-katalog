---
name: identity-ad-bloodhound
description: "Identity Ad Bloodhound."
domain: cybersecurity
---

|
| Shortest Path to Domain Admins | Find fastest route to DA |
| Find Kerberoastable Users with Path to DA | SPN accounts leading to DA |
| Find AS-REP Roastable Users | Accounts without pre-auth |
| Shortest Path from Owned Principals | Paths from compromised accounts |
| Find Computers with Unsupported OS | Legacy systems for exploitation |
| Find Users with DCSync Rights | Accounts that can replicate AD |
| Find GPOs that Modify Local Group Membership | GPO-based privilege escalation |

## Validation Criteria

- [ ] SharpHound data collected from all domains
- [ ] Attack paths identified from owned accounts to DA
- [ ] ACL-based attack paths documented
- [ ] Kerberoastable and AS-REP roastable accounts identified
- [ ] Exploitation plan created with prioritized paths
- [ ] Evidence screenshots captured for report

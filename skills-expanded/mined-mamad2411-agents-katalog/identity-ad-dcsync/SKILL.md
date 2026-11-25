---
name: identity-ad-dcsync
description: "Identity Ad Dcsync."
domain: cybersecurity
---

--|
| DrsGetNCChanges RPC calls from non-DC sources | Network monitoring for DRSUAPI traffic from unusual IPs |
| Event 4662 with Replicating Directory Changes GUIDs | Windows Security Log on DC (1131f6aa-/1131f6ad- GUIDs) |
| Event 4624 with Golden Ticket anomalies | Logon events with impossible SIDs or non-existent users |
| ACL modifications on domain root object | Event 5136 (directory service changes) |
| Replication traffic volume spike | Network baseline deviation monitoring |

## Validation Criteria

- [ ] Accounts with DCSync rights enumerated
- [ ] KRBTGT hash extracted via DCSync
- [ ] All domain credentials dumped successfully
- [ ] Golden Ticket forged and validated for DA access
- [ ] DCSync rights persistence mechanism established (if in scope)
- [ ] Access to Domain Controller validated with Golden Ticket
- [ ] Evidence documented with hash values and timestamps
- [ ] Remediation recommendations provided (double KRBTGT reset, ACL audit)

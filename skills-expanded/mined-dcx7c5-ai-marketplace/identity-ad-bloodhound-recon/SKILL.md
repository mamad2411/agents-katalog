---
name: identity-ad-bloodhound-recon
description: "Identity Ad Bloodhound Recon."
domain: cybersecurity
---

|
| ACL Abuse | Exploit misconfigured ACLs | GenericAll on DA group |
| Kerberoasting | Crack service account passwords | SPN account → DA |
| AS-REP Roasting | Attack accounts without pre-auth | No-preauth user → password crack |
| Delegation Abuse | Exploit unconstrained/constrained delegation | Computer → impersonate DA |
| GPO Abuse | Modify GPOs applied to privileged OUs | GPO write → code execution on DA |
| Session Hijack | Leverage DA sessions on compromised hosts | Admin session → token theft |

## Validation Criteria

- [ ] BloodHound CE deployed and accessible
- [ ] SharpHound v2 data collected from all domains in scope
- [ ] Data successfully imported into BloodHound CE
- [ ] Owned principals marked in the interface
- [ ] Shortest paths to Domain Admin identified
- [ ] ACL-based attack paths documented
- [ ] Kerberoastable and AS-REP roastable accounts listed
- [ ] Custom Cypher queries executed for advanced analysis
- [ ] Attack paths prioritized by feasibility and stealth
- [ ] Report generated with all identified paths and evidence

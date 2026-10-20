---
name: identity-credentials-lazagne
description: "Identity Credentials Lazagne."
domain: cybersecurity
---

--|
| LaZagne.exe process execution | EDR process monitoring with hash-based detection |
| Access to Chrome Login Data SQLite DB | File access monitoring on browser credential stores |
| DPAPI CryptUnprotectData API calls | API hooking and ETW tracing |
| Access to Windows Credential Manager | Event 5379 (Credential Manager read) |
| Mass credential store enumeration | Behavioral analysis for sequential access patterns |
| Python interpreter accessing credential files | Script block logging and file access auditing |

## Validation Criteria

- [ ] LaZagne deployed on compromised endpoint
- [ ] Full credential extraction completed (all modules)
- [ ] Credentials exported in JSON format for analysis
- [ ] Recovered credentials parsed and deduplicated
- [ ] High-value credentials identified and prioritized
- [ ] Domain credentials validated against AD
- [ ] Lateral movement opportunities identified from recovered creds
- [ ] Evidence documented with appropriate handling procedures

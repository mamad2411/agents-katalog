---
name: crypto-tools-hashcat-crack
description: "Crypto Tools Hashcat Crack."
domain: cybersecurity
---

-|
| 0 | MD5 | Legacy web apps |
| 100 | SHA-1 | Legacy systems |
| 1000 | NTLM | Windows credentials |
| 1800 | sha512crypt | Linux /etc/shadow |
| 3200 | bcrypt | Modern web apps |
| 13100 | Kerberos TGS-REP | Active Directory |

## Security Considerations

- Only perform hash cracking with explicit written authorization
- Secure all captured hash data in transit and at rest
- Report all cracked passwords immediately to asset owners
- Use results to improve password policies, not exploit users
- Destroy cracked password data after engagement concludes
- Follow rules of engagement for penetration test scope

## Validation Criteria

- [ ] Hash type identification is correct
- [ ] Dictionary attack cracks weak passwords
- [ ] Rule-based attack cracks policy-compliant passwords
- [ ] Mask attack cracks short passwords
- [ ] Results report shows password strength distribution
- [ ] All operations performed within authorized scope

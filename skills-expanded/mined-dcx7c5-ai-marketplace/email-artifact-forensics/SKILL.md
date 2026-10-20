---
name: email-artifact-forensics
description: "-| | 1 | email | test@test.com%0ACc:evil@evil.com | CC header injected | High | | 2 | email | test@test."
domain: cybersecurity
---

-|
| 1 | email | test@test.com%0ACc:evil@evil.com | CC header injected | High |
| 2 | email | test@test.com%0ABcc:evil@evil.com | BCC header injected | High |
| 3 | name | Test%0AFrom:ceo@target.com | From spoofing | Medium |

### Remediation
- Validate email addresses with strict regex rejecting newline characters
- Strip \r, \n, and encoded variants from all email-related input
- Use parameterized email APIs that separate headers from data
- Implement rate limiting on email-sending functionality
```

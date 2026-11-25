---
name: identity-saml-okta-verify
description: "Identity Saml Okta Verify."
domain: cybersecurity
---

-|
| Authentication | IA-2 | Multi-factor authentication through Okta |
| Session Management | SC-23 | SAML session lifetime controls |
| Audit Logging | AU-3 | Log all SSO authentication events |
| Certificate Management | SC-17 | PKI certificate lifecycle management |
| Access Enforcement | AC-3 | SAML attribute-based access control |

## Common Pitfalls
- Using SHA-1 instead of SHA-256 for SAML signatures
- Not validating InResponseTo in SAML responses (replay attacks)
- Clock skew between IdP and SP causing assertion rejection
- Failing to restrict audience URI allowing assertion forwarding
- Not implementing certificate rotation before expiry causes outage

## Verification
- [ ] SAML SSO login completes successfully via SP-initiated flow
- [ ] IdP-initiated flow correctly authenticates users
- [ ] SAML assertions use SHA-256 signatures
- [ ] Attribute mapping correctly populates user profile
- [ ] Session timeout forces re-authentication
- [ ] SLO properly terminates sessions on both IdP and SP
- [ ] Certificate rotation tested without service interruption

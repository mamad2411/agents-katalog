---
name: identity-mfa-duo-verify
description: "Identity Mfa Duo Verify."
domain: cybersecurity
---

-|
| MFA | IA-2(1) | Multi-factor authentication for network access |
| MFA for Privileged | IA-2(2) | MFA for privileged account access |
| Replay Resistance | IA-2(8) | Replay-resistant authentication |
| Device Identification | IA-3 | Device identity and trust |
| Authenticator Management | IA-5 | MFA enrollment and lifecycle |

## Common Pitfalls
- Not deploying phishing-resistant MFA (Verified Push/FIDO2) for privileged accounts
- Setting failmode to "safe" (allow access when Duo is down) in production
- Not disabling SMS/phone call for users with app-capable devices
- Forgetting to configure offline access for laptops
- Not monitoring for MFA fatigue/prompt bombing attacks

## Verification
- [ ] VPN login requires Duo MFA
- [ ] RDP to servers requires Duo MFA
- [ ] SSH access requires Duo MFA
- [ ] Verified Push enabled for privileged users
- [ ] Device health policy blocks non-compliant devices
- [ ] Authentication logs forwarded to SIEM
- [ ] Bypass/emergency access procedures tested
- [ ] MFA fatigue detection alerts configured

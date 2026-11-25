---
name: crypto-theory-cryptographic-learn
description: "Crypto Theory Cryptographic Learn."
domain: cybersecurity
---

|
| Weak Hashing | MD5, SHA-1 for integrity/signatures | High |
| Insecure Encryption | DES, 3DES, RC4, Blowfish | High |
| Bad Cipher Mode | ECB mode for any block cipher | High |
| Insufficient Key Size | RSA < 2048, AES-128 for long-term | Medium |
| Hardcoded Secrets | Keys/passwords in source code | Critical |
| Weak KDF | Low iteration PBKDF2, plain MD5 | High |
| Poor Entropy | time-based seeds, predictable IVs | High |
| Deprecated Protocols | SSLv3, TLS 1.0, TLS 1.1 | High |

## Security Considerations

- Review both application code and configuration files
- Check third-party dependencies for known crypto vulnerabilities
- Verify certificates and TLS configurations on deployed servers
- Ensure secrets are loaded from environment variables or vaults
- Review key storage and rotation practices

## Validation Criteria

- [ ] Scanner detects all injected test weaknesses
- [ ] MD5/SHA-1 usage for security purposes is flagged
- [ ] ECB mode usage is flagged
- [ ] Hardcoded keys/passwords are detected
- [ ] Weak KDF parameters are identified
- [ ] Report includes severity, location, and remediation
- [ ] False positive rate is below 10%

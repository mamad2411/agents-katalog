---
name: crypto-hardware-hsm-configure
description: "--| | CKO_SECRET_KEY | Symmetric keys (AES) | Encrypt, Decrypt, Wrap | | CKO_PUBLIC_KEY | Public keys (RSA, EC) | Verify, Encrypt, Wrap | | CKO_PRIVATE_KEY | Private keys (RSA, EC) | Sign, Decrypt, Unwrap | | CKO_CERTIFICATE | X."
domain: cybersecurity
---

--|
| CKO_SECRET_KEY | Symmetric keys (AES) | Encrypt, Decrypt, Wrap |
| CKO_PUBLIC_KEY | Public keys (RSA, EC) | Verify, Encrypt, Wrap |
| CKO_PRIVATE_KEY | Private keys (RSA, EC) | Sign, Decrypt, Unwrap |
| CKO_CERTIFICATE | X.509 certificates | Storage, retrieval |

## Security Considerations

- Never export private keys from HSM (use CKA_EXTRACTABLE=False)
- Use separate slots/partitions for different applications
- Implement multi-person key ceremony for CA root keys
- Enable audit logging for all HSM operations
- Implement HSM backup and disaster recovery
- Use strong PINs and enable SO (Security Officer) PIN

## Validation Criteria

- [ ] SoftHSM2 initializes with token and user PIN
- [ ] AES key generates inside HSM
- [ ] RSA key pair generates inside HSM
- [ ] Encryption/decryption uses HSM-resident keys
- [ ] Signing/verification uses HSM-resident keys
- [ ] Keys cannot be exported (non-extractable)
- [ ] Key listing shows all HSM-stored objects

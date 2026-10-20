---
name: cloud-aws-nitro-verify
description: "| | PCR0 (Image) | a1b2c3d4e5f6... | Yes | | PCR1 (Kernel) | f6e5d4c3b2a1."
domain: cybersecurity
---

|
| PCR0 (Image) | a1b2c3d4e5f6... | Yes |
| PCR1 (Kernel) | f6e5d4c3b2a1... | Yes |
| PCR2 (Application) | 1a2b3c4d5e6f... | No |
| PCR8 (Signing Cert) | 9f8e7d6c5b4a... | Yes (production) |

### KMS Key Policy Verification
- Key ARN: arn:aws:kms:us-east-1:111122223333:key/mrk-abc123
- Attestation condition: kms:RecipientAttestation:ImageSha384 = PCR0
- Signing cert condition: kms:RecipientAttestation:PCR8 = <cert-hash>
- Parent role: arn:aws:iam::111122223333:role/EnclaveParentRole
- Direct decrypt from parent: BLOCKED (attestation required)
- Decrypt from verified enclave: ALLOWED

### Security Posture
- [PASS] Debug mode disabled in production launch command
- [PASS] Vsock is the only communication channel (no network interface)
- [PASS] Attestation document nonce verification implemented
- [PASS] Certificate chain validates to AWS Nitro root CA
- [WARN] PCR0 used in policy; consider PCR8 for deployment flexibility
- [FAIL] Health check endpoint does not verify enclave attestation freshness
```

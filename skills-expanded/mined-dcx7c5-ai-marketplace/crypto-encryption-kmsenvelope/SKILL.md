---
name: crypto-encryption-kmsenvelope
description: "-| | Max data size | 4 KB | Unlimited | | Latency | Network round-trip per operation | Local encryption | | Cost | $0."
domain: cybersecurity
---

-|
| Max data size | 4 KB | Unlimited |
| Latency | Network round-trip per operation | Local encryption |
| Cost | $0.03/10,000 requests | Fewer KMS requests |
| Offline | Not possible | Yes (with cached DEKs) |

### KMS Key Types

- **AWS Managed**: AWS creates and manages (`aws/s3`, `aws/ebs`)
- **Customer Managed**: You create and manage policies
- **Custom Key Store**: Backed by CloudHSM cluster

## Security Considerations

- Never store plaintext DEK; only keep encrypted DEK
- Use key policies to restrict who can call GenerateDataKey and Decrypt
- Enable AWS CloudTrail logging for all KMS API calls
- Implement key rotation (automatic annual rotation for CMKs)
- Use encryption context for authenticated encryption metadata
- Handle KMS throttling with exponential backoff

## Validation Criteria

- [ ] GenerateDataKey returns plaintext and encrypted DEK
- [ ] Data encrypts correctly with plaintext DEK using AES-256-GCM
- [ ] Encrypted DEK can be decrypted via KMS Decrypt API
- [ ] Decrypted DEK recovers the original data
- [ ] Plaintext DEK is wiped from memory after use
- [ ] Encryption context is validated during decryption
- [ ] Key rotation re-encrypts DEKs with new master key

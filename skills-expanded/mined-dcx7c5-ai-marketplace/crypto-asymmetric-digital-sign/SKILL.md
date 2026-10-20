---
name: crypto-asymmetric-digital-sign
description: "Crypto Asymmetric Digital Sign."
domain: cybersecurity
---

-|
| Security | 128-bit | 128-bit | 128-bit |
| Public key size | 32 bytes | 384 bytes | 64 bytes |
| Signature size | 64 bytes | 384 bytes | 64 bytes |
| Key generation | ~50 us | ~100 ms | ~1 ms |
| Sign | ~70 us | ~5 ms | ~200 us |
| Verify | ~200 us | ~200 us | ~500 us |
| Deterministic | Yes | No (PSS) | No (unless RFC 6979) |

### Key Properties

- **Deterministic**: Same message + key always produces same signature
- **Collision-resistant**: No separate hash function needed
- **Side-channel resistant**: Constant-time implementation
- **Small keys**: 32 bytes each (public and private)

## Security Considerations

- Ed25519 does not support key recovery from signatures
- Verify the full message, not a hash (Ed25519 hashes internally)
- Public keys must be validated before use (check for low-order points)
- Private keys should be stored encrypted at rest
- Ed25519 is not yet approved for all NIST use cases (Ed448 is preferred for federal)

## Validation Criteria

- [ ] Key pair generation produces valid Ed25519 keys
- [ ] Signature verification succeeds for valid message
- [ ] Signature verification fails for tampered message
- [ ] Signature verification fails for wrong public key
- [ ] Deterministic: same input produces same signature
- [ ] File signing and verification works correctly
- [ ] Performance meets or exceeds RSA-3072

---
name: crypto-posthash-zero-quantum
description: "| | Completeness | Honest prover always convinces honest verifier | | Soundness | Dishonest prover cannot convince verifier (except negligible probability) | | Zero-Knowledge | Verifier learns nothing beyond the statement's truth |  ### Schnorr Protocol  1."
domain: cybersecurity
---

|
| Completeness | Honest prover always convinces honest verifier |
| Soundness | Dishonest prover cannot convince verifier (except negligible probability) |
| Zero-Knowledge | Verifier learns nothing beyond the statement's truth |

### Schnorr Protocol

1. **Setup**: Public generator g, prime p, q (order of g)
2. **Registration**: Prover computes y = g^x mod p (public key from secret x)
3. **Commitment**: Prover sends t = g^r mod p (random r)
4. **Challenge**: Verifier sends random c
5. **Response**: Prover sends s = r + c*x mod q
6. **Verify**: Check g^s == t * y^c mod p

## Security Considerations

- Use cryptographically secure random number generators
- Challenge must be unpredictable (from verifier's perspective)
- For non-interactive proofs, use Fiat-Shamir with collision-resistant hash
- ZKP alone does not provide forward secrecy; combine with TLS

## Validation Criteria

- [ ] Honest prover always verifies successfully (completeness)
- [ ] Random response without secret does not verify (soundness)
- [ ] Server never receives the secret value
- [ ] Non-interactive proof is verifiable offline
- [ ] Multiple authentications produce different transcripts
- [ ] Protocol resists replay attacks

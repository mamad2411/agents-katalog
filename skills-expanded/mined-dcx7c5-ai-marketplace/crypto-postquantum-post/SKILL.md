---
name: crypto-postquantum-post
description: "Crypto Postquantum Post."
domain: cybersecurity
---

-|
| Security Level | NIST Level 2 | NIST Level 3 | NIST Level 5 |
| Public Key Size | 1,312 bytes | 1,952 bytes | 2,592 bytes |
| Signature Size | 2,420 bytes | 3,293 bytes | 4,595 bytes |
| Secret Key Size | 2,560 bytes | 4,032 bytes | 4,896 bytes |

### Phase 6: Migration Roadmap Generation

Generate a prioritized migration roadmap based on inventory and assessment results:

```python
# Generate complete migration roadmap
python scripts/agent.py --action roadmap \
    --scan-results tls_inventory.json \
    --agility-results agility_report.json \
    --output migration_roadmap.json
```

The roadmap prioritizes systems by:
1. **Data sensitivity**: Systems handling long-lived secrets migrate first
2. **Exposure level**: Internet-facing services before internal
3. **Crypto-agility**: Systems that can easily swap algorithms first
4. **Compliance requirements**: Federal/regulated systems per NIST IR 8547 timeline
5. **Dependency chains**: Libraries and frameworks before applications

## Examples

### Full Assessment Pipeline

```bash
# Step 1: Scan all TLS endpoints
python scripts/agent.py --action scan_tls --targets hosts.txt --output scan.json

# Step 2: Assess crypto-agility
python scripts/agent.py --action assess_agility --scan-results scan.json --output agility.json

# Step 3: Test hybrid TLS on critical servers
python scripts/agent.py --action test_hybrid_tls --target critical.example.com:443

# Step 4: Validate ML-KEM support
python scripts/agent.py --action test_mlkem --output mlkem.json

# Step 5: Validate ML-DSA support
python scripts/agent.py --action test_mldsa --output mldsa.json

# Step 6: Generate migration roadmap
python scripts/agent.py --action roadmap --scan-results scan.json --agility-results agility.json --output roadmap.json
```

### Quick Server Assessment

```bash
# Single server PQC readiness check
python scripts/agent.py --action scan_tls --target server.example.com:443
```

## Validation Checklist

- [ ] Cryptographic inventory covers all TLS endpoints, certificates, and key stores
- [ ] All quantum-vulnerable algorithms (RSA, ECDH, ECDSA, DH, DSA) are identified
- [ ] Crypto-agility assessment documents library versions and upgrade paths
- [ ] Hybrid TLS (X25519MLKEM768) tested on representative server configurations
- [ ] ML-KEM key encapsulation validated at target security level (768 recommended)
- [ ] ML-DSA signature verification validated for certificate chain use
- [ ] SLH-DSA (FIPS 205) evaluated as backup signature algorithm
- [ ] Migration roadmap prioritizes by data sensitivity and compliance timeline
- [ ] OpenSSL version and oqs-provider compatibility confirmed
- [ ] Key size increases accounted for in network and storage capacity planning
- [ ] HSM/KMS compatibility with PQC algorithms verified
- [ ] Performance impact of PQC algorithms benchmarked under production load
- [ ] "Harvest now, decrypt later" risk assessed for sensitive data channels
- [ ] Certificate Authority PQC readiness confirmed for certificate issuance

## References

- NIST PQC Standards: https://csrc.nist.gov/projects/post-quantum-cryptography
- FIPS 203 (ML-KEM): https://csrc.nist.gov/pubs/fips/203/final
- FIPS 204 (ML-DSA): https://csrc.nist.gov/pubs/fips/204/final
- FIPS 205 (SLH-DSA): https://csrc.nist.gov/pubs/fips/205/final
- NIST SP 1800-38 Migration Guide: https://www.nccoe.nist.gov/crypto-agility-considerations-migrating-post-quantum-cryptographic-algorithms
- NIST IR 8547 Transition Timeline: https://csrc.nist.gov/pubs/ir/8547/ipd
- Open Quantum Safe Project: https://openquantumsafe.org/
- oqs-provider for OpenSSL: https://github.com/open-quantum-safe/oqs-provider
- OQS TLS Integration: https://openquantumsafe.org/applications/tls.html
- CISA PQC Migration Strategy: https://www.cisa.gov/sites/default/files/2024-09/Strategy-for-Migrating-to-Automated-PQC-Discovery-and-Inventory-Tools.pdf
- IETF Hybrid Key Exchange Draft: https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/
- CycloneDX Crypto BOM: https://cyclonedx.org/use-cases/cryptographic-key/

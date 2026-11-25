---
name: crypto-certificates-transparency
description: "6. Always read-only — never modify trust stores or key material 7."
domain: cybersecurity
---

## Rules for Agents

1. Rogue root CA = **CRITICAL** — immediate escalation to CYBERSEC-AGENT
2. World-readable private key = **CRITICAL**
3. Log every certificate SHA-256 fingerprint and serial number to `iocs.md`
4. Unexpected issuer for monitored domain = **HIGH**
5. OCSP/CRL next-update in the past = **MEDIUM** (revocation infrastructure offline)
6. Always read-only — never modify trust stores or key material
7. Sync all certificate IOCs to shared memory at session end

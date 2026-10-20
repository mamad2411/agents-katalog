---
name: keyvault-analyze-certificates
description: Analyze Azure Key Vault certificate lifecycle, policy, issuance, renewal, versions, chain/bundle handling, private-key access, and application consumption. Use for TLS certificate expiry, renewal failures, wrong certificate version, or certificate integration issues.
---

# Analyze Certificates

1. Identify certificate name, consuming endpoint/service, issuer model, renewal policy, and expected SAN/CN usage.
2. Inspect certificate metadata, validity, versions, policy, and renewal status.
3. Check whether the application consumes the certificate object, secret-backed PFX/PEM, or public certificate.
4. Correlate renewal/version changes with deployment/runtime behavior.
5. Distinguish certificate lifecycle problems from DNS, ingress, trust-store, or application issues.
6. Never expose private key material or certificate passwords.

## Output
- Certificate State
- Renewal/Version Findings
- Consumption Pattern
- Trust/Runtime Correlation
- Recommended Action

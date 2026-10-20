---
name: crypto-signing-code
description: "Crypto Signing Code."
domain: cybersecurity
---

|
| Code Signing | Cryptographic process of signing software artifacts to verify publisher identity and artifact integrity |
| Detached Signature | Signature stored in a separate file from the artifact, allowing independent distribution |
| Keyless Signing | Sigstore's approach using short-lived certificates tied to OIDC identities instead of long-lived keys |
| Provenance | Metadata describing how, where, and by whom an artifact was built |
| Transparency Log | Append-only log (Rekor) that records all signing events for public auditability |
| Trust Chain | Hierarchical chain from root CA to signing certificate establishing trust in the signer's identity |
| SLSA | Supply-chain Levels for Software Artifacts — framework defining levels of supply chain security |

## Tools & Systems

- **GPG/PGP**: Traditional asymmetric cryptography tool for signing and verifying artifacts
- **Sigstore (cosign)**: Modern keyless signing infrastructure using OIDC identity and transparency logs
- **Rekor**: Sigstore's transparency log recording all signing events immutably
- **Fulcio**: Sigstore's certificate authority issuing short-lived certificates bound to OIDC identities
- **notation**: Microsoft's artifact signing tool for OCI registries (Project Notary v2)

## Common Scenarios

### Scenario: Establishing Signed Release Pipeline

**Context**: An open-source project needs to sign release artifacts so users can verify authenticity and detect tampering.

**Approach**:
1. Use Sigstore keyless signing in GitHub Actions (no key management overhead)
2. Sign all release binaries with `cosign sign-blob` using OIDC identity
3. Generate and sign checksums file for bulk verification
4. Upload signatures, certificates, and checksums alongside release artifacts
5. Document verification instructions in the project README
6. Add verification step to the Homebrew formula or apt repository

**Pitfalls**: GPG key compromise requires revoking and re-signing all artifacts. Sigstore keyless signing avoids this by using ephemeral keys. Long-lived signing keys in CI/CD secrets are a supply chain risk if the CI system is compromised.

## Output Format

```
Artifact Signing Report
========================
Pipeline: Build and Sign v2.3.0
Date: 2026-02-23
Signing Method: Sigstore Keyless + GPG

SIGNED ARTIFACTS:
  app-v2.3.0-linux-amd64.tar.gz
    GPG:      PASS (ci-signing@company.com, EdDSA/Ed25519)
    Sigstore: PASS (Rekor entry: 24658135, Fulcio cert issued)
    SHA256:   a1b2c3d4...

  app-v2.3.0-darwin-arm64.tar.gz
    GPG:      PASS
    Sigstore: PASS (Rekor entry: 24658136)
    SHA256:   e5f6g7h8...

  checksums.sha256
    GPG:      PASS (detached signature)

TRANSPARENCY LOG:
  Entries recorded: 3
  Log index range: 24658135-24658137
  Verification: https://search.sigstore.dev
```

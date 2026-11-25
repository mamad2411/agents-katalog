# TSB Supply Chain Security Auditor

A reference implementation skill demonstrating TeaAgent's TSB (Provenanced Skill Bundle) capabilities for supply chain security auditing.

## Use Case

When integrating third-party AI skills or dependencies, you need to verify their provenance and security. This skill uses TeaAgent's TSB verification to:
- Verify cryptographic signatures using Sigstore keyless signing
- Check bundle hash integrity to detect tampering
- Validate audit chains for complete history
- Support offline verification for air-gapped environments

## Capabilities

- **Signature Verification**: Validates Sigstore keyless signatures with OIDC identity enforcement
- **Hash Integrity**: Detects any file content or structure tampering
- **Audit Chain Validation**: Ensures complete, tamper-evident history of changes
- **Offline Mode**: Supports verification without internet access (air-gapped)
- **Path Traversal Protection**: Prevents malicious archive extraction attacks

## Usage

```bash
# Online verification with identity enforcement
teaagent skill verify-tsb skill.tsb --identity "author@example.com" --issuer "https://accounts.google.com"

# Offline verification for air-gapped environments
teaagent skill verify-tsb skill.tsb --offline
```

## Example Workflow

1. Receive a `.tsb` skill bundle from a third party
2. Run verification with identity policy to ensure it's from a trusted author
3. Review the verification output for any security warnings
4. Extract the skill only if verification succeeds
5. Install the skill with confidence in its provenance

## Security Features

- **Path-Aware Hashing**: Includes relative file paths in hash calculation to prevent structural attacks
- **Deterministic Hashing**: Same skill produces identical hash across builds
- **Sigstore Integration**: Uses industry-standard keyless signing with Fulcio/Rekor
- **Identity Enforcement**: Can require specific OIDC email or issuer
- **Offline Verification**: No network dependency for air-gapped deployments

## Requirements

- TeaAgent with TSB support
- sigstore-python (for online verification)
- Git repository (for audit chain validation)

## Verification Output

The skill provides detailed verification results:
- Bundle hash match status
- Signature validity
- Certificate chain verification
- Audit chain integrity
- Identity policy compliance

## Author

TeaEntityLab

## License

MIT

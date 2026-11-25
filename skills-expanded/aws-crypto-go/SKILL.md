---
name: aws-crypto-go
description: "Use for any Go code involving the AWS Encryption SDK or MPL: github.com/aws/aws-encryption-sdk/releases/go/encryption-sdk, github.com/aws/aws-cryptographic-material-providers-library/releases/go/mpl. Triggers on: KMS hierarchical keyring (CreateAwsKmsHierarchicalKeyring, BranchKeyId, TtlSeconds), DynamoDB branch key storage, mpl client, esdk client, CommitmentPolicy, RequireEncryptRequireDecrypt, encryption context / AAD binding, context_mismatch or integrity_violation decrypt errors, envelope encryption in Go + KMS, reducing KMS API calls (hierarchical vs plain keyring), porting Caching CMM from Java or Python to Go (Go SDK has no Caching CMM — hierarchical keyring is the Go-native equivalent), import path questions for the Go encryption SDK, or encrypting secrets/tokens/ciphertext in a Go service with KMS. Do not answer AWS Encryption SDK + Go questions from training alone — always consult this skill."
alwaysApply: false
---

# AWS Encryption SDK for Go

Use this skill when implementing encryption/decryption with the AWS Encryption SDK in Go applications.

**Supporting files (load when needed):**
- [reference.md](reference.md) - Detailed API documentation, import paths, types
- [examples.md](examples.md) - Complete code examples for all patterns

## Library

Use the **latest version** of the official AWS Encryption SDK for Go:

```
github.com/aws/aws-encryption-sdk/releases/go/encryption-sdk
github.com/aws/aws-cryptographic-material-providers-library/releases/go/mpl
```

**API Reference:** https://pkg.go.dev/github.com/aws/aws-encryption-sdk/releases/go/encryption-sdk

---

## AWS Best Practices (MANDATORY)

These rules are derived from the [AWS Encryption SDK Best Practices](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/best-practices.html).

### 1. Use Latest Version

Always use the latest SDK version. Upgrade promptly when new versions are released. Replace deprecated APIs immediately.

### 2. Use Default Values

The SDK encodes best practices in its defaults. Use them unless you have a specific, security-reviewed reason not to.

### 3. Key Commitment (MANDATORY)

**Always use `RequireEncryptRequireDecrypt`** commitment policy:

```go
encryptionClient, err := client.NewClient(esdktypes.AwsEncryptionSdkConfig{
    CommitmentPolicy: mpltypes.ESDKCommitmentPolicyRequireEncryptRequireDecrypt.Enum(),
})
```

Key commitment:
- Verifies the unique data key identity
- Prevents decryption to multiple plaintexts
- Adds only ~30 bytes to ciphertext

**Never use** `ForbidEncryptAllowDecrypt` for new implementations.

### 4. Encryption Context (MANDATORY)

**Always provide an encryptionContext** for Additional Authenticated Data (AAD):

```go
encryptionContext := map[string]string{
    "service_id": serviceID,
    "purpose":    "token_encryption",
}
```

Rules:
- **Do NOT include secrets** — context is stored in plaintext in ciphertext header
- **Include identifying info** — tenant ID, service ID, resource type
- **Verify on decrypt** — check returned context matches expected values
- Context is cryptographically bound via AAD

### 5. Specify Wrapping Keys Explicitly

**Always specify wrapping keys** when encrypting AND decrypting:

```go
// Good: Explicit key specification
keyring, err := mplClient.CreateAwsKmsKeyring(mpltypes.CreateAwsKmsKeyringInput{
    KmsClient: kmsClient,
    KmsKeyId:  kmsKeyArn,  // Explicit ARN
})
```

Benefits:
- Prevents using unintended keys
- Avoids cross-account/cross-region issues
- Improves performance (no key discovery)

**Avoid discovery mode** unless absolutely necessary. If required, use discovery filters.

### 6. Protect Wrapping Keys

- Use AWS KMS with proper key policies
- Apply least privilege via IAM policies
- For raw keys, use HSM or AWS CloudHSM
- Never hardcode keys in source code

### 7. Use Digital Signatures

The default algorithm suite includes ECDSA signatures. **Keep this enabled** unless:
- Performance requirements are extreme
- A security engineer has explicitly approved removal
- The same entity encrypts and decrypts

### 8. Limit Encrypted Data Keys

When decrypting untrusted messages, be aware that messages can contain up to 65,535 encrypted data keys. Consider implementing limits for untrusted sources.

---

## ⚠️ Go SDK Caching Limitation

**The Go SDK does NOT support the standard Caching CMM** found in Java/Python SDKs.

For caching, cost reduction, or high-volume encryption: **Use the AWS KMS Hierarchical Keyring**.

### Hierarchical Keyring Benefits

| Feature | Benefit |
|---------|---------|
| Branch key caching | Reduces KMS API calls by ~99% |
| DynamoDB storage | Durable, scalable key storage |
| Multi-tenant isolation | Encryption context routing |
| Automatic rotation | Built-in key versioning |

### Key Hierarchy

1. **KEK** (Key Encryption Key) — AWS KMS key protecting branch keys
2. **Branch Keys** — Cached in DynamoDB, rotated periodically
3. **DEK** (Data Encryption Key) — Generated per encrypt operation

See [examples.md](examples.md) for complete Hierarchical Keyring setup code.

---

## Quick Reference

### Commitment Policies

| Policy | Use Case |
|--------|----------|
| `RequireEncryptRequireDecrypt` | **Default — always use** |
| `RequireEncryptAllowDecrypt` | Migration from old ciphertext only |
| `ForbidEncryptAllowDecrypt` | **Never use for new code** |

### Error Categories

| Error Kind | Description |
|------------|-------------|
| `encryption_failed` | Key unavailable, permissions error |
| `decryption_failed` | Wrong key, corrupted data |
| `context_mismatch` | AAD verification failed |
| `integrity_violation` | Tampering detected |
| `kek_unavailable` | KMS/branch key not accessible |

---

## Implementation Checklist

Before completing any encryption implementation:

- [ ] Using **latest SDK version**
- [ ] CommitmentPolicy is `RequireEncryptRequireDecrypt`
- [ ] All encrypt/decrypt calls include meaningful `encryptionContext`
- [ ] Encryption context does **not** contain secrets
- [ ] Wrapping keys specified **explicitly** (no discovery mode)
- [ ] Decryption **verifies** returned encryption context
- [ ] Digital signatures **enabled** (default algorithm suite)
- [ ] Branch keys created before first use (Hierarchical Keyring)
- [ ] Error handling distinguishes encryption/decryption/context errors
- [ ] Cache TTL balanced (security vs. KMS costs)
- [ ] Key policies follow least privilege

---

## External Resources

- [AWS Encryption SDK Best Practices](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/best-practices.html)
- [Hierarchical Keyring Example](https://github.com/aws/aws-encryption-sdk/blob/mainline/releases/go/encryption-sdk/examples/keyring/awskmshierarchicalkeyring/awskmshierarchicalkeyring.go)
- [Branch Key Supplier Example](https://github.com/aws/aws-encryption-sdk/blob/mainline/releases/go/encryption-sdk/examples/keyring/awskmshierarchicalkeyring/branchkeysupplier.go)

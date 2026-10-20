---
name: secrets-kms
description: Use when using AWS KMS or GCP KMS — envelope encryption, signing, key rotation, IAM/grants, cross-account, cost (KMS API calls add up).
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [secrets-vault, security, storage-object-s3, observability-essentials]
---

# AWS KMS & GCP KMS

**Iron Law: KMS never sees your plaintext. Use envelope encryption — KMS wraps a per-payload DEK, the DEK encrypts the data. Encrypt-direct only for payloads < 4KB and only when you don't care about throughput.**

**Versions:** AWS KMS API `2014-11-01` (stable) · GCP Cloud KMS `v1` (stable) — _Both stable since ~2017; new capabilities (RSA-PSS sig algorithms, HSM tiers, multi-region keys) layer onto the same primitives. Pin SDK versions, not API._

## Envelope encryption — the only sane pattern for real payloads

KMS encrypt/decrypt is **rate-limited (~10k req/s per region default) and billable per call ($0.03/10k)**. A naive design that POSTs every blob to KMS hits both limits within a week of growth.

```
                ┌─────────────────────────────────┐
plaintext ─────►│ 1. AES-GCM encrypt with DEK     │─► ciphertext (store in S3/DB)
                └──────────────┬──────────────────┘
                               │ DEK is random per-payload (or per-tenant, cached)
                               ▼
                ┌─────────────────────────────────┐
                │ 2. KMS.Encrypt(DEK) → wrapped   │─► wrapped DEK (store alongside ciphertext)
                └─────────────────────────────────┘
```

Decrypt is symmetric: `KMS.Decrypt(wrapped_DEK)` once → AES-GCM-decrypt with DEK. AWS SDK ships `GenerateDataKey` which returns plaintext + wrapped DEK in one call — use it, never roll your own DEK generation.

**Cache the DEK**. Per-tenant DEK cached for an hour (in-memory, never on disk) cuts KMS calls from per-request to per-tenant-per-hour. Document the cache window — it's also the rotation lag.

**Bind the DEK to its purpose with `EncryptionContext`** — additional authenticated data passed to `Encrypt`/`Decrypt`. KMS will refuse to decrypt unless the same context is supplied. Use `{"tenant_id": "...", "resource": "pii"}` so a stolen ciphertext for tenant A can't be decrypted as tenant B's payload by a confused caller. Without EncryptionContext, the only protection is that the ciphertext was wrapped by the right key — not what it was _for_.

```python
ct = kms.encrypt(KeyId=key, Plaintext=dek, EncryptionContext={"tenant_id": tid, "resource": "pii"})["CiphertextBlob"]
# later
pt = kms.decrypt(CiphertextBlob=ct, EncryptionContext={"tenant_id": tid, "resource": "pii"})["Plaintext"]   # mismatch → AccessDenied
```

**Hard limits:** AWS KMS `Encrypt`/`Decrypt` payload ≤ **4 KB**. GCP `cryptoKeys.encrypt` payload ≤ **64 KB**. Past these you have no choice but envelope.

## Key types (AWS) — CMK terminology

- **Symmetric (AES-256-GCM)** — default, cheap, used for envelope. Auto-rotation supported (yearly, retains old material for decrypt).
- **Asymmetric RSA / ECC** — for signing + verifying, or for clients you can't authenticate to KMS (give them the public key). Auto-rotation **not supported** — create a new key, dual-write, retire the old one.
- **HMAC** — for keyed-hash signatures (webhook signing, JWT HS256-equivalent at the KMS layer).
- **Multi-region keys** — same key material replicated across regions for active-active. Aliases point at the local replica; failover is DNS, not crypto.

**Aliases** (`alias/payments`) decouple code from key IDs. Always reference aliases in app code; key IDs (`arn:aws:kms:...:key/uuid`) belong in IaC. Rotating to a new key = repoint the alias.

## Signing — asymmetric KMS

```
KMS.Sign(KeyId='alias/release-signing', Message=sha256(payload), MessageType='DIGEST', SigningAlgorithm='RSASSA_PSS_SHA_256')
KMS.Verify(...)  # or distribute the public key and verify client-side without KMS calls
```

| Use case                            | Algorithm                           |
| ----------------------------------- | ----------------------------------- |
| Release artifacts, container images | RSA-PSS-SHA256 or ECDSA-P256        |
| JWT (`alg: RS256`)                  | RSA-PKCS1-v1_5-SHA256               |
| JWT (`alg: ES256`)                  | ECDSA-P256-SHA256                   |
| Webhook payload signing             | HMAC (lower cost, symmetric verify) |

`MessageType='DIGEST'` lets you hash large payloads client-side and only send the 32-byte hash to KMS — required for anything > 4 KB.

## Access control — grants vs key policies vs IAM

Three independent layers, **all must allow** for the call to succeed:

| Layer          | Scope                                            | Use for                                                                                                 |
| -------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| **Key policy** | Per-key (lives ON the key)                       | Foundation — must allow the account's root principal to delegate to IAM, otherwise IAM grants nothing   |
| **IAM policy** | Per-principal                                    | Standard cross-service access (Lambda → KMS, EC2 role → KMS)                                            |
| **Grants**     | Per-key, per-principal, time-bound, programmatic | Temporary delegation (a Lambda spawning a child task; STS-assumed roles needing key access for N hours) |

**Key policy gotcha**: a default-created KMS key has a permissive policy granting the account root. Tighten it. **Removing root's permission is a one-way ticket to an unrecoverable key** — always retain `kms:*` for `root` unless you're 100% sure you'll never need to repair access.

Grants are revocable, attached to the key, and survive IAM changes. Use them for ephemeral access patterns where editing IAM is too coarse.

## Cross-account

Owner account writes the key policy to trust the consumer account's principal. Consumer's IAM policy grants its principal `kms:Decrypt` on the key ARN. **Both required.** S3 bucket encrypted with a KMS key in account A, consumed from account B: A's key policy trusts B's role; B's role has IAM allowing `kms:Decrypt` on the key ARN AND `s3:GetObject` on the bucket.

## Rotation

| Key type                | Rotation                                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| AWS symmetric CMK       | Enable `EnableKeyRotation` — yearly automatic, old material retained indefinitely for decrypt of legacy ciphertext |
| AWS asymmetric          | **Manual** — create new key, switch alias, dual-decrypt grace period, schedule old key deletion                    |
| GCP symmetric CryptoKey | `nextRotationTime` + `rotationPeriod` — automatic, GCP keeps old versions for decrypt                              |
| GCP asymmetric          | Manual version creation + `primary` swap                                                                           |

**Rotation does not re-encrypt existing ciphertext.** Old wrapped DEKs decrypt with the old key version forever (until you delete versions, which is destructive). If you need ciphertext-at-rest re-encrypted post-rotation, you script a re-wrap (`Decrypt` → `Encrypt` with current version) across your storage.

## GCP KMS — what's different

- **Key rings** group keys by location (regional, multi-region, global). A key lives in exactly one ring; moves are impossible.
- **Locations** matter for compliance + latency. `global` cannot be used for high-throughput crypto (no SLA on a global key); pick a regional ring.
- **HSM tier** (`protectionLevel: HSM`) costs more per key per month + per operation; required for FIPS-validated workloads. Software-protected is fine for most.
- **External Key Manager (EKM)** for keys held outside Google (Cloud HSM via partner KMS).
- **IAM is per-key** (or per-key-ring inherited) — no equivalent of AWS grants. Use short-lived service account tokens for ephemerality.

## Cost — where the bill comes from

| Item                                           | AWS           | GCP                       |
| ---------------------------------------------- | ------------- | ------------------------- |
| Key storage                                    | $1/key/month  | $0.06/key-version/month   |
| Symmetric op (Encrypt/Decrypt/GenerateDataKey) | $0.03 / 10k   | $0.03 / 10k               |
| Asymmetric op (Sign/Verify)                    | $0.15 / 10k   | $0.15 / 10k               |
| HSM-backed                                     | +$1/key/month | $1-2.50/key-version/month |

Math: a service doing 1k req/s of KMS Decrypt = 2.6B calls/month = $7,800. Same workload with DEK cache (10k DEKs per hour, decrypted once each on cache miss) = 7.2M calls = $22. **Always cache the DEK.**

## Audit

AWS: every KMS API call lands in **CloudTrail** (data events for `Encrypt`/`Decrypt`/`GenerateDataKey` require explicit enabling — they're not free, but you want them for sensitive keys). Filter by `eventName`, `requestParameters.keyId`, `userIdentity.arn`.

GCP: **Cloud Audit Logs** — `Admin Activity` (key create/destroy/policy changes) on by default; `Data Access` (Encrypt/Decrypt) opt-in per service.

Set alerts: failed decrypt attempts (could be misconfigured client, could be exfil attempt), key deletion scheduled (always a manual review), key policy changed.

## Common pitfalls

- **No rotation enabled** — keys live for years, blast radius on compromise is total
- **KMS as a general secret store** — `Encrypt`/`Decrypt` per request, no caching. Bill arrives, panic ensues. Use envelope.
- **Removing root from key policy** — key becomes unrecoverable; AWS support cannot help
- **Forgetting `EncryptionContext`** — additional authenticated data binds ciphertext to its purpose; without it, ciphertext from `tenant_id=A` can be decrypted in a `tenant_id=B` request and the app can't tell
- **Logging the plaintext DEK** — same severity as logging the wrapped key
- **Cross-account: key policy edited but IAM forgotten** (or vice versa) — both layers required, error message is unhelpful (`AccessDenied` with no diagnostic)
- **Asymmetric key auto-rotation expected** — not supported; new key + alias swap is the path
- **`KMS:GenerateDataKey` granted but `KMS:Decrypt` denied** — app can encrypt new data but cannot decrypt it back; usually a test-env misconfig

## Hand-off

For Vault's Transit secret engine (Vault's equivalent of KMS Encrypt/Decrypt, multi-cloud abstraction): `Skill(secrets-vault)`. For SSE-KMS on object storage: `Skill(storage-object-s3)`. For the broader threat-model framing: `Skill(security)`. For CloudTrail/Cloud Audit Logs in your observability stack: `Skill(observability-essentials)`.

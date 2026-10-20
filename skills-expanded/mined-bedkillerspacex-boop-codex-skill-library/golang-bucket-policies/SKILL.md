---
name: golang-bucket-policies
description: >
  Author, test, and enforce object-storage bucket policies (S3/GCS/Azure) from Go
  tooling: least-privilege principals, public access blocks, encryption, TLS,
  and CI policy tests. Authorized cloud accounts only.
---

# Golang Bucket Policies

## Research grounding

Runbook for **bucket/object-storage policies** managed or validated by **Go**
services and CI jobs (AWS S3, GCS, Azure Blob analogs). Skill id: `golang-bucket-policies`.

## Scope And Authorization

- **In scope:** cloud accounts/projects you own or are authorized to harden.
- **Out of scope:** probing others’ buckets, making buckets public for data leaks, disabling encryption without approval.
- Prefer IaC + policy-as-code; dry-run before apply in prod.
- Redact account IDs in public docs if required; never commit access keys.
- Pair with `code-quality-standards` and secrets hygiene.

## When To Use

- Go control plane applies/validates **S3 bucket policies**, IAM, public access block.
- Preventing `Principal: *` + `s3:GetObject` accidents.
- Enforcing TLS (`aws:SecureTransport`), KMS encryption, VPC endpoint conditions.
- CI job fails PR when policy regresses to public.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| CDN in front of bucket | `golang-cdn-config` / origin shield |
| CMK rotation | `golang-cmk-rotation` |
| Terraform general hardening | `terraform-security-basics` |
| DLP on objects | `golang-cloud-dlp` |
| Code quality | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Controls | Block public ACLs/policies, default SSE-KMS, versioning, access logging |
| Policy tests | `opa`/`checkov`/custom Go tests parsing JSON policy |
| Go AWS SDK | `s3.PutBucketPolicy`, `GetPublicAccessBlock`, account BPA |
| Conditions | `aws:PrincipalOrgID`, `aws:SourceVpce`, `s3:x-amz-server-side-encryption` |
| Pitfalls | Wildcard principal, public list, ACLs enabled, cross-account without condition |

### Policy checklist

| Control | Good state |
| --- | --- |
| Public Access Block | All four true at account+bucket |
| Encryption | SSE-KMS CMK; deny unencrypted PutObject |
| Transport | Deny `SecureTransport=false` |
| Logging | Access logs to locked log bucket |
| Least privilege | App role limited prefixes |

## Workflow

### 1. Confirm scope and success criteria

1. List buckets, data classes, app roles (Go services), shared/public needs.
2. Success: no public buckets unless explicitly approved; TLS+KMS enforced; tests in CI.
3. Change window for prod policy replaces (lockout risk).

### 2. Inventory

```text
aws s3api list-buckets
aws s3api get-public-access-block --bucket "$B"
aws s3api get-bucket-policy --bucket "$B"
aws s3api get-bucket-encryption --bucket "$B"
# GCS analog: gcloud storage buckets describe
```

1. Flag public ACLs, website hosting, missing encryption.
2. Map Go task roles ARNs to required actions/prefixes.

### 3. Baseline

1. Export current policies to git (redacted); note exceptions.
2. Capture who can `s3:PutBucketPolicy`.

### 4. Author and apply least privilege

Example deny non-TLS / require KMS (fragment):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyInsecureTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::example/*", "arn:aws:s3:::example"],
      "Condition": {"Bool": {"aws:SecureTransport": "false"}}
    },
    {
      "Sid": "DenyUnencryptedObjectUploads",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::example/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "aws:kms"
        }
      }
    }
  ]
}
```

Go validation test pattern:

```go
func TestNoPublicPrincipal(t *testing.T) {
    pol := loadPolicy(t, "testdata/bucket.json")
    for _, st := range pol.Statements {
        if st.Effect == "Allow" && principalIsStar(st.Principal) && !st.HasHardCondition() {
            t.Fatalf("public-like allow: %s", st.Sid)
        }
    }
}
```

### 5. Verify with evidence

```text
go test ./internal/bucketpolicy/... -count=1

# After apply (authorized account)
aws s3api get-bucket-policy --bucket "$B"
aws s3api get-public-access-block --bucket "$B"

# Negative tests
# curl http:// should fail; PutObject without SSE-KMS should fail for app role
```

1. Attempt public ACL set should fail when BPA enabled.
2. Confirm Go app still reads/writes required prefixes only.

### 6. Observe and harden

1. Config scanners (Security Hub, SCC) + CI policy tests.
2. Alert on `PutBucketPolicy` / public access changes (CloudTrail).
3. Quarterly access review of cross-account principals.

### 7. Hand off

1. Document break-glass if policy lockout (`golang-break-glass`).
2. Link terraform-security-basics for IaC path.
3. Apply `code-quality-standards` to policy generators.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Public | Explicit exception + ticket | `Principal:*` GetObject for convenience |
| Crypto | CMK + deny unencrypted | SSE-S3 optional |
| IAM | Prefix-scoped app role | `s3:*` on `*` |
| Change | CI test + staged apply | Console click at 2am |
| Logs | Separate log bucket, no app delete | Logs in same writable bucket |

## Output Checklist

- [ ] Bucket inventory + data class
- [ ] Public access block verified
- [ ] TLS and encryption denies in policy
- [ ] Go/CI policy tests green
- [ ] App roles least-privilege confirmed
- [ ] CloudTrail/alerts on policy changes
- [ ] Lockout recovery documented
- [ ] Exceptions with owner + expiry
- [ ] `code-quality-standards` applied
- [ ] Residual risk noted

## Rules

- Authorized cloud accounts only.
- Prefer deny-public by default; public requires risk acceptance.
- Test policies to avoid locking out admin roles—keep emergency path.
- Focus on bucket policies; CDN and DLP are neighbor skills.
- Never commit long-lived cloud keys.

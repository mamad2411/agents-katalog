---
name: storage-object-s3
description: Use when using S3 / MinIO / GCS — presigned URLs, multipart upload, lifecycle, server-side encryption, content-disposition.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [secrets-kms, security, go-essentials, infra-docker-compose, observability-essentials]
---

# Object Storage (S3 / MinIO / GCS)

**Iron Law: never proxy bytes through your app. Presign for client direct-upload/download. Encrypt at rest with SSE-KMS or SSE-S3. Every bucket is private by default; public is an explicit, audited choice.**

**Versions:** AWS S3 API (Signature V4, stable) · MinIO `RELEASE.2025-*` (rolling) · GCS XML/JSON APIs (stable) — _MinIO is API-compatible with S3 SigV4 for everything you'll use; gotchas are around regions, presign paths, and lifecycle dialect._

## SDK picks

| Language   | S3/MinIO                                                                                                                                       | GCS                           |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **Go**     | `github.com/aws/aws-sdk-go-v2/service/s3` (S3, works against MinIO with `BaseEndpoint`); `github.com/minio/minio-go/v7` (MinIO-first, lighter) | `cloud.google.com/go/storage` |
| **Python** | `boto3` (S3), `minio` (MinIO), `smart_open` (read/write as file-like for big files)                                                            | `google-cloud-storage`        |

`minio-go` is the cleaner API for MinIO-only deployments. `aws-sdk-go-v2` works against both — set `BaseEndpoint` to your MinIO URL, `UsePathStyle: true`, region matches MinIO's configured region (often `us-east-1` by convention). Mixing styles silently breaks presigned URLs.

## Presigned URLs — the only sane upload path

Don't stream uploads through your API server. Issue a presigned URL, client PUTs directly to the bucket, your API gets a webhook/poll for completion.

```go
// Go aws-sdk-go-v2 — presign PUT for direct upload
ps := s3.NewPresignClient(client)
req, err := ps.PresignPutObject(ctx, &s3.PutObjectInput{
    Bucket:      aws.String("uploads"),
    Key:         aws.String("u/" + userID + "/" + uuid.NewString()),
    ContentType: aws.String("image/jpeg"),
}, s3.WithPresignExpires(15*time.Minute))
// req.URL → hand to client
```

| Property           | PUT (upload)                                                              | GET (download)                        |
| ------------------ | ------------------------------------------------------------------------- | ------------------------------------- |
| Expiration ceiling | 7 days (SigV4 hard limit)                                                 | 7 days                                |
| Recommended TTL    | 5-15 min                                                                  | 1-60 min (longer for shareable links) |
| Auth on URL        | None — possession of URL = grant                                          | Same                                  |
| Bound headers      | `Content-Type`, `Content-Length`, custom `x-amz-meta-*` must match on PUT | N/A                                   |

**S3 vs MinIO signing differences**:

- MinIO presign requires `UsePathStyle: true` (URL is `https://minio.host/bucket/key?...`, not `https://bucket.minio.host/key?...`)
- Region in the signature must match MinIO's `MINIO_REGION` (otherwise SignatureDoesNotMatch)
- Virtual-host style only works on MinIO with TLS + a wildcard cert (`*.minio.host`); usually not worth it

**Don't issue presigns without expiry** (`Expires=0` defaults to a week — far too long for upload URLs). **Don't put PII in the key** — the path is visible in logs, CDN caches, browser history.

## Multipart upload

Threshold for switching from `PutObject` to multipart: **~100 MB**. SDKs ship managers (`s3manager.Uploader` in v1, `manager.NewUploader` in v2, `Upload_from_file` in boto3) that handle the threshold automatically.

| Knob        | Default                              | Tune when                                                         |
| ----------- | ------------------------------------ | ----------------------------------------------------------------- |
| Part size   | 5 MB (S3 minimum), 16 MB SDK default | Bigger parts (32-100 MB) for fewer requests on multi-GB files     |
| Concurrency | 5                                    | Increase for fast pipes; back off if you saturate your egress     |
| Retry       | exponential, 3 attempts per part     | Failed parts retry independently — the upload as a whole survives |

**Always set up an abort policy**. Multipart uploads that never complete leave parts in storage you can't see in `ListObjects` — you pay for them. Lifecycle rule: `AbortIncompleteMultipartUpload` after 7 days.

For browser direct-multipart-upload you presign each part individually (the protocol is: `CreateMultipartUpload` → presign each `UploadPart` → client uploads parts → presigned `CompleteMultipartUpload`). Library: `evaporate.js` or roll it on `fetch` with retry.

## Downloads — Content-Disposition and Content-Type

Set on upload (in the PUT or via `Copy` after) — these become the headers the client receives on GET:

```
Content-Type: application/pdf
Content-Disposition: attachment; filename="invoice-2026-05.pdf"
```

Without `Content-Disposition` the browser renders inline or downloads with the object key as the filename (often a UUID — useless). `attachment` forces download; `inline` allows in-tab render. Quote the filename if it has spaces; use RFC 5987 (`filename*=UTF-8''...`) for non-ASCII.

For per-download filename overrides, use **response-header overrides** on the presigned GET: `?response-content-disposition=attachment;filename%3D...&response-content-type=application/pdf`. Same object, different download filename per request.

## Server-side encryption — pick one explicitly

| Mode                          | Key managed by                 | Use when                                                                                   |
| ----------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------ |
| **SSE-S3** (`AES256`)         | S3, single account-managed key | Default for low-sensitivity buckets; zero ops                                              |
| **SSE-KMS** (`aws:kms`)       | KMS CMK in your account        | Sensitive data, audit per-decrypt, cross-account access, customer-managed rotation         |
| **SSE-C** (customer-provided) | You ship key on every request  | Rare — you wanted to manage keys but not in KMS                                            |
| **CSE** (client-side)         | You, before upload             | Compliance forces zero-trust of the cloud; see envelope encryption in `Skill(secrets-kms)` |

**SSE-KMS gotcha — bucket-key**: each GET decrypts the object key with KMS = KMS call per request = bill. Enable **S3 Bucket Keys** to reduce KMS calls ~99% (a bucket-level data key is cached for an hour and used for object-level wrapping). This is a checkbox; flip it.

Apply at bucket level via default encryption: `aws s3api put-bucket-encryption --bucket X --server-side-encryption-configuration ...`. Per-object overrides on PUT.

## Lifecycle rules — control the bill

```json
{
  "Rules": [
    {
      "Id": "abort-stale-multipart",
      "Status": "Enabled",
      "AbortIncompleteMultipartUpload": { "DaysAfterInitiation": 7 }
    },
    { "Id": "expire-tmp", "Status": "Enabled", "Filter": { "Prefix": "tmp/" }, "Expiration": { "Days": 1 } },
    {
      "Id": "ia-then-glacier",
      "Status": "Enabled",
      "Filter": { "Prefix": "archive/" },
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER_IR" },
        { "Days": 365, "StorageClass": "DEEP_ARCHIVE" }
      ],
      "NoncurrentVersionExpiration": { "NoncurrentDays": 30 }
    }
  ]
}
```

Lifecycle rules are **bucket-scoped, declarative, free**. The infra-as-code answer to "we have terabytes of stale data" — never write cron jobs to delete S3 objects.

**MinIO lifecycle** supports the same XML dialect (`mc ilm`) but only `Expiration` and `Transition` to local tiers configured via `mc tier add`. Don't expect Glacier transitions on MinIO; you build them with `mc mirror` to a cheap-storage tier.

## CORS — for browser direct-upload

```xml
<CORSRule>
  <AllowedOrigin>https://app.example.com</AllowedOrigin>
  <AllowedMethod>PUT</AllowedMethod>
  <AllowedMethod>GET</AllowedMethod>
  <AllowedHeader>*</AllowedHeader>
  <ExposeHeader>ETag</ExposeHeader>
  <MaxAgeSeconds>3600</MaxAgeSeconds>
</CORSRule>
```

`ExposeHeader: ETag` is required for browser multipart — the JS needs to read the part ETag to call `CompleteMultipartUpload`. Forget it and your multipart silently breaks at the complete step.

**Never `AllowedOrigin: *` on a bucket with presigned uploads** — any origin can drive uploads from a stolen URL. Pin origins.

## Conditional requests

| Header                                     | Semantics                                                                       |
| ------------------------------------------ | ------------------------------------------------------------------------------- |
| `If-Match: "<etag>"`                       | Perform op only if current ETag matches — optimistic concurrency on overwrites  |
| `If-None-Match: "*"`                       | Create-only: fail if object exists (PG-style INSERT ... ON CONFLICT DO NOTHING) |
| `If-Modified-Since`, `If-Unmodified-Since` | Timestamp variants — less precise than ETag                                     |

`If-None-Match: "*"` on PUT is the racefree primitive for "first writer wins" patterns. Native S3 supports this as of Aug 2024; MinIO has supported it longer.

## Versioning + object lock

| Feature                                      | Use for                                                                   |
| -------------------------------------------- | ------------------------------------------------------------------------- |
| **Versioning**                               | Undo deletes/overwrites; ransomware mitigation; audit history             |
| **Object Lock** (governance/compliance mode) | Regulatory retention — even root cannot delete during the lock window     |
| **MFA Delete**                               | Requires MFA on bucket delete operations — paranoid mode for prod buckets |

Versioning + lifecycle (`NoncurrentVersionExpiration`) is how you get "soft delete with TTL" — required for any bucket holding user-uploaded data.

## Common pitfalls

- **Streaming uploads through your API** — your egress bandwidth, your latency, your problem. Presign.
- **Presigned URL with no expiry** (defaults to 7 days) — a leaked URL is a 7-day open door
- **Public-read bucket "for the website assets"** then someone PUTs `.env` to it — bucket policy must deny `s3:PutObject` for the public role even on read-public buckets
- **Body consumed twice on retry** — SDK retries fail because the io.Reader is at EOF; pass `bytes.NewReader` or `Seeker` so SDK can rewind
- **Signing with wrong region** — `SignatureDoesNotMatch` with no useful detail; check `AWS_REGION` env vs bucket region
- **Forgetting bucket-key on SSE-KMS** — KMS bill 100x what it should be
- **No `AbortIncompleteMultipartUpload` lifecycle** — invisible storage cost grows monthly
- **CDN in front of S3 without `Vary: Origin`** on CORS responses — cached response for one origin served to another
- **MinIO virtual-host style** without wildcard TLS — works on `mc` (uses path style) but breaks browser clients
- **Logging the presigned URL** to your structured logger — the URL IS the credential

## Hand-off

For SSE-KMS key management and envelope encryption of large blobs: `Skill(secrets-kms)`. For the upload-flow threat model (CSRF, file-type spoofing, malware): `Skill(security)`. For wiring MinIO into a compose/swarm stack: `Skill(infra-docker-compose)`. For Go SDK idioms: `Skill(go-essentials)`.

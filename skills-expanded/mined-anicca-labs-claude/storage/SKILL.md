---
name: storage
description: File storage on AWS S3 — presigned upload/download URLs, bucket conventions, and multi-tenant object keys. Use when implementing file upload (avatars, CVs, documents), serving private files, or debugging S3 access.
---

Files live in S3; the app never proxies file bytes through its own server. The browser talks to S3 directly using short-lived presigned URLs minted by a route handler — the AWS credentials stay server-side, always.

## The presigned-URL flow

1. Client asks your API for an upload URL: `POST /api/storage/upload-url` with `{ fileName, contentType }`.
2. The route handler authenticates the user, builds the object key, and returns a presigned PUT URL (expiry ≤ 5 minutes).
3. The browser `fetch`es the file straight to that URL with `PUT`.
4. The client tells your API the upload finished; the API stores the object key (never a raw URL) in Postgres.

Downloads of private files mirror it: route handler checks the caller may see the object → presigned GET URL (expiry minutes, not hours) → redirect or return the URL.

```ts
// src/lib/s3.ts
import 'server-only';
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

const s3 = new S3Client({ region: process.env.AWS_REGION });

export function presignUpload(key: string, contentType: string) {
  return getSignedUrl(
    s3,
    new PutObjectCommand({ Bucket: process.env.S3_BUCKET, Key: key, ContentType: contentType }),
    { expiresIn: 300 },
  );
}

export function presignDownload(key: string) {
  return getSignedUrl(
    s3,
    new GetObjectCommand({ Bucket: process.env.S3_BUCKET, Key: key }),
    { expiresIn: 300 },
  );
}
```

Deps: `@aws-sdk/client-s3` and `@aws-sdk/s3-request-presigner`. Env: `AWS_REGION`, `S3_BUCKET`, plus credentials via the standard AWS chain (`AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` locally; on Vercel set them as env vars — scope the IAM user to this one bucket).

## Multi-tenant object keys

The key encodes ownership so authorization is checkable from the key alone:

```
{orgId}/{entity}/{uuid}-{sanitizedFileName}
  e.g. 7f3a…/talent-cv/9c1e…-resume.pdf
```

Rules:

- **Never** derive the key from client input alone — the route handler builds it from the authenticated session's org, and validates on download that the requested key's `orgId` prefix matches the caller's org. This is the S3 equivalent of the tenant-isolation rule in the database.
- Sanitize file names (strip path separators, control chars); cap `contentType` to an allowlist per upload kind (images for avatars, pdf/doc for CVs).
- The bucket stays **private** (Block Public Access on). Anything that must be truly public goes through a separate public bucket or CDN, never by loosening the private one.
- Store the object key in Postgres; presign at read time. Presigned URLs in the database are expired URLs.

## Debugging

- `aws s3 ls s3://$S3_BUCKET/prefix/ --profile <profile>` — check what actually landed.
- 403 on PUT usually means the presigned `ContentType` doesn't match the request header the browser sent.
- CORS: the bucket needs a CORS rule allowing `PUT`/`GET` from the app origins (localhost + the Vercel domains) before browser uploads work.

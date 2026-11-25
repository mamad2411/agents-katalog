---
name: backend-files
description: "Files on the server: uploads straight to object storage with presigned URLs, validating type by content and size, scanning, processing images and documents in jobs, private and public buckets, signed download URLs, safe filenames and content headers, large and resumable uploads, deletion and lifecycle rules, quotas, and S3-compatible providers. Read before accepting, storing or serving user files."
---

# Files

The generated upload handler reads the whole file into memory, trusts the
extension and the `Content-Type` the browser sent, saves it under the user's
own filename in `public/uploads/`, and serves it back from the app's domain,
so an `.html` or `.svg` upload runs as a script on your site. The files
vanish on the next deploy and are never deleted otherwise. This skill gives
the upload flow, the checks, the storage layout and the serving rules. One
part of the backend; the whole is in the `backend` skill, the short security
rules in `backend-security`.

## 1. Where files live

- Object storage, never the app server's disk in production: disks vanish on
  redeploy, differ between instances and fill up. S3, Cloudflare R2, Google
  Cloud Storage, Backblaze B2 or another S3-compatible service; in
  development an S3-compatible container (MinIO) in `docker compose`, so the
  code path is the same.
- The database holds the metadata, the bucket holds the bytes:

```sql
CREATE TABLE files (
  id            uuid PRIMARY KEY,               -- UUIDv7 made by the app
  tenant_id     bigint NOT NULL,
  owner_id      bigint NOT NULL REFERENCES users (id),
  storage_key   text NOT NULL UNIQUE,
  original_name text NOT NULL,                  -- display only
  content_type  text NOT NULL,                  -- detected, not claimed
  size_bytes    bigint NOT NULL CHECK (size_bytes >= 0),
  sha256        text,
  status        text NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'scanning', 'ready', 'rejected', 'deleted')),
  created_at    timestamptz NOT NULL DEFAULT now()
);
```

- Keys: `{tenant}/{purpose}/{uuid}.{ext}` (`t12/invoices/0192f1c4-7b0e.pdf`),
  the extension taken from the detected type; nothing the user typed is ever
  part of a key. Uploads land under `tmp/` and move to their final key when
  confirmed (a server-side copy), so a lifecycle rule clears abandoned ones.
- One private bucket for user files; a separate public bucket (or a CDN in
  front) only for truly public assets, so a policy mistake on one cannot
  expose the other.

## 2. Direct uploads with presigned URLs

The bytes go from the client to the bucket, not through the app: no memory
spikes, no request timeouts, no body limits to raise.

1. The client asks: `POST /uploads` with the name, size and type it claims,
   and what the file is for.
2. The server checks the claim against that purpose's rules (allowed types,
   maximum size, the quota), inserts a `files` row as `pending` with a key it
   chose, and answers with a presigned URL valid for 5 to 15 minutes.
3. The client uploads to the bucket.
4. The client calls `POST /uploads/{id}/complete`. The server checks the row
   is the caller's, `HeadObject` shows the object and its real size, reads
   the first bytes to detect the type (section 3), copies the object from
   `tmp/` to its final key, and queues scanning and processing
   (`backend-jobs`). The bucket's event notifications (S3 to SQS or
   EventBridge, R2 to Queues) can trigger the same step.

A presigned POST enforces size and type in its policy; a presigned PUT does
not, so the size is checked on completion either way:

```ts
import { createPresignedPost } from "@aws-sdk/s3-presigned-post";

const { url, fields } = await createPresignedPost(s3, {
  Bucket: config.UPLOADS_BUCKET,
  Key: file.storageKey,
  Conditions: [
    ["content-length-range", 1, 10 * 1024 * 1024], // 10 MB for this purpose
    ["eq", "$Content-Type", file.contentType],
  ],
  Fields: { "Content-Type": file.contentType },
  Expires: 600, // seconds
});
```

- Python: `s3.generate_presigned_post(...)` with the same conditions; Go:
  `s3.NewPresignClient(client).PresignPutObject(...)`. Laravel's
  `Storage::temporaryUploadUrl()` and Rails's Active Storage direct uploads
  are this flow already: use them.
- Cloudflare R2 supports presigned `PUT` (and `GET`, `HEAD`, `DELETE`) but
  not presigned `POST`: sign a `PUT` with the `ContentType`, and check the
  size on completion.
- The bucket's CORS rules allow your origins, the method used (`PUT` or
  `POST`) and the `Content-Type` header, and expose `ETag` (multipart
  uploads need it).
- Recent AWS SDKs add checksum headers by default that some S3-compatible
  services and browser uploads do not send. When presigned uploads fail with
  signature or checksum errors, build the JavaScript client with
  `requestChecksumCalculation: "WHEN_REQUIRED"` and
  `responseChecksumValidation: "WHEN_REQUIRED"`.
- Small files through the app are fine on a server you run (an avatar under
  5 MB): streamed, with a body limit on that route only, and the same checks.

## 3. Checking what arrived

- Size limits per purpose, in config: avatars 5 MB, photos 10 to 20 MB,
  documents 25 to 50 MB; above that, multipart (section 7). A zero-byte file
  is refused.
- The type comes from the content, not the name or the header: the magic
  bytes at the start of the file (`file-type` in Node, `filetype` or
  `python-magic` in Python, `http.DetectContentType` in Go for a small set,
  Marcel in Rails, `finfo` in PHP), checked against an allow-list per
  purpose (`image/jpeg`, `image/png`, `image/webp` for photos,
  `application/pdf` for invoices). The stored type is the detected one; a
  mismatch with the claim is refused.
- Refused unless the feature truly needs them: HTML, XML, JavaScript,
  executables, archives (zip bombs, paths inside), office files with macros.
  SVG is a script container: accept it only when needed, sanitised
  (DOMPurify with its SVG profile) or rasterised, and served per section 5.
- Images are re-encoded (decoded and written anew), which drops EXIF data
  such as GPS location and anything hidden after the image data. Cap the
  pixel count against decompression bombs: sharp's `limitInputPixels`
  (50 million, section 4), `Image.MAX_IMAGE_PIXELS` in Pillow.
- Files other people will download are scanned first: ClamAV (`clamd`, with
  `freshclam` keeping signatures current) in a job, or the provider's
  scanner (GuardDuty Malware Protection for S3). While `scanning`, only the
  uploader sees the file; an infected one becomes `rejected`, moves to a
  quarantine prefix, and is never served.
- A SHA-256 computed while processing, for integrity and deduplication.

## 4. Processing in jobs

- Thumbnails, resizing, conversion, text extraction and PDF previews run in
  a background job after the upload is confirmed, never in the request. The
  job is idempotent: it writes derived files under fixed keys
  (`{uuid}/w640.webp`) and can run twice.
- Images with libvips (sharp in Node, `pyvips`, Active Storage's vips
  processor) rather than ImageMagick: faster and far lighter on memory.
  Widths of 320, 640, 1280 and 2048px in WebP or AVIF, quality 75 to 82:

```ts
const out = await sharp(input, { limitInputPixels: 50_000_000 })
  .rotate()                                          // apply EXIF orientation
  .resize({ width: 1280, withoutEnlargement: true })
  .webp({ quality: 80 })
  .toBuffer();                                       // metadata dropped by default
```

- Or resize on the fly with an image service (imgproxy, Cloudflare Images,
  the CDN's resizer) behind signed URLs, so nobody can request thousands of
  giant variants, with the results cached at the CDN.
- Untrusted PDFs and office files are parsed in an isolated worker with a
  time and memory limit (poppler's `pdftoppm`, LibreOffice headless or
  Gotenberg in its own container), never in the web process: parsers of
  complex formats have long histories of vulnerabilities.
- Video goes to a video service (Mux, Cloudflare Stream) or an ffmpeg job.

## 5. Serving files

- Private by default. The app checks that the caller may see the file (the
  same ownership rule as the record it belongs to, `backend-auth`), then
  redirects (`302`) to a signed GET URL valid for 1 to 15 minutes. A signed
  URL is a bearer credential: short-lived, never logged, never put in a page
  a CDN caches.
- The headers are yours, not the uploader's:

```http
Content-Type: application/pdf
Content-Disposition: attachment; filename="invoice-812.pdf"; filename*=UTF-8''invoice-812.pdf
X-Content-Type-Options: nosniff
Content-Security-Policy: sandbox
```

  `attachment` for anything that is not an image you produced or a PDF you
  mean to show inline. With S3 or R2, store them on the object at upload, or
  set them in the signed URL (`ResponseContentDisposition`,
  `ResponseContentType`).
- User content is served from a separate domain (`usercontent.example.net`),
  never the app's origin, so a file that slips through cannot read the app's
  cookies or call its API as the viewer.
- Public assets (product photos, a published avatar) sit behind a CDN under
  keys that change with the content, cached for a year
  (`public, max-age=31536000, immutable`, `backend-caching`).
- Downloads through the app are streamed from the bucket to the response
  with `Range` support, never read whole into memory; for large files the
  redirect is better, so the app carries no bytes at all.

## 6. Filenames

- The original name is metadata, for display and the download's filename:
  path parts and control characters stripped, cut to 255 bytes, escaped
  wherever it is shown, and encoded in the header (`filename*` with UTF-8
  percent-encoding per RFC 6266, plus an ASCII `filename` fallback).
- It never becomes a key or a path on disk (`backend-security`).

## 7. Large and resumable uploads

- Above about 100 MB, or on unreliable mobile networks, S3 multipart: the
  server creates the upload and presigns a URL per part; the client sends
  parts of 5 MiB to 5 GiB (at most 10,000 parts), 3 to 6 at a time,
  retrying a failed part alone; the server completes the upload with the
  parts' ETags.
- Uppy (`@uppy/aws-s3`, multipart on) handles the client side. Resumable
  uploads to your own server use the tus protocol (tusd, `tus-js-client`).
- A lifecycle rule aborts incomplete multipart uploads after 1 to 7 days:
  their parts are billed until then and do not show in a normal listing.

## 8. Deletion and lifecycle

- Deleting a record deletes its files: the row turns `deleted`, and a job
  removes the object and its variants after a grace period for undo (a day
  to a month). Deleting an account deletes its files (GDPR, UU PDP).
- Orphans: `pending` rows older than a day and objects with no row are
  removed by a scheduled job; for big buckets compare against the provider's
  inventory report (S3 Inventory) instead of listing everything.
- Bucket lifecycle rules: expire `tmp/` after 1 day, abort incomplete
  multipart uploads, expire noncurrent versions after about 30 days on a
  versioned bucket, move cold files to a cheaper storage class where one
  exists.
- Files that cannot be recreated (invoices, contracts, originals) get
  versioning or replication to a second bucket, and a restore that has been
  tested, like a database backup.

## 9. Quotas and abuse

- Bytes used per user or tenant, kept in a counter updated in the same
  transaction as the file row: checked when the upload is requested (the
  claimed size) and corrected on completion (the real size).
- Rate limits on upload requests (`backend-security`), a cap on pending
  uploads per user, URLs that expire.
- Completion and download check the tenant and owner of the row, so nobody
  confirms or reads an object under someone else's key.

## 10. Providers and the storage module

| Provider | Notes |
|---|---|
| AWS S3 | the reference API; Block Public Access on; objects encrypted by default |
| Cloudflare R2 | S3 API without egress fees; region `auto`; endpoint `https://{account_id}.r2.cloudflarestorage.com`; no presigned POST |
| Backblaze B2, Wasabi, DigitalOcean Spaces | S3 API, cheaper storage; check which S3 features each has |
| Google Cloud Storage | its own V4 signed URLs; S3 interoperability through HMAC keys |
| Azure Blob Storage | not S3: SAS tokens instead of presigned URLs |
| MinIO or another S3-compatible server | development and self-hosting; `forcePathStyle: true` in the AWS SDK |

- One storage module (`storage.ts`, `storage.py`) wraps the SDK with
  `presignUpload`, `head`, `signedDownloadUrl` and `remove`; the rest of the
  code never builds keys or calls the SDK, so changing providers is one file.
- The app's credentials come from the environment with the least rights:
  put, get and delete in its own bucket, nothing else, no policy changes.

## Check it

- Upload each allowed type, then a renamed file (`page.html` saved as
  `photo.jpg`), an SVG containing a script, a file one byte over the limit
  and an empty file: only the first is accepted, each refusal says why.
- An expired presigned URL, and one reused for another key: refused.
- A private file's link opened signed out and as another user: `403` or
  `404`, never the bytes. `curl -sI` on a download shows the `content-type`,
  `content-disposition` and `x-content-type-options` you set.
- `aws s3 ls s3://bucket/t12/ --recursive | head` (with `--endpoint-url`
  for R2 or MinIO): keys are yours, nothing private in a public bucket.
- Delete a record, run the jobs: the object and its variants are gone.
- Upload a large file through any route the app streams: its memory stays
  flat.

## Avoid

Files on the server's disk; the user's filename in a key or a path;
trusting the extension or the browser's `Content-Type`; uploads served from
the app's own domain with their own type; public buckets for private files;
signed URLs that live for days or end up in logs; whole files read into
memory; images processed in the request; SVG and HTML accepted like photos;
files that outlive their record; incomplete multipart uploads billed
forever; SDK calls and key building scattered through the code.

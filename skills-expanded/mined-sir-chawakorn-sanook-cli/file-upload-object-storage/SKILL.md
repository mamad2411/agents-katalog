---
name: file-upload-object-storage
description: Implements secure file/image/video upload to object storage via short-lived presigned URLs or POST policies, with content-type + size validation, magic-byte verification, non-guessable tenant-scoped key namespacing, multipart/resumable transfer, private buckets with signed-URL access, and post-upload scan/transcode + lifecycle cleanup.
when_to_use: User is adding file/image/video upload, generating presigned/direct upload URLs, handling large/resumable/multipart transfers, validating uploads, controlling object access, or serving via signed URLs/CDN. Distinct from auth-jwt-session (who the caller is — this consumes that identity) and secrets-management (storing the bucket credentials themselves).
---

## When to Use

Reach for this skill when bytes flow **from a client into a bucket** and back out under access control:

- "Let users upload an avatar / document / video to object storage (S3, GCS, R2, Azure Blob)"
- "Generate a presigned URL / POST policy so the browser uploads direct-to-bucket"
- "Handle large/resumable uploads, multipart with retry"
- "Validate uploaded files — block executables, cap size, check the real type"
- "Keep these files private and serve them with a time-limited signed URL / behind a CDN"
- "Scan/resize/transcode after upload; clean up orphaned objects when a record is deleted"

NOT this skill:
- Deciding *who* may request an upload URL or read an object → auth-jwt-session (this skill consumes the authenticated identity; it does not establish it)
- Where the bucket's own access keys / service-account JSON live → secrets-management
- Broad storage-class/egress cost modeling across services → cloud-cost-optimize (this covers only per-object lifecycle/tiering for uploads)
- Front-end image perf (responsive `srcset`, lazy-load, format) → optimize-core-web-vitals
- Validating the *other* form fields around the file → build-form-validation
- App-response caching to cut load → caching-strategy (CDN here is for object delivery, not API responses)

## Steps

1. **Default: client uploads direct-to-bucket via a short-lived presigned credential — never stream bytes through your app server.** Proxying uploads burns app memory/bandwidth and adds a hop. Your server only mints a credential and records metadata. Pick the credential type:

   | Mechanism | Use when | Constrains |
   |---|---|---|
   | **Presigned POST policy** (S3 `create_presigned_post`, R2 same) | Browser/HTML form, single file, **want server-enforced size + type** | `Content-Type`, `content-length-range`, exact key or key prefix, expiry |
   | Presigned PUT URL | Simple programmatic single-shot PUT | content-type + expiry only (no size cap pre-upload) |
   | **Multipart presigned** (`create_multipart_upload` + per-part `upload_part` URLs) | File > ~100 MB, flaky networks, resumable | per-part, parallel, retryable |
   | GCS resumable session (`x-goog-resumable:start`) / Azure Block Blob (`PutBlock`+`PutBlockList`) | GCS/Azure large or resumable | session URL + range |

   Default for web uploads = **presigned POST policy** because it is the only one that enforces a size ceiling *before* bytes land. Expiry: **5 minutes** (`Expires=300`). Generate per-upload, single-use.

2. **Validate on the boundary — twice. Never trust client-supplied MIME or extension.** A `.jpg` can be a polyglot HTML/JS or a zip bomb. Enforce in two places:
   - **In the policy (pre-upload, hard ceiling):** size via `content-length-range` and a `Content-Type` allowlist condition. Example POST policy conditions:
     ```python
     fields = {"Content-Type": content_type, "x-amz-meta-owner": str(user_id)}
     conditions = [
         {"bucket": BUCKET},
         ["starts-with", "$key", f"tenants/{tenant_id}/uploads/"],
         {"Content-Type": content_type},          # must equal the one you signed
         ["content-length-range", 1, 10 * 1024 * 1024],  # 1 B .. 10 MiB
     ]
     post = s3.generate_presigned_post(BUCKET, key, Fields=fields,
                                       Conditions=conditions, ExpiresIn=300)
     ```
     S3 rejects with `403 EntityTooLarge` / `AccessDenied` if the upload violates the policy — the server never sees the oversized body.
   - **Server-side after upload, by magic bytes:** on the upload event (step 6), read the **first 256–512 bytes** and sniff the real type (`file --mime-type -`, `python-magic`, Go `net/http.DetectContentType`, Node `file-type`). If the sniffed type is not in your allowlist, delete the object and mark the record `rejected`. Allowlist concrete types (`image/jpeg image/png image/webp image/gif application/pdf video/mp4`) — never a denylist.

3. **Design the key/namespace: non-guessable, tenant-scoped, no user-controlled path segments.** Pattern: `tenants/{tenant_id}/{kind}/{uuidv4}{ext}` — e.g. `tenants/9f3.../avatars/0b1e7d2a-...-.webp`.
   - Use a **server-generated UUIDv4/ULID** as the object id; never the raw filename. This blocks enumeration *and* path traversal (`../../etc/passwd`, leading `/`, `%2e%2e`).
   - Sanitize/extension only: strip everything but a known-good extension derived from the **validated** type, not the client name.
   - Store the real filename, owner, sniffed content-type, size, and `status` in **your DB** — the bucket is a blob store, not a database. The DB row is the source of truth; the object is referenced by key.
   - Same prefix discipline lets one IAM policy / lifecycle rule target `tenants/*/uploads/`.

4. **Large files: multipart/resumable with part retry + an abort-incomplete lifecycle rule.** Parts: **8–16 MiB** each (S3 min 5 MiB except last; max 10,000 parts). Upload parts in parallel (3–4 at a time), retry a failed part by re-PUTting just that part number, then `complete_multipart_upload` with the `{PartNumber, ETag}` list. **Failed/abandoned multipart uploads keep billable orphaned parts forever** — add the lifecycle rule:
   ```json
   { "Rules": [{ "ID": "abort-incomplete-mpu", "Status": "Enabled",
       "Filter": { "Prefix": "tenants/" },
       "AbortIncompleteMultipartUpload": { "DaysAfterInitiation": 1 } }] }
   ```
   GCS resumable / Azure uncommitted blocks need the equivalent (resumable sessions expire in 7 days; Azure uncommitted blocks GC after 7 days).

5. **Access control: private buckets by default; serve via time-limited signed URLs.** Block all public access (`PublicAccessBlockConfiguration` all-true on S3; Uniform bucket-level access + no `allUsers` on GCS). Two-bucket split:
   - **`public-assets`** bucket/prefix → genuinely public, immutable, cacheable (logos, released static media) → fronted by CDN, long `Cache-Control: public, max-age=31536000, immutable`.
   - **`private-data`** bucket → user docs, originals → **never public**. Read access = a signed GET URL minted **per request after an authz check**, short expiry (**60–300 s**). For many objects on one page (galleries) use **signed cookies** (CloudFront) / signed-URL prefix to avoid signing each object.
   The authz check (does this user own/may-read this key?) lives in **your** code before signing — the signature only proves the URL wasn't tampered with, not that the requester is entitled. That ownership decision is auth-jwt-session territory; this skill just enforces it at sign time.

6. **Post-upload pipeline: react to the upload event, go `pending → ready`.** Insert the DB row as `status=pending` when you mint the URL. Fire on the storage event (**S3 → EventBridge/SNS/SQS or Lambda; GCS → Pub/Sub; Azure → Event Grid**) — do **not** trust a client "I'm done" callback as the only signal. In the handler: (a) magic-byte validate (step 2), (b) AV scan (e.g. ClamAV / `clamdscan`) for any user-shared file, (c) derive — resize/strip-EXIF for images, transcode for video (`ffmpeg` → HLS/MP4), (d) on success flip `status=ready`, on failure delete object + `status=rejected`. Clients only ever see/serve `ready` objects.

7. **Lifecycle & cost: expire temp uploads, tier cold objects, CDN the hot reads.** Separate a `tmp/` prefix for unconfirmed uploads with a **1-day expiry** lifecycle rule (the orphan from an abandoned form never lingers). Transition originals not read in 30/90 days to Infrequent-Access / Nearline / Cool. Serve hot public reads through a CDN (CloudFront/Cloudflare/Fastly) with an origin-access identity so the bucket stays private to the world but readable by the CDN.

8. **Cleanup orphaned objects on record delete.** Deleting the DB row must enqueue a delete of its object key(s) — including derived renditions/thumbnails. Do it **transactionally-ish**: delete the row, then on commit enqueue an idempotent delete job (retry-safe; a missing key is success). A nightly **reconcile** sweep (list bucket prefix vs DB keys) catches drift in both directions — objects with no row, rows with no object.

## Common Errors

- **Proxying upload bytes through the app server.** OOMs on large files, doubles bandwidth. Mint a presigned credential; let the client PUT/POST straight to the bucket.
- **Trusting `Content-Type`/extension from the client.** Spoofable; enables stored-XSS via a `.jpg` that's really HTML served inline. Verify magic bytes server-side and serve user files with `Content-Disposition: attachment` + `X-Content-Type-Options: nosniff`.
- **Putting the user's filename in the key.** Invites path traversal and enumeration. Key on a server UUID; keep the display name in the DB.
- **Public bucket / public ACL "just to make it work."** Leaks every object and lets anyone overwrite. Block public access; use signed URLs. A `?`-less object URL that loads in incognito is a finding.
- **Presigned URL with hours/days expiry.** A leaked long-lived URL is a permanent backdoor. Cap at minutes; mint per request.
- **No `content-length-range` in the POST policy.** Client uploads a 5 GB file and you pay for it. Always set a size ceiling in the policy, not just a client-side JS check.
- **Authz only at URL-mint time, never re-checked.** Object IDs leak in logs/referers; a stale signed URL outlives the user's permission. Keep expiry short and re-authorize on every mint.
- **Forgetting `AbortIncompleteMultipartUpload`.** Failed multipart uploads accrue invisible, billable parts indefinitely. Add the 1-day abort rule on day one.
- **Marking `ready` before the scan/transcode finishes.** Serves unscanned malware or a half-written object. Flip to `ready` only from the post-upload handler.
- **Deleting the DB row but not the object (or vice-versa).** Orphans cost money and leak data; missing objects 404 live records. Enqueue an idempotent object delete on row delete + run a reconcile sweep.
- **CORS not configured on the bucket.** Browser direct-PUT/POST fails preflight. Set `AllowedMethods` (`PUT POST`), `AllowedOrigins` (your exact origins, not `*`), and expose `ETag` for multipart.
- **Same bucket for public assets and private originals.** One misconfig exposes everything. Split public-asset and private-data buckets with different policies.

## Verify

1. **Direct-to-bucket works:** client obtains a presigned POST/PUT and uploads with no bytes touching the app server (confirm app logs show only the mint call, not the body).
2. **Size ceiling enforced server-side:** upload `max+1` bytes → bucket rejects (`403 EntityTooLarge`/policy violation); the body never reaches you. A client that disables the JS size check still cannot exceed the policy.
3. **Type spoof blocked:** upload an HTML/EXE file renamed `.png` with `Content-Type: image/png` → passes the policy but the magic-byte check deletes it and sets `status=rejected`; it is never served `ready`.
4. **Key is non-guessable + traversal-proof:** the stored key is a server UUID under `tenants/{id}/...`; a key containing `../`, a leading `/`, or the raw filename is rejected/never produced.
5. **Privacy:** the raw object URL (no signature) returns `403` in an incognito session; a freshly signed URL returns `200`; the **same** URL after `Expires` returns `403`.
6. **Cross-tenant denied:** user A's signed-URL request for user B's key fails the authz check at mint time (no URL issued), not just at read time.
7. **Resumable:** kill the network mid-multipart, resume → only missing parts re-upload, `complete` succeeds, final object bytes match the source checksum (`s3 cp` then `sha256sum`).
8. **Orphan hygiene:** an abandoned multipart upload is gone after the abort window; a `tmp/` object expires per its 1-day rule; deleting a record removes its object + renditions (verify via `aws s3 ls`/reconcile sweep shows no drift).
9. **Post-upload state machine:** a fresh upload is `pending`, becomes `ready` only after scan+derive complete, and a malicious/corrupt file ends `rejected` with the object deleted.

Done = uploads go direct-to-bucket under a ≤5-min single-use credential with a server-enforced size cap and magic-byte type check; objects are private, tenant-scoped, non-guessable, and readable only via short-lived signed URLs after an ownership check; large uploads resume and abandoned parts auto-abort; and every record delete (plus a reconcile sweep) leaves zero orphaned objects.

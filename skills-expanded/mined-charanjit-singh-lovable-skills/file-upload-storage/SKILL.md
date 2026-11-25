---
name: file-upload-storage
description: >-
  Use when implementing file uploads, avatars, attachments, or Supabase Storage
  buckets with signed URLs. Not for text-only forms or external CDNs unless
  integrating upload to Storage.
---

# File upload and Supabase Storage

## Bucket setup

- Private buckets for user files; public only for truly public assets.
- RLS policies on `storage.objects`: users upload/read only their prefix (`auth.uid()` in path).
- Max file size and MIME allowlist in policy or validated client-side before upload.

## Upload flow

```ts
const MAX_BYTES = 5 * 1024 * 1024;
const ALLOWED = ["image/jpeg", "image/png", "image/webp"];

if (!ALLOWED.includes(file.type)) throw new Error("Unsupported file type");
if (file.size > MAX_BYTES) throw new Error("File is too large");

const ext = file.name.split(".").pop()?.toLowerCase() ?? "bin";
const path = `${userId}/${crypto.randomUUID()}.${ext}`;

const { error } = await supabase.storage.from("avatars").upload(path, file, {
  upsert: false,
  contentType: file.type,
  cacheControl: "3600",
});
if (error) throw error;
```

- Validate type **and** size before upload — never trust extension alone.
- Show progress and error toasts.
- On success, save the **storage path** (not the signed URL) in the DB.

## Display

- Private files: `createSignedUrl(path, expiresIn)` short TTL, or serve via edge function.
- Public bucket: `getPublicUrl(path)`.

## UI

- Drag-drop zone + file input; preview for images.
- Clear remove/replace affordance on profile flows.

## Avoid

- Public bucket for PII documents.
- Trusting client-only path without RLS (`../other-user/file`).
- Storing huge files without size limits.

## Checklist

- [ ] Storage RLS policies match path convention.
- [ ] DB column stores path; URLs generated on read.
- [ ] Loading/error on upload button.

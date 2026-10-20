---
name: volcano-storage
description: Use for file and object storage in Volcano apps, including uploads, downloads, photo galleries, file sharing, buckets, ownership-aware paths, public or private files, visibility, and resumable uploads.
---
# Volcano Storage Skill

## Role
Implement secure storage flows with explicit bucket, path, and access-control intent. This skill is self-contained: bucket selection, every file operation, public/private semantics, resumable uploads, and error handling are embedded.

## Workflow
1. Select a bucket and design ownership-aware paths.
2. Implement upload/download/list/remove using canonical APIs.
3. Keep files private by default; explicitly justify any public flag.
4. For files >100 MB or unreliable connections, use resumable uploads.

## Buckets and Paths

### Bucket selection
```ts
const avatars = volcano.storage.from('avatars');
const documents = volcano.storage.from('documents');
```
Create buckets with the CLI before referencing them — `volcano storage bucket create <name> [--allowed-mime-type <type>] [--file-size-limit <bytes>]` (local) / `volcano cloud storage bucket create ...` (cloud); `volcano storage bucket list|get` to check what already exists. `volcano-config.yaml`'s `buckets` section (see `volcano-platform`) only manages policies on buckets that already exist — it never creates or deletes them.

**A new bucket already has working owner-scoped RLS policies — do NOT hand-write them for the common case.** `bucket create` installs defaults (`default-auth-insert`, `default-auth-select-own`, `default-auth-update-own`, `default-auth-delete-own`): any authenticated user can upload, and each user can read/update/delete only their own objects. So a private, per-user upload/list app needs **zero** policy setup — just create the bucket and upload under owner-scoped paths (below). Reach for `volcano storage policy create` only for *non-default* access (public read, cross-user sharing) — see "Custom policies". Creating owner-scoped policies by hand is the most common storage mistake: they already exist, and a wrong definition denies the very uploads it was meant to allow.

### Path conventions (recommended)
```
avatars/<userId>/profile.jpg
documents/<userId>/reports/<year>/<filename>.pdf
projects/<projectId>/assets/<assetType>/<filename>
```
Avoid: random/timestamp-only paths (`file-${Date.now()}.pdf`).

## Upload

### Basic
```ts
const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
const file = fileInput.files![0];

const { data, error } = await volcano.storage
  .from('avatars')
  .upload(`${user.id}/profile.jpg`, file);
// data: { name, size, mime_type, ... }
```

### With content type
```ts
await volcano.storage
  .from('documents')
  .upload('reports/annual-2024.pdf', file, { contentType: 'application/pdf' });
```

### From Blob / ArrayBuffer
`upload()` accepts a **`File`, `Blob`, or `ArrayBuffer`** only. A Node `Buffer`
(or any `Uint8Array`) is **rejected** with `Invalid file body type. Expected
File, Blob, or ArrayBuffer` — the common trap in server Functions, where an
image/PDF/QR generator hands you a Node `Buffer`. Wrap it in a `Blob`.
```ts
const blob = new Blob(['hello'], { type: 'text/plain' });
await volcano.storage.from('uploads').upload('notes/hello.txt', blob);

// In a Function: generators return a Node Buffer — wrap it, do NOT pass it directly.
// (QRCode here is the third-party `qrcode` npm package — add it to package.json so it bundles into the function.)
const png = await QRCode.toBuffer('https://example.com'); // Node Buffer
await volcano.storage.from('uploads').upload('codes/qr.png', new Blob([png]), {
  contentType: 'image/png',
});
```

## Download

### Basic
```ts
const { data: blob, error } = await volcano.storage
  .from('documents')
  .download('reports/annual-2024.pdf');

const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'annual-2024.pdf';
a.click();
URL.revokeObjectURL(url);
```

### Display in browser (image)
```ts
const { data: blob } = await volcano.storage.from('avatars').download(`${userId}/profile.jpg`);
imgEl.src = URL.createObjectURL(blob);
```

### Partial download (range)
```ts
const { data: blob } = await volcano.storage
  .from('documents')
  .download('large-file.zip', { range: 'bytes=0-1023' });
```

## List

### Whole bucket
```ts
const { data: files, error } = await volcano.storage.from('uploads').list();
// file fields: name, size, mime_type, is_public, created_at, owner_id, public_url?
```

### With prefix
```ts
const { data: files } = await volcano.storage.from('uploads').list('images/');
const { data: mine } = await volcano.storage.from('documents').list(`${userId}/`);
```

### Paginated
```ts
const { data: files, nextCursor } = await volcano.storage
  .from('uploads')
  .list('', { limit: 100 });

if (nextCursor) {
  const { data: more } = await volcano.storage
    .from('uploads')
    .list('', { limit: 100, cursor: nextCursor });
}
```

## Delete
```ts
// Single
await volcano.storage.from('uploads').remove('old-file.txt');

// Multiple
const { data } = await volcano.storage.from('uploads').remove([
  'temp/file1.txt',
  'temp/file2.txt',
  'temp/file3.txt',
]);
// data.deleted is the list of removed paths
```

## Move and Copy
```ts
await volcano.storage.from('documents').move('drafts/report.pdf', 'published/report.pdf');
await volcano.storage.from('documents').copy('templates/invoice.pdf', 'invoices/2024-001.pdf');
```

## Public vs Private

### Default: private
Files require an authenticated session to download.

### Toggle visibility
```ts
const { data } = await volcano.storage
  .from('avatars')
  .updateVisibility(`${userId}/profile.jpg`, true);
// data.public_url present when true

await volcano.storage
  .from('avatars')
  .updateVisibility(`${userId}/profile.jpg`, false);
```

### Get public URL (does NOT verify file is actually public)
```ts
const { data } = volcano.storage.from('avatars').getPublicUrl(`${userId}/profile.jpg`);
// data.publicUrl: 'https://api.<project>.volcano.dev/public/<project-id>/avatars/<path>'
```
Public URLs require no auth, work in any browser, are CDN-friendly, and 403 if the file is later made private.

## Resumable Uploads
Use for files >100 MB or unreliable networks.

### Simple resumable upload
```ts
const { data, error } = await volcano.storage
  .from('uploads')
  .uploadResumable('large-video.mp4', file, {
    onProgress: (uploaded, total) => {
      const pct = Math.round((uploaded / total) * 100);
      progressBar.value = pct;
    },
  });
```

### Manual session control
```ts
// 1. Create session
const { data: session } = await volcano.storage
  .from('uploads')
  .createUploadSession('large-video.mp4', {
    totalSize: file.size,
    contentType: 'video/mp4',
    partSize: 10 * 1024 * 1024, // 10 MB parts
  });
// session: { session_id, total_parts, part_size }

// 2. Upload each part
for (let i = 1; i <= session.total_parts; i++) {
  const start = (i - 1) * session.part_size;
  const end = Math.min(start + session.part_size, file.size);
  const partData = file.slice(start, end);
  const { error } = await volcano.storage
    .from('uploads')
    .uploadPart('large-video.mp4', session.session_id, i, partData);
  if (error) break; // can retry this part
}

// 3. Complete
await volcano.storage
  .from('uploads')
  .completeUploadSession('large-video.mp4', session.session_id);
```

### Resume after interruption
```ts
const { data: status } = await volcano.storage
  .from('uploads')
  .getUploadSession('large-video.mp4', sessionId);
// status: { uploaded_parts, total_parts, uploaded_bytes, total_size, missing_parts, part_size }

for (const partNumber of status.missing_parts) {
  const start = (partNumber - 1) * status.part_size;
  const end = Math.min(start + status.part_size, file.size);
  await volcano.storage
    .from('uploads')
    .uploadPart('large-video.mp4', sessionId, partNumber, file.slice(start, end));
}
await volcano.storage.from('uploads').completeUploadSession('large-video.mp4', sessionId);
```

### Abort
```ts
await volcano.storage.from('uploads').abortUploadSession('large-video.mp4', sessionId);
```

### Limits
- Min part size: 5 MB
- Max part size: 25 MB (default)
- Max parts: 10,000
- Session expiry: 7 days

## Error Handling
Common error messages:
- `No active session` — sign in first.
- `File not found` — wrong path or bucket.
- `Permission denied` — access policy violation.
- `Bucket not found` — invalid bucket name.
- `File too large` — exceeds size limit.

```ts
const { data, error } = await volcano.storage.from('uploads').upload('file.txt', file);
if (error) {
  console.error('Upload failed:', error.message);
}
```

## Access Patterns

### User-scoped paths
```ts
// Allowed by typical "path starts with user's id" policy
await volcano.storage.from('uploads').upload(`${user.id}/avatar.jpg`, file);

// Denied
await volcano.storage.from('uploads').upload(`other-user-id/avatar.jpg`, file);
```

### Public read, authenticated write
- Download policy allows anyone (when `is_public`).
- Upload policy requires an authenticated session.

### Custom policies (only for non-default access)
The auto-applied defaults already cover private per-user storage — don't recreate
them. For anything else, attach policies with the CLI (or `volcano-config.yaml`'s
`buckets.<name>.policies`, which fully syncs declared policies). A `--definition`
is an RLS expression over the object row (columns include `owner_id`, `name`,
`bucket_id`, `is_public`):
```sh
volcano storage policy create avatars --operation SELECT --name public-read  --definition "is_public = true"
volcano storage policy create avatars --operation INSERT --name authed-write  --definition "auth.uid() IS NOT NULL"
volcano storage policy create docs    --operation SELECT --name owner-read    --definition "auth.uid() = owner_id"
```
`volcano storage policy list|get|delete <bucket>` to inspect/manage. `--operation`
is one of `SELECT|INSERT|UPDATE|DELETE`.

### Role-based
Policies inspect the user's role from the JWT (admin/user/etc.) — same client API, different rows visible.

## Best Practices
- **Validate before upload** (size and MIME type) for better UX:
```ts
const MAX = 10 * 1024 * 1024;
const ALLOWED = ['image/jpeg', 'image/png', 'image/gif'];
if (file.size > MAX) return showError('File too large');
if (!ALLOWED.includes(file.type)) return showError('Invalid file type');
```
- **Choose resumable above 100 MB** automatically:
```ts
const useResumable = file.size > 100 * 1024 * 1024;
```
- **Revoke object URLs** when no longer displayed:
```ts
const url = URL.createObjectURL(blob);
img.src = url;
// later:
URL.revokeObjectURL(url);
```
- **Show progress** for large uploads using `onProgress`.

## Verification Checklist
- Bucket and path strategy is explicit and ownership-aware.
- Upload/download/list/remove errors are handled.
- Private/public expectations are explicit and justified.
- Resumable upload is used for large files; cleanup-on-cancel is wired.
- No path uses random tokens without semantic prefix.

## Optional Fallback Reference

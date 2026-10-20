---
description: Run Upload Security and Media Processing Checks
globs: ["**/api/upload/**/*.ts", "**/components/upload/**/*.tsx", "**/lib/upload/**/*.ts"]
---
# Security: Uploads & Media Security

<audit_rules>
- You MUST implement a whitelist approach for file type validation using magic numbers (file signatures), NOT just file extensions.
- You MUST strictly sanitize SVG uploads by stripping `<script>` tags, `foreignObject`, and event handlers to prevent Stored XSS.
- You MUST enforce server-side file size limits (e.g., 5MB for images, 10MB for documents).
- You MUST randomize uploaded filenames (e.g., using UUIDs) to prevent file overwrite attacks and path traversal vulnerabilities.
- You MUST validate image transformations (resize, crop) against a whitelist of allowed dimensions to prevent server crash attacks (e.g., `10000x10000px`).
- You MUST ensure uploaded images are served via a CDN with proper caching headers, NOT directly from the origin server.
</audit_rules>

<example_good>
```typescript
// Server-side upload handler
import { v4 as uuidv4 } from 'uuid';
import { fileTypeFromBuffer } from 'file-type';

export async function POST(req: Request) {
  const formData = await req.formData();
  const file = formData.get('file') as File;
  
  if (file.size > 5 * 1024 * 1024) throw new Error("File too large");

  const buffer = await file.arrayBuffer();
  const type = await fileTypeFromBuffer(buffer);
  
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!type || !allowedTypes.includes(type.mime)) throw new Error("Invalid file type");

  const safeFilename = `${uuidv4()}.${type.ext}`;
  // Proceed to save with safeFilename
}
```
</example_good>

<example_bad>
```typescript
// BAD: Trusting client extension and using original filename
export async function POST(req: Request) {
  const formData = await req.formData();
  const file = formData.get('file') as File;
  
  if (!file.name.endsWith('.jpg')) throw new Error("Must be jpg");
  
  // Vulnerable to path traversal (e.g., filename: "../../../etc/passwd")
  await saveFile(file.name, file);
}
```
</example_bad>


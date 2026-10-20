---
name: "File Upload Orchestrator"
version: "1.0.0"
description: "Orchestrates file uploads with progress tracking, chunking, resumable uploads, and validation. Supports S3, GCS, and local storage."
author: "workspace"
activated: false
---

# File Upload Orchestrator

Orchestrates file uploads with progress tracking, chunking, resumable uploads, and validation. Supports S3, GCS, and local storage.

## Decision Framework

### When to Apply
Use when: File uploads > 10MB, bulk uploads, drag-and-drop, resumable uploads needed, progress tracking

### When NOT to Apply
Don't use when: Small single-file inputs (< 1MB), simple avatar uploads

## Anti-Patterns

### 1. No File Type Validation
```javascript
// BAD: Accepts anything
upload(file);

// GOOD: Validate type and size
const allowed = ['image/jpeg', 'image/png', 'application/pdf'];
if (!allowed.includes(file.type)) throw new Error('File type not allowed');
if (file.size > 10 * 1024 * 1024) throw new Error('File too large (max 10MB)');
```

### 2. Unlimited File Sizes
Always enforce size limits to prevent DoS.


## Trigger Phrases

- "File upload"
- "Drag and drop upload"
- "Chunked upload"
- "Upload progress"
- "Resumable upload"

## Patterns

### Chunked Upload
```javascript
class ChunkedUploader {
  constructor(file, options = {}) {
    this.file = file;
    this.chunkSize = options.chunkSize || 5 * 1024 * 1024; // 5MB
    this.concurrency = options.concurrency || 3;
  }

  async upload(onProgress) {
    const chunks = this.createChunks();
    const uploadId = await this.initUpload();
    let uploaded = 0;

    for (let i = 0; i < chunks.length; i += this.concurrency) {
      const batch = chunks.slice(i, i + this.concurrency);
      await Promise.all(batch.map(async (chunk, idx) => {
        await this.uploadChunk(uploadId, i + idx, chunk);
        uploaded++;
        onProgress?.({ loaded: uploaded, total: chunks.length });
      }));
    }

    return this.completeUpload(uploadId);
  }

  createChunks() {
    const chunks = [];
    for (let offset = 0; offset < this.file.size; offset += this.chunkSize) {
      chunks.push(this.file.slice(offset, offset + this.chunkSize));
    }
    return chunks;
  }
}
```

## Integration
- Works with: performance-budget-enforcer, error-recovery-orchestrator, notification-system-builder


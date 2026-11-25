---
name: files-and-media-engineering
description: Handle file upload, storage, and processing. Use when building
  uploads, media, or document workflows.
metadata:
  tags: files, media, engineering
---

# Files & Media Engineering

## Use this skill when
- Designing upload APIs and storage
- Processing images, video, and documents
- Security of uploads and serving

## Do not use this skill when
- Generic web CRUD

## Instructions
1. Validate file types server-side by content, not extension/MIME only.
2. Cap upload sizes, rate-limit, and antivirus-scan.
3. Store on object storage; generate secure signed URLs.
4. Process media asynchronously (resize, transcode) with a queue.
5. Serve via CDN with proper content-type and range support.
6. Keep filenames sanitized and never trust client paths.
7. Enforce permissions when serving user media.

## Checklist
- Content validated
- No path traversal
- Signed URLs with expiry

## Output Format
- Upload flow | storage | processing | serving | security

## Common Mistakes
- Trusting client MIME/extension
- Serving private files unauthenticated
- Blocking main thread on transcodes

---
name: skill-manual-video-processing
description: Use for manual video or audio uploads in SaaS apps, including upload UX, direct storage, validation, malware checks, quota enforcement, asynchronous processing jobs, transcription, clip extraction, review flows, signed URLs, consent, and secure media access.
category: media
risk: medium
source: local-media-pipeline-patterns
---

# Manual Video Processing

Use this skill when users upload videos or audio for transcription, clipping, editing, proposal generation, content creation, review, or publishing workflows.

## Upload Contract

1. Validate tenant quota, file type, extension, MIME sniffing result, file size, duration, codec, and requested processing level.
2. Use resumable or direct-to-storage upload for large files; avoid streaming whole files through application memory.
3. Store uploads in private buckets by default and expose only signed URLs.
4. Create or reserve a `media_assets` record before upload and finalize it only after checksum and metadata validation.
5. Create a `media_jobs` record after upload completion and before expensive processing.
6. Run malware, abuse, copyright, and content checks when the product accepts untrusted files or public uploads.
7. Queue processing stages and make them idempotent by asset checksum, job ID, stage name, and processing options hash.
8. Separate upload completion, processing completion, review approval, and publishing as distinct user-visible states.
9. Require explicit consent before using uploaded voice, face, customer data, or third-party media for AI generation or publication.
10. Minimize tokens by chunking transcripts, caching metadata, and sending only relevant segments to AI services.

## Expected Flow

1. Request upload permission and validate quota.
2. Upload directly to private storage.
3. Finalize asset metadata and checksum.
4. Queue processing job.
5. Extract metadata and audio.
6. Run transcription, AI enrichment, and clip detection when requested.
7. Save generated assets and review state.
8. Publish only after approval or explicit auto-publish consent.
9. Emit analytics and audit events.

## Data Model Hints

- `media_assets`: tenant ID, owner ID, storage path, original name hash, MIME type, size, duration, checksum, scan status, retention deadline.
- `media_jobs`: asset ID, requested outputs, status, current stage, idempotency key, retry count, error class.
- `media_reviews`: job ID, reviewer ID, decision, notes, approved asset IDs, timestamp.

## Verification

- Test oversized files, spoofed MIME types, interrupted upload resume, duplicate upload finalize, malware rejection, worker retry, quota exceeded, signed URL expiry, review rejection, and revoked consent.
- Confirm no uploaded private asset is reachable without authorization.

## Related Skills

- `skill-live-processing`
- `skill-smart-clip-detection`
- `skill-ai-orchestration`
- `skill-saas-core-limits`


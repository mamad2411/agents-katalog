---
name: skill-live-processing
description: Use for live stream and VOD ingestion pipelines, including YouTube, Twitch, uploads, capture jobs, queues, transcription, clip generation, media storage, retries, idempotent workers, consent, validation, observability, and safe server-side provider credentials.
category: media
risk: medium
source: local-media-pipeline-patterns
---

# Live Processing

Use this skill for live streams, long VODs, and media pipelines that produce transcripts, summaries, clips, thumbnails, captions, or publishable assets.

## Pipeline Contract

1. Separate ingestion, processing, enrichment, review, and publishing into explicit stages.
2. Keep platform OAuth tokens, webhook secrets, storage credentials, AI provider keys, and signing keys server-side.
3. Validate source ownership, platform terms, tenant quota, duration, codec, file size, language, and processing options before enqueueing.
4. Create a durable `media_jobs` record before downloading or running expensive work.
5. Run long work in queues or workers. Do not download, transcode, transcribe, or render inside request handlers.
6. Make every stage idempotent and resumable from stored artifacts, checksums, stage status, and provider job IDs.
7. Store source media and generated assets in private storage. Use signed URLs with short TTLs for preview and download.
8. Batch and chunk AI work. Reuse transcript segments, embeddings, shot boundaries, and thumbnails instead of resending full media context.
9. Require review before publishing clips or generated metadata unless the product has explicit auto-publish consent.
10. Emit structured progress, queue age, stage duration, retry count, artifact checksums, and sanitized failure reasons.

## Stage States

Use stable states such as:

`queued`, `validating`, `downloading`, `extracting_audio`, `transcribing`, `detecting_clips`, `rendering`, `review_ready`, `publishing`, `published`, `failed`, `cancelled`.

## Data Model Hints

- `media_jobs`: tenant ID, owner ID, source type, source URL or asset ID, status, current stage, progress, idempotency key, retry count, error class.
- `media_assets`: job ID, kind, storage path, duration, size, checksum, codec, metadata, retention deadline.
- `clip_candidates`: job ID, timestamps, score, reason, transcript excerpt hash, review status.
- `processing_events`: job ID, stage, status, duration, worker ID, details.

## Verification

- Test webhook ingestion, duplicate webhook, cancelled job, worker crash and resume, provider timeout, quota exceeded, invalid media, signed URL expiry, and publishing gate behavior.
- Confirm platform and provider secrets are not exposed in clients or logs.

## Related Skills

- `skill-smart-clip-detection`
- `skill-manual-video-processing`
- `skill-ai-orchestration`
- `skill-unified-analytics`


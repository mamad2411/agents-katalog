---
name: youtube-publishing-automation
description: Build approval-first YouTube upload queues, scheduling, playlists and multi-channel publishing.
---
# YouTube Publishing Automation
Use official YouTube OAuth and Data API. Separate preparation, validation, upload, scheduling and verification into idempotent jobs.

- Confirm channel identity and destination.
- Confirm media rights, metadata, audience setting, category, language, captions and thumbnail.
- Default visibility to private for review.
- Require explicit confirmation for public/unlisted visibility, scheduling, playlist changes and comments.
- Persist job state in a durable store; deduplicate retries by content hash and channel.
- Verify the returned video ID and final status before marking a job complete.

Do not automate browser sign-in, bypass security checks, mass-post comments or evade API quota.

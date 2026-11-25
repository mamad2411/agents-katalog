---
tags: [backend, realtime, polling, fallback]
name: realtime-vs-polling-fallback
description: Let each resource type declare `supportsRealtime`; scheduler runs push-mode at the realtime interval and falls back to a safe polling interval (e.g., 60s) otherwise
version: 1.0.0
source_project: cygnus
source_ref: cygnus@cbb96a6dfff
category: backend
triggers:
  - mixed collection pipeline (some resources push, some pull)
  - avoid hammering APIs that do not support realtime
---

# Real-Time vs Polling Fallback

See `content.md`.

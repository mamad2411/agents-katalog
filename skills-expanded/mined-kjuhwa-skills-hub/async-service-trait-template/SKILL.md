---
name: async-service-trait-template
description: Trait-based async service with Arc<Mutex<>> for connection state and per-session isolation.
category: async
version: 1.0.0
version_origin: extracted
tags: [async, service, template, trait]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: [src/server/video_service.rs, src/server/connection.rs]
imported_at: 2026-04-19T00:00:00Z
---

# Async Service Trait Template

## When to use
Trait-based async service with Arc<Mutex<>> for connection state and per-session isolation.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `src/server/video_service.rs`, `src/server/connection.rs`

## Why this generalizes
Generalizes to any long-running async service with per-client state.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

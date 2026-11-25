---
name: async-task-spawning-pattern
description: tokio::spawn for concurrent background tasks with UnboundedChannel for coordination.
category: async
version: 1.0.0
version_origin: extracted
tags: [async, pattern, spawning, task]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: src/flutter.rs
imported_at: 2026-04-19T00:00:00Z
---

# Async Task Spawning Pattern

## When to use
tokio::spawn for concurrent background tasks with UnboundedChannel for coordination.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `src/flutter.rs`

## Why this generalizes
Canonical tokio task pattern.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

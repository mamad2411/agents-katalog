---
name: feature-flag-conditional-compilation
description: Nested feature gates (hwcodec, vram, mediacodec, flutter, unix-file-copy-paste) in Cargo.toml.
category: build-system
version: 1.0.0
version_origin: extracted
tags: [build, compilation, conditional, feature, flag, system]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: Cargo.toml
imported_at: 2026-04-19T00:00:00Z
---

# Feature Flag Conditional Compilation

## When to use
Nested feature gates (hwcodec, vram, mediacodec, flutter, unix-file-copy-paste) in Cargo.toml.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `Cargo.toml`

## Why this generalizes
Template for large Rust workspaces with optional subsystems.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

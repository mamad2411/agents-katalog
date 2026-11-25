---
name: video-codec-enum-trait-dispatch
description: Trait-based encoder dispatch with EncoderCfg enum variants for VP9, AOM, HWRAM, VRAM codecs.
category: codecs
version: 1.0.0
version_origin: extracted
tags: [codec, codecs, dispatch, enum, trait, video]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: libs/scrap/src/common/codec.rs
imported_at: 2026-04-19T00:00:00Z
---

# Video Codec Enum Trait Dispatch

## When to use
Trait-based encoder dispatch with EncoderCfg enum variants for VP9, AOM, HWRAM, VRAM codecs.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `libs/scrap/src/common/codec.rs`

## Why this generalizes
Idiomatic Rust pattern for pluggable codec selection.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

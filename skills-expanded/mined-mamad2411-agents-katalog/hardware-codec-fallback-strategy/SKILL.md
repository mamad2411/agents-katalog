---
name: hardware-codec-fallback-strategy
description: Graceful fallback from hwcodec (NVENC/QSV) to software codecs (VP9/AOM) gated by feature flags + runtime probe.
category: codecs
version: 1.0.0
version_origin: extracted
tags: [codec, codecs, fallback, hardware, strategy]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: [libs/scrap/src/common/hwcodec.rs, libs/scrap/src/common/vram.rs, libs/scrap/src/common/vpx.rs]
imported_at: 2026-04-19T00:00:00Z
---

# Hardware Codec Fallback Strategy

## When to use
Graceful fallback from hwcodec (NVENC/QSV) to software codecs (VP9/AOM) gated by feature flags + runtime probe.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `libs/scrap/src/common/hwcodec.rs`, `libs/scrap/src/common/vram.rs`, `libs/scrap/src/common/vpx.rs`

## Why this generalizes
Any media app on heterogeneous hardware needs this failover.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

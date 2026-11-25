---
name: quartz-metal-gpu-display-capture
description: macOS Quartz/CoreGraphics display capture with frame rotation and adapter descriptor caching.
category: codecs
version: 1.0.0
version_origin: extracted
tags: [capture, codecs, display, gpu, metal, quartz]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: libs/scrap/src/quartz/
imported_at: 2026-04-19T00:00:00Z
---

# Quartz Metal Gpu Display Capture

## When to use
macOS Quartz/CoreGraphics display capture with frame rotation and adapter descriptor caching.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `libs/scrap/src/quartz/`

## Why this generalizes
Reusable for macOS capture tooling.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

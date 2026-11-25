---
name: cross-platform-clipboard-abstraction
description: Multi-format clipboard (text, HTML, RTF, images, files) across Windows/macOS/Linux behind one API.
category: clipboard
version: 1.0.0
version_origin: extracted
tags: [abstraction, clipboard, cross, platform]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: [src/clipboard.rs, libs/clipboard/src/]
imported_at: 2026-04-19T00:00:00Z
---

# Cross Platform Clipboard Abstraction

## When to use
Multi-format clipboard (text, HTML, RTF, images, files) across Windows/macOS/Linux behind one API.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `src/clipboard.rs`, `libs/clipboard/src/`

## Why this generalizes
Reusable blueprint for clipboard sync tools.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

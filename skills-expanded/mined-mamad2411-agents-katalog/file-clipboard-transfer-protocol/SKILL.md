---
name: file-clipboard-transfer-protocol
description: RDP-style file transfer via clipboard with CLIPRDR context abstraction and platform backends.
category: clipboard
version: 1.0.0
version_origin: extracted
tags: [clipboard, file, protocol, transfer]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: [libs/clipboard/src/lib.rs, src/clipboard_file.rs]
imported_at: 2026-04-19T00:00:00Z
---

# File Clipboard Transfer Protocol

## When to use
RDP-style file transfer via clipboard with CLIPRDR context abstraction and platform backends.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `libs/clipboard/src/lib.rs`, `src/clipboard_file.rs`

## Why this generalizes
Niche but reusable for remote-desktop or VDI style tooling.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

---
name: platform-screen-capture-abstraction
description: "Pluggable screen-capture backends: Windows DXGI, macOS Quartz, Linux X11/Wayland behind one Capturer trait."
category: codecs
version: 1.0.0
version_origin: extracted
tags: [abstraction, capture, codecs, platform, screen]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: [libs/scrap/src/dxgi/, libs/scrap/src/quartz/, libs/scrap/src/x11/, libs/scrap/src/wayland/]
imported_at: 2026-04-19T00:00:00Z
---

# Platform Screen Capture Abstraction

## When to use
Pluggable screen-capture backends: Windows DXGI, macOS Quartz, Linux X11/Wayland behind one Capturer trait.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `libs/scrap/src/dxgi/`, `libs/scrap/src/quartz/`, `libs/scrap/src/x11/`, `libs/scrap/src/wayland/`

## Why this generalizes
General template for any tool that needs desktop capture across OSes.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

---
name: platform-specific-code-organization
description: Use cfg-gated modules to split Windows/macOS/Linux/Android/iOS implementations behind one trait facade.
category: cross-platform
version: 1.0.0
version_origin: extracted
tags: [code, cross, organization, platform, specific]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: [src/platform/windows.rs, src/platform/macos.rs, src/platform/linux.rs]
imported_at: 2026-04-19T00:00:00Z
---

# Platform Specific Code Organization

## When to use
Use cfg-gated modules to split Windows/macOS/Linux/Android/iOS implementations behind one trait facade.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `src/platform/windows.rs`, `src/platform/macos.rs`, `src/platform/linux.rs`

## Why this generalizes
Applies to any Rust crate needing per-OS backend with a shared API.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

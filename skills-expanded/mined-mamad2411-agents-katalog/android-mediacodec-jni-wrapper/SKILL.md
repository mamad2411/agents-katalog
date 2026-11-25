---
name: android-mediacodec-jni-wrapper
description: Android MediaCodec FFI bindings for hardware video decode/encode via JNI.
category: codecs
version: 1.0.0
version_origin: extracted
tags: [android, codecs, jni, mediacodec, wrapper]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: libs/scrap/src/android/ffi.rs
imported_at: 2026-04-19T00:00:00Z
---

# Android Mediacodec Jni Wrapper

## When to use
Android MediaCodec FFI bindings for hardware video decode/encode via JNI.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `libs/scrap/src/android/ffi.rs`

## Why this generalizes
Reusable for Android-native media tooling.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

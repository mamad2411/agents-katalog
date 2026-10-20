---
name: canvas-coordinate-transformation-model
description: Canvas transform state (x, y, scale, scrollX, scrollY) serialization for remote rendering.
category: flutter
version: 1.0.0
version_origin: extracted
tags: [canvas, coordinate, flutter, model, transformation]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: flutter/lib/models/input_model.dart
imported_at: 2026-04-19T00:00:00Z
---

# Canvas Coordinate Transformation Model

## When to use
Canvas transform state (x, y, scale, scrollX, scrollY) serialization for remote rendering.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `flutter/lib/models/input_model.dart`

## Why this generalizes
Reusable for any Flutter canvas with zoom/pan and remote-input mapping.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

---
name: multi-window-parameter-passing
description: Window parameter serialization via Map<String, dynamic> for multi-window session state.
category: flutter
version: 1.0.0
version_origin: extracted
tags: [flutter, multi, parameter, passing, window]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: flutter/lib/desktop/pages/remote_tab_page.dart
imported_at: 2026-04-19T00:00:00Z
---

# Multi Window Parameter Passing

## When to use
Window parameter serialization via Map<String, dynamic> for multi-window session state.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `flutter/lib/desktop/pages/remote_tab_page.dart`

## Why this generalizes
Reusable for desktop_multi_window-based apps.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

---
name: permission-bitmask-control-abstraction
description: Permission flags encoded as ControlPermissions bitmask with permission_info protobuf messages.
category: auth
version: 1.0.0
version_origin: extracted
tags: [abstraction, auth, bitmask, control, permission]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/rustdesk/rustdesk.git
source_ref: master
source_commit: ac124c068056395f9456a6c42eddab89b469a3a8
source_project: rustdesk
source_path: src/server/connection.rs
imported_at: 2026-04-19T00:00:00Z
---

# Permission Bitmask Control Abstraction

## When to use
Permission flags encoded as ControlPermissions bitmask with permission_info protobuf messages.

## Source context
- Repo: `rustdesk/rustdesk` @ `ac124c0680`
- Demonstrated in: `src/server/connection.rs`

## Why this generalizes
Reusable for capability-style ACLs over a wire protocol.

## Next steps before publishing
- Read the source files above and rewrite this as a product-agnostic `how-to` — keep the pattern, drop rustdesk-specific names.
- Add a minimal code example in the target language (Rust + Dart / Rust only / etc.).
- List 2-3 gotchas you hit while reproducing it.

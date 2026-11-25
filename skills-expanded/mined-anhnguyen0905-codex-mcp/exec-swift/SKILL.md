---
name: exec-swift
description: Swift execution idioms to embed into Codex prompts when the target project is Swift — optionals, value semantics, Swift Concurrency, and error handling.
---

# Swift Idioms (embed when project is Swift)

```
Swift standards:
- Optionals: no force-unwrap (!) or try! in production paths; use if let / guard let / ??; guard for
  early exit at the top of functions. Model absence with Optional, not sentinel values.
- Errors: throwing functions + do/try/catch with typed error enums; never empty catch; use Result
  only at async/callback boundaries. Propagate, don't swallow.
- Value semantics: prefer struct/enum over class unless reference identity is needed; let over var;
  immutable properties by default; mutating methods explicit on value types.
- Swift Concurrency: async/await + structured concurrency (async let, TaskGroup); actors for shared
  mutable state; respect @MainActor for UI; propagate cancellation (Task.checkCancellation); avoid
  unstructured Task {} that outlives its scope. No blocking calls on the main thread.
- Protocol-oriented design: small protocols, protocol extensions for defaults; avoid forced downcasts
  (as!). Use generics/some over type erasure unless erasure is required.
- Memory: [weak self]/[unowned self] in escaping closures to avoid retain cycles; break cycles in
  delegates (weak).
- Follow the project's SwiftFormat/SwiftLint config and file/folder structure; SwiftUI or UIKit
  idioms as the project uses them.
- Tests: XCTest (or Swift Testing if the repo uses it); given-when-then; test behavior; match the
  existing test target layout and naming.
```

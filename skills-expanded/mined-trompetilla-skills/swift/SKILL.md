---
name: Swift
description: Write safe Swift code avoiding memory leaks, optional traps, and concurrency bugs.
metadata: {"clawdbot":{"emoji":"🦅","os":["darwin","linux"]}}
---

# Swift Gotchas

## Optional Traps
- Force unwrap `!` crashes on nil — use `guard let` or `if let` instead
- Implicitly unwrapped optionals `String!` still crash if nil — only use for IBOutlets
- Optional chaining returns optional — `user?.name?.count` is `Int?` not `Int`
- `??` default value evaluates eagerly — use `?? { expensive() }()` for lazy
- Comparing optionals: `nil < 1` is true — unexpected sort behavior

## Memory Leaks
- Closures capturing `self` strongly create retain cycles — use `[weak self]` in escaping closures
- Delegates must be `weak` — strong delegate = object never deallocates
- Timer retains target strongly — invalidate in `deinit` won't work, use `weak` or `block` API
- NotificationCenter observers retained until removed — remove in `deinit` or use `addObserver(forName:using:)` with token
- Nested closures: each level needs own `[weak self]` — inner closure captures outer's strong ref

## Concurrency Traps
- `async let` starts immediately — not when you `await`
- Actor isolation: accessing actor property from outside requires `await` — even for reads
- `@MainActor` doesn't guarantee immediate main thread — it's queued
- `Task.detached` loses actor context — inherits nothing from caller
- Sendable conformance: mutable class properties violate thread safety silently until runtime crash

## Value vs Reference
- Structs copied on assign, classes shared — mutation affects only copy or all references
- Large structs copying is expensive — profile before assuming copy-on-write saves you
- Mutating struct in collection requires reassignment — `array[0].mutate()` doesn't work, extract, mutate, replace
- `inout` parameters: changes visible only after function returns — not during

## Codable Pitfalls
- Missing key throws by default — use `decodeIfPresent` or custom init
- Type mismatch throws — `"123"` won't decode to `Int` automatically
- Enum raw value must match exactly — `"status": "ACTIVE"` fails for `.active` case
- Nested containers need manual `CodingKeys` at each level
- Custom `init(from:)` must decode ALL properties or provide defaults

## Protocol Gotchas
- Protocol extensions don't override — static dispatch ignores subclass implementation
- `Self` requirement prevents use as type — `protocol Animal` vs `any Animal`
- `@objc` required for optional protocol methods
- Associated types can't use with `any` without constraints — use generics or type erasure
- Witness matching is exact — `func foo(_: Int)` doesn't satisfy `func foo(_: some Numeric)`

## String Traps
- Characters can be multiple Unicode scalars — emoji count isn't byte count
- Subscripting is O(n) — use indices, not integers
- `String.Index` from one string invalid on another — even if contents match
- Empty string is not nil — check `.isEmpty`, not `== nil`
- `contains()` is case-sensitive — use `localizedCaseInsensitiveContains` for user search

## Collection Edge Cases
- `first` and `last` are optional — empty collection returns nil
- `removeFirst()` crashes on empty, `popFirst()` returns nil
- `index(of:)` is O(n) — for frequent lookups use Set or Dictionary
- Mutating while iterating crashes — copy first or use `reversed()` for removal
- `ArraySlice` indices don't start at 0 — use `startIndex`

## Error Handling
- `try?` swallows error details — use only when error type doesn't matter
- `try!` crashes on any error — never use in production paths
- Throwing from closure requires explicit `throws` in closure type
- `rethrows` only works if closure throws — prevents unnecessary `try` at callsite
- Error must conform to `Error` — plain `throw "message"` doesn't compile

## Build and Runtime
- Generic code bloat — specialized for each type, increases binary size
- `@inlinable` exposes implementation to other modules — ABI stability consideration
- Dynamic casting `as?` can be slow — prefer static typing
- Reflection with `Mirror` is slow — not for hot paths
- `print()` builds strings even in release — remove or use os_log

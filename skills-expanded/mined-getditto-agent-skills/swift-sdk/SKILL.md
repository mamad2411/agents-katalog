---
name: swift-sdk
description: >
  Use ONLY for tasks that use the Ditto Swift SDK (not generic SwiftUI/Xcode work
  without Ditto; other languages use their own Ditto SDK skill). Builds and
  troubleshoots Ditto Swift apps: setup, DittoConfig, Ditto.open, observers,
  authentication, lifetimes and Swift concurrency errors. Triggers on .swift,
  Package.swift or Xcode files touching import DittoSwift. Covers iOS, iPadOS,
  macOS/AppKit and Mac Catalyst on Ditto 4.14.x, 5.0.x, 5.1.x and 5.2.0.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Ditto Swift SDK

Use the shipping API: `DittoIdentity`, `startSync()` and collection APIs are deprecated
on 4.14.x and removed in v5. Establish the package pin first; emit non-deprecated forms
for that line, preferring forms that also exist in v5. Do not invent APIs from memory.

Read only the reference sections needed for the task. For long files, inspect the
contents first and read the matching section. Do not preload all references or the
README; the latter holds the capability/evidence map for coverage reviews.

## What this skill does

Writes and reviews Ditto Swift code: initialization, authentication, store access,
sync, lifetimes, threading and Xcode/SwiftPM configuration. Supports **4.14.x (LTS),
5.0.x, 5.1.x and 5.2.0**, on iOS, iPadOS, macOS and Mac Catalyst with SwiftUI/UIKit/AppKit.

### New apps and integration failures

For a new runnable Swift app, follow [getting-started.md](references/getting-started.md)
and [project-deliverables.md](references/project-deliverables.md). Use the bundled
generator for a SwiftUI Xcode project; integrate existing apps in place. For failures,
use [troubleshooting.md](references/troubleshooting.md). Load these only for that task.

## When to use this skill

Use for Swift Ditto integration and required permissions/entitlements. Other topics
have separate skills; load one only when the task needs its semantics:

| Question | Skill if installed | Otherwise |
|---|---|---|
| DQL syntax and semantics | `write-dql` | <https://docs.ditto.live/dql/dql> |
| CRDT selection, embed vs split, document size | `data-modeling` | <https://docs.ditto.live/key-concepts> |
| Subscription propagation | `sync-subscriptions` | <https://docs.ditto.live/sdk/latest/sync/syncing-data> |
| Radio selection and platform transport support | `ditto-mesh-networking` | <https://docs.ditto.live/sdk/latest/sync/customizing-transport-configurations> |
| v4 → v5 migration procedure | — | <https://docs.ditto.live/sdk/latest/migration-guides/swift-v4> and <https://docs.ditto.live/sdk/latest/migration-guides/swift-dql> |

## Supported versions and packages

SwiftPM: `https://github.com/getditto/DittoSwiftPackage`, product `DittoSwift`.
Read the relevant section of [versions.md](references/versions.md) for package pins,
platform minimums or version differences.

**5.2.0 is the latest version this skill knows about**, not a claim about today's latest.
Existing project pins win; for a new app resolve the latest stable SwiftPM tag (the
generator does this) as in [setup.md](references/setup.md). If lookup is unavailable, say
so rather than calling 5.2.0 “latest”.

Read [sdk-5.2.md](references/sdk-5.2.md) when adopting 5.2.0 features or reviewing an
upgrade: encryption, store deletion, startup configuration and behavior fixes.
The 5.2.0 public Swift API lacks `Ditto.close()` despite the release notes; release
all strong references before `Ditto.deleteStore`.

## Capability exceptions

Full twenty-row evidence map: [README.md](README.md), for capability reviews only.

| ID | Capability | Support | Required caveat |
|---|---|---|---|
| CAP-03 | Connecting: config, opening, persistence directory | preview | 4.14.x config/open is preview, no opt-in; prefer it to the deprecated identity initializer. GA on v5. |
| CAP-04 | Authentication and identity | preview | 4.14.x provider/expirationHandler is preview; GA on v5. |
| CAP-13 | Presence graph and connection requests | partial | Graph, peer metadata and observe are available; connectionRequestHandler only takes effect with a second peer. |
| CAP-20 | Preview and platform-specific APIs | preview | passphrase is not for production; multicast beta is 5.1.0+, default off, restricted entitlement required. Data Streams: 5.2.0+, `@_spi(PreviewDataStreams) import DittoSwift`, executed on macOS. [preview.md](references/preview.md), [data-streams.md](references/data-streams.md) |

## Minimum viable app

```swift
import DittoSwift
import Foundation  // v5 does not re-export Foundation

let ditto = try await Ditto.open(config: DittoConfig(   // `await`, not openSync
    databaseID: "REPLACE_ME_WITH_YOUR_DATABASE_ID",
    connect: .server(url: URL(string: "REPLACE_ME_WITH_YOUR_CONNECT_URL")!)))

// Install BEFORE sync.start(), and await the login inside it.
ditto.auth?.expirationHandler = { ditto, _ in await reauthenticate(ditto) }
try ditto.sync.start()

let query = "SELECT * FROM cars WHERE mileage > :min"
let arguments: [String: Any?] = ["min": 100]
let subscription = try ditto.sync.registerSubscription(query: query, arguments: arguments)
let observer = try ditto.store.registerObserver(query: query, arguments: arguments) { @Sendable result in
    for item in result.items {
        defer { item.dematerialize() }
        print(item.value["make"] as? String ?? "")      // [String: Any?] is not Sendable
    }
}
try await ditto.store.execute(query: "INSERT INTO cars DOCUMENTS (:car)",
                              arguments: ["car": ["make": "Toyota", "mileage": 120]])
```

Hold `ditto`, `subscription` and `observer` — see § Object lifetimes. Starting this once
from SwiftUI and hopping to the main actor without losing ordering are both in
[`references/concurrency.md`](references/concurrency.md). Complete runnable programs:
[`examples/minimal-app.md`](examples/minimal-app.md) and
[`examples/swiftui-app.md`](examples/swiftui-app.md).

## Concurrency and threading model

Read [concurrency.md](references/concurrency.md) for callback delivery and the ordered
observer→stream→consumer bridge. Core constraints:

- Never assume main-actor delivery. `deliverOn:` is ignored on **5.0.x**; hop
  explicitly inside callbacks.
- Extract Sendable values from `[String: Any?]` inside the callback. Do expensive
  conversion there; send only the final UI assignment to the main actor.
- Use one stream consumer, not one unordered Task per delivery. `.bufferingNewest(1)`
  coalesces UI snapshots. `Ditto` is Sendable on v5; no actor wrapper/shim is needed.
- On 4.14.x use `@preconcurrency import DittoSwift` for Swift 6.
- For `handlerWithSignalNext`, call `signalNext()` exactly once per delivery.
  `auth.expirationHandler` is async, Sendable and off-main: it must not touch UI state.

## Object lifetimes and retention

Keep one app-lived strong `Ditto` reference at the composition root. Its `store`,
`sync`, `presence`, `auth`, `smallPeerInfo` and `experimental` hold weak parent references:
retaining a child does not keep Ditto alive; using it after release can `fatalError`.

Dropping observer/subscription handles **does not cancel** them; work/captures remain
until cancelled or Ditto is destroyed. Releasing `AnyCancellable` does cancel.
Cancel at the owning scope's boundary (`onDisappear`/`viewDidDisappear`; deinit only
where actor isolation permits). Do not cache computed `sync.subscriptions` or
`store.observers` snapshots. Handle table/teardown: [lifetimes.md](references/lifetimes.md).

## Anti-patterns

Read [anti-patterns.md](references/anti-patterns.md) for wrong/right forms.

- Numeric casts can silently drop rows (CBOR picks widths by value): use `NSNumber`/Codable.
- Missing `signalNext()` stops delivery forever: `defer { signalNext() }` first.
- A fresh `DittoTransportConfig()` disables other radios: use `updateTransportConfig`.
- Dematerializing before `DittoDiffer.diff` crashes; diff → extract → dematerialize.
- `sync.isActive` means started, not connected.

The Sendable-shim and portal-URL mistakes are covered there too.

## Version differences

[versions.md](references/versions.md) owns deltas and upgrade/rollback results.
On 4.14.x call `try ditto.disableSyncWithV3()` before mutating DQL. 5.1.0/5.2.0 are arm64-only;
4.14.x/5.0.x also ship x86_64. 4.14.6 throws for some use-after-release calls where v5
calls `fatalError`; preserve parent ownership on every line.

## References

Pick one row; these are alternatives, not a reading list.

| Task | Read |
|---|---|
| Install/package pin, platform minimums, Info.plist/entitlements | [setup.md](references/setup.md); keep signing on or the XCFramework aborts at launch |
| Open/authenticate, re-auth or logout | [connect.md](references/connect.md); one instance, re-authenticate in place |
| Actor crossing or starting SwiftUI exactly once | [concurrency.md](references/concurrency.md) |
| Retention/cancellation | [lifetimes.md](references/lifetimes.md) |
| Store observer, signalNext, UI diffing | [observers.md](references/observers.md) |
| Diagnose a symptom | [anti-patterns.md](references/anti-patterns.md), then [errors.md](references/errors.md) if needed |
| Compare core versions | [versions.md](references/versions.md), only the relevant delta |
| Presence/Combine compatibility and patch fixes | [api-compatibility.md](references/api-compatibility.md) |
| Run Swift tests | [testing.md](references/testing.md); unset `NO_COLOR` for `swift test` |
| Execute DQL, transact, index or evict | [store.md](references/store.md) |
| Subscribe, scope sync or track status | [sync.md](references/sync.md) |
| Update radios/endpoints | [transports.md](references/transports.md) |
| Create/fetch attachments | [attachments.md](references/attachments.md); retain fetcher; token shape differs by version |
| Stream ephemeral bytes | [data-streams.md](references/data-streams.md); 5.2.0 SPI; concepts in `data-streams` |
| Presence/peer metadata | [presence.md](references/presence.md) |
| Logging and disk usage | [observability.md](references/observability.md) |
| On-disk upgrade/rollback | [storage.md](references/storage.md) |
| Preview/platform APIs | [preview.md](references/preview.md) |
| Architectural tradeoffs | [best-practices.md](best-practices.md), matching section |
| Run/configure the minimal example | [minimal-app-running.md](references/minimal-app-running.md) |
| Build a complete example | [minimal-app.md](examples/minimal-app.md) (compiled/run) or [swiftui-app.md](examples/swiftui-app.md) (compile checked) |

---
name: kotlin-sdk
description: >
  Use ONLY for the Ditto Kotlin SDK (not Swift, Java, JS, C#, C++, Rust, Flutter or Go
  — each has its own skill). Builds and troubleshoots Ditto apps on Android and the
  JVM. Triggers on .kt/.kts files, build.gradle.kts, com.ditto:ditto-kotlin, live.ditto:ditto, DittoConfig, DittoFactory.create, registerObserver, and errors like "Query result item has already been closed.",
  "Unable to find binary 'libdittoall'", "Identifier conflict … FAIL conflict policy".
  Ditto SDK 4.14.x, 5.0.x, 5.1.x, 5.2.x.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Ditto Kotlin SDK

Use the shipping API: on v5 everything is `DittoFactory.create(DittoConfig)`,
`ditto.sync`, `ditto.store` with DQL, and `suspend`/Flow observers; the v4
`Ditto(dependencies, identity)` constructor and legacy collection API are gone.
Establish the version line first (`com.ditto:ditto-kotlin` = v5, `live.ditto:ditto` =
v4, Android-only); emit v5 code by default and say which version you assumed. Do not
invent APIs from memory — the v4→v5 surface changed completely.

Read only the reference sections the task needs; inspect a long file's contents first.
Do not preload all references or the README (the capability/evidence map).

## What this skill does

Writes and reviews Ditto Kotlin code: Gradle setup, initialization, authentication,
DQL store access, sync, observers and Flows, attachments, presence, transports, object
lifetimes, threading, errors and testing. Supports **4.14.x (LTS), 5.0.x, 5.1.x and
5.2.x** on **Android** (both lines) and **plain JVM** (5.x only).

## When to use this skill

Use this skill for **Kotlin** Ditto code: API shape, initialization, object
lifetimes, threading, error types, and build configuration.

Hand off rather than restating; each row names a public URL in case the concept skill
is not installed:

| Question | Skill, if installed | Otherwise |
|---|---|---|
| DQL syntax, operators, statement semantics | `write-dql` | <https://docs.ditto.live/dql/dql> |
| Which CRDT type, embed vs split, document size, `dql_strict_mode` | `data-modeling` | <https://docs.ditto.live/key-concepts> |
| What a subscription is, mesh propagation | `sync-subscriptions` | <https://docs.ditto.live/sdk/latest/sync/syncing-data> |
| Transport selection strategy, platform radios | `ditto-mesh-networking` | <https://docs.ditto.live/sdk/latest/sync/customizing-transport-configurations> |
| v4 → v5 migration procedure | — | <https://docs.ditto.live/sdk/latest/migration-guides/kotlin-v4> and <https://docs.ditto.live/sdk/latest/migration-guides/kotlin-dql> |

## Supported versions and packages

Packages: `com.ditto:ditto-kotlin` (v5; KMP root — Gradle resolves `-android` / `-jvm`)
and `live.ditto:ditto` (4.14.x, Android-only). Published API reference:
<https://software.ditto.live/kotlin/ditto-kotlin/5.2.0/api-reference/>.

**[`references/versions.md`](references/versions.md) owns every fact that differs
across version lines**, including package coordinates per version and the minimum
toolchain. v4 and v5 are different APIs, not two versions of one.

**5.2.0 is the latest version this skill knows about**, not a claim about today's latest.
Existing project pins win; for a new app resolve the latest stable release from Maven
Central and use it for both artifacts, as in [setup.md](references/setup.md) CAP-01. If
lookup is unavailable, say so rather than calling 5.2.0 “latest”.

Read [sdk-5.2.md](references/sdk-5.2.md) when adopting 5.2.0 features or reviewing an
upgrade: encryption, store deletion, startup configuration and behavior fixes.

## Capability exceptions

Full twenty-row evidence map: [README.md](README.md), for capability reviews only.

| ID | Capability | Support | Required caveat |
|---|---|---|---|
| CAP-13 | Presence graph and connection requests | partial | Graph, metadata and `observe()` are docs-verified; `connectionRequestHandler` only fires with a second peer and was not executed. [presence.md](references/presence.md) |
| CAP-20 | Preview and platform-specific APIs | preview | Data Streams: 5.1.0+, `@file:OptIn(com.ditto.kotlin.PreviewDataStreams::class)`, "breaking changes without notice", NGN required; two-peer fixture executed on the JVM. [data-streams.md](references/data-streams.md). Multicast: beta from 5.1.0, off by default. [preview.md](references/preview.md) |

## Minimum viable app

Open → subscribe → observe → write (JVM shown; on Android hold the instance in
`Application`; no `ditto-binaries` classifier is needed there):

```kotlin
fun main() = runBlocking {
    val ditto = DittoFactory.create(
        DittoConfig(
            databaseId = "my-app",
            connect = DittoConfig.Connect.SmallPeersOnly(),
            persistenceDirectory = "/tmp/ditto-data",
        )
    )
    ditto.setOfflineOnlyLicenseToken(System.getenv("DITTO_OFFLINE_LICENSE"))
    ditto.sync.start()

    val subscription = ditto.sync.registerSubscription("SELECT * FROM cars")
    val observer = ditto.store.registerObserver("SELECT * FROM cars") { result ->
        println("cars: ${result.items.size}")   // extract inside the lambda!
    }
    ditto.store.execute(
        "INSERT INTO cars DOCUMENTS (:car) ON ID CONFLICT DO UPDATE",
        mapOf("car" to mapOf("_id" to "car1", "make" to "Toyota"))
    )

    observer.close(); subscription.close(); ditto.sync.stop(); ditto.close()
}
```

Complete program, dependencies and run transcripts (5.2.0/5.1.0/5.0.3 JVM and Android,
4.14.7 Android):
[`examples/minimal-app.md`](examples/minimal-app.md).

## Concurrency and threading model

[concurrency.md](references/concurrency.md) has the per-API suspend/thread table. Core rules:

- **Handlers start on the SDK scope: main thread on Android (`MainScope()`),
  `Dispatchers.Default` on JVM.** Hop with `withContext(Dispatchers.IO)` *inside* the
  handler; **`.flowOn()` does not reach the `observe()` transform**.
- Handlers are serialized with back-pressure: never `launch` per event or `.buffer()`;
  use `.conflate()`/`stateIn` for latest-only UI.
- `create`, `sync.start()`, `registerSubscription`, `registerObserver` are not suspend;
  `store.execute`, `auth.login` and attachment fetches are. `expirationHandler` is a
  suspend lambda: call `login` directly in it, never inside `launch { }`.

## Object lifetimes and retention

One `Ditto` per process, owned by `Application`/a DI singleton (Android) or a top-level
holder (JVM); closing it closes every child resource. Retain `DittoSyncSubscription`
and `registerObserver` handles so you can `close()` them; **never retain
`DittoQueryResult` or its items** — they die when the handler returns
(`IllegalStateException: Query result item has already been closed.`). Flows from
`observe()`/`collect()` need no handle: the collecting scope is the lifetime. Do not
cache `ditto.sync.subscriptions` or `ditto.store.observers`; they are live views. Handle
table and per-component cleanup: [lifetimes.md](references/lifetimes.md).

## Anti-patterns

Read [anti-patterns.md](references/anti-patterns.md) for wrong/right forms.

- Returning `result.items` from a handler: `Query result item has already been closed.`
- An exception escaping a `registerObserver` handler **closes the observer** (logged only).
- Casting `item.value["x"]` directly: `ClassCastException`; use `jsonString()`.
- Plain `INSERT` of an existing `_id`: `Identifier conflict … FAIL conflict policy`.
- JVM without `ditto-binaries`: `Unable to find binary 'libdittoall…'` on create.

`.buffer()`, `launch`-per-event, `flowOn` and `setExpirationHandler` mistakes are covered there too.

## Version differences

| Concern | 4.14.x | 5.0.x / 5.1.x / 5.2.x |
|---|---|---|
| Package / namespace | `live.ditto:ditto`, `live.ditto.*` (Android-only) | `com.ditto:ditto-kotlin`, `com.ditto.kotlin.*` (Android + JVM) |
| Initialization | `Ditto(deps, DittoIdentity.…)` | `DittoFactory.create(DittoConfig(…))`, not suspend |
| Start sync | `ditto.startSync()` | `ditto.sync.start()` |
| Mutating DQL | requires `ditto.disableSyncWithV3()` first (else `StoreError: … disable sync with V3 …`, executed) | works by default |
| Query model | legacy collection API (deprecated) + DQL | DQL only, via `ditto.store.execute` |
| Observers | non-suspend callback, `DittoSignalNext` | suspend handler / `observe()` Flow / `collect()` |
| Errors | `DittoError` | `DittoException` sealed hierarchy |
| On-disk store | default dir `ditto` | default dir `ditto-{databaseId}` for new stores; a default-path v4 store is picked up |

Full delta, on-disk migration and removed-API table: [`references/versions.md`](references/versions.md).

## References

Pick one row; these are alternatives, not a reading list.

| Task | Read |
|---|---|
| Install, platform minimums | [setup.md](references/setup.md) |
| Open, authenticate, start sync | [connect.md](references/connect.md) |
| Threads and hopping | [concurrency.md](references/concurrency.md) |
| Retain or close | [lifetimes.md](references/lifetimes.md) |
| Diagnose a symptom | [anti-patterns.md](references/anti-patterns.md), then [errors.md](references/errors.md) |
| Transports | [transports.md](references/transports.md) |
| Subscriptions, sync status | [sync.md](references/sync.md) |
| DQL, transactions, indexes, evict | [store.md](references/store.md) |
| Observers, Flows, diffing | [observers.md](references/observers.md) |
| Attachments | [attachments.md](references/attachments.md) |
| Presence | [presence.md](references/presence.md) |
| Logs, disk usage | [observability.md](references/observability.md) |
| Testing | [testing.md](references/testing.md) |
| 4.14.x vs 5.x API and on-disk changes | [versions.md](references/versions.md) |
| Preview/platform APIs | [preview.md](references/preview.md) |
| Data Streams (preview) | [data-streams.md](references/data-streams.md); concepts in `data-streams` |
| Generate a Gradle project | [gradle-project-generation.md](references/gradle-project-generation.md) |
| Tested Gradle build files | [reference-projects.md](references/reference-projects.md) |
| Instance placement, observer shape | [best-practices.md](best-practices.md) |
| Complete example | [minimal-app.md](examples/minimal-app.md) (compiled and run) |

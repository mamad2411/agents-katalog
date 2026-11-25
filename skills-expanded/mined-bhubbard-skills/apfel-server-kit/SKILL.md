---
name: apfel-server-kit
description: Reference for building Swift apps that talk to a local "apfel" process (Apple's on-device LLM CLI, from Arthur-Ficial/franzai.com) using the ApfelServerKit Swift package. Use this skill whenever the user is writing Swift/SwiftUI code that needs to discover, launch, health-check, or stream chat completions from a local `apfel --serve` process — for example building a macOS chat client, a menu-bar AI tool, a Spotlight-style overlay, or any native app that should use on-device AI instead of a cloud API. Trigger on mentions of ApfelServerKit, ApfelServer, ApfelClient, "spawn apfel from Swift", or "build a macOS app on top of apfel". Do not use this for someone using `apfel` from the terminal or shell scripts — that's the apfel-cli-tools skill; this one is specifically for Swift/SwiftUI app development.
---

# apfel-server-kit

`ApfelServerKit` is the shared Swift package that the `apfel` app ecosystem (apfel-quick, apfelpad, apfel-chat, apfel-clip, apfel-gui) all depend on, so app-specific code doesn't reinvent the same subprocess-lifecycle, port-scanning, SSE-parsing, and health-polling logic. The maintainer extracted it after five tools each independently wrote ~320 lines of the same code (see github.com/Arthur-Ficial/apfel/issues/106). If the user is building a new Swift app that needs to drive a local `apfel` process, start here instead of writing that plumbing from scratch.

**Requirements:** Swift 6.0+, macOS 14+. Builds with Command Line Tools — no Xcode required for the package itself (though a GUI app consuming it will typically use Xcode/SwiftUI).

## Install

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/Arthur-Ficial/apfel-server-kit.git", from: "1.0.0"),
],
targets: [
    .target(
        name: "YourTool",
        dependencies: [
            .product(name: "ApfelServerKit", package: "apfel-server-kit"),
        ]
    ),
]
```

## Quick start

```swift
import ApfelServerKit

let server = ApfelServer()
let port = try await server.start()
defer { Task { await server.stop() } }

let client = ApfelClient(port: port)
for try await delta in client.stream(prompt: "Say hi in three words.") {
    if let text = delta.text { print(text, terminator: "") }
}
```

`ApfelServer.start()` looks for an `apfel` binary, launches `apfel --serve`, and polls `/health` until it's ready, returning the port it landed on. If an `apfel` server is *already* running inside the configured port range and answers `/health`, `start()` just connects to it instead of spawning a second process, and sets `isManaged = false` — in that case `stop()` becomes a no-op, so you never accidentally kill a server your app doesn't own.

## What's in the package

| Type | Purpose |
|---|---|
| `ApfelServer` (actor) | Discover `apfel`, find a free port, spawn `apfel --serve`, poll `/health`, terminate on `stop()`. |
| `ApfelClient` | Stream `/v1/chat/completions` as `TextDelta` values; non-streaming health check. |
| `SSEParser` | Parse individual Server-Sent Event lines into typed `SSEEvent` values — reusable if you're rolling your own client on top of the raw endpoint. |
| `ApfelBinaryFinder` | Locate `apfel` across `PATH`, app bundle, Homebrew, `/usr/local/bin`, `~/.local/bin`. |
| `ChatRequest` | Minimal OpenAI-compatible chat request type — use directly or convert from apfel's fuller request types. |
| `ApfelServerError` | Typed errors: `.binaryNotFound`, `.noPortAvailable`, `.spawnFailed`, `.healthCheckTimeout` — check which one before writing generic "something went wrong" error UI. |

## Configuration

```swift
let server = ApfelServer(
    portRange: 11450...11459,             // default
    healthTimeout: .seconds(8),           // default
    arguments: ["--cors", "--permissive"] // default
)
```

Widen `portRange` if the default range might collide with another local service, and raise `healthTimeout` on first-run scenarios where the on-device model may still be initializing.

## Design principles to preserve if extending the package

- **100% local.** Only ever talks to `127.0.0.1`. Don't add code paths that reach external hosts — that would break the whole apfel privacy story.
- **Swift 6 strict concurrency.** `ApfelServer` is an `actor`; anything crossing concurrency domains must be `Sendable`.
- **TDD, no XCTest.** Tests run via `swift run apfel-server-kit-tests`, a pure-Swift runner matching the pattern `apfel` itself uses — mirror this if contributing.
- **Dependency-free.** Uses only `URLSession`, `Process`, `Darwin.bind()` — no Hummingbird or ApfelCore coupling. Keep it that way; it's meant to be a lightweight leaf dependency.
- **Honest errors.** Prefer extending `ApfelServerError` with a specific new case over stringly-typed error messages.
- **Stable public API.** `swift package diagnose-api-breaking-changes` runs in CI — see STABILITY.md before changing any public signature.

## Testing your integration

```bash
swift build -c release
swift test                    # fast, model-free
```

Full docs: `swift package generate-documentation --target ApfelServerKit`. Repo: https://github.com/Arthur-Ficial/apfel-server-kit

## Related, if the user's actual need is different

- Wants to run `apfel` from the terminal or a shell script, not Swift → use the `apfel-cli-tools` skill instead.
- Wants an existing finished app rather than to build one → point them at `apfel-quick` or `apfelpad` (see the `apfel-gui-apps` skill).
- Building the MCP/web-search layer rather than the chat client → that's `apfel-mcp`, covered in `apfel-cli-tools`.

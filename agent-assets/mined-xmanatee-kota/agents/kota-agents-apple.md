# Apple Clients (macOS + iOS)

Native KOTA clients for macOS and iOS. The package is one Swift
package contributing three targets so daemon transport, view-models,
and SwiftUI views are written once for both platforms:

- `KotaShared`  : library — daemon client, contract decoders,
  `AppState` view-model, platform protocols, and the SwiftUI views
  shared by both shells.
- `KotaMenuBar` : macOS executable — `MenuBarExtra` shell, AppKit-
  backed `MacOSPlatform`.
- `KotaiOS`     : iOS executable — `WindowGroup` + `TabView` shell,
  and UIKit-backed `iOSPlatform`.

## Conventions

- All state comes from the daemon API through the daemon client
  wrapper. Views should not scatter route strings, auth handling, or
  response decoding.
- Local and remote daemon discovery share the same connection model.
  Secrets belong in Keychain, not view state or committed files.
- If the daemon is unreachable, clear live data and show an offline
  state instead of preserving stale runtime state.
- Daemon-backed screens use the Swift-native `ResourceStateOwner` and
  `ResourceStateShell`; keep interaction state such as chat streaming, form
  editing, action confirmation, and voice capture in its domain owner.
- Do not add Swift Package dependencies without a strong reason. The
  apps are intentionally minimal.
- Voice goes through the daemon's `/voice/transcribe` and
  `/voice/synthesize` routes. Microphone capture uses
  `AVAudioRecorder`; playback uses `AVAudioPlayer`. Never import a TTS
  or STT vendor SDK in the app.

## Platform Shell Boundary

The shared module never imports `AppKit` or `UIKit`. Platform-
specific affordances (NSOpenPanel, NSWorkspace, UIApplication,
terminate) are routed through the `PlatformAffordances` protocol declared in
`Sources/KotaShared/PlatformAffordances.swift`. Each shell wires its own
concrete implementation:

- macOS — `MacOSPlatform` in `Sources/KotaMenuBar/`.
- iOS — `iOSPlatform` in `Sources/KotaiOS/`.

Each shell file is wrapped in `#if os(macOS)` / `#if os(iOS)` so the
opposite platform's executable target still compiles cleanly when
`xcodebuild` against the package builds every scheme. The wrapped-out
target falls back to a `_Stub` `@main` that aborts with a clear
message if invoked on the wrong platform.

## Daemon Contract Layout

`DaemonClient.swift` owns connection state, the error envelope, and shared
request helpers. `Sources/KotaShared/Daemon/` contains only wire contracts for
native responsibilities: identity and health, shared UI/SSE,
chat/voice, slash commands, and session termination. Operator capabilities
such as setup, workflows, knowledge, memory, and task control are rendered and
executed exclusively through `ui.surface.v1`; do not add direct Apple routes
for them.

- Identity and scope registry use the generated daemon contract.
  `ui.surface.v1` lives under `Generated/` and is regenerated from the daemon
  TypeScript contract with `pnpm
  build:ui-bindings`; never mirror that protocol by hand.

## Build & Test

- macOS app bundle: `./build-macos.sh` — wraps
  `swift build -c release` into a runnable `KotaMenuBar.app` with
  `LSUIElement=true`.
- iOS Simulator app: `./build-ios.sh` — wraps `xcodebuild` against
  the iPhone 17 Pro simulator destination.
- Cross-platform tests: `swift test` (macOS host) runs the full
  `KotaSharedTests` suite; compiling the executables verifies shell construction. To run the same
  shared suite on iOS, use
  `xcodebuild test -scheme KotaApple-Package -destination 'platform=iOS Simulator,name=iPhone 17 Pro'`
  — this exercises the same view-model and decoder code on the iOS
  runtime.

## Verification ownership

Retain platform navigation, accessibility, interaction, trust, confirmation,
rendering, and transport boundaries. Shared resource transitions and generated
wire shapes are proved at their owner; do not repeat their matrices per screen
or enumerate fixture catalogs. Client composition journeys keep production
providers, navigation, and transport, with doubles only at network and device
ports. Pure view construction is compiler proof, not rendered evidence.

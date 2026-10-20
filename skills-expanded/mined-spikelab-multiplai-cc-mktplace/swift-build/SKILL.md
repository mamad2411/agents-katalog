---
name: swift-build
description: |
  Build, test, and manage iOS/macOS projects. Requires macOS — it drives the
  Swift/Xcode toolchain (xcodebuild, xcrun/simctl), which exists only there.
  Runs the toolchain directly on a Mac; from a Docker container with a
  configured host bridge it routes the same commands to a macOS host over SSH.
  Not usable on Linux. Claude calls the script, reads structured output,
  never touches SSH directly.
when_to_use: 'Triggers: swift build, swift test, run tests (Swift project context), simulator, xcodebuild'
disable-model-invocation: false
---

# Swift Build Skill

Build and test Swift/iOS/macOS projects.

**macOS is required.** Everything here drives the Swift/Xcode toolchain — `xcodebuild`, `xcrun`/`simctl`, the iOS SDKs — and Apple ships it for macOS only. There is no Linux port and no fallback: on a Linux host the script names the missing toolchain and exits 1.

Two supported environments, both ending on a Mac:

- **macOS** — the toolchain runs locally. Nothing to configure.
- **A Docker container with a configured host bridge** (e.g. multiplai-kit's opt-in container→host SSH bridge) — the same commands are routed to a macOS host over SSH. Without that bridge configured, the container path also exits 1.

## How It Works

All commands go through a single script: `${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh`

The script handles environment detection, project detection, and output formatting. You call it; it figures out the rest.

### --package-path Flag

Use `--package-path <dir>` to target a Swift package in a different directory without `cd`:

```bash
# From any directory — works in containers without gateway cd issues
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh --package-path /path/to/ios build
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh --package-path /path/to/ios test
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh --package-path /path/to/ios test --filter MyTests
```

This is the **preferred approach in containers** — it uses `swift build --package-path` / `swift test --package-path` over SSH, which matches the gateway allowlist directly (no `cd` pattern needed).

## Environment Detection

The script detects where it's running:

| Environment | Detected by | Behavior |
|-------------|-------------|----------|
| Local macOS | `uname -s` = `Darwin` | Commands run directly — no SSH config needed |
| Container | `MULTIPLAI_CONTAINER=1` (set by the multiplai container image) or `/.dockerenv` | Commands SSH to the macOS host bridge |
| Plain Linux | anything else | Unsupported — the error explains Swift/Xcode builds need macOS |

**You do not need to detect the environment yourself.** Just run the script — it handles routing.

### SSH Configuration (Container Only)

The script reads these environment variables (all have sensible defaults matching `dclaude.sh`):

| Variable | Default | Purpose |
|----------|---------|---------|
| `SWIFT_BUILD_HOST` | `host.docker.internal` | macOS host address |
| `SWIFT_BUILD_USER` | `$SSH_BUILD_USER` from `.env` (required) | SSH username |
| `SWIFT_BUILD_KEY` | `/home/agent/.ssh/build_key` | SSH private key path |

## Project Detection

The script auto-detects project type from files in the current directory:

| Files Found | Project Type | Build Tool |
|-------------|-------------|------------|
| `Package.swift` only | `swiftpm` | `swift build` / `swift test` |
| `*.xcodeproj` or `*.xcworkspace` only | `xcode` | `xcodebuild` (auto-discovers scheme) |
| Both `Package.swift` and `*.xcodeproj` | `hybrid` | Prefers SwiftPM (`swift build` / `swift test`) |

For Xcode projects, the scheme is auto-discovered via `xcodebuild -list`.

## Commands

### Build

```bash
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh build
```

Builds the project. SwiftPM → `swift build`. Xcode → `xcodebuild -scheme <auto> -sdk iphonesimulator build`.

### Test

```bash
# Run all tests
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh test

# Run filtered tests
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh test --filter MyTestClass
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh test --filter MyTestClass/testSpecificMethod
```

For SwiftPM, `--filter` maps to `swift test --filter`. For Xcode, it maps to `-only-testing:`.

### Simulator Management

```bash
# List available simulators
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh sim list

# Boot a simulator
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh sim boot "iPhone 16 Pro"

# Open Simulator.app GUI (so the user can see/interact with the device)
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh sim open

# Install an app on the booted simulator
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh sim install /path/to/MyApp.app

# Launch an app by bundle identifier
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh sim launch com.example.MyApp

# Shutdown a simulator
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh sim shutdown

# Take a screenshot of the booted simulator
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh sim screenshot /tmp/screen.png
```

**`sim screenshot` path caveat (bridged mode):** the screenshot is written
on the **macOS host**, not in the container — the default
`/tmp/simulator-screenshot.png` lands in the host's `/tmp`, which the
container cannot read. To view the image from the container, pass a path
inside the shared workspace mount (same absolute path on both sides), e.g.
`sim screenshot /path/to/workspace/tmp/screen.png`.

For detailed simulator commands beyond what the script wraps, load `references/simulator-management.md`.

### UI Testing & Screenshots

Run an XCUITest bundle and pull the captured screenshots back out — the agent
self-verification workhorse for macOS/iOS GUI work (launch the app, drive it,
*see* the result). Uses only already-allowed commands (`xcodebuild`, `xcrun
xcresulttool`) — no gateway change.

```bash
# iOS simulator — no login session or TCC grant needed:
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh --package-path app uitest \
  --scheme MyUITests --destination 'platform=iOS Simulator,name=iPhone 17'

# macOS — real window chrome + gestures; needs an active login session AND a
# one-time Accessibility/Automation TCC grant to the test runner:
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh --package-path app uitest \
  --scheme MyUITests --destination 'platform=macOS'

# Extract XCTAttachment PNGs from the result bundle (either destination):
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh --package-path app screenshots
#   → app/.uitest-artifacts/screenshots/*.png  (+ manifest.json)
```

- `uitest` defaults the result bundle to `<pkg>/.uitest-artifacts/result.xcresult`
  (override `--result-bundle`); it cleans that path first (xcodebuild refuses a
  pre-existing `-resultBundlePath`). `--only-testing <ID>` narrows the run.
- `screenshots` reads that same default bundle; `--output`, `--test-id`, and
  `--only-failures` narrow the export.
- Put the result bundle / output **inside the workspace mount** (the defaults
  do) so the container can `Read` the PNGs at the same path.
- In the test, set `attachment.lifetime = .keepAlways` or a **green** run
  discards the screenshots.

For headless component snapshots that need no UI target at all (the cheaper
first tier), render with `ImageRenderer` inside `swift test` — see the target
project's self-verification docs.

### Tool Passthrough

`swift`, `xcodebuild`, and `xcrun` are accepted as top-level commands and
forwarded to the host verbatim (shell-quoted, run from the optional
`--package-path` dir). Use for host diagnostics/repair and custom builds:

```bash
# Diagnostics — raw output IS the answer, never wrapped
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh xcodebuild -version
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh xcrun simctl list devices

# Full build through the passthrough — add --xcsift (first arg after the
# tool name) to pipe output through xcsift and save tokens. Errors and
# warnings survive; only build noise is dropped.
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh --package-path /path/to/pkg \
  swift --xcsift build --sdk "$SIM_SDK" -Xswiftc -target -Xswiftc arm64-apple-ios17.0-simulator
```

**Rule of thumb:** pass `--xcsift` whenever the invocation compiles code;
omit it when you need to read the tool's own output (versions, build
settings, device lists).

## Output Parsing

All build/test output is piped through **xcsift** (if installed on the host) using `--format toon --quiet`.

### TOON Format

TOON is a compact, LLM-friendly format that uses 30-60% fewer tokens than JSON. Example:

```
🔴 ERROR MyApp/ContentView.swift:42
  Cannot convert value of type 'String' to expected argument type 'Int'

⚠️ WARNING MyApp/AppDelegate.swift:15
  Result of call to 'load()' is unused

✅ TEST PASSED MyAppTests/ContentViewTests/testInitialState (0.003s)

🔴 TEST FAILED MyAppTests/ContentViewTests/testButtonTap (0.012s)
  XCTAssertEqual failed: ("Hello") is not equal to ("Goodbye")
  at MyAppTests/ContentViewTests.swift:28
```

### Reading Results

- **Build succeeded:** No output (due to `--quiet`). Exit code 0.
- **Build failed:** Only errors and warnings shown. Exit code non-zero.
- **Tests passed:** No output (due to `--quiet`). Exit code 0.
- **Tests failed:** Only failures shown with file:line and assertion message. Exit code non-zero.
- **xcsift not installed:** Raw xcodebuild/swift output with a `WARNING:` line. Still functional, just noisier.

### Exit Codes

Exit codes propagate through xcsift (`set -o pipefail`). Check `$?`:
- `0` = success
- Non-zero = build/test failure

## Usage Pattern

When working on a Swift project:

1. **First, check the environment works:**
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh sim list
   ```
   If this returns simulators, the SSH bridge (or local toolchain) is working.

2. **Build to check compilation:**
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh build
   ```

3. **Run tests:**
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh test
   ```

4. **Run specific tests during TDD:**
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh test --filter TestClassName/testMethodName
   ```

## Autonomous TDD Integration

When using the `autonomous-tdd` skill on a Swift project, the test command is:

```
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh --package-path /absolute/path/to/project test
```

This is auto-detected by autonomous-tdd's stack detection (Step 2) when it finds `Package.swift` or `*.xcodeproj`.

To filter tests in TDD phases, subagents append `--filter`:

```
${CLAUDE_PLUGIN_ROOT}/skills/swift-build/scripts/swift-host.sh --package-path /absolute/path test --filter FeatureTests
```

**Always use `--package-path` with absolute paths in TDD agents** — subagents may not inherit the working directory.

## Gateway Compatibility

When running from a container, all commands the script sends over SSH are compatible with the `~/.local/bin/container-build-gateway.sh` allowlist:

- `swift build`, `swift test --filter ...`, `swift --version`
- `xcodebuild -scheme ... build`, `xcodebuild -scheme ... test`, `xcodebuild -list -quiet` (scheme discovery — `xcodebuild` is allowlisted by command prefix, so any subcommand is accepted)
- `command -v xcsift` (probes whether the xcsift formatter is installed on the host)
- `xcrun simctl list devices available`, `xcrun simctl boot ...`, `xcrun simctl io ...`, `xcrun simctl install ...`, `xcrun simctl launch ...`, `xcrun simctl shutdown ...`
- `xcodebuild test -scheme ... -destination ... -resultBundlePath ...` (the `uitest` verb) and `xcrun xcresulttool export attachments --path ... --output-path ...` (the `screenshots` verb) — both allowlisted by command prefix, no gateway change
- `open -a Simulator` (for opening the Simulator GUI)
- `cd /path && <any of the above>`
- The `2>&1 | xcsift --format toon --quiet` suffix: the gateway rejects raw pipes/redirects as shell metacharacters, but it special-cases this one **fixed, trusted suffix** — it strips it before the metacharacter check, validates the head command, then re-attaches the xcsift stage host-side as a hardcoded constant. So only this exact suffix pipes; arbitrary pipes are still denied. (Do **not** send any other redirect/pipe over the bridge — e.g. `2>/dev/null` is denied.)

### Known gateway limitations (bridged mode only)

Until the gateway-side unquoting fix ships in multiplai-container, the
gateway re-parses the quoted command string in a way that breaks on:

- **Project paths containing spaces** — the `cd '/path with spaces' && …`
  pattern is mis-split/denied. Keep container-built Swift projects at
  space-free paths for now.
- **Xcode scheme names containing parentheses** (e.g. `MyApp (iOS)`) — the
  quoted scheme is rejected as shell metacharacters. Rename the scheme or
  build that project locally on the Mac.

These are gateway limitations, not script bugs — `swift-host.sh` quotes
correctly; the fix belongs to `container-build-gateway.sh` (tracked in the
multiplai-container repo). Local macOS use is unaffected.

## Constraints

- **NEVER use raw SSH.** Do not call `ssh` directly. All host communication goes through `swift-host.sh`. The script handles hostname, key discovery, and gateway compatibility. Raw SSH will fail — the host uses an SSH gateway that only allows specific commands.
- **NEVER tell the user to run commands manually.** If a command isn't available through the script, add it to the script and the gateway — don't give up and dump shell commands on the user.
- **Path assumption:** The project directory must be at the same path on both the container and the host. This is the case with `dclaude.sh` which mounts at the identical path.
- **No interactive sessions:** The SSH gateway denies interactive shells. All commands must be non-interactive.
- **Scheme discovery:** For Xcode projects, `xcodebuild -list` must return at least one scheme. If the project hasn't been opened in Xcode yet, this may fail — open it once on the host first.

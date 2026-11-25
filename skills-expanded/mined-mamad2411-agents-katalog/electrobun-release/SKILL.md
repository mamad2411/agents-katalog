---
name: electrobun-release
description: "Build, package, sign, and distribute Electrobun apps. Covers CLI commands (init, build, dev, ship), code signing, notarization, Updater API, bsdiff patches, and release channels. Use when building, packaging, or updating Electrobun applications."
---

# Electrobun Release & Distribution

> **Electrobun is NOT Electron.** It uses Bun as its JS runtime, CEF or native WebView for rendering, and Zig for native components.

## Mental Model

```
Build pipeline:    TypeScript → Bun.build() bundle → native wrapper → platform package
Distribution:      self-extracting archives (.app/.exe/binary), bsdiff delta patches, zstd compression
Update flow:       checkForUpdate() → downloadUpdate() → applyUpdate() → quit & relaunch
Channels:          stable, canary, dev (dev disables updates)
Artifact hosting:  Static file server (S3, R2, CDN) — no dynamic backend required
```

## Decision Tree

| Need | Action |
|---|---|
| Starting new project | `electrobun init [project-name] [--template=<name>]` |
| Development with hot reload | `electrobun dev --watch` |
| Development (single run) | `electrobun dev` |
| Launch already-built dev bundle | `electrobun run` |
| Building for release | `electrobun build --env=canary` or `--env=stable` |
| Checking for updates in app | `Updater.checkForUpdate()` |
| Downloading an update | `Updater.downloadUpdate()` |
| Applying a downloaded update | `Updater.applyUpdate()` (separate call — NOT part of download) |
| Code signing (macOS) | Set `ELECTROBUN_DEVELOPER_ID` + `build.mac.codesign: true` |
| Notarization (macOS) | Set notarization env vars + `build.mac.notarize: true` |
| Reading build metadata at runtime | `Updater.localInfo.version()`, `.hash()`, `.channel()` |

## CLI Commands

### `electrobun init`

```bash
# Interactive — prompts for template selection
electrobun init

# Direct — template name becomes project name
electrobun init photo-booth

# Explicit template + project name
electrobun init my-project --template=photo-booth
```

Templates are embedded in the CLI binary. Creates project directory, extracts files, prints next steps.

### `electrobun dev`

```bash
# Build and launch once
electrobun dev

# Watch mode — rebuild + relaunch on file changes (300ms debounce)
electrobun dev --watch
```

Watch mode monitors: bun entrypoint dirs, view dirs, copy source dirs, user-configured `watch` paths. Ignores: build output, artifacts, `node_modules`, `watchIgnore` globs.

### `electrobun build`

```bash
# Dev build (default, no packaging/signing)
electrobun build

# Canary channel — full packaging, signing, delta patches
electrobun build --env=canary

# Stable channel — production release
electrobun build --env=stable
```

Non-dev builds produce: signed app bundle, compressed tarball (`.tar.zst`), bsdiff delta patch, self-extracting installer, DMG (macOS) / zip-wrapped exe (Windows) / tar.gz (Linux), `update.json` manifest.

### `electrobun run`

```bash
# Launch an already-built dev bundle without rebuilding
electrobun run
```

### Build Pipeline (17 steps)

1. Run `preBuild` hook
2. Create app bundle structure (`AppName.app/Contents/{MacOS,Resources,Frameworks}/` on macOS)
3. Write `Info.plist` (macOS)
4. Copy runtime binaries (launcher, bun, native wrapper, bspatch, zig-zstd, libasar)
5. Embed icons (`.iconset` → `.icns` on macOS, PNG on Linux, `.ico` via rcedit on Windows)
6. Bundle CEF (if `bundleCEF: true`)
7. Bundle WGPU/Dawn (if `bundleWGPU: true`)
8. Transpile app code — `Bun.build()` for bun process + each view
9. Run `postBuild` hook
10. ASAR packaging (if `useAsar: true`)
11. Content hashing (wyhash of in-memory tar)
12. Write `version.json` + `build.json`
13. Code sign (macOS, non-dev)
14. Notarize (macOS, non-dev)
15. Package: tar → bsdiff patch → zstd compress → self-extracting installer → DMG/zip/tar.gz
16. Write artifacts with platform prefix naming
17. Run `postPackage` hook

## Config (`electrobun.config.ts`)

```typescript
export default {
  app: {
    name: "MyApp",
    identifier: "com.example.myapp",   // Reverse-domain, used for data isolation
    version: "1.0.0",
    urlSchemes: ["myapp"],              // Custom URL scheme handlers
  },
  build: {
    buildFolder: "build",
    artifactFolder: "artifacts",
    useAsar: true,
    asarUnpack: ["*.node", "*.dll", "*.dylib", "*.so"],
    mac: {
      codesign: true,
      notarize: true,
      createDmg: true,
      bundleCEF: true,
      bundleWGPU: false,
      entitlements: {},                 // Merged with required defaults
      icons: "icon.iconset",
    },
    win: { bundleCEF: true, icon: "icon.ico" },
    linux: { bundleCEF: true, icon: "icon.png" },
    bun: { entrypoint: "src/bun/index.ts" },
    views: {
      main: { entrypoint: "src/views/main/index.ts" },
    },
    copy: { "assets/": "assets/" },
    watch: ["extra-dir/"],
    watchIgnore: ["**/*.log"],
  },
  scripts: {
    preBuild: "./scripts/pre.ts",
    postBuild: "./scripts/post.ts",
    postWrap: "./scripts/wrap.ts",      // Receives ELECTROBUN_WRAPPER_BUNDLE_PATH
    postPackage: "./scripts/package.ts",
  },
  release: {
    baseUrl: "https://cdn.example.com/releases",   // Static file host for updates
    generatePatch: true,                            // bsdiff delta patches
  },
};
```

### Lifecycle Hook Environment Variables

Scripts receive: `ELECTROBUN_BUILD_ENV`, `ELECTROBUN_OS`, `ELECTROBUN_ARCH`, `ELECTROBUN_BUILD_DIR`, `ELECTROBUN_APP_NAME`, `ELECTROBUN_APP_VERSION`, `ELECTROBUN_APP_IDENTIFIER`, `ELECTROBUN_ARTIFACT_DIR`. The `postWrap` hook also gets `ELECTROBUN_WRAPPER_BUNDLE_PATH`.

## Updater API

The `Updater` is a singleton object (not a class). Import from Electrobun's core.

### Check → Download → Apply

```typescript
import { Updater } from "electrobun/bun";

// 1. Check for updates
const result = await Updater.checkForUpdate();
// Returns: { version, hash, updateAvailable, updateReady, error }

if (result.updateAvailable) {
  // 2. Download update (tries bsdiff patches first, falls back to full download)
  await Updater.downloadUpdate();
  // Sets updateReady: true when complete. Does NOT apply the update.

  // 3. Apply update — extracts, replaces app bundle, quits, and relaunches
  // This is a SEPARATE call. It calls quit() internally and never returns.
  await Updater.applyUpdate();
}
```

### Progress Tracking

```typescript
// Real-time status updates
Updater.onStatusChange((entry) => {
  console.log(`[${entry.status}] ${entry.message}`);
  if (entry.details?.progress) {
    console.log(`Progress: ${entry.details.progress}%`);
  }
});

// Full history
const history = Updater.getStatusHistory();

// Clear history
Updater.clearStatusHistory();

// Unregister callback
Updater.onStatusChange(null);
```

### Status Flow

```
Check:    idle → checking → update-available | no-update | error
Download: download-starting → checking-local-tar → fetching-patch → downloading-patch
          → applying-patch → patch-chain-complete (or downloading-full-bundle → decompressing)
          → download-complete
Apply:    applying → extracting → replacing-app → launching-new-version → complete
```

### Build Metadata (Async Accessors)

```typescript
const version = await Updater.localInfo.version();   // "1.0.0"
const hash    = await Updater.localInfo.hash();       // build content hash
const channel = await Updater.localInfo.channel();    // "stable" | "canary" | "dev"
const baseUrl = await Updater.localInfo.baseUrl();    // artifact distribution URL

const info    = Updater.updateInfo();                 // cached { version, hash, updateAvailable, updateReady, error }
const dataDir = await Updater.appDataFolder();        // ~/Library/Application Support/{identifier}/{channel}/
```

## Release Channels

| Channel | Artifact Suffix | Updates | App Data Path |
|---|---|---|---|
| `stable` | (none) | ✅ Enabled | `{identifier}/stable/` |
| `canary` | `-canary` | ✅ Enabled | `{identifier}/canary/` |
| `dev` | `-dev` | ❌ Disabled | `{identifier}/dev/` |

Each channel is fully isolated: separate app data directory, CEF cache, self-extraction directory, and update artifacts.

### Artifact Naming

Platform prefix format: `{channel}-{os}-{arch}` (e.g., `canary-macos-arm64`)

```
canary-macos-arm64-update.json
canary-macos-arm64-MyApp.app.tar.zst
canary-macos-arm64-abc123def456.patch
```

## Code Signing (macOS Only)

### Environment Variable

```bash
export ELECTROBUN_DEVELOPER_ID="Developer ID Application: Your Name (TEAMID)"
```

### Config

```typescript
build: {
  mac: {
    codesign: true,
    entitlements: {
      // Custom entitlements merged with required defaults:
      //   com.apple.security.cs.allow-jit: true
      //   com.apple.security.cs.allow-unsigned-executable-memory: true
      //   com.apple.security.cs.disable-library-validation: true
    },
  },
}
```

### Signing Order (Critical)

1. CEF framework `.dylib` files
2. `.framework` bundles
3. CEF helper apps (GPU, Plugin, Alerts, Renderer)
4. All Mach-O binaries in `MacOS/`
5. `.node` native modules in `Resources/app/bun/`
6. `MacOS/launcher` (with bundle identifier)
7. App bundle itself (final seal, no `--deep`)

**Three things are separately signed and notarized:** inner app bundle, self-extracting wrapper, DMG.

## Notarization (macOS Only)

### Authentication (choose one)

**Option A — App Store Connect API Key (preferred for CI):**
```bash
export ELECTROBUN_APPLEAPIISSUER="issuer-id"
export ELECTROBUN_APPLEAPIKEY="key-id"
export ELECTROBUN_APPLEAPIKEYPATH="/path/to/AuthKey.p8"
```

**Option B — Apple ID Credentials:**
```bash
export ELECTROBUN_APPLEID="you@example.com"
export ELECTROBUN_APPLEIDPASS="app-specific-password"
export ELECTROBUN_TEAMID="TEAMID"
```

### Config

```typescript
build: {
  mac: {
    codesign: true,    // Required — notarize requires codesign
    notarize: true,
  },
}
```

### Process

1. Zips `.app` bundle → `xcrun notarytool submit --wait` → staples ticket via `xcrun stapler staple`
2. On failure: fetches notarization log, prints it, exits with error
3. Only runs when: `--env` is not `dev`, target is macOS, host is macOS, both `codesign` and `notarize` are true

### CI Setup

```bash
echo $MACOS_CERTIFICATE | base64 --decode > certificate.p12
security create-keychain -p actions build.keychain
security import certificate.p12 -k build.keychain -P $MACOS_CERTIFICATE_PWD \
  -T /usr/bin/codesign -T /usr/bin/productbuild
security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k actions build.keychain
```

## bsdiff Delta Updates

### How It Works

**Build time:** Downloads previous version's tarball from `baseUrl`, runs `bsdiff` to generate `{prevHash}.patch`.

**Runtime:** Patch chain — applies sequential patches until reaching the latest hash, falls back to full download if any patch is missing or fails.

```
currentHash → fetch {currentHash}.patch → bspatch → read nextHash from patched tar → repeat
  until nextHash === latestHash  →  patch-chain-complete
  or patch not found / failed   →  download full .tar.zst bundle
```

Cycle detection via `seenHashes` array prevents infinite loops.

### Update Server (Static Files)

| File | URL Pattern |
|---|---|
| Update manifest | `{baseUrl}/{channel}-{os}-{arch}-update.json` |
| Full bundle | `{baseUrl}/{channel}-{os}-{arch}-{AppName}.app.tar.zst` |
| Delta patch | `{baseUrl}/{channel}-{os}-{arch}-{prevHash}.patch` |

`update.json` format: `{ "version": "1.0.0", "hash": "abc123...", "platform": "macos", "arch": "arm64" }`

## Non-Negotiable Rules

1. **Channel flag syntax:** Use `electrobun build --env=canary`, NOT `electrobun build canary` (positional).
2. **`applyUpdate()` is separate from `downloadUpdate()`:** Download prepares the update and sets `updateReady: true`. Apply extracts, replaces, and relaunches. They are two distinct method calls.
3. **Only `stable`, `canary`, and `dev` channels are accepted by the CLI.** Unrecognized `--env` values silently fall back to `"dev"`.
4. **Code signing and notarization are macOS only.** Windows and Linux code signing are not implemented.
5. **All build commands for end-user apps run from the project root** (where `electrobun.config.ts` lives), not from the `package/` directory.

## Common Pitfalls

### 1. Forgetting signing environment variables

```bash
# ❌ Build fails silently or produces unsigned bundle
electrobun build --env=stable

# ✅ Set ELECTROBUN_DEVELOPER_ID before building
export ELECTROBUN_DEVELOPER_ID="Developer ID Application: ..."
electrobun build --env=stable
```

### 2. Wrong channel syntax

```bash
# ❌ WRONG — positional channel argument
electrobun build canary

# ✅ CORRECT — use --env flag
electrobun build --env=canary
```

### 3. Calling applyUpdate() without downloadUpdate()

```typescript
// ❌ WRONG — applyUpdate() requires updateReady to be true
await Updater.applyUpdate();  // Does nothing if updateReady is false

// ✅ CORRECT — download first, then apply
await Updater.downloadUpdate();
await Updater.applyUpdate();
```

### 4. bsdiff requires sequential version chain

Delta patches only work when the user has a local `.tar` of their current version. If the tar is missing (e.g., first install from DMG didn't preserve it, or user skipped versions), the updater falls back to a full download. This is handled automatically, but means:
- Skipping versions is fine (full download fallback)
- The self-extractor preserves the initial `.tar` for future patching
- `release.generatePatch: true` (default) must be set to generate patches at build time

### 5. Expecting updates in dev mode

```typescript
// Dev channel short-circuits — checkForUpdate() always returns updateAvailable: false
// This is by design. Use --env=canary or --env=stable for update testing.
```

### 6. Not setting `release.baseUrl`

Without `baseUrl`, the updater has no server to check. Set it to where you upload artifacts (S3, R2, GitHub Releases, any static file host).

## Platform-Specific Behaviors

| Behavior | macOS | Linux | Windows |
|---|---|---|---|
| App bundle format | `.app` bundle | Directory | Directory |
| Update replacement | `rmSync` + `renameSync` | Replace `app/` dir | Batch script via Task Scheduler (files locked while in use) |
| Post-update quarantine | Strips `com.apple.quarantine` xattr | Sets `chmod +x` on binaries | N/A |
| Installer format | DMG (ULFO/lzfse) | `.tar.gz` | `.zip` with `Setup.exe` |
| Relaunch method | `open` command (waits for PID exit) | Spawns launcher binary | Batch script relaunches after exit |

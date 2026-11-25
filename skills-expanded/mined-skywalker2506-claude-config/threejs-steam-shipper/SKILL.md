---
name: threejs-steam-shipper
description: Prepare, optimize, and package Three.js/WebGL/WebGPU/browser game projects as Steam-ready Windows/macOS/Linux desktop builds, static web exports, and Cordova mobile exports. Use when Codex is given a Three.js project directory and asked to create an .exe, .app, Linux desktop build, Electron/Tauri wrapper, buildable/ staging folder, SteamPipe depot layout, web export folder, Cordova Android/iOS wrapper, WebGPU port with WebGL fallback, release checklist, or performance/asset optimization pass for shipping on Steam, web, or mobile.
---

# Three.js Steam Shipper

## Goal

Turn a target Three.js project into shippable builds for Steam desktop, web, and mobile where requested, keeping changes scoped and avoiding unnecessary architecture. Default to creating a `buildable/` staging area inside the target project unless the user requests an external output path.

This skill must work standalone. Treat `$threejs-localize`, `$threejs-theme-fonts`, and other companion skills as optional: use them when available and relevant, but never require them to package an otherwise shippable game.

## Default Strategy

Prefer Electron for arbitrary Steam desktop builds because it ships a known Chromium runtime and handles WebGL consistently across Steam users' machines. Use Tauri only when the project already uses it or the user explicitly asks for a smaller WebView2-based build. Do not promise Steam Overlay support for browser-wrapper builds; verify it through Steam and treat Steamworks API integration as optional.

For Steam, optimize for an unpacked desktop app folder suitable for a depot, not only an installer. A single `.exe`, `.app`, AppImage, or installer is useful for local/direct testing, but Steam usually ships the application directory containing the executable/app bundle, resources, runtime files, and assets.

Use the source project's production static build as the shared input for all targets:

- `buildable/web/` for browser hosting/static upload.
- `buildable/steam-electron/` for Steam desktop on Windows, macOS, or Linux.
- `buildable/mobile-cordova/` for Cordova Android/iOS wrapping.

For Electron desktop scaffolds, include all three OS configs in `electron-builder.yml` (`win`, `mac`, `linux`) and create both host-aware scripts (`build:desktop-dir`, `build:desktop`) and explicit scripts (`build:win-dir`, `build:mac-dir`, `build:linux-dir`). The host-aware scripts should build the current OS by default; explicit scripts are for deliberate target/CI work.

Treat WebGPU as an optional progressive renderer path. Prefer a small renderer factory or adapter that can select WebGPU on PC/high-end browsers and keep WebGL/WebGL2 for unsupported devices. Do not rewrite shaders/materials wholesale unless the project already uses Three.js nodes/TSL or the user explicitly asks for a deeper port.

## Workflow

1. **Analyze first.** Run:

   ```bash
   node <skill>/scripts/analyze-threejs-project.mjs <target-project>
   ```

   Read the report under `<target-project>/buildable/reports/`. Identify framework, package manager, build output, Three.js dependencies, WebGL/WebGPU usage, Cordova/mobile risk, large assets, model formats, and risky path assumptions.

2. **Choose minimal targets.**
   - Use existing build tooling if it already produces static HTML/JS/CSS.
   - For Vite, ensure production uses relative asset paths (`base: './'`) before loading from Electron `file://`, static subfolders, or Cordova `www/`.
   - Avoid adding a game framework, backend server, updater, launcher, account system, or installer-only flow unless the project already needs it.

3. **Create export staging.** Run only the targets the user requested. For Steam:

   ```bash
   node <skill>/scripts/scaffold-steam-electron.mjs <target-project>
   ```

   This creates `<target-project>/buildable/steam-electron/` with an Electron wrapper, `electron-builder` config for Windows/macOS/Linux, host-aware desktop build script, web copy script, per-OS SteamPipe VDF templates, and a concise ship checklist.

   For static web and Cordova mobile:

   ```bash
   node <skill>/scripts/scaffold-web-mobile-export.mjs <target-project>
   ```

   This creates `<target-project>/buildable/web/` and `<target-project>/buildable/mobile-cordova/` with copy scripts, Cordova `config.xml`, minimal package scripts, and platform checklists. It does not install Android Studio, Xcode, signing certificates, or Cordova platforms automatically.

4. **Add WebGPU progressive renderer path when useful.**

   ```bash
   node <skill>/scripts/scaffold-webgpu-adapter.mjs <target-project>
   ```

   This creates a small `src/rendering/createThreeRenderer.mjs` adapter if missing. Integrate it manually into the app's renderer creation point, then test both WebGPU-capable and forced WebGL paths. Avoid WebGPU-only features if the game must keep fallback support.

5. **Wire the source project.**
   - Run the source project's production build.
   - Copy the built web output into every requested target: `buildable/web/dist/`, `buildable/steam-electron/web/`, and `buildable/mobile-cordova/www/`.
   - Patch only required source/config issues: relative paths, missing asset copies, CSP/file loading breakage, fullscreen/window mode, touch/pointer controls, safe-area layout, or asset loader paths.
   - Keep generated packaging files in `buildable/` unless the user wants the wrapper committed into the app.
   - If localization artifacts exist, verify packaged locale files, language switching, and flag assets. If `$threejs-localize` is available, run its compatibility verifier after target copy steps; otherwise do a manual check.

6. **Optimize assets and runtime.** Load `references/threejs-optimization.md` when models, textures, shaders, mobile GPU budgets, WebGPU/WebGL fallback behavior, or frame-time issues matter. Prefer measurable wins: compressed textures, GLB optimization, draw-call reduction, lazy loading, disposal, and bundle pruning.

7. **Build and verify.**
   - Install dependencies in each staging folder being built.
   - Steam desktop: build an unpacked host target first with `npm run build:desktop-dir`. On Windows it builds Windows, on macOS it builds macOS, and on Linux it builds Linux. Use `build:win-dir`, `build:mac-dir`, or `build:linux-dir` when an explicit target is needed.
   - Launch the generated `.exe`, `.app`, or Linux executable from its release folder and verify WebGL/WebGPU rendering, inputs, audio, saves/config, runtime errors, and clean shutdown on that OS.
   - Web: serve `buildable/web/dist/` over HTTP/HTTPS and verify relative asset paths, cache guidance, fullscreen/input, audio unlock, saves, and nonblank canvas.
   - Mobile: run `npm run prepare:android` or `cordova prepare` only after platform requirements are installed. Verify touch controls, safe areas/notches, orientation, resize, memory pressure, context loss, and app resume/pause.
   - WebGPU: verify a supported Chromium/browser path plus forced WebGL fallback. WebGPU requires secure browser contexts on the open web and is not supported everywhere, so never remove the WebGL path until target coverage is proven.
   - If localization exists, verify machine/Steam/browser/device language selection, language switching, packaged flag assets, and absence of `TODO:` translation values.
   - Produce installer, signed mobile, or store artifacts only after unpacked/debug builds work.

8. **Prepare release-specific packaging.**
   - Load `references/steam-electron-packaging.md` when creating final SteamPipe scripts, depot layout, launch options, achievements, overlay checks, or redistributable notes.
   - Load `references/web-mobile-webgpu-export.md` when creating final static web hosting notes, Cordova platform builds, Android/iOS signing notes, or WebGPU fallback QA.

## Output Shape

Use this default target layout:

```text
target-project/
  buildable/
    reports/
      threejs-steam-analysis.md
      threejs-steam-analysis.json
      webgpu-adapter-notes.md
    steam-electron/
      package.json
      electron-builder.yml
      electron/
      scripts/
        build-desktop.mjs
      web/
      release/
      steampipe/
      ship-checklist.md
    web/
      scripts/
      dist/
      release-checklist.md
    mobile-cordova/
      package.json
      config.xml
      scripts/
      www/
      mobile-checklist.md
  src/
    rendering/
      createThreeRenderer.mjs
```

If any `buildable/` target already exists, preserve user changes. Inspect it before editing, then patch only stale or missing pieces.

## References

- Read `references/steam-electron-packaging.md` for SteamPipe, Electron, Tauri tradeoffs, Steamworks, signing, and release layout details.
- Read `references/threejs-optimization.md` for Three.js-specific performance and asset optimization checks.
- Read `references/web-mobile-webgpu-export.md` for static web export, Cordova mobile, and WebGPU/WebGL fallback checks.

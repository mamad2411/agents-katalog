---
name: seeybot-release
description: Reference for the Seeybot project (what it is, architecture, data sources, gotchas) and the runbook for cutting a new release — version bump, CHANGELOG + README roadmap + website changelog, build & package, GitHub Release, and Homebrew cask update. Use when working on, updating, or releasing Seeybot.
---

# Seeybot — project reference & release runbook

## What Seeybot is
A native SwiftUI **macOS notch/Dynamic-Island widget** that shows live stats for local
**Claude Code** and **Codex** CLI sessions: session count, working vs idle, and token
usage — as a cute animated dashboard. Reads only local files; no network. Single
`swiftc`-built binary, **no Xcode**.

- Repo: <https://github.com/7757/Seeybot>  · author **musk** = <https://github.com/7757>
- Homebrew tap (separate repo): <https://github.com/7757/homebrew-seeybot> → `brew install --cask 7757/seeybot/seeybot`
- Website (GitHub Pages, this repo `index.html`): served from `main` / root
- Bundle id `com.seeybot.notch`; ad-hoc signed (no Apple Developer account → Gatekeeper handled by stripping quarantine)

## Architecture (`Sources/`)
- `SessionCollector.swift` — scans `~/.claude/projects/**/<uuid>.jsonl` and
  `~/.codex/sessions/**/rollout-*.jsonl`; `ps`+`lsof` map running `claude`/`codex`
  processes → transcripts. Per-file cache keyed on (mtime,size).
- `StatsStore.swift` — background timer (3s) → publishes `DashStats` on the main actor.
- `Models.swift` — `DashStats`, `TokenBreakdown`, `WidgetMode`, `Fmt`.
- `NotchWindow.swift` — borderless transparent non-activating `NSPanel` above the menu bar; `FirstMouseHostingView`.
- `AppDelegate.swift` — placement, cursor-poll hover, menu-bar `NSStatusItem` + in-widget `⋯` menu, update check.
- `NotchRootView.swift` — ONE morphing island (collapsed pill/bar ⇄ expanded dashboard) that animates size/corner/pad.
- `CollapsedPill.swift` / `SidesBar.swift` — collapsed forms (hanging / bar / flat).
- `DashboardView.swift`, `Components.swift`, `FlowLayout.swift`, `Mascot.swift`, `Theme.swift`.
- `Updater.swift` — GitHub-Releases version check.
- `RenderPreview.swift` — `--render <dir>` writes PNGs of every state (used for design QA without screen-recording perms). `--stats` prints the collected JSON.

## Data / accuracy notes (don't regress these)
- Claude tokens: sum assistant `message.usage`, **de-dup by `message.id`** (one reply spans many lines).
- Exclude `subagents/` sidechains from counts & totals.
- Codex tokens: last cumulative `token_count`.
- "today" attributed by per-entry **timestamp**, not file mtime.
- Sessions sharing a cwd get **distinct** transcripts (greedy claim).
- Working = transcript written < 45 s ago.

## Gotchas
- `enum Dim` is named `Dim` (not `Layout`) to avoid shadowing SwiftUI's `Layout` protocol.
- `FlowLayout` is used via a local `let layout = FlowLayout(...); layout { … }` (bare `FlowLayout(args){}` mis-parses as init).
- Non-notched Macs: `NotchMetrics.hasNotch == false`, `notchWidth == 0` → flat continuous bar, no hanging form; use `menuBarHeight` for clearance.
- Menu-bar `NSStatusItem` can be **hidden behind the notch** on crowded menu bars → the in-widget `⋯` button is the notch-proof quit.
- Build with `./build.sh` (needs Command Line Tools `swiftc`, no Xcode).

## Commit / author convention
- **Commits must NOT include a `Co-Authored-By: Claude` trailer.** Author is musk only.
- UI text is **English**; docs are multi-language (`README.md` EN, `README.zh-CN.md`, `README.ja.md`) — keep them in sync. Website (`index.html`) is currently Chinese-first.

## Cutting a release (vX.Y)
1. Bump the version in **`Info.plist`** (`CFBundleShortVersionString` and `CFBundleVersion`).
2. Update **`CHANGELOG.md`**: move `[Unreleased]` items into a new `[X.Y] — <date>` section (Added / Changed / Fixed).
3. Mirror the highlights into: **README roadmap** (all 3 languages — check finished items) and the **website `#changelog`** section in `index.html` (add a new `.log` entry at the top).
4. Build & package:
   ```bash
   ./build.sh
   ditto -c -k --keepParent build/Seeybot.app Seeybot.zip
   SHA=$(shasum -a 256 Seeybot.zip | awk '{print $1}')
   ```
5. Publish the GitHub Release:
   ```bash
   gh release create vX.Y Seeybot.zip --repo 7757/Seeybot --title "Seeybot X.Y" --notes "…from CHANGELOG…"
   ```
6. Update the **Homebrew cask** in the tap repo `7757/homebrew-seeybot`
   (`Casks/seeybot.rb`): set `version "X.Y"` and the new `sha256`, commit & push. Verify:
   `brew update && brew upgrade --cask seeybot`.
7. Commit the app repo (no Claude trailer) and push `main`; GitHub Pages redeploys the site.
8. `Updater.checkLatest` (repo `7757/Seeybot`) will then surface the new version to users
   as a badge + menu item pointing at the Releases page.

## Handy commands
- `./install.sh` — build from source, install to /Applications, LaunchAgent auto-start.
- `Seeybot --stats` / `Seeybot --render <dir>` — debug the collector / render UI states.
- Quit a running copy: menu-bar icon or the in-widget `⋯` → Quit; or
  `launchctl unload ~/Library/LaunchAgents/com.seeybot.notch.plist; pkill Seeybot`.

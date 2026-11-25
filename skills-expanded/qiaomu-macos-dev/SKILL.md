---
name: qiaomu-macos-dev
description: |
  One-sentence, one-shot development of polished native macOS apps (SwiftUI + AppKit, SwiftPM, no Xcode project): menu bar apps with a hotkey panel or normal Dock/window apps, scaffolded with an Icon Composer icon from Lucide, a settings window with About (version, update check, feedback, follow/tip QR), Sparkle auto-update, Vercel-style UI verified by offscreen snapshots, Developer ID signing, notarization, a designed DMG, a GitHub repo (private by default, ask before public) with an illustrated product-page README, PR flow and GitHub Releases with an appcast. Default skill for any macOS app work by 乔木: "做一个 mac 软件", "开发 macOS app", "菜单栏工具", "做个 Mac 小工具", "加自动更新", "做设置页/关于页", "设计 app 图标", "公证/打包 DMG", "发布 mac app 到 GitHub", plus debugging focus, hotkey, TCC permission, IME and Sparkle issues in such apps.
  Excludes: iOS/iPadOS/watchOS apps, Electron/Tauri/web apps, browser extensions and native-messaging helpers (use qiaomu-dev-skill), Obsidian plugins, .pkg installers for helpers, and generic Swift questions with no app to build.
---

# Qiaomu macOS Dev

Turn one sentence into a shipped, notarized, auto-updating Mac app that looks designed. Distilled from building 乔木闪记 / Jot end to end (github.com/joeseesun/qiaomu-jot); every rule here cost a real bug.

## Router

- New app → run the generator, then the [One-Shot Workflow](references/one-shot-workflow.md). Do not hand-write the skeleton.
- Existing app → read only the reference for the task (table below) and keep the project's conventions.
- Reply in Chinese; code, commands and identifiers stay English.
- Ask only what changes the build: the app's job in one line, Chinese + English name, menu bar vs window (infer when obvious). Everything else gets a good default and is listed in the handoff.

## Generate

```bash
python3 scripts/new_app.py --dir ~/Code/qiaomu-<slug> --name <AsciiName> --zh <中文名> \
  --bundle-id ai.qiaomu.<slug> --repo joeseesun/qiaomu-<slug> \
  --kind menubar|window --tagline "<一句话价值>" --lucide <icon> --symbol <sf-symbol>
cd ~/Code/qiaomu-<slug> && ./scripts/sparkle-key.sh && ./build.sh && build/<Name>.app/Contents/MacOS/<Name> --selftest
```

The project builds, signs and self-tests on the first run. It has a main menu (⌘, ⌘W ⌘Q and Edit keys), settings tabs plus About, Sparkle, launch at login, `--snapshot` / `--selftest`, `release.sh` (universal binary → notarize → staple → DMG → appcast) and `install-local.sh`. Details: [Project Template](references/project-template.md).

## One-Shot Phases (each has a gate)

1. **Intent**: pain point, the one core action, success in 10 seconds. Gate: one-line tagline.
2. **Scaffold**: the generator above. Gate: build + selftest pass.
3. **Core feature**: put logic in pure functions and grow `selftest()` with every feature. Gate: selftest passes.
4. **UI**: [UI Polish](references/ui-polish.md). Gate: snapshots in light and dark of every surface, looked at, not assumed.
5. **Settings + About + onboarding**: [Settings & About](references/settings-about.md). Gate: snapshot of each tab.
6. **Icon**: [Icon](references/icon.md). Gate: the icon is rendered and viewed at 1024 and 32 px.
7. **Permissions**: [Permissions](references/permissions.md). Gate: first-run path shows *why* before macOS asks.
8. **Install and dogfood**: `./install-local.sh` replaces /Applications and relaunches. Do this after every build the user will test.
9. **GitHub**: [GitHub](references/github.md). The repo is **private by default**; ask before making it public. README is a product page.
10. **Release**: [Release](references/release.md) + [Auto-Update](references/auto-update.md). Gate: Gatekeeper says "Notarized Developer ID", appcast version and EdDSA signature verified, a download from the release URL opens.

Before handing over, walk the [Details Checklist](references/details-checklist.md). When something breaks, check the [Pitfalls](references/pitfalls.md) first.

## Non-Negotiables

- **Look before you claim.** Render every user-visible surface with `--snapshot` (and the DMG window and icon), open the PNG, fix what looks wrong. Signature checks are not visual checks.
- **Design taste**: Vercel black/white, Geist, one accent at most, never purple, no muddy grey. Generous spacing, explicit close buttons, keyboard first. No vertical side-stripe accents (`border-left` bars); use a tint, weight or a small dot. Identify other apps by their logo (simple-icons, Lucide fallback), not by text.
- **Ordinary users first**: generic defaults that work with zero setup. Never tailor defaults to the developer's own folders. Save the user's content verbatim; never silently reformat it.
- **Sign with Developer ID on every build**, including dev builds, so macOS permission grants survive rebuilds. Hardened runtime. Sign nested code inside-out, never `--deep`.
- **Secrets never enter the repo or this skill**: the Sparkle private key stays in the login keychain, notarization uses the `notary` keychain profile, and only the public key is committed.
- **Git**: feature branch → PR → merge; never push to `main`. Publish, make public, or release only when the user asked.
- Lessons from a new app go into the matching reference here (bump `manifest.json` version), not into a new skill.

## Reference Map

| Task | Read |
|---|---|
| Phases, gates, handoff format | [one-shot-workflow](references/one-shot-workflow.md) |
| Generated files, scripts, how to extend | [project-template](references/project-template.md) |
| Menu bar, panels, focus, hotkeys, windows | [app-architecture](references/app-architecture.md) |
| Visual design, snapshots, motion, copy | [ui-polish](references/ui-polish.md) |
| Settings window, About, onboarding | [settings-about](references/settings-about.md) |
| App icon, menu bar glyph, DMG art | [icon](references/icon.md) |
| TCC, Accessibility, Apple Events, files from other apps | [permissions](references/permissions.md) |
| Sparkle, appcast, gentle reminders | [auto-update](references/auto-update.md) |
| Signing, notarization, DMG, versioning | [release](references/release.md) |
| Repo, README, About/topics, PRs, Releases | [github](references/github.md) |
| Known bugs and their fixes | [pitfalls](references/pitfalls.md) |
| The things users don't think to ask for | [details-checklist](references/details-checklist.md) |

Copyright (c) 向阳乔木 · X https://x.com/vista8 · GitHub https://github.com/joeseesun/

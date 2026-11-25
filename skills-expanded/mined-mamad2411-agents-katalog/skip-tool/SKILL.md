---
name: skip-tool
description: "Guides development with Skip: dual-platform iOS/Android apps and libraries using Swift and SwiftUI. Use when working on Skip projects, Swift-to-Android builds, skip CLI, Skip Fuse/Lite, SwiftUI-to-Compose, compiler directives (#if os(Android), #if SKIP), or when the user mentions Skip, skip.dev, or skip create/verify/build."
---

# Skip Tool Skill

## Overview

Use this skill to help with Skip: dual-platform iOS and Android development using a single Swift and SwiftUI codebase. Skip compiles Swift natively for both platforms (SwiftUI on iOS, Jetpack Compose on Android). The skill covers getting started (new vs existing project, environment check), mode selection (Skip Fuse vs Skip Lite), CLI usage, compiler directives, building and running, porting packages, and module/component reference. Read only the reference file(s) needed for the current request; all content is in the skill (no web dependency).

## Getting started (first), then mode selection

At the beginning of any Skip-related help:

**1) Getting started** — Establish context (see `references/getting-started.md` when the user is new or environment is unclear):
- **New vs existing project:** Ask or infer (e.g. presence of `Package.swift`, `Skip/skip.yml`, or user saying they want to create vs have an app). For new or "how do I start?", guide through getting started.
- **Is Skip installed?** Suggest `which skip` or `skip version`. If not: `brew install skiptools/skip/skip`. Prerequisites: Xcode, Android Studio, Homebrew; macOS 15+.
- **Environment check:** Recommend `skip checkup` to verify the development environment.

**2) Mode selection (Fuse vs Lite):**
- **Intent unclear:** Prompt the user to choose Skip Fuse or Skip Lite (AskQuestion if available; otherwise ask in chat).
- **Existing project:** Infer from `Skip/skip.yml` (`mode: 'native'` → Fuse, `mode: 'transpiled'` → Lite); ask only if missing or ambiguous.
- **New project:** After the user chooses, follow the appropriate flow (`skip create` or `skip init --native-app` / `--transpiled-app` and correct Package.swift dependencies).

Apply all subsequent guidance (bridging, CLI, troubleshooting) according to the chosen or detected mode.

## Workflow Decision Tree

### 0) Getting started
User new to Skip, environment unclear, or "how do I start?" → see `references/getting-started.md` (new vs existing project; check Skip installed; run `skip checkup`; prerequisites).

### 1) Creating or setting up a Skip project
Establish mode first. Then see `references/cli.md`, `references/modes.md`.

### 2) Writing dual-platform Swift/SwiftUI code
See `references/directives.md`. For UI: see `references/skip-ui.md` and the relevant `references/component-*.md` if needed.

### 3) Build or run issues
See `references/building.md`, `references/troubleshooting.md`.

### 4) Porting a package or adding dependencies
See `references/porting.md`.

### 5) Questions about a Skip module or SwiftUI/Compose component
See `references/modules-index.md`; for SkipUI/supported SwiftUI see `references/skip-ui.md`; for SkipFoundation see `references/skip-foundation.md`; for components see `references/components-index.md` or the specific `references/component-*.md`.

## Core Guidelines

- **Getting started first:** New vs existing project; check Skip installed; run `skip checkup` when environment is in question.
- **Then establish mode (Fuse vs Lite)** before giving mode-specific advice.
- **CLI basics:** `skip checkup` for environment validation; `skip create` for new projects; `skip verify` for project validation.
- **Directives:** Use `#if os(Android)` / `#if !os(Android)` for platform branches; use `#if SKIP` for code that is transpiled and can call Kotlin/Java (see `references/directives.md`).
- **All material in references/:** Do not depend on web or external URLs; read only the reference(s) needed for the request.

## Quick Reference

### Main CLI commands
| Command | Purpose |
|---------|---------|
| `skip version` | Print Skip version |
| `skip doctor` | Evaluate development environment |
| `skip checkup` | Full system check (recommended after install) |
| `skip upgrade` | Upgrade Skip |
| `skip create` | Create new project interactively |
| `skip init` | Initialize project (non-interactive) |
| `skip verify` | Verify Skip project |
| `skip export` | Export Gradle project and artifacts |
| `skip devices` | List devices and emulators |
| `skip android` | Build, run, test, sdk, emulator subcommands |

### Compiler directives
| Directive | Use |
|-----------|-----|
| `#if os(Android)` | Android-only code |
| `#if !os(Android)` | iOS-only code |
| `#if SKIP` | Transpiled code; can call Kotlin/Java API |

## Review Checklist

- [ ] New vs existing project clear
- [ ] Skip installed / environment checked (`skip checkup` if needed)
- [ ] Mode established (Fuse/Lite) or detected from skip.yml
- [ ] Correct reference file(s) read for the question
- [ ] Advice matches mode (Fuse vs Lite)

## References

- `references/getting-started.md` — New vs existing project; Skip install (Homebrew); skip checkup; prerequisites
- `references/cli.md` — Skip CLI commands and options
- `references/modes.md` — Fuse vs Lite, skip.yml, bridging, dependencies per mode
- `references/directives.md` — #if os(Android), #if SKIP, calling Kotlin/Java, platform customization
- `references/building.md` — Build/run, SKIP_ACTION, emulator, device, frameworks
- `references/troubleshooting.md` — checkup, clean build, common errors, where to get help
- `references/porting.md` — Porting packages, conditional imports, Swift Package Index
- `references/modules-index.md` — List of Skip modules and what they are for
- `references/skip-ui.md` — SkipUI, supported SwiftUI
- `references/skip-foundation.md` — SkipFoundation
- `references/components-index.md` — Overview and which reference to read for which component
- `references/component-*.md` — Per-component reference (e.g. component-button.md, component-list.md)

## Philosophy

Establish context first (getting started, then mode). Use only local reference files; keep each reference small and focused. Read only the reference(s) relevant to the user's request. No web dependency.

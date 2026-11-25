---
name: systems-desktop
description: "Choosing how to build a desktop app with Rust before writing it: Tauri (a web UI in the system webview with a Rust core) or GPUI (native, GPU-drawn, all Rust), when egui, iced or Slint fit instead, the questions that decide it, and what to settle up front (platforms, packaging, updates, signing). Read when a desktop app is asked for, or the stack is not decided yet."
---

# Choosing a desktop stack

A desktop app built without this choice picks whatever came to mind first:
a web stack for a tool that must open ten thousand files instantly, or a
GPU framework for a settings form that a web developer will maintain. The
choice is cheap now and expensive after the first screen. Ask, or decide
from the request and say why in one line, then read the stack's skill.

## 1. The two main roads

**Tauri**: the interface is a web app (HTML, CSS, any frontend framework)
in the operating system's webview; the core is Rust, reached through
commands. Small bundles, a mature plugin set (file dialogs, updater,
tray, notifications, deep links), mobile targets too.

- Choose it when the team knows web UI, the app is forms, dashboards,
  content and settings, the look should match a web product, or a web
  version exists or is planned.
- Mind: rendering differs a little per webview (WebKit on macOS and
  Linux, WebView2 on Windows); test each. The webview is a security
  boundary: expose only the commands the UI needs, with Tauri's
  capabilities, and treat everything from the UI as untrusted.
- The interface itself is built with the `frontend` and `ui` skills.

**GPUI**: native, drawn on the GPU, all Rust, the framework the Zed
editor is built on. Keyboard-first and very fast with large data.

- Choose it for editors, IDE-like tools, terminals, log and data viewers,
  anything with huge lists or text, high frame rates, or a strict
  keyboard workflow, and when the team is comfortable in Rust.
- Mind: young, its API changes between versions, documentation is mostly
  its examples, no ready-made widget kit like the web's (you build
  inputs, menus and lists from elements), no mobile. Read `systems-gpui`.

## 2. Others, briefly

- **egui**: immediate mode, quick to get going; internal tools, debug
  panels, overlays in a game or a renderer. Looks like egui unless styled
  with care.
- **iced**: Elm-like architecture, retained, cross-platform; a good fit
  for a moderate native app wanting a clean update/view model.
- **Slint**: a declarative UI language with Rust bindings; embedded
  devices and kiosks as well as desktop. Check its licence for your use.

Name the one you pick and why; do not mix two UI stacks in one app.

## 3. The questions that decide it

1. Who maintains the interface: web developers or Rust developers?
2. How much data on screen at once, and how fast must it move?
3. Platforms: which of macOS, Windows, Linux, and mobile later?
4. Must it look native, match a brand, or match a web app?
5. Size and memory budget, and does it run all day in the background?

Web skills and forms point to Tauri; huge data, text, keyboard flow and a
Rust team point to GPUI.

## 4. Settle before the first screen

- **Platforms** to build and test on, in CI as well as locally.
- **Packaging** per platform: `.app`/`.dmg` (macOS), MSI or NSIS
  (Windows), AppImage, Flatpak or `.deb` (Linux). Tauri bundles these;
  with GPUI plan the bundling yourself.
- **Signing and notarization** (macOS) and code signing (Windows): an
  unsigned app warns or is blocked on first run.
- **Updates**: Tauri's updater plugin, or your own check against a
  signed release feed. Never download and run code without verifying it.
- **Where data lives**: the platform's config and data directories, not
  the working directory.
- **Accessibility**: keyboard access everywhere, focus that shows, screen
  reader support (better in webviews today; check what a native toolkit
  offers before promising it).

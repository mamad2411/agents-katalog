---
name: containerized-dev-environment
description: Guidelines and environment instructions for running, serving, and building the webgl-v1 application inside Docker / DevContainer / WSL setup.
---

# DevContainer & Execution Guidelines

## Build & Shell Command Policy

- **DO NOT run `ng build`, `npm start`, or `npm test` automatically**. The user executes all builds, dev-server starts, and tests directly inside the DevContainer terminal.
- Only make file changes and explain root causes clearly.

## Environment Context

- **Workspace Architecture**: This repository is a containerized Angular v22 + Three.js application designed to run inside a DevContainer.
- **Node.js Requirement**: The project requires **Node.js v22.x** inside the container.

## Key Project Rules & Assets

- **Asset Routing**: All project assets (textures, particle graphics, fonts, audio) are located in `src/assets`. In `angular.json`, assets MUST be configured as `"src/assets"` so Angular CLI serves them at `/assets/*`.
- **Lighting Model**: Three.js v0.185 uses physically-based lighting strictly. Scenes require an `AmbientLight` to avoid pitch-black unlit geometry faces.
- **Color Management**: `ColorManagement.enabled` is `true` by default in Three.js v0.185. Avoid calling `.convertLinearToSRGB()` on `Color` hex instances to prevent double conversion.
- **State Synchronization**: `ObjectManagerService.LevelMaterialsUpdated` uses a `BehaviorSubject<boolean>` to prevent timing race conditions between texture loading and dialog component subscriptions.

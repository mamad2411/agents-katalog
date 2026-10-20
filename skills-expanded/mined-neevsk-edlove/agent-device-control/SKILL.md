---
name: agent-device-control
description: Guided workflow and commands for running agent-device (Callstack) and argent (SWM) controls.
---

# Agent Device Control & Automation Guide

This skill provides guides and instructions on how to use device automation tools in the Gurudevi Platform to interact with, inspect, and test mobile applications running on simulators, emulators, or **connected physical devices**.

---

## 🚀 Unified MCP Tool: `sovereign_device`

The primary way to control and query emulator or simulator states is using the `sovereign_device` tool registered on our `platform-mcp` gateway.

### Selecting a Tool

Pass `"tool": "argent"` to use the Software Mansion (SWM) tool.
Omit it (default) to use **agent-device** (Callstack).

---

## 📋 Action Verb Reference

### agent-device (Callstack) — default tool

| Action Verb | Description | Key Params |
| :--- | :--- | :--- |
| `doctor` | Health check / device readiness | — |
| `snapshot` | Accessibility tree (XML + bounds) | `{ platform: "android" \| "ios" }` |
| `screenshot` | Capture screen image | `{ platform: "android" \| "ios" }` |
| `open_app` | Launch app by bundle ID | `{ appId: "com.gurudevi", platform }` |
| `press` | Press element by a11y identifier | `{ element: "login-button" }` |
| `type` | Type text into focused input | `{ text: "hello@example.com" }` |
| `scroll` | Scroll the active view | `{ direction: "up" \| "down" \| "left" \| "right" }` |
| `tap` | Tap at physical coordinates | `{ x: number, y: number }` |
| `find-text` | Find element by visible text | `{ text: "Sign In", platform? }` |
| `find-role` | Find element by ARIA role | `{ role: "button", label?: "Submit", platform? }` |
| `logs` | Dump device/system logs | — |
| `network` | Dump captured network requests | — |
| `reload` | Hot-reload Metro JS bundle | — |
| `clear-cache` | Clear Metro cache + reload | — |
| `profile` | CPU/memory sample (JSON) | `{ duration?: number (ms) }` |

### argent (SWM) — `{ "tool": "argent" }`

| Action Verb | Description | Key Params |
| :--- | :--- | :--- |
| `doctor` | Check connected tools & devices | — |
| `screenshot` | Capture screen image | — |
| `visual-diff` | Diff screenshot vs. baseline | `{ baseline?: "/path/to/base.png" }` |
| `record` | Start/stop screen recording | `{ stop?: boolean, output?: "file.mp4" }` |
| `component-tree` | Live React Native component tree | — |
| `swipe` | Swipe gesture | `{ direction: "up"\|"down"\|"left"\|"right", element? }` |
| `pinch` | Pinch / zoom gesture | `{ direction: "in"\|"out", scale?: number }` |
| `long-press` | Long press on element | `{ element: "id", duration?: number (ms) }` |
| `wait` | Wait for element to appear | `{ element: "id", timeout?: number (ms) }` |
| `assert` | Assert element exists / has text | `{ element: "id", text?: "expected" }` |
| `network` | Dump native-level network requests | — |
| `logs` | Dump device logs | — |

---

## 🛠️ Diagnostics & Setup Verification

Always run `doctor` first to verify the connection is healthy:

```json
// agent-device
{ "action": "doctor" }

// argent
{ "action": "doctor", "params": { "tool": "argent" } }
```

---

## 👁️ Inspecting UI & Accessibility Tree

```json
// Get accessibility snapshot (agent-device)
{ "action": "snapshot", "params": { "platform": "android" } }

// Get live React Native component tree (argent)
{ "action": "component-tree", "params": { "tool": "argent" } }
```

Always read the snapshot before pressing/tapping — it reveals element identifiers.

---

## 👆 Basic Interaction

```json
// Press by a11y id
{ "action": "press", "params": { "element": "login-button" } }

// Type text
{ "action": "type", "params": { "text": "teacher@gurudevi.org" } }

// Tap by coordinate
{ "action": "tap", "params": { "x": 200, "y": 450 } }

// Scroll down
{ "action": "scroll", "params": { "direction": "down" } }
```

---

## 🔍 Finding Elements

When you don't know the a11y id, use finders (agent-device):

```json
// Find by visible text
{ "action": "find-text", "params": { "text": "Sign In", "platform": "android" } }

// Find by ARIA role
{ "action": "find-role", "params": { "role": "button", "label": "Submit" } }
```

---

## ✋ Gestures (argent 0.21+)

```json
// Swipe left on a carousel
{ "action": "swipe", "params": { "tool": "argent", "direction": "left" } }

// Pinch to zoom in
{ "action": "pinch", "params": { "tool": "argent", "direction": "in", "scale": 2.0 } }

// Long press an item to open context menu
{ "action": "long-press", "params": { "tool": "argent", "element": "post-item-42", "duration": 800 } }
```

---

## ⏳ Waiting & Asserting State (argent 0.21+)

Use `wait` before interacting with elements that load asynchronously:

```json
// Wait for the home screen to appear (max 8s)
{ "action": "wait", "params": { "tool": "argent", "element": "home-screen", "timeout": 8000 } }

// Assert the welcome text is visible
{ "action": "assert", "params": { "tool": "argent", "element": "welcome-header", "text": "Welcome back" } }
```

---

## 🌐 Network Inspection (argent 0.21+ / agent-device)

```json
// Dump native network requests (argent)
{ "action": "network", "params": { "tool": "argent" } }

// Dump network traffic (agent-device)
{ "action": "network" }
```

Use this to verify API calls are succeeding during a flow, or debug auth headers.

---

## 📸 Visual Regression Workflow (argent 0.22+)

```
1. Take a baseline screenshot of a stable state
2. Make UI changes in code
3. Run visual-diff to detect unintended changes
```

```json
// Step 1 — save baseline (omit --baseline to create it)
{ "action": "visual-diff", "params": { "tool": "argent" } }

// Step 3 — diff against saved baseline
{ "action": "visual-diff", "params": { "tool": "argent", "baseline": "/tmp/home-baseline.png" } }
```

---

## 🎬 Video Recording (argent 0.23+)

Useful for capturing a full interaction flow for bug reports:

```json
// Start recording
{ "action": "record", "params": { "tool": "argent" } }

// ... perform interactions ...

// Stop and save
{ "action": "record", "params": { "tool": "argent", "stop": true, "output": "bug-repro.mp4" } }
```

---

## 🔄 Metro Bundler Control (agent-device)

Useful during development to hot-reload without restarting:

```json
// Hot reload (fast — no cache clear)
{ "action": "reload" }

// Full reload with cache clear (slower, for stale module issues)
{ "action": "clear-cache" }
```

---

## 📊 Performance Profiling (agent-device)

```json
// 5-second CPU/memory sample
{ "action": "profile", "params": { "duration": 5000 } }
```

---

## 🩺 Recommended Debug Workflow (Connected Mode)

When diagnosing a splash screen hang or boot stall:

```
1. doctor        → verify connection
2. screenshot    → confirm what's currently on screen
3. logs          → read boot trace output ([boot trace] lines)
4. network       → check if any network call is hanging
5. reload        → hot-reload if JS bundle seems stuck
6. snapshot      → verify app rendered past splash
```

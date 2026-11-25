---
name: stand-up-report
description: Used when requested for a short -no fluff- Concise, high-density summary of technical progress, architecture decisions, and build status for the current session..
---

# Instructions:
When the user requests a report, synthesize the session history into the following structure:

* Core Accomplishments: Focus on high-level goals reached (e.g., "Phase 1 complete").
* Architecture & Logic: List specific design patterns used or decisions finalized.
* Implementation Details: List specific modules, crates, or files touched.
* The "Fix" Log: A dedicated section for compiler errors, linting (clippy), and logic bugs resolved.
* Status Check: Current build/test health (e.g., "Cargo check: Green, Tests: 50/50").

## Exampme
```md
## 🚀 Stand-up Report

### 🎯 Key Outcomes
- Successfully implemented and integrated all **Phase 1 modules**.
- Completed environment setup and dependency alignment (Rust 1.75+, OpenSSL).

### 🏗️ Architecture & Design
- **Routing:** Transitioned from single-backend to `HashMap<String, Arc<dyn CliBackend>>`.
- **Concurrency:** Resolved `Arc` self-reference issues in `TelegramProvider` by adjusting `start()` signature.
- **Data Shapes:** Finalized `MessageContext` and `ChannelProvider` traits.

### 🛠️ Implementation
- **Modules:** `types`, `config`, `security`, `session`, `command`, `backend/claude`, `executor`, `formatter`, `channel/telegram`, `router`, `main`.

### 🔧 Bug Fixes & Refactoring
- **Dependencies:** Resolved `teloxide` version mismatch (0.13 → 0.17).
- **Types:** Fixed deprecated `.from()` calls and handled UTF-8 boundaries in the formatter.
- **Linting:** Passed `cargo clippy -- -D warnings` (optimized `or_insert_with`).

### 🚦 Current Status
- **Build:** ✅ Passing (`cargo check`)
- **Tests:** 🧪 50/50 unit tests passing
```
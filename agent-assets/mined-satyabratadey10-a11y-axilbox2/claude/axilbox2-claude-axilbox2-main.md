# CLAUDE.md — Operating Guidelines for Claude Code Sessions

This document provides mandatory project context, architectural guidelines, and execution rules for Claude Code assistant sessions working in the AxilBox repository.

---

## 1. Mandatory Required Reading

Before writing or editing code, Claude MUST inspect and follow:
- [`PLAN.md`](PLAN.md): Active development phase and detailed milestone breakdown. Work strictly within the current milestone.
- [`RULES.md`](RULES.md): Non-negotiable engineering constraints (zero WebViews, zero on-device builds, zero proprietary images).
- [`RESEARCHDATA.md`](RESEARCHDATA.md): Authoritative technical facts for kernel flags, WebRTC pipelines, memory budgets, and the ARM64 `CFINV`/`HWCAP_FLAGM` bug.
- [`DESIGN.md`](DESIGN.md): UI/UX design specifications, color tokens, typography, and screen layouts.
- [`GOAL.md`](GOAL.md): Project scope, target audience, and legal boundaries (zero Apple OS, zero proprietary ROMs/GMS, zero AVF).

---

## 2. Core Operational Rules

### 2.1. CI-Only Compilation & Test Policy
- **Never run on-device Gradle, Java, or NDK compilation commands.**
- All builds, tests, and lint checks must be committed and pushed to run through GitHub Actions CI (`.github/workflows/android-ci.yml`).

### 2.2. No Self-Reported Success
- Never state that code is verified or working without actual green output from GitHub Actions CI logs.
- Never guess or simulate test results; verify via CI artifacts.

### 2.3. Zero WebView / Browser Components
- UI is 100% native Jetpack Compose.
- Do not introduce `WebView`, HTML5 canvas, or browser-based rendering anywhere in the codebase.

### 2.4. Cross-File Reference Integrity
- Prior to completing any code change, verify all imports, package declarations, Room schema annotations, and navigation routes for complete syntactic and semantic alignment.

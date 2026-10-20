# GEMINI.md — Operating Guidelines for Gemini & Google AI Studio

This document establishes operating guidelines and integration requirements for Gemini models and Google AI Studio sessions interacting with the AxilBox repository.

---

## 1. Mandatory Required Reading

Before generating or modifying code, Gemini models MUST review:
- [`PLAN.md`](PLAN.md): Active development phase and detailed milestone breakdown. Work strictly within the current milestone.
- [`RULES.md`](RULES.md): Non-negotiable engineering constraints (zero WebViews, zero on-device builds, zero proprietary images).
- [`RESEARCHDATA.md`](RESEARCHDATA.md): Authoritative technical facts for kernel flags, WebRTC pipelines, memory budgets, and the ARM64 `CFINV`/`HWCAP_FLAGM` bug.
- [`DESIGN.md`](DESIGN.md): UI/UX design specifications, color tokens, typography, and screen layouts.
- [`GOAL.md`](GOAL.md): Project scope, target audience, and legal boundaries (zero Apple OS, zero proprietary ROMs/GMS, zero AVF).

---

## 2. Reconciling AI Studio & Gemini Artifacts

When importing or proposing code snippets generated in Google AI Studio or external Gemini playgrounds:
1. **Reconciliation Against `DESIGN.md`:** Ensure all Compose components use the project's exact dark-mode color tokens, typography hierarchy, and spacing values defined in [`DESIGN.md`](DESIGN.md).
2. **Reconciliation Against `RULES.md`:** Verify that no prohibited dependencies (e.g., `WebView`, legacy support libraries, AVF references) have been introduced.
3. **Room & KSP Compatibility:** Verify that Room entities and DAOs adhere to Kotlin KSP standards with explicit column types, primary keys, and reactive `Flow` return types.

---

## 3. Core Verification Rules

- **CI-Only Verification:** Builds and tests execute exclusively in GitHub Actions CI (`.github/workflows/android-ci.yml`). Never run on-device Gradle builds.
- **No Self-Reported Success:** Code must be verified via actual CI workflow logs before marking milestones as complete.
- **Never Fabricate Research Data:** Do not invent hardware capabilities, kernel parameters, or JNI behaviors. Use [`RESEARCHDATA.md`](RESEARCHDATA.md) as the single source of truth.

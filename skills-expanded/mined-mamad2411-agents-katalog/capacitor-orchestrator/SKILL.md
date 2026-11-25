---
name: capacitor-orchestrator
description: Use when one CapacitorJS request spans multiple capability areas — setup, web integration, native APIs, plugin authoring, auth/session, offline resilience, observability, security, testing, CI integration, performance gates, migration upgrades, live updates, accessibility, deep linking, environment config, push notifications, privacy compliance, or release readiness — and needs one deterministic intake, explicit phase ownership, and a unified execution contract.
---

# Capacitor Orchestrator

## Specialization

Coordinate multi-surface CapacitorJS work from one intake when the request spans project setup, web framework integration, native API usage, custom plugin authoring, auth/session, offline resilience, observability, security hardening, testing, CI integration, migration upgrades, performance gating, or release readiness.

This skill provides intake, phase ownership, and unified synthesis. It is not a replacement for deep execution guidance inside any single Capacitor discipline — each specialist skill provides that depth.

## Objective

Produce one deterministic CapacitorJS execution contract from a single intake with explicit phase ownership, evidence expectations, and completion checks — eliminating disconnected, ad-hoc Capacitor work.

## Scope Boundaries

In scope:

- Deterministic Capacitor intake and phased execution planning.
- Phase-output ownership with exactly one owner per required output.
- Unified execution recommendation for mixed Capacitor design and delivery work.
- Routing to the correct specialist skill for each phase.

Out of scope:

- Deep execution of any one specialized phase (delegate to specialist skills).
- Non-Capacitor product areas unless they materially constrain the Capacitor slice.
- Generic project governance unrelated to the Capacitor objective.

## Trigger Conditions

- A Capacitor request spans more than one capability area.
- A new Capacitor project is being bootstrapped from scratch.
- A team wants one Capacitor intake instead of disconnected setup, integration, and native API work.
- A Capacitor app is being prepared for production and needs coordinated security, testing, and release hardening.
- A cross-project compendium consumer needs to understand which Capacitor skills apply to their situation.

## Inputs

- User objective and target Capacitor surface (new project, feature addition, production hardening, or release).
- Web framework in use (React, Vue, Angular, SvelteKit).
- Target platforms: iOS, Android, or both.
- Required capabilities (e.g., camera, push notifications, custom plugin, offline storage).
- Risk level: low (internal tool), medium (consumer app), high (regulated/PII).
- Required outputs and known evidence.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Intake contract: objective, scope boundaries, platforms, risk level, and required outputs.
- Phase-output ownership matrix.
- Unified Capacitor execution recommendation.
- Rejected-candidate table with deterministic reason codes.
- Closure check: all required outputs are owned.

## Capacitor Skill Family

| Skill | Domain | When to Invoke |
|---|---|---|
| `capacitor-source-curation` | Source grounding | When any Capacitor guidance must be verified against official sources, or before authoring/updating skills |
| `capacitor-setup` | Project initialization | When starting a new Capacitor project, adding a platform, or auditing `capacitor.config.ts` |
| `capacitor-web-integration` | Framework integration | When integrating Capacitor into React, Vue, Angular, or SvelteKit; platform detection; live-reload |
| `capacitor-native-apis` | Official plugin usage | When using Camera, Geolocation, Preferences, Push Notifications, or any official/community plugin |
| `capacitor-plugin-authoring` | Custom plugins | When a required native capability is not covered by an existing plugin |
| `capacitor-auth-session` | Authentication and session lifecycle | When implementing OAuth/PKCE flows, token refresh, callback validation, or logout hardening |
| `capacitor-offline-resilience` | Offline continuity and recovery | When network-dependent features must remain reliable during disconnect, retry, and reconnect |
| `capacitor-observability` | Telemetry and diagnostics | When production diagnostics, traceability, alerts, and privacy-safe telemetry are required |
| `capacitor-security` | Security hardening | When preparing for production, handling sensitive data, or addressing security findings |
| `capacitor-testing` | Test strategy | When establishing tests, mocking native plugins, or configuring CI test runs |
| `capacitor-ci-integration` | CI and artifact automation | When Capacitor workflows must run reproducibly in CI with signing-safe automation |
| `capacitor-performance-quality-gate` | Performance gate decisioning | When a candidate needs startup, rendering, memory, and bridge-latency go/no-go checks |
| `capacitor-migration-upgrades` | Version migration governance | When upgrading Capacitor core/plugins with compatibility and rollback controls |
| `capacitor-live-updates` | OTA live update delivery | When implementing OTA updates, staged rollout, bundle verification, or rollback governance |
| `capacitor-accessibility` | Hybrid accessibility | When VoiceOver/TalkBack, focus management, ARIA, or WCAG compliance in the WebView is required |
| `capacitor-deep-linking` | Deep links and Universal / App Links | When implementing Universal Links, App Links, custom URL schemes, or tap-to-route navigation |
| `capacitor-environment-config` | Per-environment configuration | When managing `.env` strategy, `capacitor.config.ts` variants, native-layer per-env values, or secret hygiene |
| `capacitor-push-notifications` | Push notification delivery | When implementing APNs/FCM setup, notification channels, silent pushes, opt-in UX, or tap routing |
| `capacitor-privacy-compliance` | Privacy manifests and consent | When authoring iOS PrivacyInfo.xcprivacy, ATT prompts, Android data safety form, or GDPR/CCPA consent flows |
| `capacitor-release-readiness` | Release gate | When preparing for App Store or Play Store submission |

## Request Shape → Phase Mapping

| Request Shape | Primary Skills | Secondary Skills |
|---|---|---|
| New project from scratch | `capacitor-setup` → `capacitor-web-integration` | `capacitor-security`, `capacitor-testing` |
| Add native capability | `capacitor-native-apis` | `capacitor-security`, `capacitor-testing` |
| Build custom plugin | `capacitor-plugin-authoring` | `capacitor-testing`, `capacitor-security` |
| Add login/session flows | `capacitor-auth-session` | `capacitor-security`, `capacitor-testing` |
| Add offline support | `capacitor-offline-resilience` | `capacitor-native-apis`, `capacitor-testing` |
| Improve diagnostics | `capacitor-observability` | `capacitor-security`, `capacitor-ci-integration` |
| Stabilize CI pipelines | `capacitor-ci-integration` | `capacitor-testing`, `capacitor-release-readiness` |
| Validate performance for release | `capacitor-performance-quality-gate` | `capacitor-testing`, `capacitor-observability` |
| Upgrade Capacitor versions | `capacitor-migration-upgrades` | `capacitor-source-curation`, `capacitor-testing` |
| Add OTA live updates | `capacitor-live-updates` | `capacitor-ci-integration`, `capacitor-release-readiness` |
| Audit or implement accessibility | `capacitor-accessibility` | `capacitor-testing`, `capacitor-release-readiness` |
| Configure deep links | `capacitor-deep-linking` | `capacitor-security`, `capacitor-testing` |
| Set up per-environment config | `capacitor-environment-config` | `capacitor-ci-integration`, `capacitor-security` |
| Implement push notifications | `capacitor-push-notifications` | `capacitor-native-apis`, `capacitor-deep-linking`, `capacitor-testing` |
| Satisfy App Store / Play Store privacy requirements | `capacitor-privacy-compliance` | `capacitor-release-readiness`, `capacitor-observability` |
| Harden for production | `capacitor-security` → `capacitor-testing` → `capacitor-release-readiness` | `capacitor-source-curation` |
| Full project from zero to release | All 20 skills in order | See Phase-Output Ownership Matrix |
| Source or guidance validation | `capacitor-source-curation` | Any downstream skill with stale content |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Route one Capacitor request | Intake contract and phase map exist |
| L2 Delivery | Coordinate one Capacitor feature | Every required output has one owning phase |
| L3 Hardening | Production-grade Capacitor work | Security, testing, and release evidence expectations are explicit |
| L4 Expert Standardization | Reusable Capacitor operating model | Reusable intake, ownership, and routing rubric documented for cross-project use |

## Deterministic Workflow

1. Lock the objective, web framework, target platforms, required capabilities, risk level, and required outputs.
2. Classify the request into one or more phases using the Request Shape → Phase Mapping table.
3. Assign exactly one owner per required output using the Phase-Output Ownership Matrix below.
4. Reject any phase plan with unowned or multiply owned outputs.
5. Define evidence expectations and handoff criteria between phases.
6. Select the unified execution path: sequential phased execution, parallel phases, or stop pending blockers.
7. Produce the intake contract with all phase assignments.
8. Publish closure status with residual risks and open blockers.

## Phase-Output Ownership Matrix Template

| Required Output | Owning Skill | Evidence Expectation |
|---|---|---|
| `capacitor.config.ts`, platform registration, sync | `capacitor-setup` | Clean `cap sync` on clean build |
| Framework build alignment, platform detection pattern | `capacitor-web-integration` | Build produces correct `webDir` output |
| Native API implementation, permission flows, fallbacks | `capacitor-native-apis` | Permissions tested; web fallbacks present |
| Custom plugin TypeScript + iOS + Android | `capacitor-plugin-authoring` | Bridge methods smoke-tested on device |
| OAuth/PKCE flow, callback validation, token lifecycle | `capacitor-auth-session` | Auth state transitions validated on target platforms |
| Offline queueing, retries, reconciliation outcomes | `capacitor-offline-resilience` | Recovery scenarios pass data-integrity checks |
| Correlated logs, metrics, traces, and alert routing | `capacitor-observability` | Incidents are traceable across web and native layers |
| CSP, secure storage, permission audit, deep links | `capacitor-security` | Security checklist passes |
| Plugin mocks, unit tests, E2E, CI config | `capacitor-testing` | Tests pass in CI without real devices |
| Deterministic pipeline, signing-safe automation, artifacts | `capacitor-ci-integration` | CI artifacts are reproducible and promotion-ready |
| Startup/rendering/memory/bridge latency verdict | `capacitor-performance-quality-gate` | Explicit pass/fail recommendation with thresholds |
| Compatibility matrix, migration sequence, rollback path | `capacitor-migration-upgrades` | Upgrade checkpoints pass with executable rollback |
| OTA channel config, bundle verification, rollout gates | `capacitor-live-updates` | Staged rollout plan and rollback trigger documented |
| Focus management, ARIA, VoiceOver/TalkBack, touch targets | `capacitor-accessibility` | Manual test matrix passes on physical iOS and Android |
| AASA, assetlinks.json, appUrlOpen handler, fallback pages | `capacitor-deep-linking` | All URL patterns verified on physical iOS and Android |
| .env schema, capacitor.config.ts variants, native-layer config, secret hygiene | `capacitor-environment-config` | All environments build in CI; no secrets in source |
| APNs/FCM setup, channels, token handling, tap routing | `capacitor-push-notifications` | End-to-end delivery verified on physical devices for all notification types |
| PrivacyInfo.xcprivacy, ATT prompt, data safety form, consent flow | `capacitor-privacy-compliance` | Zero Xcode privacy warnings; data safety form complete; consent captures before SDK init |
| Icons, signing, versioning, store metadata, smoke tests | `capacitor-release-readiness` | Go or no-go issued with evidence |
| Source freshness, drift log | `capacitor-source-curation` | Catalog updated; drift items assigned |

## Unified Decision Rules

- **Sequential execution** when each phase produces required inputs for the next (e.g., setup → integration → native APIs → release).
- **Parallel execution** when phases are independent (e.g., security hardening and testing can run simultaneously once setup is complete).
- **Stop pending blockers** when a required input is missing (e.g., no provisioning profile means release readiness cannot complete).

## Done Criteria

- Intake contract is documented with objective, risk level, and platform scope.
- Every required output has exactly one owning skill.
- Evidence expectations are defined for each phase.
- Execution path (sequential, parallel, or blocked) is selected and documented.
- Residual risks are explicit, prioritized, and owner-assigned.



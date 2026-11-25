# AGENTS.md — Selene

Operating manual for AI coding agents working in this repository. Read this before touching anything.

## Project snapshot

Selene is a cycle, fertility, and perimenopause tracker whose entire AI insight layer runs
on-device — no server to subpoena, breach, or sell data from, and the claim is verifiable in
airplane mode. **Who pays:** women 18–45 who churned from Flo/Clue after the $59.5M settlements,
plus the underserved 35–55 perimenopause wedge. Free manual logging forever; hard paywall on the
AI layer at $39.99/yr or $89.99 lifetime (zero marginal inference cost makes lifetime profitable).
**Status:** recommended (#1 of 9 finalists in the edge-AI run). iOS-first; Android is phase 2.

## Read first

| File | What it gives you |
|---|---|
| `README.md` | Research dossier: market evidence, adversarial review, recommended tech stack. Do not edit. |
| `DESIGN.md` | Architecture, module map, data model, key flows, milestones M0–M3. |
| `TOOLS.md` | Every command, the (deliberately tiny) external surface, CI behavior, harness notes. |

## Commands

`just` is the single source of truth. Never invoke `xcodebuild`/`swiftlint` etc. directly.

| Recipe | What it does |
|---|---|
| `just` | List recipes. |
| `just bootstrap` | Generate `Selene.xcodeproj` via XcodeGen and resolve SPM packages. |
| `just build` | Build the `Selene` scheme for the iOS Simulator. |
| `just test` | Run `swift test` (core suite, macOS), then the app suite on the simulator (falls back to an available iPhone). |
| `just lint` | SwiftLint over the repo (skips with a notice when swiftlint is absent). |
| `just format` | swiftformat in place. |
| `just ci` | lint + build + test — must be green before any commit. |

Until M0 the repo is docs-only; recipes fail with guidance instead of cryptic errors. That is expected.

## Architecture summary

Capture (manual tap-log, free-text/voice via SpeechAnalyzer, strip photo) → on-device inference
(FoundationModels `@Generable` structured extraction; custom Core ML CNN for strips) → encrypted
local store (GRDB, `NSFileProtectionComplete`, backup-excluded) → deterministic hierarchical
Bayesian `CycleEngine` produces all forecasts → `InsightKit` narrates engine output grounded in a
citation-pinned content pack → SwiftUI surface. StoreKit 2 is the only networked module. Modular
SPM packages under an XcodeGen-generated app shell; Swift 6 strict concurrency throughout.

```text
project.yml            — XcodeGen spec (committed; .xcodeproj is generated, never committed)
App/                   — SwiftUI app shell, composition root only
Packages/
  SeleneCore/          — domain models, symptom taxonomy, shared protocols (zero deps)
  CycleEngine/         — deterministic Bayesian cycle/ovulation/perimenopause forecaster (no LLM, no UI)
  Persistence/         — GRDB store, file protection, backup exclusion, migrations
  InsightKit/          — FoundationModels extraction + grounded narration over engine output
  StripVision/         — Vision strip detection + custom Core ML LH/hCG classifier
  ContentPack/         — citation-pinned ACOG/NICE-derived content + on-device embeddings (local RAG)
  Paywall/             — StoreKit 2 entitlements — the ONLY module permitted network access
  SeleneUI/            — design tokens, cycle wheel, shared components
```

## Coding standards

- Swift 6, strict concurrency enabled; no `@unchecked Sendable` without a comment justifying it.
- Files < 800 lines, functions < 50 lines; split before you hit the limit.
- Immutability by default: value types, `let`, pure functions in `CycleEngine` especially.
- Explicit error handling at every boundary — typed throws or `Result`; never swallow errors;
  user-facing failures get human copy, internals get structured log context (never log health data).
- No hardcoded secrets — and by design this app has none at runtime; anything dev-side is env vars.
- Conventional commits: `feat:` `fix:` `refactor:` `docs:` `test:` `chore:`.
- swiftformat + swiftlint are enforced by hooks and CI; don't fight them.

## Testing policy

- TDD: write the failing test first (RED → GREEN → REFACTOR). Target 80%+ coverage; `CycleEngine`
  and `Persistence` should sit near 100%.
- AAA pattern (Arrange–Act–Assert), descriptive behavior names, Swift Testing preferred (XCTest
  where UI tests require it).
- What matters most here, in order:
  1. **Forecast correctness** — golden-fixture tests for the Bayesian engine on synthetic cycle
     histories (regular, irregular, perimenopausal); seeded runs must be bit-reproducible.
  2. **Privacy proofs as tests** — egress-free operation, backup-exclusion flags, file protection
     attributes asserted in integration tests; dependency allowlist checked in CI.
  3. **Extraction fidelity** — `@Generable` free-text → structured entry against a labeled corpus,
     including refusal/unavailable fallback paths.
  4. **Strip classifier eval** — held-out accuracy gate (incl. faint-line cases) that blocks the
     feature flag, not just a unit test.
  5. **Migration safety** — GRDB schema migrations round-trip user data losslessly.

## PRODUCT INVARIANTS (non-negotiable)

Violating any of these is a blocking defect, regardless of who asked for the change.

1. **Zero health-data egress.** No networking primitive (`URLSession`, `Network`, sockets) outside
   `Paywall/`. Every feature must work in airplane mode. Testable: CI greps package sources for
   network imports outside `Paywall/`; an airplane-mode UI test exercises log → forecast → insight.
2. **Zero third-party SDKs.** No analytics, crash reporting, ads, or A/B SDKs — ever. Dependency
   allowlist (currently: GRDB) enforced against `Package.resolved` in CI.
3. **Deterministic before LLM.** Every date, probability, fertile window, and credible interval
   comes from `CycleEngine` only. The LLM never invents numbers; `InsightKit` has read-only access
   to `Forecast` and no write path into it.
4. **Grounded or silent.** Every medical claim in generated text carries a citation id resolving
   into `ContentPack`. On model refusal/unavailability, fall back to a deterministic template —
   never an error screen, never an ungrounded answer.
5. **Strip readings are advisory.** A `StripReading` is never auto-committed: explicit user
   confirmation required; below the confidence threshold the answer is "unclear — retest", never a
   guessed result. No diagnosis or contraception-efficacy language anywhere (App Review 1.4.1 /
   SaMD line; Natural Cycles needed FDA clearance for those claims — we make none).
6. **Data at rest is locked down.** GRDB with `NSFileProtectionComplete`; database excluded from
   iCloud/device backup by default; onboarding surfaces Advanced Data Protection guidance; export
   and delete are explicit local user actions. No accounts, no email collection.
7. **Manual logging is free forever.** The paywall gates the AI layer only. Never gate logging,
   historical data, or data export.

## Definition of done

- [ ] `just ci` green locally (lint + build + test).
- [ ] New behavior covered by tests written first; coverage ≥ 80% on touched modules.
- [ ] No invariant above weakened — re-read the list, it's seven items.
- [ ] No health data in logs, fixtures committed from real users, or screenshots.
- [ ] Files < 800 lines, functions < 50, errors handled at boundaries.
- [ ] Conventional commit message; docs (`DESIGN.md`/`TOOLS.md`) updated if behavior or commands changed.
- [ ] Anything touching `Persistence/`, `Paywall/`, or extraction of user text: run a security review pass.

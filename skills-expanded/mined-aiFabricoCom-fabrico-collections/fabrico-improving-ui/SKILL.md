---
name: fabrico-improving-ui
description: "Audit and verify existing web, iOS, Android, and shared-mobile UIs using runtime evidence, platform conventions, accessibility, prioritized findings, and before/after comparisons. Use for UI improvement audits, mobile visual reviews, responsive checks, or cross-platform UI verification without requiring Figma."
---

# Improving UI

Provides the cross-platform audit and evidence rules used when improving an existing product UI. Apply it to web,
iOS, Android, React Native, Flutter, Kotlin Multiplatform, and other shared-mobile projects without assuming that a
Figma design or browser target exists.

This skill audits an existing platform. It does not authorize creating a missing application target, inventing a
new visual language, or changing product behavior.

## Audit Process

Use the checklist below and track progress:

```text
UI improvement audit:
- [ ] Resolve platforms and coverage
- [ ] Establish product and design intent
- [ ] Capture a rendered baseline
- [ ] Audit and prioritize findings
- [ ] Classify the authorized change set
- [ ] Verify comparable after-state evidence
```

### 1. Resolve platforms and coverage

Detect the actual web, iOS, Android, and shared-code targets. Build a matrix of requested platforms, screens,
flows, states, themes, device classes, orientations, and accessibility conditions. Mark absent requested targets as
`NOT PRESENT`. State whether coverage is exhaustive or sampled.

### 2. Establish intent

Use approved specifications and designs, the existing design system and tokens, platform conventions, and available
research. An approved design is authoritative only for its stated scope. Record accessibility, usability, or
product conflicts instead of silently reproducing them. Without a design, preserve the existing visual direction.

### 3. Capture a baseline

Prefer a current build on a supported browser, simulator, emulator, or device. Exercise representative default,
loading, empty, error, validation, disabled, selected, focus, keyboard, text-scaling, theme, responsive, safe-area,
permission, and rotation states where supported. Collect screenshots, accessibility evidence, interactions, and
relevant runtime diagnostics.

Label each finding `OBSERVED` or `INFERRED`. Source, preview, snapshot, or stale screenshot inspection is secondary
evidence and must not be described as rendered or interaction verification.

Read and apply only the relevant [platform UI audit checks](references/platform-ui-audit.md).

### 4. Audit and prioritize

Record each finding with platform and screen, evidence, issue, user impact, recommendation, severity, confidence,
effort, implementation risk, authority class, affected scope, and verification method.

Use this severity scale:

- `CRITICAL` — prevents a core task or creates a serious accessibility, safety, or unusable-layout failure
- `MAJOR` — materially harms usability, accessibility, responsive behavior, or an important state
- `MINOR` — a limited, non-blocking defect with clear evidence
- `OPPORTUNITY` — an optional enhancement rather than a defect

Prioritize user impact over cosmetic preference. Do not present taste as evidence.

### 5. Classify the change set

- `AUTO` — objective, high-confidence, local, reversible, and preserves behavior, information architecture, brand,
  existing tokens, dependencies, and public contracts
- `APPROVAL REQUIRED` — subjective, broad, behavioral, brand, navigation, copy, dependency, asset, design-token,
  cross-platform parity, public-contract, or otherwise high-impact change
- `DEFERRED` — unsupported, out of scope, explicitly declined, or accepted for later

### 6. Verify the after state

Repeat the same platform, screen, state, device, theme, interaction, and accessibility matrix used for the baseline.
Capture comparable before/after evidence and run the project's relevant lint, type-check, unit, integration, UI,
snapshot, screenshot, build, and platform checks. A passing build is necessary evidence where applicable, but not
proof of visual quality by itself.

Allow at most three complete correction cycles. Re-run affected evidence after every correction.

## Evidence Confidence

| Confidence | Minimum evidence |
| --- | --- |
| `HIGH` | Current rendered target, representative states and interactions, relevant accessibility checks, and executable project gates |
| `MEDIUM` | Current screenshots or recordings plus source inspection and successful build or tests, but no interactive target inspection |
| `LOW` | Source, design, preview, snapshot, or stale captures only |

Do not make subjective visual changes from `LOW`-confidence evidence. Do not mark a platform `VERIFIED` without
`HIGH`-confidence after-state evidence.

## Completion States

- `VERIFIED` — runtime visual, interaction, accessibility, and required project checks passed
- `PARTIALLY VERIFIED` — safe work completed but runtime, device, state, screenshot, or assistive-technology evidence is incomplete
- `NOT PRESENT` — the requested target is absent
- `BLOCKED` — no safe implementation or verification path exists

## Connected Skills

- `fabrico-technical-context-discovering` — target and project convention discovery
- `fabrico-implementing-frontend` — compatible web and shared-framework implementation patterns
- `fabrico-ensuring-accessibility` — detailed web accessibility checks
- `fabrico-ui-verifying` — strict web Figma-versus-running-app comparison only
- `fabrico-reviewing-frontend` and `fabrico-code-reviewing` — implementation review

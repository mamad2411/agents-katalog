---
name: flutter-project-bootstrap
description: Scaffolds a Flutter app structure from developer requirements. Supports a guided questionnaire and a quick default mode, then generates architecture, dependencies, starter files, and 1-2 sample screens.
license: MIT
metadata:
  version: 0.1.0
  owner: mdazadhossain95
---
# Flutter Project Bootstrap

## Purpose
Use this skill to initialize a new Flutter project structure based on developer needs.

This skill supports two modes:
- Guided setup: ask requirement questions and generate from answers.
- Quick default setup: skip questions and apply a recommended baseline.

## Activation
Activate this skill when the user asks to bootstrap, scaffold, or initialize a Flutter app structure and wants architecture, dependencies, and starter code generated quickly.

## Non-Goals
- Do not implement full business logic for every feature.
- Do not generate production secrets or real keys.
- Do not install unsupported platform SDKs silently.

## Mode Selection
Ask this first:
- Do you want Guided setup or Quick default setup?

If user picks Quick default, skip interview and use the Default Profile section.
If user picks Guided setup, run the full questionnaire.

## Guided Questionnaire
Ask questions in this order. Accept either selected options or free text.

1) App type
- Example options: ecommerce, quick-commerce, rider, fintech, food-delivery, social, healthcare, custom.

2) Primary state management
- Example options: riverpod, bloc, getx, provider, custom.

3) Additional state management (optional)
- If multiple are chosen, keep one primary and isolate others by module.

4) Architecture style
- Example options: feature-first clean, layered by type, simple starter.

5) Backend strategy
- Example options: rest-api, firebase, supabase, hybrid.

6) API usage
- Ask: Will this app consume external APIs? (yes/no)
- If yes, ask for API style: rest, graphql, both.

7) Authentication
- Example options: email-password, google, apple, phone-otp, guest.

8) Push notifications
- Example options: firebase-fcm, onesignal, none.

9) Local persistence
- Example options: shared-preferences, secure-storage, hive, isar, sqlite, none.

10) Realtime needs
- Example options: websocket, firebase-realtime, none.

11) Payments (optional)
- Example options: stripe, razorpay, sslcommerz, none.

12) Target platforms
- Example options: android, ios, web, macos, windows, linux.

13) Flavors/environments
- Example options: dev, staging, prod.

14) Tooling
- Ask for optional setup: ci-cd, localization, accessibility baseline, analytics.

15) Starter screens
- Ask if user wants 1 or 2 sample screens and which feature area.

## Quick Default Profile
If user selects quick default, apply this baseline:
- App type: ecommerce starter
- Architecture: feature-first clean
- Primary state management: riverpod
- Backend: rest-api ready
- API usage: yes, rest
- Auth: email-password scaffold
- Push: firebase-fcm ready
- Local persistence: shared-preferences + secure-storage
- Realtime: none
- Payments: none
- Platforms: android + ios
- Flavors: dev + prod
- Starter screens: splash + home catalog sample

Always print a summary of applied defaults before generation.

## Decision Rules
- If multiple state management options are requested, require one primary and place additional patterns in separate modules only.
- Do not mix two state patterns inside the same feature module.
- If backend=firebase and push=onesignal, allow both.
- If backend=none and api=no, generate local/offline starter only.
- If platforms include web, avoid mobile-only plugin setup in generated instructions.
- If payments are enabled, scaffold abstraction layer and placeholder service only.

## Generation Contract
After collecting requirements, generate the following:

1) Folder structure
- core/
- config/
- shared/
- features/
- data/
- domain/
- presentation/
- routes/

2) Core setup
- app entry wiring
- theme setup
- route config
- dependency injection bootstrap
- environment/flavor config if requested

3) Dependencies
- Add only required packages for selected options.
- Group packages by: state, network, storage, push, auth, payments, utilities.

4) Starter implementation
- Create 1-2 sample screens based on requested app type.
- Add basic navigation between generated screens.
- Include placeholder repository/service contracts.

5) Developer handoff output
- Print:
  - selected options summary
  - generated directories/files summary
  - package summary
  - next 5 recommended implementation steps

## Validation Checklist
Before completing, verify:
- No contradictory choices remain unresolved.
- Generated structure matches selected architecture.
- Chosen state management is wired as primary.
- Selected services (push/auth/storage) are reflected in dependencies and stubs.
- At least one starter route and one starter screen exist.

## Failure Handling
If requirements conflict or are incomplete:
- Apply safe defaults for missing optional inputs.
- For blocking conflicts, resolve with deterministic fallback:
  - state management fallback: riverpod
  - backend fallback: rest-api
  - push fallback: none
- Continue generation and clearly report fallback decisions.

## Completion Output Template
Use this format at the end:
1. Setup mode: guided | quick-default
2. Selected stack: <app type, state, backend, push>
3. Generated artifacts: <folders/files/screens>
4. Installed package groups: <state/network/storage/...>
5. Next steps:
- Step 1
- Step 2
- Step 3
- Step 4
- Step 5

---
name: maui-quarterback
description: >
  Workflow skill that coordinates multi-concern .NET MAUI work before code changes.
  Use when a request touches several MAUI domains at once and Codex must choose the
  right primary skill, attach only the needed secondary skills, prevent routing or
  scope conflicts, and sequence implementation safely.
  USE FOR: "complex MAUI feature", "orchestrate MAUI", "multi-skill MAUI",
  "MAUI architecture flow", requests that combine MVVM, navigation, auth, API,
  storage, permissions, platform code, UI polish, performance, testing, or migration.
  DO NOT USE FOR: isolated single-concern tasks that already map cleanly to one skill,
  or non-MAUI work.
---

# MAUI Quarterback

Use this skill as the entrypoint for broad, ambiguous, or multi-surface .NET MAUI requests.
It does not replace feature skills. It decides ownership, sequencing, and guardrails so the
downstream skills do not fight each other.

## Core Rules

- Always load `maui-current-apis` before writing MAUI code.
- Pick exactly one primary owner skill for the request.
- Attach at most 3 secondary skills in the same implementation wave.
- Do not let helper skills take over a request that is clearly owned by a feature skill.
- Respect the repo's existing app model first: plain MAUI, Shell, Blazor Hybrid, MauiReactor, or migration.
- If the request spans too many concerns for one pass, split it into waves before editing.

## Workflow

1. Run preflight.
- Read the app `.csproj` and detect target frameworks.
- Detect app style: plain MAUI, Shell, Blazor Hybrid, MauiReactor, or Xamarin migration.
- Scan package versions that affect API choice or pattern choice.
- Load `maui-current-apis` as the API guardrail.

2. Frame the request as concerns.
- Classify each requirement into one flat list:
  `ui-structure`, `state-binding`, `navigation`, `auth`, `network`, `storage`,
  `device`, `platform`, `notifications`, `performance`, `testing`, `migration`.
- Separate the user's true outcome from implementation detail. A "login page" is usually
  a UI feature first, not an authentication skill first.

3. Choose the primary owner.
- Pick the skill that owns the user's main outcome.
- Use secondary skills only to constrain technical edges around that outcome.
- If two skills both look plausible, prefer the one that controls the feature boundary,
  not the one that handles one internal concern.

4. Build waves if needed.
- Use a single wave for a narrow feature with one owner and up to 3 helper concerns.
- Use multiple waves when the request mixes setup, reusable infrastructure, and UI delivery.
- Typical order:
  wave 1 - structure and guardrails
  wave 2 - integrations and state flow
  wave 3 - polish, performance, and tests

5. Hand off with an explicit contract.
- State the primary owner.
- State the secondary skills.
- State which nearby skills were rejected and why.
- State the verification required before the work is considered complete.

## Routing Matrix

Route by main outcome, not by whichever skill has the loudest keyword match.

- `Build or refactor a MAUI feature page, viewmodel, commands, validation, or stateful UI`:
  Use `maui-mvvm` as primary.
- `Fix or author bindings without broader feature reshaping`:
  Use `maui-data-binding` as primary.
- `Build item-heavy lists, grids, virtualization, swipe items, or templated collections`:
  Use `maui-collectionview` as primary.
- `Implement in-app Shell routes, tabs, flyouts, query parameters, or back-stack flow`:
  Use `maui-shell-navigation` as primary.
- `Handle external entry points such as app links, universal links, intent filters, or callback URIs`:
  Use `maui-deep-linking` as primary.
- `Implement sign-in, token acquisition, WebAuthenticator, or MSAL client flows`:
  Use `maui-authentication` as primary.
- `Persist secrets or credentials safely on device`:
  Use `maui-secure-storage` as primary.
- `Consume a backend over HTTP without Aspire orchestration`:
  Use `maui-rest-api` as primary.
- `Connect a MAUI app to Aspire-hosted services`:
  Use `maui-aspire` as primary.
- `Add offline/local relational persistence`:
  Use `maui-sqlite-database` as primary.
- `Handle generic file pick, save, open, or app-local file I/O`:
  Use `maui-file-handling` as primary.
- `Handle camera/gallery media capture or media picking`:
  Use `maui-media-picker` as primary.
- `Handle device location retrieval`:
  Use `maui-geolocation` as primary.
- `Render maps, pins, regions, or map interactions`:
  Use `maui-maps` as primary.
- `Bridge platform APIs or native SDK calls without building a custom control`:
  Use `maui-platform-invoke` as primary.
- `Build or migrate custom controls, handlers, or platform render behavior`:
  Use `maui-custom-handlers` as primary.
- `Handle local scheduled notifications`:
  Use `maui-local-notifications` as primary.
- `Handle remote push notifications and registration flow`:
  Use `maui-push-notifications` as primary.
- `Audit or optimize runtime responsiveness, startup, scrolling, or memory behavior`:
  Use `maui-performance` as primary.
- `Design or repair unit tests around MAUI viewmodels and services`:
  Use `maui-unit-testing` as primary.
- `Migrate Xamarin.Forms to MAUI`:
  Use `xamarin-forms-migration` as primary.
- `Migrate Xamarin.Android native apps`:
  Use `xamarin-android-migration` as primary.
- `Migrate Xamarin.iOS/macOS/tvOS native apps`:
  Use `xamarin-ios-migration` as primary.

## Conflict Rules

- `maui-current-apis` is mandatory guardrail, not the primary owner, unless the task is explicitly an API-currency audit.
- `maui-mvvm` owns end-to-end feature composition for most UI feature work.
  `maui-data-binding`, `maui-shell-navigation`, and `maui-dependency-injection` are usually helpers in that lane.
- `maui-shell-navigation` owns in-app flow. `maui-deep-linking` owns external entry.
  Do not let deep-linking drive ordinary page-to-page navigation.
- `maui-authentication` owns login and token acquisition.
  `maui-secure-storage` owns persistence only.
  `maui-rest-api` owns HTTP consumption only.
- `maui-aspire` supersedes `maui-rest-api` when the app is consuming Aspire-hosted services.
- `maui-permissions` is usually a helper skill.
  If a feature skill already documents its permission traps, keep that feature skill primary.
- `maui-platform-invoke` is for native APIs and platform services.
  `maui-custom-handlers` is for custom control rendering or platform view customization.
- `maui-local-notifications` and `maui-push-notifications` are distinct lanes.
  Do not treat remote delivery as a local-notification task.
- `maui-geolocation` gets coordinates.
  `maui-maps` renders and manipulates maps.
- `maui-media-picker` is for photos and media capture/pick flows.
  `maui-file-handling` is for generic files.
- `maui-performance` and `maui-unit-testing` should not take over feature implementation unless
  the user explicitly asked for performance work or test work.
- Migration skills win over feature skills during migration work.
  Add feature skills only for isolated post-migration follow-up.

## Common Bundles

Use these as defaults, then trim them down if the request is narrower than it sounds.

- `Authenticated CRUD page`:
  primary `maui-mvvm`; helpers `maui-authentication`, `maui-rest-api`, `maui-shell-navigation`
- `Login flow with token persistence`:
  primary `maui-authentication`; helpers `maui-secure-storage`, `maui-deep-linking`
- `Offline-first list/detail flow`:
  primary `maui-mvvm`; helpers `maui-sqlite-database`, `maui-rest-api`, `maui-collectionview`
- `Location-aware screen`:
  primary `maui-mvvm`; helpers `maui-geolocation`, `maui-maps`, `maui-permissions`
- `Capture and upload media`:
  primary `maui-media-picker`; helpers `maui-permissions`, `maui-file-handling`, `maui-rest-api`
- `Platform feature exposed through a normal page`:
  primary `maui-mvvm`; helpers `maui-platform-invoke`, `maui-dependency-injection`
- `Migration plus stabilization`:
  primary one of the `xamarin-*` skills; helpers `maui-current-apis`, `maui-performance`

## Stop Conditions

Pause and re-scope before editing when:

- the repo mixes two competing navigation models and the active one is unclear
- the target framework or package version is unknown and affects API choice
- the request mixes migration, new feature delivery, and performance work in one jump
- more than 3 helper skills are required in the same wave
- the user asks for a testing lane that depends on a missing downstream skill
- the request is really an ASP.NET Core or Figma job, not a MAUI job

## Handoff Contract

Hand off to downstream work with this structure:

- `App style`: plain MAUI, Shell, Blazor Hybrid, MauiReactor, or migration
- `Primary skill`: the single owner
- `Secondary skills`: only the helpers needed in the current wave
- `Rejected skills`: nearby skills deliberately not chosen
- `Wave`: current wave number and scope
- `Files likely touched`: page, viewmodel, services, platform files, app startup, tests
- `Verification`: build, navigation flow, permission flow, device behavior, test coverage, manual checks
- `Open risks`: package mismatch, platform asymmetry, missing assets, missing backend contract

## Special Cases

- For Blazor Hybrid inside a MAUI shell, keep `maui-current-apis` loaded and bring in `aspnet-core`
  only for Razor/component concerns. Do not let `aspnet-core` take over MAUI host decisions.
- For MauiReactor codebases, still use this skill for routing, but verify package versions before
  choosing MVVM-oriented advice from other skills.
- If a needed downstream skill is missing from the repo, call it out explicitly in the handoff
  instead of pretending another skill fully covers it.

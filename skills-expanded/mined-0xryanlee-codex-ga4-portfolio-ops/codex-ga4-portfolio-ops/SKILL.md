---
name: codex-ga4-portfolio-ops
description: Use when planning, creating, administering, instrumenting, auditing, reporting on, integrating, privacy-reviewing, or testing GA4 across websites, WebApps, macOS desktop apps, Android/iOS apps, WebViews, server-side/offline flows, or agent-operated repositories. The Agent Skills-compatible workflow covers properties, streams, events, CTA/conversion design, consent, PII, APIs, Google Ads, BigQuery, Data API, Admin API, Measurement Protocol, Computer Use, cursor flows, and Realtime/DebugView QA.
---

# Codex GA4 Portfolio Ops

## Overview

Use this skill as the portfolio-level operating procedure for GA4. It separates the reusable measurement contract from product-specific implementation, and it records every admin-console action so a later run can reproduce or audit the work. The admin-console portion is explicitly for Codex Computer Use; code changes belong in the target repository.

Read `references/ga4-lifecycle-map.md` for the full strategy, privacy, integration, reporting, and operations checklist. Read `references/agent-compatibility.md` when the caller is Claude Code, Cursor, TRAE, OpenClaw, Hermes Agent, CodeBuddy, VS Code/Copilot, OpenCode, Goose, Amp, or another Agent Skills-compatible runtime. Read `references/keyword-map.md` when writing public documentation or AEO content.

## Operating rules

- Inspect the real host, repository, runtime, and existing tags before creating a stream. Do not infer a production domain from a local preview or deployment provider.
- Use one Web data stream per independent public host unless the same user journey intentionally crosses domains. Use Firebase app streams for native Android, iOS, and macOS apps. A macOS or Android app can use GA4; native-only apps should not be treated as ordinary web pages.
- Keep exactly one GA4 loader/config per runtime surface. Preserve Enhanced Measurement where appropriate, and check for duplicate tags before adding another.
- Never put a Measurement Protocol `api_secret`, service-account credential, or browser credential in source, a mobile bundle, a public repository, or a client-side environment variable.
- GA4 event names are `lower_snake_case`, at most 40 characters, and must not start with reserved prefixes such as `firebase_`, `google_`, or `ga_`. Do not send email addresses, names, phone numbers, full URLs containing identifiers, or other direct PII as event parameters.
- Treat an intent event and a success event as different things: `cta_click` means a click; `generate_lead`, `sign_up`, `begin_checkout`, and `purchase` mean a later business outcome.
- Record Computer Use evidence as structured rows: timestamp, project, page, visible label, semantic locator or `element_index`, coordinate fallback, action, result, and verification state. Re-query the live UI before every action; element indices are not stable.
- Use `apply_patch` for repository edits and run the target repository's available lint/build/runtime checks. Do not widen a patch to fix unrelated worktree errors.
- Treat the measurement plan as a versioned contract: schema, consent, key events, integrations, QA state, owner, and deprecation notes travel with the code change.
- Use the Google Analytics Admin API for governed repeatable configuration reads/writes, the Data API for reports/realtime/funnels, and Measurement Protocol only for secure server/offline supplementation. Prefer official APIs over ad-hoc scraping when an approved credential path exists.
- Keep legal/privacy review, access roles, retention, deletion, internal traffic, unwanted referrals, Google Signals, and Consent Mode as explicit checklist items; this skill is not legal advice.

## Workflow

### 1. Inventory and scope

Create or update a measurement-plan JSON using `references/measurement-plan.template.json`. For every project record:

`project_key`, public host or app package/bundle ID, surface type (`web`, `webapp`, `android`, `ios`, `macos`, or `desktop_webview`), owner, intended journey, stream strategy, current tag/SDK state, and open questions.

Also record `privacy`, `key_events`, `integrations`, `qa`, and `change_owner`. Run `scripts/validate-ga4-map.mjs` before implementation and again after the event map changes.

Resolve these decisions before admin work:

- Independent marketing/product site: its own Web stream.
- One journey intentionally crossing domains: one stream with documented cross-domain configuration.
- Android/iOS/macOS native app: Firebase app stream and native SDK, with `screen_view` and app lifecycle events.
- Desktop app built around a web surface: instrument the web surface first; add a native bridge only when native-only actions matter.

### 2. Define the reusable contract

Start with the baseline event set and extend only when a product decision needs it:

| Intent or lifecycle | Event | Required parameters when applicable |
| --- | --- | --- |
| CTA interaction | `cta_click` | `cta_id`, `cta_location`, `destination_type` |
| Contact intent | `contact_open` / `contact_click` | `channel`, `cta_location` |
| Lead outcome | `generate_lead` | `lead_type`, `source_surface` |
| Content selection | `select_content` | `content_type`, `content_id` |
| Download intent | `download_click` | `product_id`, `platform`, `cta_location` |
| Account outcome | `sign_up` / `login` | `method` |
| Commerce | `begin_checkout` / `purchase` / `refund` | product/value fields per GA4 commerce rules |
| Native navigation | `screen_view` | `screen_name`, `screen_class` |
| Onboarding | `tutorial_begin` / `tutorial_complete` | `tutorial_id` |

Use the detailed naming and CTA rules in `references/event-and-cta-standard.md`. Run `scripts/validate-ga4-map.mjs` against the plan before implementation.

For the complete lifecycle, check strategy, collection, schema, privacy, integrations, APIs, QA, reporting, and operations in `references/ga4-lifecycle-map.md`.

### 3. Implement the smallest useful layer

For a Web or WebApp surface:

1. Load `gtag.js` once from the approved Measurement ID, normally through the framework's supported script component.
2. Set the document URL/title through the normal GA4 config path; do not manually duplicate automatic `page_view` unless there is a documented reason.
3. Add a small client-safe `trackEvent` wrapper with no secrets and a no-op fallback when `window.gtag` is unavailable.
4. Instrument meaningful CTA components with stable semantic IDs and locations. Prefer component-level instrumentation over a brittle global selector.
5. Keep success events at the point where the outcome is confirmed, not merely when the user opens a form or checkout page.

For Android, iOS, or macOS:

1. Use the Firebase/GA4 app stream and the platform SDK supported by the app's current release toolchain.
2. Map screen navigation to `screen_view`; map native-only actions to the same product event vocabulary used on the web.
3. Keep the app instance ID and SDK configuration appropriate for the platform. Never ship a Measurement Protocol secret.
4. Verify on a debug build/device with the platform's debug mechanism and GA4 DebugView.

For server-side/offline paths:

1. Keep client tagging or Firebase collection as the baseline whenever available.
2. Use Measurement Protocol only to supplement confirmed server/offline outcomes.
3. Keep `api_secret` and service credentials in a server-side secret manager, never in a bundle, skill, public repo, or log.
4. Validate identity joining, timestamp, consent, deduplication, and attribution before production use.

For reporting and integrations:

1. Mark only true business outcomes as key events.
2. Link Google Ads, Search Console, Firebase, BigQuery, Looker Studio, CRM, or commerce systems only when the reporting question and permissions are documented.
3. Use the Admin API for configuration governance and the Data API for reports; include dry-run, quota, retry, authorization, and audit controls.

### 4. Admin-console work with Codex Computer Use

Use the local Computer Use skill and the persistent `mcp__node_repl__js` session. The canonical pattern is:

```javascript
const state = await sky.get_app_state({app: "com.apple.Safari", disableDiff: true});
// Derive the current visible control from this state, then act.
```

For each click or typing action:

1. Capture the current UI state and derive a fresh `element_index` from visible text/role.
2. Prefer the semantic element index. Use coordinates only as a documented fallback, and record viewport coordinates plus visible context.
3. Execute one action, then capture the resulting state.
4. Append a structured row to the run log. The log is evidence, not a replacement for GA4 Realtime/DebugView verification.
5. Stop and surface a mismatch if the account, property, host, or stream shown by the UI is not the expected target.

Never use hidden browser APIs, DOM injection, or guessed stale indices to bypass the visible UI. The reusable action-log shape is in `references/computer-use-runbook.md`.

### 5. Reuse cursor flows and batch safely

The executed admin paths are captured as reusable cursor flows in `references/cursor-flows.md`. A flow stores the route, visible labels, expected state transitions, and any evidence-backed coordinate fallback. It is a fast path cache, not permission to blindly replay stale indices.

Before replaying a flow, verify:

1. The current account, property, route signature, viewport, and locale match the flow preconditions.
2. The visible control label and surrounding state match the expected checkpoint.
3. The cached `element_index` is re-derived from the current state. Accessibility indices are session-state data, not stable selectors.
4. A coordinate fallback is used only with the same viewport/layout and only when it was recorded from a visible control. Never guess a coordinate.

For independent streams, prepare a batch queue (`property -> host -> stream name -> verification`) and execute it as short visible batches. Keep the form-fill sequence continuous after the state is stable, but pause at every property/stream creation boundary to capture the result and Measurement ID. A batch must stop on an unexpected dialog, validation error, account change, host mismatch, or missing result.

Use bounded waits for UI animation, navigation, and network completion; prefer an explicit state check over a fixed sleep. A small, documented 150–500 ms settle window can reduce accidental double-clicks. Do not add random mouse jitter, fake hesitation, stealth timing, hidden APIs, or other behavior intended to evade bot detection or bypass a site's security controls. The goal is reliable visible automation and clear evidence, not impersonation.

### 6. Verify and hand off

Acceptance requires both code/runtime and admin-console evidence:

- Production or an explicitly documented staging host renders exactly one GA4 tag with the expected ID.
- A clean page load appears as `page_view` in Realtime; a controlled CTA click appears as `cta_click` with the expected parameters in DebugView.
- A success path produces the intended outcome event once. Check for duplicate events, not just event presence.
- Enhanced Measurement is intentionally on or off and the decision is documented.
- Only true business outcomes are marked as key events.
- Cross-domain behavior is tested only where the journey actually crosses domains.
- Build/lint/runtime results are reported with pre-existing failures separated from changes made by this skill.

## Deliverables

Every run should leave:

1. An inventory/measurement plan.
2. A naming and event map, including CTA locations.
3. A code diff or explicit no-code decision.
4. A Computer Use action log for admin changes, including button labels/positions when used.
5. Privacy/consent/PII and access-control status.
6. Integration/API/reporting status.
7. Realtime/DebugView evidence, regression checks, and unresolved follow-ups.

Use the public playbook repository's README as a shareable introduction, but keep account-specific IDs and internal project notes in the target workspace's private contract.

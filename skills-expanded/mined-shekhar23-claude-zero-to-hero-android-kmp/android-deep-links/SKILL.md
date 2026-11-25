````skill
---
name: android-deep-links
description: |
  Android deep link and app link patterns - route mapping, typed arguments, guarded entry points, deferred navigation, and integration with Compose Navigation. Use this skill whenever adding app links, handling inbound URLs, mapping external routes to screens, or deciding how deep links should interact with auth and feature navigation. Trigger on phrases like "deep link", "app link", "URL route", "handle inbound link", "open screen from link", or "deferred navigation".
---

# Android Deep Links and App Links

## Core Principles

- Deep links are external entry points and must be treated as untrusted input.
- Keep URL parsing and navigation mapping explicit.
- Pass only validated, minimal arguments into feature navigation.
- Deep links should integrate with the app's existing navigation architecture, not bypass it.
- Auth and feature availability rules still apply when arriving from a link.

---

## Route Ownership

Prefer a clear mapping layer:

```text
incoming URL -> parse -> validate -> map to app destination -> navigate
```

Do not scatter raw URI parsing across multiple screens.

A small coordinator or mapper near the app/navigation layer should decide what in-app destination a link represents.

---

## Compose Navigation Integration

Deep links should map into the same typed routes used by normal navigation.

Example flow:
- incoming URL `/notes/123`
- parser validates `123`
- app maps it to `NoteDetailRoute(noteId = "123")`
- `NavController` navigates normally

See the **android-navigation** skill for typed route patterns.

---

## Validation Rules

Always validate:
- host and scheme
- required path/query parameters
- expected ID formats
- feature availability
- auth requirements

Bad pattern:
- trusting arbitrary query params and sending them straight into screen state

Good pattern:
- parse to a typed destination only after validation succeeds

---

## Auth-Gated Deep Links

If a destination requires authentication:
- detect that requirement in the app-level deep link handler
- route user through auth if needed
- continue to the intended destination only after session is valid

```text
link -> protected destination -> auth required -> login -> continue to target
```

Do not drop the destination silently if continuation is expected.

See the **android-auth-security** skill.

---

## Deferred Navigation

Some deep links cannot open immediately because the app needs setup first:
- session restore
- onboarding completion
- feature flags/config fetch
- splash/bootstrap work

In those cases:
- store a pending destination in a small app coordinator
- complete startup/auth checks
- navigate once the app is ready

Keep this logic at the app/root level, not inside random feature screens.

---

## Fallback Behavior

Always define fallback behavior for invalid or unsupported links:
- show safe default destination
- show an error message/snackbar when appropriate
- ignore unknown routes safely
- optionally log redaction-safe diagnostics

Do not crash because a malformed link arrived.

---

## Multiple Entry Sources

Deep-link-like entry can come from:
- app links / web URLs
- push notifications
- widgets
- shortcuts
- external share/open intents

Prefer mapping all of them into one internal destination model so navigation logic stays unified.

---

## Internal Destination Model

A typed destination model keeps parsing separate from navigation:

```kotlin
sealed interface AppLinkDestination {
    data class NoteDetail(val noteId: String) : AppLinkDestination
    data object Settings : AppLinkDestination
}
```

Then convert `AppLinkDestination` to navigation actions near the app root.

---

## Security and Privacy

Rules:
- never trust inbound parameters blindly
- avoid placing secrets in deep-link URLs
- sanitize anything that may reach logs or analytics
- be careful with links that trigger destructive or sensitive actions

Deep links should usually open a screen, not perform irreversible actions automatically.

---

## Testing Guidance

Test:
- valid URL to destination mapping
- invalid URL rejection/fallback
- auth-gated continuation flow
- behavior when app is cold-started from a link
- duplicate handling when the same link is opened repeatedly

Use unit tests for parsing/mapping logic and integration tests for app navigation behavior where practical.

---

## Checklist: Adding Deep Links

- [ ] Define accepted schemes, hosts, and paths explicitly
- [ ] Parse and validate URLs in one mapping layer
- [ ] Map to typed internal destinations or nav routes
- [ ] Respect auth and startup gating rules
- [ ] Add safe fallback behavior for invalid links
- [ ] Test valid, invalid, and deferred-entry cases
````
---
name: android-analytics-logging
description: |
  Analytics, logging, and observability patterns for Android/KMP - event design, screen tracking, structured logs, crash reporting boundaries, redaction, and environment-aware telemetry. Use this skill whenever adding analytics events, logging app behavior, instrumenting user flows, or deciding what should go to logs versus metrics versus crash reports. Trigger on phrases like "analytics", "logging", "telemetry", "screen tracking", "event tracking", "crash reporting", "observability", or "redaction".
---

# Android Analytics, Logging, and Observability

## Core Principles

- Instrument intent, not noise.
- Logs are for debugging and operations; analytics are for product understanding.
- Never leak secrets, tokens, raw personal data, or sensitive payloads.
- Centralize telemetry contracts so naming stays consistent.
- Track user-relevant flows and operationally important failures.

---

## Separate the Concerns

| Concern | Purpose |
|---|---|
| Logging | developer/debug/operator visibility |
| Analytics | product usage and funnel understanding |
| Crash reporting | fatal and non-fatal failure monitoring |
| Metrics | rates, latency, counts, health signals |

Do not use one tool to imitate all four concerns.

---

## Event Design

Analytics events should be:
- stable
- human-readable
- intentionally named
- low-cardinality where possible

Good examples:
- `note_created`
- `login_succeeded`
- `paywall_shown`
- `sync_failed`

Bad examples:
- `button_clicked`
- `screen_event_7`
- raw dynamic strings as event names

Prefer fixed event names with structured properties.

---

## Event Properties

Good properties are small, explicit, and analysis-friendly:

```kotlin
data class AnalyticsEvent(
    val name: String,
    val properties: Map<String, String>
)
```

Good property examples:
- `source = settings`
- `result = success`
- `permission = camera`
- `network_state = offline`

Avoid:
- full user-entered text
- access tokens
- email addresses unless policy explicitly allows and requires it
- large blobs or stack traces in analytics payloads

---

## Screen Tracking

Track meaningful screens and major state transitions only.

Guidelines:
- one canonical name per screen
- track once on meaningful entry
- avoid duplicate emissions on every recomposition

In Compose, screen tracking should happen in a controlled side-effect wrapper or Root composable, not scattered across child composables.

---

## Logging

Use structured logging with clear tags/categories:

```kotlin
logger.i { "Sync started" }
logger.e(throwable) { "Sync failed" }
```

Good logging targets:
- startup milestones
- sync start/success/failure
- background worker outcomes
- recoverable errors that matter operationally

Do not log every recomposition, every `Flow` emission, or noisy internal loops.

---

## Crash Reporting Boundaries

Crash reporting should capture:
- uncaught fatal exceptions
- important non-fatal exceptions that indicate broken flows
- release/build metadata helpful for debugging

Do not report expected domain failures like invalid credentials as crashes.

Expected failure -> analytics/logging if useful
Unexpected failure -> crash reporting and structured logs

---

## Redaction Rules

Always redact or omit:
- passwords
- auth tokens
- refresh tokens
- cookies
- authorization headers
- personally sensitive payloads
- full request/response bodies from sensitive endpoints

Redaction is a product rule, not an optional cleanup pass.

See the **android-auth-security** skill for adjacent secret-handling guidance.

---

## Telemetry Abstraction

Wrap analytics/logging providers behind interfaces:

```kotlin
interface AnalyticsTracker {
    fun track(event: AnalyticsEvent)
}

interface AppLogger {
    fun info(message: String)
    fun error(message: String, throwable: Throwable? = null)
}
```

Benefits:
- easier testing
- vendor independence
- consistent naming and redaction policy

---

## Where Instrumentation Lives

- presentation layer -> user interactions and screen views
- domain/data layer -> operational events like sync success/failure when product-relevant
- app/bootstrap layer -> startup and environment signals

Do not spread analytics calls arbitrarily through every composable. Prefer a small number of deliberate tracking points.

---

## Environment Awareness

Telemetry behavior often differs by environment:
- debug -> verbose logs, limited analytics
- staging -> near-production analytics with safe isolation
- production -> redacted logs, full critical telemetry

Keep environment gating centralized.

---

## Testing Guidance

Test:
- correct event names/properties for critical flows
- no duplicate emission for one user action
- redaction behavior for sensitive fields
- crash/log reporting boundaries for expected vs unexpected failures

Prefer fake trackers in tests:

```kotlin
class FakeAnalyticsTracker : AnalyticsTracker {
    val events = mutableListOf<AnalyticsEvent>()
    override fun track(event: AnalyticsEvent) {
        events += event
    }
}
```

---

## Checklist: Adding Telemetry

- [ ] Define stable event names and low-cardinality properties
- [ ] Separate logs, analytics, crashes, and metrics by purpose
- [ ] Centralize tracking interfaces and naming
- [ ] Redact or omit all sensitive data
- [ ] Track only meaningful user and operational events
- [ ] Test critical event emission and non-duplication
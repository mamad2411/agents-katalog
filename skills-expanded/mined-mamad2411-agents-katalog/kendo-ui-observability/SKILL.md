---
name: kendo-ui-observability
description: Use when Kendo UI features need telemetry contracts for widget lifecycle failures, interaction latency, usage signals, and diagnosable production behavior.
---

# Kendo UI Observability

## Specialization

Define and apply Kendo-specific observability contracts that make UI behavior measurable and diagnosable: widget lifecycle errors, user interaction timings, data refresh latency, and reliability signals.

## Trigger Conditions

- Kendo UI features fail in production without actionable diagnostics.
- Teams need telemetry for Grid, forms, or dashboards.
- Performance regressions are suspected but not measured.
- Release quality decisions require UI evidence.

## Scope Boundaries

In scope:

- Event taxonomy for Kendo widget lifecycle and user actions.
- Latency metrics for load, filter, sort, and save flows.
- Error instrumentation points and correlation metadata.
- Dashboards and alerting requirements for Kendo feature health.

Out of scope:

- Telemetry platform procurement or vendor selection.
- Backend distributed tracing architecture.
- CI gate implementation details (see `kendo-ui-ci-integration`).

## Inputs

- Critical Kendo user journeys and SLAs.
- Existing logging and telemetry stack.
- Incident history and known blind spots.
- Privacy/compliance constraints for event payloads.

## Required Outputs

- Kendo telemetry event catalog with naming convention.
- Metric definitions and target thresholds.
- Error correlation contract with minimal diagnostic fields.
- Dashboard requirements for feature health.
- Validation plan proving instrumentation completeness.

## Core Patterns

### Interaction Timing Event

```javascript
function trackGridFilterApplied(startMs, resultCount) {
    emitTelemetry("kendo.grid.filter.applied", {
        durationMs: Date.now() - startMs,
        resultCount: resultCount
    });
}
```

### Widget Lifecycle Error Hook

```javascript
function onWidgetError(widgetName, errorCode, detail) {
    emitTelemetry("kendo.widget.error", {
        widget: widgetName,
        code: errorCode,
        detail: detail
    });
}
```

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Instrument one critical flow | Event emitted and queryable |
| L2 Delivery | Cover all major user journeys | Event catalog complete |
| L3 Hardening | Add thresholds and alert semantics | Regression detection is actionable |
| L4 Expert | Establish reusable observability standard | Cross-project telemetry contract published |

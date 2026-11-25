---
name: capacitor-observability
description: Use when a CapacitorJS app needs production-grade telemetry, crash diagnostics, traceable error correlation across web/native boundaries, and privacy-safe operational signals.
---

# Capacitor Observability

## Specialization

Establish a cross-layer observability model for CapacitorJS covering web telemetry, native diagnostics, crash reporting, and correlation IDs that connect user incidents to actionable engineering evidence.

## Trigger Conditions

- Production incidents cannot be diagnosed from existing logs.
- Native plugin failures are not visible in web analytics.
- Teams need privacy-safe telemetry to support SLOs and triage.

## Inputs

- Current logging and analytics stack.
- Critical user journeys and failure modes.
- Data classification constraints (PII, regulated data).
- Alerting and incident ownership model.

## Required Outputs

- Observability contract: events, logs, metrics, traces, and owners.
- Correlation strategy across web and native layers.
- Privacy-safe telemetry policy and redaction rules.
- Alert thresholds and runbook mappings.

## Deterministic Workflow

1. Identify critical journeys and high-impact failure modes.
2. Define canonical event taxonomy and correlation ID format.
3. Instrument web and native plugin boundaries consistently.
4. Apply redaction to sensitive payloads before export.
5. Map alerts to runbooks and ownership.
6. Validate end-to-end traceability with synthetic failures.

## Required Signals

- App startup success/failure and duration.
- Plugin invocation success/failure with normalized error codes.
- Network status transitions and retry outcomes.
- Crash fingerprints linked to release version and platform.
- User-visible failure events with recovery outcomes.

## Quality Gates

- Critical failures are traceable from user symptom to root-cause evidence.
- Telemetry excludes secrets, tokens, and prohibited identifiers.
- Alert thresholds are actionable and mapped to owners.
- Observability overhead stays within approved performance budget.

## Done Criteria

- Observability contract is implemented and documented.
- Correlated diagnostics are validated on iOS and Android.
- Privacy and redaction checks pass for all exported signals.

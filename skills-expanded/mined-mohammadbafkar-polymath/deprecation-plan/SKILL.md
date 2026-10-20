---
name: deprecation-plan
description: Plan a deprecation — two dates (warn + remove), telemetry-gated removal, comms cadence, exception path, code/header markers. The lifecycle plan, not the customer notice (write-sunset-notice).
---

# deprecation-plan

> Deprecation is a contract with a timeline, not a surprise. Set two dates, prove usage actually dropped before you pull it, and give people a way out.

## When to use

- A capability (API, endpoint, flag, feature, config) is going away and you need the staged plan.
- The user asks how to deprecate/sunset/retire something on a schedule.
- A workflow invokes `polymath-release:deprecation-plan` (see also the `deprecationToRemoval` / `sunsetCapability` workflows).

This is the *plan*. It is not the customer-facing notice copy (`polymath-communication:write-sunset-notice`), the consumer upgrade steps (`polymath-release:migration-guide`), or removing dead code (engineering).

## Inputs

- What is being deprecated and why; the replacement (or "no replacement").
- Who depends on it (internal/external; known consumers) and current usage signal.
- Constraints: contracts/SLAs, support windows, regulatory.

## Procedure

1. **Two dates** — *warn* (deprecation announced, still works) and *remove* (gone). State the support window between them and the rationale.
2. **Telemetry gate** — define the usage metric and the threshold the metric must be under before removal proceeds; removal is gated on data, not just the calendar.
3. **Markers** — how the deprecation is signalled in-product: `Deprecation`/`Sunset` HTTP headers, log warnings, SDK deprecation annotations, changelog.
4. **Comms cadence** — announce at warn, reminders at intervals, final notice before remove; route to the affected audience.
5. **Exception path** — how a blocked consumer requests an extension, and who approves.
6. **Migration** — link the upgrade path (`polymath-release:migration-guide`); deprecation without a migration path is just breakage.
7. Output the plan: both dates, the telemetry gate, markers, comms schedule, exception path, migration link.

## Quality bar

- Two explicit dates with a justified support window between them.
- Removal is gated on a usage threshold, not the date alone; the metric is named.
- An exception/extension path exists with an approver.
- A migration path is linked; "just stop using it" is not a migration path.

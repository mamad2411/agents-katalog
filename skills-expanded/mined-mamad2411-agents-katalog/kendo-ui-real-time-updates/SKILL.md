---
name: kendo-ui-real-time-updates
description: Use when Kendo UI data surfaces require real-time updates via push or streaming while preserving UI consistency, throughput, and user task continuity.
---

# Kendo UI Real-Time Updates

## Specialization

Implement and review real-time update patterns for Kendo UI components using push channels and incremental synchronization while preventing UI thrash, duplicate events, and inconsistent user state.

## Trigger Conditions

- Grid, chart, or dashboard data updates in near real-time.
- SignalR/websocket push integration is required.
- High-frequency updates degrade usability or performance.
- Concurrent edits and live updates can conflict.

## Scope Boundaries

In scope:

- Real-time update ingest and apply strategy.
- Throttling, debouncing, and coalescing update bursts.
- Merge conflict handling with active user edits.
- User-notice patterns for stale or superseded records.

Out of scope:

- Transport infrastructure provisioning.
- Backend event schema ownership.
- Non-Kendo event bus architecture.

## Inputs

- Update frequency and event payload structure.
- Target components and user interaction flows.
- Conflict policy (last-write, optimistic merge, review queue).
- Latency and throughput budgets.

## Required Outputs

- Update application model (full refresh vs patch).
- Throttle strategy and limits.
- Conflict handling contract during user edits.
- UI continuity rules (selection/focus retention).
- Resilience scenarios for disconnect/reconnect.

## Core Patterns

### Push to DataSource

```javascript
function onOrderUpdated(event) {
    var grid = $("#ordersGrid").data("kendoGrid");
    var ds = grid.dataSource;
    var existing = ds.get(event.id);

    if (existing) {
        existing.set("status", event.status);
        existing.set("total", event.total);
    } else {
        ds.add(event);
    }
}
```

### Coalesced Refresh

```javascript
// Batch rapid updates to avoid excessive rebinds.
var refreshPending = false;
function scheduleRefresh(grid) {
    if (refreshPending) return;
    refreshPending = true;
    setTimeout(function() {
        grid.refresh();
        refreshPending = false;
    }, 150);
}
```

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Add simple live update path | Updates appear correctly |
| L2 Delivery | Maintain UX stability under moderate event rate | Focus/selection retention verified |
| L3 Hardening | High-frequency stream resilience | Throttling and reconnect scenarios pass |
| L4 Expert | Reusable real-time Kendo pattern set | Conflict and continuity standards documented |

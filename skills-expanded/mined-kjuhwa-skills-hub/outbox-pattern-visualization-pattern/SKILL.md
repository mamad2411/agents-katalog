---

name: outbox-pattern-visualization-pattern
description: Three-lane visualization showing business transaction, outbox table, and relay publisher for outbox pattern demos
category: design
triggers:
  - outbox pattern visualization pattern
tags: [design, outbox, visualization, transaction]
version: 1.0.0
---

# outbox-pattern-visualization-pattern

Render the outbox flow as three horizontal swim-lanes stacked top-to-bottom: (1) Application/Business Transaction lane showing the domain write, (2) Outbox Table lane showing rows with status badges (PENDING → PROCESSING → PUBLISHED → FAILED), and (3) Message Broker lane showing published events. Each lane uses a distinct accent color (e.g. indigo for app, amber for outbox, emerald for broker) and connector arrows animate left-to-right to show the atomic DB write followed by the asynchronous relay step. Include a dashed vertical "transaction boundary" marker between lanes 1 and 2 to emphasize that the business insert and outbox insert commit together in one DB transaction.

For the outbox table lane, render actual row-like cards with columns for `id`, `aggregate_type`, `event_type`, `payload` (truncated), `status`, `retry_count`, and `created_at`. Highlight the row currently being polled by the relay with a pulsing border, and visually "lift" it out of the table when it transitions to the broker lane — this makes the poll-and-publish step concrete. Failed rows should shake briefly and display a retry counter badge.

Provide a control panel with: a "Commit Transaction" button (triggers lanes 1+2 together), a "Run Relay Poll" button (triggers lane 2→3), a toggle for "Simulate broker failure", and a speed slider. Show derived metrics in a sidebar: pending count, published count, failed count, average relay lag (ms from `created_at` to publish). This layout works whether the implementation is polling-based, transaction-log-tailing (CDC), or using Debezium — just swap the relay lane label.

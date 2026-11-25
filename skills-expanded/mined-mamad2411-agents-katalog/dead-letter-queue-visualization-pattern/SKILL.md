---

name: dead-letter-queue-visualization-pattern
description: Visual patterns for surfacing DLQ message flow, failure reasons, and replay decisions in triage UIs
category: design
triggers:
  - dead letter queue visualization pattern
tags: [design, dead, letter, queue, visualization]
version: 1.0.0
---

# dead-letter-queue-visualization-pattern

Dead-letter-queue UIs must make three things instantly legible: where a message came from (source topic/queue + original consumer group), why it failed (exception class, retry count, timestamp of last attempt), and what operators can do next (replay, edit-and-replay, discard, quarantine). The canonical layout is a three-pane console: left pane lists DLQ entries grouped by failure signature (hashed stack trace or error code) with counts, middle pane shows the selected message's headers/payload with a diff view against the original schema, and right pane exposes action buttons gated by RBAC. Group-by-signature beats chronological listing because DLQs typically contain bursts of the same underlying bug — showing 10,000 identical failures as one row with a count prevents operator fatigue.

For flow visualization, render the message lifecycle as a directed graph: Source → Consumer → Retry(n) → DLQ → Replay Target. Use color intensity to encode volume (number of messages on each edge) and animate only edges with recent activity to avoid a busy-but-meaningless display. Annotate each retry node with the backoff delay used and the exception raised — this turns an abstract retry policy into something operators can audit. For autopsy/report views, pair a timeline chart (messages entering DLQ per minute) with a Pareto chart of failure reasons; the 80/20 rule almost always applies, and the top 2-3 error signatures drive most remediation work.

Always expose the poison-pill detection signal visually: when a single message fails N consecutive replay attempts, flag it distinctly (red border, skull icon, or a dedicated "quarantine" lane) so it cannot be accidentally replayed into an infinite loop. The UI should refuse a replay action on quarantined messages without an explicit override confirmation, and log the override actor for audit.

---

name: event-sourcing-visualization-pattern
description: Render append-only event logs alongside derived state projections with replay scrubber controls
category: design
triggers:
  - event sourcing visualization pattern
tags: [design, event, sourcing, visualization]
version: 1.0.0
---

# event-sourcing-visualization-pattern

Event-sourcing UIs require a dual-pane layout: an immutable event stream on one side (chronological log with sequence numbers, event type badges, aggregate IDs, and payload diffs) and the materialized state on the other (current aggregate snapshot rebuilt from folded events). The log pane should use color-coded event types (e.g., green for Created, blue for Updated, red for Deleted/Compensated) and surface metadata like causationId/correlationId on hover. The state pane animates field-level changes when a new event is applied so users can see the cause-effect link.

A scrubber/timeline control is the centerpiece — users drag a playhead across the event log to "time-travel" to any point in history, and the projection pane re-folds events from offset 0 to the cursor position. Apps like time-travel-tree extend this with branching: forking the timeline at any event creates a parallel projection lane, visualized as a git-style DAG. Always show the fold direction (left-to-right replay) and current offset/total events counter.

For CQRS variants (cqrs-projection-lab), render multiple projection panes side-by-side fed from the same event stream, each with its own lag indicator and rebuild button. Highlight projection drift visually when handlers fall behind the write model, and animate event delivery as flowing tokens from log → projector → read model.

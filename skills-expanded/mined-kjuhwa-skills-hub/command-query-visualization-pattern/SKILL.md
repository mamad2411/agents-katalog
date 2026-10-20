---

name: command-query-visualization-pattern
description: Split-pane UI that visually separates command write paths from query read paths in CQRS systems
category: design
triggers:
  - command query visualization pattern
tags: [design, command, query, visualization, cqrs]
version: 1.0.0
---

# command-query-visualization-pattern

For command-query visualization, use a horizontally or vertically split canvas where the left/top half renders the command side (write model, aggregate, event store) and the right/bottom half renders the query side (read model, projections, denormalized views). Draw a prominent vertical divider labeled with the segregation boundary, and animate commands as colored pulses (e.g., red/orange) flowing left-to-right only through the write lane, while queries appear as distinct pulses (e.g., blue/green) that never cross into the write lane. Event propagation from write to read should be rendered as a dashed arrow crossing the divider with a visible delay indicator to reinforce eventual consistency.

Each node should expose its current state badge: commands show "pending/validating/applied/rejected", queries show "cache-hit/projecting/stale", and projections show lag in ms or event-count behind. Use consistent iconography — a gear or pen for commands, a magnifying glass or eye for queries, a funnel for projectors — so users build intuition across the three apps. Hover tooltips should reveal the exact command/query payload, the target aggregate ID, and the resulting event(s) emitted, letting learners trace cause-and-effect without losing the system-wide view.

Provide a timeline scrubber or step controller beneath the canvas so users can pause, rewind, and replay the flow. When scrubbed, both panes must stay synchronized to the same logical timestamp, and the read model should visibly "catch up" frame-by-frame as events are replayed into projectors. This makes the otherwise-invisible gap between write commit and read availability tangible.

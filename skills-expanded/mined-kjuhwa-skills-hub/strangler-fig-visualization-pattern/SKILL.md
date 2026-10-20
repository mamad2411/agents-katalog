---

name: strangler-fig-visualization-pattern
description: Side-by-side legacy/new system visualization with traffic routing overlay for strangler-fig migration apps
category: design
triggers:
  - strangler fig visualization pattern
tags: [design, strangler, fig, visualization, migration]
version: 1.0.0
---

# strangler-fig-visualization-pattern

Strangler-fig visualizations share a three-zone layout: a **legacy monolith panel** (left, typically rendered in muted/grey tones to signal deprecation), a **new service panel** (right, in vibrant/green tones to signal growth), and a **routing facade layer** (top or center) that shows which endpoints/routes are currently proxied to which side. Each endpoint or feature is rendered as a node with a migration-state badge: `legacy-only`, `shadowed`, `canary`, `migrated`, `retired`. Color transitions (grey → amber → green) communicate progress without requiring a legend.

The routing facade should animate request flows as particles or arrows traveling from the client through the facade to either the legacy or new backend. Percentage splits (e.g., 10% canary → new, 90% → legacy) are shown as weighted edge thickness or as a split-flow animation where particle counts match the routing ratio. Hovering a node reveals its migration metadata (dependencies, call volume, last-migrated date, rollback window).

A **vine/ivy metaphor overlay** (literal in vine-grower, abstracted in migration-simulator/route-router) works well: new-service growth visually "wraps" the legacy node until the legacy node shrinks and disappears on retirement. Timeline scrubbers let users replay migration history; a "kill legacy" control simulates the final cutover to verify no traffic still routes to the retired path.

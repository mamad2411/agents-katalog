---

name: cqrs-visualization-pattern
description: Split-panel visualization showing command-side writes and query-side reads as distinct, independently-scaling lanes with a projection bridge between them.
category: design
triggers:
  - cqrs visualization pattern
tags: [design, cqrs, visualization]
version: 1.0.0
---

# cqrs-visualization-pattern

CQRS visualizations should present the write model and read model as two visually separated lanes rather than a single pipeline. The left lane hosts the command bus, aggregate/write store, and event log; the right lane hosts one or more denormalized read models (materialized views, caches, search indexes). A central "projection bridge" animates how events flow from the write side into each read model, with per-projector lag badges (events behind, last-applied offset, replay cursor) so the eventual-consistency gap becomes legible instead of hidden.

Use distinct visual vocabularies per side: commands render as intent arrows with validation outcomes (accepted/rejected), while queries render as read-through lookups that never mutate state. Color-code by responsibility — commands in warm tones, projections in neutral, queries in cool tones — and reserve a dedicated "replay" overlay that re-drives historical events through projectors at adjustable speed. Expose controls for pausing a single projector, snapshotting a read model, and forcing a rebuild so viewers can see how decoupling affects availability on each side independently.

Always surface the three timescales that define CQRS behavior: command acceptance latency, event-to-projection lag, and query response time. Plot them on a shared timeline so the viewer can correlate a write spike with the resulting projection backlog and the read-side staleness window, which is the single most important intuition CQRS teaches.

---

name: crdt-visualization-pattern
description: Side-by-side replica panels with convergence indicators for visualizing CRDT state synchronization
category: design
triggers:
  - crdt visualization pattern
tags: [design, crdt, visualization]
version: 1.0.0
---

# crdt-visualization-pattern

CRDT visualizations should render two or more replica panels side-by-side, each showing the replica's current local state (counter value, document text, or graph nodes/edges) along with a vector clock or operation log. A central "network" zone between panels visualizes in-flight operations as animated tokens, with controls to pause, reorder, duplicate, or drop messages — this is essential for demonstrating the commutative/idempotent/associative (CIA) properties that define CRDTs. Include a prominent convergence indicator (e.g., a checkmark or colored badge) that turns green only when all replicas report byte-equal state hashes.

For counter-sync visualizations, show per-replica increment histories and the merged sum; for LWW editors, display timestamp tags on each character/field and highlight which writes "won"; for OR-Set graphs, render unique tags (UUIDs) per element-add with strikethrough on tombstoned entries to make add-wins semantics visible. Always expose a "step" mode alongside "auto-play" so users can manually trigger each merge and observe state deltas.

Include a timeline/event-log panel at the bottom showing the global operation order as perceived by each replica — this makes divergence obvious during partitions and convergence dramatic upon reconnection. Color-code operations by originating replica to track causality visually.
